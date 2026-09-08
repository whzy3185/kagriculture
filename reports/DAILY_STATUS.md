# KAGGRICULTURE DAILY SUBMISSION

Date: 2026-09-08 (Asia/Shanghai).
Decision: **NO-GO: no candidate justified a submission today**.

## Code Reviewed

New, Recently Updated, Hot/Top, high-score and required-family views actually
checked. Source/author/update/visible-score/change records: research/daily/2026-09-08.md.
- Farming V4: https://www.kaggle.com/code/lynnsakurai/farming-score-v4-a-better-shop
- Shape: https://www.kaggle.com/code/tetsutani/shape-the-shop-work-the-pasture-kaggriculture
- Adaptive V2: https://www.kaggle.com/code/reyhanksatria/adaptive-route-agent-v2
- Portable Adaptive: https://www.kaggle.com/code/boatlee/v20-adaptive-r1-multi-route-agent
- Kaito: https://www.kaggle.com/code/kaitofukami/238-238-known-streams-v58-minimax-closed-loop
- Thomas: https://www.kaggle.com/code/thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing
- Ahmed: https://www.kaggle.com/code/ahmedberatozer/notebook865729c24e

Newest useful agent update inspected: Farming V4; it is Shape-derived and did
not win our panel. Strongest tested portable public source: Ahmed v23.

## Discussion Reviewed

New/Recently Active and original message trees read. Community claims are not
automatically accepted; role and engine checks are distinguished in daily notes.
- New RL results: https://www.kaggle.com/competitions/kaggriculture/discussion/740022
- Architecture: https://www.kaggle.com/competitions/kaggriculture/discussion/740055
- Actual fills: https://www.kaggle.com/competitions/kaggriculture/discussion/739972
- Yield/lifespan: https://www.kaggle.com/competitions/kaggriculture/discussion/740087
- Staff timeout: https://www.kaggle.com/competitions/kaggriculture/discussion/739874
- Staff security warning: https://www.kaggle.com/competitions/kaggriculture/discussion/737885

Bovard's staff reply confirms agents run in parallel and 1200s is a safe whole-
run bound, not a relaxation of actTimeout. Engine-file latest change remains
August 15. No new rule amendment verified.

## Open-source Champion

Ahmed v23, exact SHA 6eb728a40cc55f7e497add6ea2946ce38b0389c24531a208219d48587435838e.
24 new paired seeds across seven entries: 1008 games, all completed. Public-
opponent points: Ahmed 91.67%, Thomas 88.33%. Close-finalist 96 unseen paired
seeds: Ahmed 134 wins / 58 losses; mean +430.71875, median +210, p10 -675;
max call 0.0264495 s. Source/provenance: agents/champion/, OPEN_SOURCE_CHAMPION.md.
Scope: reproducible Python panel, not every public strategy. Native ARA-V2
could not be run on this macOS host. Related entries are not independent lineages.
Existing health flags remain visible; research selection is not production approval.

## Replay Comparison

Latest selected top-three-team win/loss: episodes 106731757 and 106728931.
Own deployed win/loss: 106664416 and 106678954. Top pair's field and market
actions match on [0,180), then diverge. Two selected episodes do not prove
opening optimality. Two parent benchmark losses were reproduced exactly;
cash-limited purchases at 198-224 fall between its 72-turn budget checks.
Farm/private-state parity verified on recorded-action reconstruction.

## Experiment And Validation

EXP-20260908-01. Parent: Ahmed v23. Only change: activate the existing funding
guard between normal checkpoints when current estimated purchases exceed cash.
Hypothesis: reduce cash-limited execution and improve terminal paired points.
51 tests passed, including both-seat official entrypoint contract tests.
24 fresh seeds x both seats: **0 wins, 48 losses**, all games completed.
Mean -6432.1875; median -4358; p10 -14800.1; max call 0.032385916 s.
Unfilled requests/overflow/atomic planting rejections: zero in this screen.
Strict contract flags 2360 and unit no-ops 9589 remain; no zero-invalid claim.
Candidate 96-seed validation: **NOT RUN**, as required after a failed screen.

## Retrospective

Two worst candidate losses were reproduced and cash-reconciled. Revenue fell
20818 / 17025 while spending changed only +293 / -7. Both had two extra cow
losses at turn 215 and more FEED requests without carried wheat. More frequent
cash checks did not preserve maintenance resources or output. Next research
should test physical, dated, worker-specific inventory reservations, not repeat
this trigger adjustment. Selected-case diagnostics add no independent trials.

## Submission

No new competition ref/status/score: **NOT SUBMITTED**. No approved archive.
Research disclosure only: https://www.kaggle.com/code/muelsyse111/kaggriculture-exp20260908-01-funding-audit
Its Notebook completion is not competition completion. Existing submission
56072267 remains active; observed 562.6 at 09:18:35Z, not a score for today's
candidate. Latest listed public record then: 16 wins, 20 losses (36 episodes).

Champion decision: **KEEP_PARENT**. No root main.py change, no production
promotion, no PR and no reroll. Today's formal-submission count: zero.
