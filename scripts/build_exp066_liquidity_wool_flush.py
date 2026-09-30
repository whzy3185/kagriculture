from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments" / "exp065_mirror_wool_flush" / "main.py"
OUTPUT = ROOT / "experiments" / "exp066_liquidity_wool_flush" / "main.py"

source = SOURCE.read_text(encoding="utf-8")
needle = "if sheep >= 15 and rival_sheep >= 15 and step // 24 == 18 and quote >= 220:"
replacement = "if sheep >= 15 and rival_sheep >= 15 and float(farm.get(\"money\", 0) or 0) < 42000 and step // 24 == 18 and quote >= 220:"
if source.count(needle) != 1:
    raise RuntimeError("expected unique EXP065 gate")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(source.replace(needle, replacement), encoding="utf-8", newline="\n")
print(OUTPUT, OUTPUT.stat().st_size)
