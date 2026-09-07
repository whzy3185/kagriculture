# Quantitative Game Model

Evidence: official Kaggriculture 1.32.7 source, hash
`bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`;
current Overview; original Code/Discussion sources in CODE_DISCUSSION_REVIEW.md.
No agent improvement is inferred merely from this model.

## Measured Strategy Update

See STRATEGY_DEPTH_20260907.md: an exact four-game diagnostic of two existing
development seeds found zero EXP-006 sales in [0,180), versus 7315/7336 for
Shape. Similar on-hand cash concealed very different productive assets.
This is not a controlled effect of early income or livestock, and not new
independent evaluation evidence. It motivates testing an early-income bridge.

Tomato/strawberry have four lifetime production events. Under ideal eligible
fertilization and timely harvest, these can supply eight total units rather
than four, but held stock caps at four. Fertilizer acquisition, transport,
application, watering and displaced work must all be priced; a theoretical
doubling is not automatic profit. Fertilizer use also forgoes sale revenue
and can change a rival's sale prices in the shared market.

For uncertain future shops/supply, integrate E[p(I)] rather than assuming
p(E[I]) is equivalent. Use a distribution over continuation outcomes and a
liquidity constraint at each payment, not terminal cash alone. Scenario inputs
must be public/legitimate history; hidden replay information is audit-only.

## Objective And State

Let M = our terminal bank minus opponent terminal bank. Target expected points
`E[1(M>0) + 0.5*1(M=0)]`, while retaining win fraction and paired cash margins
as separate diagnostics. Assets, unsold inventory and seeds have no direct
terminal value. Final BT also depends on the active-opponent comparison graph.

State includes cash, time remaining, public farm geometry, crop/animal ages and
service flags, own shed and carried stock, labor, public market inventory/quotes,
and unlocked shops. Opponent private inventory is hidden. Inferred rival supply
is a belief with uncertainty, never ground-truth privileged information.

## Unit Economics

The following are reference inputs, NOT expected market outcomes. Crop cash
contribution assumes unfertilized peak yield at constant base price; it excludes
wages, travel, financing, sale timing and price impact.

| Asset | Initial coins | First yield age | Schedule / reference yield | Base output price | Reference crop contribution |
|---|---:|---:|---|---:|---:|
| Wheat | 10 | 2 | one-time; unfertilized peak 4 at age 4 | 25 | 90 |
| Carrot | 20 | 2 | one-time; peak 3 at age 3 | 35 | 85 |
| Tomato | 50 | 8 | 4 production ticks ages 8,9,10,11 | 60 | 190 |
| Strawberry | 100 | 10 | 4 ticks ages 10,12,14,16 | 120 | 380 |
| Melon | 80 | 10 | one-time; peak 6 at age 10 | 250 | 1420 |
| Goose | 300 | 4 | base 1 egg/day; max held 4 | 50 | horizon-dependent |
| Cow | 400 | 8 | base 1 milk/2 days; max held 6 | 160 | horizon-dependent |
| Sheep | 500 | 6 | base 1 wool/3 days; max held 6 | 200 | horizon-dependent |
| Land | 1000 / 2000 / 4000 | not applicable | 25 added tiles each; NE then SW then SE | no terminal resale | workload-dependent |
| Farm hand | marginal Fibonacci wage | after hire resolves | remaining unit actions that day, minus travel | no resale | task-dependent |
| Fertilizer | buy quote starts at 100; or collect from animal | next eligible bonus | one FERTILIZE action plus acquisition/haul; 3 inclusive days | market-dependent | incremental yield minus opportunity cost |

NW is already owned; it is not the second or third land purchase.
Animal placement needs a matching structure, carried animal, purchase, pickup,
travel and PLACE. FEED consumes wheat in that worker's inventory, not directly
from the shed. Daily wheat has both a cash price and a transport/action cost.

Planting-day watering is mandatory for survival. Later every-other-day service
can preserve life, but bonus-window watering determines one-time crop yield.
Melon fertilizer may reach the yield cap before age 10; it does **not** override
the engine's first_yield_day=10 harvest legality check.

Define for each feasible service plan:

```
initial_cost = purchase + required structure/setup financing
labor_cost = allocated hires + travel/service shadow cost
maintenance_cost = feed + consumables + replenishment/haul
expected_yield = sum over dated production events of realized collected units
expected_sale_price = expected cash from actual fills / expected units sold
tile_cost = shadow price of occupied tile-days
opportunity_cost = value of the displaced feasible plan
payback_time = first date cumulative net realized cash >= initial cost
ROI = (net realized cash - initial cost) / initial cost
NPV = -initial_cost + sum discount(t)*(sale_cash - maintenance - labor)
actions_per_income = total required unit actions / positive net cash
income_per_tile_day = net cash / occupied tile-days
income_per_worker_action = net cash / executed worker actions
```

