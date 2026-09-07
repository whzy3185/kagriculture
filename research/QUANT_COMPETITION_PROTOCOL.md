# Quantitative Competition Protocol

The user's current direction is research-first, mechanism decomposition and
independent competition, not copying. No new candidate is approved by this document.

## 1. Define The Estimand

For policy pi, opponent policy rho, seed z and seat s, let terminal cash margin
be M(pi,rho,z,s). Define points q=1 for M>0, 0.5 for M=0, otherwise 0.

```
J(pi; w) = sum_over_opponent_lineages w[l] * E_seed,seat[q(pi, rho_l)]
Delta J = J(candidate; w) - J(frozen_parent; w)
```

Weights describe a declared opponent population, not confidence derived from
notebook popularity. Report several plausible weight scenarios because the
future field is unknown. Keep raw wins/ties/losses and margins alongside points.
Final BT uses eligible active-vs-active episodes, so this is an offline strength
estimand, not a formula that predicts a specific leaderboard rating.

Mean cash and mean margin are diagnostic/screening quantities. For a constant
positive margin shift and a continuous no-tie model, additional wins come only
from games whose original margin was between minus that shift and zero.
Improving already-large wins need not improve points. Discrete ties must be
handled with the exact point function, not this continuous approximation.

## 2. State, Observability And Uncertainty

At decision time, use our own private inventory, public farms, market and shops,
and legitimate past observations. Do not read rival private stock, hidden seed,
future shops, opponent identity, submission ID or evaluation lineage labels.

Forecast rival production as a distribution, not a known tape. The set of
opponents consistent with current public state may contain opposite best
responses. More classifier complexity cannot recover information not present.

Market conservation gives a useful partial observation:

```
Delta I = own_above_floor_sales + rival_above_floor_sales
          - own_buys - rival_buys - town_consumption
rival_net_above_floor_flow = Delta I - own_above_floor_sales
                            + own_buys + town_consumption
```

Our quantities must be **actual fills**, not requested orders. The residual
does not separately identify rival buys and sales for wheat/fertilizer. Floor
sales add no inventory, so even for other goods it cannot identify all sales.
Use intervals and explicitly identify the remaining unobservable components.

## 3. Value The Complete Cash-Conversion Chain

For each independently generated plan, model:

```
funding -> buy -> acquire carried input -> travel -> service/production
        -> harvest -> carried stock -> shed -> filled SELL -> terminal bank
```

Expected profit includes all dated purchases, feed, wages, marginal price impact,
land and service opportunity costs. Feasibility includes survival, maturation,
capacity, market slots, action budgets and termination. Unsold assets are not cash.
Fertilizer can reach melon's yield cap earlier but does not bypass first-yield
harvest age. End-of-day positions reset; hands must be rehired.

For a single seller with no demand or competing transactions:
`R(q,I)=sum(k=0..q-1) p(I+k)` gives integrated sale cash, with the floor convention
handled by the official engine. State inventory itself stops increasing on
floor-price sales. This reference does not describe a general simultaneous duel.

| 50-unit sale from equilibrium | Quote budget | Integrated cash | Shortfall |
|---|---:|---:|---:|
| Milk | 8000 | 5430 | 2570 (32.125% of quote budget) |
| Strawberry | 6000 | 3648 | 2352 (39.2%) |
| Wool | 10000 | 7655 | 2345 (23.45%) |
| Melon | 12500 | 12098 | 402 (3.216%) |

These were calculated with official 1.32.7 market_price, not with a public
agent. They show a possible financing-model error, not a measured counter win.
There are no town purchases, other trades, production costs or labor in this
reference. The full nine-product table is in quantitative/market_reference.json.

Against two precommitted sale blocks only, the gain from selling x before the
rival's q instead of after is R(x,I)-R(x,I+q). Their corresponding loss is the
same telescoping difference, so relative margin moves by twice that quantity.
Do not transfer this static result to interleaved same-slot orders, changing
quantities, town demand or an opponent that reacts to our timing.

## 4. Turn Source Findings Into Tests

| ID | Estimand / H0 | Independent alternative | Measurement and falsifier |
|---|---|---|---|
| CQ-01 | Integrated financing does not improve held-out points | Our own fill-aware working-capital model | Funding error, activation and points; reject if gains are only predicted cash |
| CQ-02 | Demand/supply-conditioned production does not improve points | Our independently generated crop/herd plan under shared-price forecasts | Sold units, net contribution, service feasibility; reject on reactive-supply reversal |
| CQ-03 | Economically viable opening diversity does not improve points vs narrow public-signature routers | Independent near-equivalent openings, no copied checkpoints/thresholds | Rival branch coverage, own opportunity cost, paired points; reject if fallback is as strong |
| CQ-04 | Capacity-aware terminal conversion does not improve points | Our own feasible deposit/sale schedule, not a copied 99-slot rule | Actual sold cash, overflow, missed work; reject if own gain benefits rival more |
| CQ-05 | Extra micro-work efficiency does not improve points | Isolated current-square task deduplication after research sign-off | Useful replacement actions and points, not no-op reduction alone |

