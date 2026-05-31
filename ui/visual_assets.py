# FILE: ui/visual_assets.py
"""Visual asset rendering helpers for Checkpoint 3 placeholders and final art.

Compatibility layer: older screens can still import render_visual_identity_card
and render_visual_identity_strip, while Batch 18D routes those calls through the
new reusable recognition-card UI.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ui.recognition_card import render_recognition_card, render_recognition_strip

_ROOT = Path(__file__).resolve().parents[1]


def resolve_project_asset(*paths: str | None) -> str | None:
    """Resolve the first existing asset from project-relative path candidates."""
    for raw in paths:
        if not raw:
            continue
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = _ROOT / candidate
        if candidate.exists():
            return str(candidate)
    return None


def render_visual_identity_card(
    state: dict[str, Any] | None,
    *,
    title: str = "Recognition Form",
    compact: bool = False,
    screen: str = "town",
) -> dict[str, Any]:
    """Render a consistent visual card for the active state and return the payload."""
    return render_recognition_card(
        state,
        title=title,
        screen=screen,
        mode="compact" if compact else "standard",
    )


def render_visual_identity_strip(
    state: dict[str, Any] | None,
    *,
    screen: str = "town",
    title: str = "Visual State",
) -> dict[str, Any]:
    """Render a low-height selected-state visual strip."""
    return render_recognition_strip(state, screen=screen, title=title)
