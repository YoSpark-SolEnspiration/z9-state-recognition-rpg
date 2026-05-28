# FILE: game/explore_engine.py
from __future__ import annotations

from typing import Any

import streamlit as st

from game.pillar_engine import build_pillar_market_room
from game.reaction_engine import build_reaction_alley_room
from game.story_engine import build_story_square_room
from game.vocab_engine import build_vocab_hall_room

ROOM_BUILDERS = [
    ("vocab_hall", build_vocab_hall_room),
    ("story_square", build_story_square_room),
    ("reaction_alley", build_reaction_alley_room),
    ("pillar_market", build_pillar_market_room),
]


def get_explore_flags() -> dict[str, bool]:
    flags = st.session_state.setdefault("explore_flags", {})
    if not isinstance(flags, dict):
        flags = {}
        st.session_state["explore_flags"] = flags
    return flags


def _normalize_room(room_id: str, room: dict[str, Any]) -> dict[str, Any]:
    room.setdefault("id", room_id)
    room.setdefault("title", room_id.replace("_", " ").title())
    room.setdefault("kicker", "Recognition Room")
    room.setdefault("teaches", room.get("kicker", "Recognition"))
    room.setdefault("intro", room.get("body", ""))
    room.setdefault("objective", "Recognize the selected state before the Tower tests it.")
    room.setdefault("prompt", "What state cue is this area teaching?")

    if "nodes" not in room:
        nodes = []

        for card in room.get("cards", []):
            if isinstance(card, dict):
                nodes.append(
                    {
                        "title": card.get("heading", "Recognition Node"),
                        "body": card.get("body", ""),
                        "kicker": room.get("kicker", "Town Clue"),
                    }
                )

        if room.get("reactions"):
            for label, response in room["reactions"].items():
                nodes.append(
                    {
                        "title": label,
                        "body": str(response),
                        "kicker": "OHU Response",
                    }
                )

        if room.get("pillars"):
            for pillar in room["pillars"]:
                if isinstance(pillar, dict):
                    nodes.append(
                        {
                            "title": pillar.get("pillar", "Pillar Lens"),
                            "body": pillar.get("reading", ""),
                            "kicker": "Z9 Pillar",
                        }
                    )

        if room.get("body") and not nodes:
            nodes.append(
                {
                    "title": room.get("title", "Recognition Node"),
                    "body": room.get("body", ""),
                    "kicker": room.get("kicker", "Town Clue"),
                }
            )

        room["nodes"] = nodes

    return room


def get_explore_rooms(active_state: dict[str, Any]) -> list[dict[str, Any]]:
    flags = get_explore_flags()
    rooms: list[dict[str, Any]] = []

    for room_id, builder in ROOM_BUILDERS:
        room = builder(active_state)

        if not isinstance(room, dict):
            room = {}

        room = _normalize_room(room_id, room)
        room["complete"] = bool(flags.get(room_id, False))

        rooms.append(room)

    return rooms


def mark_room_complete(room_id: str) -> None:
    flags = get_explore_flags()
    flags[room_id] = True
    st.session_state["explore_flags"] = flags