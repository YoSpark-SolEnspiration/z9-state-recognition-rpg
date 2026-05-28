# FILE: ui/screens/battle_tower.py
from __future__ import annotations

from typing import Any, cast

import streamlit as st

from app_state import get_active_town_state, set_screen
from game.tower_engine import (
    FLOOR_ORDER,
    get_floor_questions,
    get_tower_state,
    is_tower_complete,
    next_floor,
    recompute_tower_totals,
    score_floor,
)
from ui.components import progress_steps, section_card


def _session_dict() -> dict[str, Any]:
    return cast(dict[str, Any], st.session_state)


def render_battle_tower_screen() -> None:
    session = _session_dict()

    active_state = get_active_town_state()
    if not active_state:
        st.warning("No active state selected.")
        if st.button("Return to State Selector"):
            set_screen("state_selector")
            st.rerun()
        return

    progress_steps(
        ["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"],
        4,
    )
    st.title("Battle Tower")
    st.caption("Recognition practice. Clear each floor before entering the Gym.")

    section_card("Active State", active_state.get("label", "No active state"))

    tower = get_tower_state(session)
    floor_id = tower.get("active_floor", "floor1_stage")

    floor_labels = {fid: title for fid, title, _ in FLOOR_ORDER}
    floor_descriptions = {fid: desc for fid, _, desc in FLOOR_ORDER}

    st.markdown("### Tower Floors")
    tabs = st.tabs([title for _, title, _ in FLOOR_ORDER])

    for tab, (fid, title, _desc) in zip(tabs, FLOOR_ORDER):
        with tab:
            if st.button(
                f"Set active: {title}",
                key=f"set_{fid}",
                use_container_width=True,
            ):
                tower["active_floor"] = fid
                st.rerun()

    st.divider()
    st.subheader(floor_labels.get(floor_id, "Tower Floor"))
    st.write(floor_descriptions.get(floor_id, ""))

    questions = get_floor_questions(active_state, floor_id)
    answers = tower.setdefault("answers", {})
    if not isinstance(answers, dict):
        answers = {}
        tower["answers"] = answers

    floor_answers = answers.setdefault(floor_id, {})
    if not isinstance(floor_answers, dict):
        floor_answers = {}
        answers[floor_id] = floor_answers

    for question in questions:
        question_id = question["id"]
        choice = st.radio(
            question["prompt"],
            question["options"],
            index=None,
            key=f"tower_{floor_id}_{question_id}",
        )

        if choice is not None:
            floor_answers[question_id] = choice

    if st.button("Submit Floor", use_container_width=True):
        score = score_floor(active_state, floor_id, floor_answers)

        floor_scores = tower.setdefault("floor_scores", {})
        if not isinstance(floor_scores, dict):
            floor_scores = {}
            tower["floor_scores"] = floor_scores

        floor_scores[floor_id] = score
        recompute_tower_totals(session)

        if score["total"] and score["correct"] >= max(1, score["total"] - 1):
            st.success(f"Floor cleared: {score['correct']}/{score['total']}")
            nxt = next_floor(floor_id)
            if nxt:
                tower["active_floor"] = nxt
            st.rerun()
        else:
            st.error(f"Retry this floor: {score['correct']}/{score['total']}")

    tower = recompute_tower_totals(session)

    st.divider()
    st.metric("Tower Score", f"{tower.get('correct', 0)} / {tower.get('total', 0)}")
    st.write(f"Floors cleared: {len(tower.get('cleared', []))} / {len(FLOOR_ORDER)}")

    c1, c2 = st.columns(2)

    with c1:
        if is_tower_complete(session):
            if st.button("Enter Gym", use_container_width=True):
                set_screen("gym")
                st.rerun()
        else:
            st.info("Clear all floors to unlock the Gym.")

    with c2:
        if st.button("Return to Town", use_container_width=True):
            set_screen("town")
            st.rerun()