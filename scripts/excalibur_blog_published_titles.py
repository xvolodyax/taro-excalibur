#!/usr/bin/env python3
"""Build titles-only ledger for Writer/Research (never article bodies).

Writer may know WHAT was already covered (title + slug), but must never open
old article.html / drafts / lessons. This script reads only:
- shared/published-articles.md
- existing shared/published-titles.md (never wipe if ledger has no dates)
- article.meta.json title/h1 (never article.html)
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from excalibur_blog_article_meta_index import is_stale_article_dirname

TOPIC_ID_RE = re.compile(r"^B\d+$", re.I)

HEADER = """# Published titles only — не читать тела статей

Этот файл — единственный «памятный» список для Writer/Research:
только topic_id, slug и заголовок.

**Запрещено:** открывать `memory/blog/articles/*/article.html`, drafts,
lessons, benchmarks, QA reports или соседние research-notes как образец
прозы. Заголовки нужны только чтобы не повторить уже покрытую тему.
"""


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def humanize_slug(slug: str) -> str:
    text = (slug or "").strip().strip("/").replace("-", " ").strip()
    return text[:1].upper() + text[1:] if text else ""


def load_ledger_rows(root: Path) -> list[dict[str, str]]:
    """Read published-articles.md.

    Two ledger shapes exist:
    - dated: ``| 2026-09-01 | B32 | slug | url | status |``
    - dateless (current tenant): ``| B32 | slug | status | permalink |``

    Dated rows are authoritative when present. Dateless ``| B\\d+ |`` rows
    still count so write_titles can add new IDs without requiring a date.
    """
    path = root / "shared" / "published-articles.md"
    rows: list[dict[str, str]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("| 20") and len(cells) >= 5:
            rows.append(
                {
                    "date": cells[0],
                    "topic_id": cells[1].upper(),
                    "slug": cells[2].strip().strip("/"),
                    "url": cells[3],
                    "status": cells[4].lower(),
                }
            )
            continue
        if len(cells) >= 3 and TOPIC_ID_RE.match(cells[0]):
            rows.append(
                {
                    "date": "",
                    "topic_id": cells[0].upper(),
                    "slug": cells[1].strip().strip("/"),
                    "url": cells[3] if len(cells) > 3 else "",
                    "status": cells[2].lower(),
                }
            )
    return rows


def load_existing_title_rows(path: Path) -> list[dict[str, str]]:
    """Parse shared/published-titles.md table rows (never article bodies)."""
    rows: list[dict[str, str]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        topic_id = cells[0].strip()
        if topic_id.lower() == "topic_id" or set(topic_id) <= {"-"}:
            continue
        if not (TOPIC_ID_RE.match(topic_id) or topic_id.upper() == "LIVE"):
            continue
        rows.append(
            {
                "topic_id": topic_id.upper() if TOPIC_ID_RE.match(topic_id) else topic_id,
                "slug": cells[1].strip().strip("/"),
                "title": cells[2],
                "status": cells[3].lower(),
                "date": "",
            }
        )
    return rows


def title_row_key(row: dict[str, str]) -> str:
    tid = (row.get("topic_id") or "").strip()
    if TOPIC_ID_RE.match(tid):
        return tid.upper()
    return f"{tid}|{(row.get('slug') or '').strip()}"


def title_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    tid = (row.get("topic_id") or "").strip()
    digits = re.search(r"\d+", tid) if TOPIC_ID_RE.match(tid) else None
    if digits:
        return (0, int(digits.group(0)), tid.upper())
    return (1, 0, tid)


def merge_title_rows(
    existing: list[dict[str, str]],
    built: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Keep existing titles; ledger/meta rows update matching keys.

    Durable: a dateless or empty ledger must not wipe published-titles.md.
    """
    merged: dict[str, dict[str, str]] = {}
    for row in existing:
        merged[title_row_key(row)] = dict(row)
    for row in built:
        key = title_row_key(row)
        old = merged.get(key)
        incoming = dict(row)
        if old:
            new_title = (incoming.get("title") or "").strip()
            old_title = (old.get("title") or "").strip()
            if old_title and (
                not new_title or new_title == humanize_slug(incoming.get("slug") or "")
            ):
                incoming["title"] = old_title
            if not incoming.get("status"):
                incoming["status"] = old.get("status") or ""
            if not incoming.get("slug"):
                incoming["slug"] = old.get("slug") or ""
        merged[key] = incoming
    return sorted(merged.values(), key=title_sort_key)


