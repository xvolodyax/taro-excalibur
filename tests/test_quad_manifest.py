"""Quad manifest reads tenant cover_files.style_preset (INC-20260901-1350)."""
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
    DEFAULT_STYLE_PRESET,
    build_manifest,
    resolve_tenant_style,
)


class QuadManifestTenantStyleTest(unittest.TestCase):
    def test_tenant_preset_from_config(self) -> None:
        preset, style_file = resolve_tenant_style(ROOT)
        self.assertEqual(style_file, "memory/cover/quad-style-victoria-studio.json")
        self.assertEqual(preset, "victoria-studio")

    def test_empty_preset_keeps_pink_cat_fallback(self) -> None:
        preset, style_file = resolve_tenant_style(ROOT, tenant={"cover_files": {}})
        self.assertEqual(style_file, DEFAULT_STYLE_FILE)
        self.assertEqual(preset, DEFAULT_STYLE_PRESET)
        preset2, style_file2 = resolve_tenant_style(
            ROOT, tenant={"cover_files": {"style_preset": ""}}
        )
        self.assertEqual(style_file2, DEFAULT_STYLE_FILE)
        self.assertEqual(preset2, DEFAULT_STYLE_PRESET)

    def test_missing_tenant_keeps_fallback(self) -> None:
        preset, style_file = resolve_tenant_style(ROOT, tenant={})
        self.assertEqual(style_file, DEFAULT_STYLE_FILE)
        self.assertEqual(preset, DEFAULT_STYLE_PRESET)

    def test_build_manifest_writes_tenant_style_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp)
            (article / "article.meta.json").write_text(
                json.dumps({"topic_id": "T1"}), encoding="utf-8"
            )
            (article / "article.html").write_text(
                "<h2>Один</h2><p>a</p><h2>Два</h2><p>b</p><h2>Три</h2><p>c</p>\n",
                encoding="utf-8",
            )
            manifest = build_manifest(article, ROOT, None)
            self.assertEqual(
                manifest["style_file"],
                "memory/cover/quad-style-victoria-studio.json",
            )
            self.assertEqual(manifest["style_preset"], "victoria-studio")
            self.assertNotIn("pink-cat", manifest["style_file"])


if __name__ == "__main__":
    unittest.main()
