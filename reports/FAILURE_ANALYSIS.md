# Failure Analysis - Preliminary

## 2026-09-08: Rejected Purchase-triggered Funding Check

EXP-20260908-01 extends only Ahmed v23's budget-check activation. It lost all
48 fresh paired-screen games: mean -6432.1875, median -4358, p10 -14800.1.
No candidate 96-seed evaluation or competition submission followed.

Exact selected-loss cash reconciliation:

| Seed | Candidate sales / costs | Parent sales / costs | Final margin |
|---|---|---|---:|
| 2026091018 | 135594 / 40573 | 156412 / 40280 | -21111 |
| 2026091015 | 172809 / 35390 | 189834 / 35397 | -17018 |

The main deficit is revenue, not extra purchase spending. Milk sold fell from
222 to 143 units and from 263 to 211; average milk prices were not lower.
Both selected candidate cases lost two cows at day-end turn 215, while their
parents did not at that turn. Empty-carried-wheat FEED requests were 21 vs 7
and 5 vs 0. Later animal losses also occur in one parent, so the mechanism
must not be described as a universal healthy-parent/broken-child contrast.

The candidate eliminated unfilled market requests on this 48-game screen but
retained 9589 non-PASS unit no-ops. Financing success did not preserve physical
maintenance resources or realized production. Source review shows stock
protection subtracts globally carried inventory from future pickup needs;
per-worker accessibility and dated feed reservations require separate testing.
Do not treat this observation as proof that one replacement formula will win.

Evidence: research/EXP-20260908-01-losses.json, -cashflows.json and -mechanism.json.
These are two selected existing screen cases, not additional independent trials.
The daily candidate remains frozen and rejected; do not retune it under this ID.

## Own Baseline Evidence

Frozen main.py SHA256: 712be5af7888bb489c95417e6eb3d16875def7fcaaed31c47715d85e9ad9ae7d.
20 fixed seeds x two seats against official starter; no strategy modification.
All 40 episodes DONE; 0 caught exceptions and 0 shape/JSON contract errors.
719 agent calls and 720 recorded states per episode. One extra seed/seat repeat
gave the same trajectory hash. Repeated runs are not independent new evidence.

Instrumented official unit-action function detected 12596 non-PASS no-ops among
123359 worker actions: 10.2108%, mean 314.9/game. These include duplicate WATER,
PLANT and HARVEST, with occasional DIG. State equality is the diagnostic; it does
not certify market validity or count all atomic PLANT rejections.

Cause reproduced: `_unit_action` reserves a current square but does not check
the reservation before a second co-located worker waters/plants/harvests there.
The regression test documents the existing defect; passing that diagnostic
does not mean the agent is correct. Main is deliberately unchanged.

Static risks needing separate tests: seed buys/hires do not share a conservative
sequential cash ledger; shape tests miss semantic no-ops; quoted sale price is
not full-block revenue; terminal carried inventory can be unsellable.

## Research Negative Evidence

- Goose Portfolio: reported guard never changed actions in its 48-game panel.
  Different same-code ratings are not a causal effect.
- Fieldbook: author-reported 0.9948 ordinary vs 0.6322 hard-panel points.
- Endgame thread: residual-work hiring lost 2-6 normally despite winning artificial
  scarcity stresses. Do not promote on stress-only wins.
- Island GA: idle-bank gain can reverse with a competing producer; screen/confirm
  gaps may mix selection, small samples and population mismatch.
- X-ray: diversity does not alone identify adaptation; tiny world samples and
  uncontrolled future shops/weeds remain.

## Unavailable Analyses

No independent online replays/submission results collected. No own online
strongest wins/worst losses are available. All local starter games were wins;
ten losses must not be invented. Plant loss, animal escape, shed overflow,
transport, unused land and liquidation failure counts remain UNKNOWN.

Next: named opponent strata and reconciled replay parser, then 10 strongest wins
and 10 worst losses where available, with sampling criteria frozen first.
