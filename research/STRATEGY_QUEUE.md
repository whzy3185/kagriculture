# Strategy Queue

All entries are proposals, not approved production changes. Latest controlling
workflow is AGENTS.md (2026-09-08): public-champion-first, one measured increment,
at most one official submission/day. This supersedes the earlier from-scratch
queue. Licensed public source reuse is now explicitly authorized and attributed.
Root main.py and deployed EXP-006 (56072267) remain unchanged.

## Current Decisions - 2026-09-08

- Research champion: Ahmed v23 within the portable Python panel; 1008 screen
  games followed by a 96-seed, both-seat finalist comparison (134-58).
- EXP-20260908-01: purchase-triggered budget check, NO-GO (0-48 on fresh screen).
  No 96-seed candidate run, no competition submission and no same-ID retuning.
- Next-day priority: worker-specific, time-indexed feed/inventory reservations
  before more frequent liquidation. Two rejected-candidate loss traces show
  early cow losses and fewer sold units despite all market requests filling.
- Keep strict market-slot flags separate from observed unit no-ops; do not
  silently erase either to claim zero invalid actions. Any future normalization
  must be backed by the official parser and contract regression tests.
- Native ARA-V2 reproduction remains a coverage limitation, not a measured loss.
  Its binary-only artifact needs a compatible isolated runtime/source review.

Full evidence: reports/OPEN_SOURCE_CHAMPION.md and reports/DAILY_STATUS.md.
Expected gain for the next hypothesis remains UNKNOWN. No next candidate is
authorized by a title or score, and none has been coded today after the rejection.

## Historical Decisions - 2026-09-07

See STRATEGY_DEPTH_20260907.md for reconciled phase telemetry and new priority.
Two existing development seeds, both seats, were remeasured without adding
independent evidence. The four leave-one-out ablations remain only four seed
pairs each; positive mean margins include adverse regimes and no point gains.

| Order | Experiment | Main hypothesis | Status |
|---|---|---|---|
| 1 | EXP-007 early-income crop bridge | Less opening capital lockup improves terminal paired points | GO to implementation; not submission |
| 2 | EXP-008 selective fertilizer | Additional cashable yield exceeds total service/market opportunity cost | BLOCKED on common executor |
| 3 | EXP-009 calendar labor | Fewer missed production deadlines at the same staffing improves points | GO to isolated prototype after EXP-007 freeze |
| 4 | EXP-010 livestock bridge | A funded, serviced herd improves continuation without starving crops | BLOCKED on placement/feed/survival tests |
| 5 | EXP-011 early branching | Public-state branch at 72/144 beats a feasible 180-turn opening control | BLOCKED on credible opening control |

Terminal liquidation remains a mandatory safety feature, but lower-priority
for strength optimization: +648 mean Shape margin in its small ablation,
compared with 84080/130813 deficits in two diagnostic development seeds.
Do not add ablation deltas together or treat these cross-study magnitudes as
causal decomposition. Future tuned generations require a NEW unused holdout.

## Historical EXP-001 Through EXP-005 Designs

The original slots below describe the earlier legacy-parent research phase.
Their old blockers/statuses are historical; they are not the current task queue.
They were not executed as five standalone candidates. EXP-006 later combined
independent crop mechanisms and used separate leave-one-out diagnostics.

Priority formula:
`expected_score_gain * confidence * probability_generalizes * attribution_quality / engineering_cost`.
Numeric inputs are UNKNOWN without a pilot; therefore numeric priority is UNKNOWN.
Below is a provisional evidence/risk order, explicitly not a computed ranking.

## STRAT-001 / EXP-001 - Control And Population Calibration
Hypothesis: The existing baseline's starter win rate overstates field performance.
H0: Baseline point rate is unchanged across declared opponent strata.
H1: It drops materially against deduplicated current and hard reactive strata.
Evidence: Fieldbook reports 0.9948 ordinary vs 0.6322 hard; Island GA reports population-dependent order reversal; our baseline only beat starter.
Quantitative expectation / Expected gain: UNKNOWN; calibration, not an agent improvement.
Confidence: High that opponent choice matters; size for this baseline UNKNOWN.
Engineering cost: Medium; Runtime risk: Low; Meta risk: High.
Experiment: Frozen baseline against a dated fixed/reactive/lineage-balanced panel.
Control: Official starter results; do not tune baseline during comparison.
Success condition: Complete comparable panel, all faults preserved, seed-pair confidence intervals and effective opponent count reported.
Failure condition: Missing source rights, unreconciled replay player/turn mapping, or panel contains copies counted as independent.
Status: BLOCKED - panel and full compliance review incomplete.

