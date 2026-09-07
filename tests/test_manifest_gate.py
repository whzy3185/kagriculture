from copy import deepcopy
import pytest
from scripts.submit_manifest import ROOT, digest, evaluation_gate, load_evidence


def report():
    rows = [{"opponent": op, "seed": seed, "seat": seat, "valid_terminal": True,
             "statuses": ["DONE", "DONE"], "calls": 719, "runtime_max": .01, "faults": {}}
            for op in ("main", "shape_shop_v11") for seed in (1, 2) for seat in (0, 1)]
    return {"agent_sha": "test", "engine_version": "1.32.7", "disabled": [],
            "evaluator_sha": digest(ROOT / "scripts/experiment_eval.py"),
            "seed_count": 2, "seed_start": 1, "seat_swapped": True, "rows": rows,
            "summary": {"main": {"points": 1.}, "shape_shop_v11": {"points": 0.}}}


def test_complete_control_evidence_passes_local_baseline_check():
    assert evaluation_gate(report(), "test", 2) == {1, 2}


def test_missing_seat_is_rejected():
    r = report()
    r["rows"].pop()
    with pytest.raises(ValueError):
        evaluation_gate(r, "test", 2)


def test_faults_are_not_dropped():
    r = report()
    r["rows"][0]["faults"] = {"unit_noops": 1}
    with pytest.raises(ValueError):
        evaluation_gate(r, "test", 2)


def test_wrong_agent_is_rejected():
    with pytest.raises(ValueError):
        evaluation_gate(report(), "wrong", 2)


def test_evidence_cannot_escape_repository():
    with pytest.raises(ValueError):
        load_evidence({"path": "../outside.json", "sha256": "wrong"})
