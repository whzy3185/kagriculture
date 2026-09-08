"""Fetch explicitly selected episode evidence without emitting signed URLs."""

import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", nargs="+", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from kaggle import api
    folder = ROOT / "replays/raw"
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for episode in args.episodes:
        path = folder / f"episode-{episode}-replay.json"
        try:
            if not path.exists():
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    api.competition_episode_replay(episode, path=str(folder), quiet=True)
            data = json.loads(path.read_bytes())
            if not isinstance(data.get("steps"), list) or len(data["steps"]) != 720:
                raise ValueError("Incomplete replay")
            row = {"episode_id": episode, "status": "DOWNLOADED",
                   "path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                   "engine_version": data.get("module_version"), "steps": len(data["steps"]),
                   "terminal_statuses": data.get("statuses"), "rewards": data.get("rewards")}
        except Exception as error:
            row = {"episode_id": episode, "status": "FAILED", "error_type": type(error).__name__}
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "rows": rows,
              "scope": "Selected observed episode IDs only; no population representativeness claim"}
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
