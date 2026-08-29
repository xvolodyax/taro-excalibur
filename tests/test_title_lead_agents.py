"""Title agent + Writer final pipeline."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REMOVED = (
    "agents/excalibur-blog-lead.md",
    "agents/excalibur-blog-article-editor.md",
    "agents/excalibur-blog-geo-qa.md",
    "agents/excalibur-blog-hook.md",
    "skills/lead-excalibur-blog/SKILL.md",
    "skills/article-editor-excalibur-blog/SKILL.md",
    "skills/excalibur-geo-qa/SKILL.md",
    "skills/hook-excalibur-blog/SKILL.md",
)


class TitleWriterAgentsTest(unittest.TestCase):
    def test_title_agent_exists_and_forbids_seo_tails(self) -> None:
        a = (ROOT / "agents/excalibur-blog-title.md").read_text(encoding="utf-8")
        s = (ROOT / "skills/title-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("title-brief.json", a)
        self.assertIn("без копипаста", a + s)
        self.assertNotIn('"title_id"', a + s)
        self.assertNotIn('"hook_id"', a + s)

    def test_removed_agents_and_skills_gone(self) -> None:
        for rel in REMOVED:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_article_style_file_present(self) -> None:
        style = (ROOT / "shared/article-style.md").read_text(encoding="utf-8")
        low = style.lower()
        self.assertIn("англицизм", low)
        self.assertIn("канцелярит", low)
        self.assertIn("заголовок", low)
        self.assertIn("открытие", low)
        self.assertIn("SOUL.md", style)
        self.assertIn("Возьмём:", style)
        self.assertIn("seo-article__lead", style)

    def test_soul_md_present(self) -> None:
        soul = (ROOT / "shared/SOUL.md").read_text(encoding="utf-8")
        self.assertIn("Core Truths", soul)
        self.assertIn("Vibe", soul)
        self.assertIn("Возьмём:", soul)
        self.assertTrue((ROOT / "shared/soul-examples/good-outputs.md").is_file())
        self.assertTrue((ROOT / "shared/soul-examples/bad-outputs.md").is_file())

    def test_pipeline_canon_writer_sources(self) -> None:
        canon = json.loads((ROOT / "shared/pipeline-canon.json").read_text(encoding="utf-8"))
        sources = canon["writer_allowed_sources"]
        self.assertIn("title-brief.json", sources)
        self.assertIn("research-notes.md", sources)
        self.assertNotIn("shared/SOUL.md", sources)
        self.assertIn("shared/SOUL.md", canon["sol_allowed_sources"])
        self.assertNotIn("lead.md", sources)
        self.assertNotIn("removed_agents", canon)

    def test_director_order_title_before_writer(self) -> None:
        d = (ROOT / "skills/director-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        canon_line = next(
            (ln for ln in d.splitlines() if "Title → Writer" in ln),
            "",
        )
        self.assertIn("Title → Writer", canon_line)
        self.assertIn("Sol", d)
        self.assertLess(d.find("### 1–2 Research"), d.find("### 3 Writer"))
        self.assertLess(d.find("### 3 Writer"), d.find("### 3b Sol"))


if __name__ == "__main__":
    unittest.main()
