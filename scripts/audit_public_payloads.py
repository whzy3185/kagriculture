"""Inventory nested Python payloads for manual review; never execute them."""

import ast
import base64
import hashlib
import json
from pathlib import Path
import zlib

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT.parent / "public-20260908"


def inspect_source(source, label, seen, rows):
    digest = hashlib.sha256(source.encode()).hexdigest()
    if digest in seen:
        return
    seen.add(digest)
    tree = ast.parse(source)
    imports = sorted({n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
                     {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
    sensitive = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if name in {"exec", "eval", "open", "compile", "__import__"} or any(
                    token in name for token in ("subprocess", "socket", "requests", "urlopen", "CDLL", ".write", ".open", "system")):
                sensitive.append({"line": node.lineno, "call": ast.unparse(node)[:300]})
    rows.append({"label": label, "sha256": digest, "imports": imports, "review_calls": sensitive})
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in {"b85decode", "b64decode"} or not node.args:
            continue
        try:
            value = ast.literal_eval(node.args[0])
        except (ValueError, TypeError):
            continue
        if not isinstance(value, (str, bytes)):
            continue
        decoded = getattr(base64, node.func.attr)(value)
        decoder = zlib.decompressobj()
        try:
            text = decoder.decompress(decoded, 10 * 1024 * 1024).decode()
            if not decoder.eof:
                raise ValueError("Payload exceeds review size")
        except zlib.error:
            text = decoded.decode()
        except UnicodeDecodeError:
            rows.append({"label": label + ":binary", "status": "BINARY_REQUIRES_REVIEW"})
            continue
        nested_label = label + ":L" + str(node.lineno)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            inspect_source(text, nested_label, seen, rows)
        else:
            def visit(data, key):
                if isinstance(data, dict):
                    for k, v in data.items():
                        visit(v, key + "/" + k)
                elif isinstance(data, list):
                    for i, v in enumerate(data):
                        visit(v, key + "/" + str(i))
                elif isinstance(data, str) and "\n" in data and ("def " in data or "import " in data):
                    inspect_source(data, key, seen, rows)
            visit(data, nested_label)


def main():
    rows = []
    for name in ("farming_v4", "shape_v11", "thomas_v2", "ahmed_v23", "kaito_v58"):
        inspect_source((FOLDER / "agents" / (name + ".py")).read_text(), name, set(), rows)
    (FOLDER / "payload-audit.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
