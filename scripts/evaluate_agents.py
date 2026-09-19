"""Deterministic paired-seat evaluator for Kaggriculture submissions."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.current_env import make_environment  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def play(candidate: Path, opponent: Path, seed: int, candidate_seat: int) -> dict[str, Any]:
    env = make_environment(seed)
    agents = [str(opponent), str(candidate)] if candidate_seat else [str(candidate), str(opponent)]
    started = time.perf_counter()
    env.run(agents)
    elapsed = time.perf_counter() - started

    final = env.state
    statuses = [str(state.status) for state in final]
    rewards = [float(state.reward or 0.0) for state in final]
    candidate_money = rewards[candidate_seat]
    opponent_money = rewards[1 - candidate_seat]
    return {
        "seed": seed,
        "candidate_seat": candidate_seat,
        "candidate_money": candidate_money,
        "opponent_money": opponent_money,
        "margin": candidate_money - opponent_money,
        "win": candidate_money > opponent_money,
        "tie": candidate_money == opponent_money,
        "statuses": statuses,
        "elapsed_seconds": elapsed,
    }


def summarize(candidate: Path, opponent: Path, seeds: list[int]) -> dict[str, Any]:
    games: list[dict[str, Any]] = []
    for seed in seeds:
        for seat in (0, 1):
            result = play(candidate, opponent, seed, seat)
            games.append(result)
            outcome = "W" if result["win"] else "T" if result["tie"] else "L"
            print(
                f"seed={seed:>5} seat={seat} {outcome} "
                f"money={result['candidate_money']:.0f}:{result['opponent_money']:.0f} "
                f"margin={result['margin']:+.0f} time={result['elapsed_seconds']:.2f}s",
                flush=True,
            )

    margins = [game["margin"] for game in games]
    wins = sum(bool(game["win"]) for game in games)
    ties = sum(bool(game["tie"]) for game in games)
    summary = {
        "protocol": "paired-seats-current-official-interpreter",
        "candidate": str(candidate),
        "candidate_sha256": sha256(candidate),
        "opponent": str(opponent),
        "opponent_sha256": sha256(opponent),
        "seeds": seeds,
        "games_count": len(games),
        "wins": wins,
        "ties": ties,
        "losses": len(games) - wins - ties,
        "win_rate": wins / len(games),
        "mean_margin": statistics.fmean(margins),
        "median_margin": statistics.median(margins),
        "min_margin": min(margins),
        "max_margin": max(margins),
        "mean_candidate_money": statistics.fmean(game["candidate_money"] for game in games),
        "mean_opponent_money": statistics.fmean(game["opponent_money"] for game in games),
        "total_elapsed_seconds": sum(game["elapsed_seconds"] for game in games),
        "games": games,
    }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("opponent", type=Path)
    parser.add_argument("--seeds", default="101,211,307,401,503,601")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidate = args.candidate.resolve()
    opponent = args.opponent.resolve()
    seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]
    if not candidate.is_file() or not opponent.is_file():
        raise FileNotFoundError("Candidate and opponent must both be Python files")
    if not seeds:
        raise ValueError("At least one seed is required")

    report = summarize(candidate, opponent, seeds)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

