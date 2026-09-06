#!/usr/bin/env python3
"""Verify Kaggle CLI authentication without printing secrets.

This script intentionally never reads or prints the token itself. It checks that the
official Kaggle CLI can authenticate by requesting the current user's datasets and,
optionally, the Kaggriculture competition submission list.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout.strip():
        print(proc.stdout.rstrip())
    if proc.returncode and proc.stderr.strip():
        print(proc.stderr.rstrip(), file=sys.stderr)
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--competition",
        default="kaggriculture",
        help="Competition slug used for the authenticated submission probe.",
    )
    parser.add_argument(
        "--skip-competition",
        action="store_true",
        help="Only verify account-level dataset access.",
    )
    args = parser.parse_args()

    if shutil.which("kaggle") is None:
        print("Kaggle CLI is not installed. Run: pip install -U kaggle", file=sys.stderr)
        return 2

    print("[1/2] Checking authenticated account access via 'datasets list --mine'...")
    rc = run(["kaggle", "datasets", "list", "--mine", "--page", "1"])
    if rc:
        print(
            "\nAuthentication is not available to this process. Use 'kaggle auth login' "
            "or set KAGGLE_API_TOKEN / ~/.kaggle/access_token. Do not commit credentials.",
            file=sys.stderr,
        )
        return rc

    if args.skip_competition:
        print("\nKaggle authentication probe succeeded.")
        return 0

    print("\n[2/2] Checking Kaggriculture competition access...")
    rc = run(["kaggle", "competitions", "submissions", args.competition, "--page-size", "5"])
    if rc:
        print(
            "\nAccount authentication works, but competition access failed. "
            "Make sure the competition rules have been accepted in Kaggle.",
            file=sys.stderr,
        )
        return rc

    print("\nKaggle account + competition access probe succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
