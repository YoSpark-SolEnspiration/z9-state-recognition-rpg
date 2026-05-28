# FILE: game/town_state.py
from __future__ import annotations

from typing import Any, Dict, List


def build_town_overview(active_state: Dict[str, Any]) -> Dict[str, Any]:
    """Build the player-facing town overview for the selected manual state."""

    label = active_state.get("label", "Selected State")
    subtype = active_state.get("subtype", "DD")
    stage = active_state.get("stage", 1)
    ohu = active_state.get("ohu", "Overdeveloped")

    return {
        "title": "Town Center",
        "subtitle": f"The town has loaded as a recognition village for {label}.",
        "kicker": "Course 10 Recognition Village",
        "purpose": (
            "This town teaches the player what the selected state looks like, how it behaves, "
            "how it sounds under pressure, and how it appears across the Z9 pillars before the Tower and Gym test recognition."
        ),
        "state_tags": [subtype, f"Stage {stage}", ohu],
        "rooms": [
            {
                "id": "vocab_hall",
                "title": "Vocab Hall",
                "teaches": "Meaning",
                "description": "Course 10 language: sustainability, self-regulation, resilience, adaptation, and accountability.",
            },
            {
                "id": "story_square",
                "title": "Story Square",
                "teaches": "Behavior",
                "description": "NPC scenes show how the selected state acts when pressure enters the room.",
            },
            {
                "id": "reaction_alley",
                "title": "Reaction Alley",
                "teaches": "OHU reaction",
                "description": "Compare overdeveloped, healthy, and underdeveloped expressions of the same state.",
            },
            {
                "id": "pillar_market",
                "title": "Pillar Market",
                "teaches": "Pillar lens",
                "description": "Read the same state through identity, stage pressure, motivation, dissonance, and recursion.",
            },
        ],
    }


def get_room_ids() -> List[str]:
    return ["vocab_hall", "story_square", "reaction_alley", "pillar_market"]
