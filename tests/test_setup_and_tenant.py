"""Excalibur-2-Cloud setup/tenant contracts after first-run Setup."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SetupTenantTests(unittest.TestCase):
    def test_setup_status_complete(self) -> None:
        status = json.loads((ROOT / "memory/setup/status.json").read_text(encoding="utf-8"))
        self.assertTrue(status.get("complete"))
        self.assertFalse(status.get("reopen"))
        for phase in ("cloud", "site", "author", "voice", "visual", "cta", "scout"):
            self.assertEqual(status.get("phases", {}).get(phase), "done", phase)

    def test_tenant_config_filled(self) -> None:
        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        self.assertTrue(tenant.get("setup_complete"))
        self.assertEqual(tenant.get("brand_name"), "ТАРО СЕЙЧАС")
        self.assertEqual(tenant.get("author_id"), "victoria")
        self.assertTrue(tenant.get("cta_required"))
        self.assertGreaterEqual(len(tenant.get("cta_links") or []), 3)
        self.assertTrue(tenant.get("dzen_rf_pack"))
        self.assertEqual(tenant.get("cover_mode"), "host_reference")
        self.assertTrue(tenant.get("allow_pipeline_publish"))
        self.assertTrue(tenant.get("dzen_rss"))
        hero = json.loads((ROOT / "memory/cover/blog-hero.json").read_text(encoding="utf-8"))
        self.assertEqual(hero.get("reference_image"), "memory/cover/assets/Виктория.png")
        face = ROOT / "memory/cover/assets/Виктория.png"
        inbox = ROOT / "cover-refs/Виктория.png"
        self.assertTrue(face.is_file())
        self.assertTrue(inbox.is_file())
        self.assertEqual(face.stat().st_size, 2_191_823)
        self.assertEqual(inbox.stat().st_size, 2_191_823)
        self.assertEqual(face.read_bytes(), inbox.read_bytes())
        self.assertFalse((ROOT / "memory/cover/assets/viktoriaref.png").exists())

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

    def test_templates_no_setup_required(self) -> None:
        for rel in (
            "shared/SOUL.md",
            "shared/article-style.md",
            "shared/soul-examples/good-outputs.md",
            "shared/soul-examples/SOURCE.md",
            "memory/brief/site-brief.md",
            "shared/authors-registry.json",
            "memory/cover/blog-hero.json",
            "memory/cover/cover-design-code.json",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("SETUP_REQUIRED", text, rel)

    def test_no_personal_lebedev_style_file(self) -> None:
        self.assertFalse((ROOT / "shared/lebedev-style.md").exists())
        self.assertTrue((ROOT / "shared/article-style.md").is_file())

    def test_cta_gate_requires_tenant_links(self) -> None:
        import shutil
        import subprocess

        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        links = [str(x) for x in (tenant.get("cta_links") or []) if str(x).strip()]
        self.assertTrue(links)

        article_dir = ROOT / "memory/blog/articles/_cta_gate_fixture"
        if article_dir.exists():
            shutil.rmtree(article_dir)
        article_dir.mkdir(parents=True, exist_ok=True)
        try:
            hrefs = " ".join(f'<a href="{url}">дверь</a>' for url in links)
            (article_dir / "article.html").write_text(
                f"<p>Сцена. {hrefs}</p>\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts/excalibur_blog_community_cta_gate.py"),
                    "--article-dir",
                    str(article_dir.relative_to(ROOT)),
                    "--root",
                    str(ROOT),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            report = json.loads((article_dir / "community-cta-gate.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")
        finally:
            shutil.rmtree(article_dir, ignore_errors=True)

    def test_cta_gate_fails_without_links(self) -> None:
        import shutil
        import subprocess

        article_dir = ROOT / "memory/blog/articles/_cta_gate_fixture_missing"
        if article_dir.exists():
            shutil.rmtree(article_dir)
        article_dir.mkdir(parents=True, exist_ok=True)
        try:
            (article_dir / "article.html").write_text("<p>No links here</p>\n", encoding="utf-8")
            proc = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts/excalibur_blog_community_cta_gate.py"),
                    "--article-dir",
                    str(article_dir.relative_to(ROOT)),
                    "--root",
                    str(ROOT),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        finally:
            shutil.rmtree(article_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
