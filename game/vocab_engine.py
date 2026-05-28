# FILE: game/vocab_engine.py
from __future__ import annotations

from typing import Any, Dict

from game.content_router import build_vocab_room_content


def build_vocab_hall_room(active_state: Dict[str, Any] | None) -> Dict[str, Any]:
    """Build Vocab Hall from selected-state templates."""
    room = build_vocab_room_content(active_state)
    room["source"] = "state_content/explore_room_templates.json + Course 10 concept grammar"
    return room
