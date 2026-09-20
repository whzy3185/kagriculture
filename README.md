# Kaggriculture campaign

Reproducible workspace for the Kaggle **Kaggriculture** simulation competition.
The project intentionally lives on `E:` and does not write campaign artifacts to
`C:`.

## Current challenger

- Experiment: `EXP-008`
- Agent: `agents/candidates/exp008/main.py`
- SHA-256: `D5460FC2E5488E0A340F0E4E795F2709C48B58CFF7C204CED3821A4C7DAE4555`
- Kaggle submission: `56379486`
- Initial status: `PENDING`
- Parent: `EXP-007`, submission `56363469`, public score `2607.3` at EXP-008 submission time

EXP-008 adds the Apache-2.0 early productive wheat cycle published in The 2950
Peak Farm to the exact EXP-007 parent. Original notices and licence text remain
in the source. See `agents/candidates/exp008/PROVENANCE.md`.

## Evaluation contract

The local evaluator pins the current official Kaggriculture interpreter source
at SHA-256
`BC8A54879EF02C7EA64B8B333D6A976F0EA65C4949149D01F463F23BCCEE653E`.
Every comparison uses fixed seeds and both player seats.

```powershell
E:\anaconda\python.exe scripts\evaluate_agents.py `
  agents\candidates\exp008\main.py OPPONENT.py `
  --seeds 701,809,907 --output reports\example.json
```

Package deterministically:

```powershell
E:\anaconda\python.exe scripts\package_submission.py `
  agents\candidates\exp008\main.py `
  submissions\EXP-008-early-cycle.tar.gz `
  --manifest submissions\EXP-008-early-cycle.manifest.json
```

## Decision log

- `EXP-006`: own independent controller, public score `534.3`.
- V50 screen: rejected at `3-9`, mean margin `-$903` versus V9/4.
- `EXP-007`: accepted after `6-0`, mean margin `+$24,233` versus the previous
  strong parent on independent holdout seeds; score `2607.3` when EXP-008 was submitted.
- `EXP-008`: early-cycle challenger; `31-1` against EXP-007 across ladder and
  fresh holdout worlds, and improves the matched V50 panel from `5-7 / -$497`
  to `6-6 / +$323`.

Detailed evidence is in `reports/EXP-008.md` and the JSON files under `reports/`.
