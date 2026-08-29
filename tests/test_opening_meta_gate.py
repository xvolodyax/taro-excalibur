"""Opening/meta gate: research-brief and API-calque bans."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.excalibur_blog_opening_meta_gate import check_article

ROOT = Path(__file__).resolve().parents[1]


class OpeningMetaGateTest(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue((ROOT / "scripts/excalibur_blog_opening_meta_gate.py").is_file())
        self.assertFalse((ROOT / "scripts/excalibur_blog_lead_meta_gate.py").exists())
        self.assertFalse((ROOT / "scripts/excalibur_blog_writer_finalize.py").exists())
        stamp = (ROOT / "scripts/excalibur_blog_pipeline_canon.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("stamp_article", stamp)

    def test_blocks_research_brief_description(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "article.html").write_text(
                "<p>Боль читателя. Потом продукт.</p>\n", encoding="utf-8"
            )
            (d / "article.meta.json").write_text(
                json.dumps(
                    {
                        "description": (
                            "5 августа 2026 Hark выпустил Handoff без готового стыка. "
                            "VentureBeat просит сверять поколение моделей."
                        )
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            report = check_article(d)
            self.assertEqual(report["status"], "BLOCK")
            joined = " ".join(report["errors"])
            self.assertTrue("research-brief" in joined or "api-calque-styk" in joined)

    def test_blocks_instruction_opening(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "article.html").write_text(
                "<p>Смотрите на факты запуска и оговорки прессы — не путайте с готовым доступом сегодня.</p>\n",
                encoding="utf-8",
            )
            (d / "article.meta.json").write_text(
                json.dumps({"description": "Чат отвечает, кнопки жмёшь сам."}, ensure_ascii=False),
                encoding="utf-8",
            )
            report = check_article(d)
            self.assertEqual(report["status"], "BLOCK")

    def test_blocks_vozmem_opener(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "article.html").write_text(
                "<p>Возьмём: экран смартфона загорается ближе к полуночи.</p>\n",
                encoding="utf-8",
            )
            (d / "article.meta.json").write_text(
                json.dumps({"description": "Как не путать импульс с возвратом."}, ensure_ascii=False),
                encoding="utf-8",
            )
            report = check_article(d)
            self.assertEqual(report["status"], "BLOCK", report)
            self.assertTrue(any("vozmem" in e for e in report["errors"]), report)

    def test_blocks_excerpt_clone_of_first_paragraph(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            first = (
                "Экран смартфона загорается ближе к полуночи: короткое «Привет, как ты?» "
                "или дежурное «Спишь?»."
            )
            (d / "article.html").write_text(f"<h1>Тема</h1>\n<p>{first}</p>\n<p>Дальше мысль.</p>\n", encoding="utf-8")
            (d / "article.meta.json").write_text(
                json.dumps(
                    {
                        "description": "Как не путать ночной пинг с желанием всё вернуть.",
                        "excerpt": first,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            report = check_article(d)
            self.assertEqual(report["status"], "BLOCK", report)
            self.assertTrue(any("excerpt" in e and "clone" in e for e in report["errors"]), report)

    def test_pass_without_orphan_lead_md(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "article.html").write_text(
                "<p>Чат отвечает текстом, а кнопки на сайте жмёшь сам. "
                "Hark выпустил Handoff — агент кликает сам. Пока очередь.</p>\n",
                encoding="utf-8",
            )
            (d / "article.meta.json").write_text(
                json.dumps(
                    {
                        "description": (
                            "Чат отвечает текстом, а кнопки на сайте жмёшь сам. "
                            "Hark Handoff кликает по страницам. Пока очередь."
                        )
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            report = check_article(d)
            self.assertEqual(report["status"], "PASS", report)

    def test_b135_passes_after_fix(self) -> None:
        art = ROOT / "memory/blog/articles/B135-hark-pustil-agenta-klikat-po-sajtam"
        if not art.is_dir():
            self.skipTest("B135 missing")
        report = check_article(art)
        self.assertEqual(report["status"], "PASS", report)


if __name__ == "__main__":
    unittest.main()
