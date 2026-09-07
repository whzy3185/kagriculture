# Opponent Strategy Atlas

Updated 2026-09-07. Objective: compete with the mechanisms, not copy their agents.
This is a research decomposition, not a set of implementations or proven counters.
Fourteen distinct notebooks have now received targeted review, including five
fresh source pulls that resolve versions, ancestry and runtime decision logic.

## Clean-Room Boundary

- Do not incorporate opponents' source, encoded experts, action tapes, weights,
  route fragments or fitted decision thresholds into our agent.
- Record exact opponent thresholds only as evidence about that opponent. They
  are not defaults for our implementation.
- Learn game economics from the official environment. Develop our controllers
  from an explicit objective, observable state, constraints and our own tests.
- Public executable agents may later be isolated evaluation references after
  license/security checks. Attribution stays attached; their wins are not ours.
- No behavior-cloning objective that trains our policy to reproduce a public
  agent's action sequence. Opponent flow forecasting is a separate allowed model,
  using legal runtime features, not a substitute name for copying its policy.
- A licensed fork can be legitimate. Ancestry is used for statistical deduplication,
  not as an accusation of misconduct.

## Factor The Strategy, Not The Marketing Name

An agent is a combination of dimensions, not one exclusive label:

| Dimension | Questions / observable quantities |
|---|---|
| Production | crop mix; herd mix; maturity calendar; committed future units by product |
| Capital | initial commitments; cash buffer; expansion timing; feed and wage obligations |
| Labor | marginal hire cost; feasible task capacity; routing; useful work vs requested commands |
| Market | filled quantities; supply concentration; quote impact; sale order and timing |
| Inventory | carried versus shed stock; pickup dependencies; overflow; terminal convertibility |
| Control | fixed clock plan; local repair; periodic route switch; online optimization |
| Memory | decision memory versus cache only; per-game reset and seat isolation |
| Training/search | hand-designed, tree selection, RL, evolutionary search; not an economic strategy by itself |

Stateless is not the same as unresponsive: a stateless policy can react to every
observation. A stateful route selector can remain mostly scheduled. Action-trace
variation alone does not establish either causal responsiveness or internal memory.

## M01 - Concentrated Premium Production

