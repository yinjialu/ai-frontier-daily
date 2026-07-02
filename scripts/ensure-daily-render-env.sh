#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required. Install uv first: https://docs.astral.sh/uv/" >&2
  exit 1
fi

echo "[1/5] Python environment"
uv venv .venv --python "${PYTHON_VERSION:-3.12}"
uv pip install -r requirements.txt

echo "[2/5] Node dependencies"
npm install

echo "[3/5] Playwright browser"
npx playwright install chromium

echo "[4/5] Python smoke test"
.venv/bin/python skills/ai-daily-digest/run.py --vendors >/tmp/ai-daily-vendors.json
.venv/bin/python - <<'PY'
import json
from pathlib import Path

vendors = json.loads(Path("/tmp/ai-daily-vendors.json").read_text("utf-8"))
assert vendors, "vendor list is empty"
for vendor in vendors:
    assert vendor.get("id"), vendor
print("vendors:", ", ".join(v["id"] for v in vendors))
PY

echo "[5/5] Playwright smoke test"
node - <<'NODE'
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch({ timeout: 15000 });
  const page = await browser.newPage();
  await page.setContent('<html><body><h1>ok</h1></body></html>');
  const text = await page.textContent('h1');
  await browser.close();
  if (text !== 'ok') throw new Error(`unexpected smoke text: ${text}`);
  console.log('playwright: ok');
})().catch(err => {
  console.error(err);
  process.exit(1);
});
NODE

echo "Daily render environment is ready."
