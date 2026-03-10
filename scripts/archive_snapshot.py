#!/usr/bin/env python3
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output'
ARCH = OUT / 'archive'


def copy_any(src: Path, dst: Path):
    if not src.exists():
        return
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main():
    ts = datetime.now().strftime('%Y-%m-%d')
    day = ARCH / ts
    day.mkdir(parents=True, exist_ok=True)

    for name in ['latest.json', 'latest.md', 'index.html', 'wisckey-analysis.html']:
        src = OUT / name
        copy_any(src, day / name)

    copy_any(OUT / 'analysis', day / 'analysis')

    index = ARCH / 'index.json'
    items = []
    if index.exists():
        try:
            items = json.loads(index.read_text())
        except Exception:
            items = []
    if ts not in items:
        items.insert(0, ts)
    index.write_text(json.dumps(items[:30], ensure_ascii=False, indent=2))
    print(str(day))

if __name__ == '__main__':
    main()
