# Strategy Depth Review

## Material Passport
Mode: descriptive validation and experiment prioritization. Date: 2026-09-07.
Sources: official engine 1.32.7, frozen EXP-006 development/ablation evidence,
four remeasured games (two existing development seeds, both seats), OPENING_180_AUDIT.md.
No candidate changed, no new holdout opened, no submission in this analysis.

## 1. Main Finding

EXP-006 is a functioning crop-only calibration agent, not an economically
equivalent rival to Shape v11. Matching a few late sales cannot repair a whole
production-chain deficit. A reusable opening should preserve both operating
cash and productive assets, not optimize cash alone at turn 180.

The diagnostic wraps the existing official-engine evaluator without modifying
it. Terminal rewards, candidate faults, actions and call counts match the four
original development rows exactly. All individual market-unit cash movements,
wages and land purchases reconcile both players' final bank balances.
Raw phase evidence: experiments/results/EXP-006-phase-audit.json.
Derived summaries: experiments/results/STRATEGY-DEPTH-20260907.json.

## 2. What Happens Before Turn 180

| Development seed | Metric at 180 | EXP-006 | Shape v11 |
|---|---|---:|---:|
| 201 | Cash | 267 | 374 |
| 202 | Cash | 267 | 371 |
| both | Gross sales during [0,180) | 0 | 7315 / 7336 |
| both | Owned quadrants | 1 | 2 |
| both | Active hired hands at this intraday snapshot | 4 | 8 |
| both | Planted melons / strawberries | 17 / 8 | 12 / 13 |
| both | Placed cows / sheep | 0 / 0 | 7 / 2 |

EXP-006 has tied up opening capital in slow crops, with no realized revenue by
180 in these cases. Its 3000-coin starting cash is not earning early bridge
income. Shape has already financed a much larger production system despite
similarly low on-hand cash. The difference in cash balances is therefore a
poor proxy for the difference in continuation value. This is a descriptive
whole-policy comparison, not causal attribution to buying any particular herd.

## 3. Complete Cash Accounting

| Seed | Agent | Gross realized sales | All cash spending | Final bank |
|---|---|---:|---:|---:|
| 201 | EXP-006 | 65122 | 15186 | 52936 |
| 201 | Shape | 165542 | 31526 | 137016 |
| 202 | EXP-006 | 70231 | 14921 | 58310 |
| 202 | Shape | 217844 | 31721 | 189123 |

Each bank equals 3000 + sales - spending. Shape's extra gross sales are
100420 / 147613, offset by extra spending of 16340 / 16800, leaving gaps of
84080 / 130813. These are not transferable gains from adding one component.

In seed 201, Shape's fertilizer, milk, wool and egg sales total 80998 while
EXP-006 has no such sales. These are gross receipts, NOT livestock profit:
feed, purchase, service, fertilizer opportunity cost and shared price effects
must be subtracted and some crop work may be displaced. Even existing crop
revenue differs substantially; the deficit is not only missing livestock.

During [360,540), net cash increments are 9947 vs 61116 in seed 201 and
9803 vs 81236 in seed 202. Most separation becomes visible after the opening,
but that timing does not prove the cause is a late-game decision.

## 4. Production And Labor

Seed 201 strawberry sales: EXP-006 sells 242 units from 70 purchased seeds;
Shape sells 262 from 33. Ratios are 3.46 vs 7.94 sold units per seed BOUGHT,
not biological yield estimates: unused seeds, planting and harvesting differ.
Realized strawberry revenue is 43629 vs 51529. In seed 202, EXP-006 sells
271 from 76; Shape again 262 from 33, with revenue 52727 vs 55997.

Official ongoing crops have FOUR production events, not unlimited production.
Tomato events occur at ages 8-11; strawberry at 10,12,14,16. Fertilization on
eligible watered events can raise each event from one to two units, subject
to the four-unit held cap and feasible harvesting. Unit tests verify this
arithmetic under ideal service; they do not establish fertilizer profitability.
EXP-006 contains no FERTILIZE executor. Shape uses one. This identifies a
candidate mechanism, not proof that fertilizer alone explains their difference.

Requested PASS shares: EXP-006 29.21% / 32.34%; Shape 7.39% / 7.39%.
Requested unit-action slots: 5703 / 5733 vs 7149 / 7149. PASS may be rational
waiting; movement is not automatically waste; a non-PASS request is not proof
of successful production. Do not multiply idle slots by a constant coin value.

