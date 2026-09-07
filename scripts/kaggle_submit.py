#!/usr/bin/env python3
"""Submit the repository's self-contained agent to Kaggriculture via Kaggle CLI.

Authentication is intentionally delegated to the official Kaggle CLI. Supported
methods include `kaggle auth login`, `KAGGLE_API_TOKEN`, or
`~/.kaggle/access_token`. Credentials must never be committed to this repo.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(cmd))
    return subprocess.run(cmd, text=True, capture_output=capture)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competition", default="kaggriculture")
    parser.add_argument("--file", default="main.py")
    parser.add_argument("--message", default="kagriculture baseline v0")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually upload. Without this flag, only preflight checks run.",
    )
    args = parser.parse_args()

    if args.execute:
        print(
            "NO-GO: the inherited uploader does not implement the required evidence, "
            "artifact, pending, compliance, and quota gates. Round 1 is BLOCKED. "
            "Implement and test the full gate before enabling uploads; see RUNBOOK.md.",
            file=sys.stderr,
        )
        return 3

    if shutil.which("kaggle") is None:
        print("Kaggle CLI is not installed. Run: pip install -U kaggle", file=sys.stderr)
        return 2

    submission = Path(args.file)
    if not submission.is_file():
        print(f"Submission file not found: {submission}", file=sys.stderr)
        return 2

    if submission.name != "main.py":
        print(
            "Warning: Kaggriculture single-file submissions are expected to use main.py.",
            file=sys.stderr,
        )

    # Auth probe: this avoids printing credentials and confirms account-scoped API access.
    probe = run(["kaggle", "datasets", "list", "--mine", "--page", "1"], capture=True)
    if probe.returncode:
        print(f"Authentication probe exited {probe.returncode}; raw output suppressed.", file=sys.stderr)
        print(
            "Kaggle authentication is unavailable to this process. Run 'kaggle auth login' "
            "or provide KAGGLE_API_TOKEN / ~/.kaggle/access_token.",
            file=sys.stderr,
        )
        return probe.returncode

    # Confirm the account has joined/accepted the competition before upload.
    entered = run(["kaggle", "competitions", "list", "--group", "entered", "-s", args.competition], capture=True)
    if entered.returncode:
        print(f"Competition probe exited {entered.returncode}; raw output suppressed.", file=sys.stderr)
        return entered.returncode
    if args.competition.lower() not in entered.stdout.lower():
        print(
            f"Authenticated, but '{args.competition}' was not found in entered competitions. "
            "Join the competition and accept its rules on kaggle.com first.",
            file=sys.stderr,
        )
        return 3

    print("Preflight passed: authenticated account, competition access, and submission file are present.")
    if not args.execute:
        print("Dry run only. Re-run with --execute to upload.")
        return 0

    submit = run(
        [
            "kaggle",
            "competitions",
            "submit",
            args.competition,
            "-f",
            str(submission),
            "-m",
            args.message,
        ]
    )
    return submit.returncode


if __name__ == "__main__":
    raise SystemExit(main())
