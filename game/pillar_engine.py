# FILE: game/pillar_engine.py
from __future__ import annotations

from typing import Any, Dict

PILLAR_STALLS = [
    ("DISC Identity", "Which trait expression is leading the room?"),
    ("Developmental Stage", "Which stage pressure is shaping the reaction?"),
    ("Motivation Systems", "Is motivation intrinsic, external, collapsed, or overforced?"),
    ("Cognitive Dissonance", "Where do stated values and behavior split?"),
    ("Self-Regulation", "Can the state adjust without losing direction?"),
    ("Social Learning", "What behavior is being modeled or copied?"),
    ("ZPD", "What support makes the next move reachable?"),
    ("Spiral Harmony", "Does the state stabilize or spiral into friction?"),
    ("Resonance & Recursion", "What pattern repeats across contexts?"),
]


def build_pillar_market_room(active_state: Dict[str, Any]) -> Dict[str, Any]:
    subtype = active_state.get("subtype", "DD")
    ohu = active_state.get("ohu", "Overdeveloped")

    return {
        "id": "pillar_market",
        "title": "Pillar Market",
        "teaches": "How the state appears across pillars",
        "intro": "Pillar Market turns the same state into multiple recognition lenses so the player sees the pattern across contexts.",
        "objective": "Collect pillar stamps by identifying which lens explains the visible friction.",
        "nodes": [
            {"title": name, "kicker": f"{subtype} / {ohu}", "body": question}
            for name, question in PILLAR_STALLS
        ],
        "prompt": "Recognition check: which pillar best explains the state movement you just observed?",
    }
