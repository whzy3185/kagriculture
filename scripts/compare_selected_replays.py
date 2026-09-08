"""Describe selected real replays without treating orders as fills or a causal trial."""

from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = ((0, 72), (72, 144), (144, 180), (180, 360), (360, 540), (540, 719))


def action_key(action, field):
    value = [action["farmer"], action["hands"]] if field == "field" else action["market"]
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def profile(data, seat):
    steps = data["steps"]
    if len(steps) != 720 or data["statuses"] != ["DONE", "DONE"]:
        raise ValueError("Incomplete selected replay")
    actions = [s[seat]["action"] for s in steps[1:]]
    snapshots = {}
    for t in (0, 72, 144, 180, 360, 540, 719):
        obs = steps[t][seat]["observation"]
        farm, private = obs["farms"][seat], obs["private"]
        if "tiles" not in farm:
            raise ValueError("Sparse replay; reconstruction required before asset comparison")
        assets = Counter(tile.get("crop") or tile.get("animal") or tile.get("kind")
                         for row in farm["tiles"] for tile in row if isinstance(tile, dict))
        snapshots[str(t)] = {"cash": farm["money"], "hands": len(farm["hands"]),
                             "land": farm["unlocked_quadrants"], "assets": dict(assets),
                             "carried_units": sum(sum(i.values()) for i in private["inventories"]),
                             "shed_units": sum(private["shed"].values()),
                             "shops": obs["town"]["unlocked_shops"]}
    windows = {}
    for start, end in WINDOWS:
        counts = Counter(command[0] for action in actions[start:end]
                         for command in [action["farmer"], *action["hands"]])
        market = Counter(order[0] for action in actions[start:end] for order in action["market"] if order)
        windows[f"{start}:{end}"] = {"requested_unit_actions": dict(counts),
                                     "requested_market_order_counts": dict(market),
                                     "net_cash_change": snapshots[str(end)]["cash"] - snapshots[str(start)]["cash"]}
    fingerprints = {str(n): {field: hashlib.sha256("\n".join(action_key(a, field) for a in actions[:n]).encode()).hexdigest()
                             for field in ("field", "market")} for n in (120, 180)}
    return {"seat": seat, "reward": data["rewards"][seat], "margin": data["rewards"][seat] - data["rewards"][1-seat],
            "snapshots": snapshots, "windows": windows, "opening_fingerprints": fingerprints}, actions


def main():
    selections = [(106731757, 1, "top3_team_recent_win"), (106728931, 1, "same_top3_submission_recent_loss"),
                  (106678954, 0, "EXP006_recent_large_loss"), (106664416, 1, "EXP006_recent_win")]
    rows, actions = [], {}
    for episode, seat, role in selections:
        path = ROOT / f"replays/raw/episode-{episode}-replay.json"
        raw = path.read_bytes()
        data = json.loads(raw)
        row, actions[episode] = profile(data, seat)
        row.update(episode_id=episode, role=role, replay_sha256=hashlib.sha256(raw).hexdigest(),
                   engine_version=data.get("module_version"))
        rows.append(row)
    agreement = {}
    for label, ids in (("same_top3_submission_win_vs_loss", (106731757, 106728931)),
                       ("EXP006_loss_vs_win", (106678954, 106664416))):
        agreement[label] = {}
        for start, end in WINDOWS:
            agreement[label][f"{start}:{end}"] = {field: sum(action_key(a, field) == action_key(b, field)
                for a, b in zip(actions[ids[0]][start:end], actions[ids[1]][start:end])) / (end-start)
                for field in ("field", "market")}
    result = {"scope": "Four selected recorded episodes, two submissions; descriptive, not causal or representative",
              "top_submission": 56047440, "own_submission": 56072267, "rows": rows,
              "agreement": agreement, "conditional_entropy": "NOT_ESTIMATED: two selected trajectories per submission",
              "public_champion_comparison": "PENDING public-panel selection and its own replay diagnostics",
              "market_accounting": "Order counts only; realized fills/revenue are not inferred"}
    output = ROOT / "research/REPLAY-20260908-comparison.json"
    with output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"agreement": agreement, "turn180": [{"episode": r["episode_id"], **r["snapshots"]["180"]} for r in rows]}, indent=2))


if __name__ == "__main__":
    main()
