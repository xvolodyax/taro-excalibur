"""Victoria host-credit overlay: Pillow after split, never Kie letters, never Alena."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_cover_quad_prompt import build_prompt  # noqa: E402
from excalibur_blog_cover_quad_split import (  # noqa: E402
    create_demo_canvas,
    default_manifest,
    split_canvas,
)
from excalibur_blog_host_credit_overlay import (  # noqa: E402
    CANON_VICTORIA_CREDIT,
    apply_host_credit,
    decide_host_credit,
    load_credit_canon,
    stamp_credit_on_image,
)


class HostCreditCanonTests(unittest.TestCase):
    def test_living_canon_files_hold_exact_string(self) -> None:
        hero, design = load_credit_canon(ROOT)
        self.assertEqual(hero["credit_overlay"]["text"], CANON_VICTORIA_CREDIT)
        self.assertEqual(
            CANON_VICTORIA_CREDIT, "Виктория - таролог команды «ТАРО СЕЙЧАС»"
        )
        self.assertFalse(CANON_VICTORIA_CREDIT.startswith('"'))
        self.assertFalse(CANON_VICTORIA_CREDIT.startswith("«"))
        self.assertTrue(CANON_VICTORIA_CREDIT.endswith("«ТАРО СЕЙЧАС»"))
        self.assertNotIn('"', CANON_VICTORIA_CREDIT)
        self.assertTrue(hero["credit_overlay"]["never_ask_image_model"])
        self.assertIn("Алёна", hero["credit_overlay"]["never_apply_when_name_matches"])
        self.assertNotIn("http", hero["credit_overlay"]["text"])
        self.assertNotIn("www.", hero["credit_overlay"]["text"])
        overlays = design["host_credit_overlays"]
        self.assertEqual(overlays[0]["text"], CANON_VICTORIA_CREDIT)
        self.assertTrue(any("Виктория" in rule for rule in design["cover_rules"]))

    def test_prompt_forbids_model_letters_and_omits_credit_string(self) -> None:
        manifest = {
            "cover_hook": "Расклад на новую работу",
            "cover_hook_highlight": "работу",
            "slots": {
                "cover": {"scene_hint": "Host face LARGE left half", "sticky": "не гадай сама"},
                "inline_1": {
                    "visual_type": "infographic_card",
                    "h2_anchor": "Карты",
                    "scene_hint": "fact card",
                    "labels": ["три карты", "вопрос"],
                },
                "inline_2": {"visual_type": "comparison_table_ui", "h2_anchor": "Сравнение", "scene_hint": "two columns"},
                "inline_3": {"visual_type": "workflow_diagram", "h2_anchor": "Схема", "scene_hint": "arrows"},
            },
        }
        prompt = build_prompt(manifest, {}, {}, {}, {})
        self.assertNotIn(CANON_VICTORIA_CREDIT, prompt)
        self.assertNotIn("таролог команды", prompt)
        self.assertIn("Do not paint host credit", prompt)
        self.assertIn("Pillow overlays", prompt)

    def test_old_banner_overlay_still_absent(self) -> None:
        self.assertFalse((ROOT / "scripts/excalibur_blog_cover_text_overlay.py").exists())
        apply_src = (ROOT / "scripts/excalibur_blog_quad_apply.py").read_text(encoding="utf-8")
        self.assertNotIn("cover_text_overlay", apply_src)
        self.assertTrue((ROOT / "scripts/excalibur_blog_host_credit_overlay.py").is_file())


class HostCreditDecideTests(unittest.TestCase):
    def test_victoria_cover_applies(self) -> None:
        verdict = decide_host_credit(hero={"name_ru": "Виктория"}, slot_key="cover")
        self.assertTrue(verdict["apply"])
        self.assertEqual(verdict["text"], CANON_VICTORIA_CREDIT)

    def test_alena_cover_skipped(self) -> None:
        for name in ("Алёна", "Алена", "Alena"):
            verdict = decide_host_credit(hero={"name_ru": name}, slot_key="cover")
            self.assertFalse(verdict["apply"], name)
            self.assertEqual(verdict["reason"], "alena_excluded")

    def test_inline_without_face_skipped(self) -> None:
        verdict = decide_host_credit(hero={"name_ru": "Виктория"}, slot_key="inline_1")
        self.assertFalse(verdict["apply"])
        self.assertEqual(verdict["reason"], "inline_without_host_face")

    def test_default_cover_is_victoria(self) -> None:
        verdict = decide_host_credit(hero={"cover_mode": "host_reference"}, slot_key="cover")
        self.assertTrue(verdict["apply"])
        self.assertEqual(verdict["text"], CANON_VICTORIA_CREDIT)

    def test_illustrative_without_face_skipped(self) -> None:
        verdict = decide_host_credit(hero={"cover_mode": "illustrative"}, slot_key="cover")
        self.assertFalse(verdict["apply"])


class HostCreditStampTests(unittest.TestCase):
    def test_stamp_changes_bottom_left_pixels(self) -> None:
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cover.png"
            Image.new("RGB", (1200, 675), "#FFFFFF").save(path)
            before = path.read_bytes()
            result = stamp_credit_on_image(path, CANON_VICTORIA_CREDIT)
            self.assertTrue(result["applied"])
            self.assertEqual(result["text"], CANON_VICTORIA_CREDIT)
            self.assertTrue(result["no_banner"])
            after = path.read_bytes()
            self.assertNotEqual(before, after)
            from PIL import ImageStat

            img = Image.open(path).convert("L")
            # Credit sits bottom-left; that corner must no longer be pure white.
            mean = ImageStat.Stat(img.crop((20, 620, 520, 668))).mean[0]
            self.assertLess(mean, 250)

    def test_apply_skips_alena_file(self) -> None:
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "alena.png"
            Image.new("RGB", (1200, 675), "#EEEEEE").save(path)
            before = path.read_bytes()
            result = apply_host_credit(
                path,
                hero={"name_ru": "Алёна", "credit_overlay": {"text": CANON_VICTORIA_CREDIT}},
                design_code={},
                slot_key="cover",
            )
            self.assertFalse(result["applied"])
            self.assertEqual(path.read_bytes(), before)


class HostCreditSplitTests(unittest.TestCase):
    def test_split_stamps_victoria_cover_not_inline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp)
            cover_dir = article / "cover"
            cover_dir.mkdir()
            canvas = cover_dir / "canvas-quad.png"
            create_demo_canvas(canvas, "victoria-credit")
            manifest = default_manifest(article, "cover/canvas-quad.png")
            for key in ("cover", "inline_1", "inline_2", "inline_3"):
                manifest["slots"][key]["alt"] = f"alt {key}"
            info = split_canvas(
                canvas,
                cover_dir,
                manifest,
                (1200, 675),
                split_mode="mechanical",
                hero={"name_ru": "Виктория", "cover_mode": "host_reference"},
                design_code={},
                cover_mode="host_reference",
            )
            cover_credit = info["outputs"]["cover"]["host_credit_overlay"]
            self.assertTrue(cover_credit.get("applied"))
            self.assertEqual(cover_credit.get("text"), CANON_VICTORIA_CREDIT)
            inline_credit = info["outputs"]["inline_1"]["host_credit_overlay"]
            self.assertFalse(inline_credit.get("applied"))


class HostCreditNoSecretsTests(unittest.TestCase):
    def test_overlay_module_has_no_api_keys(self) -> None:
        src = (ROOT / "scripts/excalibur_blog_host_credit_overlay.py").read_text(encoding="utf-8")
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        self.assertNotIn("KIE_API_KEY", src)
        self.assertNotIn("sk-", src)
        self.assertNotIn("api_key", json.dumps(hero))


if __name__ == "__main__":
    unittest.main()
