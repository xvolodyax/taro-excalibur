#!/usr/bin/env python3
"""Gate: early «сразу к делу» insert after the first scene paragraph.

Canon: shared/early-act-insert.md (Vladimir, 2026-08-25).
"""
from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(
    r"сразу\s+к\s+делу|если\s+коротко",
    re.I,
)
ANY_SITUATION_RE = re.compile(
    r"загадай\s+любую\s+ситуац|задай\s+любой\s+вопрос|любую\s+ситуацию",
    re.I,
)
TELEGRAM_RE = re.compile(r"telegram|t\.me|телеграм", re.I)
BOT_HREF_RE = re.compile(
    r'href\s*=\s*["\']https://max\.ru/id531102974575_bot(?!\?startapp)',
    re.I,
)
APP_HREF_RE = re.compile(
    r'href\s*=\s*["\']https://vk\.com/app54565776["\']'
    r'|href\s*=\s*["\']https://max\.ru/id531102974575_bot\?startapp=',
    re.I,
)


class _Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.events: list[tuple[str, str]] = []
        self._tag = ""
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"p", "h2", "ul"}:
            self._tag = tag.lower()
            self._buf = []

    def handle_data(self, data: str) -> None:
        if self._tag:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == self._tag:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            self.events.append((self._tag, text))
            self._tag = ""
            self._buf = []


def first_h2_and_prefix(html: str) -> tuple[str, str, str]:
    """Return (first_h2_text, html_before_second_h2, html_after_first_p)."""
    h2s = list(re.finditer(r"<h2\b[^>]*>(.*?)</h2>", html or "", flags=re.I | re.S))
    first = re.sub(r"<[^>]+>", "", h2s[0].group(1)) if h2s else ""
    first = re.sub(r"\s+", " ", first).strip()
    before_second = html[: h2s[1].start()] if len(h2s) > 1 else (html or "")
    first_p = re.search(r"<p\b[^>]*>.*?</p>", html or "", flags=re.I | re.S)
    after_first_p = html[first_p.end() :] if first_p else (html or "")
    return first, before_second, after_first_p


def check_html(html: str) -> list[str]:
    errors: list[str] = []
    if not html.strip():
        return ["article.html empty"]
    if TELEGRAM_RE.search(html):
        errors.append("Telegram is forbidden in Dzen article.html")
    if ANY_SITUATION_RE.search(html):
        errors.append("early insert must not say «загадай любую ситуацию»")

    first_p = re.search(r"<p\b[^>]*>.*?</p>", html, flags=re.I | re.S)
    if not first_p:
        errors.append("missing opening scene <p>")
        return errors
    rest_before_h2 = html[first_p.end() : re.search(r"<h2\b", html, flags=re.I).start()] if re.search(r"<h2\b", html, flags=re.I) else ""
    extra_p = re.findall(r"<p\b", rest_before_h2, flags=re.I)
    if extra_p:
        errors.append("opening must be one short <p>; early insert comes next")

    first_h2, before_second, after_first_p = first_h2_and_prefix(html)
    if not HEADING_RE.search(first_h2):
        errors.append(
            f"first H2 must be the early-act insert (Сразу к делу / Если коротко), got {first_h2!r}"
        )
    if not BOT_HREF_RE.search(before_second):
        errors.append("early insert must include Max bot href (spread door)")
    if not APP_HREF_RE.search(before_second):
        errors.append("early insert must include VK app and/or Max app href (audio door)")
    lis = re.findall(r"<li\b[^>]*>.*?</li>", before_second, flags=re.I | re.S)
    if len(lis) < 2 or len(lis) > 3:
        errors.append("early insert needs 2–3 ready card questions as <li>")
    # Insert must start after the first paragraph, not later in the body.
    if after_first_p.lstrip()[:3].lower() != "<h2":
        # allow whitespace / comments only
        stripped = re.sub(r"<!--.*?-->", "", after_first_p, flags=re.S).lstrip()
        if not stripped.lower().startswith("<h2"):
            errors.append("early-act H2 must follow the first scene paragraph")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--article-dir", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("-o", "--output", default="early-act-gate.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = (root / article_dir).resolve()
    html_path = article_dir / "article.html"
    errors: list[str] = []
    if not html_path.is_file():
        errors.append("article.html missing")
    else:
        errors.extend(check_html(html_path.read_text(encoding="utf-8")))
    status = "PASS" if not errors else "FAIL"
    report: dict[str, Any] = {
        "gate": "early-act-insert",
        "status": status,
        "canon": "shared/early-act-insert.md",
        "errors": errors,
    }
    out = article_dir / Path(args.output).name
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
