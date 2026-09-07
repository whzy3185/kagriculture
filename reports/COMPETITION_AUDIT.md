# Competition Audit

Checked: 2026-09-07, Asia/Shanghai. Status: **BLOCKED / INCOMPLETE**.
This is an evidence ledger, not a claim that the complete competition audit passed.

Continuation: full Rules/Foundational text and official Data documents were
subsequently read; authorized account/entry checks passed. See
GATE_UPDATE_20260907.md for current state. This file retains the initial audit
observations; candidate publication and competitive validation are still gated.

## Repository Takeover

- `main`: `1ab7aaa398b1cf76f0be91aed782fabbc81f2e0d`, initialization only.
- Existing draft PR #1: https://github.com/whzy3185/kagriculture/pull/1
- Existing baseline branch: `work/baseline-v0`, tip `17f61c15dc001abf8726a57319c5ead245c9ddfd`.
- Its files: agent, requirements, evaluator, connection checker, uploader, public dataset downloader and five contract tests.
- No SCORECARD, experiment registry or submission history in that baseline tree.
- Clean checkout at takeover. Full branch history inspected (12 baseline commits).
- New research branch only. No new PR, no promotion, no production agent edits.
- API auth: **AUTH_BLOCKED**, standard environment variables and token files absent;
  connection checker exited 1. Browser login is not CLI authorization.
- Browser account: `muelsyse111`; Join Competition displayed. Rules acceptance and entry unconfirmed.
- Account submission history, active/pending entries, champion, remaining quota: **UNKNOWN**.
- Python initially only system 3.9.6; isolated Python 3.12.14 installed dependencies successfully.

## Official Findings

Primary page: https://www.kaggle.com/competitions/kaggriculture/overview
Read the rendered Overview, Timeline, Evaluation, How to Play, Getting Started
and FAQ sections in the logged-in browser. Rules page inspected separately.

| Question | Verified answer / uncertainty |
|---|---|
| Objective | Manage a farm and maximize final bank coins against another player. |
| Win condition | More bank coins; ties possible. Unsold inventory and land do not add terminal score. |
| Online rating | Outcome and opponent rating matter; coin margin does not determine rating change. Exact update equation UNKNOWN. |
| Final leaderboard | Bradley-Terry uses whole-competition episodes where BOTH agents remain active at final evaluation (staff threads 732931/739410); team uses better of two, ties half-wins. Fit regularization/prior UNKNOWN. |
| Active/final bots | Overview says latest two are tracked and used for final evaluation. Rules say select up to two; preserve discrepancy and verify final UI. |
| Inputs | player, day/hour, both public farms, market, town; own private shed/seeds/worker inventories. No opponent private inventory. |
| Outputs | farmer action, list of hand actions, ordered market orders; up to 10 market orders/turn. |
| Horizon | Advertised 30 days / 24 turns each / 720 episodeSteps. Distinguish recorded states from executed action calls in runtime evidence. |
| Action timeout | Official JSON default actTimeout=1 second; remainingOverageTime=60 seconds. Actual hosted override UNKNOWN. |
| Artifact | main.py at root; single file or tar.gz. Maximum 100 MiB. |
| Resources | FAQ: 8 GiB disk, 6.5 GiB RAM, 1.6 vCPUs. |
| External data | Allowed subject to public/equal access or reasonableness and license conditions; see COMPLIANCE.md. |
| Public code | Source/license and public-sharing conditions apply; complete long-paragraph review still required. |
| Submission quota | Maximum 5/team/day. Current remaining quota UNKNOWN. |
| Entry/merge deadline | 2026-09-23 23:59 UTC = Sep 24 07:59 China time. |
| Final submission deadline | 2026-09-30 23:59 UTC = Oct 1 07:59 China time. |
| Start | Timeline says July 29; summary UI start timestamp July 30 UTC. Historical discrepancy noted, not silently reconciled. |

## Source Version

https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py

Installed PyPI 1.32.7 source matched the fetched upstream file byte-for-byte:
`bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`.
Upstream commit SHA and deployed Kaggle source SHA remain UNKNOWN; equal local
and fetched source hashes do not establish hosted-environment equivalence.

## Updated Research Coverage

- Rules: all section headings and exposed text inspected, but accessibility
  output truncates long paragraphs. **Not** counted as full wording review.
- Code: 84 unique directory entries across five sorting views and RL/BC queries;
  one additional cited notebook. Ten originals reviewed selectively and hashed.
  No third-party code executed or adopted. Method coverage and limits are in
  `research/CODE_DISCUSSION_REVIEW.md`.
- Discussion: all eight directory pages, 155 topic IDs; twelve original threads
  and visible replies reviewed. Staff confirmation is attached to specific claims.
  48 priority topics indexed; unread topics are not promoted to evidence.
- Official episode index v39 and Sep 6 daily dataset metadata inspected (CC0).
  Live leaderboard snapshot read. Competition Data tab and full raw replay
  analysis remain incomplete; metadata inspection is not episode review.
- Browser-tab automation timed out; native browser could read official pages,
  but a shared native session changed during research. Do not equate access
  difficulties with permission to skip these sources or claim absence of updates.
- CLI public-page command attempts did not retrieve content: CLI authentication
  unavailable, and the installed CLI argument parser rejected attempted forms.

Full audit remains BLOCKED by untruncated Rules review and remaining data/runtime
checks. No Notebook or strategy candidate authored. Initial baseline/diagnostics
ran before this survey was complete; they are quarantined pipeline evidence, not
satisfaction of the research-first gate. The user corrected this ordering and
all new strategy work was paused.