These are mechanism tests, not five changes to stack. Each candidate must hold
the other policy modules fixed. H1 is a positive effect above a predeclared
practical target; current expected gains remain UNKNOWN.

## 5. Opponent Panel And Leakage Control

- Register source/version/hash, permission, lineage, mechanisms, response type
  and collection time before selecting the final panel.
- Fixed recorded stream, public executable policy and independent mechanism
  surrogate are three different controls. Never label them interchangeably.
- A surrogate tests a mechanism, not whether we beat the author's real agent.
- Kaito v58 and the declared unchanged v40 fork belong to one lineage for
  primary weighting. Verify byte/behavior equivalence before detailed aggregation.
- Use historical references for regression, current distinct responsive policies
  for primary comparison, and unseen lineages/time periods for generalization.
- Old 1.32.6 results do not validate a current 1.32.7 policy. Match configuration
  and record RNG/state-consumption effects rather than assuming equal seed fixes all.
- Never choose opponent recordings by their final bank and then claim random sampling.
- Public references run only in isolated credential-free, network-disabled
  evaluation workers after inspection. Never run whole notebooks with auto-upload cells.

## 6. Pairing, Power And Selection

For each seed and opponent, run parent and candidate in both seats. The paired
effect uses the difference of their two-seat mean points. Bootstrap whole seed
blocks, keeping both seats, policies and fixed-panel opponents together. For a
population claim, additionally handle lineage sampling/dependence; a fixed-panel
interval does not quantify uncertainty about the whole ladder.

Pilot variance and intervention prevalence determine sample size. As a planning
approximation at two-sided alpha .05 and 80% power:

`n_effective = ceil(((z(.975)+z(.8))*sd(paired_effect)/minimum_effect)^2)`.

For an assumed +0.02 target, paired SD assumptions .10/.20/.30 require roughly
197/785/1766 independent seed clusters. These are **assumption scenarios**, not
observed variances or a promise that any fixed number of games is adequate.
Sparse activation and multiple testing may increase the requirement.

Pre-register primary metric, practical effect, stopping rule, opponent weights,
holdout, exclusions and correction across candidate screens. Freeze one candidate
before opening the final holdout. Do not tune after seeing it or erase failed games.
Report activation rate, uncertainty, lower-tail regressions, runtime and all faults.
Identical bootstrap outcomes give a degenerate interval, not proof of certainty.

## 7. What The First Real Replay Can Establish

CC0 episode 105954399 is one selected high-rated game, not a random sample.
Its complete recorded states give this descriptive path (zero-based days):

| Quantity | kwa | Lyesterday |
|---|---:|---:|
| Cash at day 5 start | 36 | 647 |
| Cash at day 15 start | 9076 | 22036 |
| Cash at day 25 start | 73297 | 71101 |
| Final cash | 105197 | 93666 |
| First NE observed day | 6 | 6 |
| First SW observed day | 9 | 11 |
| Maximum observed hands | 11 | 12 |
| Cows / sheep at day 20 start | 6 / 3 | 6 / 11 |

The day-15 cash leader lost. More sheep and a larger maximum hand count did not
guarantee victory in this case. None of this identifies the causal effect of
buying sheep, earlier land or hiring; crop mix and many other actions also differ.
Do not turn this one example into a population rule or copy the winning path.

A separate replay-parity prototype failed early because the callable adapter
interface was not yet correct. Full local reproduction is NOT verified. Raw
recorded-state descriptions above are distinct from replay-simulation evidence.
No candidate agent was built or tested in this research continuation.

## 8. Decision Ledger

Each hypothesis records source facts, quantitative mechanism, uncertain inputs,
H0/H1, control, smallest meaningful effect, planned sample, falsifier and status.
Priority uses expected point gain, confidence, generalization, attribution and
engineering cost only when those quantities have defensible estimates. Otherwise
state UNKNOWN; never manufacture numeric confidence from a notebook title.

Promotion additionally needs valid actions, runtime/package verification,
compliance, source separation, current parent/hash, no duplicate or pending
conflict, live quota and a complete manifest. Accepted rules and five remaining
slots are access facts, not evidence that a candidate should be submitted.
