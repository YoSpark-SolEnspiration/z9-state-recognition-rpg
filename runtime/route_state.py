# FILE: runtime/route_state.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen

GAME_FLOW = ["home", "state_selector", "town", "explore", "battle_tower", "gym", "session_snapshot"]
SCREEN_LABELS = {
    "home": "Home",
    "state_selector": "Select State",
    "town": "Town",
    "explore": "Explore",
    "battle_tower": "Battle Tower",
    "gym": "Gym",
    "session_snapshot": "Session Snapshot",
    "developer_panel": "Developer Panel",
}


def go_to(screen: str, rerun: bool = True) -> None:
    """Route to a screen and optionally refresh Streamlit."""
    set_screen(screen)
    if rerun:
        st.rerun()


def go_home(reset: bool = False) -> None:
    """Return home. When reset is True, clear the gameplay session first."""
    if reset:
        from app_state import reset_game_session
        reset_game_session()
    else:
        set_screen("home")
    st.rerun()


def route_to_town_if_ready() -> bool:
    if get_active_town_state():
        set_screen("town")
        return True
    set_screen("state_selector")
    return False


def require_active_state(fallback: str = "state_selector") -> bool:
    if get_active_town_state():
        return True
    set_screen(fallback)
    return False


def next_screen(current: str) -> str:
    if current not in GAME_FLOW:
        return "home"
    index = GAME_FLOW.index(current)
    return GAME_FLOW[min(index + 1, len(GAME_FLOW) - 1)]


def screen_label(screen: str) -> str:
    return SCREEN_LABELS.get(screen, screen.replace("_", " ").title())


def get_visual_route_payload(state: dict | None = None) -> dict:
    """Return selected character/form routing metadata without touching gameplay scoring."""
    from app_state import get_active_town_state
    from ui.visual_registry import visual_payload_for_state

    active = state if state is not None else get_active_town_state()
    visual = visual_payload_for_state(active)
    return {
        "selected_character": visual["character_name"],
        "selected_character_key": visual["character_key"],
        "selected_form": visual["form_code"],
        "selected_disc_family": visual["disc_family"],
        "selected_disc_family_color": visual["disc_family_color"],
        "selected_asset": visual.get("form_final_asset") or visual.get("form_placeholder_asset") or visual.get("character_base_asset"),
    }
