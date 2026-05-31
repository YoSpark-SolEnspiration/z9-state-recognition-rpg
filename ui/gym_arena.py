# FILE: ui/gym_arena.py
"""Gym arena visuals for Checkpoint 3.

The Gym arena is presentation only. It frames the existing deterministic Gym
rounds without changing validation, scoring, or pass/fail rules.
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
_REGISTRY = _ROOT / "data" / "visual" / "gym_scene_registry.json"


def _load_registry() -> dict[str, Any]:
    if not _REGISTRY.exists():
        return {}
    try:
        return json.loads(_REGISTRY.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _screen_payload() -> dict[str, Any]:
    registry = _load_registry()
    screens = registry.get("screens", {}) if isinstance(registry, dict) else {}
    return dict(screens.get("gym", {})) if isinstance(screens, dict) else {}


def round_payload(round_id: str) -> dict[str, Any]:
    registry = _load_registry()
    rounds = registry.get("round_visuals", {}) if isinstance(registry, dict) else {}
    return dict(rounds.get(round_id, {})) if isinstance(rounds, dict) else {}


def render_gym_arena(state: dict[str, Any] | None) -> None:
    """Render the Gym as an applied practice arena for the selected state."""
    visual = visual_payload_for_state(state)
    payload = _screen_payload()
    arena_asset = resolve_project_asset(payload.get("final_asset"), payload.get("placeholder_asset"))
    leader_asset = resolve_project_asset(payload.get("leader_final_asset"), payload.get("leader_placeholder_asset"))

    st.markdown('<div class="z9-gym-arena">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{escape(str(payload.get("kicker", "Gym")))}</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>{escape(str(payload.get("title", "Applied Practice Arena")))}</h3>', unsafe_allow_html=True)

    col_a, col_b = st.columns([0.58, 0.42])
    with col_a:
        if arena_asset:
            st.image(arena_asset, use_container_width=True)
        else:
            st.markdown('<div class="z9-scene-placeholder">Gym Arena<span>Applied pressure practice</span></div>', unsafe_allow_html=True)
    with col_b:
        if leader_asset:
            st.image(leader_asset, use_container_width=True)
        else:
            st.markdown(
                '<div class="z9-scene-placeholder">Gym Leader'
                f'<span>{escape(visual["character_name"])} · {escape(visual["form_code"])}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="z9-scene-meta">'
        f'<span><b>Anchor</b>{escape(visual["character_name"])}</span>'
        f'<span><b>Form</b>{escape(visual["form_code"])}</span>'
        f'<span><b>Practice</b>Pressure recognition</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="z9-muted">{escape(str(payload.get("purpose", "Recognize the selected state under pressure.")))}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-scene-rule">{escape(str(payload.get("rule", "Defeat by recognition, not force.")))}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_round_brief(round_id: str) -> None:
    """Render a compact round brief above a Gym question group."""
    payload = round_payload(round_id)
    if not payload:
        return
    st.markdown(
        '<div class="z9-round-brief">'
        f'<strong>{escape(str(payload.get("label", "Gym Round")))}</strong><br>'
        f'<span>{escape(str(payload.get("signal", "Recognize the state under pressure.")))}</span>'
        '</div>',
        unsafe_allow_html=True,
    )
