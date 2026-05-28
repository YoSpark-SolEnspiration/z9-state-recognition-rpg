# FILE: tests/gym_test.py
from __future__ import annotations

from game.gym_engine import PASSING_SCORE, get_gym_questions, score_gym


def test_gym_has_15_questions() -> None:
    state = {
        "disc_type": "I",
        "subtype": "IC",
        "stage": 2,
        "ohu": "Underdeveloped",
        "label": "IC / Stage 2 / Underdeveloped",
    }
    questions = get_gym_questions(state)
    assert len(questions) == 15
    for q in questions:
        assert q["answer"] in q["options"]


def test_gym_passes_with_all_correct() -> None:
    state = {
        "disc_type": "S",
        "subtype": "SD",
        "stage": 6,
        "ohu": "Healthy",
        "label": "SD / Stage 6 / Healthy",
    }
    questions = get_gym_questions(state)
    answers = {q["id"]: q["answer"] for q in questions}
    results = score_gym(state, answers)
    assert results["correct"] == 15
    assert results["total"] == 15
    assert results["passed"] is True
    assert results["correct"] >= PASSING_SCORE
