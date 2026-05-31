# FILE: ui/screens/explore.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen
from game.explore_engine import get_explore_rooms, mark_room_complete
from runtime.session_flags import get_explore_flags, reset_explore_flags
from ui.components import hero, nav_buttons, progress_steps, section_card, state_pill
from ui.scene_card import render_scene_beats, render_scene_header
from ui.visual_assets import render_visual_identity_card, render_visual_identity_strip


def render_explore_screen() -> None:
    state = get_active_town_state()
    if not state:
        st.warning("Select a state before exploring.")
        if st.button("Go to State Selector", use_container_width=True):
            set_screen("state_selector")
            st.rerun()
        return

    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 3)
    hero(
        "Explore Recognition Village",
        f"Encounter the selected state before the Tower tests it: {state['label']}.",
        "Town Teaching Areas",
    )

    flags = get_explore_flags()
    rooms = get_explore_rooms(state)
    completed = sum(1 for room in rooms if flags.get(room["id"]))

    top_left, top_right = st.columns([0.28, 0.72])
    with top_left:
        render_visual_identity_card(state, title="Encounter Anchor", compact=True, screen="explore")
    with top_right:
        st.markdown("**Active State**")
        state_pill(state["label"])
        render_visual_identity_strip(state, screen="explore")
    st.progress(completed / len(rooms) if rooms else 0)
    st.caption(f"Rooms explored: {completed} / {len(rooms)}")

    show_completed = st.toggle("Show completed rooms", value=True)

    for room in rooms:
        room_id = room["id"]
        is_complete = bool(flags.get(room_id))
        if is_complete and not show_completed:
            continue
        status = "Complete" if is_complete else "Unexplored"

        with st.expander(f"{room['title']} — {room['teaches']} ({status})", expanded=not is_complete):
            section_card(room["title"], room.get("intro", ""), room.get("teaches", "Recognition Area"))
            st.markdown(f"**Objective:** {room.get('objective', 'Recognize the selected state.')}")
            render_scene_header(room, state)
            render_scene_beats(room)

            st.info(room.get("prompt", "What state cue is this area teaching?"))

            if is_complete:
                st.success("Recognition flag collected.")
            elif st.button(f"Collect {room['title']} Flag", key=f"complete_{room_id}", use_container_width=True):
                mark_room_complete(room_id)
                st.success(f"{room['title']} flag collected.")
                st.rerun()

    st.divider()
    nav_buttons(back_label="Return to Town", back_screen="town", next_label="Enter Battle Tower", next_screen="battle_tower", home=False)

    with st.expander("Explore controls"):
        st.caption("Use only when you want to retest the room loop for the same selected state.")
        if st.button("Reset Explore Flags", use_container_width=True):
            reset_explore_flags()
            st.rerun()
