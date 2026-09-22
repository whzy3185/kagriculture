"""Export standings and a match-point matrix from a round-robin JSON report."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--standings", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    args = parser.parse_args()

    report = json.loads(args.report.resolve().read_text(encoding="utf-8"))
    standings = report["standings"]
    labels = [row["agent"] for row in standings]
    points: dict[tuple[str, str], float] = {}
    records: dict[tuple[str, str], str] = {}
    for row in report["pairwise"]:
        a, b = row["agent_a"], row["agent_b"]
        points[a, b] = float(row["match_points_a"])
        points[b, a] = 1.0 - float(row["match_points_a"])
        records[a, b] = f"{row['wins_a']}-{row['ties']}-{row['losses_a']}"
        records[b, a] = f"{row['losses_a']}-{row['ties']}-{row['wins_a']}"

    args.standings.resolve().parent.mkdir(parents=True, exist_ok=True)
    with args.standings.resolve().open("w", encoding="utf-8", newline="") as handle:
        columns = [
            "rank", "agent", "games", "wins", "ties", "losses", "match_points",
            "wilson95_low", "wilson95_high", "mean_margin", "median_margin",
        ]
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows({key: row[key] for key in columns} for row in standings)

    with args.matrix.resolve().open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["agent", *labels])
        for a in labels:
            writer.writerow(
                [a, *["--" if a == b else f"{points.get((a, b), 0.0):.3f} ({records.get((a, b), 'NA')})" for b in labels]]
            )

    print("| Rank | Agent | W-T-L | MP | Mean margin | H2H wins-ties-losses |")
    print("|---:|---|---:|---:|---:|---:|")
    for row in standings:
        h2h_wins = h2h_ties = h2h_losses = 0
        agent = row["agent"]
        for opponent in labels:
            if opponent == agent or (agent, opponent) not in points:
                continue
            value = points[agent, opponent]
            if value > 0.5:
                h2h_wins += 1
            elif value < 0.5:
                h2h_losses += 1
            else:
                h2h_ties += 1
        print(
            f"| {row['rank']} | {agent} | {row['wins']}-{row['ties']}-{row['losses']} | "
            f"{row['match_points']:.3f} | {row['mean_margin']:+.1f} | "
            f"{h2h_wins}-{h2h_ties}-{h2h_losses} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
