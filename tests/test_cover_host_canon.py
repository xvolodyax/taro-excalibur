"""Cover-host canon must stay in SOUL / living files; still-life hints fail write-batch."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_cover_host_gate import (  # noqa: E402
    CANON_CREDIT,
    checklist_errors,
    living_canon_errors,
    validate,
)
from excalibur_blog_cover_quad_prompt import (  # noqa: E402
    cover_scene_host_errors,
    local_reference_candidates,
)
from excalibur_blog_host_credit_overlay import CANON_VICTORIA_CREDIT  # noqa: E402


class LivingCanonTests(unittest.TestCase):
    def test_living_files_hold_host_canon(self) -> None:
        errors = living_canon_errors(ROOT)
        self.assertEqual(errors, [])

    def test_credit_string_is_exact(self) -> None:
        self.assertEqual(CANON_CREDIT, CANON_VICTORIA_CREDIT)
        self.assertEqual(CANON_CREDIT, "Виктория - таролог команды «ТАРО СЕЙЧАС»")

    def test_validate_without_article_passes_on_repo(self) -> None:
        verdict = validate(ROOT)
        self.assertEqual(verdict["status"], "PASS", verdict)


class ChecklistTests(unittest.TestCase):
    def test_pass_checklist(self) -> None:
        data = {
            "compared_side_by_side": True,
            "victoria_face_visible": True,
            "still_life_only": False,
            "hair_match": True,
            "eyes_match": True,
            "bone_match": True,
            "no_face_seam": True,
            "not_brunette": True,
            "not_alena": True,
            "eyes_not_brown": True,
            "credit_applied": True,
            "ref_path": "memory/cover/assets/виктория.png",
        }
        self.assertEqual(checklist_errors(data), [])

    def test_still_life_cover_blocks(self) -> None:
        data = {
            "compared_side_by_side": True,
            "victoria_face_visible": False,
            "still_life_only": True,
            "hair_match": False,
            "eyes_match": False,
            "bone_match": False,
            "no_face_seam": True,
            "not_brunette": True,
            "not_alena": True,
            "eyes_not_brown": False,
            "credit_applied": True,
            "ref_path": "memory/cover/assets/виктория.png",
        }
        errors = checklist_errors(data)
        self.assertTrue(any("victoria_face_visible" in e for e in errors))
        self.assertTrue(any("still_life_only" in e for e in errors))
        self.assertTrue(any("eyes_not_brown" in e for e in errors))

    def test_article_dir_requires_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article = Path(tmp)
            (article / "cover").mkdir()
            verdict = validate(ROOT, article_dir=article, require_checklist=True)
            self.assertEqual(verdict["status"], "BLOCK")


class SceneHintLockTests(unittest.TestCase):
    def test_face_wearing_passes(self) -> None:
        self.assertEqual(
            cover_scene_host_errors(
                "Victoria FACE visible LARGE left wearing dusty-blue shirt; "
                "GREEN iris NEVER brown eyes; tiny phone right"
            ),
            [],
        )

    def test_still_life_fails(self) -> None:
        errors = cover_scene_host_errors(
            "still-life: dusty-olive blouse + tiny muted phone on a table"
        )
        self.assertTrue(errors)

    def test_garment_without_wearing_fails(self) -> None:
        errors = cover_scene_host_errors("Victoria LARGE left; dusty-olive blouse; tiny phone")
        self.assertTrue(any("wearing" in e for e in errors))

    def test_no_face_on_cover_fails(self) -> None:
        errors = cover_scene_host_errors("flat lay phone and eucalyptus; no people")
        self.assertTrue(errors)

    def test_light_brown_pupil_phrase_fails(self) -> None:
        errors = cover_scene_host_errors(
            "Victoria FACE visible LARGE left wearing dusty-blue shirt; "
            "GREEN eyes with slight light-brown near the pupil"
        )
        self.assertTrue(any("brown" in e.lower() for e in errors))

    def test_cat_hero_skips_lock(self) -> None:
        self.assertEqual(
            cover_scene_host_errors("situational cat on a sofa", host_required=False),
            [],
        )


class ReferenceAliasTests(unittest.TestCase):
    def test_victoria_alias_is_offered(self) -> None:
        paths = local_reference_candidates(
            {"reference_image": "memory/cover/assets/виктория.png", "input_urls": []},
            {"local_reference": "memory/cover/assets/виктория.png"},
        )
        self.assertIn("memory/cover/assets/виктория.png", paths)
        self.assertIn("memory/cover/assets/victoria.png", paths)

    def test_blog_hero_json_names_alias(self) -> None:
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        self.assertEqual(hero["reference_alias"], "memory/cover/assets/victoria.png")
        self.assertEqual(hero["hall_redraw"], "forbidden")
        self.assertEqual(hero["identity_fail_is"], "hard_reject_rebuild_whole_canvas")


if __name__ == "__main__":
    unittest.main()
