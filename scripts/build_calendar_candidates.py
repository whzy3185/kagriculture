"""Reproduce two calendar-only candidates from the immutable EXP045/054 bytes."""
from pathlib import Path
import difflib
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASES = {
    "045": ("EXP-045-masterv4-step1002", "6744b67f9491a65404b70b200bd61a0fd588de513db4f11b119ca0213493686b"),
    "054": ("EXP-054-highquote-150", "3d0002923d42add183e88f912c52b5015639e4386c9a78d7eb3dba91310c33f7"),
}
OLD = b"    pending = {22: 0.25, 24: 0.25}"
NEW = b"    pending = {21: 0.25, 24: 0.25}"
OLD_COMMENT = b"seven shops by day 22, eight by day 24"
NEW_COMMENT = b"seven shops by day 21, eight by day 24"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def source_bytes(package):
    local = ROOT / "benchmark_packages" / package / "main.py"
    if local.is_file():
        return local.read_bytes()
    archive = ROOT / "submissions" / (package + ".tar.gz")
    with tarfile.open(archive, "r:gz") as handle:
        member = handle.getmember("main.py")
        assert member.isfile() and member.size <= 2_000_000
        return handle.extractfile(member).read()

def main():
    manifest = {"mechanism": "calendar-only: seventh future shop opens on day 21, not day 22",
                "base_commit": "a1d81080538d33f9cbd0646eb8dd845f360e353b", "candidates": {}}
    for number, (package, expected) in BASES.items():
        original = source_bytes(package)
        assert digest(original) == expected, package
        baseline_path = ROOT / "benchmark_packages" / package / "main.py"
        if not baseline_path.exists():
            baseline_path.parent.mkdir(parents=True, exist_ok=True)
            baseline_path.write_bytes(original)
        assert original.count(OLD) == original.count(OLD_COMMENT) == 1
        changed = original.replace(OLD, NEW).replace(OLD_COMMENT, NEW_COMMENT)
        path = ROOT / "agents" / "candidates" / ("exp20260930_calendar_" + number) / "main.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(changed)
        patch = "".join(difflib.unified_diff(original.decode().splitlines(True), changed.decode().splitlines(True),
                    fromfile="benchmark_packages/" + package + "/main.py", tofile=str(path.relative_to(ROOT))))
        report = ROOT / "reports" / ("calendar_" + number + "_exact.diff")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(patch)
        manifest["candidates"][number] = {"base_package": package, "base_sha256": expected,
            "candidate": str(path.relative_to(ROOT)), "candidate_sha256": digest(changed),
            "bytes": len(changed), "diff": str(report.relative_to(ROOT)),
            "changes": ["one integer calendar key: 22 to 21", "matching explanatory comment"],
            "unchanged": ["0.25 probability", "9000 revenue gate", "HD2 future multiplier 0.0",
                          "production/action/market layers", "entry point and licensing notices"]}
    destination = ROOT / "reports" / "calendar_candidate_manifest.json"
    destination.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
