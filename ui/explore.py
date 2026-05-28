# FILE: ui/screens/explore.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen
from game.explore_engine import get_explore_rooms, mark_room_complete
from ui.components import card, hero, progress_steps


def _render_room(room: dict) -> None:
    with st.expander(f"{room['title']} — {room['teaches']}", expanded=room.get("default_open", False)):
        st.markdown(room["intro"])
        st.markdown("**Playable objective**")
        st.markdown(room["objective"])

        for node in room.get("nodes", []):
            card(node["title"], node["body"], node.get("kicker"))

        st.markdown("**Recognition prompt**")
        st.info(room["prompt"])

        if st.button(f"Mark {room['title']} Complete", key=f"complete_{room['id']}", use_container_width=True):
            mark_room_complete(room["id"])
            st.rerun()


def render_explore_screen() -> None:
    state = get_active_town_state()
    if not state:
        st.warning("Select a state before exploring.")
        if st.button("Go to State Selector"):
            set_screen("state_selector")
            st.rerun()
        return

    rooms = get_explore_rooms(state)
    completed = sum(1 for room in rooms if room.get("complete"))

    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 3)
    hero(
        "Explore Recognition Village",
        f"Encounter {state['label']} through meaning, behavior, reaction, and pillar expression.",
        "Learn before testing",
    )

    st.progress(completed / max(len(rooms), 1), text=f"Explore flags found: {completed}/{len(rooms)}")

    for room in rooms:
        _render_room(room)

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Back to Town", use_container_width=True):
            set_screen("town")
            st.rerun()
    with c2:
        if st.button("Go to Battle Tower", use_container_width=True):
            set_screen("battle_tower")
            st.rerun()
    with c3:
        if st.button("Developer Panel", use_container_width=True):
            set_screen("developer_panel")
            st.rerun()
