# EXP067 first-three-Pizza wheat route

Date: 2026-09-30

Status: promoted local candidate; packaged for repository sync; not submitted to Kaggle.

## Failure signal

The largest inspected EXP054 failure, official episode `115058783` against Happy Farm, unlocks `PIZZA_SHOP` on days 3, 6, and 9. Those shops consume wheat, milk, and tomato, but EXP054 still expands strawberry from 20 to 33 planted tiles on day 11. The score gap starts widening before the later tomato conversion, making the early crop mix the more plausible intervention point.

EXP067 inherits EXP066 and activates only when the first three public unlocked shops are exactly three Pizza Shops. From steps 216 through 287 it redirects at most six new strawberry seed/plant actions to wheat. It does not alter existing crops, movement, harvest, animals, sales, or any other shop route.

## Dose selection

On the exact Happy Farm tape:

| Candidate | Margin | Delta vs EXP066 |
|---|---:|---:|
| EXP066 | -44,082 | 0 |
| W4 | -47,798 | -3,716 |
| W6 | -41,157 | +2,925 |
| W8 | -41,651 | +2,431 |
| W10 | -41,212 | +2,870 |
| W13 | -53,997 | -9,915 |
| W16 | -53,997 | -9,915 |

The response is strongly dose-sensitive. W6 was selected instead of the slightly stronger five-seed W10 result because it produced the best official-tape improvement with the smaller intervention.

On five independently scanned first-three-Pizza seeds, paired seats versus EXP066:

| Candidate | W-L | Mean margin |
|---|---:|---:|
| W4 | 9-1 | +595.2 |
| W6 | 9-1 | +481.6 |
| W8 | 7-3 | +204.2 |
| W10 | 9-1 | +759.1 |
| W13 | 7-3 | +518.4 |

The seeds were selected only by the public shop-route condition, not by candidate outcome.

## Official failure-tape regression

Across eight locally available official heavy-loss replays, W6 changed three cases and left five exact:

- Episode `115058783`: -44,082 to -41,157, delta +2,925.
- Episode `114826333`: -5,671 to -4,639, retaining EXP066's +1,032 wool-flush gain.
- Episode `114924649`: -4,347 to -4,047, retaining EXP066's +300 wool-flush gain.
- Other five episodes: exact equality to EXP054/EXP066 as applicable.

The eight-case mean margin improves from -12,761.625 to -12,229.5, an average +532.125. No loss flips to a win, so this is a partial failure reduction rather than a solved matchup.

## Broad and targeted local simulation

Regular strong open-source pool, six seeds and paired seats:

- Against 12 open-source packages: 134 wins, 0 ties, 10 losses.
- Directly against EXP066: 12 ties.
- Mean margin over the full 156-game slate, including the 12 direct ties: +9,217.5.
- This is exactly the EXP066 result on the regular pool, showing no observed broad-pool regression.

Targeted first-three-Pizza pool, five seeds, paired seats, against Farm2945, MarketSmart, MultiRoute, Peak2950, RankAgentV11, and V43:

- EXP066: 54 wins, 6 losses.
- EXP067-W6: 57 wins, 3 losses.
- Outcome transitions: 3 loss-to-win, 54 win-to-win, 3 loss-to-loss, 0 win-to-loss.
- Mean paired margin delta: +726.75.
- Every opponent has a positive mean paired margin delta, ranging from +258.2 to +1,332.6.

Unselected fresh direct check, 40 seeds and paired seats:

- 80 games: 2 wins, 76 ties, 2 losses versus EXP066.
- Mean margin: exactly 0.
- The four non-ties are two seat-mirrored pairs (`±68`, `±564`), so paired-seat aggregate is neutral.

## Decision

Promote W6 as EXP067, ahead of EXP066 for local packaging. The gate is public and narrow, the official failure delta is positive, the targeted route test has no win-to-loss flips, and the regular pool remains unchanged. Keep EXP066 as the rollback package until EXP067 receives live Kaggle evidence.

Known limitations:

- The first-three-Pizza targeted set has only five distinct seeds.
- The official eight-case set is loss-conditioned and not an unbiased leaderboard sample.
- Tests use the current local official-interpreter reproduction; no new live Kaggle result is included.

## Reproducible artifacts

- `reports/exp067_happy_tape_full.json`
- `reports/exp067_pizza3_holdout5.json`
- `reports/exp067_w6_official8.json`
- `reports/exp067_w6_vs_current_open_source_6seeds.json`
- `reports/exp067_pizza3_strong6_candidate.json`
- `reports/exp067_pizza3_strong6_baseline.json`
- `reports/exp067_pizza3_strong6_paired_delta.json`
- `reports/exp067_w6_vs_exp066_fresh40.json`
