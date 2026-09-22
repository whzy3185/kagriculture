# EXP015 provenance

- Created: 2026-09-22
- Parent: `external/gold_20260922/pipe19/extracted/main.py`
- Parent SHA-256: `111863BD708CC8134D0A7CC26AE9AC8B7CB5266E061CD71D8429CAEFB48B1C51`
- Change: raise the clone-aware `V9_RACE_DEFAULT` floor from 41 to its existing
  maximum of 48 turns.
- Purpose: test whether Clone48's longer reservation horizon composes safely
  with Pipe19's overflow reclaim, three-turn sale advance, and queue closure.
- Packaged archive: `submissions/EXP-015-h48-sale-advance.tar.gz`
- Archive SHA-256: `51EF2D3DCB1C2BD77A932C66C164CCB8C3D4D97EA3B890E492D744B98D6918CD`
- Kaggle submission: `56460311`
- Validation episode: `111966853`, completed successfully on 2026-09-22

All upstream license and attribution notices remain embedded in `main.py`.
