"""Freeze the rejected daily result and champion provenance, never submit."""

import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(path):
    return {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}


def main():
    exp = "EXP-20260908-01"
    candidate = ROOT / "agents/candidates/exp20260908_01.py"
    parent = ROOT / "agents/champion/ahmed_v23.py"
    screen_path = ROOT / f"experiments/results/{exp}-screen.json"
    finalist_path = ROOT / "experiments/results/PUBLIC-20260908-finalists.json"
    screen, finalists = (json.loads(p.read_text()) for p in (screen_path, finalist_path))
    result = screen["summary"]["exp20260908_01 vs ahmed_v23"]
    if result["games"] != 48 or result["wins"] != 0 or not result["valid"]:
        raise ValueError("Not the documented complete rejection result")
    if screen["source_hashes"] != {"exp20260908_01": sha(candidate), "ahmed_v23": sha(parent)}:
        raise ValueError("Measured source changed")
    git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    committed = subprocess.check_output(["git", "show", git_sha + ":agents/candidates/exp20260908_01.py"], cwd=ROOT)
    if hashlib.sha256(committed).hexdigest() != sha(candidate):
        raise ValueError("Candidate not committed identically")
    junit = ROOT / f"experiments/results/{exp}-tests.xml"
    suites = ET.parse(junit).getroot().findall("testsuite")
    count = sum(int(s.attrib["tests"]) for s in suites)
    if count < 51 or any(int(s.attrib.get(k, 0)) for s in suites for k in ("errors", "failures", "skipped")):
        raise ValueError("Tests not verified")
    entry = {"exp_id": exp, "date": "2026-09-08", "decision": "NO-GO", "champion_decision": "KEEP_PARENT",
             "parent": "ahmed_v23", "parent_sha256": sha(parent), "candidate_sha256": sha(candidate),
             "local_source_git_sha": git_sha, "git_sha_kind": "local checkout provenance",
             "tests": count, "test_evidence": evidence(junit), "screen_evidence": evidence(screen_path),
             "screen": result, "candidate_96_seed": "NOT_RUN_FAILED_SCREEN",
             "submission_ref": None, "artifact_sha": None, "previous_active_submission": 56072267,
             "publication_ref": "muelsyse111/kaggriculture-exp20260908-01-funding-audit",
             "publication_scope": "Source disclosure only; no agent execution or competition submission",
             "live_check": {"checked_at": "2026-09-08T10:07:54.468381+00:00", "submissions_today": 0,
                            "remaining_quota": 5, "public_notebook_version": 1, "public_notebook_status": "COMPLETE"}}
    selection = {"date": "2026-09-08", "status": "RESEARCH_CHAMPION_ONLY", "name": "ahmed_v23",
                 "source_url": "https://www.kaggle.com/code/ahmedberatozer/notebook865729c24e",
                 "author": "Ahmed Berat Ozer", "notebook_version": 3, "source_date": "2026-09-07T22:16:47Z",
                 "source_file": str(parent.relative_to(ROOT)), "code_sha256": sha(parent),
                 "local_source_git_sha": git_sha, "engine_version": "1.32.7", "engine_sha256": finalists["engine_sha"],
                 "selection_seeds": {"start": 2026090800, "count": 24, "both_seats": True, "panel_games": 1008},
                 "finalist_seeds": {"start": 2026090900, "count": 96, "both_seats": True},
                 "finalist_result": finalists["summary"]["ahmed_v23 vs thomas_v2"],
                 "evidence": evidence(finalist_path), "production_approval": False,
                 "limitations": ["Portable Python panel only; native ARA-V2 not reproduced.",
                                 "Related source families are not independent population samples.",
                                 "Health flags remain; no unchanged-parent competition upload."]}
    registry = ROOT / "experiments/registry.jsonl"
    if registry.exists() and any(json.loads(line).get("exp_id") == exp for line in registry.read_text().splitlines()):
        raise ValueError("Experiment already recorded")
    with registry.open("a") as handle:
        handle.write(json.dumps(entry) + "\n")
    manifest = {**entry, "purpose": "rejected_daily_experiment", "execute_allowed": False}
    for path, data in ((ROOT / "agents/champion/selection.json", selection),
                       (ROOT / f"submissions/manifests/{exp}.json", manifest)):
        with path.open("x") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
    print(json.dumps({"exp_id": exp, "decision": "NO-GO", "local_source_git_sha": git_sha, "tests": count}))


if __name__ == "__main__":
    main()
