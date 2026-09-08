"""Add a required portable family without repeating completed round-robin games."""

import argparse
from datetime import datetime, timezone
import json
import multiprocessing
from pathlib import Path

from evaluate_public_panel import evaluator, game, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=Path, required=True)
    parser.add_argument("--opponents", nargs="+", type=Path, required=True)
    parser.add_argument("--seed-start", type=int, required=True)
    parser.add_argument("--seeds", type=int, required=True)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = [args.agent, *args.opponents]
    hashes = {p.stem: evaluator.sha(p) for p in paths}
    if args.output.exists() or len(hashes) != len(paths) or args.seeds < 1:
        raise ValueError("Invalid star experiment")
    tasks = [(str(args.agent.resolve()), str(p.resolve()), seed, seat) for p in args.opponents
             for seed in range(args.seed_start, args.seed_start + args.seeds) for seat in (0, 1)]
    rows = []
    with args.output.with_suffix(".progress.jsonl").open("x") as log:
        with multiprocessing.get_context("fork").Pool(args.workers, maxtasksperchild=1) as pool:
            for row in pool.imap_unordered(game, tasks):
                rows.append(row)
                log.write(json.dumps(row) + "\n")
                log.flush()
                if len(rows) % 12 == 0 or not row["valid_terminal"] or len(rows) == len(tasks):
                    print(json.dumps({"completed": len(rows), "total": len(tasks),
                                      "last_opponent": row["opponent"], "valid": row["valid_terminal"]}), flush=True)
    if {p.stem: evaluator.sha(p) for p in paths} != hashes:
        raise ValueError("Source changed during star experiment")
    rows.sort(key=lambda r: (r["opponent"], r["seed"], r["seat"]))
    result = {"timestamp": datetime.now(timezone.utc).isoformat(), "engine_version": evaluator.__version__,
              "source_hashes": hashes, "engine_sha": evaluator.sha(evaluator.engine.__file__),
              "harness_sha": evaluator.sha(__file__), "game_harness_sha": evaluator.sha(Path(__file__).with_name("evaluate_public_panel.py")),
              "evaluator_sha": evaluator.sha(evaluator.__file__), "seed_start": args.seed_start,
              "seed_count": args.seeds, "seat_swapped": True, "rows": rows,
              "summary": summary(rows), "submission_approval": False}
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
