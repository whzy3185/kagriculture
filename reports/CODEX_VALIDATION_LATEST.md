# Codex Validation

## EXP-006 Update, 2026-09-07

Decision: **COMPLETE; initial online calibration only**.
Candidate is eligible for first online baseline calibration only, not promotion.

- Independent candidate SHA: `84f11eaeceb1f2053c51947d7369b71ef6c7bdebfc66b815fbc0d04d62ecbd77`.
- Development: 96 games. Holdout: 192 games, 32 paired seeds per opponent.
- Holdout wins: legacy 64/64, starter 64/64, Shape v11 0/64.
- Candidate monitored faults: zero; holdout max call 0.052651 seconds.
- Public competition-associated Kaggle Notebook v2 COMPLETE: 11 tests and
  8 complete games, zero monitored faults; maximum cloud call 0.161371 seconds.
- Downloaded archive, candidate, license and notice match local files bytewise.
  Raw cloud reports and JUnit are retained under experiments/results/EXP-006-*.
- Local verification is reproducible with scripts/verify_cloud_evidence.py.
- User authorized public release and real submission. All gates passed before
  upload; manifest is submissions/manifests/EXP-006.json.
- Actual submission: 56072267. One quota unit consumed, four remain at check.
  COMPLETE verified at 07:56:26Z, initial score 600.0. Episode 106387464 is
  self-play VALIDATION, not evidence of beating an external opponent.
  Latest API status is in submissions/EXP-006-status.json, not inferred from
  Notebook completion. No champion approval or root main.py promotion occurred.
- GitHub source 298d2074 and local source b968c37 have identical file trees.

The earlier audit below is historical and superseded where this update differs.

## Earlier Audit

Decision: **BLOCKED / NO-GO**. Date: 2026-09-07.

- Code/Discussion: 14 targeted Notebook reviews plus the earlier Discussion audit;
  strategy mechanisms and source lineages decomposed, not every expert audited.
- Full Rules: complete competition/general/foundational text recovered and read;
  source-sharing/winner-license obligations still require candidate-specific clearance.
- Authentication / competition entry: PASS after explicit user-approved acceptance.
- Fixed seeds / seat swap: 40 completed cases; one repeat hash matched.
- Holdout: registered, NOT RUN; strategy engineering paused on user correction.
- Invalid actions: full semantic count UNKNOWN; unit no-ops observed.
- Runtime: local callable measured, hosted sandbox not certified.
- Account history: zero submissions; five slots available at check. Recheck before
  upload. No parent submission or champion exists yet.
- Candidate artifact / compliance: no candidate approved.
- No new artifact submitted; main.py byte-identical.
- Git main / existing PR untouched. New PR forbidden by latest user instruction.

No candidate was built or strategy experiment run in the continuation. Latest
direction is research-first, independent counter-strategy design, not copying
source/tapes/weights. Replay parity prototype failed early; no parity claim.

Do not use legacy uploader or raw CLI to bypass these gates. Starter-only wins,
passing software tests and the research survey do not establish live readiness.
