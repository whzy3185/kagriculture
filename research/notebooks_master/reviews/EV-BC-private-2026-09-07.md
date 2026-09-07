# EV-B / EV-C Notebook Review

Observed: 2026-09-07, Asia/Shanghai.
Status: both notebooks are uploaded and privately run-verified; public release is awaiting confirmation.
No competition prediction, final-submission selection, raw data upload or paid compute was performed.

| Candidate | Kaggle URL | ID | Reviewed version | Stage |
|---|---|---:|---:|---|
| EV-B | https://www.kaggle.com/code/muelsyse111/s6e9-validation-stability-and-id-order-tests | 133393947 | 1 | PRIVATE_RUN_VERIFIED |
| EV-C | https://www.kaggle.com/code/muelsyse111/s6e9-cpu-baselines-and-paired-auc | 133393970 | 2 | PRIVATE_RUN_VERIFIED |

## Design And Distinct Contributions

EV-B changes validation partitions while keeping the logistic pipeline fixed.
It reports stratified and ordinary shuffled holdouts at seeds 17/43/91, plus
ID-tail and ID-head stress tests. ID order is not a timestamp. Exact-duplicate
leakage is not assumed; EV-A found no full-feature duplicates.

EV-C changes model families on the same fixed stratified holdout: prior,
logistic and HistGradientBoosting. All preprocessing is train-fold-only. HGB has
fixed 120 iterations with early stopping disabled. The predeclared contrast is
HGB minus logistic AUC, with 500 paired label-stratified bootstrap replicates.
This interval is conditional on the fitted pair and holdout, not training or
leaderboard uncertainty. Within-class row independence is an assumption; unknown
clustering would limit the interpretation. No production promotion is recommended.

Both use only the official train.csv, sample seed 20260907, 120,000 rows, with
96,000 training and 24,000 validation rows per fit. Test.csv is never read.
Design notes were written locally before execution, not registered with an
independent preregistration service. They are retained without hindsight edits.

## Input And Partition Provenance

- Official competition: https://www.kaggle.com/competitions/playground-series-s6e9
- Data: https://www.kaggle.com/competitions/playground-series-s6e9/data
- Rules: https://www.kaggle.com/competitions/playground-series-s6e9/rules
- train.csv SHA256: eae9eaa4e6378df405e755f853771d7e26d212bd93258349fc797b771021946a.
- Full training rows: 668,665. Sampled rows: 120,000.
- Sample ID SHA256: 2148b6935cfdb1e320984e05a1ee6d433a09568911c391a089ed338dfb6142ae.
- Seed-17 stratified training ID SHA256: a7fe310015c39b685aafb6754a73d66f1906e2e1d2ff69bff66b0deb2fb32c15.
- Seed-17 stratified validation ID SHA256: c68d77ef131d785a461712ff3f9b5fd67745cbde9abe62d83c17b2ad5a168472.
- All input/sample/partition fingerprints agree between local and Kaggle runs.

## Verified Results

EV-B logistic ROC-AUC across the eight holdouts ranges from 0.9367944562 to
0.9413710190. The range across the three stratified seeds is 0.0025785984,
versus 0.0008321137 for the three ordinary shuffled seeds. These overlapping
holdouts are not independent folds; the smaller observed shuffle range is not
evidence that ordinary shuffling is generally better.

The High-anxiety subgroup has no positive validation examples in seven of eight
holdouts. Its AUC is undefined there. The remaining holdout has only one positive;
its defined AUC is not a stable subgroup estimate. All subgroup counts and the
undefined metrics are retained. This is synthetic-data diagnostics, not a claim
about a real population or individuals.

EV-C latest Kaggle holdout results:

| Model | ROC-AUC |
|---|---:|
| Prior | 0.5000000000 |
| Logistic | 0.9393377357 |
| HGB | 0.9411786462 |

HGB minus logistic: 0.0018409104. Conditional paired percentile interval:
[0.0011476586, 0.0024933665]. This is not a Public LB score or an interval for a
future leaderboard gain. Other metrics, measured fit/predict time, and warnings
are retained in the aggregate artifacts rather than reporting only AUC.

## Environment Discrepancy Preserved

