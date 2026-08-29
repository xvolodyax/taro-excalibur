#!/usr/bin/env python3
"""Site-API publish after GATE PASS (swarm, not Hall)."""
from __future__ import annotations

import json
import sys
import tarfile
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from excalibur_blog_opening_editorial import (  # noqa: E402
    first_body_paragraph,
    live_double_lead_errors,
    sanitize_site_meta,
)
from excalibur_blog_site_publish import (  # noqa: E402
    DEFAULT_SITE_BASE,
    PROTECTED_LIVE_TOPIC_IDS,
    TOKEN_ENV_NAMES,
    HttpResponse,
    build_tgz_bytes,
    collect_telegram_hrefs,
    live_second_cover_errors,
    main,
    prepare_site_html,
    publish_env_report,
    redact_secrets,
    resolve_publish_token,
    rewrite_rasklad_back_to_telegram,
    run_publish,
    strip_cover_hero,
    telegram_rewritten_to_rasklad,
    tgz_member_names,
)

MIN_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
    b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)

DESCRIPTION = (
    "Короткий тизер карточки не про заголовок и не про первый абзац — "
    "зачем читать материал сегодня вечером."
)


def _article_html(*, cover_hero: bool = True, telegram: bool = True) -> str:
    tg = (
        '<p>Ответ можно снять в <a href="https://t.me/example_bot?start=ref1">боте</a>.</p>\n'
        if telegram
        else "<p>Ответ можно снять без мессенджера.</p>\n"
    )
    hero = (
        '<figure class="cover-hero">\n'
        '  <img src="cover/cover.png" alt="Обложка про паузу в переписке">\n'
        "</figure>\n"
        if cover_hero
        else ""
    )
    paras = "".join(
        f"<p>Абзац смысла номер {i} про паузу, не про термин-дамп и не про SEO.</p>\n"
        for i in range(1, 8)
    )
    return (
        "<h1>Он прочитал и молчит</h1>\n"
        "<p>Многие ждут ответа сразу. Здесь другая картина вечера.</p>\n"
        f"{hero}"
        f"{tg}"
        f"{paras}"
        '<h2>Что происходит</h2>\n'
        '<figure class="inline-quad" data-slot="inline_1">\n'
        '  <img src="cover/inline-01.png" alt="Схема паузы">\n'
        "</figure>\n"
        "<p>Ещё абзац после первой врезки, чтобы тело было длиннее двухсот знаков.</p>\n"
        '<h2>Что не делать</h2>\n'
        '<figure class="inline-quad" data-slot="inline_2">\n'
        '  <img src="cover/inline-02.png" alt="Чеклист">\n'
        "</figure>\n"
        "<p>Второй блок смысла держит тему и не повторяет обложку в теле.</p>\n"
        '<h2>Какой вопрос к картам</h2>\n'
        '<figure class="inline-quad" data-slot="inline_3">\n'
        '  <img src="cover/inline-03.png" alt="Вопросы к картам">\n'
        "</figure>\n"
        "<p>Финал без второй обложки и без переписывания ссылок на расклад.</p>\n"
    )


