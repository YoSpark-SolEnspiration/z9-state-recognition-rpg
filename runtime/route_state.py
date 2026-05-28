# FILE: runtime/route_state.py
from __future__ import annotations

import streamlit as st

from app_state import get_active_town_state, set_screen

GAME_FLOW = ["home", "state_selector", "town", "explore", "battle_tower", "gym", "session_snapshot"]


def go_to(screen: str, rerun: bool = True) -> None:
    """Route to a player-facing screen and optionally refresh Streamlit."""
    set_screen(screen)
    if rerun:
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
