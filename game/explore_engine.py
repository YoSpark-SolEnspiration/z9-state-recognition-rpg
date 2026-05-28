# FILE: game/explore_engine.py
from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from game.pillar_engine import build_pillar_market_room
from game.reaction_engine import build_reaction_alley_room
from game.story_engine import build_story_square_room
from game.vocab_engine import build_vocab_hall_room
from runtime.session_flags import get_explore_flags, set_explore_flag


def get_explore_rooms(active_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    flags = get_explore_flags()
    rooms = [
        build_vocab_hall_room(active_state),
        build_story_square_room(active_state),
        build_reaction_alley_room(active_state),
        build_pillar_market_room(active_state),
    ]
    for room in rooms:
        room["complete"] = bool(flags.get(room["id"]))
        room["default_open"] = not room["complete"]
    return rooms


def mark_room_complete(room_id: str) -> None:
    set_explore_flag(room_id, True)
    st.session_state.setdefault("session_events", []).append(
        {"event": "explore_room_complete", "payload": {"room_id": room_id}}
    )
