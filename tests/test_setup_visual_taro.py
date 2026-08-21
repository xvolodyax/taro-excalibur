"""Setup Visual — ТАРО СЕЙЧАС: только Виктория, канон-лист в git."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VICTORIA_REF = "memory/cover/assets/виктория.png"


def _load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class SetupVisualTaroTests(unittest.TestCase):
    def test_blog_hero_victoria_sheet_ready(self) -> None:
        hero = _load("memory/cover/blog-hero.json")
        self.assertEqual(hero["cover_mode"], "host_reference")
        self.assertEqual(hero["status"], "READY")
        self.assertEqual(hero["assets_status"], "present")
        self.assertNotEqual(hero["status"], "NEED_MORE_REFS")
        self.assertNotEqual(hero["assets_status"], "need_upload")
        self.assertEqual(hero["default_host_id"], "victoria")
        self.assertEqual(hero.get("cover_hosts_allowed"), ["victoria"])
        self.assertEqual(list(hero["hosts"].keys()), ["victoria"])
        self.assertNotIn("alena", hero["hosts"])
        self.assertEqual(hero["host_selection"].get("alena_if"), "never_on_cover")
        self.assertEqual(hero.get("reference_url_hosted"), "")
        self.assertEqual(hero.get("reference_url_source"), f"local:{VICTORIA_REF}")
        self.assertEqual(hero.get("reference_image"), VICTORIA_REF)
        self.assertEqual(hero.get("reference_sheet"), VICTORIA_REF)
        self.assertEqual(hero.get("input_urls"), [VICTORIA_REF])
        self.assertFalse(any("alena" in str(x).casefold() for x in hero.get("input_urls") or []))
        self.assertNotIn("SETUP_REQUIRED", json.dumps(hero))
        lock = hero["visual_lock"]
        self.assertIn("зелён", lock["eyes"])
        self.assertIn("светло-кари", lock["eyes"])
        self.assertIn("новые", hero["outfit_rule"])
        self.assertIn("outfit", lock["do_not_lock_from_ref"])
        self.assertIn("expression", lock["do_not_lock_from_ref"])
        self.assertIn("camisole", lock["do_not_lock_from_ref"])
        self.assertTrue(any("meme_caption_ru" in x for x in hero["cover_hook_rules"]))
        self.assertIn("GREEN", hero["prompt_fragment"])
        self.assertIn("light-brown", hero["prompt_fragment"])

    def test_victoria_png_on_disk(self) -> None:
        path = ROOT / VICTORIA_REF
        self.assertTrue(path.is_file(), VICTORIA_REF)
        data = path.read_bytes()
        self.assertGreater(len(data), 0)
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_design_code_and_style_preset(self) -> None:
        design = _load("memory/cover/cover-design-code.json")
        style = _load("memory/cover/quad-style-taro-seichas.json")
        tenant = _load("shared/tenant-config.json")
        self.assertNotIn("SETUP_REQUIRED", json.dumps(design))
        self.assertNotEqual(design.get("design_code_id"), "tenant_unset")
        self.assertEqual(design["color_palette"]["background"], "#FFFFFF")
        self.assertTrue(design["color_palette"]["accent_primary"])
        self.assertFalse(style.get("allows_animal_stickers"))
        self.assertFalse(style.get("skip_human_host"))
        self.assertEqual(style.get("cover_hero_mode"), "host")
        self.assertEqual(style.get("local_reference"), VICTORIA_REF)
        self.assertTrue(style.get("prefer_local_reference"))
        self.assertIn("GREEN", style.get("global_prompt_prefix", ""))
        self.assertIn("no Alena", style.get("global_prompt_prefix", ""))
        self.assertEqual(
            tenant["cover_files"]["style_preset"],
            "memory/cover/quad-style-taro-seichas.json",
        )
        self.assertEqual(tenant["cover_mode"], "host_reference")
        self.assertEqual(tenant.get("cover_hosts_allowed"), ["victoria"])

    def test_inline_types_are_catalog_without_faces(self) -> None:
        catalog = _load("memory/cover/inline-visual-types.json")
        self.assertNotEqual(catalog.get("status"), "SETUP_REQUIRED")
        self.assertFalse(catalog.get("faces_allowed"))
        types = catalog["types"]
        self.assertIsInstance(types, dict)
        for key in (
            "comparison_table_ui",
            "workflow_diagram",
            "checklist_board",
            "schema_faq_ui",
            "infographic_card",
        ):
            self.assertIn(key, types)
            self.assertTrue(types[key].get("no_people"))
            self.assertTrue(types[key].get("keywords"))

    def test_alena_not_a_cover_asset(self) -> None:
        for rel in (
            "images/refs/alena-face.jpg",
            "memory/cover/assets/alena-face.jpg",
        ):
            self.assertFalse((ROOT / rel).is_file(), rel)
        registry = _load("shared/authors-registry.json")
        by_id = {a["id"]: a for a in registry.get("authors") or []}
        self.assertFalse(by_id["alena"].get("cover_i2i"))
        self.assertTrue(by_id["victoria"].get("cover_i2i"))

    def test_docs_point_to_victoria_png_not_alena(self) -> None:
        for rel in (
            "images/refs/README.md",
            "memory/cover/assets/README.md",
            "memory/cover/assets/NEED_UPLOAD.md",
            "memory/brief/site-brief.md",
            "memory/setup/answers.md",
            "memory/setup/visual-inbox/notes.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("alena-face", text, rel)
            self.assertNotIn("victoria-waist", text, rel)
            self.assertIn("виктория.png", text, rel)

    def test_manifest_reads_tenant_style(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_quad_manifest import (  # type: ignore
            pick_visual_type,
            tenant_style_defaults,
        )

        preset, style_file = tenant_style_defaults(ROOT)
        self.assertEqual(preset, "taro-seichas")
        self.assertEqual(style_file, "memory/cover/quad-style-taro-seichas.json")
        catalog = _load("memory/cover/inline-visual-types.json")
        picked = pick_visual_type("Пауза или конец — что это значит", catalog, set())
        self.assertIn(picked, catalog["types"])

    def test_prompt_uses_tenant_style_victoria_eyes(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import build_prompt

        style = _load("memory/cover/quad-style-taro-seichas.json")
        design = _load("memory/cover/cover-design-code.json")
        hero = _load("memory/cover/blog-hero.json")
        catalog = _load("memory/cover/inline-visual-types.json")
        manifest = {
            "cover_hook": "Пауза или конец?",
            "cover_hook_highlight": "Пауза",
            "slots": {
                "cover": {"scene_hint": hero["prompt_fragment"], "sticky": ""},
                "inline_1": {
                    "visual_type": "schema_faq_ui",
                    "h2_anchor": "Что это значит",
                    "scene_hint": "карточка вопроса без людей",
                    "labels": ["пауза", "не конец", "подожди"],
                },
                "inline_2": {
                    "visual_type": "comparison_table_ui",
                    "h2_anchor": "Ждать или написать",
                    "scene_hint": "две колонки",
                    "labels": ["ждать", "написать"],
                },
                "inline_3": {
                    "visual_type": "workflow_diagram",
                    "h2_anchor": "Что он чувствует",
                    "scene_hint": "схема шагов",
                    "labels": ["тишина", "выбор", "шаг"],
                },
            },
        }
        prompt = build_prompt(manifest, style, hero, catalog, design)
        self.assertIn("#8B3A3A", prompt)
        self.assertIn("Пауза или конец?", prompt)
        self.assertNotIn("situational funny cat", prompt)
        self.assertNotIn("#FF1493", prompt)
        self.assertIn("NO people/faces", prompt)
        self.assertIn("GREEN", prompt)
        self.assertIn("light-brown", prompt)
        self.assertIn("EVEN IF", prompt)
        self.assertIn("Victoria", prompt)
        self.assertIn("no Alena", prompt)
        self.assertIn("new outfit", prompt.lower())

    def test_resolve_cover_reference_uses_git_png(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import resolve_cover_reference

        hero = _load("memory/cover/blog-hero.json")
        style = _load("memory/cover/quad-style-taro-seichas.json")
        url, prefer_local, local_rel = resolve_cover_reference(hero, style, ROOT)
        self.assertTrue(prefer_local)
        self.assertEqual(local_rel, VICTORIA_REF)
        self.assertIn("виктория.png", url)
        self.assertIn("{{SITE_BASE}}", url)


if __name__ == "__main__":
    unittest.main()
