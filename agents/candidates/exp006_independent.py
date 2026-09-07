"""Independent crop-economy controller; no public-agent source or tapes.

Game constants and price equations follow Kaggle's Apache-2.0 environment.
Policy, budgeting, task assignment and terminal transport are independently written.
"""

import math

DEMAND_AWARE = True
EXPAND_LAND = True
ADAPTIVE_LABOR = True
TERMINAL_CASH = True

# seed, first harvest, unfertilized peak age, interval, yield, base, bonus start
CROPS = {
    "WHEAT": (10, 2, 4, 0, 4, 25, 2),
    "CARROT": (20, 2, 3, 0, 3, 35, 2),
    "TOMATO": (50, 8, 11, 1, 4, 60, 0),
    "STRAWBERRY": (100, 10, 16, 2, 4, 120, 0),
    "MELON": (80, 10, 10, 0, 6, 250, 6),
}
SHOPS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
# base, throughput, scarcity shape/target, surplus shape/target
PRICES = {
    "WHEAT": (25, 400, "sqrt", .8, "log", .2),
    "CARROT": (35, 450, "hinge", 1., "sqrt", .7),
    "TOMATO": (60, 200, "hinge", .4, "sqrt", .6),
    "STRAWBERRY": (120, 100, "sqrt", .7, "linear", 1.6),
    "MELON": (250, 300, "log", .2, "sq", 3.6),
    "EGG": (50, 332, "hinge", .4, "log", .2),
    "MILK": (160, 122, "sqrt", .6, "linear", 1.6),
    "WOOL": (200, 105, "log", .2, "sq", 3.2),
    "FERTILIZER": (100, 200, "linear", .4, "linear", .4),
}


def _shape(kind, x, throughput):
    x = max(0., x)
    if kind == "sqrt":
        return math.sqrt(x)
    if kind == "log":
        return math.log1p(x)
    if kind == "log10":
        return math.log10(1. + x)
    if kind == "sq":
        return x * x
    if kind == "hinge":
        u = x / throughput
        return u + 8. * max(0., u - 1.) ** 2
    return x


def price(item, inventory, params=None):
    base, throughput, below, bt, above, at = PRICES[item]
    p = (params or {}).get(item, {})
    base, throughput = p.get("base", base), p.get("T", throughput)
    equilibrium = p.get("I0", 10000)
    low = inventory < equilibrium
    kind = p.get("below_func", below) if low else p.get("above_func", above)
    target = p.get("below_target", bt) if low else p.get("above_target", at)
    move = target * base * _shape(kind, abs(inventory - equilibrium), throughput) / _shape(kind, throughput, throughput)
    return max(1, round(base + move if low else base - move))


def _distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _move(a, b):
    if a[0] != b[0]:
        return ["EAST" if a[0] < b[0] else "WEST"]
    if a[1] != b[1]:
        return ["SOUTH" if a[1] < b[1] else "NORTH"]
    return ["PASS"]


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _demand(item, shops, day, horizon, config):
    interval = config.get("townShopUnlockInterval", 3)
    ticks = config.get("turnsPerDay", 24) / config.get("townShopSellInterval", 4)
    center = config.get("turnsPerDay", 24) / config.get("townCenterSellInterval", 24)
    rate = sum((2 if len(SHOPS[s]) == 1 else 1) for s in shops if s in SHOPS and item in SHOPS[s]) * ticks
    expected_new = sum((2 if len(v) == 1 else 1) for v in SHOPS.values() if item in v) * ticks / len(SHOPS)
    count, result = len(shops), 0.
    for offset in range(1, horizon + 1):
        if (day + offset) % interval == 0 and count < 8:
            rate += expected_new
            count += 1
        result += rate + center
    return result


def _supply(crop, farms, day, horizon):
    _, first, peak, interval, units, _, _ = CROPS[crop]
    result = 0
    for farm in farms:
        for row in farm.get("tiles", []):
            for tile in row:
                if not isinstance(tile, dict) or tile.get("crop") != crop:
                    continue
                age = day - tile["planted_day"]
                if interval:
                    result += tile.get("yield_units", 0)
                    result += sum(age < first + k * interval <= age + horizon for k in range(4))
                elif age + horizon >= first:
                    result += max(tile.get("yield_units", 0), units)
    return result


