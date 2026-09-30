"""Verify archived EXP045/054 and materialize only their root main.py files."""
import hashlib
import json
from pathlib import Path
import tarfile

ROOT=Path(__file__).resolve().parents[1]
BASELINES=('EXP-045-masterv4-step1002','EXP-054-highquote-150')

def main():
    for label in BASELINES:
        archive=ROOT/'submissions'/f'{label}.tar.gz'
        manifest=json.loads((ROOT/'submissions'/f'{label}.manifest.json').read_text())
        assert hashlib.sha256(archive.read_bytes()).hexdigest().upper()==manifest['archive_sha256']
        with tarfile.open(archive) as opened:
            members=opened.getmembers()
            assert len(members)==1 and members[0].isfile() and members[0].name=='main.py'
            raw=opened.extractfile(members[0]).read()
        assert hashlib.sha256(raw).hexdigest().upper()==manifest['main_py_sha256']
        target=ROOT/'benchmark_packages'/label/'main.py'
        if target.exists():
            assert target.read_bytes()==raw, f'Refusing to replace different baseline: {target}'
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        print(label,'archive and source hashes verified')

if __name__=='__main__':main()
