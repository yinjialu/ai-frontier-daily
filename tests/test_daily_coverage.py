import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_daily_coverage.py"


class DailyCoverageTest(unittest.TestCase):
    def test_missing_ledger_is_rejected(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--check", "--date", "2099-01-01"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("缺少", proc.stderr)

    def test_validator_requires_cn_matrix_and_open_prs(self):
        text = SCRIPT.read_text("utf-8")
        self.assertTrue("cn_companies" in text or "daily-search-matrix.json" in text)
        self.assertIn("--include-open-prs", text)