def title_from_meta(article_dir: Path) -> str:
    meta_path = article_dir / "article.meta.json"
    if not meta_path.is_file():
        return ""
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    if not isinstance(meta, dict):
        return ""
    for key in ("title", "h1"):
        value = str(meta.get(key) or "").strip()
        if value:
            return value
    return ""


def find_article_dir(blog_dir: Path, topic_id: str, slug: str) -> Path | None:
    preferred = blog_dir / f"{topic_id}-{slug}"
    if preferred.is_dir() and not is_stale_article_dirname(preferred.name):
        return preferred
    prefix = f"{topic_id}-"
    matches: list[Path] = []
    if not blog_dir.is_dir():
        return None
    for path in sorted(blog_dir.iterdir()):
        if not path.is_dir() or is_stale_article_dirname(path.name):
            continue
        if path.name.upper().startswith(prefix.upper()):
            matches.append(path)
    if not matches:
        return None
    if slug:
        for path in matches:
            if path.name.endswith(f"-{slug}") or slug in path.name:
                return path
    return matches[0]


def build_titles(
    root: Path,
    *,
    statuses: set[str] | None = None,
) -> list[dict[str, str]]:
    allowed = statuses or {
        "published",
        "in_progress",
        "draft_ready",
        "live",
        "quality_review",
        "hall-anti-dup",
        "hall-pack",
    }
    blog_dir = root / "memory" / "blog" / "articles"
    latest: dict[str, dict[str, str]] = {}
    for row in load_ledger_rows(root):
        if row["status"] not in allowed:
            continue
        topic_id = row["topic_id"]
        slug = row["slug"]
        article_dir = find_article_dir(blog_dir, topic_id, slug)
        title = title_from_meta(article_dir) if article_dir else ""
        if not title:
            title = humanize_slug(slug)
        latest[topic_id] = {
            "topic_id": topic_id,
            "slug": slug,
            "title": title,
            "status": row["status"],
            "date": row["date"],
        }
    return sorted(latest.values(), key=title_sort_key)


def render_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        HEADER.strip(),
        "",
        "| topic_id | slug | title | status |",
        "|----------|------|-------|--------|",
    ]
    for row in rows:
        title = row["title"].replace("|", "/")
        lines.append(
            f"| {row['topic_id']} | {row['slug']} | {title} | {row['status']} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_titles(
    root: Path,
    *,
    out_path: Path | None = None,
    article_dir: Path | None = None,
) -> dict[str, Any]:
    shared_path = out_path or (root / "shared" / "published-titles.md")
    built = build_titles(root)
    existing = load_existing_title_rows(shared_path)
    if not built and existing:
        # Ledger has no dated (or dateless B-id) rows — do not wipe titles.
        rows = existing
    elif existing:
        rows = merge_title_rows(existing, built)
    else:
        rows = built
    text = render_markdown(rows)
    shared_path.parent.mkdir(parents=True, exist_ok=True)
    shared_path.write_text(text, encoding="utf-8")
    article_copy: Path | None = None
    if article_dir is not None:
        article_dir.mkdir(parents=True, exist_ok=True)
        article_copy = article_dir / "published-titles-only.md"
        article_copy.write_text(text, encoding="utf-8")
    return {
        "count": len(rows),
        "shared_path": str(shared_path),
        "article_copy": str(article_copy) if article_copy else None,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None, help="shared/published-titles.md")
    parser.add_argument(
        "--article-dir",
        type=Path,
        default=None,
        help="Also write published-titles-only.md into article dir",
    )
    args = parser.parse_args()
    root = args.root or project_root()
    result = write_titles(root, out_path=args.out, article_dir=args.article_dir)
    print(f"OK titles={result['count']} shared={result['shared_path']}")
    if result["article_copy"]:
        print(f"article_copy={result['article_copy']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
