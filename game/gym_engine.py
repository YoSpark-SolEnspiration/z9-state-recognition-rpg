# FILE: game/gym_engine.py
from __future__ import annotations

from typing import Any

from game.content_router import get_state_label, gym_questions_for_state


PASSING_SCORE = 12


def get_gym_questions(active_state: dict[str, Any]) -> list[dict[str, Any]]:
    return gym_questions_for_state(active_state)


def score_gym(active_state: dict[str, Any], answers: dict[str, str]) -> dict[str, Any]:
    questions = get_gym_questions(active_state)
    total = len(questions)
    correct = sum(1 for q in questions if answers.get(q["id"]) == q["answer"])
    accuracy = round((correct / total) * 100) if total else 0
    passed = correct >= PASSING_SCORE

    if accuracy >= 90:
        strength = "Healthy response recognition"
        missed = "Minor refinement only"
        ohu_pattern = "OHU shifts recognized cleanly"
        state_movement = "Recognition stabilized under pressure"
    elif accuracy >= 75:
        strength = "Core state recognition"
        missed = "Mixed OHU/stage pressure needs review"
        ohu_pattern = "OHU shifts partially recognized"
        state_movement = "Recognition improving under pressure"
    else:
        strength = "Early recognition"
        missed = "Primary state pattern needs reinforcement"
        ohu_pattern = "OHU shifts need replay"
        state_movement = "Recognition pathway initiated"

    return {
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "passed": passed,
        "required": PASSING_SCORE,
        "recognition_strength": strength,
        "missed_pattern": missed,
        "ohu_pattern": ohu_pattern,
        "state_movement": state_movement,
        "next_path": (
            "Return Home and run a new state simulation"
            if passed
            else "Retry the Gym after reviewing Tower and Explore patterns"
        ),
        "state_label": get_state_label(active_state),
    }


def save_gym_results(session: dict[str, Any], results: dict[str, Any]) -> None:
    session["gym_results"] = results
    session["gym"] = results

def gym_summary(session: dict[str, Any]) -> dict[str, Any]:
    gym = session.get("gym", {})

    if not isinstance(gym, dict):
        return {
            "correct": 0,
            "total": 15,
            "accuracy": 0,
        }

    correct = int(gym.get("correct", 0))
    total = int(gym.get("total", 15))
    accuracy = int(round((correct / total) * 100)) if total else 0

    return {
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "passed": correct >= 12,
    }    