Initial local stack: NumPy 2.5.3, pandas 3.0.5, SciPy 1.18.1, scikit-learn 1.9.0.
Its HGB AUC was 0.9409975683. The difference from Kaggle was 0.0001810779;
therefore the initial 1e-6 cross-environment metric check correctly failed.
That initial failure receipt is retained as EV-C-kaggle-v1-2026-09-07.json.

A separate local environment with NumPy 2.0.2, pandas 2.3.3, SciPy 1.16.3 and
scikit-learn 1.6.1 reproduced Kaggle's AUC, average precision and paired interval.
Remaining logistic log-loss/Brier differences were at floating-point roundoff.
This changes several libraries together and does not isolate one causal package.
EV-C version 2 adds this observation and records SciPy in its live manifest;
model settings, data and partitions did not change.

Non-convergence was not observed. Solver deprecation warnings in the matched
environment are counted separately, not erased or reported as convergence failures.
The original cross-version metric mismatch remains false in the latest receipt;
the successful matched-library check is recorded separately.

## Execution And Output Review

- Eight unit tests passed in both the initial and matched numerical environments.
- Source code cells read back from Kaggle match the reviewed notebook sources.
- Official metadata confirms both notebooks remain private, CPU-only, no runtime
  internet, and only the official competition input attached.
- EV-B version 1 and EV-C versions 1 and 2 reached COMPLETE; latest artifacts were
  downloaded through official SDK-provided URLs with TLS certificate checks intact.
- EV-B has six outputs: two PNGs, three aggregate CSVs and summary.json.
- EV-C has four outputs: two PNGs, one aggregate CSV and summary.json.
- CSV files contain at most 30 aggregate rows and no record ID column. Text and
  logs were scanned for API-token markers, private local paths and tracebacks.
- PNGs were visually reviewed for labels, plotted values, legends and axes. CPU
  runtime bars vary between runs as expected; this is not a fixed hardware ranking.
- EV-B experiment timer: 13.76 seconds; EV-C latest timer: 17.96 seconds. Timers
  exclude kernel startup and initial imports. Exact runtime/memory are in receipts.
- No raw records, row predictions, model weights, official data files or credentials
  are present in the notebook output inventory or repository commit.

## Related Work And Evidence Boundaries

URL: https://www.kaggle.com/code/georgymamarin/s6e9-starter-how-to-tell-a-real-gain-from-noise
Title: S6E9 starter: how to tell a real gain from noise
Author: Georgy Mamarin
Published: UNVERIFIED; publication time not inferred from runtime or observation.
Observed: 2026-09-07.
Type: Public Notebook.
License: UNVERIFIED in this API read; no code copied or executed.
Competition version: S6E9; reference input fingerprints not independently verified.
Claimed score: Not adopted.
Verified score: UNVERIFIED.
Evidence: Read downloaded Markdown and code prefixes; not a full line-by-line code audit.
Method: CV/noise/feature comparisons and an adversarial-validation discussion.
Risk: Existing coverage means our work is not a first discovery of validation noise.
Reproduction difficulty: Not evaluated; third-party code not run.

URL: https://www.kaggle.com/code/evgendvorkin/s6e9-single-xgb-cv-0-94583
Title: S6E9 Single XGB CV: 0.94583
Author: evgendvorkin / Дворкин Евгений Владимирович
Published: UNVERIFIED; listing lastRunTime was 2026-09-05 13:21:03.030000, not publication proof.
Observed: 2026-09-07.
Type: Public Notebook.
License: UNVERIFIED in this API read; no code copied or executed.
Competition version: S6E9; exact input fingerprints unverified.
Claimed score: Title 0.94583; body also reports 0.94488 OOF / 0.94460 LB.
Verified score: UNVERIFIED; these differing claims are not reconciled or adopted.
Evidence: Read downloaded Markdown; listing showed 57 votes at observation.
Method: Feature-engineered XGB with CV, digit/frequency/target-encoding discussions.
Risk: Title/body score inconsistency and different data/model/evaluation scope.
Reproduction difficulty: Not evaluated; GPU/reference inputs were not run.

Official voteCount and dateCreated listing queries each examined three results.
Two close references were read for this implementation. This is a bounded
related-work check, not an exhaustive novelty or license audit.

## Publication Gate

Technical/content review: PASS, with the explicit environment and conditional-
uncertainty limitations above. Both notebooks are still PRIVATE.
Await confirmation to make EV-B and EV-C public; no competition submission is authorized.
