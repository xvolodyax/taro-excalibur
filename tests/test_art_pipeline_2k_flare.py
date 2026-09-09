"""Vladimir 2026-09-09 Art canon: ONE Flare 2K quad, never four 1K gens."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_art_canon import (  # noqa: E402
    HOST_AGE,
    KIE_IMAGE_MODEL,
    KIE_MODEL_PREFIX,
    MCP_RESOLUTION,
    require_2k_resolution,
    require_kie_model,
)
from excalibur_blog_cover_quad_prompt import (  # noqa: E402
    build_prompt,
    tenant_style_file,
)
from excalibur_blog_kie_gpt_image2_api import (  # noqa: E402
    DEFAULT_MODEL,
    KieApiError,
    batch_mcp_args,
    resolve_batch_model,
)
from excalibur_blog_quad_manifest import tenant_cover_style  # noqa: E402
from excalibur_blog_site_base import encode_expanded_media_url  # noqa: E402


class ArtCanonConstantsTest(unittest.TestCase):
    def test_model_is_flare_family(self) -> None:
        self.assertTrue(KIE_IMAGE_MODEL.startswith(KIE_MODEL_PREFIX))
        self.assertEqual(KIE_IMAGE_MODEL, "gpt-image-2-5-flare-image-to-image")
        self.assertEqual(DEFAULT_MODEL, KIE_IMAGE_MODEL)
        self.assertEqual(MCP_RESOLUTION, "2K")
        self.assertEqual(HOST_AGE, 33)

    def test_require_helpers(self) -> None:
        self.assertEqual(require_kie_model(KIE_IMAGE_MODEL), KIE_IMAGE_MODEL)
        self.assertEqual(require_2k_resolution("2K"), "2K")
        with self.assertRaises(ValueError):
            require_kie_model("gpt-image-2-image-to-image")
        with self.assertRaises(ValueError):
            require_2k_resolution("1K")


class KieBatchGuardTest(unittest.TestCase):
    def _write_batch(self, tmp: Path, **overrides: object) -> Path:
        job = {
            "api_args": {"model": KIE_IMAGE_MODEL},
            "mcp_args": {
                "prompt": "quad canvas",
                "input_urls": ["https://example.test/Виктория.png"],
                "aspect_ratio": "16:9",
                "resolution": "2K",
            },
        }
        batch = {
            "preferred_image_flow": {"model": KIE_IMAGE_MODEL},
            "jobs": [job],
        }
        batch.update(overrides)
        path = tmp / "quad-mcp-batch.json"
        path.write_text(json.dumps(batch), encoding="utf-8")
        return path

    def test_rejects_1k_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            path = self._write_batch(tmp)
            data = json.loads(path.read_text(encoding="utf-8"))
            data["jobs"][0]["mcp_args"]["resolution"] = "1K"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(KieApiError) as ctx:
                batch_mcp_args(path)
            self.assertIn("2K", str(ctx.exception))

    def test_rejects_legacy_model(self) -> None:
        with self.assertRaises(KieApiError):
            resolve_batch_model(
                {
                    "preferred_image_flow": {"model": "gpt-image-2-image-to-image"},
                    "jobs": [{"api_args": {"model": "gpt-image-2-image-to-image"}}],
                },
                "gpt-image-2-image-to-image",
            )

    def test_rejects_four_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            path = self._write_batch(
                tmp,
                jobs=[{"mcp_args": {"prompt": "a", "input_urls": ["https://x/a"]}}] * 4,
            )
            with self.assertRaises(KieApiError) as ctx:
                batch_mcp_args(path)
            self.assertIn("exactly one job", str(ctx.exception))


class PromptLockTest(unittest.TestCase):
    def _manifest(self) -> dict:
        return {
            "cover_hook": "Он написал еду и пропал",
            "cover_hook_highlight": "пропал",
            "slots": {
                "cover": {"scene_hint": "Host face LARGE left half", "sticky": "не пиши еду"},
                "inline_1": {
                    "visual_type": "infographic_card",
                    "h2_anchor": "Цифры",
                    "scene_hint": "fact card",
                    "labels": ["написал еду", "и пропал"],
                },
                "inline_2": {
                    "visual_type": "comparison_table_ui",
                    "h2_anchor": "Сравнение",
                    "scene_hint": "two columns",
                },
                "inline_3": {
                    "visual_type": "workflow_diagram",
                    "h2_anchor": "Схема",
                    "scene_hint": "arrows",
                },
            },
        }

    def test_cover_cell_and_inline_locks(self) -> None:
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        style = json.loads(
            (ROOT / "memory/cover/quad-style-victoria-studio.json").read_text(encoding="utf-8")
        )
        design = json.loads(
            (ROOT / "memory/cover/cover-design-code.json").read_text(encoding="utf-8")
        )
        prompt = build_prompt(self._manifest(), style, hero, {"types": {}}, design)
        self.assertIn("Victoria age 33", prompt)
        self.assertIn("B14 ON IMAGE", prompt)
        self.assertIn("COVER BRAND LINE ON IMAGE", prompt)
        self.assertIn("ТАРО СЕЙЧАС", prompt)
        self.assertIn("no red frame", prompt.lower())
        self.assertIn("Victoria face", prompt)
        self.assertIn("NO people/faces/host", prompt)
        self.assertIn("thin white gutters", prompt)
        self.assertIn("«Он написал еду и пропал»", prompt)
        self.assertNotIn("four separate 1K", prompt)

    def test_tenant_style_not_pink_cat(self) -> None:
        self.assertEqual(
            tenant_style_file(ROOT),
            "memory/cover/quad-style-victoria-studio.json",
        )
        style_file, preset = tenant_cover_style(ROOT, None)
        self.assertEqual(style_file, "memory/cover/quad-style-victoria-studio.json")
        self.assertEqual(preset, "victoria-studio")
        self.assertNotIn("pink-cat", style_file)


class SiteBaseEncodeTest(unittest.TestCase):
    def test_cyrillic_filename_is_quoted(self) -> None:
        url = "https://www.example.test/wp-content/uploads/excalibur/Виктория.png"
        encoded = encode_expanded_media_url(url)
        self.assertIn("%", encoded)
        self.assertNotIn("Виктория", encoded)
        self.assertTrue(encoded.startswith("https://www.example.test/"))


class TenantJsonCanonTest(unittest.TestCase):
    def test_hero_and_design_use_flare_2k(self) -> None:
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        design = json.loads(
            (ROOT / "memory/cover/cover-design-code.json").read_text(encoding="utf-8")
        )
        self.assertEqual(hero["visual_lock"]["age"], 33)
        self.assertEqual(hero["image_provider"]["model"], KIE_IMAGE_MODEL)
        self.assertEqual(hero["image_provider"]["resolution"], "2K")
        self.assertEqual(design["image_provider"]["model"], KIE_IMAGE_MODEL)
        self.assertEqual(design["brand_line"], "ТАРО СЕЙЧАС")

    def test_contracts_ban_four_1k(self) -> None:
        canvas = (ROOT / "shared/blog-cover-quad-canvas-contract.md").read_text(encoding="utf-8")
        kie = (ROOT / "shared/kie-gpt-image-api-contract.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills/cover-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        for blob in (canvas, kie, skill):
            self.assertIn("2026-09-09", blob)
            self.assertIn("gpt-image-2-5-flare", blob)
            self.assertIn("2K", blob)
        self.assertIn("четыре отдельные 1K", canvas)
        self.assertIn("не перерисовывать", canvas)


if __name__ == "__main__":
    unittest.main()
