# FILE: ui/scene_card.py
"""Scene rendering helpers for Checkpoint 3 town/explore visuals.

Scenes are visual wrappers around the existing deterministic content. They do
not own scoring, routing, or state logic; they make the selected state readable
as lived context before Tower/Gym validation.
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
_SCENE_REGISTRY = _ROOT / "data" / "visual" / "town_scene_registry.json"


def _load_scene_registry() -> dict[str, Any]:
    if not _SCENE_REGISTRY.exists():
        return {}
    try:
        return json.loads(_SCENE_REGISTRY.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def scene_payload(room: dict[str, Any] | None, state: dict[str, Any] | None) -> dict[str, Any]:
    """Resolve visual scene metadata for a room and selected state."""
    room = room or {}
    registry = _load_scene_registry()
    room_id = str(room.get("id") or "default")
    scenes = registry.get("rooms", {}) if isinstance(registry, dict) else {}
    default = scenes.get("default", {}) if isinstance(scenes, dict) else {}
    scene = dict(scenes.get(room_id, default)) if isinstance(scenes, dict) else {}

    visual = visual_payload_for_state(state)
    return {
        "room_id": room_id,
        "room_title": room.get("title", scene.get("title", "Recognition Scene")),
        "scene_title": scene.get("title", room.get("title", "Recognition Scene")),
        "kicker": scene.get("kicker", room.get("kicker", "Town Scene")),
        "purpose": scene.get("purpose", room.get("objective", "Recognize the selected state in context.")),
        "visual_rule": scene.get("visual_rule", "Scene changes by selected state; identity remains stable."),
        "final_asset": scene.get("final_asset"),
        "placeholder_asset": scene.get("placeholder_asset", "assets/placeholders/town/default.png"),
        "character": visual.get("character_name", "Selected Anchor"),
        "form_code": visual.get("form_code", "--"),
        "disc_family": visual.get("disc_family", "Selected Family"),
        "disc_family_color": visual.get("disc_family_color", "Z9"),
    }


def render_scene_header(room: dict[str, Any], state: dict[str, Any] | None) -> dict[str, Any]:
    """Render the room scene hero/card and return scene metadata."""
    payload = scene_payload(room, state)
    asset = resolve_project_asset(payload.get("final_asset"), payload.get("placeholder_asset"))

    st.markdown('<div class="z9-scene-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{escape(str(payload["kicker"]))}</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>{escape(str(payload["scene_title"]))}</h3>', unsafe_allow_html=True)

    if asset:
        st.image(asset, use_container_width=True)
    else:
        st.markdown(
            '<div class="z9-scene-placeholder">'
            f'{escape(str(payload["room_id"]).replace("_", " ").title())}'
            f'<span>{escape(str(payload["character"]))} · {escape(str(payload["form_code"]))}</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="z9-scene-meta">'
        f'<span><b>Anchor</b>{escape(str(payload["character"]))}</span>'
        f'<span><b>Form</b>{escape(str(payload["form_code"]))}</span>'
        f'<span><b>Family</b>{escape(str(payload["disc_family_color"]))} · {escape(str(payload["disc_family"]))}</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="z9-muted">{escape(str(payload["purpose"]))}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-scene-rule">{escape(str(payload["visual_rule"]))}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return payload


def render_scene_beats(room: dict[str, Any]) -> None:
    """Render scene cards/scene_cards as actual readable scene beats."""
    scene_cards = room.get("scene_cards") or []
    if scene_cards:
        st.markdown("#### Scene Movement")
        cols = st.columns(min(len(scene_cards), 4))
        for index, scene in enumerate(scene_cards):
            with cols[index % len(cols)]:
                st.markdown('<div class="z9-scene-beat">', unsafe_allow_html=True)
                st.markdown(f'<div class="z9-kicker">{escape(str(scene.get("context", "Context")))}</div>', unsafe_allow_html=True)
                st.markdown(f'<strong>{escape(str(scene.get("cue", "The state becomes visible.")))}</strong>', unsafe_allow_html=True)
                st.markdown(f'<p>{escape(str(scene.get("visible_state", "Visible state cue.")))}</p>', unsafe_allow_html=True)
                st.markdown(f'<span>{escape(str(scene.get("recognition_move", "Name the state, then choose the next useful move.")))}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        return

    nodes = room.get("nodes") or []
    if nodes:
        st.markdown("#### Recognition Clues")
        for node in nodes:
            st.markdown('<div class="z9-scene-node">', unsafe_allow_html=True)
            st.markdown(f'<div class="z9-kicker">{escape(str(node.get("kicker", "Town Clue")))}</div>', unsafe_allow_html=True)
            st.markdown(f'<strong>{escape(str(node.get("title", "Recognition Node")))}</strong>', unsafe_allow_html=True)
            st.markdown(f'<p>{escape(str(node.get("body", "")))}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
