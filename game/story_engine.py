# FILE: game/story_engine.py
from __future__ import annotations

from typing import Any, Dict

CHARACTER_BY_TYPE = {
    "D": "Donte",
    "I": "Isaac",
    "S": "Samantha",
    "C": "Caleb",
}


def build_story_square_room(active_state: Dict[str, Any]) -> Dict[str, Any]:
    disc_type = active_state.get("disc_type", "D")
    character = CHARACTER_BY_TYPE.get(disc_type, "Donte")
    subtype = active_state.get("subtype", "DD")
    stage = active_state.get("stage", 1)
    ohu = active_state.get("ohu", "Overdeveloped")

    return {
        "id": "story_square",
        "title": "Story Square",
        "teaches": "How the state behaves",
        "intro": f"Story Square stages a playable NPC encounter around {character}, {subtype}, Stage {stage}, and {ohu} expression.",
        "objective": "Watch the behavior pattern instead of reading a definition. The player should identify the pressure, not memorize trivia.",
        "nodes": [
            {
                "title": f"{character} enters the scene",
                "kicker": f"{subtype} / Stage {stage}",
                "body": "A routine task becomes emotionally loaded. The NPC's behavior shows whether the selected state is controlling, stabilizing, withdrawing, performing, over-accommodating, or over-analyzing.",
            },
            {
                "title": "Witness NPC",
                "kicker": "State made visible",
                "body": "A second NPC reacts to the main character, giving the player contrast between what the state intends and what others experience.",
            },
            {
                "title": "Pressure beat",
                "kicker": "Recognition trigger",
                "body": "The scene introduces a shift: missing information, changed plan, social uncertainty, delay, or accountability demand.",
            },
        ],
        "prompt": f"Recognition check: what behavior tells you this is {subtype} under Stage {stage} pressure rather than a generic conflict?",
    }
