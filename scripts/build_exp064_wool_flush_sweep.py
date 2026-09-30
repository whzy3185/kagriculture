from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments" / "exp063_wool_flush" / "main.py"
source = SOURCE.read_text(encoding="utf-8")


def with_min_wool(text: str, minimum: int) -> str:
    needle = "if wool < 12 or actor in active:"
    replacement = f"if wool < {minimum} or actor in active:"
    if text.count(needle) != 1:
        raise RuntimeError(f"missing unique trigger: {needle}")
    return text.replace(needle, replacement)


def with_one_trigger(text: str) -> str:
    replacements = {
        "_E63_ACTIVE = {}\n_E63_REPORT": "_E63_ACTIVE = {}\n_E64_USED = {}\n_E63_REPORT",
        "_E63_ACTIVE[seat] = {}\n        _E63_REPORT.update": "_E63_ACTIVE[seat] = {}\n        _E64_USED[seat] = 0\n        _E63_REPORT.update",
        "for actor, (pos, inventory) in enumerate(zip(positions, inventories)):\n                wool": "for actor, (pos, inventory) in enumerate(zip(positions, inventories)):\n                if _E64_USED.get(seat, 0) >= 1:\n                    break\n                wool",
        "_E63_REPORT[\"triggers\"] += 1\n": "_E63_REPORT[\"triggers\"] += 1\n                    _E64_USED[seat] = _E64_USED.get(seat, 0) + 1\n",
    }
    for needle, replacement in replacements.items():
        if text.count(needle) != 1:
            raise RuntimeError(f"missing unique one-trigger insertion point: {needle!r}")
        text = text.replace(needle, replacement)
    return text


variants = {
    "exp064_wool_t18_both": with_min_wool(source, 18),
    "exp064_wool_t12_one": with_one_trigger(source),
    "exp064_wool_t18_one": with_one_trigger(with_min_wool(source, 18)),
}

for name, text in variants.items():
    output = ROOT / "experiments" / name / "main.py"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8", newline="\n")
    print(name, output.stat().st_size)
