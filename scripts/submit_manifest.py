"""Fail-closed first-baseline submission, using immutable evidence and live checks."""

import argparse
import contextlib
import fcntl
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_evidence(ref):
    path = (ROOT / ref["path"]).resolve()
    if not path.is_relative_to(ROOT) or digest(path) != ref["sha256"]:
        raise ValueError("Evidence path/hash mismatch")
    return json.loads(path.read_text())


def evaluation_gate(report, agent_sha, minimum_seeds):
    if report["agent_sha"] != agent_sha or report["engine_version"] != "1.32.7" or report["disabled"]:
        raise ValueError("Evaluation identity mismatch")
    if report["evaluator_sha"] != digest(ROOT / "scripts/experiment_eval.py"):
        raise ValueError("Evaluator changed after measurement")
    if report["seed_count"] < minimum_seeds or report["seat_swapped"] is not True:
        raise ValueError("Incomplete seed suite")
    rows = report["rows"]
    opponents = set(report["summary"])
    expected = {(op, seed, seat) for op in opponents
                for seed in range(report["seed_start"], report["seed_start"] + report["seed_count"])
                for seat in (0, 1)}
    actual = [(r["opponent"], r["seed"], r["seat"]) for r in rows]
    if set(actual) != expected or len(actual) != len(expected):
        raise ValueError("Missing or duplicated games")
    for row in rows:
        if not row["valid_terminal"] or row["statuses"] != ["DONE", "DONE"] or row["calls"] != 719:
            raise ValueError("Incomplete/failed episode")
        if any(value != 0 for value in row["faults"].values()):
            raise ValueError("Action/market/runtime health failure")
        if not math.isfinite(row["runtime_max"]) or row["runtime_max"] >= .5:
            raise ValueError("Runtime headroom insufficient")
    if report["summary"]["main"]["points"] < .75:
        raise ValueError("No improvement over declared legacy parent")
    # The strong-reference losses remain in evidence. This is NOT champion approval.
    if "shape_shop_v11" not in opponents:
        raise ValueError("Strong-reference negative control missing")
    return {r["seed"] for r in rows}


def validate_local(manifest):
    if manifest["purpose"] != "first_baseline_calibration" or manifest["parent_submission"] is not None:
        raise ValueError("This gate is restricted to a documented first baseline")
    artifact = (ROOT / manifest["artifact_file"]).resolve()
    if not artifact.is_relative_to(ROOT) or artifact.stat().st_size > 100 * 1024 * 1024:
        raise ValueError("Artifact path/size invalid")
    if digest(artifact) != manifest["artifact_sha"]:
        raise ValueError("Artifact hash mismatch")
    with tarfile.open(artifact) as tar:
        if tar.getnames() != ["main.py", "LICENSE.txt", "NOTICE.txt"]:
            raise ValueError("Unexpected package members")
        if not all(member.isfile() for member in tar):
            raise ValueError("Package contains nonregular members")
        agent_bytes = tar.extractfile("main.py").read()
    agent_sha = hashlib.sha256(agent_bytes).hexdigest()
    if agent_sha != manifest["agent_sha"]:
        raise ValueError("Packaged agent identity mismatch")
    committed = subprocess.check_output(["git", "show", manifest["git_sha"] + ":" + manifest["source_file"]], cwd=ROOT)
    if hashlib.sha256(committed).hexdigest() != agent_sha:
        raise ValueError("Git source and artifact differ")
    if digest(ROOT / "main.py") != manifest["parent_agent_sha"]:
        raise ValueError("Legacy parent changed")
    tests = load_evidence(manifest["tests"])
    if tests["return_code"] != 0 or tests["tests"] < 21 or tests["agent_sha"] != agent_sha:
        raise ValueError("Tests not verified on candidate")
    development = load_evidence(manifest["development"])
    holdout = load_evidence(manifest["holdout"])
    if evaluation_gate(development, agent_sha, 16) & evaluation_gate(holdout, agent_sha, 32):
        raise ValueError("Development/holdout overlap")
    for report in (development, holdout):
        if report["opponent_hashes"]["main"] != manifest["parent_agent_sha"]:
            raise ValueError("Evaluated parent mismatch")
    runtime = load_evidence(manifest["kaggle_runtime"])
    if (runtime["agent_sha"] != agent_sha or runtime["artifact_sha"] != manifest["artifact_sha"]
            or runtime["faults"] != 0 or runtime["episodes"] < 8 or runtime["tests"] < 11
            or runtime["runtime_max"] >= .5 or runtime["engine_version"] != "1.32.7"):
        raise ValueError("Kaggle runtime evidence mismatch")
    if not manifest.get("limitations") or manifest["approval"] != "BASELINE_CALIBRATION_ONLY":
        raise ValueError("Missing calibrated approval/limitations")
    return artifact


