"""Bind verified EXP-006 evidence to its public kernel and frozen source."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from submit_manifest import ROOT, digest, validate_local
from verify_cloud_evidence import verify


def main():
    from kaggle import api
    from kagglesdk.kernels.types.kernels_api_service import ApiGetKernelRequest

    runtime = verify()
    ref = "muelsyse111/kaggriculture-exp006-independent-baseline-audit"
    status = api.kernels_status(ref).to_dict()["status"]
    request = ApiGetKernelRequest()
    request.user_name, request.kernel_slug = ref.split("/")
    with api.build_kaggle_client() as client:
        metadata = client.kernels.kernels_api_client.get_kernel(request).metadata
    if (status != "COMPLETE" or metadata.is_private or metadata.current_version_number != 2
            or "kaggriculture" not in metadata.competition_data_sources):
        raise ValueError("Public kernel v2 is not complete and competition-associated")
    source_git = "b968c37227404c84349ee380b5bd106c57e7b594"
    remote_git = "298d2074be9be6d8ecf3f00ee45dbfd625993612"
    tree = subprocess.check_output(["git", "rev-parse", source_git + "^{tree}"], cwd=ROOT, text=True).strip()
    if tree != "1fb2ef632ff0d664d4cf618e62539a16f955af90":
        raise ValueError("Frozen source tree changed")
    def evidence(name):
        path = "experiments/results/EXP-006-" + name + ".json"
        return {"path": path, "sha256": digest(ROOT / path)}
    development = json.loads((ROOT / "experiments/results/EXP-006-development-full.json").read_text())
    holdout = json.loads((ROOT / "experiments/results/EXP-006-holdout.json").read_text())
    manifest = {
        "exp_id": "EXP-006", "date": datetime.now(timezone.utc).isoformat(),
        "purpose": "first_baseline_calibration", "approval": "BASELINE_CALIBRATION_ONLY",
        "hypothesis": "Independent feasible crop control improves legacy paired points; calibrate online only.",
        "parent_submission": None, "parent_score": None,
        "parent_agent_sha": digest(ROOT / "main.py"),
        "git_sha": source_git, "github_git_sha": remote_git, "source_tree_sha": tree,
        "source_file": "agents/candidates/exp006_independent.py",
        "artifact_file": "submissions/artifacts/EXP-006/submission.tar.gz",
        "artifact_sha": runtime["artifact_sha"], "agent_sha": runtime["agent_sha"],
        "tests": evidence("local-tests"), "development": evidence("development-full"),
        "holdout": evidence("holdout"), "kaggle_runtime": evidence("cloud-verified"),
        "kernel_ref": ref, "kernel_version": 2,
        "publication": {"is_private": False, "status": status,
                        "competition_sources": list(metadata.competition_data_sources),
                        "authorization": "User authorized Kaggle submission and GitHub synchronization after explicit public-release question."},
        "seed_suite": {"development": [201, 216], "holdout": [3001, 3032], "seat_swapped": True},
        "local_games": len(development["rows"]), "holdout_games": len(holdout["rows"]),
        "local_win_rate_by_opponent": {k: v["wins"] / v["games"] for k, v in development["summary"].items()},
        "holdout_win_rate_by_opponent": {k: v["wins"] / v["games"] for k, v in holdout["summary"].items()},
        "runtime": {"cloud_max_seconds": runtime["runtime_max"]}, "expected_delta": None,
        "limitations": ["Shape v11 holdout: 0/64 wins; no champion promotion.",
                        "Ablations improved cash margins, not win/loss classifications.",
                        "No parent online rating; first submission is calibration only.",
                        "Local and GitHub commits differ; exact source tree identity verified."],
        "submission_message": "EXP-006 first-baseline parent=none git=298d2074 local=b968c37; independent crop calibration",
    }
    validate_local(manifest)
    path = ROOT / "submissions/manifests/EXP-006.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError("Manifest already exists; do not overwrite submission provenance")
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("Prepared", path.relative_to(ROOT), "with verified public kernel v2")


if __name__ == "__main__":
    main()
