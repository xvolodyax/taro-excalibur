"""Guard Title subject and multi-Wordstat rules."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TitleSubjectWordstatTest(unittest.TestCase):
    def test_title_skill_requires_subject_in_h1(self) -> None:
        s = (ROOT / "skills/title-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        low = s.lower()
        self.assertIn("тема", low)
        self.assertIn("label head", low)
        self.assertIn("openai", low)

    def test_title_agent_bans_hiding_subject(self) -> None:
        a = (ROOT / "agents/excalibur-blog-title.md").read_text(encoding="utf-8")
        self.assertIn("Тема/имя в заголовке", a)
        self.assertIn("OpenAI", a)

    def test_scout_uses_multiple_wordstat_calls(self) -> None:
        s = (ROOT / "skills/scout-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        low = s.lower()
        self.assertIn("несколько вызовов", low)
        self.assertIn("2–4", low)
        self.assertNotIn("solo `callmcptool`, 1 вызов", low)

    def test_research_uses_multiple_wordstat_calls(self) -> None:
        r = (ROOT / "skills/excalibur-research/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("несколько вызовов", r.lower())

    def test_writer_owns_h1_subject_not_hidden(self) -> None:
        w = (ROOT / "agents/excalibur-blog-writer.md").read_text(encoding="utf-8")
        t = (ROOT / "skills/title-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        blob = (w + t).lower()
        self.assertTrue("тема" in blob or "h1" in blob)

    def test_title_agent_requires_gemini_and_bans_default_text(self) -> None:
        a = (ROOT / "agents/excalibur-blog-title.md").read_text(encoding="utf-8")
        self.assertIn("gemini-3.8-flash", a)
        self.assertIn("reasoning_effort", a)
        self.assertIn("В эфир с default/inherit Cloud Agent не уходит НИКАКОЙ текст", a)
        self.assertIn("Нет Gemini = FAIL", a)


if __name__ == "__main__":
    unittest.main()
