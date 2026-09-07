# Kaggriculture Strategy Queue

Updated: 2026-09-07

Promotion rule: public Code/Discussion evidence creates an experiment candidate, never an automatic `main.py` change. All candidates must be evaluated on the current Kaggriculture engine with fresh seeds and both seats.

## Priority 0 — measurement infrastructure

### STRAT-001 — 0–180 action entropy and lineage map

Status: **APPROVED_FOR_EXPERIMENT**

Hypothesis: the first 180 turns are not one globally optimal tape; instead, a low-entropy backbone is punctuated by a small number of shop/state-conditioned forks.

Evidence:
- public replay-meta work fingerprints the first 120 actions and finds strong strategy families;
- x-ray evidence reports top-route forks around t=72–144 tied to shop draws;
- another observed top runtime agent diverged far earlier, showing that fixed replay is not a proof of optimality.

Experiment:
1. ingest fresh top replay episodes;
2. compute turn-level action entropy, modal action rate, and fingerprints;
3. condition on shop signature, seat, and lineage;
4. mark windows as `FREEZE`, `CONDITIONAL`, or `OPEN`.

Success condition: reproducible low-entropy windows and conditional forks across multiple daily dumps.

Failure condition: entropy remains high after family/shop conditioning or results are dominated by one copied lineage.

### STRAT-002 — build replay family round-robin harness

Status: **APPROVED_FOR_EXPERIMENT**

Hypothesis: economic strength is approximately transitive across current public strategy families.

Experiment:
- select representative public families;
- run fresh-seed round robin, both seats;
- estimate pairwise win matrix and detect intransitive cycles;
- record final-money and win-rate correlation.

Promotion use: establishes which public schedule is a legitimate Champion baseline.

## Priority 1 — schedule champion

### STRAT-010 — strong schedule backbone + shop route fork

Status: **RESEARCH_SUPPORTED**

Hypothesis: a strong open-loop production schedule with a small route switch at the shop epoch beats both the current melon baseline and a fully reactive rewrite.

Evidence families:
- v48 Fast Routes: six routes / four observable events;
- Adaptive Route / Shop Guard / Public-State Multi-Route;
- replay x-ray showing shop-conditioned forks around t=72–144.

Required ablation:
- backbone only;
- backbone + shop fork;
- backbone + generic reactive layer.

No-Go: do not paste a full public 720-turn tape and call it solved. Record provenance and license for any reused public implementation.

### STRAT-011 — timing-window schedule surgery

Status: **RESEARCH_SUPPORTED**

Hypothesis: a small number of economically meaningful intervention windows can improve a strong schedule without destabilizing worker positions.

Evidence:
- Farming Score series: three-day decision epochs, shop-aligned decision windows, guarded execution.

Experiment:
- change one window at a time;
- preserve all outside actions;
- require local paired improvement on fresh seeds.

## Priority 2 — livestock / pasture economics

### STRAT-020 — conserved livestock substitution

Status: **RESEARCH_SUPPORTED**

Hypothesis: replacing a bounded portion of the backbone asset mix with livestock improves long-run action/tile economics while preserving schedule geometry.

Evidence:
- Farming Score V3 public structure explicitly tests conserved livestock substitution.

Experiment dimensions:
- cow timing;
- sheep timing;
- feed reserve;
- structure amortization;
- care-frequency value;
- fertilizer side value.

Gate: one asset substitution per experiment.

### STRAT-021 — guarded latent-pasture activation

Status: **RESEARCH_SUPPORTED**

Hypothesis: preplanned pasture capacity should activate only when cash/shop/state thresholds support it.

Gate: compare fixed activation day against state-guarded activation using identical backbone.

## Priority 3 — market / terminal layer

### STRAT-030 — adaptive market hysteresis

Status: **RESEARCH_SUPPORTED**

Hypothesis: two-threshold/hysteresis market decisions reduce flip-flopping and improve near-mirror matchups versus simple fixed sell-price ratios.

Evidence:
- Adaptive Market Hysteresis notebook;
- discussion consensus that shared market is the primary direct interaction surface.

Experiment:
- fixed sell threshold;
- hysteresis thresholds;
- opponent-pressure-conditioned thresholds.

Primary metric: win rate, not average money alone.

### STRAT-031 — exact terminal frontier / liquidation policy

Status: **RESEARCH_SUPPORTED**

Hypothesis: the late-game terminal frontier can be optimized largely independently after production investment stops.

Measure:
- stranded inventory;
- unsold product value;
- late-care/water actions with no payback;
- liquidation ordering;
- final worker travel waste.

## Priority 4 — runtime adaptive challenger

### STRAT-040 — high-entropy-only runtime policy

Status: **APPROVED_FOR_DESIGN**

Hypothesis: a runtime policy should control only decisions identified as high-entropy / state-sensitive while replaying the champion backbone elsewhere.

Inputs considered first:
- shop signature;
- market pressure;
- opponent strategy fingerprint;
- weeds / execution drift;
- cash shortfall;
- terminal inventory.

Gate: must beat `Champion + shop fork` in paired fresh-seed matches.

### STRAT-041 — opponent-family market guard

Status: **RESEARCH_SUPPORTED**

Hypothesis: opponent adaptation is most valuable against near-mirror families because production plans are similar and market timing becomes the differentiator.

Experiment: detect opponent family from early public observations and alter only sell/buy timing.

## Priority 5 — search / learning

### STRAT-050 — island GA over compiled schedule deltas

Status: **RESEARCH_SUPPORTED**

Hypothesis: evolutionary search is useful when optimizing a thin layer over a valid base schedule, not independent atomic actions.

Evidence:
- Island GA notebook: “base plus thin layer”; compiler-centered representation.

Gate:
- candidate representation must compile to valid actions;
- evaluate each delta against multiple opponents/seeds;
- mutation corridor must be bounded.

### STRAT-051 — end-to-end PPO

Status: **DEFERRED**

Reason:
- public high-rank evidence still favors heuristics/schedules;
- reported end-to-end PPO results are noisy / weak;
- long credit assignment and structured action dependencies make naive atomic-action RL costly.

Revisit only after schedule champion + replay evaluator are stable.

### STRAT-052 — hybrid RL for opponent modelling / route gate

Status: **WATCH**

Rationale: high-ranked public commentary reports moderate hybrid success and RL work concentrated in opponent modelling. This is a more plausible learning target than full 720-turn control.

## Current experiment order

1. STRAT-001 — opening entropy / lineage map
2. STRAT-002 — family round robin
3. STRAT-010 — schedule backbone + shop fork
4. STRAT-020 — livestock substitution
5. STRAT-030 — market hysteresis
6. STRAT-031 — terminal frontier
7. STRAT-040 — high-entropy runtime challenger
8. STRAT-050 — thin-layer search

## Submission discipline

Do not use five daily submission slots mechanically. Maintain one stable Champion. Use the second active slot for a Challenger only after local/holdout/seat-swap gates pass. Never submit duplicate artifact hashes merely to reroll live rating.
