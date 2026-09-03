#!/usr/bin/env python3
"""Cover identity gate — host face/hair lock from tenant blog-hero.json.

Tenant check (always):
- host_reference must lock hair color to the reference photo;
- required Cover prompt phrase present;
- lock must not prescribe platinum / ice-blonde as the look.

Article check (--article-dir):
- quad prompt / batch must contain the required hair phrase;
- prompt must not instruct platinum / ice-blonde / lighten as the hair look
  (negations like «no platinum» / «do not lighten» are allowed).

Platinum or strongly lighter hair on a generated cover = rebuild canvas
(COVER IDENTITY BLOCKER). Do not inpaint hair outside the quad.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_HAIR_PHRASE = (
    "hair color copied exactly from reference photo, same root depth, "
    "do not lighten, no platinum"
)

# Positive look instructions that mean the model should paint platinum/ice hair.
FORBIDDEN_LOOK = (
    r"(?<!no )(?<!not )(?<!never )platinum(?:\s+blonde)?",
    r"ice[-\s]?blonde",
    r"white blonde",
    r"bleach(?:ed)?\s+hair",
    r"lighten(?:ed)?\s+(?:the\s+)?(?:hair|roots|blonde)",
)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _hair_lock(hero: dict) -> dict:
    lock = hero.get("hair_color_lock")
    if not isinstance(lock, dict):
        lock = (hero.get("visual_lock") or {}).get("hair_color_lock")
    return lock if isinstance(lock, dict) else {}


def _prescribes_forbidden_look(text: str) -> list[str]:
    hits: list[str] = []
    blob = text or ""
    for pat in FORBIDDEN_LOOK:
        if re.search(pat, blob, flags=re.I):
            hits.append(pat)
    return hits


def validate_tenant(hero: dict, *, cover_mode: str) -> list[str]:
    errors: list[str] = []
    if cover_mode != "host_reference":
        return errors
    lock = _hair_lock(hero)
    prompt = str(lock.get("prompt") or "").strip()
    if REQUIRED_HAIR_PHRASE not in prompt:
        errors.append(
            f"hair_color_lock.prompt must contain exactly: {REQUIRED_HAIR_PHRASE!r}"
        )
    hair = str((hero.get("visual_lock") or {}).get("hair") or "")
    fragment = str(hero.get("prompt_fragment") or "")
    for field, text in (("visual_lock.hair", hair), ("prompt_fragment", fragment)):
        if re.search(r"\bplatinum\b", text, flags=re.I) and not re.search(
            r"\b(?:no|not|never)\s+platinum\b", text, flags=re.I
        ):
            errors.append(f"{field} prescribes platinum — lock must copy the reference")
        if re.search(r"ice[-\s]?blonde", text, flags=re.I) and not re.search(
            r"\b(?:no|not|never)\s+ice", text, flags=re.I
        ):
            errors.append(f"{field} prescribes ice-blonde — lock must copy the reference")
    return errors


def _strip_negation_windows(text: str) -> str:
    """Drop lock phrase and Ban/Neg lines so only positive look instructions remain."""
    blob = (text or "").replace(REQUIRED_HAIR_PHRASE, " ")
    blob = re.sub(
        r"\b(?:ban|neg|negative|запрещ\w*)[:\s][^\n]{0,400}",
        " ",
        blob,
        flags=re.I,
    )
    blob = re.sub(
        r"\b(?:no|not|never|do not|don't|не)\b[\w\s,/-]{0,40}\b"
        r"(?:platinum|ice[- ]blonde|white blonde|bleach|lighten)",
        " ",
        blob,
        flags=re.I,
    )
    return blob


def validate_prompt(prompt: str) -> list[str]:
    errors: list[str] = []
    text = prompt or ""
    if REQUIRED_HAIR_PHRASE not in text:
        errors.append(f"Cover prompt missing hair lock phrase: {REQUIRED_HAIR_PHRASE!r}")
    look = _strip_negation_windows(text)
    if re.search(r"\bplatinum blonde\b", look, flags=re.I):
        errors.append("Cover prompt instructs platinum blonde")
    for pat in _prescribes_forbidden_look(look):
        errors.append(f"Cover prompt paints forbidden hair look ({pat})")
    return errors


def collect_article_prompt(article_dir: Path) -> str:
    chunks: list[str] = []
    txt = article_dir / "cover" / "quad-mcp-prompt.txt"
    if txt.is_file():
        chunks.append(txt.read_text(encoding="utf-8"))
    batch = article_dir / "cover" / "quad-mcp-batch.json"
    if batch.is_file():
        try:
            data = load_json(batch)
            jobs = data.get("jobs") or []
            if jobs:
                args = jobs[0].get("mcp_args") or jobs[0].get("api_args") or {}
                chunks.append(str(args.get("prompt") or args.get("input", {}).get("prompt") or ""))
        except json.JSONDecodeError:
            errors_note = "quad-mcp-batch.json invalid JSON"
            chunks.append(errors_note)
    return "\n".join(chunks)


def run_gate(*, root: Path, article_dir: Path | None) -> dict:
    errors: list[str] = []
    hero_path = root / "memory/cover/blog-hero.json"
    tenant_path = root / "shared/tenant-config.json"
    hero = load_json(hero_path) if hero_path.is_file() else {}
    tenant = load_json(tenant_path) if tenant_path.is_file() else {}
    cover_mode = str(hero.get("cover_mode") or tenant.get("cover_mode") or "").strip()
    errors.extend(validate_tenant(hero, cover_mode=cover_mode))
    prompt = ""
    if article_dir is not None:
        prompt = collect_article_prompt(article_dir)
        if not prompt.strip():
            errors.append("article cover prompt/batch missing — run quad prompt first")
        else:
            errors.extend(validate_prompt(prompt))
    status = "PASS" if not errors else "BLOCK"
    return {
        "status": status,
        "cover_mode": cover_mode,
        "required_hair_phrase": REQUIRED_HAIR_PHRASE,
        "errors": errors,
        "blocker": None if status == "PASS" else "COVER IDENTITY BLOCKER",
        "rebuild": "Platinum / strongly lighter than reference hair → rebuild the 2K canvas. Do not fix hair outside the canvas.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--article-dir", default="")
    ap.add_argument("-o", "--output", default="cover-identity-gate.json")
    args = ap.parse_args()
    root = project_root()
    article_dir: Path | None = None
    if str(args.article_dir).strip():
        article_dir = Path(args.article_dir)
        if not article_dir.is_absolute():
            article_dir = root / article_dir

    try:
        verdict = run_gate(root=root, article_dir=article_dir)
    except json.JSONDecodeError as exc:
        print(f"❌ COVER IDENTITY BLOCKER: bad JSON: {exc}", file=sys.stderr)
        return 1

    out_name = Path(args.output).name
    if article_dir is not None:
        article_dir.mkdir(parents=True, exist_ok=True)
        out_path = article_dir / out_name
    else:
        out_path = root / "memory/cover" / out_name
    out_path.write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK gate={out_path} status={verdict['status']}")
    for err in verdict["errors"]:
        print(f"  - {err}")
    if verdict["status"] != "PASS":
        print(f"❌ {verdict['blocker']}: {verdict['rebuild']}", file=sys.stderr)
    return 0 if verdict["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