ROI is undefined at zero investment and actions_per_income is undefined when
net cash <=0. Do not report them as zero. Expected prices, shadow prices,
discount factor and failure probabilities remain **UNKNOWN / UNCALIBRATED**
until measured on the declared opponent population and environment version.

## Dynamic Market Model

For resource r, `p_r(I)` is the official rounded piecewise curve with floor 1.
Before floor saturation, sale revenue is the sum of marginal quotes, not
quantity times the first quote. Both players' order positions resolve together,
one unit at a time. At the floor, sales earn one coin but add no market inventory.
Buys quote post-buy inventory; an isolated immediate buy/resell is zero-profit.

```
I_next = I + above_floor_sales - player_buys - town_consumption
demand_r/day = 1[r != fertilizer]
               + 6 * sum(active_shop_instances requiring r)
                   with double weight for a single-product shop
```

Shops are drawn with replacement every three days, capped at eight instances.
Melon is absent from all shop menus: town demand is only one unit/day. Future
shops are unknown at runtime; condition forecasts on visible shops and a
declared future distribution, never on the simulation seed or future replay.

From equilibrium with one seller, no demand/buys and enough stock, the saved
Actual Trades notebook reports the first floor-priced unit at sale numbers:
melon 159, milk 77, wool 60, strawberry 63. These are reference impact examples,
not recommended production quantities; reconcile exact quote convention before
using them. Competing supply can erase the apparent melon base-price advantage.

## Finite-Horizon Control

```
ExpectedProfit(policy, state, remaining_days)
  = E[sum(actual sales - seeds - animals - feed - fertilizer - hires - land)]
```

Subject to funding at each substep; daily water/feed survival; production dates;
inventory locations and 100-item shed capacity; travel, worker and market-slot
budgets; competitor price impact; and a harvest-to-deposit-to-sale path before
termination. Use paired counterfactual rollouts only after engine parity is
established. Cash, assets and output are not interchangeable terminal measures.

The official framework records 720 states with 719 action calls at episodeSteps
720 in the inspected version. Count executed opportunities directly. End-of-day
deposit after the final market phase cannot be assumed sellable afterward.

## Action Values And Labor

`ValuePerAction = expected marginal feasible terminal cash / actions consumed`.
This is a scheduling heuristic, not the full competitive point objective.

| Action | Marginal value that must be evaluated |
|---|---|
| MOVE | Enables reachable profitable work; movement alone is not waste |
| PLANT | Feasible collected-and-sold yield minus seed and future service obligations |
| WATER | Avoided irreversible crop loss plus eligible marginal yield; second same-day watering zero |
| HARVEST | Realizable inventory net of haul/sale capacity and early-harvest opportunity cost |
| FEED | Avoided escape and next production/care value minus carried-wheat opportunity cost |
| CARE | Next scheduled bonus that fits max_held and can be collected/sold before horizon |
| BUILD | Marginal production enabled, not immediate revenue |
| PICKUP | Correct carried resource for a funded and reachable task |
| DROP | Sale/space enabled minus discarded overflow risk |
| PLACE | Feasible animal installation or shed transfer; resource/structure requirements matter |
| DIG | Freed tile value minus destroyed crop and worker opportunity cost |
| COLLECT_FERTILIZER | Sale/use value minus travel and displaced service; stock does not accumulate |

Fibonacci cumulative wages: 4 hands=7, 6=20, 8=54, 10=143, 12=376, 13=609.
The thirteenth hand costs 233 more than twelve. Hire only if its marginal
reachable, cashable tasks justify that wage and working capital. Day-end
positions do not carry into next morning: farmer resets, hands disappear.

Land's payback is not 25 times a static crop ROI. Expansion can be negative if
labor and cash cannot service it. Quantity, location and timing must be evaluated
jointly while changing only one nominated policy variable per experiment.

## Statistical Design

- Experimental unit: seed pair, not two independent seats. For population tests,
  account for both seed and opponent lineage clustering.
- Score q=(wins+0.5*ties)/games. Always report wins/ties/losses separately.
- Fit explanatory P(win|features) only after data extraction is reconciled.
  Split by submission/lineage/time; avoid leakage from final assets/rating.
- Top 1/5/10%, middle and bottom groups require a declared sampling frame.
  A top-only daily dump cannot support whole-ladder percentile inference.
- Report effect size, variance, activation rate, failure rates and uncertainty.
  A bootstrap point interval on all wins is not proof of certainty.
- Screen on development seeds; freeze one candidate before untouched holdout.
  Multiple testing and repeated screening require correction or a fresh final test.
- Quantitative win-gain estimates and numerical priority values remain UNKNOWN
  until independent pilot data exist. Literature performance is not our prior score.
