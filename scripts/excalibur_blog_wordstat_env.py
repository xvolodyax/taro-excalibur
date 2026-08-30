#!/usr/bin/env python3
"""Load Wordstat / Yandex Cloud Search API key without ever printing it.

Safe slot:
- Cloud Secrets / env: YANDEX_CLOUD_SEARCH_API_KEY
- Local paste file: memory/wordstat.env.local (gitignored)
- Template (empty): memory/wordstat.env.local.example

CLI prints only present/missing + source. Never dumps the key.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ENV_KEYS = ("YANDEX_CLOUD_SEARCH_API_KEY", "YANDEX_SEARCH_API_KEY")
FOLDER_ENV_KEYS = ("YANDEX_FOLDER_ID", "YANDEX_CLOUD_FOLDER_ID")
LOCAL_REL = "memory/wordstat.env.local"


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def _strip_value(raw: str) -> str:
    value = (raw or "").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return value


def read_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.is_file():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            env[key.strip()] = _strip_value(value)
    return env


def load_wordstat_api_key(root: Path | None = None) -> tuple[str, str]:
    """Return (key, source). source is env | local_file | missing. Key may be empty."""
    root = root or project_root()
    local = read_env_file(root / LOCAL_REL)
    for key_name in ENV_KEYS:
        env_val = _strip_value(os.environ.get(key_name, ""))
        if env_val:
            return env_val, "env"
        local_val = local.get(key_name, "")
        if local_val:
            return local_val, "local_file"
    return "", "missing"


def load_wordstat_folder_id(root: Path | None = None) -> tuple[str, str]:
    """Return (folder_id, source). Never print the value."""
    root = root or project_root()
    local = read_env_file(root / LOCAL_REL)
    for key_name in FOLDER_ENV_KEYS:
        env_val = _strip_value(os.environ.get(key_name, ""))
        if env_val:
            return env_val, "env"
        local_val = local.get(key_name, "")
        if local_val:
            return local_val, "local_file"
    return "", "missing"


def wordstat_key_status(root: Path | None = None) -> dict[str, object]:
    key, source = load_wordstat_api_key(root)
    folder, folder_source = load_wordstat_folder_id(root)
    present = bool(key)
    return {
        "present": present,
        "source": source if present else "missing",
        "length": len(key) if present else 0,
        "env_key": ENV_KEYS[0],
        "folder_present": bool(folder),
        "folder_source": folder_source if folder else "missing",
        "local_file": LOCAL_REL,
    }


def main() -> int:
    status = wordstat_key_status()
    if status["present"]:
        print(
            f"wordstat_key=present source={status['source']} "
            f"length={status['length']} "
            f"folder={'present' if status['folder_present'] else 'missing'} "
            f"folder_source={status['folder_source']}"
        )
        return 0
    print(
        "wordstat_key=missing "
        f"paste_into={LOCAL_REL} or Cloud Secret {ENV_KEYS[0]}"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
