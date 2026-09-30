"""Build one frozen candidate; never modify the EXP054 baseline package."""
from pathlib import Path
import hashlib

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'benchmark_packages/EXP-054-highquote-150/main.py'
DEST=ROOT/'agents/candidates/exp20260930_expected_demand/main.py'
EXPECTED='3d0002923d42add183e88f912c52b5015639e4386c9a78d7eb3dba91310c33f7'
raw=BASE.read_bytes()
assert hashlib.sha256(raw).hexdigest()==EXPECTED
layer=b'''

# EXP-20260930-01: expected future shop demand in the existing HERD2 model.
# One strategic change: use the already-implemented expected demand of future
# uniformly drawn shops when valuing a new supported animal choice. Keep all
# cash, gain, ratio, timing, placement, and action-rewrite guards unchanged.
# This is an experimental local candidate, not a promoted or submitted policy.
_HD2_FUTURE = 1.0
_E67_PARENT = exp054_highquote_gated_closure_agent
_E67_REPORT = {"calls": 0, "future_demand_multiplier": 1.0}

def exp20260930_expected_demand_agent(observation, configuration=None):
    if int(observation.get("step", 0)) == 0:
        _E67_REPORT["calls"] = 0
    _E67_REPORT["calls"] += 1
    return _E67_PARENT(observation, configuration)

exp20260930_expected_demand_agent.telemetry = _E67_REPORT
agent = exp20260930_expected_demand_agent
kaggle_submission_agent = agent
'''
DEST.parent.mkdir(parents=True,exist_ok=True)
DEST.write_bytes(raw+layer)
print(DEST,hashlib.sha256(DEST.read_bytes()).hexdigest())
