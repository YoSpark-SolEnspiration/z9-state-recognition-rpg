# FILE: game/state_selector.py
from __future__ import annotations

DISC_TYPES = ["D", "I", "S", "C"]
OHU_OPTIONS = ["Overdeveloped", "Healthy", "Underdeveloped", "All"]
STAGES = list(range(1, 9))
SUBTYPES = {
    "D": ["DD", "DI", "DS", "DC"],
    "I": ["ID", "II", "IS", "IC"],
    "S": ["SD", "SI", "SS", "SC"],
    "C": ["CD", "CI", "CS", "CC"],
}
TYPE_NAMES = {
    "D": "Dominance / Direction",
    "I": "Influence / Expression",
    "S": "Steadiness / Support",
    "C": "Conscientiousness / Precision",
}


def get_subtypes(disc_type: str) -> list[str]:
    return SUBTYPES.get(disc_type, SUBTYPES["D"])


def build_active_state(disc_type: str, subtype: str, stage: int, ohu: str) -> dict:
    return {
        "disc_type": disc_type,
        "disc_label": TYPE_NAMES.get(disc_type, disc_type),
        "subtype": subtype,
        "stage": int(stage),
        "ohu": ohu,
        "course": "course10",
        "label": f"{subtype} / Stage {int(stage)} / {ohu}",
    }
