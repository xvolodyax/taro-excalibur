"""HTML linter whitelist: CTA wrappers stay unwrap, not new tags."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_html_linter import ALLOWED_TAGS, lint_html_file  # noqa: E402


class HtmlLinterWhitelistTest(unittest.TestCase):
    def test_div_and_strong_not_in_whitelist(self) -> None:
        self.assertNotIn("div", ALLOWED_TAGS)
        self.assertNotIn("strong", ALLOWED_TAGS)
        self.assertIn("h1", ALLOWED_TAGS)
        self.assertIn("p", ALLOWED_TAGS)
        self.assertIn("b", ALLOWED_TAGS)
        self.assertIn("a", ALLOWED_TAGS)

    def test_cta_div_strong_remain_forbidden(self) -> None:
        html = (
            "<h1>Заголовок</h1>\n"
            "<p>Текст.</p>\n"
            '<div class="cta"><p><strong>бот</strong> '
            '<a href="https://example.com/x">ссылка</a></p></div>\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.html"
            path.write_text(html, encoding="utf-8")
            report = lint_html_file(path, ALLOWED_TAGS)
        self.assertEqual(report["verdict"], "fail")
        joined = " ".join(report["errors"])
        self.assertIn("<div>", joined)
        self.assertIn("<strong>", joined)

    def test_unwrapped_cta_paragraph_passes(self) -> None:
        html = (
            "<h1>Заголовок</h1>\n"
            "<p>Текст сцены.</p>\n"
            '<p><b>бот</b> <a href="https://example.com/x">ссылка</a></p>\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.html"
            path.write_text(html, encoding="utf-8")
            report = lint_html_file(path, ALLOWED_TAGS)
        self.assertEqual(report["verdict"], "pass", report.get("errors"))


if __name__ == "__main__":
    unittest.main()