def submit(args):
    manifest = json.loads(args.manifest.read_text())
    try:
        artifact = validate_local(manifest)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print("NO-GO:", type(error).__name__, str(error)[:180])
        return 3
    from kaggle import api
    from kagglesdk.kernels.types.kernels_api_service import ApiGetKernelRequest
    if api.config_values.get("username") != "muelsyse111":
        raise ValueError("Unexpected authenticated account")
    status = api.kernels_status(manifest["kernel_ref"]).to_dict()["status"]
    if status != "COMPLETE":
        raise ValueError("Kaggle Notebook has not completed")
    with api.build_kaggle_client() as client:
        request = ApiGetKernelRequest()
        request.user_name, request.kernel_slug = manifest["kernel_ref"].split("/")
        kernel = client.kernels.kernels_api_client.get_kernel(request)
    if (kernel.metadata.is_private or kernel.metadata.current_version_number != manifest["kernel_version"]
            or "kaggriculture" not in kernel.metadata.competition_data_sources):
        raise ValueError("Competition-associated code sharing/version not verified")
    history = api.competition_submissions("kaggriculture", page_size=100) or []
    if history:
        raise ValueError("Not an empty first-baseline history; review existing submissions")
    if api.competition_get_submission_limits("kaggriculture").num_allowed_now < 1:
        raise ValueError("No quota")
    ledger = ROOT / "submissions/ledger.jsonl"
    previous = [json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
    latest = {row["artifact_sha"]: row for row in previous}
    if any(r.get("artifact_sha") == manifest["artifact_sha"] or r["status"] in {"DISPATCHING", "PENDING", "SUBMITTED"} for r in latest.values()):
        raise ValueError("Duplicate artifact or unresolved dispatch")
    print("PASS: baseline evidence, package, source, sharing, runtime, history and quota")
    if not args.execute:
        print("Dry run only")
        return 0
    entry = {"date": datetime.now(timezone.utc).isoformat(), "exp_id": manifest["exp_id"],
             "artifact_sha": manifest["artifact_sha"], "git_sha": manifest["git_sha"], "status": "DISPATCHING"}
    with ledger.open("a") as handle:
        handle.write(json.dumps(entry) + "\n")
        handle.flush()
    # Never emit signed upload URLs or raw uploader diagnostics.
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = api.competition_submit(str(artifact), manifest["submission_message"], "kaggriculture", quiet=True)
    except Exception as error:
        print("DISPATCH_UNCERTAIN:", type(error).__name__, "Reconcile history before retrying.")
        return 4
    if not result.ref:
        raise RuntimeError("Submission outcome uncertain; reconcile dispatch before retry")
    entry.update(status="SUBMITTED", submission_ref=result.ref)
    with ledger.open("a") as handle:
        handle.write(json.dumps(entry) + "\n")
    print(json.dumps(entry))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        return submit(args)
    with (ROOT / "submissions/.submit.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("NO-GO: another submission process holds the lock")
            return 3
        return submit(args)


if __name__ == "__main__":
    raise SystemExit(main())
