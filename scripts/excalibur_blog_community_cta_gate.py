#!/usr/bin/env python3
"""Hard gate: article CTA links and product-funnel split.

If cta_required is false and cta_links is empty → PASS (CTA optional).
If cta_required is true → every URL in cta_links must appear in article.html.
If cta_required is false but cta_links non-empty → require all listed URLs
(tenant asked for those links when present).

When tenant-config.cta_funnel is set, also enforce:
bots = spreads (triplet / Celtic), not audio / «Суть – Тень – Вектор»;
apps = audio «Суть – Тень – Вектор», not bot spreads;
Dzen articles must not send STV to the bot or mention Telegram.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

STV_RE = re.compile(r"суть\s*[–—\-]\s*тень\s*[–—\-]\s*вектор", re.I)
AUDIO_RE = re.compile(r"аудиоразбор", re.I)
TRIPLET_RE = re.compile(r"триплет", re.I)
CELTIC_RE = re.compile(r"кельтск", re.I)
FREE3_RE = re.compile(r"(?:3|три)\s+бесплатн", re.I)
VOICE_RE = re.compile(r"голос", re.I)
ADVICE_RE = re.compile(r"практическ\w*\s+совет", re.I)
CLARIFY_RE = re.compile(r"уточняющ", re.I)
TELEGRAM_RE = re.compile(r"telegram|t\.me|телеграм", re.I)
BOT_WORD_RE = re.compile(r"бот", re.I)
GO_TO_BOT_STV_RE = re.compile(
    r"(хочешь|нужен|нужна|иди|открой|запусти|переходи).{0,80}"
    r"суть\s*[–—\-]\s*тень\s*[–—\-]\s*вектор"
    r".{0,80}бот"
    r"|"
    r"суть\s*[–—\-]\s*тень\s*[–—\-]\s*вектор"
    r".{0,80}(иди|открой|запусти|переходи).{0,40}бот",
    re.I | re.S,
)


def load_tenant(root: Path) -> dict:
    path = root / "shared/tenant-config.json"
    if not path.is_file():
        return {"cta_required": False, "cta_links": []}
    return json.loads(path.read_text(encoding="utf-8"))


def url_patterns(url: str) -> re.Pattern[str]:
    """Build a loose href matcher for a concrete CTA URL."""
    url = (url or "").strip()
    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").rstrip("/")
    host_re = re.escape(host)
    path_re = re.escape(path) if path else ""
    if path_re:
        pat = rf"""https?://{host_re}{path_re}(?:/|\b|"|'|>|\?)"""
    else:
        pat = rf"""https?://{host_re}(?:/|\b|"|'|>|\?)"""
    return re.compile(pat, re.I)


def _same_cta(href: str, expected: str) -> bool:
    """Match host+path; query-aware so bot URL ≠ Max mini-app ?startapp=."""
    got = urlparse((href or "").strip())
    want = urlparse((expected or "").strip())
    if (got.netloc or "").lower() != (want.netloc or "").lower():
        return False
    if (got.path or "").rstrip("/") != (want.path or "").rstrip("/"):
        return False
    got_q = parse_qs(got.query or "")
    want_q = parse_qs(want.query or "")
    if want_q:
        return all(got_q.get(key) == value for key, value in want_q.items())
    return "startapp" not in got_q


def href_in(text: str, url: str) -> bool:
    if not url:
        return False
    hrefs = re.findall(r"""href\s*=\s*["']([^"']+)["']""", text or "", flags=re.I)
    if any(_same_cta(href, url) for href in hrefs):
        return True
    # Fallback for plain-text mentions without an href attribute.
    if hrefs:
        return False
    return _same_cta((text or "").strip(), url)


def iter_paragraphs(html: str) -> list[str]:
    return re.findall(r"<p\b[^>]*>.*?</p>", html or "", flags=re.I | re.S)


def funnel_urls(tenant: dict) -> tuple[str, str]:
    funnel = tenant.get("cta_funnel") or {}
    dzen = funnel.get("dzen") or {}
    spread = dzen.get("spread") or {}
    audio = dzen.get("audio") or {}
    bot_url = str(spread.get("href") or "").strip()
    app_url = str(audio.get("href") or "").strip()
    links = [str(x).strip() for x in (tenant.get("cta_links") or []) if str(x).strip()]
    if not bot_url and links:
        bot_url = next((u for u in links if "max.ru" in u and "bot" in u), "")
    if not app_url and links:
        app_url = next((u for u in links if "vk.com/app" in u), "")
    return bot_url, app_url


