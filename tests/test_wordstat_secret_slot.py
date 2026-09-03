"""Wordstat secret slot: empty field in git, value never committed."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_wordstat_env import (  # noqa: E402
    ENV_KEYS,
    LOCAL_REL,
    load_wordstat_api_key,
    wordstat_key_status,
)


class WordstatSecretSlotTest(unittest.TestCase):
    def test_example_field_is_empty_and_named(self) -> None:
        example = (ROOT / "memory/wordstat.env.local.example").read_text(
            encoding="utf-8"
        )
        self.assertIn("YANDEX_CLOUD_SEARCH_API_KEY=", example)
        self.assertNotIn("yc1.", example)
        self.assertIn("gitignored", example.lower())
        env_ex = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("YANDEX_CLOUD_SEARCH_API_KEY=", env_ex)

    def test_local_file_is_gitignored_example_is_not(self) -> None:
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "memory/wordstat.env.local"],
            cwd=ROOT,
        )
        self.assertEqual(ignored.returncode, 0)
        tracked_example = subprocess.run(
            ["git", "check-ignore", "-q", "memory/wordstat.env.local.example"],
            cwd=ROOT,
        )
        self.assertEqual(tracked_example.returncode, 1)

    def test_status_never_returns_key_material(self) -> None:
        status = wordstat_key_status(ROOT)
        self.assertIn("present", status)
        self.assertIn("source", status)
        blob = str(status)
        self.assertNotIn("YANDEX_CLOUD_SEARCH_API_KEY=", blob)

    def test_loads_from_gitignored_file_without_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local = root / LOCAL_REL
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(
                f"{ENV_KEYS[0]}=unit-test-not-a-real-key\n", encoding="utf-8"
            )
            old = os.environ.pop(ENV_KEYS[0], None)
            try:
                key, source = load_wordstat_api_key(root)
            finally:
                if old is not None:
                    os.environ[ENV_KEYS[0]] = old
            self.assertEqual(source, "local_file")
            self.assertEqual(key, "unit-test-not-a-real-key")
            self.assertEqual(wordstat_key_status(root)["present"], True)

    def test_cli_does_not_print_key(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/excalibur_blog_wordstat_env.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        out = proc.stdout + proc.stderr
        self.assertIn("wordstat_key=", out)
        self.assertNotIn("yc1.", out)
        self.assertNotRegex(out, r"YANDEX_CLOUD_SEARCH_API_KEY=.+")


if __name__ == "__main__":
    unittest.main()
