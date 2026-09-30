from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments" / "exp063_wool_flush" / "main.py"
OUTPUT = ROOT / "experiments" / "exp065_mirror_wool_flush" / "main.py"

source = SOURCE.read_text(encoding="utf-8")
needle = '''        quote = int((observation.get("market") or {}).get("prices", {}).get("WOOL", 0) or 0)
        if sheep >= 15 and step // 24 == 18 and quote >= 220:
'''
replacement = '''        rival = observation["farms"][1 - seat]
        rival_sheep = sum(
            1
            for row in rival["tiles"]
            for tile in row
            if isinstance(tile, dict) and tile.get("animal") == "SHEEP"
        )
        quote = int((observation.get("market") or {}).get("prices", {}).get("WOOL", 0) or 0)
        if sheep >= 15 and rival_sheep >= 15 and step // 24 == 18 and quote >= 220:
'''
if source.count(needle) != 1:
    raise RuntimeError("expected unique EXP063 gate")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(source.replace(needle, replacement), encoding="utf-8", newline="\n")
print(OUTPUT, OUTPUT.stat().st_size)
