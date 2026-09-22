"""Parallel, resumable paired-seat round robin for Kaggriculture agents."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def game_key(agent_a: str, agent_b: str, seed: int, seat_a: int) -> str:
    return f"{agent_a}|{agent_b}|{seed}|{seat_a}"


def play(job: tuple[str, str, str, str, int, int]) -> dict[str, Any]:
    label_a, path_a, label_b, path_b, seed, seat_a = job
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from src.current_env import make_environment

        env = make_environment(seed)
        agents = [path_b, path_a] if seat_a else [path_a, path_b]
        started = time.perf_counter()
        env.run(agents)
        elapsed = time.perf_counter() - started
    final = env.state
    rewards = [float(state.reward or 0.0) for state in final]
    statuses = [str(state.status) for state in final]
    money_a = rewards[seat_a]
    money_b = rewards[1 - seat_a]
    margin = money_a - money_b
    return {
        "key": game_key(label_a, label_b, seed, seat_a),
        "agent_a": label_a,
        "agent_b": label_b,
        "seed": seed,
        "seat_a": seat_a,
        "money_a": money_a,
        "money_b": money_b,
        "margin_a": margin,
        "outcome_a": "W" if margin > 0 else "L" if margin < 0 else "T",
        "statuses": statuses,
        "elapsed_seconds": elapsed,
    }


def wilson(successes: float, games: int, z: float = 1.96) -> tuple[float, float]:
    if games == 0:
        return (0.0, 0.0)
    p = successes / games
    denom = 1.0 + z * z / games
    center = (p + z * z / (2 * games)) / denom
    half = z * math.sqrt(p * (1 - p) / games + z * z / (4 * games * games)) / denom
    return (center - half, center + half)


def build_report(
    roster: dict[str, Path],
    seeds: list[int],
    games: list[dict[str, Any]],
    complete: bool,
    pairs: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    selected_pairs = pairs if pairs is not None else list(combinations(roster, 2))
    pairwise = []
    for label_a, label_b in selected_pairs:
        rows = [g for g in games if g["agent_a"] == label_a and g["agent_b"] == label_b]
        if not rows:
            continue
        margins = [float(g["margin_a"]) for g in rows]
        wins = sum(g["outcome_a"] == "W" for g in rows)
        ties = sum(g["outcome_a"] == "T" for g in rows)
        losses = len(rows) - wins - ties
        points = wins + 0.5 * ties
        pairwise.append(
            {
                "agent_a": label_a,
                "agent_b": label_b,
                "games": len(rows),
                "wins_a": wins,
                "ties": ties,
                "losses_a": losses,
                "match_points_a": points / len(rows),
                "mean_margin_a": statistics.fmean(margins),
                "median_margin_a": statistics.median(margins),
                "min_margin_a": min(margins),
                "max_margin_a": max(margins),
            }
        )

    standings = []
    for label in roster:
        outcomes: list[str] = []
        margins: list[float] = []
        for game in games:
            if game["agent_a"] == label:
                outcomes.append(game["outcome_a"])
                margins.append(float(game["margin_a"]))
            elif game["agent_b"] == label:
                reverse = {"W": "L", "L": "W", "T": "T"}[game["outcome_a"]]
                outcomes.append(reverse)
                margins.append(-float(game["margin_a"]))
        wins = outcomes.count("W")
        ties = outcomes.count("T")
        losses = outcomes.count("L")
        points = wins + 0.5 * ties
        lo, hi = wilson(points, len(outcomes))
        standings.append(
            {
                "agent": label,
                "games": len(outcomes),
                "wins": wins,
                "ties": ties,
                "losses": losses,
                "match_points": points / len(outcomes) if outcomes else 0.0,
                "wilson95_low": lo,
                "wilson95_high": hi,
                "mean_margin": statistics.fmean(margins) if margins else 0.0,
                "median_margin": statistics.median(margins) if margins else 0.0,
            }
        )
    standings.sort(key=lambda row: (row["match_points"], row["mean_margin"]), reverse=True)
    for rank, row in enumerate(standings, 1):
        row["rank"] = rank

    return {
        "protocol": "paired-seats-current-official-interpreter-round-robin",
        "complete": complete,
        "seeds": seeds,
        "agents": {
            label: {"path": str(path), "sha256": sha256(path)} for label, path in roster.items()
        },
        "expected_games": len(selected_pairs) * len(seeds) * 2,
        "completed_games": len(games),
        "standings": standings,
        "pairwise": pairwise,
        "games": sorted(games, key=lambda row: row["key"]),
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--seeds", default="2117343235,1206908045,1271775642")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--anchor",
        help="Only evaluate pairs containing this roster label; default is a full round robin.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw = json.loads(args.roster.resolve().read_text(encoding="utf-8"))
    roster = {label: (REPO_ROOT / value).resolve() for label, value in raw.items()}
    missing = [str(path) for path in roster.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing agents: {missing}")
    seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]
    if not seeds:
        raise ValueError("At least one seed is required")
    if args.anchor and args.anchor not in roster:
        raise ValueError(f"Anchor is not in roster: {args.anchor}")
    pairs = list(combinations(roster, 2))
    if args.anchor:
        pairs = [pair for pair in pairs if args.anchor in pair]

    output = args.output.resolve()
    games: list[dict[str, Any]] = []
    if output.exists():
        previous = json.loads(output.read_text(encoding="utf-8"))
        games = list(previous.get("games", []))
    finished = {game["key"] for game in games}

    jobs = []
    for label_a, label_b in pairs:
        for seed in seeds:
            for seat_a in (0, 1):
                key = game_key(label_a, label_b, seed, seat_a)
                if key not in finished:
                    jobs.append(
                        (label_a, str(roster[label_a]), label_b, str(roster[label_b]), seed, seat_a)
                    )

    expected = len(pairs) * len(seeds) * 2
    print(f"agents={len(roster)} expected_games={expected} resumed={len(games)} pending={len(jobs)}", flush=True)
    errors = []
    started = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(play, job): job for job in jobs}
        for index, future in enumerate(as_completed(futures), 1):
            job = futures[future]
            try:
                games.append(future.result())
            except Exception as exc:  # pragma: no cover - diagnostic path
                errors.append({"job": job, "error": repr(exc)})
            if index % 20 == 0 or index == len(jobs):
                complete = len(games) == expected and not errors
                report = build_report(roster, seeds, games, complete, pairs)
                report["errors"] = errors
                write_report(output, report)
                elapsed = time.perf_counter() - started
                print(
                    f"progress={len(games)}/{expected} new={index}/{len(jobs)} "
                    f"errors={len(errors)} elapsed={elapsed:.1f}s",
                    flush=True,
                )

    report = build_report(roster, seeds, games, len(games) == expected and not errors, pairs)
    report["errors"] = errors
    write_report(output, report)
    for row in report["standings"]:
        print(
            f"{row['rank']:>2} {row['agent']:<22} "
            f"{row['wins']}-{row['ties']}-{row['losses']} "
            f"MP={row['match_points']:.3f} margin={row['mean_margin']:+.1f}"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
