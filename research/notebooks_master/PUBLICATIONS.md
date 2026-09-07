# Notebook Publication Register

Updated: 2026-09-07. Time zone: Asia/Shanghai.
Scope: public research Notebooks, not competition prediction submissions.

| Candidate | Notebook | Version | Status |
|---|---|---:|---|
| EV-A | [S6E9 - Data Audit and ID-Aware Drift](https://www.kaggle.com/code/muelsyse111/s6e9-data-audit-and-id-aware-drift) | 2 | PUBLIC_RUN_VERIFIED |
| EV-B | [Validation Stability and ID-Order Tests](https://www.kaggle.com/code/muelsyse111/s6e9-validation-stability-and-id-order-tests) | 3 | PUBLIC_RUN_VERIFIED |
| EV-C | [CPU Baselines and Paired AUC](https://www.kaggle.com/code/muelsyse111/s6e9-cpu-baselines-and-paired-auc) | 4 | PUBLIC_RUN_VERIFIED |

## EV-A Publication Receipt

- Kaggle title: `S6E9 | Data Audit and ID-Aware Drift`.
- Kernel ID: 133389741.
- The user explicitly confirmed publication of the reviewed Notebook and its aggregate outputs.
- Published by updating the existing Notebook, retaining the same slug and ID.
- No code change from the reviewed private version 1; only visibility changed.
- Official CLI reported successful push of version 2. Worker status then reached COMPLETE.
- Authenticated metadata readback confirms `is_private=false`, CPU, internet off,
  and the sole official input `playground-series-s6e9`.
- Version 2 audit start: 2026-09-07T04:30:37.801609+00:00 (12:30:37 +08:00).
- Audit timer: 13.72 seconds, excluding kernel startup and initial imports.
- Process peak RSS: 593.01 MiB, not isolated incremental audit memory.
- All eight expected aggregate output artifacts downloaded and checked.
- Source cells, official input fingerprints and stable aggregate results match
  the reviewed source/local reference. The version 2 run timestamp is newer than
  the private version 1 timestamp, so old outputs were not mistaken for this run.
- All four PNGs are byte-identical to the visually reviewed version 1 charts.
- Logs contain the known-answer and input-contract PASS markers, with no traceback.
- Text artifacts contain no API token markers or private local paths.
- No raw records, official input data files, record-level predictions or
  competition submission file were published.
- Credentials are not part of this repository or the uploaded Notebook.
- Code medal, vote count and leaderboard score: not claimed.

Machine-readable receipt: `runs/EV-A-kaggle-v2-2026-09-07.json`.
Earlier private/local review files remain historical records, not the current publication status.

## EV-B / EV-C Publication Receipt

The user authorized autonomous publication of reviewed, finished research
Notebooks. EV-B version 3 and EV-C version 4 update the existing notebook IDs;
source and model settings are unchanged from the reviewed private editions.

- Official metadata confirms `is_private=false`, CPU, internet off and only the
  official S6E9 competition input for both notebooks.
- Both public runs reached COMPLETE; artifacts were freshly downloaded and their
  timestamps were checked against the preceding private versions.
- Source cells, data and partition fingerprints match the reviewed sources.
- EV-B metrics match the local reference; EV-C matches its separately verified
  Kaggle-version numerical stack, with the initial-stack discrepancy retained.
- EV-B charts and EV-C's interval chart match the previously reviewed charts
  byte for byte; the latest EV-C runtime chart was visually checked separately.
- No raw records, row predictions, weights, credentials or competition submission
  files were published. No prediction was submitted or selected.
- Machine-readable receipts: `runs/EV-B-kaggle-v3-2026-09-07.json` and
  `runs/EV-C-kaggle-v4-2026-09-07.json`.

Both have distinct questions, train-only experiments, unit tests and reviewed
aggregate outputs. EV-C's initial cross-library metric mismatch was retained and
resolved by a separate Kaggle-matched numerical-library reproduction; its latest
notebook explains this limitation. Full review:
`reviews/EV-BC-private-2026-09-07.md`.

The latest versions apply the user's reader-ready editorial standard: results
first, concise tables, reusable code examples and less audit-log clutter. The
experiments and model settings are unchanged. Latest editorial/run receipt:
`reviews/EV-BC-reader-ready-2026-09-07.md`.

## Score And Publication Policy

Autonomous publication is authorized after run/content/compliance review; this
does not authorize competition prediction submissions or new spending/credentials.
Prefer stronger runnable baselines and medal-eligible competitions going forward.
Do not label local holdout AUC or another author's score as our leaderboard result.
S6E9 Playground does not award Competition medals. EV-C's HGB AUC 0.941179 is a
24,000-row holdout score, not a leaderboard or medal-zone result. Code medals
remain governed by eligible votes/reuse and are not guaranteed by publication.

No automation, recurring publication job, prediction submission or final-submission
selection was created by this release.
