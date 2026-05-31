# FILE: ui/layout.py
"""Shared layout primitives for the game shell."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import streamlit as st

from app_state import get_active_town_state

SCREEN_LABELS = {
    "home": "Home Screen",
    "state_selector": "Manual State Selector",
    "town": "Town Center",
    "explore": "Explore",
    "battle_tower": "Battle Tower",
    "gym": "Gym",
    "session_snapshot": "Session Snapshot",
    "developer_panel": "Developer Panel",
}

@contextmanager
def render_game_shell(screen: str) -> Iterator[None]:
    state = get_active_town_state()
    active_label = state.get("label", "No active state") if state else "No active state"

    st.markdown('<div class="z9-shell">', unsafe_allow_html=True)
    left, right = st.columns([0.62, 0.38], vertical_alignment="center")
    with left:
        st.markdown('<div class="z9-kicker">Z9 State Recognition RPG</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="z9-small">Current Screen: {SCREEN_LABELS.get(screen, screen)}</div>', unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="z9-small">Active Town State</div><span class="z9-state-pill">{active_label}</span>', unsafe_allow_html=True)
    st.divider()
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)
