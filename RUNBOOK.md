# Kaggriculture Execution Runbook

## Current Authority

- Repository: https://github.com/whzy3185/kagriculture
- New branch: `research/round1-audit-20260907`, based on `work/baseline-v0` at `17f61c15dc001abf8726a57319c5ead245c9ddfd`.
- Latest user override (2026-09-07): create a new branch; **do not create a PR**. This supersedes the PR step in `CODEX_TASK_CHAIN.md`, which preserves the supplied text verbatim.
- Do not merge, change the existing PR, or overwrite `main.py`.
- `CODEX_TASK_CHAIN.md` is the requested long-term protocol, not evidence of completed work.
- This branch is not a production-approved champion.

## Environment

Use Python 3.12 with a dedicated virtual environment. Install `requirements.txt`
and `kaggle==2.2.4`. The inspected environment is `kaggle-environments==1.32.7`,
`kagglehub==1.0.2`, `pytest==9.1.1`. Pin the environment for comparisons.

```bash
python scripts/kaggle_connection_check.py
python -m pytest -q
python scripts/evaluate.py --games 20 --opponent starter
python scripts/audit_baseline.py --split fixed --output experiments/results/EXP-000-fixed.json
python scripts/audit_baseline.py --split holdout --output experiments/results/EXP-000-holdout.json
```

Evidence files are immutable: the audit script refuses to overwrite them. It is
single-process instrumentation, not safe for concurrent games in one process.
Fresh baseline modules are loaded per game. The repeatability game is separate
from win-rate denominators. Paired seats are not independent statistical samples.
Holdout seeds become consumed upon inspection; register new seeds before tuning.

## Blocking Gates

1. Finish the complete Rules text review and competition Data/runtime audit.
   The initial Code/Discussion survey and public dataset/leaderboard snapshot are
   now recorded in research/CODE_DISCUSSION_REVIEW.md. Targeted source review is
   not an exhaustive audit of every notebook or embedded component.
2. Confirm the intended Kaggle identity with the owner. GitHub owner `whzy3185`
   and browser account `muelsyse111` need not be the same name; do not assume they are.
3. The owner must join the competition and accept its rules; the observed UI
   still displayed Join Competition. Do not accept binding terms silently.
4. Obtain CLI authorization via the owner's local login; never paste credentials
   in chats, notebooks, logs, commits, or submission messages.
5. Complete semantic action/market validation, candidate ablations, new holdout,
   genuine sandbox runtime validation, provenance review, artifact/git binding,
   duplicate ledger check, current pending check and live quota check.

The inherited uploader only checked authentication, entry and file existence.
`--execute` is now explicitly disabled until the full evidence gate is implemented
and tested. Its dry run is **not** submission approval. Do not bypass this block
with raw CLI commands. Only APPROVE may promote a candidate; only a verified
COMPLETE server result may create a SCORECARD row.

## Resume

Continue with the remaining compliance/data audit, then reproduce the collision
diagnostic as a single scheduling ablation in `agents/candidates/`. Do not combine
it with livestock/land/market changes. The five Round 1 slots are not five completed
strategy experiments. No notebook has been created or uploaded in this round.

Daily and weekly tasks in the supplied chain are requirements. No perpetual
process or scheduled automation has been activated by this branch. Resume the
loop after the research and authorization gates are resolved; stop uploads at
the official final submission deadline and continue rating/replay monitoring
through final leaderboard convergence.
