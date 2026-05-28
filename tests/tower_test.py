# FILE: tests/tower_test.py
from __future__ import annotations

from game.tower_engine import FLOOR_ORDER, get_floor_questions, score_floor


def test_all_tower_floors_have_questions() -> None:
    state = {
        "disc_type": "C",
        "subtype": "CI",
        "stage": 5,
        "ohu": "Overdeveloped",
        "label": "CI / Stage 5 / Overdeveloped",
    }

    for floor_id, _, _ in FLOOR_ORDER:
        questions = get_floor_questions(state, floor_id)
        assert len(questions) == 3
        for q in questions:
            assert q["answer"] in q["options"]


def test_tower_floor_scores_correctly() -> None:
    state = {
        "disc_type": "D",
        "subtype": "DD",
        "stage": 1,
        "ohu": "Overdeveloped",
        "label": "DD / Stage 1 / Overdeveloped",
    }
    questions = get_floor_questions(state, "floor4_ohu")
    answers = {q["id"]: q["answer"] for q in questions}
    score = score_floor(state, "floor4_ohu", answers)
    assert score["correct"] == 3
    assert score["total"] == 3
