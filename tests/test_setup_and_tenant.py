"""Excalibur-2-Cloud tenant «ТАРО СЕЙЧАС» after Setup."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SetupTenantTests(unittest.TestCase):
    def test_setup_status_complete(self) -> None:
        status = json.loads((ROOT / "memory/setup/status.json").read_text(encoding="utf-8"))
        self.assertTrue(status.get("complete"))
        for phase in ("cloud", "site", "author", "voice", "cta", "scout"):
            self.assertEqual(status["phases"][phase], "done", phase)
        self.assertEqual(status["phases"]["visual"], "need_refs")
        self.assertIn("рефы", status.get("notes", "").lower())

    def test_tenant_config_taro(self) -> None:
        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        self.assertTrue(tenant.get("setup_complete"))
        self.assertEqual(tenant.get("brand_name"), "ТАРО СЕЙЧАС")
        self.assertEqual(tenant.get("author_id"), "victoria")
        self.assertTrue(tenant.get("cta_required"))
        self.assertEqual(
            tenant.get("cta_links"),
            [
                "https://max.ru/id531102974575_bot",
                "https://vk.com/app54565776",
            ],
        )
        self.assertTrue(tenant.get("dzen_rf_pack"))
        self.assertEqual(tenant.get("cover_mode"), "host_reference")
        self.assertFalse(tenant.get("wordpress_publish"))
        self.assertEqual(tenant.get("wordstat_folder_id"), "b1g0a71ifv910gjalmhp")
        self.assertIn("https://dzen.ru/todaytaro_bot", tenant.get("scout_signal_urls") or [])

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

    def test_templates_filled_no_setup_required(self) -> None:
        for rel in (
            "shared/SOUL.md",
            "shared/article-style.md",
            "shared/soul-examples/good-outputs.md",
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

        article_dir = ROOT / "memory/blog/articles/_cta_gate_fixture"
        if article_dir.exists():
            shutil.rmtree(article_dir)
        article_dir.mkdir(parents=True, exist_ok=True)
        try:
            (article_dir / "article.html").write_text(
                "<p>Проверь <a href=\"https://max.ru/id531102974575_bot\">бот в Макс</a> "
                "или <a href=\"https://vk.com/app54565776\">аудиоразбор</a>.</p>\n",
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

    def test_authors_registry_ready(self) -> None:
        registry = json.loads((ROOT / "shared/authors-registry.json").read_text(encoding="utf-8"))
        self.assertEqual(registry.get("status"), "READY")
        ids = {a["id"] for a in registry.get("authors") or []}
        self.assertEqual(ids, {"victoria", "alena"})
        self.assertEqual(registry.get("support", {}).get("handle"), "@OnlineKsenia")

    def test_publish_flag_stays_off_in_example(self) -> None:
        text = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("EXCALIBUR_BLOG_ALLOW_PUBLISH=no", text)
        self.assertNotIn("EXCALIBUR_BLOG_ALLOW_PUBLISH=yes", text)

    def test_rf_cta_ok_matches_tenant(self) -> None:
        rf = json.loads((ROOT / "shared/rf-blocked-entities.json").read_text(encoding="utf-8"))
        tenant = json.loads((ROOT / "shared/tenant-config.json").read_text(encoding="utf-8"))
        self.assertEqual(rf.get("cta_ok"), tenant.get("cta_links"))


if __name__ == "__main__":
    unittest.main()