def check_html(html: str, links: list[str], *, required: bool) -> tuple[list[str], dict[str, bool]]:
    errors: list[str] = []
    present: dict[str, bool] = {}
    if not links:
        if required:
            errors.append("cta_required=true but tenant-config.cta_links is empty")
        return errors, present
    for link in links:
        ok = href_in(html, link)
        present[link] = ok
        if not ok:
            errors.append(f"missing required CTA href {link}")
    return errors, present


def check_forbidden(html: str, tenant: dict) -> list[str]:
    errors: list[str] = []
    for needle in tenant.get("cta_forbidden") or []:
        n = str(needle).strip()
        if n and n.lower() in (html or "").lower():
            errors.append(f"forbidden CTA token present: {n}")
    return errors


def check_funnel(html: str, tenant: dict) -> list[str]:
    """Enforce bot vs app product split when cta_funnel is configured."""
    funnel = tenant.get("cta_funnel")
    if not funnel:
        return []
    errors: list[str] = []
    dzen = funnel.get("dzen") or {}
    bot_url, app_url = funnel_urls(tenant)

    if dzen.get("telegram_href") is False or dzen.get("telegram_mention") is False:
        if TELEGRAM_RE.search(html or ""):
            errors.append("Telegram mention or href is forbidden in Dzen article")

    if GO_TO_BOT_STV_RE.search(html or ""):
        errors.append("cannot send «Суть – Тень – Вектор» to the bot")

    for para in iter_paragraphs(html or ""):
        bot_here = href_in(para, bot_url)
        app_here = href_in(para, app_url)
        stv = bool(STV_RE.search(para))
        audio = bool(AUDIO_RE.search(para))
        if bot_here and app_here:
            errors.append("bot href and app href share a paragraph")
        if bot_here and (stv or audio):
            errors.append(
                "аудиоразбор / «Суть – Тень – Вектор» cannot share a paragraph with the Max bot"
            )
        if app_here and (TRIPLET_RE.search(para) or CELTIC_RE.search(para) or FREE3_RE.search(para)):
            errors.append(
                "triplet / Celtic / 3 free spreads cannot share a paragraph with the app href"
            )
        if stv and BOT_WORD_RE.search(para) and not app_here:
            errors.append("«Суть – Тень – Вектор» cannot be attached to the bot")

    required = list(funnel.get("gate_required_mentions") or [])
    lowered = html or ""
    mention_checks = {
        "триплет": TRIPLET_RE,
        "кельтск": CELTIC_RE,
        "аудиоразбор": AUDIO_RE,
        "суть-тень-вектор": STV_RE,
        "голос": VOICE_RE,
        "практический совет": ADVICE_RE,
        "уточняющ": CLARIFY_RE,
    }
    for key in required:
        cre = mention_checks.get(key)
        if cre is None:
            if key.lower() not in lowered.lower():
                errors.append(f"missing required funnel mention: {key}")
        elif not cre.search(lowered):
            errors.append(f"missing required funnel mention: {key}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--article-dir", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("-o", "--output", default="community-cta-gate.json")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = (root / article_dir).resolve()

    tenant = load_tenant(root)
    links = [str(x).strip() for x in (tenant.get("cta_links") or []) if str(x).strip()]
    cta_required = bool(tenant.get("cta_required"))

    html_path = article_dir / "article.html"
    errors: list[str] = []
    html = ""
    present: dict[str, bool] = {}
    if not html_path.is_file():
        errors.append("article.html missing")
    else:
        html = html_path.read_text(encoding="utf-8")
        if not links and not cta_required:
            present = {}
        else:
            link_errors, present = check_html(html, links, required=cta_required)
            errors.extend(link_errors)
        errors.extend(check_forbidden(html, tenant))
        errors.extend(check_funnel(html, tenant))
    if not links and not cta_required and html_path.is_file():
        present = present or {}

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "article_dir": str(article_dir.relative_to(root)).replace("\\", "/"),
        "cta_required": cta_required,
        "required": links,
        "present": present,
        "funnel": bool(tenant.get("cta_funnel")),
        "errors": errors,
    }
    out_name = Path(args.output).name
    out_path = article_dir / out_name
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
