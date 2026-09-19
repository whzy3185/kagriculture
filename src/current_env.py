"""Load the pinned current Kaggriculture interpreter with the local Kaggle core.

The installed ``kaggle-environments`` package is older than the competition's
current interpreter.  This module loads the pinned official interpreter source
from ``data/reference/master`` while reusing the package's generic Environment
runner.  The seed helper is patched in before importing the interpreter because
it was added after the locally installed package release.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from kaggle_environments.core import Environment
from kaggle_environments import utils as kaggle_utils


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INTERPRETER = REPO_ROOT / "data" / "reference" / "master" / "kaggriculture.py"


def resolve_episode_seed(
    env: Any,
    *,
    config_key: str = "seed",
    fallback: Callable[[], int] | None = None,
) -> int:
    """Backport the official seed helper used by the current interpreter."""

    if not hasattr(env, "info") or env.info is None:
        env.info = {}
    seed = env.info.get("seed")
    config = env.configuration
    if seed is None:
        seed = getattr(config, config_key, None)
        if seed is None and isinstance(config, dict):
            seed = config.get(config_key)
    if seed is None:
        seed = fallback() if fallback is not None else random.randrange(2**31)
    try:
        setattr(config, config_key, None)
    except (AttributeError, TypeError):
        config[config_key] = None
    env.info["seed"] = seed
    return int(seed)


def load_interpreter(path: Path = DEFAULT_INTERPRETER):
    """Import the pinned interpreter after installing the seed-helper backport."""

    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Current interpreter not found: {resolved}")

    kaggle_utils.resolve_episode_seed = resolve_episode_seed
    module_name = f"_kaggriculture_current_{abs(hash(str(resolved)))}"
    spec = importlib.util.spec_from_file_location(module_name, resolved)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import interpreter: {resolved}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def make_environment(seed: int, *, debug: bool = False) -> Environment:
    """Create a fresh two-player environment for one deterministic episode."""

    module = load_interpreter()
    specification = deepcopy(module.specification)
    return Environment(
        specification=specification,
        configuration={"seed": int(seed)},
        info={},
        agents=module.agents,
        interpreter=module.interpreter,
        renderer=module.renderer,
        html_renderer=module.html_renderer,
        debug=debug,
    )

