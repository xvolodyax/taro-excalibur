"""Guard OpenAI chat_completions.py FAIL-only path."""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "chat_completions.py"


class ChatCompletionsFailTest(unittest.TestCase):
    def test_missing_key_fails_without_invented_text(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--user", "тест"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("OPENAI_API_KEY missing", proc.stderr)
        self.assertFalse((proc.stdout or "").strip())


if __name__ == "__main__":
    unittest.main()
