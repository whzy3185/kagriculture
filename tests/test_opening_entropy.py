from collections import Counter

from scripts.analyze_opening_entropy import (
    entropy_stats,
    extract_episode_seats,
    find_episode,
    find_shop_signature,
    fingerprint,
)


def test_find_episode_through_wrapper():
    payload = {"data": {"episode": {"id": 7, "steps": [[{}, {}]]}}}
    episode = find_episode(payload)
    assert episode is not None
    assert episode["id"] == 7


def test_find_shop_signature_nested():
    obs = {"shared": {"townShops": [{"kind": "BAKERY"}]}}
    signature = find_shop_signature(obs)
    assert signature is not None
    assert "BAKERY" in signature


def test_entropy_stats_identical_actions_are_zero_entropy():
    stats = entropy_stats(Counter({'["PASS"]': 10}))
    assert stats["entropy_bits"] == 0.0
    assert stats["mode_share"] == 1.0


def test_extract_episode_seats_and_fingerprints():
    episode = {
        "id": "demo",
        "steps": [
            [
                {"action": ["PASS"], "observation": {"townShops": []}},
                {"action": ["PASS"], "observation": {"townShops": []}},
            ],
            [
                {"action": ["NORTH"], "observation": {"townShops": ["BAKERY"]}},
                {"action": ["SOUTH"], "observation": {"townShops": ["BAKERY"]}},
            ],
        ],
    }
    seats = extract_episode_seats(episode, "demo", 180)
    assert len(seats) == 2
    assert len(seats[0]["actions"]) == 2
    assert seats[0]["actions"][1] != seats[1]["actions"][1]
    assert fingerprint(seats[0]["actions"], 2) != fingerprint(seats[1]["actions"], 2)
