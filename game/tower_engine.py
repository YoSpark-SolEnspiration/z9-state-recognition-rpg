# FILE: game/tower_engine.py
from __future__ import annotations

from typing import Any

from game.content_router import get_state_label, tower_questions_for_state

FLOOR_ORDER = [
    ("floor1_stage", "Floor 1: Stage Recognition", "Practice identifying developmental pressure."),
    ("floor2_disc", "Floor 2: DISC Recognition", "Practice identifying DISC expression without judging the person."),
    ("floor3_pillars", "Floor 3: Pillar Recognition", "Practice seeing one behavior through Z9 lenses."),
    ("floor4_ohu", "Floor 4: Wing / PType / OHU Recognition", "Practice distinguishing overdeveloped, healthy, and underdeveloped expressions."),
]


def get_tower_state(session: dict[str, Any]) -> dict[str, Any]:
    if "tower" not in session or not isinstance(session["tower"], dict):
        session["tower"] = {
            "active_floor": "floor1_stage",
            "answers": {},
            "floor_scores": {},
            "correct": 0,
            "total": 0,
            "cleared": [],
        }
    return session["tower"]


def get_floor_questions(active_state: dict[str, Any], floor_id: str) -> list[dict[str, Any]]:
    return tower_questions_for_state(active_state).get(floor_id, [])


def score_floor(active_state: dict[str, Any], floor_id: str, answers: dict[str, str]) -> dict[str, int]:
    questions = get_floor_questions(active_state, floor_id)
    total = len(questions)
    correct = 0
    for q in questions:
        if answers.get(q["id"]) == q["answer"]:
            correct += 1
    return {"correct": correct, "total": total}


def recompute_tower_totals(session: dict[str, Any]) -> dict[str, Any]:
    tower = get_tower_state(session)
    correct = 0
    total = 0
    cleared = []
    for floor_id, _, _ in FLOOR_ORDER:
        floor_score = tower.get("floor_scores", {}).get(floor_id, {})
        c = int(floor_score.get("correct", 0))
        t = int(floor_score.get("total", 0))
        correct += c
        total += t
        if t and c >= max(1, t - 1):
            cleared.append(floor_id)
    tower["correct"] = correct
    tower["total"] = total
    tower["cleared"] = cleared
    tower["accuracy"] = round((correct / total) * 100) if total else 0
    session["tower_results"] = {
        "correct": correct,
        "total": total,
        "accuracy": tower["accuracy"],
        "cleared": cleared,
        "state_label": get_state_label(session.get("active_town_state", {})),
    }
    return tower


def next_floor(current_floor: str) -> str | None:
    ids = [item[0] for item in FLOOR_ORDER]
    if current_floor not in ids:
        return ids[0]
    idx = ids.index(current_floor)
    if idx + 1 >= len(ids):
        return None
    return ids[idx + 1]


def is_tower_complete(session: dict[str, Any]) -> bool:
    tower = recompute_tower_totals(session)
    return len(tower.get("cleared", [])) == len(FLOOR_ORDER)

def tower_summary(
    tower: dict[str, Any],
    active_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(tower, dict):
        return {
            "correct": 0,
            "total": 0,
            "cleared": [],
            "floors_cleared": 0,
        }

    correct = int(tower.get("correct", 0))
    total = int(tower.get("total", 0))
    cleared = tower.get("cleared", [])

    if not isinstance(cleared, list):
        cleared = []

    return {
        "correct": correct,
        "total": total,
        "cleared": cleared,
        "floors_cleared": len(cleared),
    }