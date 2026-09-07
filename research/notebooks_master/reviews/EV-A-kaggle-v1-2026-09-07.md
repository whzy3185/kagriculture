# EV-A Kaggle Run Review

Stage: KAGGLE_RUN_VERIFIED_PRIVATE. Publication has not occurred.
Notebook: https://www.kaggle.com/code/muelsyse111/s6e9-data-audit-and-id-aware-drift
Kernel ID: 133389741. Pushed version: 1. Kaggle worker status: COMPLETE.
Review date: 2026-09-07, Asia/Shanghai.

## Verified

- Updated the existing private draft; did not create a duplicate notebook.
- Official CLI readback confirms private visibility, CPU execution, internet off,
  and only the official `playground-series-s6e9` competition input attached.
- All nine code-cell sources match the locally validated source notebook.
- Downloaded all eight expected artifacts: four PNG charts, three aggregate CSVs
  and one JSON summary. No raw data, record-level predictions or submission file.
- Input SHA256 fingerprints and all stable summary statistics match the local run.
- Numeric/category distance tables match within 1e-12 relative / 1e-15 absolute
  floating-point tolerances. Schema counts match; pandas 2 versus pandas 3 string
  dtype labels differ as expected.
- Kaggle logs contain `Known-answer controls: PASS` and `Input contract: PASS`.
  No traceback. Installed mistune/nbconvert emitted SyntaxWarnings while rendering.
- All four downloaded Kaggle PNGs visually checked; labels and plotted data render.
- Artifact text checked for API token markers and private local paths: absent.
- Audit timer: 9.86 seconds, excluding kernel startup and initial imports.
- Process peak RSS: 593.17 MiB, not an incremental audit-memory measurement.
- Kaggle environment: Python 3.12.13, pandas 2.3.3, NumPy 2.0.2, SciPy 1.16.3,
  Matplotlib 3.10.0. Exact Docker image digest recorded in the JSON verification.

## Transport Issues And Boundaries

The browser editor remained in Loading Editor with Firebase auth/internal-error.
The user authorized creation of a dedicated API token, allowing the official CLI
to upload and run the private notebook. Credentials are not in this repository.

CLI pull with a `/1` suffix returned 403; a latest-version pull of the same owned
notebook succeeded. Only version 1 has been pushed at review time; no concurrent
update occurred. Source readback is therefore of the sole uploaded version, not
an unsupported claim that version-suffixed retrieval worked.

The standard output downloader failed TLS negotiation with kaggleusercontent.
Downloaded from the URLs returned by the official SDK using system curl with
normal certificate verification, checking successful HTTP status and file types.
Signed download URLs are omitted from repository artifacts.

## Publication Decision

Technical and content review: PASS for this source and the checked aggregate outputs.
Current visibility: PRIVATE.
Public visibility change: awaiting confirmation for this reviewed notebook.
No competition prediction was created, submitted or selected.
