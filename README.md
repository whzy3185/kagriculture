# Kaggriculture campaign

Reproducible workspace for the Kaggle **Kaggriculture** simulation competition.
The project intentionally lives on `E:` and does not write campaign artifacts to
`C:`.

## Current champion

- Experiment: `EXP-007`
- Agent: `agents/candidates/exp007/main.py`
- SHA-256: `BFEE70E9DAAEBEAE0737A880F1DF8F1C60D0783C59AF620136CC0D28EF482BC7`
- Kaggle submission: `56363469`
- Status at submission time: `PENDING`

The candidate is the exact Apache-2.0 V9/4 public agent recovered from Thomas
Schinkel's published notebook. Its original notices and licence text remain in
the source. See `agents/candidates/exp007/PROVENANCE.md`.

## Evaluation contract

The local evaluator pins the current official Kaggriculture interpreter source
at SHA-256
`BC8A54879EF02C7EA64B8B333D6A976F0EA65C4949149D01F463F23BCCEE653E`.
Every comparison uses fixed seeds and both player seats.

```powershell
E:\anaconda\python.exe scripts\evaluate_agents.py `
  agents\candidates\exp007\main.py OPPONENT.py `
  --seeds 701,809,907 --output reports\example.json
```

Package deterministically:

```powershell
E:\anaconda\python.exe scripts\package_submission.py `
  agents\candidates\exp007\main.py `
  submissions\EXP-007-v9_4-2945.tar.gz `
  --manifest submissions\EXP-007-v9_4-2945.manifest.json
```

## Decision log

- `EXP-006`: own independent controller, public score `534.3`.
- V50 screen: rejected at `3-9`, mean margin `-$903` versus V9/4.
- `EXP-007`: accepted after `6-0`, mean margin `+$24,233` versus the previous
  strong parent on independent holdout seeds.

Detailed evidence is in `reports/EXP-007.md` and the JSON files under `reports/`.

