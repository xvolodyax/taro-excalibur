"""Early-act insert after the first scene paragraph (canon 2026-08-25)."""
from __future__ import annotations

import re
import unittest

from scripts.excalibur_blog_early_act_gate import check_html

OK = """<p>Сцена: окно, листок, паузы в чате.</p>
<h2>Сразу к делу</h2>
<p>Ты крутишь одно лето. Число года покажет ритм. Дальше можно спросить карты.</p>
<p>Скопируй вопрос:</p>
<ul>
<li>Что моё личное число года делает с этими отношениями до конца лета?</li>
<li>В этом ритме мне ждать его шага или действовать самой?</li>
</ul>
<p>Открой <a href="https://vk.com/app54565776">аудиоразбор</a> в <a href="https://vk.com/app54565776">приложении во ВКонтакте</a>.</p>
<p>Карты на эти вопросы: <a href="https://max.ru/id531102974575_bot">бот в Макс</a>.</p>
<h2>Как посчитать</h2>
<p>Дальше длинный разбор.</p>
<h2>Когда цифра уже есть</h2>
<p>Цифра уже есть. Чтобы услышать, как она садится в твою историю, открой <a href="https://vk.com/app54565776">аудиоразбор</a> «Суть – Тень – Вектор» в <a href="https://vk.com/app54565776">приложении во ВКонтакте</a>.</p>
<p>Если нужны карты на этот ритм, открой <a href="https://max.ru/id531102974575_bot">бот в Макс</a>: три бесплатных расклада, триплет или кельтский крест.</p>
"""


class EarlyActGateTest(unittest.TestCase):
    def test_pass_on_canon_insert(self) -> None:
        self.assertEqual(check_html(OK), [])

    def test_rejects_missing_first_h2(self) -> None:
        html = OK.replace("<h2>Сразу к делу</h2>", "<h2>Как посчитать</h2>", 1)
        errors = check_html(html)
        self.assertTrue(any("first H2" in e or "early-act" in e for e in errors))

    def test_rejects_telegram(self) -> None:
        html = OK.replace("бот в Макс", "бот в Telegram t.me/TodayTaro_bot")
        errors = check_html(html)
        self.assertTrue(any("Telegram" in e for e in errors))

    def test_rejects_any_situation(self) -> None:
        html = OK.replace(
            "Что моё личное число года делает с этими отношениями до конца лета?",
            "Загадай любую ситуацию",
        )
        errors = check_html(html)
        self.assertTrue(any("ситуацию" in e for e in errors))

    def test_rejects_extra_p_before_insert(self) -> None:
        html = "<p>Сцена.</p><p>Ещё прогрев.</p>" + OK[OK.find("<h2>") :]
        errors = check_html(html)
        self.assertTrue(any("one short" in e or "early insert" in e for e in errors))

    def test_rejects_referral_closer(self) -> None:
        html = OK.replace(
            "Цифра уже есть. Чтобы услышать, как она садится в твою историю, открой",
            "Вопросы и ссылки - в начале, сразу после сцены. Чтобы услышать, открой",
        )
        errors = check_html(html)
        self.assertTrue(any("referral" in e or "в начале" in e for e in errors))

    def test_rejects_missing_end_doors(self) -> None:
        html = re.sub(
            r"<h2>Когда цифра уже есть</h2>.*",
            "<h2>Когда цифра уже есть</h2><p>Просто закрой вкладку.</p>",
            OK,
            flags=re.S,
        )
        errors = check_html(html)
        self.assertTrue(any("ending must" in e for e in errors))


class InlineH2SkipTests(unittest.TestCase):
    def test_manifest_skips_early_act_and_closer(self) -> None:
        from pathlib import Path
        from tempfile import TemporaryDirectory

        from scripts.excalibur_blog_quad_manifest import extract_h2_titles

        html = (
            "<p>Сцена.</p>"
            "<h2>Сразу к делу</h2>"
            "<h2>Почему время приглашения говорит больше самих слов</h2>"
            "<h2>Разовая спонтанность или привычка</h2>"
            "<h2>Как работает карта дня</h2>"
            "<h2>Как поступить сегодня вечером и получить точный ответ</h2>"
        )
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.html"
            path.write_text(html, encoding="utf-8")
            titles = extract_h2_titles(path)
        self.assertEqual(
            titles,
            [
                "Почему время приглашения говорит больше самих слов",
                "Разовая спонтанность или привычка",
                "Как работает карта дня",
            ],
        )


if __name__ == "__main__":
    unittest.main()
