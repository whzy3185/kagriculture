# Open-source Champion - 2026-09-08

Research champion: **Ahmed v23**, within the declared reproducible Python panel.
This is NOT approval to deploy its unchanged artifact or promote root main.py.

- Source: https://www.kaggle.com/code/ahmedberatozer/notebook865729c24e
- Author: Ahmed Berat Ozer; Notebook version 3, updated 2026-09-07T22:16:47Z.
- Exact source SHA256: 6eb728a40cc55f7e497add6ea2946ce38b0389c24531a208219d48587435838e.
- Notebook SHA256: 7b537d1b235fa8eb9b4527a0d3abe542e465c758f6e3c11682f83fbd29ff6f2a.
- License: Apache-2.0 embedded in exact source; credits preserved for Thomas,
  yhay81 and tetsutani. Thomas v2 donor SHA verified before reconstruction.
- Engine: kaggle-environments 1.32.7, official source hash recorded in reports.
- Source copies and selection manifest: agents/champion/.
- Upstream license-comment spacing is preserved byte-for-byte; do not autoformat
  frozen sources just to remove trailing-space warnings and invalidate their hashes.

## Measured Selection

24 fresh seeds 2026090800-2026090823, both seats, seven entries (six public
policies plus EXP-006): 1008 games, all completed. Weak EXP-006 is excluded
from public-strength ranking. Pairwise details: PUBLIC_PANEL_SUMMARY_20260908.json.
Average public-opponent points: Ahmed 91.67%, Thomas 88.33%, Shape 50.83%,
Farming V4 42.50%, Kaito 26.67%, portable boatlee Adaptive 0%.

Close-finalist confirmation: 96 unseen seeds 2026090900-2026090995, both seats.
Ahmed vs Thomas: 134 wins, 58 losses, no draws; 69.79% points.
Mean margin +430.71875; median +210; p10 -675; variance 1129318.0252;
maximum measured call 0.0264495 seconds. All 192 games completed.

These are finite-panel comparisons, not a guarantee against every public agent.
Farming/Shape and Thomas/Ahmed share ancestry. Native ARA-V2 is not reproduced
on macOS (agent.so only, no agent.dylib, Docker unavailable); portable Adaptive
is a distinct family representative, not a claim of equivalent performance.

## Safety And Replay Findings

The finalist run retains 2 atomic planting rejections, 491 failed market-unit
attempts, 1068 unfilled requested units, 11880 unit no-ops and 8770 strict
contract flags. Some contract flags are intentional empty market slots; no
blanket zero-invalid-action claim is made. Overflow was zero. Correctness and
submission gates still apply to any derived candidate.

Two worst initial-panel losses reproduced exactly: seeds 2026090808 and
2026090816, margins -791 and -637. Recorded-action replay matched both full
farms and private inventories at every step. Failed purchases occurred at
198,200,202,204,206,217 and 224 because cash was below the next unit's price.
The existing budget guard only runs on 72-turn boundaries. This motivates a
single-variable trigger experiment, not a wholesale economic rewrite.

Latest top-three-team win/loss replay comparison is recorded in
research/REPLAY-20260908-comparison.json. Its identical [0,180) action prefixes
support keeping the strong opening while studying subsequent financing.
No inference of the top agent's hidden algorithm is claimed.
