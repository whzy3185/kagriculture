"""Record available own-submission episodes; keep raw replay payloads out of Git."""

import contextlib
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    from kaggle import api

    status = json.loads((ROOT / "submissions/EXP-006-status.json").read_text())
    ref = status["submission_ref"]
    episodes = api.competition_list_episodes(ref) or []
    checked = datetime.now(timezone.utc).isoformat()
    snapshot = {"submission_ref": ref, "checked_at": checked,
                "listed_episode_count": len(episodes),
                "coverage": "API listing only; not assumed to be complete lifetime history",
                "episodes": [e.to_dict() for e in episodes], "downloads": []}
    index = ROOT / "replays/index.csv"
    with index.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fields, index_rows = reader.fieldnames, list(reader)
    known = {r["episode_id"] for r in index_rows}
    for episode in [e for e in episodes if e.state.name == "COMPLETED"][:2]:
        if str(episode.id) in known:
            continue
        folder = ROOT / "replays/raw"
        folder.mkdir(parents=True, exist_ok=True)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                api.competition_episode_replay(episode.id, path=str(folder), quiet=True)
            path = folder / f"episode-{episode.id}-replay.json"
            json.loads(path.read_bytes())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except Exception as error:
            snapshot["downloads"].append({"episode_id": episode.id, "status": "FAILED",
                                          "error_type": type(error).__name__})
            continue
        snapshot["downloads"].append({"episode_id": episode.id, "status": "DOWNLOADED",
                                      "path": str(path.relative_to(ROOT)), "sha256": digest})
        index_rows.append({"episode_id": episode.id, "submission_ref": ref,
                           "source_url": "", "observed_at": checked,
                           "environment_version": "UNKNOWN", "local_path": str(path.relative_to(ROOT)),
                           "sha256": digest, "status": "DOWNLOADED_VIA_OFFICIAL_API_NOT_YET_ANALYZED"})
    with index.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(index_rows)
    (ROOT / "submissions/EXP-006-episodes.json").write_text(json.dumps(snapshot, indent=2, default=str) + "\n")
    print(json.dumps({k: v for k, v in snapshot.items() if k != "episodes"}))


if __name__ == "__main__":
    main()