Sources: [official tutorial](https://www.kaggle.com/code/bovard/kaggriculture-getting-started),
[V17 market/storage](https://www.kaggle.com/code/boatlee/v17-r1-rc2-high-score-10c-4s-market-storage).

Mechanism: commit cash and tile-days to large premium output, then monetize it.
Melon-only production and recurring livestock are different financing paths,
but both can be exposed to the same crowded premium-price curves.

Quantitative state: expected units reaching sale before horizon; public market
inventory; remaining demand; feed costs; occupied tile-days; marginal worker actions.
Apparent strength: high base-price yield and efficient recurring production.
Failure condition: marginal revenue after our and rival supply no longer repays
seed/feed/labor, or capital cannot bridge the first-yield delay.

Independent counter hypothesis: select our marginal production against projected
joint supply and demand, instead of sharing an already-crowded product. A switch
is justified only by incremental expected points and cashable value, not variety.
Falsifier: gains disappear with rival reaction, or added logistics exceed the
price-diversification benefit. No fixed cow/sheep/crop counts transplanted.

## M02 - Three-Day Funding And A Sparse Route Switch

Source: [Three-Day Shop Router](https://www.kaggle.com/code/yhay81/three-day-shop-router), v7.
Source inspected: policy.cpp cell 4, budget-guard header cell 6, manifest cell 17.

Verified mechanism: 72-turn financing boundaries; one route decision at step
360. Alternate route condition is first shop BAKERY and fertilizer inventory
<=10232.5, or PET_CAFE and rival planted tiles <=64.5. Integer state makes the
effective cutoffs 10232 and 64. Those are opponent facts, not our parameters.
Context stores selected_route, so this controller has decision memory.

Funding model: planned costs over the next block, protected starting resources,
then sell excess stock if estimated cash is insufficient. Both anticipated sale
receipts and product-purchase costs use current quotes. Extra funding sales may
be moved ahead of other orders.

Quantitative concern: q*p(I) is not integrated sale proceeds. The guard can
overestimate current cash realizability and underestimate future feed costs;
its failure to credit future sales can also make it overly conservative. The
net error's sign is state-dependent, so it must be measured, not assumed.

Independent counter hypothesis: model financing stress from public market and
visible commitments, and choose our production/sale timing only when the margin
benefit exceeds our own liquidity cost. Test responsive opponents, not tapes.
Falsifier: guard shortfall is rare, its repairs absorb the error, or our timing
change reduces our own value more than the rival's.

## M03 - Prefix-Compatible Routes With Capacity Repair

Source: [Shape the Shop](https://www.kaggle.com/code/tetsutani/shape-the-shop-work-the-pasture-kaggriculture), v11.
Decoded source was inspected without execution; SHA256
2b97e2c653018ac4aeffb8463ec91c8f26b097b4cef81289acc25ccdbc68f916.

Verified mechanism: four stored route tails and three decision checkpoints
(226, 360, 433), using Yarn Store, carrot price and milk inventory. The selected
tail must match the already-executed prefix. The current route persists in Agent.cur.
Daily-close repair targets 99 of 100 shed items; other layers repair weed no-ops,
clamp sells to projected shed stock and sell stock with no remaining planned sale.

Quantitative concern: closeout projections use requested harvest/feed/place/buy
commands; actual maturity, resource availability, duplicate work and partial
fills can change the projection. A one-slot reserve is not a calibrated bound
on that error. Dropping a SELL also changes later market order positions.

Independent counter hypothesis: value inventory capacity and sale timing from
actual feasible fills and service completion, and exploit opportunities only
when our benefit survives a responsive closeout policy.
Falsifier: residual capacity errors never bind or improved own cash funds the
rival's sales more than ours. Do not copy the 99-slot rule or route checkpoints.

## M04 - Six-Day Public-State Portfolio

Source: [Six-Day Fieldbook](https://www.kaggle.com/code/yhay81/six-day-public-state-fieldbook), v3.
Five 144-turn blocks, eight route tapes and 30 possible paths are author-described.
The attached separated source dataset has not been fully audited; exact deployed
tree predicates and all resource compatibility guarantees remain UNKNOWN here.

Evidence: author reports 24064 frozen-release games and 0.9485 draw-adjusted
points; regular panel 0.9948 versus hard panel 0.6322. Not independently reproduced.

Strength: amortize expensive planning offline, retain option-compatible branches
and make decisions at useful economic milestones.
Failure hypothesis: a small route library lacks a good continuation in some
reachable demand/rival-supply states. This is not proved by being finite alone.
Independent counter: our own feasible plans generated from the economic model;
evaluate value of additional decision opportunities against their compute cost.
Falsifier: the existing library already spans relevant states, or more frequent
planning merely adds noisy switches and destroys financing compatibility.

## M05 - Public-Signature Minimax Experts

Original source: [Kaito v58](https://www.kaggle.com/code/kaitofukami/238-238-known-streams-v58-minimax-closed-loop), v11.
Derivative: [Structured Economic Policy](https://www.kaggle.com/code/pilkwang/kaggriculture-structured-economic-policy), v40.

Critical lineage correction: v40 explicitly forks Kaito's controller unchanged
apart from attribution and a loader shim. It is NOT an independent economic
scheduler merely because that notebook retained its older title. Earlier v39
economic prose must not be assigned to the latest executable.

Static byte check independently found the complete 315484-character original
core verbatim inside the v40 source, preceded by 1512 characters of magic/header
and followed by a 579-character loader shim. Runtime equivalence was not executed.

Verified original-source SHA256:
b041058ec187a8d0a01edc0eab8de068b53deca3e6c1973faf74ace6916ddcb9.
Source inspected: _v58_recovery_mode, _v58_known_yarn, mirror test, warm-up and
the final agent function. Several branches use exact tuples of public cash,
wheat market inventory and rival assets. Other decisions use second shops and
a 240-turn public-farm equality streak. Decision points include 72, 96, 144,
360. Experts remain synchronized and can contain their own local repair logic.
This is offline-selected robust continuation plus runtime routing, not an
unrestricted minimax search recomputed over the whole game every turn.

Evidence: 238/238 known frozen development games is explicitly retrospective.
The author's fresh dynamic comparison versus v57 is 2 wins / 8 ties / 2 losses
(50% points), despite +998 mean cash margin. That is not universal dominance.

Independent counter hypotheses:
1. Use independently generated economically viable openings outside narrow
   signature regions; measure both branch activation and our opportunity cost.
2. Where public observations alias different rival continuations, use a
   calibrated uncertainty set rather than pretending to identify the hidden suffix.
Falsifier: fallback experts are equally strong, or the changed opening costs
more than any lost best-response coverage. Only legally reachable game states
count; editing observations is not a competitive experiment.

## M06 - Premium SELL Preemption And Terminal Recovery

Source: [V17-R1-RC2](https://www.kaggle.com/code/boatlee/v17-r1-rc2-high-score-10c-4s-market-storage), v3.
Production backbone is described as 10 cows/4 sheep on three quadrants, with
next-turn premium sales pulled forward under a visible rival-structure gate.
Late handlers redirect otherwise-PASS carriers near the shed and liquidate
reachable stock. These overlays do not establish a new production architecture.

Evidence: reported deduplicated holdout 138 wins/2 losses in 140 games, seven
references and ten seeds, using **1.32.6**. Source acknowledges lower live-ladder
performance and a missing adaptive-opponent class. One animal escape remained.
The headline result is not transferable to today's 1.32.7 field without retesting.

Independent counter: price our feasible SELL timing jointly with opponent
response, market-slot order and terminal transport. A purely static block-order
calculation is a mechanism test, not proof against an adaptive seller.
Falsifier: advance sales consume working capital/stock needed later, or the rival
also advances and the expected edge disappears.

## M07 - Joint Cow/Goose Portfolio Valuation

Source: [Goose Portfolio](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-goose-portfolio-historical-lb-2615), v2.
Compare the incremental value of two cows, a mixed pair and two geese, including
price impact on the existing herd. Purchase must be followed by compatible
build/pickup/placement, feeding, care, harvest and sale.

Author thresholds 600/2000 projected coins and a 0.35 future-shop demand weight
are not measured constants of the game and will not be adopted.
The archived 48-game panel did not activate the second-goose guard. It therefore
does not measure that guard's causal effect. Same-code ratings 2615 versus
1833.3 do not supply an ablation either.

Independent counter: jointly price our and rival herd supply instead of valuing
one animal in isolation. Include feed acquisition and feasible labor, not just
nominal recurring yield. Refit uncertainty from independent data.
Falsifier: demand-sensitive reallocations fail to install/feed successfully or
lose their marginal value when other producers make the same allocation.

## M08 - Learned Market Residual

Source: [Graph + RL](https://www.kaggle.com/code/djamilabenchikh/graph-reinforcement-learning), v3.
Architecture/configuration reviewed: V16 backbone, 204-node graph, GCN and
Double-DQN KEEP versus delayed premium-sale actions; 18 training games configured.
Weights, full training trace and independent generalization are not established.
AUTO_SUBMIT=True appears in the notebook; no notebook code was executed.

Independent counter: evaluate a responsive sale policy under inventory, demand
and rival-supply regimes absent from its development set. An RL label does not
prove either strength or weakness; training objective and support matter.
Falsifier: apparent improvement vanishes on fresh seeds/opponents or depends on
impossible states. Do not transplant weights, labels or delay fractions.

## M09 - Search-Generated Plans / End-To-End RL

Sources: [Island GA](https://www.kaggle.com/code/destbreso/island-ga-an-owned-schedule-is-a-moat)
and [PPO retrospective](https://www.kaggle.com/competitions/kaggriculture/discussion/738619).
These describe ways to generate controllers, not a unique crop/livestock policy.
The GA's strongest executor and winning schedules are withheld; the public
method must not be treated as that private artifact. PPO's plateau/compute
figures are author reports, not reproduced measurements here.

Quantitative lesson: a fitness panel defines a population. Reported idle-bank
gain reversed with a rival present; a different opponent population reversed
base ordering. A fixed tiny seed screen can also exaggerate the selected winner.
Independent counter: construct our own planning/search process with paired
current-engine duels, holdout lineages/time, and population sensitivity analysis.
Falsifier: the improvement survives only its own screen population.

## What This Changes In Our Work

1. Correctness fixes are necessary but are not automatically competitive gains.
2. Build an opponent **mechanism coverage matrix**, then select distinct source
   lineages. Do not count a renamed fork as another independent opponent.
3. Keep recorded streams as historical diagnostics only. They cannot test a
   rival's response to a counterfactual market decision.
4. First proposed competitive questions are integrated-price financing,
   demand-conditioned production and robustness to reactive rival responses.
5. Every counter remains HYPOTHESIS until a frozen, attributable experiment
   improves held-out point rate without violating safety/resource constraints.
