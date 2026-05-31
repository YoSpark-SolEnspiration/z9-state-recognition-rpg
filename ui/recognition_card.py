# FILE: ui/recognition_card.py
"""Reusable recognition-card UI for Checkpoint 3.

This module keeps visual state presentation consistent across Town, Explore,
Tower, Gym, and Snapshot without moving gameplay or scoring logic into UI code.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Literal

import streamlit as st

from ui.visual_registry import visual_payload_for_state

_ROOT = Path(__file__).resolve().parents[1]
DetailMode = Literal["compact", "standard", "snapshot"]

SCREEN_PURPOSES = {
    "state_selector": "Choose the person/form pairing before the town renders.",
    "town": "The town shows the selected state in lived context.",
    "explore": "Explore rooms turn the state into observable clues.",
    "tower": "The Tower tests whether the state can be recognized under questions.",
    "gym": "The Gym applies the same state under pressure and transformation.",
    "snapshot": "The Snapshot proves what was recognized during play.",
}


def _resolve_asset(*paths: str | None) -> str | None:
    """Resolve final art first, then placeholder art, without broken image output."""
    for raw in paths:
        if not raw:
            continue
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = _ROOT / candidate
        if candidate.exists():
            return str(candidate)
    return None


def recognition_payload(state: dict[str, Any] | None) -> dict[str, Any]:
    """Public wrapper for resolving a state's visual identity."""
    return visual_payload_for_state(state)


def render_recognition_card(
    state: dict[str, Any] | None,
    *,
    title: str = "Recognition Form",
    screen: str = "town",
    mode: DetailMode = "standard",
) -> dict[str, Any]:
    """Render the selected character/form card and return its payload."""
    visual = recognition_payload(state)
    asset = _resolve_asset(
        visual.get("form_final_asset"),
        visual.get("form_placeholder_asset"),
        visual.get("character_base_asset"),
    )
    purpose = SCREEN_PURPOSES.get(screen, "The selected state is being made visible.")
    state_label = str((state or {}).get("label") or visual.get("form_code") or "Selected State")

    st.markdown(
        f'<div class="z9-recognition-card z9-recognition-{escape(str(mode))}">',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="z9-kicker">{escape(title)}</div>', unsafe_allow_html=True)

    if asset:
        st.image(asset, use_container_width=True)
    else:
        st.markdown(
            f'<div class="z9-empty-visual">{escape(visual["form_code"])}'
            f'<br><span>{escape(visual["character_name"])}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="z9-form-title">{escape(visual["character_name"])} · {escape(visual["form_code"])}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="z9-form-meta">{escape(visual["disc_family_color"])} · {escape(visual["disc_family"])}</div>',
        unsafe_allow_html=True,
    )

    if mode != "compact":
        st.markdown(
            '<div class="z9-recognition-facts">'
            f'<span><b>State</b>{escape(state_label)}</span>'
            f'<span><b>Anchor</b>{escape(visual["character_name"])}</span>'
            f'<span><b>Form</b>{escape(visual["form_code"])}</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<p class="z9-form-desc">{escape(visual["form_label"])}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="z9-small">{escape(purpose)}</p>', unsafe_allow_html=True)

    if mode == "snapshot":
        st.markdown(
            f'<div class="z9-form-grid-note">{escape(visual["visual_rule"])}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
    return visual


def render_recognition_strip(
    state: dict[str, Any] | None,
    *,
    screen: str = "town",
    title: str = "Visual State",
) -> dict[str, Any]:
    """Render a compact state identity strip for horizontal screen headers."""
    visual = recognition_payload(state)
    purpose = SCREEN_PURPOSES.get(screen, "Selected visual state route.")
    st.markdown(
        '<div class="z9-visual-strip">'
        f'<span class="z9-kicker">{escape(title)}</span>'
        f'<strong>{escape(visual["character_name"])} · {escape(visual["form_code"])}</strong>'
        f'<span>{escape(visual["disc_family_color"])} · {escape(visual["disc_family"])}</span>'
        f'<span>{escape(purpose)}</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    return visual
