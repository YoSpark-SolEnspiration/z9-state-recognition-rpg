# FILE: ui/screens/state_selector.py
from __future__ import annotations

import streamlit as st

from app_state import set_active_town_state, set_screen
from game.state_selector import DISC_TYPES, OHU_OPTIONS, STAGES, TYPE_NAMES, build_active_state, get_subtypes
from ui.components import card, hero, progress_steps


def render_state_selector_screen() -> None:
    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 1)
    hero(
        "Manual State Selector",
        "Presenter mode: choose the exact state the town will teach. This replaces assessment logic for the demo.",
        "Set Active Town State",
    )

    left, right = st.columns([0.55, 0.45])
    with left:
        disc_type = st.selectbox("Type", DISC_TYPES, format_func=lambda x: f"{x} — {TYPE_NAMES[x]}")
        subtype = st.selectbox("Subtype / Wing", get_subtypes(disc_type))
        stage = st.selectbox("Stage", STAGES, index=0, format_func=lambda x: f"Stage {x}")
        ohu = st.selectbox("OHU", OHU_OPTIONS, index=0)

        payload = build_active_state(disc_type, subtype, stage, ohu)
        st.json(payload, expanded=False)

        if st.button("Enter Town", type="primary", use_container_width=True):
            set_active_town_state(payload)
            set_screen("town")
            st.rerun()

    with right:
        card(
            "What this creates",
            "This selection becomes `active_town_state`. The Town, Explore rooms, Tower, Gym, and Session Snapshot all read from this state.",
            "Routing Contract",
        )
        card(
            "Example",
            "DD / Stage 1 / Overdeveloped loads a town that teaches overcontrolled D behavior under trust-pressure.",
            "Demo State",
        )
