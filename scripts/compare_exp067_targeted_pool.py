import argparse
import json
from collections import defaultdict
from pathlib import Path


OPEN_SOURCE = {
    "RankAgentV11",
    "Farm2945",
    "Peak2950",
    "MarketSmart",
    "V43",
    "MultiRoute",
}


def load_games(path: Path, anchor: str):
    payload = json.loads(path.read_text(encoding="utf-8"))
    games = {}
    for game in payload["games"]:
        if game["agent_a"] != anchor or game["agent_b"] not in OPEN_SOURCE:
            continue
        key = (game["agent_b"], game["seed"], game["seat_a"])
        games[key] = game
    return games


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    candidate = load_games(args.candidate, "EXP067_W6")
    baseline = load_games(args.baseline, "EXP066")
    if candidate.keys() != baseline.keys():
        missing_candidate = sorted(set(baseline) - set(candidate))
        missing_baseline = sorted(set(candidate) - set(baseline))
        raise SystemExit(
            f"pairing mismatch: missing_candidate={missing_candidate}, "
            f"missing_baseline={missing_baseline}"
        )

    rows = []
    by_opponent = defaultdict(list)
    for key in sorted(candidate):
        cand = candidate[key]
        base = baseline[key]
        row = {
            "opponent": key[0],
            "seed": key[1],
            "seat_a": key[2],
            "candidate_money": cand["money_a"],
            "baseline_money": base["money_a"],
            "candidate_opponent_money": cand["money_b"],
            "baseline_opponent_money": base["money_b"],
            "candidate_margin": cand["margin_a"],
            "baseline_margin": base["margin_a"],
            "delta_own_money": cand["money_a"] - base["money_a"],
            "delta_opponent_money": cand["money_b"] - base["money_b"],
            "delta_margin": cand["margin_a"] - base["margin_a"],
            "candidate_outcome": cand["outcome_a"],
            "baseline_outcome": base["outcome_a"],
        }
        row["changed"] = bool(
            row["delta_own_money"] or row["delta_opponent_money"]
        )
        rows.append(row)
        by_opponent[key[0]].append(row)

    def summarize(group):
        n = len(group)
        flips = defaultdict(int)
        for row in group:
            flips[f'{row["baseline_outcome"]}->{row["candidate_outcome"]}'] += 1
        return {
            "games": n,
            "changed_games": sum(row["changed"] for row in group),
            "mean_delta_own_money": sum(row["delta_own_money"] for row in group) / n,
            "mean_delta_opponent_money": sum(row["delta_opponent_money"] for row in group) / n,
            "mean_delta_margin": sum(row["delta_margin"] for row in group) / n,
            "candidate_wins": sum(row["candidate_outcome"] == "W" for row in group),
            "baseline_wins": sum(row["baseline_outcome"] == "W" for row in group),
            "outcome_transitions": dict(sorted(flips.items())),
        }

    result = {
        "candidate": str(args.candidate),
        "baseline": str(args.baseline),
        "paired_games": len(rows),
        "overall": summarize(rows),
        "by_opponent": {
            opponent: summarize(by_opponent[opponent])
            for opponent in sorted(by_opponent)
        },
        "changed_rows": [row for row in rows if row["changed"]],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["overall"], indent=2))
    for opponent, summary in result["by_opponent"].items():
        print(opponent, json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
