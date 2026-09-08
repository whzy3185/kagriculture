# Compliance Audit

## 2026-09-08 Controlling Update

The user explicitly replaced the earlier independent-only engineering policy
with licensed public-champion reproduction plus one measured increment. Today's
research parent is byte-identical Ahmed v23, with full Apache-2.0 license and
upstream credits retained. The rejected derivative marks our only modification.
Public Code/Discussion and source-specific provenance were checked before edits.
Both parent and rejected derivative are disclosed in the competition-associated
research Notebook kaggriculture-exp20260908-01-funding-audit under muelsyse111.
That Notebook writes research source only, executes no agent and makes no
competition submission. No raw replays or credentials are published in Git.
The candidate failed its 24-seed gate and must not be submitted. The earlier
no-public-code-adoption statements below are historical, not today's policy.

Status: **EXP-006 PUBLICATION CLEARED; LIVE SUBMISSION GATES REQUIRED**.

## EXP-006 Release Authorization, 2026-09-07

After the explicit Apache-2.0 public Notebook/GitHub release question, the user
authorized Kaggle submission and GitHub synchronization. The independent
EXP-006 candidate is published under agents/candidates/EXP006-LICENSE.txt,
with attribution in EXP006-NOTICE.txt. No opponent code, tapes or weights are
included in the three-file submission archive. Root main.py remains unchanged.

Kaggle API confirmed public, competition-associated Notebook version 2 COMPLETE:
https://www.kaggle.com/code/muelsyse111/kaggriculture-exp006-independent-baseline-audit
Downloaded v2 outputs passed source/archive/member and full-game verification.
GitHub source commit 298d2074be9be6d8ecf3f00ee45dbfd625993612 has the exact
same file tree as frozen local source commit b968c37227404c84349ee380b5bd106c57e7b594.
The release clears this candidate only; it is not champion promotion or a
general license grant for unrelated pre-existing repository code.

Earlier audit text below is retained as historical evidence and is superseded
by this release update where it describes publication as blocked.

Checked at: 2026-09-07 (Asia/Shanghai). Later continuation update below supersedes
the initial text-truncation findings without treating rule acceptance as clearance.
Source for all rule entries below: https://www.kaggle.com/competitions/kaggriculture/rules
Long paragraphs in the accessibility view were truncated. These are partial,
source-backed summaries, not a complete legal clearance.

## Ownership
Rule: General 14, warranty and rights.
Official wording summary: Submission must be original work with sufficient rights to submit and grant required licenses.
Engineering implication: Preserve authorship and provenance; public visibility alone is not permission.
Allowed: Independently authored policies with verified rights.
Disallowed: Unlicensed copying or claiming third-party code as original.
Unknown: Complete long-paragraph qualifications still require review.
Source: Rules / General 14.
Checked at: 2026-09-07.

## Sharing And Open Source
Rule: General 6, submission code requirements.
Official wording summary: Private sharing between separate teams is prohibited absent permission/merger; open-source usage requires suitable OSI-approved licensing without commercial restrictions.
Engineering implication: Record author, URL, license, method, copied/reimplemented status, attribution. Keep raw competition data out of public Git.
Allowed: Properly licensed public resources after full rule review.
Disallowed: Private cross-team code exchange; adopting unknown-license agents.
Unknown: Full public-code-sharing paragraph, including required publication venue, is not fully captured. Repository currently has no LICENSE file; no public agent license is granted by this audit.
Source: Rules / General 6 and Foundational 6.
Checked at: 2026-09-07.

## External Data And Tools
Rule: Specific 6.
Official wording summary: External resources must be publicly/equally accessible without cost or meet the host's reasonableness criteria. AML tools require appropriate licensing.
Engineering implication: Record exact dataset/model versions, licenses, access requirements and cost. Evaluate each resource separately.
Allowed: Verified reasonably accessible tools/data within the rule.
Disallowed: Assuming every public notebook/dataset is permissible.
Unknown: Complete qualifications and asset-specific clearance.
Source: Rules / Specific 6.
Checked at: 2026-09-07.

## Competition Data
Rule: Specific terms 7 and Specific 4.
Official wording summary: Data access/use lists Apache 2.0, but the security provision also prohibits providing Competition Data to nonparticipants.
Engineering implication: Do not interpret the displayed license as unrestricted redistribution. Keep raw replays in excluded storage; review official public dataset licenses independently.
Allowed: Permitted research use under the complete rules.
Disallowed: Publishing raw competition data to GitHub without resolving restrictions.
Unknown: Scope of the apparent license/security tension.
Source: Rules / terms 7 and Specific 4.
Checked at: 2026-09-07.

