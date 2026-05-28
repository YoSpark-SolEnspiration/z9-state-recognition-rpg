# FILE: ui/screens/explore.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen
from game.explore_engine import get_explore_rooms, mark_room_complete
from runtime.session_flags import get_explore_flags
from ui.components import card, hero, progress_steps, section_card


def _render_room_nodes(room: dict) -> None:
    nodes = room.get("nodes", [])
    if not nodes:
        st.info("This room is waiting for content nodes.")
        return

    for index, node in enumerate(nodes, start=1):
        title = node.get("title", f"Recognition Node {index}")
        body = node.get("body", "")
        kicker = node.get("kicker", "Town Clue")
        card(title, body, kicker)


def render_explore_screen() -> None:
    state = get_active_town_state()
    if not state:
        st.warning("Select a state before exploring.")
        if st.button("Go to State Selector"):
            set_screen("state_selector")
            st.rerun()
        return

    progress_steps(
        ["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"],
        3,
    )
    hero(
        "Explore Recognition Village",
        f"Encounter the selected state before the Tower tests it: {state['label']}.",
        "Checkpoint 2A · State-Aware Explore Rooms",
    )

    flags = get_explore_flags()
    rooms = get_explore_rooms(state)
    completed = sum(1 for room in rooms if flags.get(room["id"]))

    st.progress(completed / len(rooms) if rooms else 0)
    st.caption(f"Rooms explored: {completed} / {len(rooms)}")

    for room in rooms:
        room_id = room["id"]
        is_complete = bool(flags.get(room_id))
        status = "Complete" if is_complete else "Unexplored"
        title = room.get("title", room_id.replace("_", " ").title())
        teaches = room.get("teaches", "Recognition Area")

        with st.expander(f"{title} — {teaches} ({status})", expanded=not is_complete):
            section_card(title, room.get("intro", ""), teaches)
            st.markdown(f"**Objective:** {room.get('objective', 'Recognize the selected state.')} ")

            source = room.get("source")
            if source:
                st.caption(f"Template source: {source}")

            _render_room_nodes(room)

            prompt = room.get("prompt", "What state cue is this area teaching?")
            st.info(prompt)

            if is_complete:
                st.success("Recognition flag collected.")
            elif st.button(f"Collect {title} Flag", key=f"complete_{room_id}", use_container_width=True):
                mark_room_complete(room_id)
                st.success(f"{title} flag collected.")
                st.rerun()

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Return to Town", use_container_width=True):
            set_screen("town")
            st.rerun()
    with c2:
        if st.button("Enter Battle Tower", use_container_width=True):
            set_screen("battle_tower")
            st.rerun()
    with c3:
        if st.button("Reset Explore Flags", use_container_width=True):
            st.session_state["explore_flags"] = {}
            st.rerun()
