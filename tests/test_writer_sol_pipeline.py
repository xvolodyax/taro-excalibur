"""Guard Writer → Sol human-first contracts."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WriterSolContractsTest(unittest.TestCase):
    def test_pipeline_canon_writer_then_sol(self) -> None:
        canon = json.loads((ROOT / "shared/pipeline-canon.json").read_text(encoding="utf-8"))
        self.assertFalse(canon["writer_is_final"])
        self.assertTrue(canon["sol_is_final"])
        self.assertEqual(canon["sol_agent"], "excalibur-blog-sol")
        self.assertEqual(canon["writer_output"], "drafts/writer.html")
        self.assertEqual(canon["sol_output"], "article.html")
        self.assertIn("shared/SOUL.md", canon["sol_allowed_sources"])
        self.assertIn("drafts/writer.html", canon["sol_allowed_sources"])
        self.assertNotIn("shared/SOUL.md", canon["writer_allowed_sources"])
        self.assertTrue(canon["opening_rules"].get("sol_owns_opening"))
        self.assertTrue(canon["opening_rules"].get("no_vozmem_label"))
        self.assertTrue(canon["opening_rules"].get("lead_once_in_body"))
        self.assertTrue(canon["opening_rules"].get("on_page_excerpt_empty"))

    def test_sol_agent_and_skill_exist(self) -> None:
        self.assertTrue((ROOT / "agents/excalibur-blog-sol.md").is_file())
        self.assertTrue((ROOT / ".cursor/agents/excalibur-blog-sol.md").is_file())
        self.assertTrue((ROOT / "skills/sol-excalibur-blog/SKILL.md").is_file())
        skill = (ROOT / "skills/sol-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("drafts/writer.html", skill)
        self.assertIn("good-outputs.md", skill)
        self.assertIn("SOUL.md", skill)

    def test_writer_outputs_meaning_draft(self) -> None:
        skill = (ROOT / "skills/writer-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("drafts/writer.html", skill)
        self.assertIn("Sol", skill)
        self.assertNotIn("финальный article.html целиком", skill.lower())

    def test_director_orders_sol_before_stamp(self) -> None:
        d = (ROOT / "skills/director-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("excalibur-blog-sol", d)
        self.assertLess(d.find("### 3 Writer"), d.find("### 3b Sol"))
        self.assertLess(d.find("### 3b Sol"), d.find("### 4 Stamp"))

    def test_soul_owned_by_sol(self) -> None:
        soul = (ROOT / "shared/SOUL.md").read_text(encoding="utf-8")
        self.assertIn("excalibur-blog-sol", soul)
        self.assertIn("drafts/writer.html", soul)


if __name__ == "__main__":
    unittest.main()
