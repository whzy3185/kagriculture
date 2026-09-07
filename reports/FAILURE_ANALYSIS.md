# Failure Analysis - Preliminary

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
