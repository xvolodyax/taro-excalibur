"""Excalibur-2-Cloud setup/tenant skeleton contracts."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SetupTenantTests(unittest.TestCase):
    def test_setup_status_incomplete_by_default(self) -> None:
        status = json.loads((ROOT / "memory/setup/status.json").read_text(encoding="utf-8"))
        self.assertFalse(status.get("complete"))
        for phase in ("cloud", "site", "author", "voice", "visual", "cta", "scout"):
            self.assertIn(phase, status.get("phases", {}))

    def test_tenant_config_defaults(self) -> None:
        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        self.assertIn("setup_complete", tenant)
        self.assertIn("cta_required", tenant)
        self.assertIn("cta_links", tenant)
        self.assertTrue(tenant.get("dzen_rf_pack"))

    def test_setup_agents_present(self) -> None:
        for rel in (
            "agents/excalibur-blog-setup.md",
            "agents/excalibur-blog-setup-voice.md",
            "agents/excalibur-blog-setup-visual.md",
            "skills/setup-excalibur-blog/SKILL.md",
            "skills/setup-voice-excalibur-blog/SKILL.md",
            "skills/setup-visual-excalibur-blog/SKILL.md",
            ".cursor/agents/excalibur-blog-setup.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_templates_mark_setup_required(self) -> None:
        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        if not tenant.get("setup_complete") and not any((ROOT / "memory/setup/voice-inbox/notes.md").exists() for _ in (1,)):
            for rel in (
                "shared/SOUL.md",
                "shared/article-style.md",
                "shared/soul-examples/good-outputs.md",
                "memory/brief/site-brief.md",
            ):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("SETUP_REQUIRED", text, rel)

    def test_no_personal_lebedev_style_file(self) -> None:
        self.assertFalse((ROOT / "shared/lebedev-style.md").exists())
        self.assertTrue((ROOT / "shared/article-style.md").is_file())

    def test_cta_gate_optional_when_empty(self) -> None:
        import shutil
        import subprocess
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "shared").mkdir(parents=True)
            (tmp_root / "shared/tenant-config.json").write_text(
                json.dumps({"cta_required": False, "cta_links": []}),
                encoding="utf-8",
            )
            article_dir = tmp_root / "memory/blog/articles/_cta_gate_fixture"
            article_dir.mkdir(parents=True, exist_ok=True)
            (article_dir / "article.html").write_text("<p>No links here</p>\n", encoding="utf-8")
            proc = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts/excalibur_blog_community_cta_gate.py"),
                    "--article-dir",
                    str(article_dir.relative_to(tmp_root)),
                    "--root",
                    str(tmp_root),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            report = json.loads((article_dir / "community-cta-gate.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
