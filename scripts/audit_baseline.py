"""Instrument the unchanged baseline using the installed official interpreter.

Only the official unit-action function is wrapped, never reimplemented. No-op
counts exclude PASS and do not mean schema-invalid actions. Market no-ops and
atomic rejected PLANT requests are not fully covered, so this is not a gate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import time

from kaggle_environments import __version__, make
from kaggle_environments.envs.kaggriculture import kaggriculture as game

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def distribution(values):
    return {
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "std": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def run_episode(seed, seat, steps):
    spec = importlib.util.spec_from_file_location("isolated_baseline", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    env = make("kaggriculture", configuration={"episodeSteps": steps, "seed": seed})
    actions, noops = Counter(), Counter()
    timings = []
    exceptions = 0
    schema_errors = 0
    original_unit = game._apply_unit_action
    original_interpreter = env.interpreter
    current_farms = []

    def measured_agent(obs):
        nonlocal exceptions, schema_errors
        start = time.perf_counter()
        try:
            action = module.agent(obs)
            json.dumps(action, allow_nan=False)
            if (not isinstance(action, dict)
                    or any(not isinstance(action.get(k), list) for k in ("farmer", "hands", "market"))):
                schema_errors += 1
            return action
        except Exception:
            exceptions += 1
            raise
        finally:
            timings.append(time.perf_counter() - start)

    def tracked_unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
        ours = len(current_farms) > seat and farm is current_farms[seat]
        before = deepcopy((farm, private)) if ours else None
        result = original_unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        if ours:
            op = action[0] if isinstance(action, list) and action else "MALFORMED"
            actions[op] += 1
            if op != "PASS" and before == (farm, private):
                noops[op] += 1
        return result

    def tracked_interpreter(state, environment):
        nonlocal current_farms
        current_farms = state[0].observation.farms
        return original_interpreter(state, environment)

    env.interpreter = tracked_interpreter
    game._apply_unit_action = tracked_unit
    start = time.perf_counter()
    try:
        players = ["starter", "starter"]
        players[seat] = measured_agent
        env.run(players)
    finally:
        game._apply_unit_action = original_unit
    elapsed = time.perf_counter() - start
    final = env.steps[-1]
    statuses = [s.status for s in final]
    rewards = [s.reward for s in final]
    valid = statuses == ["DONE", "DONE"] and all(isinstance(x, (int, float)) for x in rewards)
    record = {
        "seed": seed, "seat": seat, "statuses": statuses,
        "recorded_states": len(env.steps), "agent_calls": len(timings),
        "ours": rewards[seat], "opponent": rewards[1 - seat],
        "valid_terminal": valid, "exceptions": exceptions, "schema_errors": schema_errors,
        "actions": dict(actions), "unit_noops": dict(noops),
        "market_invalid_actions": "UNKNOWN", "atomic_plant_rejections": "UNKNOWN",
        "runtime_seconds": distribution(timings), "wall_seconds": elapsed,
    }
    # Hash state/action trajectory without logs: timing logs are nondeterministic.
    trajectory = [[{"observation": s.observation, "action": s.action,
                    "status": s.status, "reward": s.reward} for s in step] for step in env.steps]
    record["trajectory_sha256"] = hashlib.sha256(
        json.dumps(trajectory, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", type=Path, default=ROOT / "configs/round1_seeds.json")
    parser.add_argument("--split", choices=["fixed", "holdout"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    suite = json.loads(args.suite.read_text())
    assert set(suite["fixed"]).isdisjoint(suite["holdout"])
    assert all(len(suite[k]) == len(set(suite[k])) for k in ("fixed", "holdout"))
    if args.output.exists():
        raise SystemExit("Refusing to overwrite evidence; choose a new output path")
    rows = []
    for seed in suite[args.split]:
        for seat in suite["seats"]:
            row = run_episode(seed, seat, suite["episode_steps"])
            rows.append(row)
            print(json.dumps({k: row[k] for k in ("seed", "seat", "ours", "opponent", "unit_noops", "valid_terminal")}), flush=True)
    repeat = run_episode(suite[args.split][0], 0, suite["episode_steps"])
    reproducible = repeat["trajectory_sha256"] == rows[0]["trajectory_sha256"]
    valid = all(r["valid_terminal"] for r in rows)
    margins = [r["ours"] - r["opponent"] for r in rows] if valid else []
    pair_means = [statistics.fmean(margins[i:i + 2]) for i in range(0, len(margins), 2)]
    result = {
        "exp_id": "EXP-000", "split": args.split, "suite_id": suite["suite_id"],
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "artifact_sha": sha(ROOT / "main.py"), "evaluator_sha": sha(__file__),
        "seed_suite_sha": sha(args.suite), "environment_version": __version__,
        "environment_sha": sha(game.__file__), "opponent": "official starter",
        "games": len(rows), "repeatability_check_games": 1,
        "repeatability_pass": reproducible, "valid_terminals": valid,
        "win_rate": sum(m > 0 for m in margins) / len(margins) if margins else None,
        "score": distribution([r["ours"] for r in rows]) if valid else None,
        "margin": distribution(margins) if margins else None,
        "paired_seed_mean_margin": distribution(pair_means) if pair_means else None,
        "invalid_action_count": "UNKNOWN: semantic market and atomic validation incomplete",
        "runtime_scope": "Local callable wall time only; not Kaggle sandbox certification",
        "submission_decision": "NO-GO", "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
    if not valid or not reproducible:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
