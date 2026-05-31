# FILE: app.py
"""Z9 State Recognition RPG demo entrypoint."""
from __future__ import annotations

import streamlit as st

from app_state import (
    developer_mode_enabled,
    get_active_town_state,
    get_screen,
    init_session_state,
    set_developer_mode,
    set_screen,
)
from runtime.route_state import get_visual_route_payload, screen_label
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

def _render_sidebar(screen: str) -> None:
    with st.sidebar:
        st.caption("Z9 Demo Controls")
        st.write(f"Current screen: **{screen_label(screen)}**")
        state = get_active_town_state()
        if state:
            st.caption(f"State: {state.get('label', 'Selected')}")
            visual_route = get_visual_route_payload(state)
            st.caption(f"Visual: {visual_route['selected_character']} · {visual_route['selected_form']}")

        if st.button("Return Home", use_container_width=True):
            set_screen("home")
            st.rerun()

        developer_enabled = st.toggle("Developer Mode", value=developer_mode_enabled())
        set_developer_mode(developer_enabled)
        if developer_enabled:
            if st.button("Open Developer Panel", use_container_width=True):
                set_screen("developer_panel")
                st.rerun()

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

    _render_sidebar(screen)

if __name__ == "__main__":
    main()
