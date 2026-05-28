# FILE: ui/screens/battle_tower.py
from __future__ import annotations

from typing import Dict

import streamlit as st

from game.scoring import deterministic_option_order
from game.tower_engine import evaluate_floor, get_tower_floors, tower_summary
from runtime.route_state import go_to
from runtime.session_flags import get_flag, mark_tower_floor
from ui.components import section_card


def render_battle_tower_screen() -> None:
    state = get_flag("active_town_state")
    progress = get_flag("tower_progress", {})

    st.title("Battle Tower")
    st.caption("Recognition practice. Clear each floor before entering the Gym.")

    if not state:
        st.warning("Select a state before entering the Battle Tower.")
        if st.button("Return to State Selector"):
            go_to("state_selector")
        return

    state_label = state.get("label") or f"{state.get('subtype', 'DD')} / Stage {state.get('stage', 1)} / {state.get('ohu', 'Overdeveloped')}"
    section_card("Active State", state_label)

    floors = get_tower_floors()
    tabs = st.tabs([floor["title"] for floor in floors])

    for tab, floor in zip(tabs, floors):
        with tab:
            st.subheader(floor["title"])
            st.write(floor["purpose"])

            selected: Dict[str, str] = {}
            for q in floor.get("questions", []):
                qid = q["id"]
                st.markdown(f"**{q.get('prompt', '')}**")
                options = deterministic_option_order(
                    q.get("options", []),
                    f"tower:{state_label}:{floor['key']}:{qid}",
                )
                if options:
                    selected[qid] = st.radio(
                        "Choose one:",
                        options,
                        key=f"tower_{floor['key']}_{qid}",
                        label_visibility="collapsed",
                    )

            if st.button(f"Submit {floor['title']}", key=f"submit_{floor['key']}"):
                result = evaluate_floor(floor["key"], selected)
                mark_tower_floor(floor["key"], result)
                if result["passed"]:
                    st.success(f"Floor cleared: {result['correct']}/{result['total']}")
                else:
                    st.warning(f"Retry recommended: {result['correct']}/{result['total']}")
                    for item in result["results"]:
                        if not item["is_correct"]:
                            st.info(item.get("hint", "Review Explore clues."))
                st.rerun()

            if floor["key"] in progress:
                r = progress[floor["key"]]
                st.caption(f"Current result: {r.get('correct', 0)}/{r.get('total', 0)} | Passed: {r.get('passed', False)}")

    summary = tower_summary(get_flag("tower_progress", {}))
    st.divider()
    st.write(
        f"Tower score: {summary['correct']} / {summary['total']} "
        f"({summary['accuracy']}%) | Floors cleared: {summary['floors_cleared']} / {summary['floors_total']}"
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Return to Town"):
            go_to("town")
    with c2:
        if st.button("Review Explore"):
            go_to("explore")
    with c3:
        if st.button("Enter Gym", disabled=not summary["qualified_for_gym"]):
            go_to("gym")


def render_battle_tower() -> None:
    render_battle_tower_screen()
