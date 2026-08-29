"""Canon 2026-08-29: cover.png stays out of article body."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from excalibur_blog_html_linter import detect_cover_hero_in_body, lint_html_file, ALLOWED_TAGS  # noqa: E402


class CoverHeroBodyBanTest(unittest.TestCase):
    def test_cover_hero_class_fails(self) -> None:
        errs = detect_cover_hero_in_body('<figure class="cover-hero" data-slot="cover"></figure>')
        self.assertTrue(any("cover-hero" in e for e in errs))

    def test_cover_png_src_fails(self) -> None:
        errs = detect_cover_hero_in_body('<img src="cover/cover.png" alt="x">')
        self.assertTrue(any("cover.png" in e for e in errs))

    def test_scena_word_fails(self) -> None:
        errs = detect_cover_hero_in_body("<p>Сцена: телефон</p>")
        self.assertTrue(any("Сцена" in e for e in errs))

    def test_inline_only_ok(self) -> None:
        html = '<h2>X</h2><figure class="inline-quad" data-slot="inline_1"></figure>'
        self.assertEqual(detect_cover_hero_in_body(html), [])

    def test_b22_article_has_no_cover_hero(self) -> None:
        path = ROOT / "memory/blog/articles/B22-on-pishet-hotya-vy-uzhe-rasstalis/article.html"
        self.assertTrue(path.is_file())
        report = lint_html_file(path, ALLOWED_TAGS)
        self.assertEqual(report["verdict"], "pass", report)
        html = path.read_text(encoding="utf-8")
        self.assertNotIn("cover-hero", html)
        self.assertNotIn("cover/cover.png", html)


if __name__ == "__main__":
    unittest.main()
