"""Validate a complete paired panel before ranking immutable public policies."""

from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import statistics

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def summarize(reports):
    if not reports or len({r["engine_sha"] for r in reports}) != 1 or len({r["evaluator_sha"] for r in reports}) != 1:
        raise ValueError("Missing reports or mismatched measurement implementation")
    hashes, pairs, provenance = {}, defaultdict(list), []
    for report in reports:
        if report["engine_version"] != "1.32.7" or not report["seat_swapped"]:
            raise ValueError("Engine/seat identity mismatch")
        if report["seed_start"] != 2026090800 or report["seed_count"] != 24:
            raise ValueError("Not the registered selection suite")
        for name, sha in report["source_hashes"].items():
            if name in hashes and hashes[name] != sha:
                raise ValueError("Policy source differs between panels")
            hashes[name] = sha
        for row in report["rows"]:
            if not row["valid_terminal"]:
                raise ValueError("Failed game blocks selection; do not drop it")
            names = tuple(sorted((row["candidate"], row["opponent"])))
            pairs[names].append(row)
        provenance.append({k: report[k] for k in ("engine_sha", "evaluator_sha", "harness_sha")})
    names = sorted(hashes)
    if set(pairs) != set(itertools.combinations(names, 2)):
        raise ValueError("Incomplete round-robin coverage")
    comparison, point_rates, win_counts, tails = {}, defaultdict(list), defaultdict(int), defaultdict(list)
    for pair, rows in pairs.items():
        ids = [(r["seed"], r["seat"]) for r in rows]
        expected = {(seed, seat) for seed in range(2026090800, 2026090824) for seat in (0, 1)}
        if len(ids) != 48 or set(ids) != expected:
            raise ValueError("Missing or duplicate paired games")
        for name in pair:
            opponent = next(n for n in pair if n != name)
            points = [r["points"] if r["candidate"] == name else 1-r["points"] for r in rows]
            margins = [r["margin"] if r["candidate"] == name else -r["margin"] for r in rows]
            measured = [r for r in rows if r["candidate"] == name]
            rate = statistics.fmean(points)
            entry = {"games": len(rows), "wins": sum(p == 1 for p in points),
                     "draws": sum(p == .5 for p in points), "points": rate,
                     "mean_margin": statistics.fmean(margins), "median_margin": statistics.median(margins),
                     "p10_margin": float(np.quantile(margins, .1)), "variance": statistics.variance(margins),
                     "directly_instrumented_games": len(measured),
                     "runtime_max": max((r["runtime_max"] for r in measured), default=None),
                     "faults": {k: sum(r["faults"].get(k, 0) for r in measured)
                                for k in sorted({k for r in measured for k in r["faults"]})} if measured else None}
            comparison[name + " vs " + opponent] = entry
            if name != "exp006_independent" and opponent != "exp006_independent":
                point_rates[name].append(rate)
                win_counts[name] += int(rate > .5)
                tails[name].append(entry["p10_margin"])
    ranking = [{"name": name, "mean_public_opponent_points": statistics.fmean(rates),
                "pairwise_wins": win_counts[name], "worst_opponent_p10": min(tails[name])}
               for name, rates in point_rates.items()]
    ranking.sort(key=lambda r: (-r["mean_public_opponent_points"], -r["worst_opponent_p10"], r["name"]))
    first, second = ranking[:2]
    close = (first["pairwise_wins"] == second["pairwise_wins"] or
             first["mean_public_opponent_points"] - second["mean_public_opponent_points"] <= .05)
    return {"status": "SCREEN_COMPLETE_NOT_SUBMISSION_APPROVAL", "games": sum(len(r["rows"]) for r in reports),
            "source_hashes": hashes, "rankings": ranking, "comparisons": comparison,
            "finalists": [first["name"], second["name"]], "requires_96_seed_tiebreak": close,
            "provenance": provenance,
            "limits": ["Related sources are not independent lineages; no population p-value is claimed.",
                       "Fault/runtime metrics are unavailable for reverse rows, never assumed zero.",
                       "Native ARA-V2 excluded; champion scope is the portable Python panel.",
                       "Strict contract flags include deliberately empty market slots; retained separately from terminal failures."]}


if __name__ == "__main__":
    paths = [ROOT / f"experiments/results/PUBLIC-20260908-{name}.json" for name in ("screen", "adaptive")]
    result = summarize([json.loads(p.read_text()) for p in paths])
    result["report_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    with (ROOT / "reports/PUBLIC_PANEL_SUMMARY_20260908.json").open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps({k: result[k] for k in ("status", "games", "rankings", "finalists", "requires_96_seed_tiebreak")}, indent=2))
