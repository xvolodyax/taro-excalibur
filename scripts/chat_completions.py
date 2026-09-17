#!/usr/bin/env python3
"""Call OpenAI Chat Completions. Article text author = openai-api-gpt-5.5.

HARD (slot 17.09+): Title / Writer / Sol / Description / Cover-text go through
this script only. Director / Cursor catalog must not write the article.

No key or HTTP 401 → exit 2 (FAIL). Never print the key.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "gpt-5.5"
DEFAULT_URL = "https://api.openai.com/v1/chat/completions"
WRITTEN_BY = "openai-api-gpt-5.5"
UA = "ExcaliburBlogOpenAI/1.0"


def load_key() -> str:
    return str(os.environ.get("OPENAI_API_KEY") or "").strip()


def read_text(path: str | None, inline: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return inline or ""


def chat_completions(
    *,
    model: str,
    system: str,
    user: str,
    max_completion_tokens: int,
    timeout: int,
) -> dict:
    key = load_key()
    if not key:
        raise SystemExit("FAIL: OPENAI_API_KEY missing — text roles stop, no self-write")

    url = (os.environ.get("OPENAI_BASE_URL") or DEFAULT_URL).strip()
    messages: list[dict[str, str]] = []
    if system.strip():
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    payload: dict = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_completion_tokens,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", "replace")[:800]
        if exc.code == 401:
            raise SystemExit(
                "FAIL: OpenAI API 401 — text roles stop, no self-write"
            ) from exc
        raise SystemExit(f"FAIL: OpenAI API HTTP {exc.code}: {err_body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"FAIL: OpenAI API network: {type(exc).__name__}") from exc
    return body


def extract_text(body: dict) -> str:
    choices = body.get("choices") or []
    if not choices:
        raise SystemExit(f"FAIL: OpenAI API empty choices: {json.dumps(body, ensure_ascii=False)[:400]}")
    msg = (choices[0] or {}).get("message") or {}
    content = msg.get("content")
    if isinstance(content, str) and content.strip():
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") in {"text", "output_text"}:
                parts.append(str(item.get("text") or ""))
            elif isinstance(item, str):
                parts.append(item)
        text = "".join(parts).strip()
        if text:
            return text
    raise SystemExit(
        "FAIL: OpenAI API returned no text "
        f"(finish={choices[0].get('finish_reason')!r})"
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--system", default="")
    ap.add_argument("--system-file", default="")
    ap.add_argument("--user", default="")
    ap.add_argument("--user-file", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--meta-out", default="")
    ap.add_argument("--max-completion-tokens", type=int, default=8000)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()

    if not load_key():
        print("FAIL: OPENAI_API_KEY missing — text roles stop, no self-write", file=sys.stderr)
        return 2

    system = read_text(args.system_file or None, args.system)
    if args.probe:
        user = "Reply with exactly: OK"
        system = "You are a connectivity probe. Reply with exactly OK."
        max_tokens = 32
    else:
        user = read_text(args.user_file or None, args.user)
        max_tokens = args.max_completion_tokens
        if not user.strip():
            print("FAIL: empty user prompt", file=sys.stderr)
            return 2

    body = chat_completions(
        model=args.model,
        system=system,
        user=user,
        max_completion_tokens=max_tokens,
        timeout=args.timeout,
    )
    text = extract_text(body)
    usage = body.get("usage") or {}
    meta = {
        "written_by": WRITTEN_BY,
        "model": args.model,
        "id": body.get("id"),
        "usage": {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
        },
    }
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text if text.endswith("\n") else text + "\n")
    if args.meta_out:
        Path(args.meta_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.meta_out).write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.probe:
        print(f"PROBE_OK written_by={WRITTEN_BY} model={args.model} id={body.get('id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
