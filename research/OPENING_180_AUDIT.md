# Opening 180 Audit

Observed: 2026-09-07. Strong reusable opening schedules are a credible research
baseline; a universal fixed 180-action optimum is NOT established. No agent
changes, copied routes or new submissions in this audit.

Follow-up: STRATEGY_DEPTH_20260907.md now adds exact cash-reconciled phase
telemetry for two existing development seeds against Shape. It supports
prioritizing an independent early-income opening control before comparing
72/144/180 feedback boundaries. No new opening-policy superiority was tested.

## Sources And Limits

- [Closed-loop discussion](https://www.kaggle.com/competitions/kaggriculture/discussion/733002):
  messages 3508844, 3508847 and 3509460 describe stable production-plan meta.
  Community interpretation, not an optimality proof or fresh opening experiment.
- [Determinism/RL](https://www.kaggle.com/competitions/kaggriculture/discussion/737937):
  message 3517810 favors search/planning. Reproducibility conditional on a seed
  does not make future shops or opponent actions known at runtime.
- [X-ray discussion](https://www.kaggle.com/competitions/kaggriculture/discussion/738563):
  message 3518952 reports leader plan divergence from turn 34. AUTHOR_REPORTED;
  action divergence alone proves neither RL nor superiority over a fixed plan.
- [Kaito v58](https://www.kaggle.com/code/kaitofukami/238-238-known-streams-v58-minimax-closed-loop):
  cells 1-3 describe shared-prefix experts branching at 72, 96, 144 and 360.
  These are concrete pre-180 feedback mechanisms, not proof of optimal branches.
- [Findings from Zero to Top Meta](https://www.kaggle.com/code/raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta):
  cell 13 describes five teams' nearly identical routes. Cell 43 reports a weed
  blocking construction at 176 and repair at 177-180, changing one reconstructed
  matchup from -7288 to +3455. Cells 47-50 report opening feed denial addressed
  by moving the existing five-wheat purchase to slot zero. Author-run evidence,
  not independently reproduced here; early execution is not immutable.
- [177/180 Conditional Memory](https://www.kaggle.com/code/kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory):
  cell 0 defines 180 as six trajectories per 30 submissions, 134 unique episodes.
  It is NOT an opening length. The 177 wins are a frozen-replay holdout claim.
- [Live Meta Guide](https://www.kaggle.com/code/cjlcjlcjl/kaggriculture-what-the-top-farms-do-a-live-meta):
  downloaded saved report is August 11, not September 7. Final compositions and
  first-ORDER days do not establish exact opening action agreement or optimality.

Official 1.32.7 _end_of_day draws weeds daily and shops every three days at
24 turns/day: weeds and two shop unlocks can affect the first 180 turns.
Shared-market settlement also couples opening finance to the opponent.

## Quantitative Decision

Treat an independently optimized opening as a control to avoid redundant search.
Do not import another player's tape. Keep identical legality/recovery code in
all variants, and compare the following independently attributable policies:

| Arm | Opening control |
|---|---|
| A | Macro opening through 180; feasibility repairs only |
| B | Same architecture, state-conditioned continuation allowed from 72 |
| C | Same architecture, state-conditioned continuation allowed from 144 |
| D | Fully state-conditioned control |

H0: early branching does not improve terminal paired win/half-draw points over A.
Evaluate the COMPLETE season, not cash at 180. Record terminal margin, liquidity
failures, lost production, runtime and branch activation. Low opening cash may
represent productive capital, not failure. Use a state-valid common continuation
or recompile at the boundary; never graft a position/inventory-incompatible suffix.

Match seeds and seats across independent opponent lineages; cluster uncertainty
by seed. Include feed-purchase pressure, early shop regimes and weed obstruction.
Freeze before untouched holdout. Report per-lineage results, not only pooled means.
Measure field and market agreement separately over [0,72), [72,144), [144,180),
within and between lineages. Copies are not independent confirmations. These
fresh agreement statistics were NOT computed here; percentages remain UNKNOWN.

## Audit Scope

Three notebooks downloaded as JSON only; no third-party cells executed. Targeted
source/markdown review, not full security audit. Raw notebooks remain outside Git.

| Notebook | SHA256 |
|---|---|
| Findings from Zero to Top Meta | a7447511510ed22b73f2315246b6bf4de66f219ffe3ba692a377f3fb47931331 |
| 177/180 Conditional Memory | 32471f25e3bc3c206a0539d8fd08ab3db52db8460c6ab90cac75249c6819e2d5 |
| Live Meta Guide | fec9f3252c35466b503314d5866df9411b7f8485451a3263f855d5ba79d39bf9 |

Five original discussion message trees read: 733002, 737937, 738325, 738563,
736219. The last includes outdated final-episode claims and is not authority
for current scoring rules. Current recent-topic page lists 155 total topics;
only one directory page refreshed, not every reply. Edge browser automation
was unavailable, so official Kaggle API supplied the current source reads.
