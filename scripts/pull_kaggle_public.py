"""Download public Kaggle datasets used for Kaggriculture analysis.

Public Kaggle datasets generally do not require authentication. Competition
resources that require accepting rules are a separate case.

Examples:
    python scripts/pull_kaggle_public.py index
    python scripts/pull_kaggle_public.py episode-day --date 2026-08-08
    python scripts/pull_kaggle_public.py handle kaggle/kaggriculture-episodes-2026-08-08

The downloaded files are written under ``data/raw`` by default. That directory
is intentionally not committed to git.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import kagglehub

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "raw"
INDEX_HANDLE = "kaggle/kaggriculture-episodes-index"


def download(handle: str, output_dir: Path, path: str | None = None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = kagglehub.dataset_download(
        handle,
        path=path,
        output_dir=str(output_dir / handle.replace("/", "__")),
    )
    result = Path(downloaded)
    print(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Local destination root (default: data/raw)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    index = sub.add_parser("index", help="Download the public episode index dataset")
    index.add_argument(
        "--file",
        default=None,
        help="Optional single file, e.g. manifest.csv",
    )

    day = sub.add_parser("episode-day", help="Download one public daily episode dataset")
    day.add_argument("--date", required=True, help="YYYY-MM-DD, e.g. 2026-08-08")
    day.add_argument("--file", default=None, help="Optional exact file path inside the dataset")

    arbitrary = sub.add_parser("handle", help="Download any public Kaggle dataset handle")
    arbitrary.add_argument("handle", help="owner/dataset-slug")
    arbitrary.add_argument("--file", default=None, help="Optional exact file path inside the dataset")

    args = parser.parse_args()

    if args.command == "index":
        handle = INDEX_HANDLE
        file_path = args.file
    elif args.command == "episode-day":
        handle = f"kaggle/kaggriculture-episodes-{args.date}"
        file_path = args.file
    else:
        handle = args.handle
        file_path = args.file

    download(handle, args.output_dir, file_path)


if __name__ == "__main__":
    main()
