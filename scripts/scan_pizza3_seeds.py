from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


REPO = Path(r"E:\kaggriculture")
AGENT_PATH = Path(__file__).resolve().parents[1] / "experiments/exp066_liquidity_wool_flush/main.py"
_AGENT = None


def load_agent():
    global _AGENT
    if _AGENT is None:
        spec = importlib.util.spec_from_file_location("pizza3_scan_agent", AGENT_PATH)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        _AGENT = module.kaggle_submission_agent
    return _AGENT


def scan(seed: int):
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from src.current_env import make_environment

        agent = load_agent()
        env = make_environment(seed)
        env.configuration.episodeSteps = 217
        env.run([agent, agent])
        shops = list(env.state[0].observation.get("town", {}).get("unlocked_shops", []))
    return seed, shops


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=27_000_000)
    parser.add_argument("--count", type=int, default=4096)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--need", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    matches = []
    chunk = 256
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for offset in range(0, args.count, chunk):
            seeds = range(args.start + offset, args.start + min(args.count, offset + chunk))
            for seed, shops in pool.map(scan, seeds, chunksize=4):
                if shops[:3] == ["PIZZA_SHOP"] * 3:
                    matches.append({"seed": seed, "shops": shops})
                    print(seed, shops, flush=True)
            print(f"scanned={min(args.count, offset + chunk)} matches={len(matches)}", flush=True)
            if len(matches) >= args.need:
                break
    args.output.write_text(json.dumps(matches, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
