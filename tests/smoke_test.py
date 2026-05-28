# FILE: tests/smoke_test.py
from app_state import AppState


def test_app_state_defaults():
    state = AppState()
    assert state.screen == "home"
    assert state.active_state.subtype == "DD"
