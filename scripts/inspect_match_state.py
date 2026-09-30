from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from collections import Counter
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("agent_a", type=Path)
parser.add_argument("agent_b", type=Path)
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--step", type=int, required=True)
args = parser.parse_args()

repo = Path(r"E:\kaggriculture")
sys.path.insert(0, str(repo))
from src.current_env import make_environment  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    env = make_environment(args.seed)
    env.run([str(args.agent_a.resolve()), str(args.agent_b.resolve())])

frame = env.steps[args.step]
obs = dict(frame[0].observation)
farms = []
for farm in obs["farms"]:
    animals = Counter()
    crops = Counter()
    for row in farm["tiles"]:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("animal"):
                animals[tile["animal"]] += 1
            if tile.get("crop"):
                crops[tile["crop"]] += 1
    farms.append(
        {
            "money": farm["money"],
            "hands": len(farm.get("hands") or []),
            "animals": animals,
            "crops": crops,
            "positions": [farm["farmer"], *(farm.get("hands") or [])],
        }
    )

print(
    json.dumps(
        {
            "seed": args.seed,
            "step": args.step,
            "shops": obs["town"]["unlocked_shops"],
            "market": obs["market"],
            "farms": farms,
        },
        ensure_ascii=False,
        indent=2,
    )
)
