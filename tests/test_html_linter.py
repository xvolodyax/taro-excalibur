"""HTML whitelist: <h1> is a body tag, not a forbidden tag."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_html_linter import ALLOWED_TAGS, lint_html_file  # noqa: E402


class HtmlLinterAllowH1Test(unittest.TestCase):
    def test_h1_in_allowed_tags(self) -> None:
        self.assertIn("h1", ALLOWED_TAGS)
        source = (ROOT / "scripts/excalibur_blog_html_linter.py").read_text(encoding="utf-8")
        self.assertIn('"h1"', source)
        self.assertIn("h1, h2, h3", source)

    def test_h1_article_does_not_fail_forbidden_tag(self) -> None:
        html = (
            "<h1>Он пишет только ночью, а днём молчит</h1>\n"
            "<p>Ночной чат есть, дневного места нет.</p>\n"
            "<h2>Что происходит</h2>\n"
            "<p>Ещё абзац смысла без запретных тегов.</p>\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.html"
            path.write_text(html, encoding="utf-8")
            report = lint_html_file(path, ALLOWED_TAGS)
        self.assertEqual(report["verdict"], "pass", report)
        blob = " ".join(report["errors"]).lower()
        self.assertNotIn("forbidden html tag <h1>", blob)

    def test_unknown_tag_still_forbidden(self) -> None:
        html = "<h1>Заголовок</h1>\n<script>alert(1)</script>\n<p>Текст.</p>\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.html"
            path.write_text(html, encoding="utf-8")
            report = lint_html_file(path, ALLOWED_TAGS)
        self.assertEqual(report["verdict"], "fail")
        self.assertTrue(any("<script>" in err.lower() for err in report["errors"]))


if __name__ == "__main__":
    unittest.main()
