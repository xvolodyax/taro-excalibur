#!/usr/bin/env python3
"""Call OpenAI Chat Completions (gpt-5.5) for Excalibur air text.

FAIL ONLY: missing OPENAI_API_KEY or API error → non-zero exit, no invented text.
Stamp author: openai-api-gpt-5.5
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
DEFAULT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
AUTHOR_STAMP = "openai-api-gpt-5.5"


def fail(msg: str, code: int = 2) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(code)


def read_text(path: str | None, inline: str | None) -> str:
    if path:
        p = Path(path)
        if not p.is_file():
            fail(f"file not found: {path}")
        return p.read_text(encoding="utf-8")
    return inline or ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    ap.add_argument("--system", default="", help="System prompt inline")
    ap.add_argument("--system-file", default="", help="System prompt file")
    ap.add_argument("--user", default="", help="User prompt inline")
    ap.add_argument("--user-file", default="", help="User prompt file")
    ap.add_argument("--out", default="", help="Write assistant text here")
    ap.add_argument("--raw-out", default="", help="Write full JSON response here")
    ap.add_argument("--max-completion-tokens", type=int, default=8192)
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not key:
        fail("OPENAI_API_KEY missing — text roles cannot run. Do not write with Cursor model.")

    system = read_text(args.system_file or None, args.system).strip()
    user = read_text(args.user_file or None, args.user).strip()
    if not user:
        fail("empty user prompt")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    payload = {
        "model": args.model,
        "messages": messages,
        "max_completion_tokens": int(args.max_completion_tokens),
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        args.endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "ExcaliburBlogChatCompletions/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read().decode("utf-8")
            status = getattr(resp, "status", 200)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")[:2000]
        fail(f"OpenAI HTTP {exc.code}: {err_body}")
    except urllib.error.URLError as exc:
        fail(f"OpenAI network error: {exc}")
    except TimeoutError:
        fail("OpenAI timeout")

    if status >= 400:
        fail(f"OpenAI HTTP {status}: {raw[:2000]}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"OpenAI JSON decode error: {exc}")

    if args.raw_out:
        Path(args.raw_out).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    err = data.get("error")
    if err:
        fail(f"OpenAI API error: {err}")

    choices = data.get("choices") or []
    if not choices:
        fail("OpenAI returned no choices")
    message = (choices[0] or {}).get("message") or {}
    text = (message.get("content") or "").strip()
    if not text:
        fail("OpenAI empty assistant content")

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")

    print(text)
    print(f"written_by={AUTHOR_STAMP} model={args.model}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
