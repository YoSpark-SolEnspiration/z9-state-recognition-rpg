# FILE: ui/screens/explore.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen
from ui.components import card, hero, progress_steps


def render_explore_screen() -> None:
    state = get_active_town_state()
    if not state:
        st.warning("Select a state before exploring.")
        if st.button("Go to State Selector"):
            set_screen("state_selector")
            st.rerun()
        return
    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 3)
    hero("Explore", f"Explore rooms are staged for {state['label']}.", "Batch 2 Placeholder")
    card("Next Batch", "Batch 3/4 will wire Vocab Hall, Story Square, Reaction Alley, and Pillar Market content.")
    if st.button("Go to Battle Tower", use_container_width=True):
        set_screen("battle_tower")
        st.rerun()