def crop_values(obs, config, last_day):
    day = obs["day"]
    inventory = obs["market"]["inventory"]
    params = obs["market"].get("params", {})
    shops = obs.get("town", {}).get("unlocked_shops", [])
    values = {}
    for crop, (cost, first, peak, interval, maximum, base, bonus) in CROPS.items():
        horizon = min(peak, last_day - 1 - day)
        if horizon < first:
            continue
        units = sum(first + i * interval <= horizon for i in range(4)) if interval else min(maximum, 1 + max(0, horizon - bonus + 1))
        if DEMAND_AWARE:
            future_inventory = inventory[crop] + _supply(crop, obs["farms"], day, horizon) + units
            future_inventory -= _demand(crop, shops, day, horizon, config)
            expected_price = min(base * 3., price(crop, future_inventory, params)) * .9
        else:
            expected_price = base
        values[crop] = (units * expected_price - cost) / (horizon + 1)
    return values


def agent(obs, configuration=None):
    farms = obs.get("farms") or []
    player = int(obs.get("player", 0))
    if not farms or not 0 <= player < len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farm = farms[player]
    tiles = farm.get("tiles") or []
    if not tiles:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    config = configuration or {}
    tpd, total = config.get("turnsPerDay", 24), config.get("episodeSteps", 720)
    day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
    turn = day * tpd + hour
    last_day, turns_left = (total - 2) // tpd, total - 1 - turn
    final_day = TERMINAL_CASH and day == last_day
    private = obs.get("private") or {}
    seeds = dict(private.get("seeds") or {})
    carried = [dict(i) for i in private.get("inventories", [])]
    positions = [tuple(farm.get("farmer", [0, 0])), *map(tuple, farm.get("hands", []))]
    while len(carried) < len(positions):
        carried.append({})
    shed = dict(private.get("shed") or {})
    capacity = config.get("shedCapacity", 100)
    cargo = sum(sum(inv.values()) for inv in carried)
    half = len(tiles) // 2
    access = [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]
    quotes = (obs.get("market") or {}).get("prices", {})
    market_obs = dict(obs.get("market") or {})
    market_obs.setdefault("inventory", {k: 10000 for k in PRICES})
    model_obs = dict(obs, market=market_obs, day=day)
    values = crop_values(model_obs, config, last_day)
    plantable = hour <= tpd - 2 and bool(values)
    active, empty = 0, 0
    jobs = {}
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            pos = (x, y)
            if tile is None:
                empty += 1
                if plantable:
                    jobs[pos] = ("PLANT", 90.)
            elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                if plantable:
                    jobs[pos] = ("DIG", 50.)
            elif isinstance(tile, dict) and tile.get("crop") in CROPS:
                active += 1
                crop = tile["crop"]
                _, first, peak, interval, _, base, bonus = CROPS[crop]
                age = day - tile["planted_day"]
                watered = bool(tile.get("watered_today"))
                yield_units = int(tile.get("yield_units", 0))
                bonus_water = not interval and bonus <= age <= (12 if crop == "MELON" else peak)
                needs_water = not watered and (tile.get("consecutive_unwatered", 0) >= 1 or bonus_water)
                ready = yield_units > 0 and age >= first and (interval or age >= peak or day >= last_day - 1)
                if needs_water and not (final_day and not bonus_water):
                    urgency = 4000. if tile.get("consecutive_unwatered", 0) >= 1 else 1500.
                    jobs[pos] = ("WATER", urgency)
                elif ready:
                    weight = 500. + min(1500., yield_units * quotes.get(crop, base))
                    jobs[pos] = ("HARVEST", weight)

    actions = [None] * len(positions)
    worked, destinations = set(), set()

    def eligible(pos, origin):
        if pos in worked:
            return False
        op, _ = jobs[pos]
        if op == "PLANT" and not any(seeds.get(c, 0) > 0 for c in values):
            return False
        if op == "HARVEST":
            units = tiles[pos[1]][pos[0]]["yield_units"]
            if cargo + units > capacity:
                return False
            if final_day:
                return _distance(origin, pos) + 1 + min(_distance(pos, a) for a in access) + 1 <= turns_left
        if final_day and op == "WATER":
            return _distance(origin, pos) + 2 + min(_distance(pos, a) for a in access) + 1 <= turns_left
        return True

    # Local work is assigned before travel, with separate completed-tile reservations.
    for i, pos in enumerate(positions):
        inv = carried[i]
        held = sum(inv.values())
        nearest_shed = min(access, key=lambda a: (_distance(pos, a), a))
        returning = held > 0 and (final_day or cargo > 65 or held >= 12)
        if held and pos in access and (returning or hour >= tpd - 4):
            room = max(0, capacity - sum(shed.values()))
            if room >= held:
                actions[i] = ["DROP"]
                for item, quantity in inv.items():
                    shed[item] = shed.get(item, 0) + quantity
                cargo -= held
                continue
            if room:
                item = max(inv, key=lambda item: (quotes.get(item, 0), item))
                amount = min(room, inv[item])
                actions[i] = ["PLACE", item, amount]
                shed[item] = shed.get(item, 0) + amount
                cargo -= amount
                continue
        if returning and pos not in access:
            actions[i] = _move(pos, nearest_shed)
            continue
        if pos not in jobs or not eligible(pos, pos):
            continue
        op, _ = jobs[pos]
        if op == "PLANT":
            choices = [c for c in values if seeds.get(c, 0) > 0]
            crop = max(choices, key=lambda c: (values[c], c))
            seeds[crop] -= 1
            actions[i] = ["PLANT", crop]
        else:
            actions[i] = [op]
            if op == "HARVEST":
                cargo += tiles[pos[1]][pos[0]]["yield_units"]
        worked.add(pos)

    for i, pos in enumerate(positions):
        if actions[i] is not None:
            continue
        possible = [p for p in jobs if p not in destinations and p != pos and eligible(p, pos)]
        if possible:
            target = max(possible, key=lambda p: (jobs[p][1] / (1 + _distance(pos, p)), -p[1], -p[0]))
            actions[i] = _move(pos, target)
            destinations.add(target)
        else:
            actions[i] = ["PASS"]

    limit = config.get("maxMarketOrdersPerTurn", 10)
    market = [["SELL", item, int(q)] for item, q in sorted(shed.items()) if item in PRICES and q > 0][:limit]
    budget = float(farm.get("money", 0))
    # Purchases spend existing cash only. Unknown simultaneous sale receipts are not borrowed.
    if hour <= 2 and (active or empty and plantable or final_day and cargo):
        target = min(10, max(3, math.ceil((active + min(empty, 10) if plantable else active) / 7))) if ADAPTIVE_LABOR else min(4, active // 5)
        hires_today = int(farm.get("hires_today", len(farm.get("hands", []))))
        for count in range(max(0, target - len(farm.get("hands", [])))):
            cost = _fib(hires_today + count) * config.get("farmHandCostMult", 1)
            if budget < cost + 20 or len(market) >= limit:
                break
            market.append(["HIRE"])
            budget -= cost
    quadrants = len(farm.get("unlocked_quadrants", ["NW"]))
    unlocked = sum(tile != "LOCKED" for row in tiles for tile in row)
    if EXPAND_LAND and quadrants < 3 and day <= last_day - 6 and active >= unlocked * .75:
        cost = (1000, 2000, 4000)[quadrants - 1]
        if budget >= cost + 800 and len(market) < limit:
            market.append(["BUY_LAND"])
            budget -= cost
    if plantable and empty and values and len(market) < limit:
        best = max(values, key=lambda c: (values[c], c))
        if values[best] > 0:
            # Purchases arrive after this turn's planting; replenish the remaining visible stock.
            need = max(0, min(6, empty) - seeds.get(best, 0))
            amount = min(need, max(0, int((budget - 80) // CROPS[best][0])))
            if amount:
                market.append(["BUY_SEED", best, amount])
    return {"farmer": actions[0], "hands": actions[1:], "market": market}
