#!/usr/bin/env python3
"""HARD editorial rules for the opening (Vladimir 29.08).

1. «Возьмём:» / «Возьмем:» is forbidden. First body line is the situation.
2. Lead is written once — in the article body. Theme ``p.seo-article__lead``
   must not reprint the first paragraph (live B22 double-lead).
3. On-page excerpt/dek/lead stays empty. Description is the Dzen/RSS card,
   not a dek under H1.
"""
from __future__ import annotations

import re
from typing import Any

VOZMEM_RE = re.compile(r"возьм[её]м\s*:", re.IGNORECASE)
ON_PAGE_LEAD_CLASS_RE = re.compile(
    r"<p\b[^>]*\bclass=['\"][^'\"]*\b(?:seo-article__lead|excerpt|dek|lead)\b[^'\"]*['\"][^>]*>",
    re.I,
)
LEAD_P_RE = re.compile(
    r"<p\b([^>]*)>(.*?)</p>",
    re.I | re.S,
)
AUTHOR_LINE_RE = re.compile(r"^\s*автор\s*:", re.I)
ON_PAGE_EXCERPT_KEYS = ("excerpt", "dek", "lead", "subtitle", "on_page_excerpt")


def plain(text: str) -> str:
    out = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", out).strip()


def norm_prefix(text: str, n: int = 80) -> str:
    t = plain(text).casefold()
    t = re.sub(r"[\"«»„“”]+", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n]


def has_vozmem_label(text: str) -> bool:
    return bool(VOZMEM_RE.search(text or ""))


def first_body_paragraph(html: str) -> str:
    """First real body <p> — skip theme lead/excerpt and the author line."""
    for match in LEAD_P_RE.finditer(html or ""):
        attrs, inner = match.group(1), match.group(2)
        cls = attrs.lower()
        if re.search(r"\b(?:seo-article__lead|excerpt|dek|lead|cover-credit)\b", cls):
            continue
        text = plain(inner)
        if not text or AUTHOR_LINE_RE.match(text):
            continue
        if text.casefold().startswith("виктория - таролог"):
            continue
        return text
    return ""


def extract_theme_lead(html: str) -> str:
    match = re.search(
        r"<p\b[^>]*\bclass=['\"][^'\"]*\bseo-article__lead\b[^'\"]*['\"][^>]*>(.*?)</p>",
        html or "",
        flags=re.I | re.S,
    )
    return plain(match.group(1)) if match else ""


def clones_opening(excerpt: str, body_html: str, *, min_chars: int = 40) -> bool:
    """True when excerpt/dek is a truncated copy of the first body paragraph."""
    desc = plain(excerpt).rstrip("…").rstrip(".,;:").strip()
    if len(desc) < min_chars:
        return False
    first = first_body_paragraph(body_html)
    if not first:
        return False
    a, b = norm_prefix(desc, 80), norm_prefix(first, 80)
    if not a or not b:
        return False
    return b.startswith(a[: min(len(a), 60)]) or a.startswith(b[: min(len(b), 60)])


def article_html_double_lead_errors(html: str) -> list[str]:
    """Source article.html must not emit a theme dek or two identical opening <p>."""
    errors: list[str] = []
    if ON_PAGE_LEAD_CLASS_RE.search(html or ""):
        errors.append(
            "article.html must not emit p.seo-article__lead / excerpt / dek; "
            "lead lives once in the body"
        )
    paras: list[str] = []
    for match in LEAD_P_RE.finditer(html or ""):
        text = plain(match.group(2))
        if text and not AUTHOR_LINE_RE.match(text):
            paras.append(text)
        if len(paras) >= 2:
            break
    if len(paras) >= 2 and clones_opening(paras[0], f"<p>{paras[1]}</p>", min_chars=40):
        errors.append("first two <p> after H1 are the same lead twice")
    return errors


def live_double_lead_errors(live_html: str) -> list[str]:
    """Live theme printed seo-article__lead that clones the first body paragraph."""
    lead = extract_theme_lead(live_html)
    if not lead:
        return []
    first = first_body_paragraph(live_html)
    if first and clones_opening(lead, f"<p>{first}</p>", min_chars=24):
        return ["live seo-article__lead clones first body paragraph"]
    # Title + first paragraph glued into excerpt (B23 upload default).
    if first and first[:40].casefold() in lead.casefold():
        return ["live seo-article__lead contains first body paragraph"]
    return []


def meta_on_page_excerpt_errors(meta: dict[str, Any], body_html: str) -> list[str]:
    errors: list[str] = []
    excerpt = str(meta.get("excerpt") or "").strip()
    dek = str(meta.get("dek") or "").strip()
    lead = str(meta.get("lead") or "").strip()
    for label, value in (("excerpt", excerpt), ("dek", dek), ("lead", lead)):
        if has_vozmem_label(value):
            errors.append(f"article.meta.json {label}: vozmem-label")
        if value and clones_opening(value, body_html):
            errors.append(f"article.meta.json {label} clones first body paragraph")
    if meta.get("on_page_excerpt") is True:
        errors.append("article.meta.json on_page_excerpt must be false")
    return errors


def sanitize_site_meta(meta: dict[str, Any]) -> dict[str, Any]:
    """Theme always prints excerpt as p.seo-article__lead. Keep it empty."""
    out = dict(meta)
    out["excerpt"] = ""
    out["dek"] = ""
    out["lead"] = ""
    out["on_page_excerpt"] = False
    blocks = dict(out.get("theme_blocks") or {})
    if not isinstance(blocks, dict):
        blocks = {}
    blocks["lead"] = "skip"
    for key in ("faq", "quiz", "side_stickers"):
        blocks.setdefault(key, "skip")
    out["theme_blocks"] = blocks
    return out


def vozmem_hits(text: str) -> list[str]:
    return ["vozmem-label"] if has_vozmem_label(text) else []
