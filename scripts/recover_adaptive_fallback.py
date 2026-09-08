"""Recover the separately reviewed portable Adaptive family without running cells."""

import ast
import base64
import json

from recover_public_sources import RAW, OUT, constants, digest, inflate, source_cells
from audit_public_payloads import inspect_source


def main():
    path, cells = source_cells("boatlee")
    values = constants(cells)
    assignment = next(n for s in cells for n in ast.parse(s).body
                      if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                      and n.targets[0].id == "_PACKED_SOURCE")
    parts = ast.literal_eval(assignment.value.args[0])
    payload = inflate(base64.b85decode("".join(parts)))
    if digest(payload) != values["EXPECTED_SOURCE_SHA256"] or len(payload) != values["EXPECTED_SOURCE_BYTES"]:
        raise ValueError("Portable Adaptive source mismatch")
    output = OUT / "boatlee_v20.py"
    with output.open("xb") as handle:
        handle.write(payload)
    audit = []
    inspect_source(payload.decode(), "boatlee_v20", set(), audit)
    record = {"name": "boatlee_v20", "source_sha256": digest(payload), "notebook_sha256": digest(path.read_bytes()),
              "url": "https://www.kaggle.com/code/boatlee/v20-adaptive-r1-multi-route-agent",
              "author": "boatlee", "notebook_version": 2, "source_date": "2026-08-17",
              "license": "Apache-2.0, source page verified", "audit": audit}
    (RAW / "adaptive-recovery.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
