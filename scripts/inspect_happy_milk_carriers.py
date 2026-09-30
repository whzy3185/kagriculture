from __future__ import annotations

import json
from pathlib import Path


PATH = Path(r"E:\kaggriculture\reports\online_reruns_20260929_selected\episode-115058783-replay.json")
ACCESS = ((4, 4), (4, 5), (5, 4), (5, 5))


def distance(pos):
    return min(abs(int(pos[0]) - x) + abs(int(pos[1]) - y) for x, y in ACCESS)


replay = json.loads(PATH.read_text(encoding="utf-8"))
seat = 1
for step, frame in enumerate(replay["steps"]):
    if not 280 <= step <= 460:
        continue
    state = frame[seat]
    obs = state.get("observation") or {}
    private = obs.get("private") or {}
    farms = obs.get("farms") or []
    if len(farms) < 2:
        continue
    farm = farms[seat]
    positions = [farm.get("farmer"), *(farm.get("hands") or [])]
    inventories = private.get("inventories") or []
    action = state.get("action") or {}
    commands = [action.get("farmer"), *(action.get("hands") or [])]
    carriers = []
    for actor, (pos, inventory) in enumerate(zip(positions, inventories)):
        milk = int((inventory or {}).get("MILK", 0) or 0)
        if milk >= 3 and distance(pos) <= 4:
            carriers.append((actor, pos, milk, distance(pos), commands[actor] if actor < len(commands) else None))
    if not carriers:
        continue
    market = action.get("market") or []
    print(
        step,
        f"d{step // 24}h{step % 24}",
        f"money={farm.get('money')}/{farms[0].get('money')}",
        f"quote={((obs.get('market') or {}).get('prices') or {}).get('MILK')}",
        f"shed={private.get('shed', {}).get('MILK')}",
        f"carriers={carriers}",
        f"market={[order for order in market if len(order) > 1 and order[1] == 'MILK']}",
    )
