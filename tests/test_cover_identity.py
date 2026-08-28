"""Cover identity gate: hair color copied from Victoria reference, no platinum."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CoverIdentityTest(unittest.TestCase):
    def test_tenant_hair_lock_forbids_platinum_look(self) -> None:
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        lock = (hero.get("visual_lock") or {}).get("hair_color_lock") or {}
        self.assertTrue(lock.get("from_reference_only"))
        self.assertIn(
            "hair color copied exactly from reference photo, same root depth, do not lighten, no platinum",
            lock.get("prompt") or "",
        )
        hair = str((hero.get("visual_lock") or {}).get("hair") or "")
        self.assertNotIn("platinum blonde", hair.lower().replace("not platinum", ""))
        self.assertIn("honey", hair.lower())
        self.assertIn("root", hair.lower())

    def test_canon_face_png_on_disk(self) -> None:
        path = ROOT / "memory/cover/assets/viktoriaref.png"
        self.assertTrue(path.is_file(), path)
        self.assertGreater(path.stat().st_size, 1_000_000)
        self.assertTrue(path.read_bytes()[:8].startswith(b"\x89PNG\r\n\x1a\n"))

    def test_old_face_files_deleted(self) -> None:
        assets = ROOT / "memory/cover/assets"
        for name in (
            "victoria-sheet.png",
            "victoria-sheet-front.png",
            "victoria-face.png",
        ):
            self.assertFalse((assets / name).exists(), name)

    def test_canon_face_is_viktoriaref_only(self) -> None:
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        self.assertEqual(hero.get("reference_image"), "memory/cover/assets/viktoriaref.png")
        self.assertFalse(hero.get("source_sheet"))
        self.assertTrue(hero.get("sole_face_reference"))
        eye = ((hero.get("visual_lock") or {}).get("eye_color_lock") or {}).get("prompt") or ""
        self.assertIn("green with a slight hazel / light-brown tint", eye)
        forbidden = {
            "victoria-sheet.png",
            "victoria-sheet-front.png",
            "victoria-face.png",
            "victoria.png",
            "victoria_ref.jpg",
            "alena.png",
            "character-sheet-2k.png",
        }
        for folder in (ROOT / "memory" / "cover", ROOT / "cover-refs"):
            if not folder.is_dir():
                continue
            for path in folder.rglob("*"):
                self.assertNotIn(path.name.lower(), {n.lower() for n in forbidden})

    def test_tenant_gate_passes(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_identity_gate import run_gate

        verdict = run_gate(root=ROOT, article_dir=None)
        self.assertEqual(verdict["status"], "PASS", verdict)

    def test_prompt_injects_hair_lock(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import REQUIRED_HAIR_PHRASE, build_prompt

        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        design = json.loads((ROOT / "memory/cover/cover-design-code.json").read_text(encoding="utf-8"))
        style = json.loads((ROOT / "memory/cover/quad-style-victoria-studio.json").read_text(encoding="utf-8"))
        manifest = {
            "cover_hook": "Он написал в одиннадцать",
            "cover_hook_highlight": "написал",
            "slots": {
                "cover": {"scene_hint": "Victoria LARGE left", "sticky": ""},
                "inline_1": {"visual_type": "infographic_card", "h2_anchor": "Сцена", "scene_hint": "card", "labels": ["две галочки", "пауза"]},
                "inline_2": {"visual_type": "comparison_table_ui", "h2_anchor": "Двери", "scene_hint": "cols"},
                "inline_3": {"visual_type": "workflow_diagram", "h2_anchor": "Шаг", "scene_hint": "arrows"},
            },
        }
        prompt = build_prompt(manifest, style, hero, {}, design)
        self.assertTrue(
            prompt.startswith("same woman as viktoriaref.png"),
            prompt[:160],
        )
        self.assertIn("viktoriaref.png", prompt)
        self.assertNotIn("victoria-sheet-front.png", prompt)
        self.assertNotIn("victoria-face.png", prompt)
        self.assertIn(REQUIRED_HAIR_PHRASE, prompt)
        self.assertNotIn("platinum blonde", prompt.lower().split("no platinum")[0])
        from excalibur_blog_cover_identity_gate import validate_prompt

        self.assertEqual(validate_prompt(prompt), [], prompt[:400])

    def test_gate_blocks_platinum_instruction(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_identity_gate import validate_prompt

        errors = validate_prompt("Cover hero platinum blonde hair, ice-blonde, lighten the hair")
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
