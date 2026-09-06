from main import agent


def _obs(seeds=None, shed=None, hands=None, money=3000, day=1, hour=1):
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            row.append(None if x < 5 and y < 5 else "LOCKED")
        tiles.append(row)

    me = {
        "money": money,
        "farmer": [4, 4],
        "hands": hands or [],
        "tiles": tiles,
    }
    opp = {
        "money": 3000,
        "farmer": [4, 4],
        "hands": [],
        "tiles": [row[:] for row in tiles],
    }
    return {
        "player": 0,
        "day": day,
        "hour": hour,
        "farms": [me, opp],
        "private": {"seeds": seeds or {}, "shed": shed or {}},
        "market": {"prices": {"WHEAT": 25, "MELON": 250}},
    }


def test_contract_keys_and_action_lists():
    result = agent(_obs())
    assert set(result) == {"farmer", "hands", "market"}
    assert isinstance(result["farmer"], list)
    assert isinstance(result["hands"], list)
    assert isinstance(result["market"], list)


def test_farmer_plants_visible_seed():
    result = agent(_obs(seeds={"MELON": 1}))
    assert result["farmer"] == ["PLANT", "MELON"]


def test_simultaneous_planting_never_exceeds_visible_seed_count():
    result = agent(
        _obs(
            seeds={"MELON": 2},
            hands=[[3, 4], [2, 4], [1, 4]],
        )
    )
    all_actions = [result["farmer"], *result["hands"]]
    plant_actions = [a for a in all_actions if a and a[0] == "PLANT"]
    assert len(plant_actions) <= 2


def test_locked_tiles_are_not_selected_for_planting():
    obs = _obs(seeds={"MELON": 1})
    obs["farms"][0]["farmer"] = [5, 4]  # passable but locked tile
    result = agent(obs)
    assert result["farmer"][0] in {"WEST", "NORTH", "SOUTH", "EAST", "PASS"}
    assert result["farmer"][0] != "PLANT"


def test_invalid_observation_falls_back_to_pass():
    assert agent({}) == {"farmer": ["PASS"], "hands": [], "market": []}
