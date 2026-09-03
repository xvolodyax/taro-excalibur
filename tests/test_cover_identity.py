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

    def _write_kie_batch(
        self, tmp: str, *, prefer_local: bool, local_reference: str
    ) -> Path:
        batch_path = Path(tmp) / "quad-mcp-batch.json"
        batch_path.write_text(
            json.dumps(
                {
                    "prefer_local_reference": prefer_local,
                    "local_reference": local_reference,
                    "jobs": [
                        {
                            "mcp_args": {
                                "prompt": "test",
                                "input_urls": [
                                    "{{SITE_BASE}}/wp-content/uploads/excalibur/Виктория.png"
                                ],
                                "aspect_ratio": "16:9",
                                "resolution": "2K",
                            }
                        }
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return batch_path

    def test_kie_prefer_local_skips_site_base_expand(self) -> None:
        import os
        import sys
        import tempfile

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_kie_gpt_image2_api import batch_mcp_args

        for key in ("PUBLIC_SITE_URL", "WP_SITE_URL", "WP_HOME"):
            os.environ.pop(key, None)
        with tempfile.TemporaryDirectory() as tmp:
            batch_path = self._write_kie_batch(
                tmp,
                prefer_local=True,
                local_reference="memory/cover/assets/Виктория.png",
            )
            args = batch_mcp_args(batch_path)
            self.assertEqual(
                args["input_urls"],
                ["{{SITE_BASE}}/wp-content/uploads/excalibur/Виктория.png"],
            )

    def test_kie_without_prefer_local_requires_site_base(self) -> None:
        import os
        import sys
        import tempfile

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_kie_gpt_image2_api import KieApiError, batch_mcp_args

        for key in ("PUBLIC_SITE_URL", "WP_SITE_URL", "WP_HOME"):
            os.environ.pop(key, None)
        with tempfile.TemporaryDirectory() as tmp:
            batch_path = self._write_kie_batch(
                tmp, prefer_local=False, local_reference=""
            )
            with self.assertRaises(KieApiError) as ctx:
                batch_mcp_args(batch_path)
            self.assertIn("{{SITE_BASE}}", str(ctx.exception))
            self.assertIn("unset", str(ctx.exception))

    def test_kie_playground_blank_is_retryable_infra_not_sensitive(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from excalibur_blog_kie_gpt_image2_api import (
            classify_record_info,
            is_playground_blank_fail,
            is_retryable_server_fail,
            is_sensitive_content_fail,
            retry_kind_for_server_fail,
            KieRetryableFail,
        )

        msg = "generate playground failed, task id is blank"
        self.assertTrue(is_playground_blank_fail(422, msg))
        self.assertTrue(is_retryable_server_fail(422, msg))
        self.assertFalse(is_sensitive_content_fail(422, msg))
        self.assertEqual(retry_kind_for_server_fail(422, msg), "playground_blank")

        sensitive = "The input or output was flagged as sensitive"
        self.assertFalse(is_playground_blank_fail(422, sensitive))
        self.assertFalse(is_retryable_server_fail(422, sensitive))
        self.assertTrue(is_sensitive_content_fail(422, sensitive))
        self.assertEqual(retry_kind_for_server_fail(422, sensitive), "server_500")

        self.assertTrue(is_retryable_server_fail(500, "try again later"))
        with self.assertRaises(KieRetryableFail):
            classify_record_info(
                {"state": "fail", "failCode": 422, "failMsg": msg},
                "task-blank",
            )


if __name__ == "__main__":
    unittest.main()
