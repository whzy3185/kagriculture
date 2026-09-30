from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmark_packages" / "EXP-054-highquote-150" / "main.py"
TARGETS = (80, 100, 120, 175, 200)

source = SOURCE.read_text(encoding="utf-8")
needle = "_E54_THRESHOLD = 150"
if source.count(needle) != 1:
    raise RuntimeError(f"expected exactly one {needle!r}, found {source.count(needle)}")

for threshold in TARGETS:
    output = ROOT / "experiments" / f"exp062_hq{threshold}" / "main.py"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        source.replace(needle, f"_E54_THRESHOLD = {threshold}"),
        encoding="utf-8",
        newline="\n",
    )
    print(threshold, output, output.stat().st_size)
