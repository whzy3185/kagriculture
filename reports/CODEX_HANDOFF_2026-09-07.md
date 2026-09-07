# Codex Handoff — Meta Research v1 (2026-09-07)

Branch: `work/meta-research-v1`

This handoff converts current public Code/Discussion evidence into an executable first-round validation plan. It does **not** approve a production submission by itself.

## Non-negotiable environment gate

1. Pin and print the actual `kaggle-environments` version used for every experiment.
2. Target the current competition engine (`1.32.7` unless Kaggle has published a newer required version at execution time).
3. Run both seats; do not trust seat-0-only tests.
4. Check the current official environment for the reported seat-1 `obs["step"]` issue before using `obs["step"]` as the sole clock.
5. Record runtime and invalid actions.

## Round 1 objective

Replace the current melon/wheat pipeline baseline with a **measured Champion baseline derived from the current public strategy frontier**, without yet attempting a full end-to-end RL agent.

## Task 1 — acquire current public replay evidence

Use public Kaggle replay sources, preferring newest data:

- daily top replay archives;
- public episode service / CDN where allowed;
- representative public notebooks / agents.

Record every source in a manifest:

```text
source_url
author
license
retrieved_at
script_version / dataset_version
engine_version
```

Do not commit large raw replay archives to Git.

## Task 2 — quantify turns 0–180

Run:

```bash
python scripts/analyze_opening_entropy.py \
  --input <replay-dir> \
  --out-dir results/opening_entropy \
  --max-turn 180
```

Review:

- `opening_entropy.csv`
- `opening_conditional_entropy.csv`
- `opening_turn_classes.csv`
- `lineages.csv`
- `summary.json`

Important caveat: copied public lineages can make action entropy artificially low. Repeat across multiple dates and source families.

### Required conclusion

Partition 0–180 into contiguous windows labelled:

- `FREEZE_CANDIDATE`
- `CONDITIONAL_CANDIDATE`
- `OPEN_OR_LINEAGE_MIXED`

Do not call any window “optimal” from entropy alone.

## Task 3 — select representative public opponents / backbones

At execution time, fetch the latest public versions and record exact provenance. Candidate families to inspect first:

1. Kaito Fukami — Fast Routes family
2. Arlene — Farming Score / replay-revised / timing-optimized family
3. Shape the Shop Work the Pasture family
4. Adaptive Route Agent family
5. one genuinely reactive / runtime public agent if available

Public notebook score is not the selection criterion. Prefer fresh head-to-head evidence.

## Task 4 — build family round robin

Triage stage:

- >= 24 fresh seeds;
- both seats;
- all candidate families;
- record win rate and final-money delta.

Promotion stage for top candidates:

- >= 96 fresh seeds;
- both seats;
- report confidence interval;
- check for intransitive cycles.

The main metric is **win rate**. Final money is diagnostic / explanatory.

## Task 5 — establish Champion

Champion requirements:

- strongest or statistically tied strongest representative in the round robin;
- reproducible source/artifact;
- license/provenance recorded;
- no runtime errors;
- valid under current engine;
- survives both seats.

Store Champion separately from production `main.py` until gates pass.

## Task 6 — first five isolated challengers

Run these as isolated experiments, one major variable each.

### EXP-META-001 — shop-conditioned fork

Parent: Champion backbone.

Change: route only at the shop-conditioned divergence window found by entropy/x-ray analysis.

### EXP-META-002 — livestock substitution

Parent: Champion backbone.

Change: one bounded cow/sheep asset substitution. Preserve surrounding schedule as much as possible.

### EXP-META-003 — latent pasture activation

Parent: Champion backbone.

Change: fixed pasture activation -> state/cash/shop guarded activation.

### EXP-META-004 — market hysteresis

Parent: Champion backbone.

Change: fixed sale policy -> bounded two-threshold / opponent-pressure-aware market policy.

### EXP-META-005 — terminal frontier

Parent: Champion backbone.

Change: late-game investment cutoff / liquidation order only.

## Task 7 — promotion statistics

For each challenger report:

```text
exp_id
parent
seeds
both_seats
wins
losses
ties
win_rate
Wilson/bootstrapped CI
mean_money_delta
median_money_delta
worst_decile_delta
runtime_errors
invalid_actions
p95_runtime
```

A candidate is not promoted on a single high-money run.

## Task 8 — production promotion

Only after an experiment passes:

1. fixed-seed gate;
2. holdout-seed gate;
3. both-seat gate;
4. runtime gate;
5. provenance/compliance gate;
6. artifact hash gate.

Then build a new self-contained `main.py` candidate and rerun the complete suite.

## Task 9 — Kaggle submission strategy

Do not mechanically consume five submissions/day.

Maintain:

- Slot A: stable Champion / current best COMPLETE agent;
- Slot B: one genuine Challenger.

Submit only after local promotion. Never submit a duplicate artifact hash to reroll live rating.

Poll to terminal status and only record `COMPLETE` scores in `SCORECARD.md`.

## Round 1 stop condition

Round 1 is complete only when we have:

- an entropy map for 0–180 from fresh replay data;
- a current public-family round robin;
- a reproducible Champion;
- results for the five isolated challengers;
- at least one evidence-backed production candidate OR a documented NO-GO;
- replay/failure analysis for any actual Kaggle submission.

## Research judgment to preserve

Current evidence supports this architecture order:

```text
strong schedule backbone
+ shop/state route gate
+ bounded livestock/pasture changes
+ market hysteresis
+ terminal frontier
+ high-entropy runtime challenger
```

End-to-end PPO remains deferred until the schedule/evaluation pipeline is stable.
