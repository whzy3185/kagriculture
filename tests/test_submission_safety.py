import importlib.util
from pathlib import Path
import subprocess
from types import SimpleNamespace


def load_script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_connection_probe_never_echoes_cli_output(monkeypatch, capsys):
    module = load_script("kaggle_connection_check")
    monkeypatch.setattr(module.subprocess, "run", lambda *a, **kw: SimpleNamespace(
        returncode=1, stdout="SECRET_SENTINEL", stderr="SECRET_SENTINEL"))
    assert module.run(["kaggle", "datasets", "list", "--mine"]) == 1
    captured = capsys.readouterr()
    assert "SECRET_SENTINEL" not in captured.out + captured.err


def test_connection_probe_timeout_is_bounded(monkeypatch):
    module = load_script("kaggle_connection_check")

    def timeout(*args, **kwargs):
        assert kwargs["timeout"] == 60
        raise subprocess.TimeoutExpired(args[0], 60)

    monkeypatch.setattr(module.subprocess, "run", timeout)
    assert module.run(["kaggle", "datasets", "list", "--mine"]) == 124


def test_execute_is_fail_closed_before_network(monkeypatch):
    module = load_script("kaggle_submit")
    monkeypatch.setattr(module.sys, "argv", ["kaggle_submit.py", "--execute"])

    def forbidden(*args, **kwargs):
        raise AssertionError("No CLI/network action allowed before the gate")

    monkeypatch.setattr(module.subprocess, "run", forbidden)
    assert module.main() == 3
