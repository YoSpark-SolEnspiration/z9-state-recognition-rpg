# FILE: ui/screens/town.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen
from game.town_state import build_town_overview
from ui.components import card, hero, progress_steps, state_pill
from ui.visual_assets import render_visual_identity_card, render_visual_identity_strip


def render_town_screen() -> None:
    state = get_active_town_state()

    if not state:
        st.warning("No active town state selected.")
        if st.button("Go to State Selector"):
            set_screen("state_selector")
            st.rerun()
        return

    town = build_town_overview(state)

    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 2)

    hero(
        town["title"],
        town["subtitle"],
        town["kicker"],
    )

    visual_col, state_col = st.columns([0.34, 0.66])
    with visual_col:
        render_visual_identity_card(state, title="Town Anchor", compact=True, screen="town")
    with state_col:
        st.markdown("**Active State**")
        state_pill(state["label"])
        render_visual_identity_strip(state, screen="town")
        st.markdown(town["purpose"])

    cols = st.columns(4)

    for index, room in enumerate(town["rooms"]):
        with cols[index % 4]:
            card(room["title"], room["description"], room["teaches"])

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Explore Recognition Village", use_container_width=True):
            set_screen("explore")
            st.rerun()

    with c2:
        if st.button("Return to State Selector", use_container_width=True):
            set_screen("state_selector")
            st.rerun()