"""Guard quad-manifest tenant style + FAQ-like schema_faq_ui (INC-20260831-0640)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_quad_manifest import (  # noqa: E402
    DEFAULT_STYLE_FILE,
    DEFAULT_STYLE_ID,
    build_manifest,
    is_faq_like_h2,
    pick_visual_type,
    resolve_tenant_style,
)


class QuadManifestTest(unittest.TestCase):
    def test_tenant_style_is_victoria_studio_not_pink_cat(self) -> None:
        style_id, style_file = resolve_tenant_style(ROOT)
        self.assertEqual(style_id, "victoria-studio")
        self.assertEqual(style_file, "memory/cover/quad-style-victoria-studio.json")
        self.assertNotIn("pink-cat", style_file)
        self.assertEqual(style_id, DEFAULT_STYLE_ID)
        self.assertEqual(style_file, DEFAULT_STYLE_FILE)
        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        self.assertEqual(tenant["cover_files"]["style_preset"], style_file)

    def test_build_manifest_writes_tenant_style(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article_dir = Path(tmp) / "B99-style"
            article_dir.mkdir()
            (article_dir / "article.html").write_text(
                "<h1>Тема</h1>\n"
                "<h2>Что происходит</h2>\n"
                "<h2>Как часто он пишет</h2>\n"
                "<h2>Какой вопрос к картам</h2>\n",
                encoding="utf-8",
            )
            (article_dir / "article.meta.json").write_text(
                json.dumps({"topic_id": "B99"}, ensure_ascii=False),
                encoding="utf-8",
            )
            manifest = build_manifest(article_dir, ROOT, None)
            self.assertEqual(manifest["style_preset"], "victoria-studio")
            self.assertEqual(
                manifest["style_file"],
                "memory/cover/quad-style-victoria-studio.json",
            )
            self.assertNotIn("pink-cat", manifest["style_file"])
            self.assertNotEqual(manifest["style_preset"], "tenant_unset")

    def test_schema_faq_skipped_on_bare_chasto(self) -> None:
        types = json.loads(
            (ROOT / "memory/cover/inline-visual-types.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("часто", types["types"]["schema_faq_ui"]["keywords"])
        self.assertFalse(is_faq_like_h2("Как часто он пишет"))
        self.assertTrue(is_faq_like_h2("Частые вопросы про паузу"))
        self.assertTrue(is_faq_like_h2("FAQ"))
        picked = pick_visual_type("Как часто он пишет", types, set())
        self.assertNotEqual(picked, "schema_faq_ui")
        faq = pick_visual_type("Частые вопросы про паузу", types, set())
        self.assertEqual(faq, "schema_faq_ui")


if __name__ == "__main__":
    unittest.main()
