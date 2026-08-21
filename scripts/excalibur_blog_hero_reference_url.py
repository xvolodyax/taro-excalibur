#!/usr/bin/env python3
"""Ensure blog hero reference has a public URL for MCP gpt-image-2 input_urls."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from excalibur_blog_site_base import (
    REDACTED_LITERAL,
    SITE_BASE_PLACEHOLDER,
    expand_site_base,
    resolve_public_base_from_env,
    to_git_safe_site_url,
)


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upload_catbox(image_path: Path) -> str:
    boundary = "----ExcaliburHeroBoundary"
    body_prefix = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        f"fileupload\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{image_path.name}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8")
    body_suffix = f"\r\n--{boundary}--\r\n".encode("utf-8")
    file_bytes = image_path.read_bytes()
    body = body_prefix + file_bytes + body_suffix

    request = urllib.request.Request(
        "https://catbox.moe/user/api.php",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "ExcaliburBlogHero/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        url = response.read().decode("utf-8", errors="replace").strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"catbox upload failed: {url[:200]}")
    return url


def upload_0x0(image_path: Path) -> str:
    boundary = "----ExcaliburHero0x0"
    body_prefix = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{image_path.name}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8")
    body_suffix = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = body_prefix + image_path.read_bytes() + body_suffix
    request = urllib.request.Request(
        "https://0x0.st",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "ExcaliburBlogHero/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        url = response.read().decode("utf-8", errors="replace").strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"0x0 upload failed: {url[:200]}")
    return url


def resolve_reference_path(root: Path, hero: dict) -> Path:
    rel = hero.get("reference_image") or "memory/cover/assets/victoria-character-sheet-2k.png"
    path = Path(rel)
    if not path.is_absolute():
        path = root / path
    return path


def git_safe_hero_url(url: str) -> str:
    """Prefer {{SITE_BASE}}/wp-content/... for committed blog-hero.json."""
    value = (url or "").strip()
    if not value:
        return value
    if value.startswith(SITE_BASE_PLACEHOLDER):
        return value
    safe = to_git_safe_site_url(value)
    if safe.startswith(SITE_BASE_PLACEHOLDER):
        return safe
    if REDACTED_LITERAL in value:
        # Legacy tool-mask host → keep media path under placeholder.
        rest = value.split(REDACTED_LITERAL, 1)[1]
        if not rest.startswith("/"):
            rest = "/" + rest
        return f"{SITE_BASE_PLACEHOLDER}{rest}"
    if "://" in value and "/wp-content/" in value:
        path = urlparse(value).path or "/"
        return f"{SITE_BASE_PLACEHOLDER}{path}"
    return value


def normalize_existing_hero_url(hero: dict, hero_path: Path) -> str | None:
    """Rewrite [REDACTED] or live site host to {{SITE_BASE}} in place when possible."""
    existing = (hero.get("reference_url_hosted") or "").strip()
    if not existing:
        return None
    safe = git_safe_hero_url(existing)
    if safe != existing:
        hero["reference_url_hosted"] = safe
        hero["reference_url_updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        save_json(hero_path, hero)
    return safe


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hero-json", default="memory/cover/blog-hero.json")
    ap.add_argument("--force", action="store_true", help="Re-upload even if URL exists")
    ap.add_argument("--provider", choices=("catbox", "0x0", "auto"), default="auto")
    args = ap.parse_args()

    root = project_root()
    hero_path = Path(args.hero_json)
    if not hero_path.is_absolute():
        hero_path = root / hero_path
    if not hero_path.is_file():
        print(f"❌ HERO BLOCKER: missing {hero_path}", file=sys.stderr)
        return 1

    hero = load_json(hero_path)
    ref_path = resolve_reference_path(root, hero)
    if not ref_path.is_file():
        print(f"❌ HERO BLOCKER: reference image not found: {ref_path}", file=sys.stderr)
        return 1

    existing = normalize_existing_hero_url(hero, hero_path)
    if existing and not args.force:
        # Expand for agent visibility only; file stays git-safe.
        live = resolve_public_base_from_env()
        shown = expand_site_base(existing, live) if live and SITE_BASE_PLACEHOLDER in existing else existing
        print(f"OK reference_url_hosted={existing}")
        if shown != existing:
            print(f"OK runtime_expand_available=yes")
        return 0

    env_url = os.environ.get("BLOG_HERO_REFERENCE_URL", "").strip()
    if env_url:
        safe = git_safe_hero_url(env_url)
        hero["reference_url_hosted"] = safe
        hero["reference_url_source"] = "env:BLOG_HERO_REFERENCE_URL"
        hero["reference_url_updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        save_json(hero_path, hero)
        print(f"OK reference_url_hosted={safe}")
        return 0

    providers = ["catbox", "0x0"] if args.provider == "auto" else [args.provider]
    last_error: Exception | None = None
    for provider in providers:
        try:
            url = upload_catbox(ref_path) if provider == "catbox" else upload_0x0(ref_path)
            # Third-party hosts are not PUBLIC_SITE_URL; keep as-is (not secret-scanned site base).
            hero["reference_url_hosted"] = url
            hero["reference_url_source"] = provider
            hero["reference_url_updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            save_json(hero_path, hero)
            print(f"OK reference_url_hosted={url}")
            return 0
        except (urllib.error.URLError, RuntimeError, TimeoutError) as exc:
            last_error = exc
            print(f"WARN upload via {provider} failed: {exc}", file=sys.stderr)

    print(f"❌ HERO BLOCKER: could not host reference: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
