import json
from pathlib import Path

import main


def test_seed_suites_are_unique_disjoint_and_seat_swapped():
    suite = json.loads((Path(__file__).resolve().parents[1] / "configs/round1_seeds.json").read_text())
    assert suite["seats"] == [0, 1]
    assert suite["episode_steps"] == 720
    assert set(suite["fixed"]).isdisjoint(suite["holdout"])
    for key in ("fixed", "holdout"):
        assert len(suite[key]) == len(set(suite[key])) == 20


def test_documents_existing_colocated_water_duplicate():
    # Diagnostic, not an assertion of desirable behavior. Keep production frozen.
    tile = {"kind": "PLANT", "crop": "WHEAT", "watered_today": False, "yield_units": 1, "planted_day": 0}
    obs = {"player": 0, "day": 1, "hour": 1,
           "farms": [{"tiles": [[tile]], "farmer": [0, 0], "hands": [[0, 0]], "money": 0}],
           "private": {"seeds": {}, "shed": {}}}
    result = main.agent(obs)
    assert result["farmer"] == ["WATER"]
    assert result["hands"] == [["WATER"]]
