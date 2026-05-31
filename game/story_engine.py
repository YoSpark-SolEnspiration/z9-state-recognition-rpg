# FILE: game/story_engine.py
from __future__ import annotations

from typing import Any, Dict

from game.content_router import build_story_room_content


def build_story_square_room(active_state: Dict[str, Any] | None) -> Dict[str, Any]:
    """Build Story Square from selected-state NPC, stage, and OHU templates."""
    room = build_story_room_content(active_state)
    room["source"] = "state_content/ptype_scene_templates.json + narrative_scene_index.json"
    return room
