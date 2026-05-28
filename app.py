# FILE: app.py
"""Z9 State Recognition RPG demo entrypoint."""
from __future__ import annotations

import streamlit as st

from app_state import get_screen, init_session_state, set_screen
from ui.layout import render_game_shell
from ui.screens.battle_tower import render_battle_tower_screen
from ui.screens.developer_panel import render_developer_panel_screen
from ui.screens.explore import render_explore_screen
from ui.screens.gym import render_gym_screen
from ui.screens.home import render_home_screen
from ui.screens.session_snapshot import render_session_snapshot_screen
from ui.screens.state_selector import render_state_selector_screen
from ui.screens.town import render_town_screen
from ui.theme import apply_theme

SCREEN_RENDERERS = {
    "home": render_home_screen,
    "state_selector": render_state_selector_screen,
    "town": render_town_screen,
    "explore": render_explore_screen,
    "battle_tower": render_battle_tower_screen,
    "gym": render_gym_screen,
    "session_snapshot": render_session_snapshot_screen,
    "developer_panel": render_developer_panel_screen,
}

def main() -> None:
    st.set_page_config(
        page_title="Z9 State Recognition RPG",
        page_icon="◇",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    init_session_state()
    apply_theme()
    screen = get_screen()
    renderer = SCREEN_RENDERERS.get(screen, render_home_screen)

    with render_game_shell(screen):
        renderer()

    with st.sidebar:
        st.caption("Z9 Demo Controls")
        if st.button("Home", use_container_width=True):
            set_screen("home")
            st.rerun()
        if st.button("Developer Panel", use_container_width=True):
            set_screen("developer_panel")
            st.rerun()

if __name__ == "__main__":
    main()
