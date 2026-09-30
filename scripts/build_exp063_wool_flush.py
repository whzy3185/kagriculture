from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmark_packages" / "EXP-054-highquote-150" / "main.py"
OUTPUT = ROOT / "experiments" / "exp063_wool_flush" / "main.py"

layer = r'''

# EXP063: bounded high-quote wool flush.  On the sheep-heavy route only, two
# workers can otherwise keep harvesting while carrying valuable wool and miss
# the public high-price window.  Commit a triggered carrier to the nearest shed
# access, place its wool, and sell it immediately.  All other actions inherit
# EXP054 exactly.
_E63_PARENT = exp054_highquote_gated_closure_agent
_E63_ACTIVE = {}
_E63_REPORT = {"calls": 0, "triggers": 0, "moves": 0, "places": 0, "errors": 0}
_E63_ACCESS = ((4, 4), (4, 5), (5, 4), (5, 5))


def _e63_command(pos, target):
    x, y = int(pos[0]), int(pos[1])
    tx, ty = target
    if x > tx:
        return ["WEST"]
    if x < tx:
        return ["EAST"]
    if y > ty:
        return ["NORTH"]
    if y < ty:
        return ["SOUTH"]
    return None


def _e63_set_actor(action, actor, command, hand_count):
    if actor == 0:
        action["farmer"] = command
        return
    hands = [list(value) for value in (action.get("hands") or [])]
    while len(hands) < hand_count:
        hands.append(["PASS"])
    hands[actor - 1] = command
    action["hands"] = hands


def exp063_wool_flush_agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    if step == 0:
        _E63_ACTIVE[seat] = {}
        _E63_REPORT.update(calls=0, triggers=0, moves=0, places=0, errors=0)
    _E63_REPORT["calls"] += 1
    parent = _E63_PARENT(observation, configuration)
    try:
        farm = observation["farms"][seat]
        private = observation["private"]
        inventories = private["inventories"]
        positions = [farm["farmer"], *(farm.get("hands") or [])]
        hand_count = len(positions) - 1
        active = _E63_ACTIVE.setdefault(seat, {})
        sheep = sum(
            1
            for row in farm["tiles"]
            for tile in row
            if isinstance(tile, dict) and tile.get("animal") == "SHEEP"
        )
        quote = int((observation.get("market") or {}).get("prices", {}).get("WOOL", 0) or 0)
        if sheep >= 15 and step // 24 == 18 and quote >= 220:
            for actor, (pos, inventory) in enumerate(zip(positions, inventories)):
                wool = int(inventory.get("WOOL", 0) or 0)
                if wool < 12 or actor in active:
                    continue
                target = min(
                    _E63_ACCESS,
                    key=lambda xy: (abs(int(pos[0]) - xy[0]) + abs(int(pos[1]) - xy[1]), xy),
                )
                if abs(int(pos[0]) - target[0]) + abs(int(pos[1]) - target[1]) <= 2:
                    active[actor] = target
                    _E63_REPORT["triggers"] += 1

        result = dict(parent)
        placed = 0
        for actor, target in list(active.items()):
            if actor >= len(positions):
                active.pop(actor, None)
                continue
            wool = int(inventories[actor].get("WOOL", 0) or 0)
            if wool <= 0:
                active.pop(actor, None)
                continue
            command = _e63_command(positions[actor], target)
            if command is None:
                capacity = int((configuration or {}).get("shedCapacity", 100) if isinstance(configuration, dict) else getattr(configuration, "shedCapacity", 100))
                room = max(0, capacity - sum(int(v or 0) for v in private["shed"].values()) - placed)
                quantity = min(wool, room)
                if quantity <= 0:
                    active.pop(actor, None)
                    continue
                command = ["PLACE", "WOOL", quantity]
                placed += quantity
                active.pop(actor, None)
                _E63_REPORT["places"] += 1
            else:
                _E63_REPORT["moves"] += 1
            _e63_set_actor(result, actor, command, hand_count)

        if placed:
            market = [list(order) for order in (result.get("market") or [])]
            market = [order for order in market if not (len(order) >= 2 and order[0] == "SELL" and order[1] == "WOOL")]
            available = int(private["shed"].get("WOOL", 0) or 0) + placed
            if available > 0:
                if len(market) >= 10:
                    market = market[:9]
                market.insert(0, ["SELL", "WOOL", available])
            result["market"] = market

        if result != parent:
            state = _RACE_STATE.get(seat)
            if state is not None and state.get("prev_action") is not None and state.get("step") == step:
                state["prev_action"] = result
        return result
    except Exception:
        _E63_REPORT["errors"] += 1
        return parent


exp063_wool_flush_agent.telemetry = _E63_REPORT
agent = exp063_wool_flush_agent
kaggle_submission_agent = agent
'''

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(SOURCE.read_text(encoding="utf-8") + layer, encoding="utf-8", newline="\n")
print(OUTPUT, OUTPUT.stat().st_size)
