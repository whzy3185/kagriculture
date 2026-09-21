"""Summarize Kaggriculture replay JSON files without retaining full frames."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def tile_counts(farm: dict[str, Any]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []):
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "PLANT":
                counts[tile.get("crop", "UNKNOWN")] += 1
            elif tile.get("animal"):
                counts[tile["animal"]] += 1
            else:
                counts[tile.get("kind", "UNKNOWN")] += 1
    return dict(sorted(counts.items()))


def summarize(path: Path, username: str) -> dict[str, Any]:
    replay = json.loads(path.read_text(encoding="utf-8"))
    steps = replay["steps"]
    names = replay.get("info", {}).get("TeamNames", [])
    if username not in names:
        raise ValueError(f"{username!r} not found in {names!r} for {path.name}")
    ours = names.index(username)
    theirs = 1 - ours

    market: list[Counter[str]] = [Counter(), Counter()]
    field: list[Counter[str]] = [Counter(), Counter()]
    for frame in steps[1:]:
        for player, state in enumerate(frame):
            action = state.get("action") or {}
            units = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
            for order in units:
                if order:
                    field[player][str(order[0])] += 1
            for order in action.get("market") or []:
                if not order:
                    continue
                op = str(order[0])
                item = str(order[1]) if len(order) > 1 else ""
                quantity = int(order[2]) if len(order) > 2 and isinstance(order[2], (int, float)) else 1
                market[player][f"{op}:{item}".rstrip(":")] += quantity

    daily = []
    for day in range(31):
        frame_index = min(day * 24, len(steps) - 1)
        obs = steps[frame_index][0].get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) < 2:
            continue
        daily.append(
            {
                "day": day,
                "our_money": float(farms[ours]["money"]),
                "their_money": float(farms[theirs]["money"]),
                "margin": float(farms[ours]["money"] - farms[theirs]["money"]),
            }
        )

    final_states = steps[-1]
    rewards = [float(state.get("reward") or 0.0) for state in final_states]
    final_obs = final_states[0]["observation"]
    final_farms = final_obs["farms"]
    margins = [row["margin"] for row in daily]
    first_negative_day = next((row["day"] for row in daily if row["margin"] < 0), None)
    last_lead_day = max((row["day"] for row in daily if row["margin"] >= 0), default=None)
    reward_margin = rewards[ours] - rewards[theirs]
    outcome = "W" if reward_margin > 0 else "L" if reward_margin < 0 else "T"
    comeback = outcome == "W" and any(margin < 0 for margin in margins[:-1])
    blown_lead = outcome == "L" and any(margin > 0 for margin in margins[:-1])

    return {
        "episode_id": int(replay.get("info", {}).get("EpisodeId", path.stem.split("-")[1])),
        "seed": int(replay.get("info", {}).get("seed", -1)),
        "our_seat": ours,
        "opponent": names[theirs],
        "our_reward": rewards[ours],
        "their_reward": rewards[theirs],
        "margin": reward_margin,
        "outcome": outcome,
        "win": outcome == "W",
        "tie": outcome == "T",
        "loss": outcome == "L",
        "comeback": comeback,
        "blown_lead": blown_lead,
        "max_daily_lead": max(margins),
        "min_daily_lead": min(margins),
        "first_negative_day": first_negative_day,
        "last_lead_day": last_lead_day,
        "shops": final_obs.get("town", {}).get("unlocked_shops", []),
        "our_tiles": tile_counts(final_farms[ours]),
        "their_tiles": tile_counts(final_farms[theirs]),
        "our_market": dict(sorted(market[ours].items())),
        "their_market": dict(sorted(market[theirs].items())),
        "our_field": dict(sorted(field[ours].items())),
        "their_field": dict(sorted(field[theirs].items())),
        "daily": daily,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--username", default="muelsyse111")
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--csv-output", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted(args.directory.resolve().glob("episode-*-replay.json"))
    if not paths:
        raise FileNotFoundError(f"No replay JSON files in {args.directory}")
    summaries = []
    for path in paths:
        item = summarize(path, args.username)
        summaries.append(item)
        outcome = item["outcome"]
        print(
            f"{item['episode_id']} {outcome} seat={item['our_seat']} "
            f"vs={item['opponent']} money={item['our_reward']:.0f}:{item['their_reward']:.0f} "
            f"margin={item['margin']:+.0f} first_negative={item['first_negative_day']}"
        )

    aggregate = {
        "username": args.username,
        "games": len(summaries),
        "wins": sum(item["win"] for item in summaries),
        "ties": sum(item["tie"] for item in summaries),
        "losses": sum(item["loss"] for item in summaries),
        "match_points": (
            sum(item["win"] for item in summaries)
            + 0.5 * sum(item["tie"] for item in summaries)
        ) / len(summaries),
        "comebacks": sum(item["comeback"] for item in summaries),
        "blown_leads": sum(item["blown_lead"] for item in summaries),
        "mean_margin": sum(item["margin"] for item in summaries) / len(summaries),
        "episodes": summaries,
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")

    args.csv_output.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "episode_id", "seed", "our_seat", "opponent", "our_reward", "their_reward",
        "margin", "outcome", "win", "tie", "loss", "comeback", "blown_lead",
        "max_daily_lead", "min_daily_lead", "first_negative_day", "last_lead_day",
    ]
    with args.csv_output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for item in summaries:
            writer.writerow({key: item[key] for key in columns})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
