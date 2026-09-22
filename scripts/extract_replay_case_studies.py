"""Extract compact, auditable timelines for selected Kaggriculture replays."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def money(frame: list[dict[str, Any]], seat: int) -> float:
    observation = frame[0].get("observation") or {}
    return float(observation["farms"][seat]["money"])


def public_market(frame: list[dict[str, Any]]) -> dict[str, Any]:
    observation = frame[0].get("observation") or {}
    market = observation.get("market") or {}
    return {
        "prices": dict(market.get("prices") or {}),
        "inventory": dict(market.get("inventory") or {}),
    }


def action_summary(action: dict[str, Any] | None) -> dict[str, Any]:
    action = action or {}
    units = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    return {
        "market": [list(order) for order in (action.get("market") or [])],
        "unit_ops": dict(sorted(Counter(str(order[0]) for order in units if order).items())),
    }


def market_totals(steps: list[list[dict[str, Any]]], seat: int, start: int) -> dict[str, int]:
    result: Counter[str] = Counter()
    for frame in steps[start:]:
        action = frame[seat].get("action") or {}
        for order in action.get("market") or []:
            if not order:
                continue
            op = str(order[0])
            item = str(order[1]) if len(order) > 1 else ""
            quantity = int(order[2]) if len(order) > 2 else 1
            result[f"{op}:{item}"] += quantity
    return dict(sorted(result.items()))


def summarize(path: Path, username: str, top_events: int) -> dict[str, Any]:
    replay = json.loads(path.read_text(encoding="utf-8"))
    steps = replay["steps"]
    names = list(replay.get("info", {}).get("TeamNames") or [])
    ours = names.index(username)
    theirs = 1 - ours

    margins = [money(frame, ours) - money(frame, theirs) for frame in steps]
    daily = []
    for day in range(31):
        index = min(day * 24, len(steps) - 1)
        daily.append(
            {
                "day": day,
                "step": index,
                "our_money": money(steps[index], ours),
                "their_money": money(steps[index], theirs),
                "margin": margins[index],
            }
        )

    events = []
    for step in range(1, len(steps)):
        delta = margins[step] - margins[step - 1]
        if delta == 0:
            continue
        previous = steps[step - 1]
        events.append(
            {
                "result_step": step,
                "day": step // 24,
                "hour": step % 24,
                "margin_before": margins[step - 1],
                "margin_after": margins[step],
                "margin_delta": delta,
                "our_money_delta": money(steps[step], ours) - money(previous, ours),
                "their_money_delta": money(steps[step], theirs) - money(previous, theirs),
                "market_before": public_market(previous),
                "market_after": public_market(steps[step]),
                "our_action": action_summary(previous[ours].get("action")),
                "their_action": action_summary(previous[theirs].get("action")),
            }
        )
    decisive = sorted(events, key=lambda row: abs(row["margin_delta"]), reverse=True)[:top_events]

    rewards = [float(state.get("reward") or 0.0) for state in steps[-1]]
    final_margin = rewards[ours] - rewards[theirs]
    return {
        "episode_id": int(replay.get("info", {}).get("EpisodeId", path.stem.split("-")[1])),
        "source": str(path.resolve()),
        "names": names,
        "our_seat": ours,
        "opponent": names[theirs],
        "our_reward": rewards[ours],
        "their_reward": rewards[theirs],
        "final_margin": final_margin,
        "outcome": "W" if final_margin > 0 else "L" if final_margin < 0 else "T",
        "max_lead": max(margins),
        "max_deficit": min(margins),
        "last_nonnegative_step": max((i for i, value in enumerate(margins) if value >= 0), default=None),
        "daily": daily,
        "market_totals": {
            "full": {
                "ours": market_totals(steps, ours, 0),
                "theirs": market_totals(steps, theirs, 0),
            },
            "day18_plus": {
                "ours": market_totals(steps, ours, 18 * 24),
                "theirs": market_totals(steps, theirs, 18 * 24),
            },
            "day27_plus": {
                "ours": market_totals(steps, ours, 27 * 24),
                "theirs": market_totals(steps, theirs, 27 * 24),
            },
        },
        "decisive_events": decisive,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("replays", type=Path, nargs="+")
    parser.add_argument("--username", default="muelsyse111")
    parser.add_argument("--top-events", type=int, default=16)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = {
        "username": args.username,
        "cases": [summarize(path.resolve(), args.username, args.top_events) for path in args.replays],
    }
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for case in report["cases"]:
        print(
            f"{case['episode_id']} vs={case['opponent']} outcome={case['outcome']} "
            f"margin={case['final_margin']:+.0f} max_lead={case['max_lead']:+.0f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
