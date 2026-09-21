"""Create a byte-reproducible Kaggle submission archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("main_py", type=Path)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        type=Path,
        help="Additional root file to include; repeat for multiple files.",
    )
    args = parser.parse_args()

    source = args.main_py.resolve()
    archive = args.archive.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    source_bytes = source.read_bytes()
    compile(source_bytes, "main.py", "exec")

    members = [("main.py", source_bytes)]
    seen = {"main.py"}
    for extra_arg in args.extra:
        extra = extra_arg.resolve()
        if not extra.is_file():
            raise FileNotFoundError(extra)
        if extra.name in seen:
            raise ValueError(f"Duplicate archive member: {extra.name}")
        seen.add(extra.name)
        members.append((extra.name, extra.read_bytes()))

    archive.parent.mkdir(parents=True, exist_ok=True)
    with archive.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as tar:
                for name, content in members:
                    info = tarfile.TarInfo(name)
                    info.size = len(content)
                    info.mtime = 0
                    info.mode = 0o644
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    tar.addfile(info, io.BytesIO(content))

    archive_bytes = archive.read_bytes()
    with tarfile.open(archive, "r:gz") as tar:
        names = tar.getnames()
        archived = {name: tar.extractfile(name).read() for name in names}
    expected = dict(members)
    if names != [name for name, _ in members] or archived != expected:
        raise RuntimeError("Archive verification failed")

    manifest = {
        "source": str(source),
        "archive": str(archive),
        "root_members": names,
        "main_py_bytes": len(source_bytes),
        "main_py_sha256": digest(source_bytes),
        "member_sha256": {name: digest(content) for name, content in members},
        "archive_bytes": len(archive_bytes),
        "archive_sha256": digest(archive_bytes),
    }
    rendered = json.dumps(manifest, indent=2)
    print(rendered)
    if args.manifest:
        target = args.manifest.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
