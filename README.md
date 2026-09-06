# kagriculture

Working repository for the Kaggle **Kaggriculture** simulation competition.

## Goal

Build, evaluate, and iterate a deterministic farming agent for the 720-turn two-player Kaggriculture environment.

## Current status

- Repository initialized.
- Competition contract verified against Kaggle's public `kaggle-environments` implementation and README.
- Development will happen on feature branches; `main` stays as the stable base.

## Development plan

1. Establish a self-contained submission agent (`main.py`).
2. Add local head-to-head evaluation with seat swapping and deterministic seeds.
3. Add contract/smoke tests for the observation/action schema.
4. Build a reproducible experiment loop and promote only measured improvements.
5. Add stronger crop/labor/land/market policies after the baseline is stable.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Kaggle's public environment can be created with:

```python
from kaggle_environments import make

env = make("kaggriculture")
```

## Submission

The submission policy is intentionally kept self-contained so it can be copied/packaged as `main.py` or `submission.py` in a Kaggle notebook without depending on the rest of this repository.
