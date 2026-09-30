import hashlib
from pathlib import Path
import pytest
from kaggle_environments.agent import get_last_callable

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'benchmark_packages/EXP-054-highquote-150/main.py'
CANDIDATE=ROOT/'agents/candidates/exp20260930_expected_demand/main.py'

@pytest.fixture(scope='module')
def policies():
    return [get_last_callable(p.read_text(),path=str(p)) for p in (BASE,CANDIDATE)]

def test_baseline_immutable_and_candidate_additive():
    raw=BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='3d0002923d42add183e88f912c52b5015639e4386c9a78d7eb3dba91310c33f7'
    assert CANDIDATE.read_bytes().startswith(raw)

def test_only_expected_demand_strategy_constant_changes(policies):
    baseline,candidate=[p.__globals__ for p in policies]
    assert baseline['_HD2_FUTURE']==0.0
    assert candidate['_HD2_FUTURE']==1.0
    for name in ['_HD2_FROM','_HD2_TO','_HD2_RATIO','_HD2_MIN_GAIN','_HD2_LOOKBACK','_HD2_OPTIONS','_HD2_CARE','_HD2_SPEC','_HD2_SHOP_TYPES']:
        assert baseline[name]==candidate[name]
    assert candidate['_IMPL'].chassis.routes==baseline['_IMPL'].chassis.routes

def test_expected_demand_matches_official_uniform_draws(policies):
    f=policies[1].__globals__['_hd2_future_demand_per_day']
    assert f('WOOL')==1.5  # one single-product shop, 12 per day, probability 1/8
    assert f('MILK')==2.25 # three multi-product shops, 6 per day each, probability 1/8
    assert f('EGG')==1.5

def test_kaggle_loader_selects_candidate(policies):
    assert policies[1].__name__=='exp20260930_expected_demand_agent'
