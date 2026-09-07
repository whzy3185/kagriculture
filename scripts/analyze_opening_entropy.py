#!/usr/bin/env python3
"""Quantify Kaggriculture replay opening entropy and strategy lineages.

This script is intentionally dependency-free. It accepts directories/files containing
Kaggle replay JSON/JSONL records and produces turn-level action entropy plus compact
fingerprints for the first N turns of every seat.

Typical Kaggle-notebook usage:

    python scripts/analyze_opening_entropy.py \
        --input /kaggle/input/kaggriculture-top10-replay-archive \
        --out-dir /kaggle/working/opening_entropy \
        --max-turn 180

Outputs:
- opening_entropy.csv
- opening_conditional_entropy.csv
- opening_turn_classes.csv
- lineages.csv
- summary.json

The parser is deliberately tolerant of wrappers used by different public replay
archives. A record is considered an episode when a dict containing ``steps`` is found.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple


SHOP_KEYS = {
    "shops",
    "townshops",
    "town_shops",
    "unlockedshops",
    "unlocked_shops",
    "townshop",
    "town_shop",
}


def canonical(value: Any) -> str:
    """Return a stable JSON representation suitable for counting/hashing."""
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except TypeError:
        return repr(value)


def iter_json_files(inputs: Sequence[str]) -> Iterator[Path]:
    seen: set[Path] = set()
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            candidates = list(path.rglob("*.json")) + list(path.rglob("*.jsonl"))
        elif path.is_file():
            candidates = [path]
        else:
            continue
        for candidate in sorted(candidates):
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield candidate


def iter_records(path: Path) -> Iterator[Any]:
    """Yield JSON values from .json or line-delimited .jsonl files."""
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
        return

    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return

    if isinstance(payload, list):
        # A list may itself be `steps`, but public archives more commonly store a
        # list of episode records. Yield each item and let `find_episode` decide.
        for item in payload:
            yield item
    else:
        yield payload


def find_episode(value: Any, depth: int = 0) -> Optional[Mapping[str, Any]]:
    """Find the first nested mapping with a list-valued ``steps`` field."""
    if depth > 6:
        return None
    if isinstance(value, Mapping):
        steps = value.get("steps")
        if isinstance(steps, list) and steps:
            return value
        # Common wrappers first.
        for key in ("episode", "replay", "data", "result"):
            if key in value:
                found = find_episode(value[key], depth + 1)
                if found is not None:
                    return found
        # Fall back to a shallow recursive search.
        for child in value.values():
            if isinstance(child, (Mapping, list)):
                found = find_episode(child, depth + 1)
                if found is not None:
                    return found
    elif isinstance(value, list):
        for child in value:
            found = find_episode(child, depth + 1)
            if found is not None:
                return found
    return None


def find_shop_signature(value: Any, depth: int = 0) -> Optional[str]:
    """Extract a stable public shop-state signature from an observation if present."""
    if depth > 5:
        return None
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).replace("-", "_").lower()
            compact = normalized.replace("_", "")
            if normalized in SHOP_KEYS or compact in {k.replace("_", "") for k in SHOP_KEYS}:
                return canonical(child)
        for child in value.values():
            if isinstance(child, (Mapping, list)):
                found = find_shop_signature(child, depth + 1)
                if found is not None:
                    return found
    elif isinstance(value, list):
        for child in value:
            found = find_shop_signature(child, depth + 1)
            if found is not None:
                return found
    return None


def episode_id(episode: Mapping[str, Any], fallback: str) -> str:
    for key in ("id", "episodeId", "episode_id", "ref"):
        value = episode.get(key)
        if value is not None:
            return str(value)
    return fallback


def shannon_entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total <= 0:
        return 0.0
    h = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            h -= p * math.log2(p)
    return h


def normalized_entropy(counter: Counter[str]) -> float:
    k = len(counter)
    if k <= 1:
        return 0.0
    return shannon_entropy(counter) / math.log2(k)


def entropy_stats(counter: Counter[str]) -> Dict[str, Any]:
    total = sum(counter.values())
    if total <= 0:
        return {
            "n": 0,
            "distinct": 0,
            "entropy_bits": 0.0,
            "normalized_entropy": 0.0,
            "mode_action": "",
            "mode_count": 0,
            "mode_share": 0.0,
        }
    mode_action, mode_count = counter.most_common(1)[0]
    return {
        "n": total,
        "distinct": len(counter),
        "entropy_bits": shannon_entropy(counter),
        "normalized_entropy": normalized_entropy(counter),
        "mode_action": mode_action,
        "mode_count": mode_count,
        "mode_share": mode_count / total,
    }


def weighted_conditional_entropy(groups: Mapping[str, Counter[str]]) -> float:
    total = sum(sum(counter.values()) for counter in groups.values())
    if total <= 0:
        return 0.0
    return sum(
        (sum(counter.values()) / total) * shannon_entropy(counter)
        for counter in groups.values()
        if counter
    )


def fingerprint(actions: Sequence[str], turns: int) -> str:
    payload = "\n".join(actions[:turns]).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:20]


def extract_episode_seats(
    episode: Mapping[str, Any],
    ep_id: str,
    max_turn: int,
) -> List[Dict[str, Any]]:
    steps = episode.get("steps")
    if not isinstance(steps, list) or not steps:
        return []

    seat_count = 0
    for step in steps:
        if isinstance(step, list):
            seat_count = max(seat_count, len(step))
    if seat_count == 0:
        return []

    seats: List[Dict[str, Any]] = []
    for seat in range(seat_count):
        actions: List[str] = []
        shops: List[Optional[str]] = []
        for turn, step in enumerate(steps[:max_turn]):
            if not isinstance(step, list) or seat >= len(step):
                actions.append(canonical(None))
                shops.append(None)
                continue
            state = step[seat]
            if not isinstance(state, Mapping):
                actions.append(canonical(None))
                shops.append(None)
                continue
            actions.append(canonical(state.get("action")))
            observation = state.get("observation")
            shops.append(find_shop_signature(observation))

        seats.append(
            {
                "episode_id": ep_id,
                "seat": seat,
                "actions": actions,
                "shops": shops,
            }
        )
    return seats


def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def classify_turn(mode_share: float, entropy_bits: float, conditional_gain: float) -> str:
    # Conservative labels. They are triage hints, not claims of optimality.
    if mode_share >= 0.95 and entropy_bits <= 0.25:
        return "FREEZE_CANDIDATE"
    if conditional_gain >= 0.20:
        return "CONDITIONAL_CANDIDATE"
    return "OPEN_OR_LINEAGE_MIXED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, help="Replay file or directory; repeatable")
    parser.add_argument("--out-dir", default="results/opening_entropy")
    parser.add_argument("--max-turn", type=int, default=180)
    parser.add_argument("--fingerprint-turns", type=int, nargs="+", default=[120, 180])
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    max_turn = max(1, args.max_turn)
    fp_turns = sorted({n for n in args.fingerprint_turns if n > 0})

    turn_counts: Dict[int, Counter[str]] = defaultdict(Counter)
    conditional_counts: Dict[int, Dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    lineage_rows: List[Dict[str, Any]] = []

    files_seen = 0
    records_seen = 0
    episodes_seen = 0
    seats_seen = 0

    for path in iter_json_files(args.input):
        files_seen += 1
        for record_index, record in enumerate(iter_records(path)):
            records_seen += 1
            episode = find_episode(record)
            if episode is None:
                continue
            episodes_seen += 1
            ep_id = episode_id(episode, f"{path.name}:{record_index}")
            for seat_record in extract_episode_seats(episode, ep_id, max_turn):
                seats_seen += 1
                actions = seat_record["actions"]
                shops = seat_record["shops"]
                for turn, action in enumerate(actions):
                    turn_counts[turn][action] += 1
                    signature = shops[turn] if turn < len(shops) else None
                    if signature is not None:
                        conditional_counts[turn][signature][action] += 1

                row: Dict[str, Any] = {
                    "episode_id": ep_id,
                    "seat": seat_record["seat"],
                    "turns_observed": len(actions),
                    "source_file": str(path),
                }
                for n in fp_turns:
                    row[f"fp_{n}"] = fingerprint(actions, n)
                lineage_rows.append(row)

    entropy_rows: List[Dict[str, Any]] = []
    conditional_rows: List[Dict[str, Any]] = []
    class_rows: List[Dict[str, Any]] = []

    for turn in range(max_turn):
        stats = entropy_stats(turn_counts[turn])
        cond_groups = conditional_counts.get(turn, {})
        cond_h = weighted_conditional_entropy(cond_groups) if cond_groups else stats["entropy_bits"]
        conditional_gain = max(0.0, stats["entropy_bits"] - cond_h)

        entropy_rows.append({"turn": turn, **stats})
        conditional_rows.append(
            {
                "turn": turn,
                "unconditional_entropy_bits": stats["entropy_bits"],
                "shop_conditional_entropy_bits": cond_h,
                "entropy_reduction_bits": conditional_gain,
                "shop_states_observed": len(cond_groups),
                "n_with_shop_signature": sum(sum(c.values()) for c in cond_groups.values()),
            }
        )
        class_rows.append(
            {
                "turn": turn,
                "mode_share": stats["mode_share"],
                "entropy_bits": stats["entropy_bits"],
                "shop_entropy_reduction_bits": conditional_gain,
                "classification": classify_turn(
                    float(stats["mode_share"]),
                    float(stats["entropy_bits"]),
                    float(conditional_gain),
                ),
            }
        )

    lineage_fields = ["episode_id", "seat", "turns_observed", "source_file"] + [f"fp_{n}" for n in fp_turns]
    write_csv(
        out_dir / "opening_entropy.csv",
        ["turn", "n", "distinct", "entropy_bits", "normalized_entropy", "mode_action", "mode_count", "mode_share"],
        entropy_rows,
    )
    write_csv(
        out_dir / "opening_conditional_entropy.csv",
        [
            "turn",
            "unconditional_entropy_bits",
            "shop_conditional_entropy_bits",
            "entropy_reduction_bits",
            "shop_states_observed",
            "n_with_shop_signature",
        ],
        conditional_rows,
    )
    write_csv(
        out_dir / "opening_turn_classes.csv",
        ["turn", "mode_share", "entropy_bits", "shop_entropy_reduction_bits", "classification"],
        class_rows,
    )
    write_csv(out_dir / "lineages.csv", lineage_fields, lineage_rows)

    lineage_summaries: Dict[str, List[Dict[str, Any]]] = {}
    for n in fp_turns:
        counts = Counter(row[f"fp_{n}"] for row in lineage_rows)
        lineage_summaries[str(n)] = [
            {"fingerprint": fp, "seats": count, "share": count / seats_seen if seats_seen else 0.0}
            for fp, count in counts.most_common()
        ]

    summary = {
        "files_seen": files_seen,
        "records_seen": records_seen,
        "episodes_seen": episodes_seen,
        "seats_seen": seats_seen,
        "max_turn": max_turn,
        "fingerprint_turns": fp_turns,
        "lineages": lineage_summaries,
        "caveat": (
            "Low action entropy demonstrates convergence of the sampled public meta, not global optimality. "
            "Copied lineages can make entropy artificially small; always compare multiple dates and source families."
        ),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(json.dumps({k: summary[k] for k in ("files_seen", "records_seen", "episodes_seen", "seats_seen")}, indent=2))
    print(f"wrote: {out_dir}")
    return 0 if seats_seen else 2


if __name__ == "__main__":
    raise SystemExit(main())
