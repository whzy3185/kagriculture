# Code And Discussion Review - 2026-09-07

Historical initial survey. The latest continuation, exact source ancestry and
independent mechanism decomposition are in OPPONENT_STRATEGY_ATLAS.md and
QUANT_COMPETITION_PROTOCOL.md. The v40 source supersedes the v39 narrative as the
current Structured Economic Policy executable; do not conflate those versions.
Access/Rules blockers below have since been resolved; see reports/GATE_UPDATE_20260907.md.

## Scope And Evidence Labels

Research was performed in Microsoft Edge. Its kaggleusercontent notebook frame
failed, so the original ipynb files were downloaded through Edge and parsed as
JSON without executing them. No third-party agent, model, or action tape was
adopted. Notebook source hashes are recorded in `sources/notebooks.json`.

- 84 distinct Code directory entries: Hotness, Most Votes, Recently Run,
  Public Score, Recently Created; additional searches `reinforcement` and
  `behavior cloning`. Each sorting view's first 20 unpinned entries was scanned,
  not every notebook on the site. Search is not an exhaustive method classifier.
- One additional notebook followed through a source citation: Wins, not money.
- 10 notebooks received targeted original-source/markdown/saved-output review.
  This is not a full security audit or independent re-execution of all code cells.
- All 8 Discussion directory pages scanned: 155 unique topic IDs. Twelve original
  threads and their visible replies reviewed; 48 priority topics indexed. The
  remaining topics are retained as IDs in the coverage manifest, not claimed read.
- Two official datasets inspected: index v39 and 2026-09-06 daily replays.
  No online episode independently replayed or statistically analyzed in this round.
- Live leaderboard observed: HowardLeeTW 2960.4, 3jeonghun 2838.1, Mengfei Li
  2834.7. Display-name transliteration here is for ASCII; scores are a timestamped
  snapshot, not convergence evidence. Do not compare them to historical notebook ratings.

`OFFICIAL_VERIFIED` means the original staff text was read. `SOURCE_VERIFIED`
means an engine rule was inspected. `AUTHOR_REPORTED` means saved output or a
claim was read but not reproduced. `CATALOG_ONLY` means only directory metadata.
An official answer does not verify unrelated community statistics in the same thread.

## Official Clarifications

