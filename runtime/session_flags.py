# FILE: runtime/session_flags.py
from __future__ import annotations

from typing import Any, Dict

import streamlit as st

DEFAULT_FLAGS: Dict[str, Any] = {
    "screen": "home",
    "active_town_state": None,
    "explore_flags": {},
    "tower_progress": {},
    "gym_progress": {},
    "gym_answers": {},
    "gym_results": {},
    "snapshot_ready": False,
}


def init_session_flags() -> None:
    for key, value in DEFAULT_FLAGS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, dict) else value


def set_flag(name: str, value: Any) -> None:
    init_session_flags()
    st.session_state[name] = value


def get_flag(name: str, default: Any = None) -> Any:
    init_session_flags()
    return st.session_state.get(name, default)


def get_explore_flags() -> Dict[str, Any]:
    init_session_flags()
    flags = st.session_state.get("explore_flags", {})
    return dict(flags) if isinstance(flags, dict) else {}


def set_explore_flag(flag_key: str, value: Any = True) -> None:
    init_session_flags()
    flags = get_explore_flags()
    flags[flag_key] = value
    st.session_state["explore_flags"] = flags


def mark_explore_flag(flag_key: str, value: Any = True) -> None:
    set_explore_flag(flag_key, value)


def reset_explore_flags() -> None:
    st.session_state["explore_flags"] = {}


def mark_tower_floor(floor_key: str, result: Dict[str, Any]) -> None:
    init_session_flags()
    progress = dict(st.session_state.get("tower_progress", {}))
    progress[floor_key] = result
    st.session_state["tower_progress"] = progress


def reset_tower_progress() -> None:
    st.session_state["tower_progress"] = {}


def mark_gym_round(round_key: str, result: Dict[str, Any]) -> None:
    init_session_flags()
    progress = dict(st.session_state.get("gym_progress", {}))
    progress[round_key] = result
    st.session_state["gym_progress"] = progress
    st.session_state["gym_results"] = progress


def reset_gym_run() -> None:
    st.session_state["gym_progress"] = {}
    st.session_state["gym_answers"] = {}
    st.session_state["gym_results"] = {}
    st.session_state["snapshot_ready"] = False


def set_snapshot_ready(value: bool = True) -> None:
    init_session_flags()
    st.session_state["snapshot_ready"] = value


def reset_gameplay() -> None:
    for key, value in DEFAULT_FLAGS.items():
        st.session_state[key] = value.copy() if isinstance(value, dict) else value
