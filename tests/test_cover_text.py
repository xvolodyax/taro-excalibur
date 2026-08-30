"""Guard cover-text gate and prompt TEXT LOCK (no overlay: network draws text)."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CoverTextTest(unittest.TestCase):
    def test_gate_pass_on_clear_russian_strings(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_text_gate import validate_cover_text

        verdict = validate_cover_text(
            {
                "hook": "Cursor стал дешевле на треть",
                "highlight": "дешевле",
                "sticky": "новой модели нет",
                "inline_labels": {
                    "inline_1": ["заявление 3 августа", "минус 20–30%", "без новой модели"],
                    "inline_2": ["с экраном", "без экрана", "до 80%"],
                    "inline_3": ["MCP", "навыки", "экран"],
                },
            }
        )
        self.assertEqual(verdict["status"], "PASS")

    def test_gate_blocks_english_headline(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_text_gate import validate_cover_text

        verdict = validate_cover_text(
            {
                "hook": "Token burn rate",
                "highlight": "burn",
                "sticky": "",
                "inline_labels": {
                    "inline_1": ["токены", "экран"],
                    "inline_2": ["токены", "экран"],
                    "inline_3": ["токены", "экран"],
                },
            }
        )
        self.assertEqual(verdict["status"], "BLOCK")
        self.assertTrue(any("Latin words" in e for e in verdict["errors"]))

    def test_gate_blocks_highlight_outside_hook(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_text_gate import validate_cover_text

        verdict = validate_cover_text(
            {
                "hook": "Cursor стал дешевле на треть",
                "highlight": "бюджет",
                "sticky": "",
                "inline_labels": {
                    "inline_1": ["токены", "экран"],
                    "inline_2": ["токены", "экран"],
                    "inline_3": ["токены", "экран"],
                },
            }
        )
        self.assertEqual(verdict["status"], "BLOCK")

    def test_prompt_has_text_lock_and_russian_hook(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import build_prompt

        manifest = {
            "cover_hook": "Cursor стал дешевле на треть",
            "cover_hook_highlight": "дешевле",
            "slots": {
                "cover": {"scene_hint": "Host face LARGE left half", "sticky": "новой модели нет"},
                "inline_1": {
                    "visual_type": "infographic_card",
                    "h2_anchor": "Цифры",
                    "scene_hint": "fact card",
                    "labels": ["минус 20–30%", "заявление вендора"],
                },
                "inline_2": {"visual_type": "comparison_table_ui", "h2_anchor": "Сравнение", "scene_hint": "two columns"},
                "inline_3": {"visual_type": "workflow_diagram", "h2_anchor": "Схема", "scene_hint": "arrows"},
            },
        }
        prompt = build_prompt(manifest, {}, {}, {}, {})
        self.assertIn("TEXT LANGUAGE LOCK", prompt)
        self.assertIn("«Cursor стал дешевле на треть»", prompt)
        self.assertIn("ONLY these exact Russian strings", prompt)
        self.assertIn("«минус 20–30%»", prompt)
        self.assertIn("«новой модели нет»", prompt)

    def test_prompt_does_not_default_bold_condensed_or_pink(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import build_prompt

        manifest = {
            "cover_hook": "Он написал в одиннадцать",
            "cover_hook_highlight": "написал",
            "slots": {
                "cover": {"scene_hint": "Victoria LARGE left", "sticky": "не отвечай сразу"},
                "inline_1": {
                    "visual_type": "infographic_card",
                    "h2_anchor": "Сцена",
                    "scene_hint": "fact card",
                    "labels": ["две галочки", "пауза"],
                },
                "inline_2": {"visual_type": "comparison_table_ui", "h2_anchor": "Двери", "scene_hint": "two columns"},
                "inline_3": {"visual_type": "workflow_diagram", "h2_anchor": "Шаг", "scene_hint": "arrows"},
            },
        }
        empty = build_prompt(manifest, {}, {}, {}, {})
        self.assertNotIn("big bold condensed", empty.lower())
        self.assertNotIn("bold condensed cyrillic", empty.lower())
        self.assertNotIn("#FF1493", empty)
        self.assertIn("editorial display", empty.lower())

        import json
        design = json.loads((ROOT / "memory/cover/cover-design-code.json").read_text(encoding="utf-8"))
        style = json.loads((ROOT / "memory/cover/quad-style-victoria-studio.json").read_text(encoding="utf-8"))
        tenant = build_prompt(manifest, style, {}, {}, design)
        lock_line = next(line for line in tenant.splitlines() if "COVER TEXT LOCK" in line)
        self.assertNotIn("bold condensed", lock_line.lower())
        self.assertNotIn("accent #FF1493", tenant)
        self.assertIn("accent #C4A574", tenant)
        self.assertIn("humanist sans", tenant.lower())
        self.assertIn("Victoria", tenant)

    def test_overlay_script_removed(self) -> None:
        self.assertFalse(
            (ROOT / "scripts/excalibur_blog_cover_text_overlay.py").exists(),
            "banner overlay was rejected by user — network must draw the text",
        )
        apply_src = (ROOT / "scripts/excalibur_blog_quad_apply.py").read_text(encoding="utf-8")
        self.assertNotIn("cover_text_overlay", apply_src)


if __name__ == "__main__":
    unittest.main()
