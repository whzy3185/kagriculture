# Gold-band research, 2026-09-30

Start with `GOLD_STRATEGY_REVIEW_20260930.md` for the live leaderboard, cross-game interpretation and a minimal EXP054 integration plan. See `GOLD_REPLAY_MECHANICS_20260930.md` for detailed verified ledgers and events.

## Included evidence

- `provenance.json`: official replay URLs, IDs, timestamps, raw hashes and evidence limits
- `gold_replay_features.json`: compact per-game statistics, costs, daily layouts and validation results
- `daily_layouts.csv`: daily money/layout/shops/prices in seat order
- `overflow_fixtures.json`: original observations/actions and exact item-level overflow events for review, not proof of a defect in EXP054
- `analyze_exact.py`: continuously replay original actions through the fixed official interpreter and record successful unit trades, physical events and overflow
- `build_report.py`: derive compact statistics, fixtures and the mechanics report
- `reference/kaggriculture.py`, `reference/kaggriculture.json`: the repository's frozen official game engine and rules, preserved for portable reconstruction

## Reproduction

Use the source links in `provenance.json`. On each official Game History, select that episode and use More actions → Download replay. Save it as the listed `raw_filename` here. Verify the raw SHA256 before reproducing.

Run from this directory with Python 3:

    python -B analyze_exact.py episode115649229.json episode115650653.json episode115653683.json episode115648413.json
    python -B build_report.py

Raw JSONs and generated `episode*_exact.json` are intentionally excluded from the small repository bundle. The analysis expects 720 recorded frames, DONE/DONE and zero mismatches for all 719 transitions per game; the output's `mismatches` list is decisive. It compares game observations, not execution runtime timing. `build_report.py` requires raw inputs and generated exact files.

The original replay's opponent private state is available for retrospective accounting. The proposed runtime agent must use only its legal observation, never the opponent's hidden inventory, future action sequence, future shop sequence or episode seed.

No strategy was changed or submitted as part of this research. Repository integration is separate from a claim that a candidate is validated or recommended.
