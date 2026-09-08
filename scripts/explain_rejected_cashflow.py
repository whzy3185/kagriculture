"""Cash-reconcile already observed rejected-candidate losses; no new efficacy test."""

import json
from pathlib import Path

from analyze_strategy_phases import run_diagnostic
from evaluate_public_panel import evaluator, source_loader
from replay_public_case import source

ROOT = Path(__file__).resolve().parents[1]


def main():
    selected = json.loads((ROOT / "research/EXP-20260908-01-losses.json").read_text())
    evaluator.load_agent = source_loader
    rows, overview = [], []
    for case in selected["cases"]:
        row = run_diagnostic(source(selected["candidate"]), str(source(case["opponent"])), case["seed"], case["seat"])
        if row["evaluation"]["margin"] != case["measurement"]["margin"]:
            raise ValueError("Cash diagnostic changed the recorded outcome")
        rows.append(row)
        totals = {}
        for label, seat in (("candidate", case["seat"]), ("parent", 1-case["seat"])):
            flows = [f for f in row["flows"] if f["seat"] == seat]
            sales = sum(f["cash_delta"] for f in flows if f["op"] == "SELL")
            costs = -sum(f["cash_delta"] for f in flows if f["op"] != "SELL")
            totals[label] = {"sales": sales, "costs": costs, "bank": 3000+sales-costs,
                             "by_category": {op: sum(f["cash_delta"] for f in flows if f["op"] == op)
                                             for op in sorted({f["op"] for f in flows})}}
        overview.append({"seed": case["seed"], "seat": case["seat"], "totals": totals})
        print(json.dumps(overview[-1]), flush=True)
    with (ROOT / "research/EXP-20260908-01-cashflows.json").open("x") as handle:
        json.dump({"scope": "Two selected worst development losses remeasured, not independent evidence",
                   "overview": overview, "rows": rows}, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
