#!/usr/bin/env python3
"""HARD topic-focus gate for Scout / research_start / today.

Blocks PageSpeed / Metrika / Webmaster / Direct / indexing topics even when
the card mentions «Cursor». Soft Scout prompts failed repeatedly (B91–B99).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# Substrings matched case-insensitively against joined topic text.
# DENY wins over ALLOW — «Cursor + PageSpeed» is still BLOCK.
DENY_PATTERNS: tuple[str, ...] = (
    r"pagespeed",
    r"page\s*speed",
    r"core\s*web\s*vitals",
    r"\blcp\b",
    r"\binp\b",
    r"\bcls\b",
    r"скорость\s+сайта",
    r"скорость\s+загрузки",
    r"провер\w*\s+скорост",
    r"google\s*analytics",
    r"\bga4\b",
    r"gtag\.js",
    r"вебвизор",
    r"webvisor",
    r"utm[\s_-]?мет",
    r"яндекс\s*директ",
    r"yandex\s*direct",
    r"ретаргет",
    r"retarget",
    r"вебмастер",
    r"webmaster",
    r"search\s*console",
    r"search-console",
    r"индексац",
    r"провер\w*\s+индекс",
    r"цели\s+в\s+яндекс\s*метрик",
    r"настро\w*\s+цели\w*\s+.*метрик",
    r"установ\w*\s+google\s*analytics",
    r"установ\w*\s+ga4",
    r"включ\w*\s+вебвизор",
    # RF / Dzen DENY heroes — shared/rf-blocked-entities.json + dzen-content-rules.md
    # Meta Platforms / Facebook / Instagram (суд 21.03.2022). Не «meta-теги» SEO.
    r"\bfacebook\b",
    r"\bфейсбук\b",
    r"\bmeta\s*platforms?\b",
    r"\bmeta\s*ai\b",
    r"research\.meta\.ai",
    r"\bmuse\s*code\b",
    r"\bmuse\s*spark\b",
    r"\bthreads\b",
    r"\bу\s+meta\b",
    r"\bmeta\s+(?!teg|тег)",
    r"\binstagram\b",
    r"\bинстаграм\b",
    r"\bинсте\b",
    r"\bинста\b",
    r"\blinkedin\b",
    r"\bлинкедин\b",
    r"\btwitter\b",
    r"\bx\.com\b",
    r"\bdiscord\b",
    r"\bдискорд\b",
    r"мессенджер\s+signal\b",
    r"\bsignal\s+messenger\b",
    r"\bприложение\s+signal\b",
    r"\bвайбер\b",
    r"\bviber\b",
    r"обход\w*\s+блокир",
    r"\bvpn\b.*обход",
    r"обход\w*.*\bvpn\b",
    r"как\s+обойти\s+блокир",
    # Tenant ТАРО СЕЙЧАС — not article heroes
    r"\bсво\b",
    r"самолечен",
    r"прочитать\s+мысл",
    r"читать\s+мысл",
    r"прочит\w*\s+мысл",
    r"\btelegram\b",
    r"\bt\.me\b",
    r"таргет\s*13",
    r"подростк",
)

# At least one core marker must appear (after DENY pass).
# Tenant ТАРО СЕЙЧАС: отношения / пауза / таро — не Cursor/AI-скелет.
ALLOW_PATTERNS: tuple[str, ...] = (
    r"тар[оo]",
    r"расклад",
    r"пауз",
    r"отношен",
    r"верн(ёт|ется|уться|улся|ётся)",
    r"чувств",
    r"написать\s+перв",
    r"звон",
    r"набрать",
    r"смотр\w*\s+истор",
    r"истории",
    r"карт(ы|а|ами|ах)?\b",
    r"расста",
    r"измен",
    r"любов",
    r"парень",
    r"молчит",
    r"молчан",
    r"конец\b",
    r"аудиоразбор",
    r"бот\s+в\s+макс",
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def focus_check(text: str) -> dict[str, Any]:
    """Return PASS/BLOCK verdict for topic card / query text."""
    blob = normalize(text)
    if not blob:
        return {
            "status": "BLOCK",
            "blocker": "TOPIC FOCUS BLOCKER",
            "reason": "empty topic text",
            "deny_hit": None,
            "allow_hit": None,
        }

    for pat in DENY_PATTERNS:
        if re.search(pat, blob, flags=re.IGNORECASE):
            return {
                "status": "BLOCK",
                "blocker": "TOPIC FOCUS BLOCKER",
                "reason": (
                    "forbidden cluster (PageSpeed/Metrika/Webmaster/Direct/"
                    f"indexing/analytics): matched /{pat}/"
                ),
                "deny_hit": pat,
                "allow_hit": None,
            }

    allow_hit = None
    for pat in ALLOW_PATTERNS:
        if re.search(pat, blob, flags=re.IGNORECASE):
            allow_hit = pat
            break
    if not allow_hit:
        return {
            "status": "BLOCK",
            "blocker": "TOPIC FOCUS BLOCKER",
            "reason": (
                "no core-focus marker (таро/расклад/пауза/отношения/"
                "что чувствует/вернётся/написать первой/смотрит истории)"
            ),
            "deny_hit": None,
            "allow_hit": None,
        }

    return {
        "status": "PASS",
        "blocker": None,
        "reason": "on-focus",
        "deny_hit": None,
        "allow_hit": allow_hit,
    }


def topic_card_text(card: dict[str, Any]) -> str:
    # Identity fields only. beginner_angle often says «не PageSpeed / не Метрика»
    # as a negative — do not treat those mentions as the topic itself.
    secondary = card.get("secondary_queries") or ""
    if isinstance(secondary, list):
        secondary = " ".join(str(x) for x in secondary)
    parts = [
        str(card.get("topic_id") or ""),
        str(card.get("h1") or ""),
        str(card.get("primary_query") or ""),
        str(card.get("slug") or ""),
        str(secondary),
    ]
    return " ".join(parts)


def assert_topic_focus(card: dict[str, Any]) -> None:
    """Raise ValueError with TOPIC FOCUS BLOCKER if off-focus."""
    verdict = focus_check(topic_card_text(card))
    if verdict["status"] != "PASS":
        tid = card.get("topic_id") or "?"
        raise ValueError(
            f"{verdict['blocker']}: topic {tid} off-focus — {verdict['reason']}"
        )


def main() -> int:
    ap = argparse.ArgumentParser(description="Excalibur BLOG hard topic-focus gate")
    ap.add_argument("--text", required=True, help="h1 + primary_query + slug (+ more)")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    verdict = focus_check(args.text)
    print(f"status={verdict['status']}")
    print(f"reason={verdict['reason']}")
    if verdict.get("deny_hit"):
        print(f"deny_hit={verdict['deny_hit']}")
    if verdict.get("allow_hit"):
        print(f"allow_hit={verdict['allow_hit']}")
    if verdict["status"] != "PASS":
        print(f"BLOCKER: {verdict['blocker']}")
        return 1
    print("TOPIC FOCUS PASS")
    return 0


if __name__ == "__main__":
    # Allow `python3 scripts/excalibur_blog_topic_focus.py` self-test path.
    _ = Path(__file__).resolve()
    sys.exit(main())
