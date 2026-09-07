# Strategy Queue

All entries: research-to-experiment proposals, not approved production changes.
Continuation: source review expanded to 14 unique notebooks. User requires
independent mechanism competition, not reuse of public agent/tape/weight/threshold
artifacts. Research questions CQ-01 through CQ-05 in QUANT_COMPETITION_PROTOCOL.md
are the current conceptual queue. The older EXP slots below remain unexecuted.
Access blockers are resolved; full competitive and publication gates are not.
Latest user instruction: finish Code/Discussion investigation first. No candidate
was authored or executed after that instruction. Main remains byte-identical.

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
