"""Reduce hash-bound descriptive telemetry and matched ablations."""

from collections import defaultdict
import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments/results"


def load(name, provenance):
    path = RESULTS / name
    payload = path.read_bytes()
    provenance[name] = hashlib.sha256(payload).hexdigest()
    return json.loads(payload)


def summarize(provenance):
    report = load("EXP-006-phase-audit.json", provenance)
    cases = []
    for row in report["rows"]:
        own = row["evaluation"]["seat"]
        case = {"seed": row["evaluation"]["seed"], "candidate_seat": own, "players": {}}
        for label, seat in (("candidate", own), ("reference", 1 - own)):
            flows = [f for f in row["flows"] if f["seat"] == seat]
            actions = [a for a in row["requested_unit_actions"] if a["seat"] == seat]
            gross = sum(f["cash_delta"] for f in flows if f["op"] == "SELL")
            costs = -sum(f["cash_delta"] for f in flows if f["op"] != "SELL")
            total = sum(a["count"] for a in actions)
            idle = sum(a["count"] for a in actions if a["op"] == "PASS")
            phase_flows = {}
            for window in ("0:72", "72:144", "144:180", "180:360", "360:540", "540:719"):
                phase_flows[window] = {
                    "sales": sum(f["cash_delta"] for f in flows if f["phase"] == window and f["op"] == "SELL"),
                    "net_cash": sum(f["cash_delta"] for f in flows if f["phase"] == window)}
            products = {}
            for item in sorted({f["item"] for f in flows if f["op"] == "SELL"}):
                trades = [f for f in flows if f["op"] == "SELL" and f["item"] == item]
                units = sum(f["filled_units_or_events"] for f in trades)
                revenue = sum(f["cash_delta"] for f in trades)
                seeds = sum(f["filled_units_or_events"] for f in flows if f["op"] == "BUY_SEED" and f["item"] == item)
                products[item] = {"sold_units": units, "sales_cash": revenue,
                                  "realized_price": revenue / units if units else None,
                                  "seeds_bought": seeds, "sold_units_per_seed_bought": units / seeds if seeds else None}
            case["players"][label] = {"gross_sales": gross, "cash_costs": costs,
                                      "terminal_cash": 3000 + gross - costs,
                                      "requested_action_slots": total, "pass_slots": idle,
                                      "pass_fraction": idle / total,
                                      "phase_flows": phase_flows, "products": products,
                                      "snapshots": {t: values[seat] for t, values in row["snapshots"].items()}}
        cases.append(case)
    development = load("EXP-006-development-full.json", provenance)
    indexed = {(r["opponent"], r["seed"], r["seat"]): r for r in development["rows"]}
    ablations = {}
    for flag in ("DEMAND_AWARE", "EXPAND_LAND", "ADAPTIVE_LABOR", "TERMINAL_CASH"):
        ablation = load("EXP-006-ablation-" + flag + ".json", provenance)
        if ablation["agent_sha"] != development["agent_sha"] or ablation["disabled"] != [flag]:
            raise ValueError("Ablation identity mismatch")
        groups = defaultdict(lambda: defaultdict(list))
        for row in ablation["rows"]:
            parent = indexed[(row["opponent"], row["seed"], row["seat"])]
            if not row["valid_terminal"] or not parent["valid_terminal"]:
                raise ValueError("Failed game cannot be dropped from comparison")
            groups[row["opponent"]][row["seed"]].append(
                (row["seat"], parent["margin"] - row["margin"], parent["points"] - row["points"]))
        ablations[flag] = {}
        for opponent, seeds in groups.items():
            if any(sorted(r[0] for r in pair) != [0, 1] for pair in seeds.values()):
                raise ValueError("Missing/duplicate ablation seat")
            deltas = [statistics.fmean(r[1] for r in pair) for pair in seeds.values()]
            points = [statistics.fmean(r[2] for r in pair) for pair in seeds.values()]
            ablations[flag][opponent] = {"seed_pairs": len(deltas), "mean_margin_delta": statistics.fmean(deltas),
                                         "seed_pair_std": statistics.stdev(deltas),
                                         "min_seed_pair_delta": min(deltas), "max_seed_pair_delta": max(deltas),
                                         "mean_point_delta": statistics.fmean(points)}
    return {"scope": "Exploratory; diagnostic replays are existing development cases, not new independent trials",
            "unique_diagnostic_seeds": len({c["seed"] for c in cases}), "cases": cases,
            "leave_one_out_restoration": ablations, "source_sha256": provenance,
            "causal_limit": "Whole-policy cash differences do not isolate opening, fertilizer, livestock or timing effects"}


if __name__ == "__main__":
    destination = RESULTS / "STRATEGY-DEPTH-20260907.json"
    data = summarize({})
    with destination.open("x") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"diagnostic_seeds": data["unique_diagnostic_seeds"],
                      "ablations": data["leave_one_out_restoration"]}, indent=2))
