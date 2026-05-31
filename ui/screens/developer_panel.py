# FILE: ui/screens/developer_panel.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, reset_game_session, set_screen


def render_developer_panel_screen() -> None:
    st.title("Developer Panel")
    st.caption("Debug details stay here, outside the normal player flow.")

    st.subheader("Active Town State")
    with st.expander("View active state payload", expanded=True):
        st.json(get_active_town_state() or {}, expanded=True)

    st.subheader("Session State")
    with st.expander("View full session payload", expanded=False):
        st.json({k: v for k, v in st.session_state.items() if k != "_is_running_with_streamlit"}, expanded=False)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Return to Player Home", use_container_width=True):
            set_screen("home")
            st.rerun()
    with c2:
        if st.button("Return to Town", use_container_width=True):
            set_screen("town")
            st.rerun()
    with c3:
        if st.button("Reset Game Session", use_container_width=True):
            reset_game_session()
            st.rerun()
