from __future__ import annotations

import json
from pathlib import Path


path = Path(r"E:\kaggriculture\reports\online_reruns_20260929_selected\episode-115058783-replay.json")
replay = json.loads(path.read_text(encoding="utf-8"))
seat = 1
for step, frame in enumerate(replay["steps"]):
    if not 120 <= step <= 360:
        continue
    state = frame[seat]
    obs = state.get("observation") or {}
    action = state.get("action") or {}
    commands = [action.get("farmer"), *(action.get("hands") or [])]
    plants = [(i, command) for i, command in enumerate(commands) if command and command[0] in {"PLANT", "DIG"}]
    buys = [order for order in action.get("market") or [] if order and order[0] == "BUY_SEED"]
    if plants or buys:
        private = obs.get("private") or {}
        print(
            step,
            f"d{step // 24}h{step % 24}",
            f"money={(obs.get('farms') or [{}, {}])[seat].get('money')}",
            f"seeds={private.get('seeds')}",
            f"plants={plants}",
            f"buys={buys}",
        )
