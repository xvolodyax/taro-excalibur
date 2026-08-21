"""Kie GPT Image 2: local Victoria ref does not need PUBLIC_SITE_URL."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import excalibur_blog_kie_gpt_image2_api as kie  # noqa: E402


class PreferLocalReferenceExpandTests(unittest.TestCase):
    def test_expand_keeps_placeholder_when_prefer_local_and_no_public_site(self) -> None:
        urls = ["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"]
        with mock.patch.object(kie, "resolve_public_base_from_env", return_value=""):
            out = kie.expand_input_urls(urls, allow_unexpanded_site_base=True)
        self.assertEqual(out, urls)

    def test_expand_still_requires_public_site_without_prefer_local(self) -> None:
        urls = ["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"]
        with mock.patch.object(kie, "resolve_public_base_from_env", return_value=""):
            with self.assertRaises(kie.KieApiError) as ctx:
                kie.expand_input_urls(urls, allow_unexpanded_site_base=False)
        self.assertIn("PUBLIC_SITE_URL", str(ctx.exception))

    def test_batch_mcp_args_allows_placeholder_when_prefer_local(self) -> None:
        batch = {
            "prefer_local_reference": True,
            "local_reference": "memory/cover/assets/виктория.png",
            "jobs": [
                {
                    "mcp_args": {
                        "prompt": "test prompt",
                        "input_urls": [
                            "{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"
                        ],
                        "aspect_ratio": "16:9",
                        "resolution": "2K",
                    }
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "quad-mcp-batch.json"
            path.write_text(json.dumps(batch), encoding="utf-8")
            with mock.patch.object(kie, "resolve_public_base_from_env", return_value=""):
                args = kie.batch_mcp_args(path)
        self.assertEqual(args["resolution"], "2K")
        self.assertTrue(args["input_urls"][0].startswith("{{SITE_BASE}}"))

    def test_create_rejects_unexpanded_placeholder(self) -> None:
        with self.assertRaises(kie.KieApiError):
            kie.assert_input_urls_ready_for_create(
                ["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"]
            )


if __name__ == "__main__":
    unittest.main()
