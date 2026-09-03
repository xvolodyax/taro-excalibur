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
        self.assertIn("Виктория.png", tenant)
        self.assertIn("Host LARGE left", tenant)

    def test_victoria_studio_short_hints_fit_prompt_budget(self) -> None:
        """Tenant style + 4 short hints + 4 labels must stay ≤3500 (INC-20260829-1753)."""
        import json
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import (
            MAX_MCP_PROMPT_CHARS,
            build_prompt,
            validate_prompt_budget,
        )

        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        design = json.loads(
            (ROOT / "memory/cover/cover-design-code.json").read_text(encoding="utf-8")
        )
        style = json.loads(
            (ROOT / "memory/cover/quad-style-victoria-studio.json").read_text(
                encoding="utf-8"
            )
        )
        cover_hint = (
            "Victoria LARGE left half, tiny phone on the table, high-key studio, "
            "no MUST face essay."
        )
        inline_hint = (
            "White card, two columns, gold accent, humanist sans labels, no faces."
        )
        manifest = {
            "cover_hook": "Ты видишь измену в его паузе",
            "cover_hook_highlight": "паузе",
            "slots": {
                "cover": {"scene_hint": cover_hint, "sticky": "не пиши первой"},
                "inline_1": {
                    "visual_type": "infographic_card",
                    "h2_anchor": "Разбор ситуации",
                    "scene_hint": inline_hint,
                    "labels": ["две галочки", "пауза", "не отвечай", "смотри время"],
                },
                "inline_2": {
                    "visual_type": "comparison_table_ui",
                    "h2_anchor": "Две двери",
                    "scene_hint": inline_hint,
                    "labels": ["дверь А", "дверь Б", "пауза", "ответ"],
                },
                "inline_3": {
                    "visual_type": "workflow_diagram",
                    "h2_anchor": "Что делать",
                    "scene_hint": inline_hint,
                    "labels": ["шаг один", "шаг два", "шаг три", "стоп"],
                },
            },
        }
        prompt = build_prompt(manifest, style, hero, {}, design)
        self.assertLessEqual(len(prompt), MAX_MCP_PROMPT_CHARS, len(prompt))
        self.assertTrue(validate_prompt_budget(prompt))
        self.assertGreater(len(prompt), 2000)
        self.assertIn("Host LARGE left", prompt)
        self.assertIn("Виктория.png", prompt)
        self.assertRegex(prompt, r"type cannot drop/replace host")

    def test_victoria_studio_first_try_host_lock(self) -> None:
        """First billed gen must lock Host LARGE left + Виктория.png (INC-0636)."""
        import json
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_cover_quad_prompt import build_prompt

        style = json.loads(
            (ROOT / "memory/cover/quad-style-victoria-studio.json").read_text(
                encoding="utf-8"
            )
        )
        prefix = str(style.get("global_prompt_prefix") or "")
        self.assertIn("Виктория.png", prefix)
        self.assertIn("Host LARGE left", prefix)
        self.assertIn("NEVER replace host", prefix)
        design = json.loads(
            (ROOT / "memory/cover/cover-design-code.json").read_text(encoding="utf-8")
        )
        manifest = {
            "cover_hook": "Он не обсуждает будущее",
            "cover_hook_highlight": "будущее",
            "slots": {
                "cover": {
                    "scene_hint": "Host LARGE left half, tiny Saturday calendar RIGHT only",
                    "sticky": "там посмотрим",
                },
                "inline_1": {
                    "visual_type": "infographic_card",
                    "h2_anchor": "Сцена",
                    "scene_hint": "fact card",
                },
                "inline_2": {
                    "visual_type": "comparison_table_ui",
                    "h2_anchor": "Двери",
                    "scene_hint": "two columns",
                },
                "inline_3": {
                    "visual_type": "workflow_diagram",
                    "h2_anchor": "Шаг",
                    "scene_hint": "arrows",
                },
            },
        }
        prompt = build_prompt(manifest, style, {}, {}, design)
        self.assertIn("face fills left", prompt)
        self.assertIn("RIGHT only", prompt)
        self.assertEqual(style.get("style_id"), "victoria-studio")
        self.assertNotIn("pink-cat collage", str(style.get("global_prompt_prefix") or "").lower())

    def test_overlay_script_removed(self) -> None:
        self.assertFalse(
            (ROOT / "scripts/excalibur_blog_cover_text_overlay.py").exists(),
            "banner overlay was rejected by user — network must draw the text",
        )
        apply_src = (ROOT / "scripts/excalibur_blog_quad_apply.py").read_text(encoding="utf-8")
        self.assertNotIn("cover_text_overlay", apply_src)


if __name__ == "__main__":
    unittest.main()
