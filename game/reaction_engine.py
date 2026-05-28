# FILE: game/reaction_engine.py
from __future__ import annotations

from typing import Any, Dict


def build_reaction_alley_room(active_state: Dict[str, Any]) -> Dict[str, Any]:
    subtype = active_state.get("subtype", "DD")
    stage = active_state.get("stage", 1)

    return {
        "id": "reaction_alley",
        "title": "Reaction Alley",
        "teaches": "How the state sounds and reacts",
        "intro": "Reaction Alley repeats one pressure event three ways so the player can compare OHU expressions.",
        "objective": "Identify the healthy expression by noticing regulation, not volume, charm, patience, or precision alone.",
        "nodes": [
            {
                "title": "Same pressure",
                "kicker": "The plan changed",
                "body": "The player sees the same disruption across overdeveloped, healthy, and underdeveloped responses.",
            },
            {
                "title": "Overdeveloped reaction",
                "kicker": "Too much trait",
                "body": "The state attempts to solve pressure by amplifying its default survival strategy.",
            },
            {
                "title": "Healthy reaction",
                "kicker": "Regulated trait",
                "body": "The state names what matters, adapts the next step, and protects consistency without collapsing into pressure.",
            },
            {
                "title": "Underdeveloped reaction",
                "kicker": "Withheld trait",
                "body": "The state avoids, withdraws, freezes, performs helplessness, or gives up its useful strength.",
            },
        ],
        "prompt": f"Recognition check: which {subtype} response shows regulated action under Stage {stage} pressure?",
    }
