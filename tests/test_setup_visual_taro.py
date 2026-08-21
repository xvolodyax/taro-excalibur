"""Setup Visual — ТАРО СЕЙЧАС: rules ready, refs honestly missing."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class SetupVisualTaroTests(unittest.TestCase):
    def test_blog_hero_host_reference_need_more_refs(self) -> None:
        hero = _load("memory/cover/blog-hero.json")
        self.assertEqual(hero["cover_mode"], "host_reference")
        self.assertEqual(hero["status"], "NEED_MORE_REFS")
        self.assertEqual(hero["default_host_id"], "victoria")
        self.assertIn("alena", hero["hosts"])
        self.assertEqual(hero.get("reference_url_hosted"), "")
        self.assertEqual(hero.get("reference_url_source"), "")
        self.assertFalse(hero.get("reference_image"))
        self.assertNotIn("SETUP_REQUIRED", json.dumps(hero))
        lock = hero["visual_lock"]
        self.assertIn("новые", hero["outfit_rule"])
        self.assertIn("outfit", lock["do_not_lock_from_ref"])
        self.assertIn("expression", lock["do_not_lock_from_ref"])
        self.assertTrue(any("meme_caption_ru" in x for x in hero["cover_hook_rules"]))

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
        self.assertEqual(style.get("local_reference"), "")
        self.assertEqual(
            tenant["cover_files"]["style_preset"],
            "memory/cover/quad-style-taro-seichas.json",
        )
        self.assertEqual(tenant["cover_mode"], "host_reference")

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

    def test_no_face_assets_in_git_paths(self) -> None:
        for rel in (
            "images/refs/victoria-face.jpg",
            "images/refs/victoria-waist.jpg",
            "images/refs/alena-face.jpg",
            "images/refs/alena-waist.jpg",
            "memory/cover/assets/victoria-face.jpg",
            "memory/cover/assets/alena-face.jpg",
        ):
            self.assertFalse((ROOT / rel).is_file(), rel)

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

    def test_prompt_uses_tenant_style_not_cat_hero(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