1. [Final episode set](https://www.kaggle.com/competitions/kaggriculture/discussion/732931):
   Addison Howard and Bovard confirm that episodes across the whole competition
   count only if **both participating submissions are still active** at final evaluation.
   This resolves the ambiguity in the Overview's phrase "those episodes".
2. [Team and ties](https://www.kaggle.com/competitions/kaggriculture/discussion/739410):
   team score uses its better of two agents; a team cannot occupy two ranks;
   ties count as half-wins. Increased post-deadline play frequency is not promised.
3. [Replay permission](https://www.kaggle.com/competitions/kaggriculture/discussion/738837):
   public replays may be used to train, build and inform submissions.
4. [Public code](https://www.kaggle.com/competitions/kaggriculture/discussion/737788):
   staff says freely/publicly available material is permitted. Retain attribution,
   asset licenses and rule review; do not interpret this as relicensing third-party code.
5. [Daily sampling](https://www.kaggle.com/competitions/kaggriculture/discussion/731215):
   daily episodes are ranked by contemporaneous mean agent rating and truncated
   near 20 GB. This is a selected high-rating corpus, not a random ladder sample.
6. [Version boundary](https://www.kaggle.com/competitions/kaggriculture/discussion/735311):
   Aug 15 staff announced scarcity-curve changes for carrot, tomato and egg,
   recommended >=1.32.7 and called it the last planned change except game-breaking
   bugs. [Sep 1 reply](https://www.kaggle.com/competitions/kaggriculture/discussion/737570)
   says parameters do not change mid-competition/final. Record the historical
   discrepancy and treat versions explicitly; do not pool pre/post-patch episodes.
7. [Visual rating bug](https://www.kaggle.com/competitions/kaggriculture/discussion/739699):
   one reported inverted result was contradicted by backend records (+105.8/-4.5).
   Verify backend records, not a screenshot alone. This is not a universal diagnosis.
8. [Whole-run timeout](https://www.kaggle.com/competitions/kaggriculture/discussion/739874):
   a new question, with zero replies when read. Local default runTimeout=1200
   does not establish how hosted agents are scheduled. Hosted interpretation UNKNOWN.

## Notebook Findings

| Source | Method and evidence read | What is reusable as a hypothesis | Limits / decision |
|---|---|---|---|
| [Getting Started](https://www.kaggle.com/code/bovard/kaggriculture-getting-started), v4 | Melon tutorial, observation schema, submission workflow | Baseline correctness and sale price-impact tests | Old internal competition link and string PASS example; use current official contract, not literal tutorial copying |
| [Six-Day Fieldbook](https://www.kaggle.com/code/yhay81/six-day-public-state-fieldbook), v3 | Five 144-turn blocks; 8 route tapes, 30 paths; public-state trees and cash guards | Compare fixed route to boundary routing with identical feasible assets | Author reports 24064 frozen games, 0.9485 point score, CI 0.9371-0.9565; regular panel 0.9948 vs hard panel 0.6322. Not reproduced. Source dataset not audited |
| [X-ray](https://www.kaggle.com/code/destbreso/x-ray-your-agent), v53 | Modal actions, within-world variation, lineage, daily staffing, rating drift; saved run 74 episodes | Diagnose action changes separately from within-world state response; stratify by opponent rating and episode age | Classification is heuristic; first-two-shop grouping leaves later shops and weeds uncontrolled; 1-3 episodes/world is weak evidence |
| [Wins, not money](https://www.kaggle.com/code/destbreso/wins-not-money), v21 | Win objective vs mean margin; author corpus 32570 episodes; 267 submissions with >=30 games; 14 opponents x10 seeds x2 seats | Report actual points, paired margins and per-opponent results; deduplicate lineages | Normal/location-scale model is approximate. Reported field MAE 7.5pp and only 69% within nominal two-SE bands do not establish calibrated probabilities |
| [Really Better?](https://www.kaggle.com/code/hank0123/kaggriculture-is-your-agent-really-better), v1 | Seed-pair bootstrap, strict input validation, raw wins vs half-draw points | Resample whole seed pairs and preserve faults | Its 96 rows/48 pairs and 56.25% points are explicitly SYNTHETIC, not agent evidence. Saved 38 software tests are not competition validation |
| [Actual Trades](https://www.kaggle.com/code/az05192000gmailcom/kaggriculture-from-orders-to-actual-trades), v4 | Unitwise market reconstruction after unit actions; partial fills, cash and shed caps | Attribute filled trades, not requested quantities; reconcile both cash balances | Demo reports 6480 quotes and 1438 player-turns with zero mismatches; one demo, not broad correctness. Net reconciliation can hide offsetting errors |
| [Structured Economic Policy](https://www.kaggle.com/code/pilkwang/kaggriculture-structured-economic-policy) | Shadow prices, funding ledger, greedy jobs, Fibonacci hiring | Complete cash-conversion chain and workload-conditioned labor | Page served v39 of40; latest code version must be checked. Prose on overnight positioning contradicts engine resets; its mean-margin objective is not final point rate |
| [Goose Portfolio](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-goose-portfolio-historical-lb-2615), v2 | Compare 2 cows / cow+goose / 2 geese jointly, including price impact on existing herd | Test marginal portfolio value, not isolated animal ROI; measure intervention activation rate | Historical same-code ratings 2615 vs 1833.3 are not a controlled comparison. 48-game archive produced identical actions with/without the second-goose guard, hence no measured guard effect |
| [Island GA](https://www.kaggle.com/code/destbreso/island-ga-an-owned-schedule-is-a-moat), v18 | Compiler and island search; paired screen/confirm; separate idle/fixed/reactive panels | Separate growth from financing/execution; preserve an independent confirm panel | Author reports +13.2k idle and -13.9k accompanied on same deltas; ordering reversed under population change. Winning executor/schedules withheld; public MIT repo is not equivalent artifact |
| [Graph + RL](https://www.kaggle.com/code/djamilabenchikh/graph-reinforcement-learning), v3 | V16 backbone; 204-node graph, GCN and Double-DQN residual KEEP/delay-sales actions; config 18 training games | Isolate a small market residual from the backbone | Architecture/config review only; no demonstrated independent gain established here. Source sets AUTO_SUBMIT=True; never execute an unreviewed notebook |

All ten notebook pages displayed Apache 2.0. This clears neither every embedded
upstream component nor external datasets/models. No code was adopted. Full
download hashes bind the reviewed files even when a page's selected version is
older than its latest/best version.

## Independent Critiques

- Expected margin is not equivalent to `P(win)+0.5 P(tie)`. The normal-model
  `Phi(mu/sigma)` is a possible surrogate only under checked shape assumptions;
  do not make it the promotion gate. Ties matter under the official final rule.
- Linearity of expectation does **not** imply two policy modifications have
  additive effects. They compete for cash, labor, tiles and market depth. The
  "safe composability under expected margin" argument in Wins, not money is
  not justified. Greedy monotonic improvement is not a global-optimum proof.
- X-ray prose says up to nine shops; official 1.32.7 caps instances at eight.
  It says nothing observable differs before turn 48; `_end_of_day` can spawn
  weeds after the first day. Do not use either blanket claim as a parser invariant.
- Structured policy suggests ending a day near tomorrow's work improves next
  morning position. Official `_end_of_day` resets the farmer at the shed and
  dismisses hands. Reuse assignment ideas only after removing that premise.
- A market order is not a fill. Requested quantity x quoted price overstates
  revenue when stock/cash is insufficient or the price moves during settlement.
- A frozen action stream is a useful controlled opponent but not equivalent to
  a reactive policy on counterfactual seeds/states. Both must be represented.
- Official top replay samples cannot identify the bottom quartile of the full
  ladder. Percentiles must name their sampling frame and contemporaneous rating.

## Current Data And Meta Snapshot

[Official index](https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-index)
v39 has 39 daily rows, July 30 through Sep 6, and CC0 license. Sep 6 contains
662 episodes, 21464632922 uncompressed bytes, top average rating 3017.729278,
median average rating 2862.661763. The daily page reports 663 files including
metadata and 21.46 GB; its JSON preview is explicitly truncated. These are
dataset metadata, not 662 replays independently analyzed here.

The observed notebook mix includes frozen schedules, repairs, public-state
route portfolios, market residuals, GA, RL and diagnostic tooling. This is a
current cross-sectional observation. Without yesterday's equivalent snapshot,
we cannot claim a measured overnight meta shift or infer top-agent internals.

## Next Gate

This survey is now substantive, but the full Rules text still needs an
untruncated review. Candidate engineering remains paused under the user's latest
instruction. `STRATEGY_QUEUE.md` preregisters five independent decisions rather
than claiming five finished experiments. AUTH_BLOCKED also prevents submission.
