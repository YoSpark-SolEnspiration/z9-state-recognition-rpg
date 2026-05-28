# FILE: ui/screens/developer_panel.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, reset_game_session, set_screen


def render_developer_panel_screen() -> None:
    st.title("Developer Panel")
    st.caption("Debug details stay here, outside the normal player flow.")
    st.subheader("Active Town State")
    st.json(get_active_town_state() or {}, expanded=True)
    st.subheader("Session State")
    st.json({k: v for k, v in st.session_state.items() if k != "_is_running_with_streamlit"}, expanded=False)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Return Home", use_container_width=True):
            set_screen("home")
            st.rerun()
    with c2:
        if st.button("Reset Game Session", use_container_width=True):
            reset_game_session()
            st.rerun()
