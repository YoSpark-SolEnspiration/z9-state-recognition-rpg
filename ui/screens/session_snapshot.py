# FILE: ui/screens/session_snapshot.py
from __future__ import annotations

import json

import streamlit as st

from app_state import reset_game_session
from game.session_summary import build_session_summary
from reports.pdf_export import build_snapshot_pdf
from reports.session_snapshot_builder import build_snapshot_payload
from runtime.route_state import go_to
from ui.components import progress_steps, section_card


def render_session_snapshot_screen() -> None:
    progress_steps(["Home", "Select State", "Town", "Explore", "Tower", "Gym", "Snapshot"], 6)
    st.title("Session Snapshot")
    st.caption("The report is the proof of gameplay. The game remains the center.")

    summary = build_session_summary({str(k): v for k, v in st.session_state.items()})
    report_payload = build_snapshot_payload(summary)

    selected_state = summary.get("selected_state", {})
    if not selected_state:
        st.warning("No selected state found. Return Home and start a new session.")
        if st.button("Return Home", use_container_width=True):
            reset_game_session()
            st.rerun()
        return

    section_card("Town State", summary.get("state_label", "No state selected"), "Selected State")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Explore", f"{summary['rooms_explored']}/{summary['rooms_total']}")
    with m2:
        st.metric("Tower", f"{summary['tower']['correct']}/{summary['tower']['total']}")
    with m3:
        st.metric("Gym", f"{summary['gym']['correct']}/{summary['gym']['total']}")
    with m4:
        st.metric("Accuracy", f"{summary['recognition_accuracy']}%")

    st.divider()
    for section in report_payload.get("sections", []):
        section_card(section.get("heading", "Snapshot Section"), section.get("body", ""))

    pdf_bytes = build_snapshot_pdf(summary)
    json_bytes = json.dumps(report_payload, indent=2).encode("utf-8")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Download Session Snapshot PDF",
            data=pdf_bytes,
            file_name="z9_session_snapshot.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download Snapshot JSON",
            data=json_bytes,
            file_name="z9_session_snapshot.json",
            mime="application/json",
            use_container_width=True,
        )
    with c3:
        if st.button("Return Home / Reset", use_container_width=True):
            reset_game_session()
            st.rerun()

    if st.button("Retry Gym", use_container_width=True):
        go_to("gym")
        st.rerun()
