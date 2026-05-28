# FILE: game/vocab_engine.py
from __future__ import annotations

from typing import Any, Dict


def build_vocab_hall_room(active_state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": "vocab_hall",
        "title": "Vocab Hall",
        "teaches": "What the state means",
        "intro": "Vocab Hall turns Course 10 concepts into recognition cards before the player faces pressure.",
        "objective": "Collect the meaning of long-term sustainability so the player can recognize when a state supports or disrupts it.",
        "nodes": [
            {
                "title": "Sustainability Card",
                "kicker": "Course 10 term",
                "body": "Sustainability is the ability to maintain health behaviors over time. In town logic, this asks whether the state can keep going after intensity fades.",
            },
            {
                "title": "Self-Regulation Card",
                "kicker": "Course 10 term",
                "body": "Self-regulation is managing behavior and emotion to maintain consistency. It becomes visible when pressure changes the plan.",
            },
            {
                "title": "Cognitive Flexibility Card",
                "kicker": "Course 10 term",
                "body": "Cognitive flexibility is the ability to shift strategies when needed instead of abandoning the goal.",
            },
            {
                "title": "Accountability Card",
                "kicker": "Course 10 term",
                "body": "Accountability systems are external structures that help sustain motivation and discipline.",
            },
        ],
        "prompt": "Recognition check: when a plan changes, does this state adapt toward consistency or tighten into control?",
    }
