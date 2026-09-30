from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(r"E:\kaggriculture")
INDEX = REPO / "recovered/online_reruns_20260929_selected_opponents/index.json"
REPLAYS = REPO / "reports/online_reruns_20260929_selected"
OUTPUT = Path(__file__).resolve().parents[1] / "reports/official_route_signals_8cases.json"
SNAPSHOT_DAYS = {0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 29}


def tile_counts(farm: dict) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []):
        for tile in row:
            if not isinstance(tile, dict):
                continue
            crop = tile.get("crop")
            animal = tile.get("animal")
            if crop:
                counts[str(crop)] += 1
            if animal:
                counts[str(animal)] += 1
    return dict(sorted(counts.items()))


def market_totals(steps: list, seat: int, through_step: int) -> dict[str, dict[str, int]]:
    totals: dict[str, Counter[str]] = {
        "sell": Counter(),
        "buy_seed": Counter(),
        "buy_product": Counter(),
        "buy_animal": Counter(),
    }
    operation_map = {
        "SELL": "sell",
        "BUY_SEED": "buy_seed",
        "BUY_PRODUCT": "buy_product",
        "BUY_ANIMAL": "buy_animal",
    }
    for frame in steps[1 : through_step + 1]:
        action = frame[seat].get("action") or {}
        for order in action.get("market") or []:
            if len(order) < 3 or order[0] not in operation_map:
                continue
            totals[operation_map[order[0]]][str(order[1])] += int(order[2])
    return {kind: dict(sorted(values.items())) for kind, values in totals.items()}


def action_events(steps: list, seat: int) -> list[dict]:
    events = []
    for step, frame in enumerate(steps[1:], 1):
        action = frame[seat].get("action") or {}
        for order in action.get("market") or []:
            if order and order[0] == "SELL" and len(order) >= 3:
                obs = frame[seat].get("observation") or {}
                events.append(
                    {
                        "step": step,
                        "day": step // 24,
                        "product": order[1],
                        "quantity": int(order[2]),
                        "quote": ((obs.get("market") or {}).get("prices") or {}).get(order[1]),
                    }
                )
    return events


def analyze_case(case: dict) -> dict:
    episode = int(case["episode"])
    replay = json.loads((REPLAYS / f"episode-{episode}-replay.json").read_text(encoding="utf-8"))
    steps = replay["steps"]
    our_seat = int(case["our_seat"])
    snapshots = []
    for day in sorted(SNAPSHOT_DAYS):
        step = min(day * 24, len(steps) - 1)
        obs = steps[step][0].get("observation") or {}
        farms = obs.get("farms") or []
        prices = (obs.get("market") or {}).get("prices") or {}
        snapshots.append(
            {
                "day": day,
                "step": step,
                "shops": list((obs.get("town") or {}).get("unlocked_shops") or []),
                "prices": {key: prices.get(key) for key in ("WHEAT", "TOMATO", "STRAWBERRY", "CARROT", "MILK", "WOOL", "EGG")},
                "ours": {
                    "money": farms[our_seat].get("money"),
                    "tiles": tile_counts(farms[our_seat]),
                    "cumulative": market_totals(steps, our_seat, step),
                },
                "rival": {
                    "money": farms[1 - our_seat].get("money"),
                    "tiles": tile_counts(farms[1 - our_seat]),
                    "cumulative": market_totals(steps, 1 - our_seat, step),
                },
            }
        )
    return {
        **case,
        "rewards": replay.get("rewards"),
        "shops_final": list((steps[-1][0]["observation"].get("town") or {}).get("unlocked_shops") or []),
        "snapshots": snapshots,
        "our_sell_events": action_events(steps, our_seat),
        "rival_sell_events": action_events(steps, 1 - our_seat),
    }


def main() -> None:
    cases = json.loads(INDEX.read_text(encoding="utf-8"))
    result = [analyze_case(case) for case in cases]
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for case in result:
        print(f"\n{case['episode']} {case['opponent']} shops={case['shops_final']}")
        for snap in case["snapshots"]:
            if snap["day"] not in {6, 9, 12, 15, 18, 24, 29}:
                continue
            ours = snap["ours"]
            rival = snap["rival"]
            print(
                f"d{snap['day']:02d} money={ours['money']:.0f}/{rival['money']:.0f} "
                f"tiles={ours['tiles']}/{rival['tiles']} "
                f"soldT={ours['cumulative']['sell'].get('TOMATO', 0)}/{rival['cumulative']['sell'].get('TOMATO', 0)} "
                f"soldS={ours['cumulative']['sell'].get('STRAWBERRY', 0)}/{rival['cumulative']['sell'].get('STRAWBERRY', 0)}"
            )


if __name__ == "__main__":
    main()