def _write_article(tmp: Path, *, topic_id: str = "B99", cover_hero: bool = True) -> Path:
    article_dir = tmp / f"{topic_id}-on-prochital-i-molchit"
    cover = article_dir / "cover"
    cover.mkdir(parents=True)
    html = _article_html(cover_hero=cover_hero)
    (article_dir / "article.html").write_text(html, encoding="utf-8")
    (article_dir / "article.meta.json").write_text(
        json.dumps(
            {
                "topic_id": topic_id,
                "slug": "on-prochital-i-molchit",
                "title": "Он прочитал и молчит",
                "h1": "Он прочитал и молчит",
                "description": DESCRIPTION,
                "pipeline_canon": "human-first-v2",
                "editorial_swarm": False,
                "theme_blocks": {"faq": "skip", "quiz": "skip", "side_stickers": "skip"},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (article_dir / "description-brief.json").write_text(
        json.dumps(
            {
                "topic_id": topic_id,
                "title": "Он прочитал и молчит",
                "description": DESCRIPTION,
                "char_count": len(DESCRIPTION),
                "verdict": "PASS",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    for name in ("cover.png", "inline-01.png", "inline-02.png", "inline-03.png"):
        (cover / name).write_bytes(MIN_PNG)
    return article_dir


def _live_html(*, second_cover: bool = False, rewrite_tg: bool = False) -> str:
    tg_href = (
        "/rasklad-taro-online/"
        if rewrite_tg
        else "https://t.me/example_bot?start=ref1"
    )
    extra = ""
    if second_cover:
        extra = (
            '<figure class="seo-article__figure">'
            '<img src="/assets/blog/on-prochital-i-molchit/cover.png" alt="dup">'
            "</figure>"
        )
    return (
        "<html><body><article>"
        '<figure class="seo-article__cover">'
        '<img src="/assets/blog/on-prochital-i-molchit/cover.png" alt="hero">'
        "</figure>"
        f'<p>Снять ответ в <a href="{tg_href}">боте</a>.</p>'
        f"{extra}"
        '<figure class="seo-article__figure">'
        '<img src="/assets/blog/on-prochital-i-molchit/inline-01.png" alt="a">'
        "</figure>"
        '<figure class="seo-article__figure">'
        '<img src="/assets/blog/on-prochital-i-molchit/inline-02.png" alt="b">'
        "</figure>"
        '<figure class="seo-article__figure">'
        '<img src="/assets/blog/on-prochital-i-molchit/inline-03.png" alt="c">'
        "</figure>"
        "</article></body></html>"
    )


class FakeHttp:
    def __init__(
        self,
        *,
        live_html: str | None = None,
        live_after_restore: str | None = None,
        upload_id: str = "art-99",
    ) -> None:
        self.calls: list[tuple[str, str]] = []
        self.live_html = live_html or _live_html()
        self.live_after_restore = live_after_restore
        self.upload_id = upload_id
        self.seen_headers: list[dict[str, str]] = []
        self.telegram_patched = False

    def __call__(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        data: bytes | None = None,
        timeout: float = 30,
    ) -> HttpResponse:
        self.calls.append((method.upper(), url))
        self.seen_headers.append(dict(headers or {}))
        path = url.split("://", 1)[-1]
        if path.endswith("/api/admin/content/excalibur/upload"):
            return HttpResponse(201, {}, json.dumps({"id": self.upload_id, "url": "/blog/on-prochital-i-molchit/"}).encode(), url)
        if "/approve" in path or path.endswith("/publish"):
            return HttpResponse(200, {}, b'{"ok":true}', url)
        if method.upper() == "PATCH" and "/articles/" in path:
            if data and b"preserve_telegram" in data:
                self.telegram_patched = True
            return HttpResponse(200, {}, b'{"ok":true}', url)
        if method.upper() == "GET" and "/blog/" in path:
            html = self.live_html
            if self.live_after_restore is not None and getattr(self, "telegram_patched", False):
                html = self.live_after_restore
            return HttpResponse(200, {"content-type": "text/html"}, html.encode("utf-8"), url)
        return HttpResponse(404, {}, b'{"error":"no"}', url)


class SitePublishUnitTest(unittest.TestCase):
    def test_token_order(self) -> None:
        self.assertEqual(
            TOKEN_ENV_NAMES,
            (
                "SITE_PUBLISH_TOKEN",
                "HALL_PUBLISH_TOKEN",
                "PUBLISH_TOKEN",
                "TARO_SITE_TOKEN",
            ),
        )
        name, value = resolve_publish_token(
            {
                "HALL_PUBLISH_TOKEN": "hall-secret",
                "TARO_SITE_TOKEN": "taro-secret",
            }
        )
        self.assertEqual(name, "HALL_PUBLISH_TOKEN")
        self.assertEqual(value, "hall-secret")
        name, value = resolve_publish_token({})
        self.assertEqual(name, "")
        self.assertEqual(value, "")

    def test_redact_never_leaks_token(self) -> None:
        raw = "Authorization: Bearer super-secret-token-value"
        out = redact_secrets(raw, "super-secret-token-value")
        self.assertNotIn("super-secret-token-value", out)
        self.assertIn("<redacted>", out)

    def test_strip_cover_hero(self) -> None:
        html = _article_html(cover_hero=True)
        self.assertIn("cover-hero", html)
        cleaned, n = strip_cover_hero(html)
        self.assertGreaterEqual(n, 1)
        self.assertNotIn("cover-hero", cleaned)
        self.assertIn('data-slot="inline_1"', cleaned)
        site, info = prepare_site_html(html)
        self.assertGreaterEqual(info["cover_hero_removed"], 1)
        self.assertNotIn("cover-hero", site)
        self.assertNotIn('src="cover/cover.png"', site)

    def test_tgz_members_and_no_hero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article_dir = _write_article(Path(tmp), cover_hero=True)
            raw = (article_dir / "article.html").read_text(encoding="utf-8")
            site, _ = prepare_site_html(raw)
            blob = build_tgz_bytes(article_dir, site)
            names = tgz_member_names(blob)
            self.assertEqual(
                names,
                [
                    "article.html",
                    "article.meta.json",
                    "description-brief.json",
                    "cover/cover.png",
                    "cover/inline-01.png",
                    "cover/inline-02.png",
                    "cover/inline-03.png",
                ],
            )
            with tarfile.open(fileobj=BytesIO(blob), mode="r:gz") as tar:
                member = tar.extractfile("article.html")
                assert member is not None
                packed = member.read().decode("utf-8")
                meta_member = tar.extractfile("article.meta.json")
                assert meta_member is not None
                packed_meta = json.loads(meta_member.read().decode("utf-8"))
            self.assertNotIn("cover-hero", packed)
            self.assertIn("https://t.me/example_bot?start=ref1", packed)
            self.assertNotIn("/rasklad-taro-online/", packed)
            self.assertEqual(packed_meta.get("excerpt"), "")
            self.assertFalse(packed_meta.get("on_page_excerpt"))
            disk = (article_dir / "article.html").read_text(encoding="utf-8")
            self.assertIn("cover-hero", disk)

    def test_sanitize_meta_clears_first_paragraph_excerpt(self) -> None:
        dirty = {
            "excerpt": "Многие ждут ответа сразу. Здесь другая картина вечера.",
            "description": DESCRIPTION,
            "theme_blocks": {"faq": "skip"},
        }
        clean = sanitize_site_meta(dirty)
        self.assertEqual(clean["excerpt"], "")
        self.assertEqual(clean["dek"], "")
        self.assertEqual(clean["lead"], "")
        self.assertFalse(clean["on_page_excerpt"])
        self.assertEqual(clean["theme_blocks"]["lead"], "skip")
        self.assertEqual(clean["description"], DESCRIPTION)

    def test_live_double_lead_detects_b22_pattern(self) -> None:
        first = (
            "Возьмём: экран смартфона загорается ближе к полуночи: короткое «Привет, как ты?» "
            "или дежурное «Спишь?»."
        )
        html = (
            f"<h1>Он пишет, хотя вы уже расстались</h1>"
            f'<p class="seo-article__lead">{first} Вы разъехались, не</p>'
            f"<p>Автор: Виктория</p>"
            f"<div class=\"seo-content\"><p>{first} Вы разъехались, не строите общих планов.</p></div>"
        )
        self.assertTrue(live_double_lead_errors(html))
        clean = (
            "<h1>Он зашёл в сеть и молчит</h1>"
            "<p>Автор: Виктория</p>"
            "<div class=\"seo-content\"><p>Субботний вечер, экран телефона загорается.</p></div>"
        )
        self.assertFalse(live_double_lead_errors(clean))

    def test_first_body_paragraph_skips_cover_credit(self) -> None:
        html = (
            '<p class="cover-credit">Виктория - таролог команды «ТАРО СЕЙЧАС»</p>\n'
            "<h1>Он зашёл в сеть и молчит</h1>\n"
            "<p>Субботний вечер, 21:17: экран телефона загорается, а входящего нет.</p>\n"
        )
        self.assertIn("Субботний вечер", first_body_paragraph(html))
        self.assertNotIn("Виктория", first_body_paragraph(html))

    def test_telegram_rewrite_detect_and_restore_local(self) -> None:
        source = _article_html(cover_hero=False)
        live = _live_html(rewrite_tg=True)
        errors = telegram_rewritten_to_rasklad(source, live)
        self.assertTrue(errors)
        hrefs = collect_telegram_hrefs(source)
        fixed = rewrite_rasklad_back_to_telegram(live, hrefs)
        self.assertIn("https://t.me/example_bot?start=ref1", fixed)
        self.assertFalse(telegram_rewritten_to_rasklad(source, fixed))

    def test_second_cover_on_live(self) -> None:
        self.assertTrue(live_second_cover_errors(_live_html(second_cover=True)))
        self.assertFalse(live_second_cover_errors(_live_html(second_cover=False)))

    def test_skip_without_token(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article_dir = _write_article(Path(tmp))
            code, result = run_publish(
                article_dir=article_dir,
                root=ROOT,
                env={},
                site_base=DEFAULT_SITE_BASE,
                dry_run=False,
                skip_gates=False,
                http=FakeHttp(),
            )
            self.assertEqual(code, 0)
            self.assertEqual(result["verdict"], "skip")
            self.assertEqual(result["gate"], "PASS")
            self.assertEqual(result["publish"], "SKIP")
            self.assertEqual(result["reason"], "нет ключа")
            report = json.loads((article_dir / "site-publish-result.json").read_text(encoding="utf-8"))
            self.assertEqual(report["reason"], "нет ключа")
            blob = json.dumps(report)
            self.assertNotIn("Bearer ", blob)

    def test_publish_when_token_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article_dir = _write_article(Path(tmp))
            http = FakeHttp()
            code, result = run_publish(
                article_dir=article_dir,
                root=ROOT,
                env={"SITE_PUBLISH_TOKEN": "unit-test-token-not-for-git"},
                site_base=DEFAULT_SITE_BASE,
                dry_run=False,
                skip_gates=False,
                http=http,
            )
            self.assertEqual(code, 0, result)
            self.assertEqual(result["verdict"], "pass")
            self.assertEqual(result["publish"], "PUBLISHED")
            self.assertTrue(any(u.endswith("/excalibur/upload") for _, u in http.calls))
            self.assertTrue(any("/approve" in u for _, u in http.calls))
            self.assertTrue(any(u.endswith("/publish") for _, u in http.calls))
            self.assertFalse(any("dzen.ru" in u for _, u in http.calls))
            self.assertIn("Authorization", http.seen_headers[0])
            self.assertIn("X-Publish-Token", http.seen_headers[0])
            report = (article_dir / "site-publish-result.json").read_text(encoding="utf-8")
            self.assertNotIn("unit-test-token-not-for-git", report)
            self.assertNotIn("{{SITE_BASE}}".replace("SITE_BASE", "nope"), report)
            self.assertIn("{{SITE_BASE}}/blog/on-prochital-i-molchit/", report)

    def test_restore_telegram_if_site_rewrote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            article_dir = _write_article(Path(tmp), cover_hero=False)
            http = FakeHttp(
                live_html=_live_html(rewrite_tg=True),
                live_after_restore=_live_html(rewrite_tg=False),
            )
            code, result = run_publish(
                article_dir=article_dir,
                root=ROOT,
                env={"PUBLISH_TOKEN": "unit-test-token-not-for-git"},
                site_base=DEFAULT_SITE_BASE,
                dry_run=False,
                skip_gates=False,
                http=http,
            )
            self.assertEqual(code, 0, result)
            self.assertTrue(result.get("telegram_restored"))
            self.assertTrue(any(c[0] == "PATCH" for c in http.calls))

    def test_b21_never_hits_live(self) -> None:
        self.assertIn("B21", PROTECTED_LIVE_TOPIC_IDS)
        self.assertIn("B22", PROTECTED_LIVE_TOPIC_IDS)
        with tempfile.TemporaryDirectory() as tmp:
            article_dir = _write_article(Path(tmp), topic_id="B21")
            http = FakeHttp()
            code, result = run_publish(
                article_dir=article_dir,
                root=ROOT,
                env={"SITE_PUBLISH_TOKEN": "unit-test-token-not-for-git"},
                site_base=DEFAULT_SITE_BASE,
                dry_run=False,
                skip_gates=False,
                http=http,
            )
            self.assertEqual(code, 0)
            self.assertEqual(result["reason"], "B21 live protected")
            article_dir_b22 = _write_article(Path(tmp), topic_id="B22")
            http22 = FakeHttp()
            code22, result22 = run_publish(
                article_dir=article_dir_b22,
                root=ROOT,
                env={"SITE_PUBLISH_TOKEN": "unit-test-token-not-for-git"},
                site_base=DEFAULT_SITE_BASE,
                dry_run=False,
                skip_gates=False,
                http=http22,
            )
            self.assertEqual(code22, 0)
            self.assertEqual(result22["reason"], "B22 live protected")
            self.assertEqual(http22.calls, [])
            self.assertEqual(http.calls, [])

    def test_env_check_cli_no_secret(self) -> None:
        report = publish_env_report({})
        self.assertFalse(report["token_configured"])
        self.assertFalse(report["hall_upload"])
        self.assertFalse(report["dzen_studio"])
        code = main(["--env-check"])
        self.assertEqual(code, 0)

    def test_docs_and_doctor_wire_site_publish(self) -> None:
        contract = (ROOT / "shared/excalibur-site-publish-contract.md").read_text(encoding="utf-8")
        self.assertIn("нет ключа", contract)
        self.assertIn("SITE_PUBLISH_TOKEN", contract)
        self.assertIn("Hall", contract)
        self.assertIn("B21", contract)
        self.assertIn("B22", contract)
        doctor = (ROOT / "scripts/excalibur_blog_doctor.py").read_text(encoding="utf-8")
        self.assertIn("excalibur_blog_site_publish.py", doctor)
        director = (ROOT / "skills/director-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("excalibur_blog_site_publish.py", director)
        publish = (ROOT / "skills/publish-excalibur-blog/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("excalibur_blog_site_publish.py", publish)
        self.assertIn("нет ключа", publish)
        self.assertNotIn("Hall вызывает upload", publish)
        env_ex = (ROOT / ".env.example").read_text(encoding="utf-8")
        for name in TOKEN_ENV_NAMES:
            self.assertIn(f"{name}=", env_ex)
        self.assertNotRegex(env_ex, r"TOKEN=.+")


if __name__ == "__main__":
    unittest.main()
