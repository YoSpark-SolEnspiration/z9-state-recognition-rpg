# FILE: ui/screens/home.py
from __future__ import annotations

import streamlit as st

from app_state import set_screen
from ui.components import card, hero, progress_steps


def render_home_screen() -> None:
    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 0)
    hero(
        "Open Game",
        "A self-contained state-recognition RPG. Select a state, enter the town, learn its signals, then practice recognition before the Gym test.",
        "Z9 Game Seed Engine Demo",
    )
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        card("Recognition Village", "The town teaches what the selected state looks like, how it sounds, and how it reacts.", "Town")
    with c2:
        card("Battle Tower", "Practice recognizing stage, DISC, pillar, and OHU signals before the Gym.", "Practice")
    with c3:
        card("Gym", "Recognize the same state under pressure. The boss is defeated by recognition, not force.", "Evaluation")
    st.write("")
    if st.button("Start Session", use_container_width=True):
        set_screen("state_selector")
        st.rerun()
