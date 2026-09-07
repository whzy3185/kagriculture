# EV-B / EV-C Experimental Brief

Written before these experiments are executed, 2026-09-07.
Common data: official S6E9 train.csv, SHA256 eae9eaa4e6378df405e755f853771d7e26d212bd93258349fc797b771021946a.
No test input, hidden labels, original-source dataset, external models or submission export.

EV-B: Hold a logistic pipeline fixed. Compare stratified and ordinary shuffled
20% holdouts for seeds 17/43/91, and two ID-order endpoint holdouts. The 120,000-row
sample is drawn once, stratified with seed 20260907. ID is never a predictor and
is not assumed to encode chronology. Measure overall ROC-AUC, class proportions,
and Range_Anxiety_Level subgroup class coverage / whether subgroup AUC is defined.
Hypothesis: stratification constrains global prevalence variation; no prior claim
of which regime has higher AUC. Exact duplicates were absent in EV-A, so there is
no premise of exact duplicate leakage. All conditional findings and score outcomes
are UNVERIFIED until execution. Repeated holdouts overlap and are not independent
folds; show their ranges descriptively, not an iid significance test.

EV-C: Use the same fixed sample and stratified seed-17 holdout to compare prior,
logistic regression and HistGradientBoosting pipelines. Preprocessing is fitted
only on the 96,000 training rows. HGB has fixed 120 iterations and early stopping
disabled, avoiding selection of the number of rounds on the scored holdout.
Primary contrast: HGB minus logistic ROC-AUC. Hypothesis of positive contrast is
UNVERIFIED. Also report average precision, log loss, Brier and measured time.
Use 500 paired, label-stratified bootstrap replicates of that holdout contrast,
seed 2026. This conditional interval does not include training/split variability
or establish leaderboard generalization. No parameter selection from these runs.

References reviewed read-only: georgymamarin/s6e9-starter-how-to-tell-a-real-gain-from-noise
(validation/noise discussion) and evgendvorkin/s6e9-single-xgb-cv-0-94583
(feature-engineered XGB baseline). Their code is not copied or executed. No first
discovery or state-of-the-art claim is made. Third-party scores are not our verified scores.

Publication gates: unit tests, clean local run, clean private Kaggle run, aggregate
output/content review, then user confirmation. These experiments do not choose a
production model or submit any competition prediction.
