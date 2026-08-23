"""prefer_local_reference must not require PUBLIC_SITE_URL to parse a git-safe batch."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_kie_gpt_image2_api import (  # noqa: E402
    KieApiError,
    batch_mcp_args,
    expand_input_urls,
)


class PreferLocalSiteBaseTests(unittest.TestCase):
    def test_expand_raises_without_live_host(self) -> None:
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PUBLIC_SITE_URL", None)
            os.environ.pop("WP_HOME", None)
            os.environ.pop("WP_SITE_URL", None)
            with self.assertRaises(KieApiError):
                expand_input_urls(["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"])

    def test_expand_keeps_placeholder_when_allow_unexpanded(self) -> None:
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PUBLIC_SITE_URL", None)
            os.environ.pop("WP_HOME", None)
            os.environ.pop("WP_SITE_URL", None)
            urls = expand_input_urls(
                ["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"],
                allow_unexpanded=True,
            )
        self.assertEqual(
            urls, ["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"]
        )

    def test_batch_mcp_args_prefer_local_without_site_url(self) -> None:
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
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("PUBLIC_SITE_URL", None)
                os.environ.pop("WP_HOME", None)
                os.environ.pop("WP_SITE_URL", None)
                args = batch_mcp_args(path)
        self.assertEqual(
            args["input_urls"],
            ["{{SITE_BASE}}/wp-content/uploads/excalibur/виктория.png"],
        )
        self.assertEqual(args["resolution"], "2K")


if __name__ == "__main__":
    unittest.main()
