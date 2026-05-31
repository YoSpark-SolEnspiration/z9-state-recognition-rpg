# FILE: app_state.py
"""Session-state helpers for the Z9 State Recognition RPG demo."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

import streamlit as st

DEFAULT_SCREEN = "home"
VALID_SCREENS = {
    "home", "state_selector", "town", "explore", "battle_tower",
    "gym", "session_snapshot", "developer_panel",
}
PLAYER_SCREENS = {
    "home", "state_selector", "town", "explore", "battle_tower", "gym", "session_snapshot",
}

@dataclass(frozen=True)
class ActiveTownState:
    """The manually selected state that drives the playable town."""

    disc_type: str
    subtype: str
    stage: int
    ohu: str
    course: str = "course10"
    label: str = ""

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        if not payload.get("label"):
            payload["label"] = f"{self.subtype} / Stage {self.stage} / {self.ohu}"
        return payload

def init_session_state() -> None:
    """Initialize all gameplay session keys without overwriting progress."""

    st.session_state.setdefault("screen", DEFAULT_SCREEN)
    st.session_state.setdefault("active_town_state", None)
    st.session_state.setdefault("explore_flags", {})
    st.session_state.setdefault("tower_progress", {})
    st.session_state.setdefault("gym_progress", {})
    st.session_state.setdefault("gym_answers", {})
    st.session_state.setdefault("gym_results", {})
    st.session_state.setdefault("session_events", [])
    st.session_state.setdefault("developer_mode", False)
    st.session_state.setdefault("show_developer_payloads", False)

def get_screen() -> str:
    screen = st.session_state.get("screen", DEFAULT_SCREEN)
    return screen if screen in VALID_SCREENS else DEFAULT_SCREEN

def set_screen(screen: str) -> None:
    if screen not in VALID_SCREENS:
        raise ValueError(f"Unknown screen route: {screen}")
    st.session_state["screen"] = screen

def is_player_screen(screen: str | None = None) -> bool:
    return (screen or get_screen()) in PLAYER_SCREENS

def set_developer_mode(enabled: bool) -> None:
    st.session_state["developer_mode"] = bool(enabled)
    if not enabled:
        st.session_state["show_developer_payloads"] = False

def developer_mode_enabled() -> bool:
    return bool(st.session_state.get("developer_mode", False))

def developer_payloads_enabled() -> bool:
    return bool(st.session_state.get("developer_mode", False)) and bool(
        st.session_state.get("show_developer_payloads", False)
    )

def set_active_town_state(payload: Dict[str, Any]) -> None:
    st.session_state["active_town_state"] = payload
    log_event("state_selected", payload)

def get_active_town_state() -> Optional[Dict[str, Any]]:
    state = st.session_state.get("active_town_state")
    return state if isinstance(state, dict) else None

def reset_game_session() -> None:
    """Return to Home while clearing gameplay progress."""

    st.session_state["screen"] = DEFAULT_SCREEN
    st.session_state["active_town_state"] = None
    st.session_state["explore_flags"] = {}
    st.session_state["tower_progress"] = {}
    st.session_state["gym_progress"] = {}
    st.session_state["gym_answers"] = {}
    st.session_state["gym_results"] = {}
    st.session_state["session_events"] = []
    st.session_state["show_developer_payloads"] = False

def log_event(event_name: str, payload: Optional[Dict[str, Any]] = None) -> None:
    event = {"event": event_name, "payload": payload or {}}
    st.session_state.setdefault("session_events", []).append(event)
