# Kaggriculture campaign

Reproducible workspace for the Kaggle **Kaggriculture** simulation competition. Campaign artifacts live on `E:`; the workflow does not use `C:` as its workspace.

## Current strategy status

- Stable baseline: `EXP-054-highquote-150`
- Low-risk experimental candidate: `EXP-066-liquidity-wool-flush`
- EXP066 improves two known official wool-race loss tapes by `+1,032` and `+300`, preserves EXP054's `134-0-10` result against 12 strong open-source agents on six paired-seat seeds, and ties EXP054 in all 40 games on 20 fresh paired-seat seeds.
- EXP066 remains experimental because the two official losses were narrowed but not flipped. See `reports/EXP045_EXP054_KAGGLE_FAILURE_OPTIMIZATION_20260930.md`.

## Submission packages

`submissions/` contains byte-reproducible archives and SHA-256 manifests for:

`EXP-007`, `EXP-008`, `EXP-009`, `EXP-010`, `EXP-011`, `EXP-012`, `EXP-014`, `EXP-015`, `EXP-018`, `EXP-020`, `EXP-028`, `EXP-035`, `EXP-040`, `EXP-045`, `EXP-046`, `EXP-054`, and `EXP-066`.

Each archive has `main.py` at the archive root. Packages are produced with:

```powershell
python scripts\package_submission.py agents\candidates\<candidate>\main.py `
  submissions\<package>.tar.gz --manifest submissions\<package>.manifest.json
```

## Evaluation contract

Local comparisons use fixed seeds and both player seats. The principal tools are:

- `scripts/evaluate_agents.py` for direct paired-seat tests;
- `scripts/evaluate_round_robin.py` for resumable leagues and anchor screens;
- `scripts/evaluate_replay_tapes.py` for exact public-opponent action-tape replay;
- `scripts/package_submission.py` for deterministic packaging and hash verification.

## Evidence

- `reports/EXP045_EXP054_VS_CURRENT_OPEN_SOURCE_20260930.md`
- `reports/EXP045_EXP054_KAGGLE_FAILURE_OPTIMIZATION_20260930.md`
- machine-readable JSON reports under `reports/`
- source candidates under `agents/candidates/`

The repository contains both promoted and rejected experiments so that strategy decisions remain auditable. Formal Kaggle upload is a separate, explicit action; creating or syncing a package does not submit it.
