# FILE: runtime/save_state.py

from typing import Any, Dict

import streamlit as st


def get_app_state() -> Dict[str, Any]:
    return {str(key): value for key, value in st.session_state.items()}


def save_value(name: str, value: Any) -> None:
    st.session_state[name] = value


def load_value(name: str, default: Any = None) -> Any:
    return st.session_state.get(name, default)


def clear_app_state() -> None:
    st.session_state.clear()