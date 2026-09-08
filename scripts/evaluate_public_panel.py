"""Unmodified public-source round robin with paired seeds and isolated workers."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import inspect
import itertools
import json
import multiprocessing
from pathlib import Path
import signal
import statistics

import numpy as np
import experiment_eval as evaluator
from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parents[1]


def source_loader(path, disabled=()):
    if disabled:
        raise ValueError("Public benchmark must not modify a policy")
    fn = get_last_callable(Path(path).read_text(), path=str(Path(path).resolve()))
    parameters = len(inspect.signature(fn).parameters)
    return lambda obs, config: fn(obs, config) if parameters >= 2 else fn(obs)


def timeout(signum, frame):
    raise TimeoutError("Public game exceeded 180 seconds")


def game(task):
    a, b, seed, seat = task
    evaluator.load_agent = source_loader
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(180)
    try:
        row = evaluator.run_game(a, b, seed, seat)
        row["candidate"] = Path(a).stem
        return row
    except Exception as error:
        return {"candidate": Path(a).stem, "opponent": Path(b).stem, "seed": seed,
                "seat": seat, "valid_terminal": False, "error_type": type(error).__name__}
    finally:
        signal.alarm(0)


def summary(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["candidate"], row["opponent"])].append(row)
    result = {}
    for (a, b), games in groups.items():
        entry = {"games": len(games), "valid": all(r["valid_terminal"] for r in games)}
        if entry["valid"]:
            margins = [r["margin"] for r in games]
            entry.update(wins=sum(r["points"] == 1 for r in games),
                         draws=sum(r["points"] == .5 for r in games),
                         points=statistics.fmean(r["points"] for r in games),
                         mean_margin=statistics.fmean(margins), median_margin=statistics.median(margins),
                         p10_margin=float(np.quantile(margins, .1)), variance=statistics.variance(margins),
                         runtime_max=max(r["runtime_max"] for r in games),
                         monitored_faults={k: sum(r["faults"].get(k, 0) for r in games)
                                           for k in sorted({k for r in games for k in r["faults"]})})
        result[a + " vs " + b] = entry
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agents", nargs="+", type=Path, required=True)
    parser.add_argument("--seed-start", type=int, required=True)
    parser.add_argument("--seeds", type=int, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--legacy-smoke-provenance", type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.seeds < 1 or len(args.agents) < 2:
        raise ValueError("Invalid benchmark or existing output")
    if len({p.stem for p in args.agents}) != len(args.agents):
        raise ValueError("Ambiguous policy labels")
    hashes = {p.stem: evaluator.sha(p) for p in args.agents}
    tasks = [(str(a.resolve()), str(b.resolve()), seed, seat)
             for a, b in itertools.combinations(args.agents, 2)
             for seed in range(args.seed_start, args.seed_start + args.seeds) for seat in (0, 1)]
    rows = []
    progress = args.output.with_suffix(".progress.jsonl")
    checkpoint = args.output.with_suffix(".checkpoint.json")
    identity = {"source_hashes": hashes, "seed_start": args.seed_start, "seed_count": args.seeds,
                "engine_sha": evaluator.sha(evaluator.engine.__file__),
                "evaluator_sha": evaluator.sha(evaluator.__file__)}
    harness_sha = evaluator.sha(__file__)
    prior_harness = harness_sha
    if args.resume:
        if checkpoint.exists():
            saved = json.loads(checkpoint.read_text())
            if saved["identity"] != identity:
                raise ValueError("Checkpoint identity changed")
            prior_harness = saved["initial_harness_sha"]
        elif args.legacy_smoke_provenance:
            prior = json.loads(args.legacy_smoke_provenance.read_text())
            for key in ("source_hashes", "engine_sha", "evaluator_sha"):
                if prior[key] != identity[key]:
                    raise ValueError("Legacy checkpoint source/engine mismatch")
            prior_harness = prior["harness_sha"]
            if prior_harness != "c61288bf1547a607ffd7915e285cc5721daf01521cc13770b84f5f32082f0589":
                raise ValueError("Unrecognized legacy checkpoint harness")
        else:
            raise ValueError("Resume requires checkpoint provenance")
        rows = [json.loads(line) for line in progress.read_text().splitlines()]
        for row in rows:
            row.setdefault("measurement_harness_sha", prior_harness)
    elif progress.exists() or checkpoint.exists():
        raise ValueError("Checkpoint exists; use explicit validated resume")
    key = lambda r: (r["candidate"], r["opponent"], r["seed"], r["seat"])
    expected = {(Path(a).stem, Path(b).stem, seed, seat) for a, b, seed, seat in tasks}
    done = {key(r) for r in rows}
    if len(done) != len(rows) or not done <= expected:
        raise ValueError("Duplicate or foreign checkpoint games")
    pending = [t for t in tasks if (Path(t[0]).stem, Path(t[1]).stem, t[2], t[3]) not in done]
    checkpoint.write_text(json.dumps({"identity": identity, "initial_harness_sha": prior_harness,
                                     "current_harness_sha": harness_sha}, indent=2) + "\n")
    print(json.dumps({"resumed": len(rows), "remaining": len(pending), "total": len(tasks)}), flush=True)
    with progress.open("a" if args.resume else "x") as log:
        # Each worker handles one game: bundled modules and policy state cannot leak to another game.
        with multiprocessing.get_context("fork").Pool(args.workers, maxtasksperchild=1) as pool:
            for row in pool.imap_unordered(game, pending):
                row["measurement_harness_sha"] = harness_sha
                rows.append(row)
                log.write(json.dumps(row) + "\n")
                log.flush()
                if len(rows) % 12 == 0 or not row["valid_terminal"] or len(rows) == len(tasks):
                    print(json.dumps({"completed": len(rows), "total": len(tasks),
                                      "last_pair": [row["candidate"], row["opponent"]],
                                      "valid": row["valid_terminal"]}), flush=True)
    if {p.stem: evaluator.sha(p) for p in args.agents} != hashes:
        raise ValueError("Policy source changed during benchmark")
    rows.sort(key=lambda r: (r["candidate"], r["opponent"], r["seed"], r["seat"]))
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "engine_version": evaluator.__version__,
              "engine_sha": evaluator.sha(evaluator.engine.__file__), "source_hashes": hashes,
              "harness_sha": evaluator.sha(__file__), "evaluator_sha": evaluator.sha(evaluator.__file__),
              "measurement_harness_shas": sorted({r["measurement_harness_sha"] for r in rows}),
              "seed_start": args.seed_start, "seed_count": args.seeds, "seat_swapped": True,
              "scope": "Public round robin; candidate-side faults measured, not opponent-side fault counts",
              "summary": summary(rows), "rows": rows, "submission_approval": False}
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
