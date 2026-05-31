# FILE: ui/screens/gym.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen
from game.gym_engine import PASSING_SCORE, get_gym_questions, save_gym_results, score_gym
from runtime.session_flags import reset_gym_run
from ui.components import nav_buttons, progress_steps, section_card, state_pill
from ui.visual_assets import render_visual_identity_card, render_visual_identity_strip
from ui.gym_arena import render_gym_arena, render_round_brief


def render_gym_screen() -> None:
    active_state = get_active_town_state()
    if not active_state:
        st.warning("No active state selected.")
        if st.button("Return to State Selector", use_container_width=True):
            set_screen("state_selector")
            st.rerun()
        return

    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 5)

    st.title("Gym")
    st.caption("Recognition under pressure. The boss is defeated by recognizing the state, not overpowering it.")

    visual_col, state_col = st.columns([0.28, 0.72])
    with visual_col:
        render_visual_identity_card(active_state, title="Gym Form", compact=True, screen="gym")
    with state_col:
        section_card("Gym Context", "Recognize the selected state under pressure.")
        st.markdown("**Active State**")
        state_pill(active_state.get("label", "No active state"))
        render_visual_identity_strip(active_state, screen="gym")
        st.info(f"Gym rule: 15 prompts. {PASSING_SCORE} correct defeats the Gym Leader. Retry Gym only if needed.")

    render_gym_arena(active_state)

    questions = get_gym_questions(active_state)
    answers = st.session_state.setdefault("gym_answers", {})

    round_tabs = st.tabs([
        "Round 1: Warm Pressure",
        "Round 2: Mixed OHU",
        "Round 3: Story Pressure",
        "Round 4: Gym Leader",
    ])

    chunks = [
        questions[0:3],
        questions[3:6],
        questions[6:11],
        questions[11:15],
    ]

    round_ids = ["warm_pressure", "mixed_ohu", "story_pressure", "gym_leader"]

    for tab, chunk, round_id in zip(round_tabs, chunks, round_ids):
        with tab:
            render_round_brief(round_id)
            for q in chunk:
                choice = st.radio(
                    q["prompt"],
                    q["options"],
                    index=None,
                    key=f"gym_{q['id']}",
                )
                if choice is not None:
                    answers[q["id"]] = choice

    st.divider()

    if st.button("Submit Gym Run", use_container_width=True):
        results = score_gym(active_state, answers)
        save_gym_results(st.session_state, results)

        if results["passed"]:
            st.success(f"Gym Leader defeated: {results['correct']}/{results['total']} ({results['accuracy']}%)")
            set_screen("session_snapshot")
            st.rerun()
        else:
            st.error(f"Retry Gym: {results['correct']}/{results['total']} ({results['accuracy']}%)")

    results = st.session_state.get("gym_results", {})
    st.metric(
        "Gym score",
        f"{results.get('correct', 0)} / {results.get('total', len(questions))}",
        f"{results.get('accuracy', 0)}%",
    )

    passed = bool(results.get("passed"))
    if passed:
        nav_buttons(back_label="Back to Tower", back_screen="battle_tower", next_label="View Snapshot", next_screen="session_snapshot", home=False)
    else:
        nav_buttons(back_label="Back to Tower", back_screen="battle_tower", home=False)

    with st.expander("Gym controls"):
        st.caption("Use only when you want to retry the same selected state under pressure.")
        if st.button("Retry Gym", use_container_width=True):
            reset_gym_run()
            st.rerun()
