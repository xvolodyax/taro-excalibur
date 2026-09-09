"""Vladimir 2026-09-09 Art canon — ONE Kie 2K quad, never four 1K gens.

Cover cell: host (Victoria age 33) + B14 Cyrillic cover-text ON the PNG +
brand line; no red frame. Inlines: no host face. Do not redraw live articles.
"""

from __future__ import annotations

KIE_IMAGE_MODEL = "gpt-image-2-5-flare-image-to-image"
KIE_MODEL_PREFIX = "gpt-image-2-5-flare"
MCP_RESOLUTION = "2K"
FORBIDDEN_RESOLUTIONS = frozenset({"1K", "1k", "4K", "4k"})
CANVAS_PX = (2048, 1152)
PANEL_PX = (1024, 576)
JOBS_REQUIRED = 1
HOST_AGE = 33
RULE_DATE = "2026-09-09"


def is_allowed_kie_model(model: str) -> bool:
    value = str(model or "").strip()
    return value.startswith(KIE_MODEL_PREFIX)


def require_kie_model(model: str) -> str:
    value = str(model or "").strip()
    if not is_allowed_kie_model(value):
        raise ValueError(
            f"Kie model must be {KIE_MODEL_PREFIX}-* "
            f"(rule {RULE_DATE}), got {value!r}"
        )
    return value


def require_2k_resolution(resolution: str) -> str:
    value = str(resolution or "").strip() or MCP_RESOLUTION
    if value != MCP_RESOLUTION:
        raise ValueError(
            f"resolution must be {MCP_RESOLUTION} "
            f"(rule {RULE_DATE}: no 1K / no four separate gens), got {value!r}"
        )
    return value
