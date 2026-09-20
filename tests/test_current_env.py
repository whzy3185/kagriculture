from pathlib import Path

from kaggle_environments.agent import get_last_callable

from src.current_env import DEFAULT_INTERPRETER, make_environment


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_current_interpreter_contract():
    text = DEFAULT_INTERPRETER.read_text(encoding="utf-8")
    assert '"COW":   {"cost": 400' in text
    assert '"below_func": "hinge"' in text
    env = make_environment(123)
    assert env.configuration.episodeSteps == 720
    assert env.configuration.turnsPerDay == 24
    assert env.info["seed"] == 123


def test_current_candidate_is_kaggle_loadable_and_smokes():
    candidate = REPO_ROOT / "agents" / "candidates" / "exp008" / "main.py"
    callable_agent = get_last_callable(candidate.read_text(encoding="utf-8"), path=str(candidate))
    assert callable(callable_agent)

    env = make_environment(123)
    env.configuration.episodeSteps = 3
    env.run([str(candidate), "starter"])
    assert all(str(state.status) == "DONE" for state in env.state)
