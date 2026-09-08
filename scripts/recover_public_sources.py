"""Recover literal public artifacts without executing any Notebook cell."""

import ast
import base64
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import tarfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / "public-20260908"
OUT = RAW / "agents"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_cells(author):
    path, = (RAW / author).glob("*.ipynb")
    notebook = json.loads(path.read_bytes())
    return path, ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def constants(cells):
    result = {}
    for source in cells:
        if source.startswith("%"):
            continue
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                try:
                    result[node.targets[0].id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
    return result


def inflate(payload):
    decoder = zlib.decompressobj()
    data = decoder.decompress(payload, 10 * 1024 * 1024)
    if not decoder.eof or decoder.unused_data:
        raise ValueError("Oversized/trailing compressed data")
    return data


def main():
    OUT.mkdir(exist_ok=True)
    inventory = []
    for author, name in (("lynnsakurai", "farming_v4"), ("tetsutani", "shape_v11"),
                         ("kaitofukami", "kaito_v58"), ("reyhanksatria", "adaptive_v2"),
                         ("thomastschinkel", "thomas_v2")):
        path, cells = source_cells(author)
        values = constants(cells)
        if author in {"lynnsakurai", "tetsutani"}:
            payload = base64.b64decode(values["MAIN_B64"], validate=True)
            expected = values.get("EXPECTED_SOURCE_SHA256", values.get("EXPECTED_MAIN_SHA256"))
        elif author == "kaitofukami":
            payload = inflate(base64.b85decode(values["payload"]))
            expected = "b041058ec187a8d0a01edc0eab8de068b53deca3e6c1973faf74ace6916ddcb9"
        elif author == "reyhanksatria":
            archive = inflate(base64.b64decode(values["PAYLOAD"]))
            if digest(archive) != values["EXPECTED_ARCHIVE_SHA"]:
                raise ValueError("Archive hash mismatch")
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                member = tar.getmember("main.py")
                if not member.isfile() or member.size > 10 * 1024 * 1024:
                    raise ValueError("Invalid main member")
                payload = tar.extractfile(member).read()
                print("Adaptive archive members:", tar.getnames(), flush=True)
            expected = None
        else:
            cell, = [s for s in cells if s.startswith("%%writefile main.py\n")]
            payload = cell.split("\n", 1)[1].encode()
            expected = None
        if expected and digest(payload) != expected:
            raise ValueError("Source hash mismatch: " + name)
        tree = ast.parse(payload)
        imports = sorted({n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
                         {alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names})
        (OUT / (name + ".py")).write_bytes(payload)
        metadata = json.loads((path.parent / "kernel-metadata.json").read_text())
        inventory.append({"name": name, "author_handle": author, "url": "https://www.kaggle.com/code/" + metadata["id"],
                          "notebook_sha256": digest(path.read_bytes()), "source_sha256": digest(payload),
                          "bytes": len(payload), "imports": imports,
                          "status": "RECOVERED_NOT_EXECUTED_SECURITY_REVIEW_REQUIRED"})
    path, cells = source_cells("ahmedberatozer")
    values = constants(cells)
    donor = (OUT / "thomas_v2.py").read_bytes()
    if digest(donor) != values["DONOR_SHA256"]:
        raise ValueError("Ahmed's versioned donor is not the recovered Thomas source")
    assignment = next(n for n in ast.parse(donor).body if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Tuple))
    blob = next(n.value for n in ast.walk(assignment.value)
                if isinstance(n, ast.Constant) and isinstance(n.value, str))
    schedules, _ = json.loads(inflate(base64.b85decode(blob)))
    if len(schedules) != 5 or any(len(route) != 719 for route in schedules):
        raise ValueError("Unexpected donor schedules")
    encoded = "".join(values["V23_TEMPLATE_B64"].split())
    encoded = encoded.replace("j1upVZZ0tyhW", "j1upVZ0tyhW").replace("xHeLNAMGEliRp", "xHeLNAMdliRp")
    template = inflate(base64.b64decode(encoded, validate=True))
    if digest(template) != "985d07220622767f8f90351c1dfd82c4b56c43407b3168692672e0435c26d841":
        raise ValueError("Ahmed template identity mismatch")
    license_text = (RAW / "LICENSE-2.0.txt").read_text().replace("\r\n", "\n")
    if digest(license_text.encode()) != "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30":
        raise ValueError("Canonical Apache license mismatch")
    data = {"base": deepcopy(schedules[0]), "patches": {}}
    for branch in (1, 2, 3, 4):
        tape = deepcopy(schedules[branch])
        tape[:144] = data["base"][:144]
        if branch in (3, 4):
            tape[144:288] = deepcopy(schedules[2][144:288])
        data["patches"][str(branch)] = [[step, action] for step, action in enumerate(tape)
                                      if action != data["base"][step]]
    route_blob = base64.b85encode(zlib.compress(json.dumps(data, separators=(",", ":")).encode(), 9)).decode()
    notice = "# SPDX-License-Identifier: Apache-2.0\n"
    notice += "# v23 modifications: public production router, audited Python chassis, and build tooling.\n"
    notice += "# Credits: thomastschinkel, yhay81, tetsutani; offline simulator: destbreso/nikital7.\n"
    notice += "".join("# " + line + "\n" for line in license_text.splitlines())
    payload = (notice + template.decode().replace("__V23_ROUTE_BLOB__", repr(route_blob))).encode()
    if digest(payload) != "6eb728a40cc55f7e497add6ea2946ce38b0389c24531a208219d48587435838e":
        raise ValueError("Ahmed final source mismatch")
    ast.parse(payload)
    (OUT / "ahmed_v23.py").write_bytes(payload)
    inventory.append({"name": "ahmed_v23", "author_handle": "ahmedberatozer",
                      "url": "https://www.kaggle.com/code/ahmedberatozer/notebook865729c24e",
                      "notebook_sha256": digest(path.read_bytes()), "source_sha256": digest(payload),
                      "bytes": len(payload), "status": "RECOVERED_NOT_EXECUTED_SECURITY_REVIEW_REQUIRED"})
    (RAW / "recovery.json").write_text(json.dumps(inventory, indent=2) + "\n")
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
