#!/usr/bin/env python3
"""Upload → approve → publish one article to the tenant site (not Hall, not WP).

After GATE PASS the swarm calls this script. Token comes only from env /
Cursor Cloud Secret. Missing token → SKIP «нет ключа», exit 0.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import tarfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin

from excalibur_blog_opening_editorial import (
    live_double_lead_errors,
    sanitize_site_meta,
)
from excalibur_blog_pipeline_canon import validate_article_canon
from excalibur_blog_site_base import (
    SITE_BASE_PLACEHOLDER,
    normalize_public_base,
    redact_site_base,
    redact_structure,
)
from excalibur_repo_paths import repo_relative

TOKEN_ENV_NAMES = (
    "SITE_PUBLISH_TOKEN",
    "HALL_PUBLISH_TOKEN",
    "PUBLISH_TOKEN",
    "TARO_SITE_TOKEN",
)
DEFAULT_SITE_BASE = "https://www.xn--80aaoqxlidb0d.xn--p1ai"
PROTECTED_LIVE_TOPIC_IDS = frozenset({"B21", "B22"})
RASKLAD_PATH = "/rasklad-taro-online/"
TGZ_MEMBERS = (
    "article.html",
    "article.meta.json",
    "description-brief.json",
    "cover/cover.png",
    "cover/inline-01.png",
    "cover/inline-02.png",
    "cover/inline-03.png",
)
INLINE_SLOTS = ("inline_1", "inline_2", "inline_3")
COVER_HERO_RE = re.compile(
    r"<figure\b(?=[^>]*\bclass=['\"][^'\"]*\bcover-hero\b)[^>]*>.*?</figure>\s*",
    re.I | re.S,
)
COVER_PNG_FIGURE_RE = re.compile(
    r"<figure\b[^>]*>[\s\S]*?</figure>",
    re.I,
)
TELEGRAM_HREF_RE = re.compile(
    r"""href\s*=\s*(['"])(https?://(?:t\.me|telegram\.me)/[^'"]+)\1""",
    re.I,
)
UA = "ExcaliburBlogSitePublish/1.0"


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def resolve_site_base(env: dict[str, str] | None = None, override: str = "") -> str:
    if override.strip():
        return normalize_public_base(override)
    merged = env or {}
    return normalize_public_base(
        merged.get("PUBLIC_SITE_URL")
        or merged.get("WP_HOME")
        or merged.get("WP_SITE_URL")
        or DEFAULT_SITE_BASE
    )


def resolve_publish_token(env: dict[str, str] | None = None) -> tuple[str, str]:
    """Return (env_name, token). Token value is never logged by callers.

    Only ``os.environ`` (Cursor Cloud Secret → env). Not site.env.local.
    """
    source = env if env is not None else os.environ
    for name in TOKEN_ENV_NAMES:
        value = str(source.get(name) or "").strip()
        if value:
            return name, value
    return "", ""


def redact_secrets(text: str, token: str = "") -> str:
    out = str(text or "")
    secret = (token or "").strip()
    if secret and secret in out:
        out = out.replace(secret, "<redacted>")
    for name in TOKEN_ENV_NAMES:
        # Never echo ``NAME=value`` even if a caller concatenated env dumps.
        out = re.sub(rf"{re.escape(name)}\s*=\s*\S+", f"{name}=<redacted>", out)
    return out


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def article_topic_id(article_dir: Path) -> str:
    meta = load_json(article_dir / "article.meta.json") if (article_dir / "article.meta.json").is_file() else {}
    return str(meta.get("topic_id") or "").strip().upper()


def article_slug(article_dir: Path) -> str:
    meta = load_json(article_dir / "article.meta.json") if (article_dir / "article.meta.json").is_file() else {}
    return str(meta.get("slug") or "").strip().strip("/")


def strip_cover_hero(html: str) -> tuple[str, int]:
    """Remove figure.cover-hero. cover.png stays a file, not a body figure."""
    cleaned, n = COVER_HERO_RE.subn("", html or "")
    return cleaned, n


def strip_cover_png_body_figures(html: str) -> tuple[str, int]:
    """Drop body <figure> whose img is cover.png (second cover). Keep inlines."""

    def _keep(match: re.Match[str]) -> str:
        block = match.group(0)
        if re.search(r"\bcover-hero\b", block, flags=re.I):
            return ""
        src = re.search(r"""<img\b[^>]*\bsrc\s*=\s*['"]([^'"]+)['"]""", block, flags=re.I)
        if not src:
            return block
        name = Path(src.group(1).split("?", 1)[0]).name.lower()
        if name == "cover.png":
            return ""
        return block

    cleaned, n = COVER_PNG_FIGURE_RE.subn(_keep, html or "")
    # subn counts all figures; recount removals from length/content change
    removed = html.count("<figure") - cleaned.count("<figure") if html else 0
    return cleaned, max(removed, 0)


def prepare_site_html(html: str) -> tuple[str, dict[str, int]]:
    out, hero_n = strip_cover_hero(html)
    out, cover_n = strip_cover_png_body_figures(out)
    return out, {"cover_hero_removed": hero_n, "cover_png_figures_removed": cover_n}


def collect_telegram_hrefs(html: str) -> list[str]:
    return [m.group(2) for m in TELEGRAM_HREF_RE.finditer(html or "")]


def rewrite_rasklad_back_to_telegram(live_html: str, telegram_hrefs: list[str]) -> str:
    """If the site swapped t.me → /rasklad-taro-online/, put t.me back (round-robin)."""
    hrefs = [h for h in telegram_hrefs if h]
    if not hrefs or RASKLAD_PATH not in (live_html or ""):
        return live_html
    idx = 0

    def _swap(match: re.Match[str]) -> str:
        nonlocal idx
        href = hrefs[idx % len(hrefs)]
        idx += 1
        quote = match.group(1)
        return f"href={quote}{href}{quote}"

    return re.sub(
        rf"""href\s*=\s*(['"]){re.escape(RASKLAD_PATH)}\1""",
        _swap,
        live_html or "",
        flags=re.I,
    )


def telegram_rewritten_to_rasklad(source_html: str, live_html: str) -> list[str]:
    errors: list[str] = []
    wanted = collect_telegram_hrefs(source_html)
    if not wanted:
        return errors
    live = live_html or ""
    missing = [href for href in wanted if href not in live]
    if missing and RASKLAD_PATH in live:
        errors.append(
            "live page replaced t.me with /rasklad-taro-online/ "
            f"(missing {len(missing)} telegram href(s))"
        )
    elif missing:
        errors.append(f"live page dropped {len(missing)} t.me href(s)")
    return errors


def live_second_cover_errors(live_html: str) -> list[str]:
    html = live_html or ""
    errors: list[str] = []
    if re.search(r"<figure\b[^>]*\bcover-hero\b", html, flags=re.I):
        errors.append("live body still has figure.cover-hero (second cover)")
    article = re.search(
        r"<article\b[^>]*>([\s\S]*?)</article>",
        html,
        flags=re.I,
    )
    body = article.group(1) if article else html
    # Page hero (seo-article__cover) may show cover.png once. Extra body figure = second cover.
    body_cover_figs = 0
    for block in COVER_PNG_FIGURE_RE.findall(body):
        if re.search(r"\bseo-article__cover\b", block, flags=re.I):
            continue
        if re.search(r"""src\s*=\s*['"][^'"]*cover\.png""", block, flags=re.I):
            body_cover_figs += 1
    if body_cover_figs:
        errors.append(f"live body has {body_cover_figs} extra cover.png figure(s)")
    return errors


def inline_slot_errors(html: str) -> list[str]:
    errors: list[str] = []
    for slot in INLINE_SLOTS:
        n = (html or "").count(f'data-slot="{slot}"')
        if n != 1:
            errors.append(f"article.html requires exactly one {slot} slot, found {n}")
    return errors


def payload_errors(article_dir: Path, site_html: str) -> list[str]:
    errors: list[str] = []
    for rel in TGZ_MEMBERS:
        if rel == "article.html":
            if len(site_html) < 200:
                errors.append("article.html missing or too small after cover-hero strip")
            continue
        path = article_dir / rel
        if not path.is_file() or path.stat().st_size < 8:
            errors.append(f"{rel} missing or too small")
    errors.extend(inline_slot_errors(site_html))
    if COVER_HERO_RE.search(site_html):
        errors.append("figure.cover-hero still present after strip")
    return errors


def build_tgz_bytes(article_dir: Path, site_html: str) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for rel in TGZ_MEMBERS:
            if rel == "article.html":
                data = site_html.encode("utf-8")
            elif rel == "article.meta.json":
                meta = sanitize_site_meta(load_json(article_dir / rel) if (article_dir / rel).is_file() else {})
                data = (json.dumps(meta, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            else:
                data = (article_dir / rel).read_bytes()
            info = tarfile.TarInfo(name=rel)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def tgz_member_names(data: bytes) -> list[str]:
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        return [m.name for m in tar.getmembers() if m.isfile()]


@dataclass
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes
    url: str

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def json(self) -> Any:
        raw = self.text().strip()
        if not raw:
            return {}
        return json.loads(raw)


HttpFn = Callable[..., HttpResponse]


def _default_http(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout: float = 30,
) -> HttpResponse:
    req = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers=headers or {},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return HttpResponse(
                status=int(resp.status),
                headers={k.lower(): v for k, v in resp.headers.items()},
                body=resp.read(),
                url=str(resp.geturl()),
            )
    except urllib.error.HTTPError as exc:
        body = exc.read() if exc.fp else b""
        return HttpResponse(
            status=int(exc.code),
            headers={k.lower(): v for k, v in (exc.headers.items() if exc.headers else [])},
            body=body,
            url=url,
        )


def auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "X-Publish-Token": token,
        "User-Agent": UA,
        "Accept": "application/json, text/plain, */*",
    }


def encode_tgz_multipart(tgz: bytes, field: str = "tgz") -> tuple[bytes, str]:
    boundary = "----ExcaliburSitePublishBoundary7f3a9c"
    crlf = b"\r\n"
    parts = [
        f"--{boundary}".encode("ascii"),
        crlf,
        f'Content-Disposition: form-data; name="{field}"; filename="article.tgz"'.encode("ascii"),
        crlf,
        b"Content-Type: application/gzip",
        crlf,
        crlf,
        tgz,
        crlf,
        f"--{boundary}--".encode("ascii"),
        crlf,
    ]
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def extract_article_id(payload: Any) -> str:
    if isinstance(payload, dict):
        for key in ("id", "article_id", "articleId"):
            value = payload.get(key)
            if value not in (None, ""):
                return str(value)
        for nested_key in ("article", "data", "result"):
            nested = payload.get(nested_key)
            found = extract_article_id(nested)
            if found:
                return found
    if isinstance(payload, list):
        for item in payload:
            found = extract_article_id(item)
            if found:
                return found
    return ""


def extract_permalink(payload: Any, site_base: str, slug: str) -> str:
    if isinstance(payload, dict):
        for key in ("url", "permalink", "canonical", "public_url", "href"):
            value = str(payload.get(key) or "").strip()
            if value.startswith("http://") or value.startswith("https://"):
                return value
            if value.startswith("/"):
                return site_base.rstrip("/") + value
        for nested_key in ("article", "data", "result"):
            found = extract_permalink(payload.get(nested_key), site_base, slug)
            if found:
                return found
    if slug:
        return f"{site_base.rstrip('/')}/blog/{slug.strip('/')}/"
    return ""


def check_site_gates(article_dir: Path, root: Path, site_html: str) -> list[str]:
    blockers = payload_errors(article_dir, site_html)
    blockers.extend(validate_article_canon(article_dir, root))
    return blockers


def write_result(article_dir: Path, result: dict[str, Any], site_base: str) -> Path:
    safe = redact_structure(result, site_base)
    path = article_dir / "site-publish-result.json"
    path.write_text(json.dumps(safe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _safe_print(text: str, token: str) -> None:
    print(redact_secrets(text, token))


def _request_json(
    http: HttpFn,
    method: str,
    url: str,
    token: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 45,
) -> tuple[HttpResponse, Any]:
    hdrs = auth_headers(token)
    if headers:
        hdrs.update(headers)
    resp = http(method, url, headers=hdrs, data=data, timeout=timeout)
    payload: Any = {}
    try:
        payload = resp.json()
    except json.JSONDecodeError:
        payload = {"raw": redact_secrets(resp.text()[:400], token)}
    return resp, payload


def fetch_live(http: HttpFn, permalink: str) -> HttpResponse:
    return http(
        "GET",
        permalink,
        headers={"User-Agent": UA, "Accept": "text/html"},
        data=None,
        timeout=25,
    )


def patch_on_page_excerpt_empty(
    http: HttpFn,
    site_base: str,
    token: str,
    article_id: str,
) -> HttpResponse:
    """Theme prints excerpt as p.seo-article__lead. Never send first-paragraph copy."""
    patch_url = urljoin(site_base.rstrip("/") + "/", f"api/admin/content/articles/{article_id}")
    patch_body = json.dumps({"excerpt": "", "on_page_excerpt": False}, ensure_ascii=False).encode("utf-8")
    resp, _ = _request_json(
        http,
        "PATCH",
        patch_url,
        token,
        data=patch_body,
        headers={"Content-Type": "application/json"},
    )
    return resp


def run_publish(
    *,
    article_dir: Path,
    root: Path,
    env: dict[str, str],
    site_base: str,
    dry_run: bool,
    skip_gates: bool,
    http: HttpFn,
    resume_article_id: str = "",
) -> tuple[int, dict[str, Any]]:
    html_path = article_dir / "article.html"
    raw_html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    site_html, strip_info = prepare_site_html(raw_html)
    topic_id = article_topic_id(article_dir)
    slug = article_slug(article_dir)
    token_name, token = resolve_publish_token(env)

    result: dict[str, Any] = {
        "topic_id": topic_id,
        "slug": slug,
        "publish_method": "site-api",
        "hall": "not_used",
        "dzen_studio": "not_used",
        "token_env": token_name or None,
        "token_configured": bool(token),
        "cover_hero_stripped": strip_info["cover_hero_removed"] > 0
        or strip_info["cover_png_figures_removed"] > 0,
        "strip": strip_info,
        "gate": "PASS",
        "publish": "SKIP",
        "verdict": "skip",
        "reason": "",
        "permalink": f"{SITE_BASE_PLACEHOLDER}/blog/{slug}/" if slug else "",
    }

    if not skip_gates:
        blockers = check_site_gates(article_dir, root, site_html)
        if blockers:
            result["gate"] = "FAIL"
            result["verdict"] = "fail"
            result["publish"] = "SKIP"
            result["reason"] = "gate_fail"
            result["blockers"] = blockers
            write_result(article_dir, result, site_base)
            return 2, result
    result["gate"] = "PASS"

    if topic_id in PROTECTED_LIVE_TOPIC_IDS:
        result["verdict"] = "skip"
        result["publish"] = "SKIP"
        result["reason"] = f"{topic_id} live protected"
        result["protected_live"] = topic_id
        write_result(article_dir, result, site_base)
        return 0, result

    tgz = build_tgz_bytes(article_dir, site_html)
    result["tgz_members"] = tgz_member_names(tgz)
    result["tgz_bytes"] = len(tgz)

    if dry_run:
        result["verdict"] = "pass" if token else "skip"
        result["publish"] = "DRY_RUN" if token else "SKIP"
        result["reason"] = "" if token else "нет ключа"
        result["dry_run"] = True
        result["on_page_excerpt"] = ""
        write_result(article_dir, result, site_base)
        return 0, result

    if not token:
        result["verdict"] = "skip"
        result["publish"] = "SKIP"
        result["reason"] = "нет ключа"
        write_result(article_dir, result, site_base)
        return 0, result

    article_id = str(resume_article_id or "").strip()
    if article_id:
        result["article_id"] = article_id
        result["upload_status"] = "resumed"
        result["resumed"] = True
    else:
        upload_url = urljoin(site_base.rstrip("/") + "/", "api/admin/content/excalibur/upload")
        body, content_type = encode_tgz_multipart(tgz)
        upload_headers = auth_headers(token)
        upload_headers["Content-Type"] = content_type
        upload_resp, upload_payload = _request_json(
            http,
            "POST",
            upload_url,
            token,
            data=body,
            headers=upload_headers,
            timeout=60,
        )
        result["upload_status"] = upload_resp.status
        article_id = extract_article_id(upload_payload)
        result["article_id"] = article_id
        if upload_resp.status >= 400 or not article_id:
            result["verdict"] = "fail"
            result["publish"] = "FAIL"
            result["reason"] = f"upload status={upload_resp.status}"
            write_result(article_dir, result, site_base)
            return 1, result

    excerpt_resp = patch_on_page_excerpt_empty(http, site_base, token, article_id)
    result["excerpt_clear_status"] = excerpt_resp.status
    if excerpt_resp.status == 403:
        # Hall token can upload/approve/publish, but not PATCH article fields.
        result["excerpt_clear_skipped"] = "hall_token_no_patch"
    elif excerpt_resp.status >= 400:
        result["verdict"] = "fail"
        result["publish"] = "FAIL"
        result["reason"] = f"excerpt clear status={excerpt_resp.status}"
        write_result(article_dir, result, site_base)
        return 1, result

    for action in ("approve", "publish"):
        action_url = urljoin(
            site_base.rstrip("/") + "/",
            f"api/admin/content/articles/{article_id}/{action}",
        )
        resp, payload = _request_json(
            http,
            "POST",
            action_url,
            token,
            data=b"{}",
            headers={"Content-Type": "application/json"},
        )
        result[f"{action}_status"] = resp.status
        if resp.status >= 400:
            detail = ""
            if isinstance(payload, dict):
                detail = str(payload.get("detail") or payload.get("error") or "")
            result[f"{action}_detail"] = detail
            # 409 "already approved" can continue. Quality-review 409 cannot publish.
            if action == "approve" and resp.status == 409 and "одобрен" in detail.lower():
                pass
            else:
                result["verdict"] = "fail"
                result["publish"] = "FAIL"
                result["reason"] = f"{action} status={resp.status}"
                if detail:
                    result["reason_detail"] = detail
                write_result(article_dir, result, site_base)
                return 1, result
        permalink_guess = extract_permalink(payload, site_base, slug)
        if permalink_guess:
            result["permalink_live"] = permalink_guess

    permalink = str(result.get("permalink_live") or extract_permalink({}, site_base, slug))
    result["permalink"] = redact_site_base(permalink, site_base)

    live_resp = fetch_live(http, permalink)
    result["live_status"] = live_resp.status
    if live_resp.status >= 400:
        result["verdict"] = "fail"
        result["publish"] = "FAIL"
        result["reason"] = f"live fetch status={live_resp.status}"
        write_result(article_dir, result, site_base)
        return 1, result

    live_html = live_resp.text()
    tg_errors = telegram_rewritten_to_rasklad(site_html, live_html)
    if tg_errors:
        patch_url = urljoin(
            site_base.rstrip("/") + "/",
            f"api/admin/content/articles/{article_id}",
        )
        patch_body = json.dumps(
            {"html": site_html, "preserve_telegram": True},
            ensure_ascii=False,
        ).encode("utf-8")
        patch_resp, _ = _request_json(
            http,
            "PATCH",
            patch_url,
            token,
            data=patch_body,
            headers={"Content-Type": "application/json"},
        )
        result["telegram_restore_status"] = patch_resp.status
        live_resp = fetch_live(http, permalink)
        live_html = live_resp.text()
        tg_errors = telegram_rewritten_to_rasklad(site_html, live_html)
        if tg_errors:
            result["verdict"] = "fail"
            result["publish"] = "FAIL"
            result["reason"] = "t.me rewritten to /rasklad-taro-online/"
            result["live_errors"] = tg_errors
            write_result(article_dir, result, site_base)
            return 1, result
        result["telegram_restored"] = True

    cover_errors = live_second_cover_errors(live_html)
    if cover_errors:
        result["verdict"] = "fail"
        result["publish"] = "FAIL"
        result["reason"] = "second cover on live"
        result["live_errors"] = cover_errors
        write_result(article_dir, result, site_base)
        return 1, result

    lead_errors = live_double_lead_errors(live_html)
    if lead_errors:
        retry = patch_on_page_excerpt_empty(http, site_base, token, article_id)
        result["excerpt_clear_retry_status"] = retry.status
        live_resp = fetch_live(http, permalink)
        live_html = live_resp.text()
        lead_errors = live_double_lead_errors(live_html)
        if lead_errors:
            result["verdict"] = "fail"
            result["publish"] = "FAIL"
            result["reason"] = "double lead on live (seo-article__lead clones first p)"
            result["live_errors"] = lead_errors
            write_result(article_dir, result, site_base)
            return 1, result
        result["double_lead_cleared"] = True

    result["verdict"] = "pass"
    result["publish"] = "PUBLISHED"
    result["reason"] = ""
    result["live_ok"] = True
    write_result(article_dir, result, site_base)
    return 0, result


def publish_env_report(env: dict[str, str]) -> dict[str, Any]:
    name, token = resolve_publish_token(env)
    return {
        "token_configured": bool(token),
        "token_env": name or None,
        "token_env_order": list(TOKEN_ENV_NAMES),
        "site_base_configured": bool(resolve_site_base(env)),
        "hall_upload": False,
        "dzen_studio": False,
        "protected_live_topics": sorted(PROTECTED_LIVE_TOPIC_IDS),
    }


def main(argv: list[str] | None = None, http: HttpFn | None = None) -> int:
    parser = argparse.ArgumentParser(description="Site API publish after GATE PASS (not Hall)")
    parser.add_argument("--article-dir", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--env-check", action="store_true")
    parser.add_argument("--site-base", default="")
    parser.add_argument("--skip-gates", action="store_true")
    parser.add_argument(
        "--resume-article-id",
        default="",
        help="Skip upload and continue approve/publish for an already uploaded article",
    )
    args = parser.parse_args(argv)

    root = project_root()
    env = {key: str(os.environ.get(key) or "") for key in (
        *TOKEN_ENV_NAMES,
        "PUBLIC_SITE_URL",
        "WP_HOME",
        "WP_SITE_URL",
    )}
    site_base = resolve_site_base(env, args.site_base)
    token_name, token = resolve_publish_token(env)

    if args.env_check:
        print(json.dumps(publish_env_report(env), ensure_ascii=False, indent=2))
        return 0

    if args.article_dir is None:
        print("--article-dir is required unless --env-check", file=sys.stderr)
        return 2

    article_dir = args.article_dir if args.article_dir.is_absolute() else root / args.article_dir
    try:
        code, result = run_publish(
            article_dir=article_dir,
            root=root,
            env=env,
            site_base=site_base,
            dry_run=bool(args.dry_run),
            skip_gates=bool(args.skip_gates),
            http=http or _default_http,
            resume_article_id=str(args.resume_article_id or ""),
        )
    except Exception as exc:  # noqa: BLE001 — surface type only, never secret
        _safe_print(f"BLOCKER: site publish crashed: {type(exc).__name__}: {exc}", token)
        return 1

    verdict = str(result.get("verdict") or "")
    reason = str(result.get("reason") or "")
    if verdict == "skip" and reason == "нет ключа":
        _safe_print("SKIP publish: нет ключа (GATE PASS, pipeline continues)", token)
    elif verdict == "skip" and "B21" in reason:
        _safe_print("SKIP publish: B21 live protected", token)
    elif verdict == "pass" and result.get("dry_run"):
        _safe_print(
            f"OK dry-run site-publish topic={result.get('topic_id')} slug={result.get('slug')}",
            token,
        )
    elif verdict == "pass":
        _safe_print(
            f"OK site-publish article_id={result.get('article_id')} "
            f"permalink={result.get('permalink')}",
            token,
        )
    else:
        _safe_print(
            f"FAIL site-publish reason={reason} report={repo_relative(article_dir / 'site-publish-result.json', root)}",
            token,
        )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