## Winner Obligations
Rule: Specific terms 6, Specific 5 and 8.
Official wording summary: Winner license lists CC-BY 4.0; reproducible methodology and a code repository may be required, alongside prize/legal documents.
Engineering implication: Retain source, environment versions, parameters and reproducible evidence. Do not sign eligibility or tax declarations on the owner's behalf.
Allowed: Producing reproducibility records now.
Disallowed: Promising rights not held.
Unknown: Wording labels CC-BY 4.0 an OSI-approved license; this is a legal/template ambiguity, not resolved by this audit.
Source: Rules / Specific 5 and 8.
Checked at: 2026-09-07.

## Network Isolation
Rule: Specific 12, no ingress or egress.
Official wording summary: During episode evaluation submissions may not obtain information outside the submission/environment or send information out.
Engineering implication: Bundle required runtime artifacts; agent must not use network, credentials or live external APIs.
Allowed: Local decision-making on the provided observation and bundled artifacts.
Disallowed: Network inference or external state lookup during episodes.
Unknown: Hosted package/library versions.
Source: Rules / Specific 12.
Checked at: 2026-09-07.

## Team, Quota, Final And Runtime
Rule: Specific 1-3; Overview Evaluation and FAQ.
Official wording summary: Teams at most five; five submissions/day; up to two final submissions. Overview says latest two. FAQ specifies 100 MiB artifact and resource limits.
Engineering implication: Check live team/entry/pending/quota and final selection, not static assumptions. Enforce resource budget before upload.
Allowed: At most five distinct, validated uploads per day within live quota.
Disallowed: Multiple accounts, duplicated artifacts for rating resets, unknown gate evidence.
Unknown: Account-specific status and any actual sandbox timeout overrides.
Source: Rules; https://www.kaggle.com/competitions/kaggriculture/overview
Checked at: 2026-09-07.

## Provenance Used In This Branch

| Author | Source | License | Method | Copied | Reimplemented | Attribution |
|---|---|---|---|---|---|---|
| Repository owner | Existing baseline PR #1 at 17f61c1 | Repository license absent | Crop/labor policy | Inherited unchanged main.py | No | Existing Git history |
| Kaggle | kaggle-environments 1.32.7 | Apache 2.0 package header | Simulator and starter opponent | Installed dependency; no source vendored in Git | No | Imports and environment hash recorded |
| User | Supplied autonomous task chain | User-supplied instructions | Workflow | Verbatim CODEX_TASK_CHAIN.md | No | This task |

No community notebook code, models, or replay assets have been adopted.

## Staff Clarifications Read Later In This Audit

- 737788: Addison Howard (2026-08-28) permits freely and publicly available
  material. This is competition permission, not replacement asset licensing.
- 738837: Bovard (2026-09-02) permits and encourages public replay use to train,
  build and inform submissions. It does not expose hidden runtime data.
- 732931: both agents must remain active for an episode to enter final BT;
  the episode may come from any time during the competition.
- 739410: better of two submissions; ties half-wins; future play rate not guaranteed.
- Official episode index v39 and Sep 6 daily dataset both display CC0. Other
  datasets need separate checks. The daily JSON preview is truncated.
- Ten downloaded notebook pages display Apache 2.0. Hashes and targeted scope
  are recorded in research/sources/notebooks.json. Embedded backbones, compiled
  sources and models are not automatically cleared by the page's license.

Sources: research/discussion_index.csv and research/CODE_DISCUSSION_REVIEW.md.
Full legal-text review remains incomplete.

## Full-Text Continuation Update

The complete competition-specific/general and Foundational Rules were read from
an Edge MHTML export, decoding the HTML part as UTF-8. Earlier HTML-only export
contained just a shell. Full-text review is now complete, not blocked by truncation.
Raw browser exports remain outside Git; no credential or browser storage is included
in the published research. User explicitly authorized accepting the rules, and
Edge/API verified muelsyse111 has entered this competition.

Previously truncated General/Foundational 6.b explicitly requires publicly shared
Competition Code to be shared on this competition's Kaggle forum or notebooks.
The current public repository alone is not assumed to discharge that condition.
No public Kaggle post or notebook was made in this continuation. New executable
policy publication remains gated; research summaries are not a candidate release.

Our chosen engineering policy is stricter than mere permission to fork: no public
agent source, weights, tapes or fitted thresholds enter our agent. Sources inform
mechanism analysis; any later reference execution must be isolated, attributed,
credential-free and network-disabled. The unchanged declared fork of Kaito v58
is not counted as an independent lineage in opponent weighting.
