# Kaggriculture campaign

Reproducible workspace for the Kaggle **Kaggriculture** simulation competition.
The project intentionally lives on `E:` and does not write campaign artifacts to
`C:`.

## Current challenger

- Experiment: `EXP-010`
- Agent: `agents/candidates/exp010/main.py`
- SHA-256: `213E054BEA4AB82C4675BE7C4C9B941E368DCA8C229303C2CF9F5F924F008163`
- Kaggle submission: `56417558`
- Initial status: `PENDING`
- Previous challenger: `EXP-009`, submission `56417069`, rating in progress

EXP-010 combines the public-gold-stack failure-atomic opening and effective
sale-queue closure with EXP-009's one-more-wheat harvest. It preserves the
Metav4/Pipe16 production stack and Apache-2.0 notices. See
`agents/candidates/exp010/PROVENANCE.md`.

## Evaluation contract

The local evaluator pins the current official Kaggriculture interpreter source
at SHA-256
`BC8A54879EF02C7EA64B8B333D6A976F0EA65C4949149D01F463F23BCCEE653E`.
Every comparison uses fixed seeds and both player seats.

```powershell
E:\anaconda\python.exe scripts\evaluate_agents.py `
  agents\candidates\exp010\main.py OPPONENT.py `
  --seeds 701,809,907 --output reports\example.json
```

The submitted multi-file archive is pinned byte-for-byte in the manifest:

```powershell
Get-FileHash submissions\EXP-010-gold-stack-hybrid.tar.gz -Algorithm SHA256
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
- `EXP-010`: gold-stack hybrid; `16-0`, mean `+$27.63`, versus Farmer John V55
  and `32` ties versus EXP-009 across fresh and recent-ladder worlds.

Detailed evidence is in `reports/EXP-010.md` and the JSON files under `reports/`.
