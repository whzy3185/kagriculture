"""Reproduce selected public-panel losses with exact source/reward checks."""

import argparse
import hashlib
import json
from pathlib import Path

from compare_selected_replays import profile
from evaluate_public_panel import evaluator, source_loader

ROOT = Path(__file__).resolve().parents[1]


def source(name):
    if not name.isidentifier():
        raise ValueError("Invalid policy identifier")
    for folder in ("agents/candidates", "agents/champion"):
        candidate = ROOT / folder / (name + ".py")
        if candidate.is_file():
            return candidate
    return ROOT.parent / "public-20260908/agents" / (name + ".py")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--reports", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    losses, hashes = [], {}
    for path in args.reports:
        report = json.loads(path.read_text())
        for name, sha in report["source_hashes"].items():
            if name in hashes and hashes[name] != sha:
                raise ValueError("Policy hash disagreement")
            hashes[name] = sha
        for row in report["rows"]:
            if args.candidate not in (row["candidate"], row["opponent"]) or not row["valid_terminal"]:
                continue
            margin = row["margin"] if row["candidate"] == args.candidate else -row["margin"]
            if margin < 0:
                losses.append((margin, row))
    losses.sort(key=lambda item: (item[0], item[1]["seed"], item[1]["seat"]))
    selected, seen = [], set()
    for margin, row in losses:
        key = (row["seed"], row["candidate"], row["opponent"])
        if key not in seen:
            selected.append((margin, row))
            seen.add(key)
        if len(selected) == 2:
            break
    cases = []
    for margin, row in selected:
        opponent = row["opponent"] if row["candidate"] == args.candidate else row["candidate"]
        seat = row["seat"] if row["candidate"] == args.candidate else 1-row["seat"]
        for name in (args.candidate, opponent):
            if evaluator.sha(source(name)) != hashes[name]:
                raise ValueError("Source changed after selection")
        original_make, captured = evaluator.make, []
        def make(*a, **kw):
            env = original_make(*a, **kw)
            captured.append(env)
            return env
        evaluator.make = make
        evaluator.load_agent = source_loader
        try:
            measured = evaluator.run_game(source(args.candidate), str(source(opponent)), row["seed"], seat)
        finally:
            evaluator.make = original_make
        if not measured["valid_terminal"] or measured["margin"] != margin:
            raise ValueError("Diagnostic does not reproduce selected loss")
        data = captured[0].toJSON()
        raw = ROOT / f"replays/raw/{args.candidate}-{opponent}-{row['seed']}-{seat}.json"
        with raw.open("x") as handle:
            json.dump(data, handle, separators=(",", ":"))
        diagnostic, _ = profile(data, seat)
        rival_profile, _ = profile(data, 1-seat)
        cases.append({"seed": row["seed"], "opponent": opponent, "seat": seat,
                      "measurement": measured, "profile": diagnostic, "opponent_profile": rival_profile,
                      "raw_path": str(raw.relative_to(ROOT)), "raw_sha256": hashlib.sha256(raw.read_bytes()).hexdigest()})
        print(json.dumps({"candidate": args.candidate, "opponent": opponent, "seed": row["seed"],
                          "margin": margin, "faults": measured["faults"]}), flush=True)
    result = {"candidate": args.candidate, "source_hashes": hashes, "cases": cases,
              "scope": "Worst selected development losses on distinct seed/opponent cases; no new independent games"}
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
