# Kaggriculture campaign

Reproducible workspace for the Kaggle **Kaggriculture** simulation competition.
The project intentionally lives on `E:` and does not write campaign artifacts to
`C:`.

## Current challenger

- Experiment: `EXP-009`
- Agent: `agents/candidates/exp009/main.py`
- SHA-256: `10F58185B916392CA39697C83F67F455DF81A74DFB6EB1AACD60FD81D50C9970`
- Kaggle submission: `56417069`
- Initial status: `PENDING`
- Previous challenger: `EXP-008`, submission `56379486`, public score `2529.6`

EXP-009 is the exact, hash-verified Apache-2.0 One More Wheat submission. It
combines the Metav4/Pipe16 efficiency stack with a temporary opening wheat crop
that grows one additional day before harvest. Original notices and licence
text remain in both the candidate directory and archive. See
`agents/candidates/exp009/PROVENANCE.md`.

## Evaluation contract

The local evaluator pins the current official Kaggriculture interpreter source
at SHA-256
`BC8A54879EF02C7EA64B8B333D6A976F0EA65C4949149D01F463F23BCCEE653E`.
Every comparison uses fixed seeds and both player seats.

```powershell
E:\anaconda\python.exe scripts\evaluate_agents.py `
  agents\candidates\exp009\main.py OPPONENT.py `
  --seeds 701,809,907 --output reports\example.json
```

The submitted multi-file archive is pinned byte-for-byte in the manifest:

```powershell
Get-FileHash submissions\EXP-009-one-more-wheat.tar.gz -Algorithm SHA256
```

## Decision log

- `EXP-006`: own independent controller, public score `534.3`.
- V50 screen: rejected at `3-9`, mean margin `-$903` versus V9/4.
- `EXP-007`: accepted after `6-0`, mean margin `+$24,233` versus the previous
  strong parent on independent holdout seeds; score `2607.3` when EXP-008 was submitted.
- `EXP-008`: early-cycle challenger; `31-1` against EXP-007 across ladder and
  fresh holdout worlds, and improves the matched V50 panel from `5-7 / -$497`
  to `6-6 / +$323`.
- `EXP-009`: accepted at `30-2`, mean margin `+$1,775.06` versus EXP-008 over
  ladder and fresh holdout worlds. Its final one-more-wheat layer is `16-0`,
  mean `+$27.63`, against the exact direct parent.

Detailed evidence is in `reports/EXP-009.md` and the JSON files under `reports/`.
