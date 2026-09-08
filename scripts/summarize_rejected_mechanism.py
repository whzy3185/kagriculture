"""Extract observed feed failures and animal losses from rejected-candidate replays."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    selected = json.loads((ROOT / "research/EXP-20260908-01-losses.json").read_text())
    results = []
    for case in selected["cases"]:
        replay = json.loads((ROOT / case["raw_path"]).read_text())
        players = []
        for player in (0, 1):
            escaped, empty_feed = [], []
            for t in range(719):
                before = replay["steps"][t][player]["observation"]
                after = replay["steps"][t+1][player]["observation"]
                farm = before["farms"][player]
                action = replay["steps"][t+1][player]["action"]
                invs = before["private"]["inventories"]
                positions = [farm["farmer"], *farm["hands"]]
                for i, command in enumerate([action["farmer"], *action["hands"]]):
                    if command and command[0] == "FEED" and i < len(invs) and invs[i].get("WHEAT", 0) == 0:
                        empty_feed.append({"turn": t, "unit": i, "position": positions[i]})
                if before["day"] == after["day"]:
                    continue
                for y, row in enumerate(farm["tiles"]):
                    for x, tile in enumerate(row):
                        following = after["farms"][player]["tiles"][y][x]
                        if isinstance(tile, dict) and tile.get("animal") and (
                                not isinstance(following, dict) or following.get("animal") != tile["animal"]):
                            escaped.append({"turn": t, "animal": tile["animal"], "position": [x, y]})
            players.append({"role": "candidate" if player == case["seat"] else "parent",
                            "empty_carried_wheat_feed_requests": empty_feed, "animal_disappearances_at_day_end": escaped})
        results.append({"seed": case["seed"], "players": players, "replay_sha256": case["raw_sha256"]})
    result = {"scope": "Descriptive selected-loss mechanism trace; no new independent evaluation games",
              "interpretation_limit": "Observed missing feed and disappearances do not isolate every intermediate causal link",
              "cases": results}
    with (ROOT / "research/EXP-20260908-01-mechanism.json").open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps([{ "seed": c["seed"], "players": [{"role": p["role"],
        "empty_feed_requests": len(p["empty_carried_wheat_feed_requests"]),
        "animal_losses": p["animal_disappearances_at_day_end"]} for p in c["players"]]} for c in results], indent=2))


if __name__ == "__main__":
    main()
