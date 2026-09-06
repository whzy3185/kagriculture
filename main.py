"""Self-contained Kaggriculture baseline agent.

Design goals:
- valid JSON-safe actions
- deterministic decisions
- no dependency on project-local modules
- conservative inventory accounting for simultaneous PLANT actions
- simple crop / labor / market policy that is easy to benchmark and replace
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

CROP_RULES = {
    "WHEAT": {"seed_cost": 10, "max_yield_day": 4, "base_price": 25, "last_plant_day": 25},
    "MELON": {"seed_cost": 80, "max_yield_day": 10, "base_price": 250, "last_plant_day": 18},
}

# Start with a robust short-cycle crop, switch to melons once cash is available,
# then return to wheat near the end so capital is not stranded.
MELON_START_CASH = 500
TARGET_SEED_BUFFER = 8
MAX_DAILY_HIRES = 4
SELL_PRICE_RATIO = 0.90
LATE_LIQUIDATION_DAY = 28

Coord = Tuple[int, int]
Action = List[Any]


def _prices(obs: Dict[str, Any]) -> Dict[str, float]:
    """Support both public observation layouts seen in notebooks/environment."""
    market = obs.get("market") or {}
    prices = market.get("prices")
    if isinstance(prices, dict):
        return prices
    direct = obs.get("prices")
    return direct if isinstance(direct, dict) else {}


def _step_toward(start: Coord, target: Coord) -> Optional[str]:
    sx, sy = start
    tx, ty = target
    if sx > tx:
        return "WEST"
    if sx < tx:
        return "EAST"
    if sy > ty:
        return "NORTH"
    if sy < ty:
        return "SOUTH"
    return None


def _tile_kind(tile: Any) -> Optional[str]:
    if not isinstance(tile, dict):
        return None
    return tile.get("kind")


def _crop_name(tile: Any) -> Optional[str]:
    if not isinstance(tile, dict):
        return None
    return tile.get("crop") or tile.get("seed")


def _is_unlocked_empty(tile: Any) -> bool:
    return tile is None


def _is_weed(tile: Any) -> bool:
    return isinstance(tile, dict) and tile.get("kind") == "WEED"


def _is_plant(tile: Any) -> bool:
    return isinstance(tile, dict) and tile.get("kind") == "PLANT"


def _harvest_ready(tile: Any, day: int) -> bool:
    if not _is_plant(tile):
        return False

    crop = _crop_name(tile)
    planted_day = tile.get("planted_day")
    yield_units = tile.get("yield_units", 0) or 0

    if yield_units <= 0:
        return False

    # For crops we actively plant, wait for the configured peak day.
    if crop in CROP_RULES and planted_day is not None:
        age = day - int(planted_day)
        return age >= int(CROP_RULES[crop]["max_yield_day"])

    # Unknown/public crops: if the engine reports yield, harvesting is safer
    # than ignoring mature produce forever.
    return True


def _needs_water(tile: Any) -> bool:
    return _is_plant(tile) and not bool(tile.get("watered_today", False))


def _manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _nearest(
    origin: Coord,
    candidates: Iterable[Coord],
    reserved: Set[Coord],
) -> Optional[Coord]:
    available = [p for p in candidates if p not in reserved]
    if not available:
        return None
    return min(available, key=lambda p: (_manhattan(origin, p), p[1], p[0]))


def _scan_tasks(
    tiles: Sequence[Sequence[Any]],
    day: int,
) -> Dict[str, List[Coord]]:
    tasks = {"harvest": [], "water": [], "weed": [], "plant": []}
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            pos = (x, y)
            if tile == "LOCKED":
                continue
            if _harvest_ready(tile, day):
                tasks["harvest"].append(pos)
            elif _needs_water(tile):
                tasks["water"].append(pos)
            elif _is_weed(tile):
                tasks["weed"].append(pos)
            elif _is_unlocked_empty(tile):
                tasks["plant"].append(pos)
    return tasks


def _target_crop(day: int, money: float) -> Optional[str]:
    if day <= CROP_RULES["MELON"]["last_plant_day"] and money >= MELON_START_CASH:
        return "MELON"
    if day <= CROP_RULES["WHEAT"]["last_plant_day"]:
        return "WHEAT"
    return None


def _unit_action(
    pos: Coord,
    tiles: Sequence[Sequence[Any]],
    tasks: Dict[str, List[Coord]],
    day: int,
    crop_to_plant: Optional[str],
    seeds_left: Dict[str, int],
    reserved: Set[Coord],
) -> Action:
    x, y = pos
    tile = tiles[y][x]

    # Prefer productive work on the current square before moving.
    if _harvest_ready(tile, day):
        reserved.add(pos)
        return ["HARVEST"]

    if _needs_water(tile):
        reserved.add(pos)
        return ["WATER"]

    if _is_weed(tile):
        reserved.add(pos)
        return ["DIG"]

    if (
        tile is None
        and crop_to_plant
        and seeds_left.get(crop_to_plant, 0) > 0
    ):
        seeds_left[crop_to_plant] -= 1
        reserved.add(pos)
        return ["PLANT", crop_to_plant]

    # Route to the highest-priority unreserved task.
    for task_name in ("harvest", "water", "weed"):
        target = _nearest(pos, tasks[task_name], reserved)
        if target is not None:
            reserved.add(target)
            step = _step_toward(pos, target)
            return [step] if step else ["PASS"]

    if crop_to_plant and seeds_left.get(crop_to_plant, 0) > 0:
        target = _nearest(pos, tasks["plant"], reserved)
        if target is not None:
            reserved.add(target)
            step = _step_toward(pos, target)
            return [step] if step else ["PASS"]

    return ["PASS"]


def _market_orders(
    obs: Dict[str, Any],
    farm: Dict[str, Any],
    private: Dict[str, Any],
    crop_to_plant: Optional[str],
    active_workers: int,
) -> List[Action]:
    day = int(obs.get("day", 0) or 0)
    hour = int(obs.get("hour", 0) or 0)
    money = float(farm.get("money", 0) or 0)
    seeds = private.get("seeds") or {}
    shed = private.get("shed") or {}
    prices = _prices(obs)

    orders: List[Action] = []

    # Sell stocked crops on acceptable prices, and force liquidation near season end.
    for crop, rule in CROP_RULES.items():
        qty = int(shed.get(crop, 0) or 0)
        if qty <= 0:
            continue
        price = float(prices.get(crop, rule["base_price"]) or 0)
        threshold = float(rule["base_price"]) * SELL_PRICE_RATIO
        if day >= LATE_LIQUIDATION_DAY or price >= threshold:
            orders.append(["SELL", crop, qty])

    # Seed purchases are a buffer for future turns; planting only consumes seeds
    # already visible in private state, avoiding same-turn ordering assumptions.
    if crop_to_plant:
        have = int(seeds.get(crop_to_plant, 0) or 0)
        desired = max(TARGET_SEED_BUFFER, active_workers * 2)
        need = max(0, desired - have)
        cost = int(CROP_RULES[crop_to_plant]["seed_cost"])
        affordable = max(0, int(money // cost))
        buy = min(need, affordable)
        if buy > 0:
            orders.append(["BUY_SEED", crop_to_plant, buy])

    # Hire only once at the start of each in-game day. Hires are deliberately
    # capped until local evaluation proves that more labor pays for itself.
    if hour == 0 and day < LATE_LIQUIDATION_DAY:
        active_plants = sum(
            1
            for row in (farm.get("tiles") or [])
            for tile in row
            if _is_plant(tile)
        )
        target_hands = min(MAX_DAILY_HIRES, max(0, active_plants // 5))
        existing_hands = len(farm.get("hands") or [])
        hires = max(0, target_hands - existing_hands)
        orders.extend([["HIRE"] for _ in range(hires)])

    return orders[:10]


def agent(obs: Dict[str, Any]) -> Dict[str, Any]:
    """Kaggle entrypoint: return farmer, hands, and market actions."""
    farms = obs.get("farms") or []
    player = int(obs.get("player", 0) or 0)

    if player < 0 or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}

    farm = farms[player]
    tiles = farm.get("tiles") or []
    if not tiles:
        return {"farmer": ["PASS"], "hands": [], "market": []}

    private = obs.get("private") or {}
    seeds = dict(private.get("seeds") or {})
    day = int(obs.get("day", 0) or 0)
    money = float(farm.get("money", 0) or 0)
    crop_to_plant = _target_crop(day, money)

    tasks = _scan_tasks(tiles, day)
    reserved: Set[Coord] = set()

    farmer_pos = tuple(farm.get("farmer") or (0, 0))
    hand_positions = [tuple(p) for p in (farm.get("hands") or [])]

    farmer_action = _unit_action(
        farmer_pos,
        tiles,
        tasks,
        day,
        crop_to_plant,
        seeds,
        reserved,
    )

    hand_actions = [
        _unit_action(
            pos,
            tiles,
            tasks,
            day,
            crop_to_plant,
            seeds,
            reserved,
        )
        for pos in hand_positions
    ]

    market_orders = _market_orders(
        obs,
        farm,
        private,
        crop_to_plant,
        1 + len(hand_positions),
    )

    return {
        "farmer": farmer_action,
        "hands": hand_actions,
        "market": market_orders,
    }


# Useful aliases for notebooks that expect a differently named callable.
main = agent
