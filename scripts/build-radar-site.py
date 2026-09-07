#!/usr/bin/env python3
"""Package the public Pages surface only; never copy local server state."""
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
if OUT.is_symlink():
    raise RuntimeError('Refusing to build into a symlink')
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
# Tracked files are the public allowlist. No local drafts, heartbeats or receipts.
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
paths = [p for p in tracked if p.startswith(('data/', 'output/', 'content/deepdive/'))]
paths += ['index.html', 'publish.html', 'assets/radar.css', 'assets/radar.js',
          'skills/ai-daily-digest/cards.css', 'skills/ai-daily-digest/cards.js']
for name in sorted(set(paths)):
    source = ROOT / name
    if source.is_symlink():
        raise RuntimeError(f'Refusing symlink: {name}')
    if not source.is_file():
        raise RuntimeError(f'Missing public file: {name}')
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
index = json.loads((OUT / 'output/index.json').read_text())
for day in index['days']:
    path = OUT / 'data' / day.get('vendor', 'anthropic') / f"{day['date']}.json"
    if not path.is_file():
        raise RuntimeError(f'Missing edition: {path}')
print(f'Built {len(set(paths))} public files; verified {len(index["days"])} edition references.')
