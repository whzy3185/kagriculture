# kagriculture

Working repository for the Kaggle **Kaggriculture** simulation competition.

## Goal

Build, evaluate, and iterate a deterministic farming agent for the 720-turn two-player Kaggriculture environment.

## Current baseline

`work/baseline-v0` contains the first reproducible baseline:

- `main.py` — self-contained Kaggle agent with crop, watering, harvesting, basic labor, and market logic.
- `scripts/evaluate.py` — local head-to-head evaluator using deterministic seeds and both player seats.
- `tests/test_agent_contract.py` — action/schema smoke tests, including simultaneous seed accounting.
- `requirements.txt` — local Kaggle environment and pytest dependencies.

The baseline deliberately favors correctness and measurement over leaderboard-specific tricks. It currently uses melons while there is enough time/cash, falls back to wheat late in the season, sells inventory above a simple price floor, and caps daily hiring until experiments justify more labor.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The public competition implementation is provided through `kaggle-environments`:

```python
from kaggle_environments import make

env = make("kaggriculture")
```

## Test the action contract

```bash
pytest -q
```

## Local evaluation

Play the baseline against the built-in random opponent. Every seed is evaluated from both seats:

```bash
python scripts/evaluate.py --games 10
```

Compare against another local agent:

```bash
python scripts/evaluate.py --games 20 --opponent path/to/opponent.py
```

Use mean/median margin and the seat-swapped record as the minimum promotion criteria. Do not promote a strategy because of a single favorable seed.

## Submission

The competition entrypoint is `agent(obs)` in `main.py`. The policy is intentionally self-contained so it can be copied or packaged as `main.py` / `submission.py` in a Kaggle notebook without depending on project-local modules.

## Planned iterations

1. Run a stable seed suite against random and prior baselines.
2. Add farm-hand task assignment diagnostics and latency measurement.
3. Sweep crop mix, planting cutoffs, sale floors, and daily hand count.
4. Add land expansion only after measuring utilization and payback.
5. Evaluate livestock and market-demand timing as separate, attributable changes.
6. Archive every promoted agent so leaderboard submissions remain reproducible.
