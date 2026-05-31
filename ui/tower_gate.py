# FILE: ui/tower_gate.py
"""Tower gate visuals for Checkpoint 3.

The Tower gate is presentation only. It keeps the selected state/form visible
while the existing tower engine continues to own questions, scoring, and floor
progression.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any
import json

import streamlit as st

from ui.visual_assets import resolve_project_asset
from ui.visual_registry import visual_payload_for_state

_ROOT = Path(__file__).resolve().parents[1]
_REGISTRY = _ROOT / "data" / "visual" / "tower_scene_registry.json"


def _load_registry() -> dict[str, Any]:
    if not _REGISTRY.exists():
        return {}
    try:
        return json.loads(_REGISTRY.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _screen_payload(key: str = "battle_tower") -> dict[str, Any]:
    registry = _load_registry()
    screens = registry.get("screens", {}) if isinstance(registry, dict) else {}
    return dict(screens.get(key, {})) if isinstance(screens, dict) else {}


def _floor_payload(floor_id: str) -> dict[str, Any]:
    registry = _load_registry()
    floors = registry.get("floor_visuals", {}) if isinstance(registry, dict) else {}
    return dict(floors.get(floor_id, {})) if isinstance(floors, dict) else {}


def render_tower_gate(state: dict[str, Any] | None, *, floor_id: str = "floor1_stage") -> None:
    """Render the Tower as a recognition gate while preserving live Tower flow."""
    visual = visual_payload_for_state(state)
    payload = _screen_payload("battle_tower")
    floor = _floor_payload(floor_id)
    asset = resolve_project_asset(payload.get("final_asset"), payload.get("placeholder_asset"))

    st.markdown('<div class="z9-tower-gate">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{escape(str(payload.get("kicker", "Battle Tower")))}</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>{escape(str(payload.get("title", "Recognition Gate")))}</h3>', unsafe_allow_html=True)

    if asset:
        st.image(asset, use_container_width=True)
    else:
        st.markdown(
            '<div class="z9-scene-placeholder">Recognition Gate'
            f'<span>{escape(visual["character_name"])} · {escape(visual["form_code"])}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="z9-scene-meta">'
        f'<span><b>Anchor</b>{escape(visual["character_name"])}</span>'
        f'<span><b>Form</b>{escape(visual["form_code"])}</span>'
        f'<span><b>Active Gate</b>{escape(str(floor.get("label", "Tower Floor")))}</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="z9-muted">{escape(str(payload.get("purpose", "Practice state recognition.")))}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-scene-rule">{escape(str(payload.get("rule", "Advance by recognition.")))}</div>', unsafe_allow_html=True)
    if floor.get("signal"):
        st.markdown(f'<div class="z9-tower-signal">{escape(str(floor["signal"]))}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
