# FILE: dev/qa_mode.py
from __future__ import annotations

from typing import Any

from game.content_router import selected_npc, tower_questions_for_state
from game.gym_engine import get_gym_questions


QA_STATES = [
    {"disc_type": "D", "subtype": "DD", "stage": 1, "ohu": "Overdeveloped", "label": "DD / Stage 1 / Overdeveloped"},
    {"disc_type": "S", "subtype": "SD", "stage": 6, "ohu": "Healthy", "label": "SD / Stage 6 / Healthy"},
    {"disc_type": "I", "subtype": "IC", "stage": 2, "ohu": "Underdeveloped", "label": "IC / Stage 2 / Underdeveloped"},
    {"disc_type": "C", "subtype": "CI", "stage": 5, "ohu": "Overdeveloped", "label": "CI / Stage 5 / Overdeveloped"},
]


def checkpoint_2a_report() -> list[dict[str, Any]]:
    report = []

    for state in QA_STATES:
        tower = tower_questions_for_state(state)
        gym = get_gym_questions(state)
        report.append(
            {
                "state": state["label"],
                "npc": selected_npc(state),
                "tower_floors": {floor: len(questions) for floor, questions in tower.items()},
                "gym_questions": len(gym),
                "tower_mentions_npc": selected_npc(state) in " ".join(
                    q["prompt"] for qs in tower.values() for q in qs
                ),
                "gym_mentions_npc": selected_npc(state) in " ".join(q["prompt"] for q in gym),
            }
        )

    return report
