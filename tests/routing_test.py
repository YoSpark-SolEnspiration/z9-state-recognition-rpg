# FILE: tests/routing_test.py
from __future__ import annotations

from game.content_router import selected_npc, tower_questions_for_state


def test_type_to_npc_routing() -> None:
    assert selected_npc({"disc_type": "D", "subtype": "DD"}) == "Donte"
    assert selected_npc({"disc_type": "I", "subtype": "II"}) == "Isaac"
    assert selected_npc({"disc_type": "S", "subtype": "SD"}) == "Samantha"
    assert selected_npc({"disc_type": "C", "subtype": "CI"}) == "Caleb"


def test_tower_questions_route_to_selected_type_language() -> None:
    state = {
        "disc_type": "S",
        "subtype": "SD",
        "stage": 6,
        "ohu": "Healthy",
        "label": "SD / Stage 6 / Healthy",
    }
    floors = tower_questions_for_state(state)
    text = " ".join(q["prompt"] for qs in floors.values() for q in qs)
    assert "Samantha" in text
