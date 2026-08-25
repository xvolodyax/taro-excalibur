"""CTA funnel: bots = spreads, apps = Суть–Тень–Вектор audio."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_community_cta_gate import check_funnel, check_html, load_tenant


class CtaFunnelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tenant = load_tenant(ROOT)

    def test_canon_file_and_tenant_split(self) -> None:
        text = (ROOT / "shared/cta-funnel.md").read_text(encoding="utf-8")
        self.assertIn("триплет", text)
        self.assertIn("кельтский крест", text)
        self.assertIn("Суть – Тень – Вектор", text)
        self.assertIn("иди в бот", text)
        self.assertIn("Telegram", text)
        funnel = self.tenant["cta_funnel"]
        self.assertNotIn("аудиоразбор", " ".join(funnel["bots"]["spreads"]))
        self.assertIn("аудиоразбор", " ".join(funnel["bots"]["not"]))

    def test_split_paragraphs_pass(self) -> None:
        html = (
            "<p>Открой <a href=\"https://max.ru/id531102974575_bot\">бот в Макс</a>. "
            "Там три бесплатных расклада на три любых вопроса: голосом или текстом. "
            "Можно взять триплет из трёх карт или кельтский крест из десяти.</p>"
            "<p>Для <a href=\"https://vk.com/app54565776\">аудиоразбора</a> "
            "«Суть – Тень – Вектор» открой "
            "<a href=\"https://vk.com/app54565776\">приложение во ВКонтакте</a>. "
            "Там карта практического совета и уточняющие вопросы.</p>"
        )
        errors, present = check_html(html, self.tenant["cta_links"], required=True)
        self.assertEqual(errors, [])
        self.assertTrue(all(present.values()))
        self.assertEqual(check_funnel(html, self.tenant), [])

    def test_stv_on_bot_fails(self) -> None:
        html = (
            "<p>Для «Суть – Тень – Вектор» открой "
            "<a href=\"https://max.ru/id531102974575_bot\">бот в Макс</a> "
            "и послушай аудиоразбор.</p>"
            "<p>Или <a href=\"https://vk.com/app54565776\">приложение во ВКонтакте</a>.</p>"
        )
        errors = check_funnel(html, self.tenant)
        self.assertTrue(any("бот" in e.lower() or "Вектор" in e or "аудиоразбор" in e for e in errors), errors)

    def test_want_stv_go_to_bot_fails(self) -> None:
        html = "<p>Хочешь «Суть – Тень – Вектор» - иди в бот.</p>"
        errors = check_funnel(html, self.tenant)
        self.assertTrue(any("bot" in e.lower() or "бот" in e.lower() for e in errors), errors)

    def test_telegram_mention_fails(self) -> None:
        html = (
            "<p>Открой <a href=\"https://max.ru/id531102974575_bot\">бот в Макс</a>. "
            "Триплет или кельтский крест, три бесплатных, голосом.</p>"
            "<p><a href=\"https://vk.com/app54565776\">аудиоразбор</a> "
            "«Суть – Тень – Вектор», практического совета, уточняющие. "
            "Есть ещё бот в Telegram.</p>"
        )
        errors = check_funnel(html, self.tenant)
        self.assertTrue(any("Telegram" in e for e in errors), errors)

    def test_max_app_startapp_is_not_bot_href(self) -> None:
        html = (
            "<p>Открой <a href=\"https://max.ru/id531102974575_bot\">бот в Макс</a>. "
            "Там три бесплатных расклада на три любых вопроса: голосом или текстом. "
            "Можно взять триплет из трёх карт или кельтский крест из десяти.</p>"
            "<p>Для <a href=\"https://vk.com/app54565776\">аудиоразбора</a> "
            "«Суть – Тень – Вектор» открой "
            "<a href=\"https://vk.com/app54565776\">приложение во ВКонтакте</a> "
            "или <a href=\"https://max.ru/id531102974575_bot?startapp=ref_9BAD4149\">"
            "приложение Макс</a>. Там карта практического совета и уточняющие вопросы.</p>"
        )
        self.assertEqual(check_funnel(html, self.tenant), [])

    def test_article_package_matches_canon(self) -> None:
        candidates = [
            ROOT / "memory/blog/articles/B05-chto-on-skryvaet-v-otnosheniyah-i-skazhet-li-pravdu/article.html",
            ROOT / "memory/blog/articles/B02-chto-on-chuvstvuet/article.html",
        ]
        html_path = next((p for p in candidates if p.is_file()), None)
        if html_path is None:
            self.skipTest("no tenant article.html in this checkout")
        html = html_path.read_text(encoding="utf-8")
        errors, present = check_html(html, self.tenant["cta_links"], required=True)
        self.assertEqual(errors, [])
        self.assertTrue(all(present.values()))
        self.assertEqual(check_funnel(html, self.tenant), [])
        self.assertNotIn("Для детального анализа ситуации по структуре", html)


if __name__ == "__main__":
    unittest.main()