## 5. Reinterpret The Ablations

These are full policy minus one module, restored against the frozen full policy,
NOT standalone component additions to one common stripped-down baseline.
There are only FOUR development seed pairs per opponent, not eight independent
trials. The following cash-margin effects are relative to Shape:

| Restored module | Mean margin delta | Seed-pair SD | Observed minimum | Point delta |
|---|---:|---:|---:|---:|
| Demand | +34702.25 | 26245.33 | -1047 | 0 |
| Land | +12873 | 25283.76 | -18859 | 0 |
| Labor | +11507.5 | 27624.44 | -18311 | 0 |
| Terminal transport | +648 | 504.34 | +30 | 0 |

Positive mean does NOT imply a positive effect in every regime. Effects cannot
be added: land, labor, pricing and planting interact. No component-level point
gain, broad generalization, p-value, or reliable population interval follows
from this small screen. Preserve negative seed pairs rather than optimizing
against the average only. Terminal hygiene remains a safety feature, but is
not the highest-value strength experiment at the observed scale of losses.

## 6. Revised Independent Architecture

1. Capital allocator: dated receipts and payments, seed/feed/rehire reserves,
   liquidity-shortfall risk and remaining productive horizon. Recognize the
   option value of waiting for a shop; do not read the hidden seed.
2. Production calendar: explicit crop event limits, fertilizer windows, animal
   feed/care/harvest, shed access and replanting. Model the full cash-conversion
   chain and compare alternatives per constrained worker action and tile-day.
3. Feasible scheduler: fund and reserve work before assigning it; honor daily
   respawn, positions, carried resources and recoverable route disruptions.
4. Market executor: marginal realized prices and order priority with quantities
   conserved. Product mix affects the rival's prices; optimize paired points,
   not just our receipts. Buying fertilizer can help a rival selling fertilizer.
5. Sparse public-state feedback: adapt when the expected continuation changes,
   rather than blindly locking 180 steps or rebuilding every action from zero.

Expected price should integrate possible future inventories, E[p(I)], not
silently substitute p(E[I]) under nonlinear curves. That is a model-risk
finding, not a reason to change the frozen submitted baseline without a test.

## 7. Five Decisions And Next Experiments

| Priority / ID | Main variable | Control and gate | Decision |
|---|---|---|---|
| 1 / EXP-007 | Opening allocation to an early-income crop bridge | Frozen EXP-006; same executor, budget safety and later policy; full-season paired points | GO to independent implementation, not submission |
| 2 / EXP-008 | Selective fertilizer service | Common fertilizer-capable executor on/off; price, carry, water and harvest costs included | BLOCKED on shared executor and ledger tests |
| 3 / EXP-009 | Calendar-aware labor assignment | Same crop/land decisions and hand count; measure missed deadlines and actual fills | GO to isolated prototype after EXP-007 freeze |
| 4 / EXP-010 | Small funded livestock bridge | First build and certify a shared executor; compare allocation within it | BLOCKED on feed/placement/survival accounting |
| 5 / EXP-011 | Early public-state branching | Common feasible macro baseline; 72/144/180 boundaries, no incompatible suffix graft | BLOCKED on credible opening control |

For each efficacy trial: predeclare H0 of no positive terminal point effect,
development budget, seeds, lineage panel, activation and safety metrics. Freeze
one candidate before a NEW unused holdout. The old 3001-3032 suite is now
historical evidence, not a fresh holdout for later tuned generations. No new
submission until actual gates pass. Numeric expected gains remain UNKNOWN;
priority is engineering judgment from observed bottlenecks, not a fitted score.

## 8. Statistical And Provenance Limits

11 fallacy checks: stratify opponents (Simpson); no field-wide inference
(ecological); repeated seats/replayed seeds not independent (pseudoreplication);
whole-policy comparison confounded; selected opponent panel does not define
ladder base rates; no before/after rating improvement claim (regression to mean);
no failed games dropped (survivorship); report all four ablations (look-elsewhere);
label this exploratory (forking paths); no causal component attribution;
early assets and later success can share causes (reverse-causality caution).

Only two diagnostic seeds and one strong reference lineage were examined in
detail. These four reruns add ZERO independent trial count to the development
suite. No third-party Notebook was executed. Reference runs had no credentials
and network was disabled. The frozen agent and evaluator are unchanged.
