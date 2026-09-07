# KAGGRICULTURE ROUND 1

## Latest Continuation: EXP-006

The historical handoff below predates authorized implementation and is retained
for provenance. Current status: candidate verified, submission cycle incomplete.
Rules have been read and account entry confirmed in the intervening audit.
Independent EXP-006 completed 96 development and 192 holdout games. Holdout
wins are 64/64 against legacy, 64/64 against starter, and 0/64 against Shape v11.
This supports initial calibration, not a competitive-strength claim.
Four module ablations increased mean margins when restored but did not change
win/loss classes; those contrasts do not establish separate point gains.

Public Kaggle Notebook v2 completed 11 tests and 8 games. Downloaded archive
and all three members match the frozen local sources; maximum call 0.161371 s,
zero monitored faults. All dispatch gates passed; actual submission 56072267
is COMPLETE, with one quota unit consumed and four remaining at check. Initial
score is 600.0, not a converged estimate. The first downloaded episode 106387464
is self-play VALIDATION, rewards 48298 and 49336; not a public win/loss sample.
Root main.py remains unchanged; no PR is created.
See CODEX_VALIDATION_LATEST.md and experiments/results/EXP-006-cloud-verified.json.

## Historical Research Handoff

Status: research handoff; **Round 1 submission cycle NOT COMPLETE**.
Latest user direction prioritized Code/Discussion investigation, quantitative
modeling, Edge, and a new branch without a PR. Strategy engineering remains paused.

## Competition Audit
BLOCKED: untruncated Rules and competition Data/runtime review incomplete.
Kaggle auth: AUTH_BLOCKED. Browser displays Join Competition. Submission
history, parent, pending and remaining quota are UNKNOWN.

## Research
- 84 unique Code directory entries, plus one cited source: 85 indexed total.
- 10 targeted original Notebook reviews; zero third-party notebooks re-executed.
- 155 Discussion titles across all 8 pages; 12 original threads/replies read;
  48 priority topics indexed with unread entries clearly marked.
- Two official dataset metadata pages: index v39 and Sep 6 daily set.
- Online replays independently analyzed: 0. Published statistics are AUTHOR_REPORTED.

## Quantitative Findings
1. Optimize win/half-draw points, not mean cash alone. Phi(mu/sigma) needs checked assumptions.
2. Final BT includes historical active-vs-active episodes only; both agents must
   remain active. Better of the team's two submissions, with half-wins for ties.
3. Top-selected daily replays cannot support whole-ladder bottom-quartile inference.
4. Count fills and marginal price impact, not requested quantities times quotes;
   include joint herd supply, funding, transport and terminal liquidation.
5. Published opponent-stratum splits and non-activating ablations require lineage
   control, activation measurement, untouched seeds and combination tests.

## Baseline - Pipeline Evidence Only
games: 40 unique seed-seat cases (20 seeds), plus one repeatability check.
An earlier uninstrumented run repeated the same 40 cases; do not pool it as 80.
win rate: 100% versus official starter; 40 wins, zero draws/losses.
mean bank: 33755.625; median: 33887.5; std: 621.6578.
mean margin: 30147; median margin: 30332.5; std margin: 652.8768.
runtime: mean callable 0.02597 ms, max 17.9738 ms; instrumented games 51.1488 s,
excluding import/setup. No hosted runtime certification.
unit no-ops: 12596/123359 (10.2108%); comprehensive invalid count UNKNOWN.
Holdout: NOT RUN. New strategy work paused on user correction.

## Experiments
| ID | Hypothesis | Result | Decision |
|---|---|---|---|
| EXP-001 | Field panel changes calibration vs starter | Field panel not run | BLOCKED |
| EXP-002 | Conditional joint herd allocation improves points | No common livestock executor/ablation | BLOCKED |
| EXP-003 | Earlier funded land improves points | Model only; no validated land-capable parent | BLOCKED |
| EXP-004 | Reservations recover useful actions | Defect documented; candidate not coded/run | BLOCKED |
| EXP-005 | Feasible terminal deposit/sale improves points | Sources reviewed; accounting tests pending | BLOCKED |

These are five experiment designs/decisions, not five completed candidate runs.
Our expected gains and numerical priority remain UNKNOWN. Provisional sample
sizes and success/failure conditions are recorded in STRATEGY_QUEUE.md.

## Submissions
Submissions: 0. Ref/status/score: not applicable.
Best approved candidate: NONE. Champion: NOT ESTABLISHED.
Online delta: UNKNOWN. SCORECARD has no fabricated COMPLETE rows.
No promotion; main.py unchanged.

## Negative Evidence
See FAILURE_ANALYSIS.md: duplicate work, weak opponent calibration, published
inactive guard, adverse late hiring and population shifts. No own online
strongest-win/worst-loss analysis is yet possible.

## Repository
Repository: https://github.com/whzy3185/kagriculture
Branch: research/round1-audit-20260907. No new PR or merge.
Baseline source parent: 17f61c15dc001abf8726a57319c5ead245c9ddfd.
Remote task-chain commit: 9e7b88dc54da07487f41783e37366b65c464f718.
Result JSON records local-only 9340feda5ff72ff4193964d65d25393f5aed073d;
its tracked tree matches the remote task-chain commit. Diagnostic code was
uncommitted at execution and separately SHA-bound in that JSON. Do not describe
the local SHA as present on GitHub. Subsequent research commit carries the evidence.

## Next Experiments
1. Finish compliance/data checks and define a rights-cleared, lineage-aware panel.
2. After calibration, run EXP-004 alone; measure useful replacement actions and
   untouched-seed points, not merely fewer no-ops.
3. Reconcile market/terminal accounting before EXP-005; keep herd/land isolated.
   Obtain CLI authorization and competition entry before any actual submission.
