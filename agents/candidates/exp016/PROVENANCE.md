# EXP016 provenance

- Created: 2026-09-22
- Parent: `agents/candidates/exp015/main.py`
- Parent mechanism: Pipe19 overflow/sale-advance stack with clone-aware
  reservation horizon 48.
- Change: a three-turn sale may advance only while its current quote is at or
  above the product's public base price in `V9_RACEPX_BASE`.
- Purpose: retain mirror front-running while avoiding early sales into an
  already glutted book that town demand may repair before the native sale.
- Submission status: local candidate only; not uploaded.

All upstream license and attribution notices remain embedded in `main.py`.
