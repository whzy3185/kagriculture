"""Poll the recorded EXP-006 dispatch without ever creating another submission."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    from kaggle import api
    ledger = ROOT / "submissions/ledger.jsonl"
    entries = [json.loads(line) for line in ledger.read_text().splitlines()]
    dispatches = [r for r in entries if r["exp_id"] == "EXP-006" and r.get("submission_ref")]
    if not dispatches:
        raise ValueError("No known submission ref; reconcile uncertain upload manually")
    entry = dispatches[-1]
    deadline = time.monotonic() + args.timeout
    last_status = entry["status"]
    while True:
        history = api.competition_submissions("kaggriculture", page_size=100) or []
        matches = [r for r in history if str(r.ref) == str(entry["submission_ref"])]
        if len(matches) != 1:
            raise ValueError("Recorded submission not uniquely visible in live history")
        row = matches[0]
        status = row.status.name
        snapshot = {"checked_at": datetime.now(timezone.utc).isoformat(),
                    "exp_id": "EXP-006", "submission_ref": row.ref, "status": status,
                    "submitted_at": row.date.isoformat(), "description": row.description,
                    "file_name": row.file_name, "total_bytes": row.total_bytes,
                    "public_score": row.public_score or None,
                    "has_error": bool(row.error_description),
                    "quota_remaining": api.competition_get_submission_limits("kaggriculture").num_allowed_now,
                    "games_played": None, "rating_confidence": "Uncalibrated first submission"}
        (ROOT / "submissions/EXP-006-status.json").write_text(json.dumps(snapshot, indent=2) + "\n")
        if status != last_status:
            entry = {**entry, "date": snapshot["checked_at"], "status": status}
            with ledger.open("a") as handle:
                handle.write(json.dumps(entry) + "\n")
            print(json.dumps(snapshot), flush=True)
            last_status = status
        if status in {"COMPLETE", "ERROR", "FAILED"}:
            return 0 if status == "COMPLETE" else 2
        if time.monotonic() >= deadline:
            print("POLL_TIMEOUT: submission remains", status, "do not resubmit", flush=True)
            return 3
        time.sleep(30)


if __name__ == "__main__":
    raise SystemExit(main())
