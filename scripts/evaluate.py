"""Local head-to-head evaluation for Kaggriculture.

Examples:
    python scripts/evaluate.py --games 10
    python scripts/evaluate.py --games 20 --opponent path/to/other_agent.py
"""

from __future__ import annotations

import argparse
import importlib.util
import statistics
from pathlib import Path
from typing import Any, Callable, List, Tuple

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AGENT = ROOT / "main.py"


def load_agent(path: Path) -> Callable[[dict], dict]:
    spec = importlib.util.spec_from_file_location(f"agent_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load agent module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name in ("agent", "main"):
        candidate = getattr(module, name, None)
        if callable(candidate):
            return candidate
    raise AttributeError(f"{path} must expose callable agent(obs) or main(obs)")


def resolve_opponent(value: str) -> Any:
    path = Path(value)
    if path.exists():
        return load_agent(path.resolve())
    return value


def final_rewards(env: Any) -> Tuple[float, float]:
    final = env.steps[-1]
    return float(final[0].reward or 0), float(final[1].reward or 0)


def run_once(
    our_agent: Callable[[dict], dict],
    opponent: Any,
    seed: int,
    our_seat: int,
    episode_steps: int,
) -> Tuple[float, float]:
    config = {"episodeSteps": episode_steps, "seed": seed}
    env = make("kaggriculture", configuration=config, debug=False)

    players: List[Any] = [opponent, opponent]
    players[our_seat] = our_agent
    env.run(players)

    rewards = final_rewards(env)
    ours = rewards[our_seat]
    theirs = rewards[1 - our_seat]
    return ours, theirs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=Path, default=DEFAULT_AGENT)
    parser.add_argument("--opponent", default="random")
    parser.add_argument("--games", type=int, default=10, help="Number of seeds; each seed is played from both seats.")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--episode-steps", type=int, default=720)
    args = parser.parse_args()

    our_agent = load_agent(args.agent.resolve())
    opponent = resolve_opponent(args.opponent)

    margins: List[float] = []
    wins = losses = ties = 0

    for offset in range(args.games):
        seed = args.seed + offset
        for seat in (0, 1):
            ours, theirs = run_once(
                our_agent=our_agent,
                opponent=opponent,
                seed=seed,
                our_seat=seat,
                episode_steps=args.episode_steps,
            )
            margin = ours - theirs
            margins.append(margin)
            if margin > 0:
                wins += 1
            elif margin < 0:
                losses += 1
            else:
                ties += 1
            print(
                f"seed={seed:4d} seat={seat} ours={ours:10.1f} "
                f"opp={theirs:10.1f} margin={margin:10.1f}"
            )

    mean_margin = statistics.fmean(margins) if margins else 0.0
    median_margin = statistics.median(margins) if margins else 0.0
    stdev_margin = statistics.stdev(margins) if len(margins) > 1 else 0.0

    print("\n=== summary ===")
    print(f"episodes       : {len(margins)}")
    print(f"record         : {wins}-{losses}-{ties}")
    print(f"mean margin    : {mean_margin:.2f}")
    print(f"median margin  : {median_margin:.2f}")
    print(f"stdev margin   : {stdev_margin:.2f}")


if __name__ == "__main__":
    main()
