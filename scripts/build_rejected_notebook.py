"""Disclose the rejected experiment on Kaggle without executing or submitting its agent."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "kaggle_notebooks/exp20260908-01"
    folder.mkdir(parents=True, exist_ok=True)
    candidate = (ROOT / "agents/candidates/exp20260908_01.py").read_text()
    parent = (ROOT / "agents/champion/ahmed_v23.py").read_text()
    report = json.loads((ROOT / "experiments/results/EXP-20260908-01-screen.json").read_text())
    expected = "7a3c12b2ec8efe8fac107ce984e5951e92e8595dced39fcd787536cbcc887607"
    if hashlib.sha256(candidate.encode()).hexdigest() != expected:
        raise ValueError("Rejected candidate changed after measurement")
    files = {"rejected_candidate.py": candidate, "parent.py": parent,
             "screen-summary.json": json.dumps({"decision": "NO-GO", "candidate_sha256": expected,
                 "engine_version": report["engine_version"], "seed_start": report["seed_start"],
                 "seed_count": report["seed_count"], "seat_swapped": True,
                 "summary": report["summary"], "candidate_96_seed_run": False,
                 "competition_submitted": False}, indent=2)}
    text = """# EXP-20260908-01: Rejected Funding-Trigger Experiment

**NO-GO. This candidate was not submitted to the competition.**

The only policy change adds an off-boundary budget check when estimated current
purchases exceed cash. It extends the unmodified public Ahmed v23 research parent.

The parent was selected from 1,008 paired-screen games across six public Python
policies plus our old baseline. In a separate 96-seed, both-seat finalist test,
it beat Thomas v2 134-58 (mean margin +430.72). Native ARA-V2 was not reproduced
on our macOS host; the claim is restricted to the documented Python panel.

Our incremental candidate then lost **all 48 games** in its 24-fresh-seed,
both-seat test against the parent. Mean margin -6,432.19; median -4,358;
p10 -14,800.1. Zero unfilled requested units did not imply economic improvement.
The candidate's 96-seed gate was deliberately NOT run. No quota was consumed.

The cell below only writes source and measured-result files and checks a hash.
It does not import either agent, run a game, build a submission archive, or call
the competition submission API. These are research disclosures, not cloud
runtime validation or permission to upload this rejected candidate.

## Provenance

- Parent: https://www.kaggle.com/code/ahmedberatozer/notebook865729c24e (Notebook v3).
- Parent source SHA: 6eb728a40cc55f7e497add6ea2946ce38b0389c24531a208219d48587435838e.
- Upstream credits to Thomas Tschinkel, yhay81 and tetsutani are retained in source.
- The full Apache-2.0 license is preserved in both source files.
- Our only modification is explicitly marked EXP-20260908-01 by whzy3185.
- Research, raw result tables and tests: https://github.com/whzy3185/kagriculture/tree/research/round1-audit-20260907
"""
    code = "from pathlib import Path\nimport hashlib\nFILES = " + repr(files) + "\n"
    code += "for name, source in FILES.items():\n    Path(name).write_text(source)\n"
    code += "assert hashlib.sha256(Path('rejected_candidate.py').read_bytes()).hexdigest() == " + repr(expected) + "\n"
    code += "print('NO-GO: source disclosure only; no competition submission.')\n"
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {
        "name": "python3", "display_name": "Python 3", "language": "python"}}, "cells": [
        {"cell_type": "markdown", "id": "audit", "metadata": {}, "source": text},
        {"cell_type": "code", "id": "disclosure", "metadata": {}, "execution_count": None, "outputs": [], "source": code}]}
    (folder / "notebook.ipynb").write_text(json.dumps(notebook, indent=2) + "\n")
    metadata = {"id": "muelsyse111/kaggriculture-exp20260908-01-funding-audit",
                "title": "Kaggriculture EXP20260908 01 Funding Audit", "code_file": "notebook.ipynb",
                "language": "python", "kernel_type": "notebook", "is_private": False,
                "enable_gpu": False, "enable_internet": False, "dataset_sources": [],
                "competition_sources": ["kaggriculture"], "kernel_sources": []}
    (folder / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("Built public research disclosure, not a competition submission")


if __name__ == "__main__":
    main()
