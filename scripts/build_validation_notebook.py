"""Build a credential-free notebook and deterministic baseline submission package."""

import ast
import hashlib
import io
import gzip
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "kaggle_notebooks/exp006-validation"
    folder.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "agents/candidates/exp006_independent.py").read_text()
    ast.parse(source)
    files = {
        "main.py": source,
        "agents/candidates/exp006_independent.py": source,
        "legacy_parent.py": (ROOT / "main.py").read_text(),
        "scripts/experiment_eval.py": (ROOT / "scripts/experiment_eval.py").read_text(),
        "tests/test_independent_controller.py": (ROOT / "tests/test_independent_controller.py").read_text(),
        "LICENSE.txt": (ROOT / "agents/candidates/EXP006-LICENSE.txt").read_text(),
        "NOTICE.txt": (ROOT / "agents/candidates/EXP006-NOTICE.txt").read_text(),
    }
    digest = hashlib.sha256(source.encode()).hexdigest()
    setup = '''import importlib.metadata, subprocess, sys
if importlib.metadata.version("kaggle-environments") != "1.32.7":
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kaggle-environments==1.32.7"], check=True)
import hashlib, json, pathlib
from kaggle_environments import __version__
assert __version__ == "1.32.7"
'''
    materialize = "FILES = " + repr(files) + "\nEXPECTED_AGENT_SHA = " + repr(digest) + '''
for name, source in FILES.items():
    path = pathlib.Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source)
assert hashlib.sha256(pathlib.Path("main.py").read_bytes()).hexdigest() == EXPECTED_AGENT_SHA
print("Candidate source hash verified:", EXPECTED_AGENT_SHA)
'''
    tests = '''import xml.etree.ElementTree as ET
run = subprocess.run([sys.executable, "-m", "pytest", "tests/test_independent_controller.py", "-q", "--junitxml=cloud-tests.xml"], capture_output=True, text=True)
print(run.stdout)
assert run.returncode == 0, "Cloud unit/contract tests failed"
suites = ET.parse("cloud-tests.xml").getroot().findall("testsuite")
test_count = sum(int(s.attrib["tests"]) for s in suites)
assert test_count >= 11
'''
    games = '''run = subprocess.run([sys.executable, "scripts/experiment_eval.py", "--agent", "main.py", "--opponents", "legacy_parent.py", "main.py", "--seed-start", "4001", "--seeds", "2", "--output", "cloud-runtime.json"], capture_output=True, text=True)
assert run.returncode == 0, "Cloud evaluation failed; inspect cloud-runtime.progress.jsonl"
report = json.loads(pathlib.Path("cloud-runtime.json").read_text())
assert report["agent_sha"] == EXPECTED_AGENT_SHA
assert len(report["rows"]) == 8
for row in report["rows"]:
    assert row["valid_terminal"] and row["calls"] == 719
    assert not any(row["faults"].values()), row["faults"]
    assert row["runtime_max"] < 0.5
print(json.dumps(report["summary"], indent=2))
'''
    pack = '''import gzip, io, tarfile
buffer = io.BytesIO()
with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
    with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for name in ("main.py", "LICENSE.txt", "NOTICE.txt"):
            payload = pathlib.Path(name).read_bytes()
            entry = tarfile.TarInfo(name)
            entry.size, entry.mode, entry.mtime = len(payload), 0o644, 0
            tar.addfile(entry, io.BytesIO(payload))
artifact = buffer.getvalue()
pathlib.Path("submission.tar.gz").write_bytes(artifact)
with tarfile.open("submission.tar.gz") as tar:
    assert tar.getnames() == ["main.py", "LICENSE.txt", "NOTICE.txt"]
    assert hashlib.sha256(tar.extractfile("main.py").read()).hexdigest() == EXPECTED_AGENT_SHA
verification = {
    "exp_id": "EXP-006", "agent_sha": EXPECTED_AGENT_SHA,
    "artifact_sha": hashlib.sha256(artifact).hexdigest(),
    "engine_version": report["engine_version"], "tests": test_count,
    "episodes": len(report["rows"]), "faults": 0,
    "runtime_max": max(r["runtime_max"] for r in report["rows"]),
    "scope": "Runtime and baseline validation, not evidence of beating strong public agents",
}
pathlib.Path("runtime-verification.json").write_text(json.dumps(verification, indent=2))
print(json.dumps(verification, indent=2))
'''
    cells = [{"cell_type": "markdown", "metadata": {}, "source": (
        "# EXP-006: Independent Crop Controller\n\n"
        "An independently written baseline for Kaggriculture. It budgets existing cash, "
        "models future supply/demand, reserves worker tasks and transports terminal inventory.\n\n"
        "Local tests beat the legacy repository baseline but lose to the public Shape v11 reference. "
        "This is a baseline/runtime audit, not a leaderboard-strength claim. No public opponent "
        "source, action tapes or weights are included in the submitted artifact.\n\n"
        "Source and research: https://github.com/whzy3185/kagriculture/tree/research/round1-audit-20260907\n\n"
        "The artifact is distributed under Apache-2.0, with game-rule attribution in NOTICE.txt. "
        "No credentials are included and this notebook does not submit to the competition."
    )}]
    for text in (setup, materialize, tests, games, pack):
        cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text})
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "cells": cells}
    for i, cell in enumerate(cells):
        cell["id"] = "exp006-" + str(i)
    (folder / "notebook.ipynb").write_text(json.dumps(notebook, indent=2) + "\n")
    metadata = {"id": "muelsyse111/kaggriculture-exp006-independent-baseline-audit", "title": "Kaggriculture EXP006 Independent Baseline Audit",
                "code_file": "notebook.ipynb", "language": "python", "kernel_type": "notebook",
                "is_private": True, "enable_gpu": False, "enable_internet": True,
                "dataset_sources": [], "competition_sources": ["kaggriculture"], "kernel_sources": []}
    (folder / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    artifact_dir = ROOT / "submissions/artifacts/EXP-006"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    data = io.BytesIO()
    with gzip.GzipFile(fileobj=data, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tar:
            for name in ("main.py", "LICENSE.txt", "NOTICE.txt"):
                payload = files[name].encode()
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(payload), 0o644, 0
                tar.addfile(info, io.BytesIO(payload))
    (artifact_dir / "submission.tar.gz").write_bytes(data.getvalue())
    print(json.dumps({"agent_sha": digest, "artifact_sha": hashlib.sha256(data.getvalue()).hexdigest(), "artifact_bytes": len(data.getvalue())}))


if __name__ == "__main__":
    main()
