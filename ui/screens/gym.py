# FILE: ui/screens/gym.py
from __future__ import annotations

from typing import Dict

import streamlit as st

from game.gym_engine import evaluate_gym_round, get_gym_rounds, gym_summary
from game.scoring import deterministic_option_order
from runtime.route_state import go_to
from runtime.session_flags import get_flag, mark_gym_round, set_snapshot_ready
from ui.components import section_card


def render_gym_screen() -> None:
    state = get_flag("active_town_state")
    progress = get_flag("gym_progress", {})

    st.title("Gym")
    st.caption("Recognition under pressure. The boss is defeated by recognizing the state, not overpowering it.")

    if not state:
        st.warning("Select a state before entering the Gym.")
        if st.button("Return to State Selector"):
            go_to("state_selector")
        return

    state_label = state.get("label") or f"{state.get('subtype', 'DD')} / Stage {state.get('stage', 1)} / {state.get('ohu', 'Overdeveloped')}"
    section_card("Active State", state_label, "Gym Context")

    st.info("Gym rule: 15 total recognition prompts. 12 correct defeats the Gym Leader. 11 or below means retry the Gym, not the whole town.")

    rounds = get_gym_rounds()
    tabs = st.tabs([gym_round["title"] for gym_round in rounds])

    for tab, gym_round in zip(tabs, rounds):
        with tab:
            st.subheader(gym_round["title"])
            st.write(gym_round["purpose"])

            selected: Dict[str, str] = {}
            for q in gym_round.get("questions", []):
                qid = q["id"]
                st.markdown(f"**{q.get('prompt', '')}**")
                options = deterministic_option_order(
                    q.get("options", []),
                    f"gym:{state_label}:{gym_round['key']}:{qid}",
                )
                if options:
                    selected[qid] = st.radio(
                        "Choose one:",
                        options,
                        key=f"gym_{gym_round['key']}_{qid}",
                        label_visibility="collapsed",
                    )

            if st.button(f"Submit {gym_round['title']}", key=f"submit_gym_{gym_round['key']}"):
                result = evaluate_gym_round(gym_round["key"], selected)
                mark_gym_round(gym_round["key"], result)
                if result["passed"]:
                    st.success(f"Round recognized: {result['correct']}/{result['total']}")
                else:
                    st.warning(f"Pressure pattern missed: {result['correct']}/{result['total']}")
                    for item in result["results"]:
                        if not item["is_correct"]:
                            st.info(item.get("hint", "Review recognition clues."))
                st.rerun()

            if gym_round["key"] in progress:
                r = progress[gym_round["key"]]
                st.caption(f"Current result: {r.get('correct', 0)}/{r.get('total', 0)} | Passed: {r.get('passed', False)}")

    summary = gym_summary(get_flag("gym_progress", {}))
    st.divider()
    st.write(
        f"Gym score: {summary['correct']} / {summary['total']} "
        f"({summary['accuracy']}%) | Required: {summary['required_correct']}"
    )

    if summary["passed"]:
        set_snapshot_ready(True)
        st.success("Gym Leader defeated. Session Snapshot is ready.")
    elif summary["total"] > 0:
        st.warning("Retry the Gym rounds to reach 12 correct recognitions.")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Return to Tower"):
            go_to("battle_tower")
    with c2:
        if st.button("Review Explore"):
            go_to("explore")
    with c3:
        if st.button("Open Snapshot", disabled=not summary["passed"]):
            go_to("session_snapshot")
