# Gate Update - 2026-09-07

This update supersedes the earlier AUTH_BLOCKED and truncated-Rules findings.
Earlier reports remain historical evidence, not the current gate state.

## Confirmed

- Full competition-specific/general Rules and Foundational Rules read from an
  Edge single-file MHTML export. HTML-only export was only a page shell and was
  not used as evidence. The MHTML's HTML part must be decoded as UTF-8 before parsing.
- User explicitly authorized accepting Kaggriculture rules. Edge showed
  `Rules accepted. Good luck!` and `Submit Agent`; API reports entered=True.
- Existing authorization reused in file-path mode without printing or copying
  the credential. Authenticated username: muelsyse111. No new token created.
- Account/competition connection checker PASS. Submission history: zero entries.
  Live allowance at check: five. Recheck immediately before any eventual upload.
- Official Data package downloaded after joining: README.md 26824 bytes and
  AGENTS.md 13708 bytes. Both read in full. Raw package stays excluded from Git.
- Discussion Hotness view checked; its visible topic IDs were already in the
  initial catalogue. Earlier full Recent Comments sweep remains the baseline.
- Public CC0 replay 105954399 downloaded completely after using compressed HTTP.
  A first timed-out partial download is quarantined and never parsed as evidence.

## Rule Implications

General/Foundational 6.b requires public Competition Code to be shared through
this competition's Kaggle forum or notebooks. Merely having a public GitHub
repository is not assumed sufficient. Existing repository linkage and any new
public code need a competition-associated sharing record and an appropriate
open-source license. No public Kaggle post has been made by this task yet.

Public code and replay permissions, winner obligations, network isolation,
single-account/team limits, five daily submissions and latest-two final agents
remain as previously recorded. Generic private-leaderboard language conflicts
with simulation-specific wording; follow directly verified staff scoring
clarifications while preserving the textual ambiguity for final-review attention.

## Initial Continuation Decisions (Superseded Below)

- Local, isolated EXP-004 pilot: GO for experimentation, not promotion.
- Start with correctness and replay parity; then compare fixed seed pairs against
  the unchanged parent, official starter and two explicit frozen replay streams.
- This pilot is smaller than the provisional full opponent panel. It is a
  preregistered feasibility/attribution pilot, not a powered whole-field benchmark.
- New candidate code remains local until publication/sharing obligations are
  resolved. No edits to root main.py, no PR, no automatic submission.
- Submission gate still NO-GO: candidate validation, semantic market coverage,
  sandbox verification, source sharing and complete manifest/ledger checks pending.

## Latest User Direction And Current State

The user subsequently required deeper notebook investigation, decomposition of
opponent strategies, independent competition rather than copying, and quantitative
reasoning. No candidate was created. The earlier proposed EXP-004 run did not start.

Current deliverables: OPPONENT_STRATEGY_ATLAS.md, QUANT_COMPETITION_PROTOCOL.md,
analytic market-impact references, one descriptive recorded-game case and source
lineage evidence. Fourteen unique notebooks have now been examined with explicit
per-source review scope. Public sources, route tapes and weights stay outside our
policy and outside the repository.

One replay-parity adapter prototype failed before a complete local reproduction;
its source and failed result are retained in ../research-scratch, not published or
used to claim simulator parity. Descriptive raw replay facts are labelled separately.

Authentication and entry PASS. Full Rules and official Data documents have been
read. Competitive validation and source-publication obligations remain pending.
Submission remains NO-GO. Root main.py unchanged; no Kaggle submission or new PR.