## STRAT-002 / EXP-002 - Joint Livestock Value
Hypothesis: Conditional mixed-herd allocation beats fixed cow-heavy allocation when visible egg demand justifies the entire herd's price impact.
H0: Mixed allocation does not improve expected points against the same opponents.
H1: It improves points and paired cash margins in triggered states without damaging other states.
Evidence: Goose Portfolio compares two cows / mixed / two geese; its second-goose guard never activated in its archived 48-game panel, so no causal gain is established.
Quantitative expectation / Expected gain: UNKNOWN; 600/2000-coin buffers are author heuristics, not transplanted parameters.
Confidence: Medium mechanistic plausibility; low effect confidence.
Engineering cost: High; Runtime risk: Medium; Meta risk: High.
Experiment: First validate one shared livestock executor; then change only the allocation rule. Log activation, paid purchases, successful placement, daily feed, filled sales and total herd impact.
Control: Same executor with fixed two-cow choice, not a wholly different crop-only architecture.
Success condition: Positive held-out point effect with enough triggered independent seed pairs and no safety regression.
Failure condition: No activations, purchase/placement mismatch, starvation, or gains vanish under reactive supply.
Status: BLOCKED - common livestock executor and parent not established.

## STRAT-003 / EXP-003 - Land Timing
Hypothesis: Earlier first expansion helps only where funded labor can monetize extra reachable tiles.
H0: Moving first eligible expansion from displayed Day 7 to Day 5 does not improve expected points.
H1: Earlier expansion improves points conditional on a predeclared cash/workload threshold.
Evidence: Official 1000/2000/4000 prices; economic-policy workload constraints; route switching needs compatible asset state.
Quantitative expectation / Expected gain: UNKNOWN; no copying a high agent's final land count.
Confidence: Low effect confidence; Engineering cost: Medium; Runtime risk: Low; Meta risk: Medium.
Experiment: Change only first-land eligibility day, with identical funding/service policy and explicit zero-based day mapping.
Control: Same land-capable policy with Day 7 eligibility.
Success condition: Positive held-out point effect; measured incremental serviced tile-days repay land and extra labor before termination.
Failure condition: Idle expansion, cash starvation, or opposite sign on hard/reactive panel.
Status: BLOCKED - no validated land-capable parent; never stack with livestock first.

## STRAT-004 / EXP-004 - Duplicate Work Reservations
Hypothesis: Reserving current-square tasks as well as destinations reduces duplicate work and improves expected points without increasing labor.
H0: Deduplicating co-located work does not improve points.
H1: It improves points through recovered service capacity at the same hand count.
Evidence: Frozen baseline diagnostic shows repeat WATER/PLANT/HARVEST no-ops; direct co-located-water regression documents the cause. Structured policy describes single-use mission assignment.
Quantitative expectation: Recoverable actions are a measured upper bound, not a cash-gain prediction; freed time may become PASS or travel.
Expected gain: UNKNOWN. Confidence: High for mechanism, UNKNOWN for win effect.
Engineering cost: Low; Runtime risk: Low; Meta risk: Medium.
Experiment: One isolated candidate alters reservation checks only; retain crop, hiring, land, market and liquidation rules.
Control: Exact frozen main.py SHA 712be5af7888bb489c95417e6eb3d16875def7fcaaed31c47715d85e9ad9ae7d.
Success condition: No duplicate effective tasks; positive held-out point effect, reported productive-action replacement and no increased missed deadlines.
Failure condition: No-op reduction merely increases idling, missed crop deadlines or losses.
Status: BLOCKED - engineering paused until research/compliance gate; proposed first strategy pilot after calibration.

## STRAT-005 / EXP-005 - Terminal Cash Conversion
Hypothesis: A horizon-feasible liquidation schedule improves final cash without speculative late production.
H0: Reserving terminal deposit/sale capacity does not improve expected points.
H1: It improves points by monetizing otherwise stranded inventory.
Evidence: Actual Trades distinguishes fills from orders; official terminal reward excludes inventory; Endgame Economics reports seed cutoff positive but static/adaptive hiring failures.
Quantitative expectation / Expected gain: UNKNOWN for this parent. Its wheat planting cutoff already differs from the published control; do not transplant Day 26 blindly.
Confidence: Medium; Engineering cost: Medium; Runtime risk: Low; Meta risk: Medium.
Experiment: Change only terminal deposit-and-sale scheduling; keep seed and hiring rules unchanged. Record incremental sold units, realized prices and displaced work.
Control: Frozen parent terminal policy.
Success condition: Positive held-out point effect with a reconciled per-turn ledger; no extra market-slot truncation or shed overflow.
Failure condition: Own cash gain helps the opponent more, or claimed gain is requested-but-unfilled sales.
Status: BLOCKED - complete market/action accounting and terminal path tests required.

## Shared Preregistration

Proposed screen: 32 development seed pairs x 8 distinct opponent lineages, both
candidate and parent against identical panels (1024 episodes per candidate).
Freeze one challenger before 64 untouched pairs x 8 lineages (2048 episodes).
These are provisional compute/sample sizes, not a claim of statistical power.
Pilot variance and intervention prevalence determine the final sample size.
Primary practical target: +2 percentage points in draw-adjusted score; report
paired cluster uncertainty and reject if evidence does not distinguish benefit.
Do not declare gains from mean bank alone, degenerate intervals or 5-way selection
without a fresh final evaluation. No cumulative combination before independent
contributions and a separate interaction test.
