# FILE: game/scoring.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class ScoreResult:
    correct: int
    total: int
    accuracy: float
    passed: bool
    label: str


def score_answers(responses: Iterable[Dict[str, Any]], pass_ratio: float = 0.67) -> ScoreResult:
    items: List[Dict[str, Any]] = list(responses)
    total = len(items)
    correct = sum(1 for item in items if item.get("is_correct") is True)
    accuracy = 0.0 if total == 0 else correct / total
    passed = total > 0 and accuracy >= pass_ratio
    label = "Cleared" if passed else "Retry Recommended"
    return ScoreResult(correct=correct, total=total, accuracy=accuracy, passed=passed, label=label)


def floor_passed(correct: int, total: int, required: int = 2) -> bool:
    return total > 0 and correct >= required


def gym_passed(correct: int, total: int, required: int = 12) -> bool:
    return total > 0 and correct >= required


def accuracy_percent(correct: int, total: int) -> int:
    if total <= 0:
        return 0
    return round((correct / total) * 100)
