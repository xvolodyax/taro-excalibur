#!/usr/bin/env python3
"""Excalibur BLOG LLMs Generator: AI-First Crawler Policy.

Generates and maintains standard llms.txt and llms-full.txt in the root folder,
providing LLM-readable indices and plain-text summaries of all blog articles.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.excalibur_blog_site_base import redact_site_base  # noqa: E402


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def strip_html(html: str) -> str:
    # Remove script and style tags completely
    html = re.sub(r"<(script|style)[^>]*>[\s\S]*?</\1>", "", html, flags=re.IGNORECASE)
    # Convert paragraph endings and headers to newlines
    html = re.sub(r"</?(p|h1|h2|h3|li|div|blockquote)[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Remove all other HTML tags
    text = re.sub(r"<[^>]+>", "", html)
    # Normalize whitespaces and newlines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()


def load_articles(blog_dir: Path) -> list[dict[str, Any]]:
    articles = []
    if not blog_dir.is_dir():
        return articles

    for article_dir in blog_dir.iterdir():
        if not article_dir.is_dir():
            continue
        meta_path = article_dir / "article.meta.json"
        html_path = article_dir / "article.html"
        if meta_path.is_file() and html_path.is_file():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                html_content = html_path.read_text(encoding="utf-8")
                plain_text = strip_html(html_content)

                # Use AEO description as the highly dense summaries for AI
                meta_ab = meta.get("meta_ab", {})
                aeo_desc = meta_ab.get("description_aeo") or meta_ab.get("description_seo") or meta.get("description", "")

                articles.append({
                    "slug": meta.get("slug", article_dir.name),
                    "title": meta_ab.get("title_aeo") or meta_ab.get("title_seo") or meta.get("title") or meta.get("h1", article_dir.name),
                    "description": aeo_desc,
                    "plain_text": plain_text,
                })
            except Exception as e:
                print(f"Error loading {article_dir.name}: {e}")
    return articles


def load_tenant_config(root: Path) -> dict[str, Any]:
    cfg_path = root / "shared/tenant-config.json"
    if cfg_path.is_file():
        try:
            return json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def parse_existing_llms_txt(path: Path) -> tuple[str, str, list[dict[str, str]]]:
    if not path.is_file():
        return "", "", []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return "", "", []
    lines = content.splitlines()
    site_name = ""
    site_desc = ""
    articles: list[dict[str, str]] = []
    in_articles = False
    for line in lines:
        s = line.strip()
        if s.startswith("# ") and not site_name:
            site_name = s[2:].strip()
        elif s.startswith("> ") and not site_desc:
            site_desc = s[2:].strip()
        elif s.startswith("## Blog Articles"):
            in_articles = True
        elif in_articles and s.startswith("- ["):
            m = re.match(r"^-\s*\[(.*?)\]\((.*?)\):\s*(.*)$", s)
            if m:
                articles.append({
                    "title": m.group(1).strip(),
                    "url": m.group(2).strip(),
                    "description": m.group(3).strip(),
                })
    return site_name, site_desc, articles


def parse_existing_llms_full_txt(path: Path) -> tuple[str, list[dict[str, str]]]:
    if not path.is_file():
        return "", []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return "", []
    parts = re.split(r"\n---\n?", content)
    if not parts:
        return "", []
    header = parts[0].strip()
    articles: list[dict[str, str]] = []
    for part in parts[1:]:
        p_str = part.strip()
        if not p_str:
            continue
        m = re.match(
            r"^##\s*(.*?)\n-\s*\*\*URL\*\*:\s*([^\n]+)\n-\s*\*\*Summary\*\*:\s*([^\n]+)\n*(.*)$",
            p_str,
            flags=re.DOTALL,
        )
        if m:
            articles.append({
                "title": m.group(1).strip(),
                "url": m.group(2).strip(),
                "description": m.group(3).strip(),
                "plain_text": m.group(4).strip(),
            })
        else:
            url_m = re.search(r"-\s*\*\*URL\*\*:\s*([^\n]+)", p_str)
            url = url_m.group(1).strip() if url_m else ""
            title_m = re.search(r"^##\s*(.*?)\n", p_str)
            title = title_m.group(1).strip() if title_m else ""
            summary_m = re.search(r"-\s*\*\*Summary\*\*:\s*([^\n]+)", p_str)
            summary = summary_m.group(1).strip() if summary_m else ""
            articles.append({
                "title": title,
                "url": url,
                "description": summary,
                "plain_text": p_str,
            })
    return header, articles


def article_url(site_base: str, blog_path: str, slug: str) -> str:
    site_base = site_base.rstrip("/")
    path = "/" + blog_path.strip("/")
    if path == "/":
        return f"{site_base}/{slug}/"
    return f"{site_base}{path}/{slug}/"


def build_llms_txt(
    site_name: str,
    site_desc: str,
    articles: list[dict[str, Any]],
    site_base: str,
    blog_path: str,
) -> str:
    lines = [
        f"# {site_name}",
        f"> {site_desc}",
        "",
        "## Blog Articles",
        ""
    ]
    for a in articles:
        url = a.get("url") or article_url(site_base, blog_path, a["slug"])
        lines.append(f"- [{a['title']}]({url}): {a['description']}")

    return "\n".join(lines) + "\n"


def build_llms_full_txt(site_name: str, articles: list[dict[str, Any]], site_base: str, blog_path: str) -> str:
    lines = [
        f"# {site_name} - Full LLM Knowledge Base",
        "This file contains full plain-text articles optimized for AI reasoning and semantic search.",
        "",
        "---",
        ""
    ]

    for a in articles:
        url = a.get("url") or article_url(site_base, blog_path, a["slug"])
        lines.extend([
            f"## {a['title']}",
            f"- **URL**: {url}",
            f"- **Summary**: {a['description']}",
            "",
            a["plain_text"],
            "",
            "---",
            ""
        ])

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate AI-friendly llms.txt and llms-full.txt")
    ap.add_argument("--blog-dir", type=Path, default=None)
    ap.add_argument("--site-name", type=str, default=None)
    ap.add_argument("--site-desc", type=str, default=None)
    ap.add_argument(
        "--site-base",
        type=str,
        default="{{SITE_BASE}}",
        help="Git-safe site base for committed llms artifacts (default: {{SITE_BASE}}; publish expands)",
    )
    ap.add_argument("--blog-path", type=str, default="/", help="URL prefix for posts, e.g. /blog/ or /")
    ap.add_argument("--out-dir", type=Path, default=None, help="Output directory for llms.txt/llms-full.txt")
    args = ap.parse_args()

    root = project_root()
    blog_dir = args.blog_dir or root / "memory/blog/articles"
    if not blog_dir.is_absolute():
        blog_dir = root / blog_dir

    out_dir = args.out_dir or root
    if not out_dir.is_absolute():
        out_dir = root / out_dir

    llms_path = out_dir / "llms.txt"
    llms_full_path = out_dir / "llms-full.txt"

    tenant_cfg = load_tenant_config(root)
    existing_site_name, existing_site_desc, existing_articles = parse_existing_llms_txt(llms_path)
    existing_full_header, existing_full_articles = parse_existing_llms_full_txt(llms_full_path)

    site_name = (
        args.site_name
        or existing_site_name
        or tenant_cfg.get("brand_name")
        or "Maya AI — Excalibur BLOG"
    ).strip()

    site_desc = (
        args.site_desc
        or existing_site_desc
        or tenant_cfg.get("niche")
        or "Практический блог по автоматизации бизнеса на Make.com, вайбкодингу и ИИ-агентам."
    ).strip()

    site_base = (args.site_base or "").strip() or "{{SITE_BASE}}"
    if site_base == "[REDACTED]":
        print(
            "WARN --site-base [REDACTED] is invalid for git artifacts; using {{SITE_BASE}}",
            file=sys.stderr,
        )
        site_base = "{{SITE_BASE}}"

    new_articles = load_articles(blog_dir)
    print(f"Loaded {len(new_articles)} new/updated articles from {blog_dir}.")

    # Merge into existing_articles for llms.txt
    merged_articles = list(existing_articles)
    for na in new_articles:
        url = article_url(site_base, args.blog_path, na["slug"])
        norm_url = url.rstrip("/")
        found_idx = None
        for idx, ea in enumerate(merged_articles):
            if ea.get("url", "").rstrip("/") == norm_url:
                found_idx = idx
                break
        entry = {
            "title": na["title"],
            "url": url,
            "description": na["description"],
            "slug": na["slug"],
        }
        if found_idx is not None:
            merged_articles[found_idx] = entry
        else:
            merged_articles.insert(0, entry)

    # Merge into existing_full_articles for llms-full.txt
    merged_full = list(existing_full_articles)
    for na in new_articles:
        url = article_url(site_base, args.blog_path, na["slug"])
        norm_url = url.rstrip("/")
        found_idx = None
        for idx, efa in enumerate(merged_full):
            if efa.get("url", "").rstrip("/") == norm_url:
                found_idx = idx
                break
        entry = {
            "title": na["title"],
            "url": url,
            "description": na["description"],
            "plain_text": na["plain_text"],
        }
        if found_idx is not None:
            merged_full[found_idx] = entry
        else:
            merged_full.insert(0, entry)

    print(f"Total articles indexed: {len(merged_articles)} in llms.txt, {len(merged_full)} in llms-full.txt.")

    # redact_site_base: full PUBLIC_SITE_URL → {{SITE_BASE}}, bare host in prose
    # (legacy article excerpts in llms-full) → {{SITE_HOST}} via env / public base.
    llms_txt = redact_site_base(
        build_llms_txt(site_name, site_desc, merged_articles, site_base, args.blog_path)
    )
    llms_full_txt = redact_site_base(
        build_llms_full_txt(site_name, merged_full, site_base, args.blog_path)
    )

    llms_path.write_text(llms_txt, encoding="utf-8")
    llms_full_path.write_text(llms_full_txt, encoding="utf-8")

    print(f"llms.txt generated at {llms_path.relative_to(root) if root in llms_path.parents else llms_path}")
    print(f"llms-full.txt generated at {llms_full_path.relative_to(root) if root in llms_full_path.parents else llms_full_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
