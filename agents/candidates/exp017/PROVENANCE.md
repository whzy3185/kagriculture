# EXP017 provenance

- Created: 2026-09-22
- Parent: `agents/candidates/exp015/main.py`
- Change: abstain from the three-turn sale-advance layer when the first two
  publicly unlocked town shops are `SMOOTHIE_SHOP`, then `BAKERY`.
- Rationale: this public town sequence repeatedly drains milk, strawberry, and
  wheat, so waiting for the native sale can recover a glutted quote.
- The episode seed is never read or hard-coded.
- Submission status: experimental local candidate only; not uploaded.

All upstream license and attribution notices remain embedded in `main.py`.
