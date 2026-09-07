"""Verify downloaded EXP-006 outputs before recording submission evidence."""

import hashlib
import json
import math
from pathlib import Path
import tarfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_count(path, minimum):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    count = sum(int(s.attrib["tests"]) for s in suites)
    if count < minimum or any(int(s.attrib.get(k, 0)) for s in suites
                              for k in ("errors", "failures", "skipped")):
        raise ValueError("Incomplete or failed test suite")
    if sum(len(s.findall("testcase")) for s in suites) != count:
        raise ValueError("JUnit count mismatch")
    return count


def verify(root=ROOT):
    output = root / "kaggle_notebooks/exp006-validation/output"
    agent = root / "agents/candidates/exp006_independent.py"
    artifact = root / "submissions/artifacts/EXP-006/submission.tar.gz"
    report = json.loads((output / "cloud-runtime.json").read_text())
    receipt = json.loads((output / "runtime-verification.json").read_text())
    if sha(artifact) != sha(output / "submission.tar.gz"):
        raise ValueError("Local/cloud archives differ")
    with tarfile.open(output / "submission.tar.gz") as tar:
        expected_files = {"main.py": agent,
                          "LICENSE.txt": root / "agents/candidates/EXP006-LICENSE.txt",
                          "NOTICE.txt": root / "agents/candidates/EXP006-NOTICE.txt"}
        if tar.getnames() != list(expected_files) or not all(m.isfile() for m in tar):
            raise ValueError("Unexpected archive members")
        for name, path in expected_files.items():
            if tar.extractfile(name).read() != path.read_bytes():
                raise ValueError("Archive content mismatch: " + name)
    if (report["agent_sha"] != sha(agent) or report["engine_version"] != "1.32.7"
            or report["evaluator_sha"] != sha(root / "scripts/experiment_eval.py")
            or report["disabled"] or report["seat_swapped"] is not True
            or report["seed_start"] != 4001 or report["seed_count"] != 2):
        raise ValueError("Cloud identity mismatch")
    if report["opponent_hashes"] != {"main": sha(agent), "legacy_parent": sha(root / "main.py")}:
        raise ValueError("Cloud opponents differ")
    expected = {(op, seed, seat) for op in ("main", "legacy_parent")
                for seed in (4001, 4002) for seat in (0, 1)}
    rows = report["rows"]
    actual = [(r["opponent"], r["seed"], r["seat"]) for r in rows]
    if set(actual) != expected or len(actual) != len(expected):
        raise ValueError("Missing/duplicate cloud games")
    for row in rows:
        if (not row["valid_terminal"] or row["statuses"] != ["DONE", "DONE"]
                or row["calls"] != 719 or any(row["faults"].values())
                or not math.isfinite(row["runtime_max"]) or not 0 <= row["runtime_max"] < .5):
            raise ValueError("Cloud health failure")
    verified = {"exp_id": "EXP-006", "agent_sha": sha(agent), "artifact_sha": sha(artifact),
                "engine_version": "1.32.7", "episodes": len(rows), "faults": 0,
                "tests": test_count(output / "cloud-tests.xml", 11),
                "runtime_max": max(r["runtime_max"] for r in rows)}
    if any(receipt.get(k) != v for k, v in verified.items()):
        raise ValueError("Receipt disagrees with raw evidence")
    return verified


def main():
    verified = verify()
    output = ROOT / "kaggle_notebooks/exp006-validation/output"
    results = ROOT / "experiments/results"
    local_xml = results / "EXP-006-local-tests.xml"
    local = {"return_code": 0, "tests": test_count(local_xml, 26),
             "agent_sha": verified["agent_sha"], "junit_sha256": sha(local_xml),
             "verification": "JUnit contains no errors, failures or skipped tests"}
    # Preserve the raw outputs; the receipt alone is not independent evidence.
    for name in ("cloud-runtime.json", "cloud-tests.xml", "runtime-verification.json"):
        destination = results / ("EXP-006-" + name)
        destination.write_bytes((output / name).read_bytes())
    verified["raw_evidence"] = {name: sha(output / name) for name in
                                ("cloud-runtime.json", "cloud-tests.xml", "runtime-verification.json")}
    verified["publication_verified"] = False
    for name, data in (("cloud-verified", verified), ("local-tests", local)):
        (results / ("EXP-006-" + name + ".json")).write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(verified, indent=2))


if __name__ == "__main__":
    main()
