from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_045 = ROOT / "reports" / "exp045_vs_current_open_source_6seeds.json"
REPORT_054 = ROOT / "reports" / "exp054_vs_current_open_source_6seeds.json"
OUT_JSON = ROOT / "reports" / "exp045_exp054_open_source_comparison.json"
OUT_MD = ROOT / "reports" / "EXP045_EXP054_VS_CURRENT_OPEN_SOURCE_20260930.md"


def load_games(path: Path, anchor: str, exclude: str) -> dict[tuple[str, int, int], dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["complete"] is True
    assert not payload["errors"]
    games = {}
    for game in payload["games"]:
        if game["agent_a"] != anchor or game["agent_b"] == exclude:
            continue
        key = (game["agent_b"], int(game["seed"]), int(game["seat_a"]))
        games[key] = game
    return games


def wtl(games: list[dict]) -> dict[str, int]:
    counts = Counter(g["outcome_a"] for g in games)
    return {"wins": counts["W"], "ties": counts["T"], "losses": counts["L"]}


def mean(values: list[float]) -> float:
    return statistics.fmean(values)


g045 = load_games(REPORT_045, "EXP045", "EXP054")
g054 = load_games(REPORT_054, "EXP054", "EXP045")
assert set(g045) == set(g054), (set(g045) - set(g054), set(g054) - set(g045))

opponents = sorted({key[0] for key in g045})
rows = []
for opponent in opponents:
    keys = sorted(key for key in g045 if key[0] == opponent)
    a = [g045[key] for key in keys]
    b = [g054[key] for key in keys]
    money_delta = [y["money_a"] - x["money_a"] for x, y in zip(a, b)]
    margin_delta = [y["margin_a"] - x["margin_a"] for x, y in zip(a, b)]
    row = {
        "opponent": opponent,
        "games": len(keys),
        "exp045": {
            **wtl(a),
            "mean_money": mean([g["money_a"] for g in a]),
            "mean_margin": mean([g["margin_a"] for g in a]),
            "min_margin": min(g["margin_a"] for g in a),
        },
        "exp054": {
            **wtl(b),
            "mean_money": mean([g["money_a"] for g in b]),
            "mean_margin": mean([g["margin_a"] for g in b]),
            "min_margin": min(g["margin_a"] for g in b),
        },
        "paired": {
            "mean_money_delta_054_minus_045": mean(money_delta),
            "mean_margin_delta_054_minus_045": mean(margin_delta),
            "money_better_equal_worse": [
                sum(x > 0 for x in money_delta),
                sum(x == 0 for x in money_delta),
                sum(x < 0 for x in money_delta),
            ],
            "margin_better_equal_worse": [
                sum(x > 0 for x in margin_delta),
                sum(x == 0 for x in margin_delta),
                sum(x < 0 for x in margin_delta),
            ],
            "min_money_delta": min(money_delta),
            "max_money_delta": max(money_delta),
        },
    }
    rows.append(row)

all_keys = sorted(g045)
all045 = [g045[key] for key in all_keys]
all054 = [g054[key] for key in all_keys]
all_money_delta = [y["money_a"] - x["money_a"] for x, y in zip(all045, all054)]
all_margin_delta = [y["margin_a"] - x["margin_a"] for x, y in zip(all045, all054)]

summary = {
    "protocol": "same-opponent same-seed same-seat paired comparison",
    "seeds": sorted({key[1] for key in all_keys}),
    "opponents": opponents,
    "games_per_candidate": len(all_keys),
    "exp045": {
        **wtl(all045),
        "match_points": (wtl(all045)["wins"] + 0.5 * wtl(all045)["ties"]) / len(all045),
        "mean_money": mean([g["money_a"] for g in all045]),
        "mean_margin": mean([g["margin_a"] for g in all045]),
        "median_margin": statistics.median(g["margin_a"] for g in all045),
        "min_margin": min(g["margin_a"] for g in all045),
    },
    "exp054": {
        **wtl(all054),
        "match_points": (wtl(all054)["wins"] + 0.5 * wtl(all054)["ties"]) / len(all054),
        "mean_money": mean([g["money_a"] for g in all054]),
        "mean_margin": mean([g["margin_a"] for g in all054]),
        "median_margin": statistics.median(g["margin_a"] for g in all054),
        "min_margin": min(g["margin_a"] for g in all054),
    },
    "paired": {
        "mean_money_delta_054_minus_045": mean(all_money_delta),
        "median_money_delta_054_minus_045": statistics.median(all_money_delta),
        "mean_margin_delta_054_minus_045": mean(all_margin_delta),
        "median_margin_delta_054_minus_045": statistics.median(all_margin_delta),
        "money_better_equal_worse": [
            sum(x > 0 for x in all_money_delta),
            sum(x == 0 for x in all_money_delta),
            sum(x < 0 for x in all_money_delta),
        ],
        "margin_better_equal_worse": [
            sum(x > 0 for x in all_margin_delta),
            sum(x == 0 for x in all_margin_delta),
            sum(x < 0 for x in all_margin_delta),
        ],
        "min_money_delta": min(all_money_delta),
        "max_money_delta": max(all_money_delta),
    },
    "by_opponent": sorted(
        rows,
        key=lambda row: row["paired"]["mean_money_delta_054_minus_045"],
        reverse=True,
    ),
}

OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# EXP045 / EXP054 对当前强力开源包本地对局",
    "",
    "- 官方固定解释器；同对手、同种子、同座位配对。",
    f"- {len(opponents)} 个开源对手，6 个种子，双换位；每个候选 {len(all_keys)} 局。",
    "- 两份原始报告均 complete=true、errors=[]。",
    "",
    "## 总览（已排除 045/054 彼此互打）",
    "",
    "| 包 | 胜-平-负 | 比赛分 | 平均钱数 | 平均分差 | 中位分差 | 最差分差 |",
    "|---|---:|---:|---:|---:|---:|---:|",
    f"| EXP045 | {summary['exp045']['wins']}-{summary['exp045']['ties']}-{summary['exp045']['losses']} | {summary['exp045']['match_points']:.3f} | {summary['exp045']['mean_money']:.1f} | {summary['exp045']['mean_margin']:+.1f} | {summary['exp045']['median_margin']:+.1f} | {summary['exp045']['min_margin']:+.0f} |",
    f"| EXP054 | {summary['exp054']['wins']}-{summary['exp054']['ties']}-{summary['exp054']['losses']} | {summary['exp054']['match_points']:.3f} | {summary['exp054']['mean_money']:.1f} | {summary['exp054']['mean_margin']:+.1f} | {summary['exp054']['median_margin']:+.1f} | {summary['exp054']['min_margin']:+.0f} |",
    "",
    "## 同种子钱数对比",
    "",
    f"- EXP054 - EXP045 平均自身钱数差：{summary['paired']['mean_money_delta_054_minus_045']:+.2f}。",
    f"- 中位自身钱数差：{summary['paired']['median_money_delta_054_minus_045']:+.2f}。",
    f"- 054 自身钱数更高/相同/更低：{summary['paired']['money_better_equal_worse'][0]}/{summary['paired']['money_better_equal_worse'][1]}/{summary['paired']['money_better_equal_worse'][2]}。",
    f"- 054 分差更好/相同/更差：{summary['paired']['margin_better_equal_worse'][0]}/{summary['paired']['margin_better_equal_worse'][1]}/{summary['paired']['margin_better_equal_worse'][2]}。",
    f"- 单局自身钱数差范围：{summary['paired']['min_money_delta']:+.0f} 到 {summary['paired']['max_money_delta']:+.0f}。",
    "",
    "## 分对手明细",
    "",
    "| 对手 | 045胜平负 | 054胜平负 | 045均钱 | 054均钱 | 054-045均钱 | 045均分差 | 054均分差 | 钱数更高/同/低 |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
]
for row in summary["by_opponent"]:
    a = row["exp045"]
    b = row["exp054"]
    p = row["paired"]
    beq = "/".join(str(x) for x in p["money_better_equal_worse"])
    lines.append(
        f"| {row['opponent']} | {a['wins']}-{a['ties']}-{a['losses']} | "
        f"{b['wins']}-{b['ties']}-{b['losses']} | {a['mean_money']:.1f} | "
        f"{b['mean_money']:.1f} | {p['mean_money_delta_054_minus_045']:+.1f} | "
        f"{a['mean_margin']:+.1f} | {b['mean_margin']:+.1f} | {beq} |"
    )

lines += [
    "",
    "## 判定",
    "",
    "胜负泛化能力在本轮完全相同；若只按本轮平均钱数，EXP054 略优。结合此前多种子 Top-7 联赛中 EXP045 的小幅领先，当前更稳妥的主包仍是 EXP045，EXP054 保留为高报价变体。",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(json.dumps(summary, ensure_ascii=False, indent=2))
