# FILE: game/session_summary.py
from __future__ import annotations

from typing import Any, Dict, List

from game.scoring import accuracy_percent


def _count_true_flags(flags: Dict[str, Any]) -> int:
    return sum(1 for value in flags.values() if bool(value))


def _safe_state_label(state: Dict[str, Any] | None) -> str:
    if not state:
        return "No state selected"

    return state.get("label") or (
        f"{state.get('subtype', 'DD')} / "
        f"Stage {state.get('stage', 1)} / "
        f"{state.get('ohu', 'Overdeveloped')}"
    )


def _safe_tower_summary(tower: Dict[str, Any]) -> Dict[str, Any]:
    correct = int(tower.get("correct", 0))
    total = int(tower.get("total", 0))
    cleared = tower.get("cleared", [])

    if not isinstance(cleared, list):
        cleared = []

    return {
        "correct": correct,
        "total": total,
        "accuracy": accuracy_percent(correct, total),
        "floors_cleared": len(cleared),
        "floors_total": 4,
        "passed": len(cleared) >= 4,
    }


def _safe_gym_summary(gym: Dict[str, Any]) -> Dict[str, Any]:
    correct = int(gym.get("correct", 0))
    total = int(gym.get("total", 15))
    accuracy = int(gym.get("accuracy", accuracy_percent(correct, total)))
    passed = bool(gym.get("passed", correct >= 12))

    return {
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "passed": passed,
        "required_correct": int(gym.get("required", gym.get("required_correct", 12))),
        "recognition_strength": gym.get("recognition_strength", ""),
        "missed_pattern": gym.get("missed_pattern", ""),
        "ohu_pattern": gym.get("ohu_pattern", ""),
        "state_movement": gym.get("state_movement", ""),
        "next_path": gym.get("next_path", ""),
    }


def build_session_summary(session: Dict[str, Any]) -> Dict[str, Any]:
    state = session.get("active_town_state") or {}
    explore_flags = session.get("explore_flags") or {}

    tower_progress = session.get("tower") or session.get("tower_progress") or {}
    gym_progress = session.get("gym") or session.get("gym_results") or session.get("gym_progress") or {}

    tower = (
        _safe_tower_summary(tower_progress)
        if isinstance(tower_progress, dict)
        else _safe_tower_summary({})
    )
    gym = (
        _safe_gym_summary(gym_progress)
        if isinstance(gym_progress, dict)
        else _safe_gym_summary({})
    )

    rooms_found = _count_true_flags(explore_flags) if isinstance(explore_flags, dict) else 0
    rooms_total = 4

    total_correct = int(tower.get("correct", 0)) + int(gym.get("correct", 0))
    total_prompts = int(tower.get("total", 0)) + int(gym.get("total", 0))
    overall_accuracy = accuracy_percent(total_correct, total_prompts)

    gym_passed = bool(gym.get("passed", False))

    return {
        "selected_state": state,
        "state_label": _safe_state_label(state),
        "rooms_explored": rooms_found,
        "rooms_total": rooms_total,
        "tower": tower,
        "gym": gym,
        "recognition_accuracy": overall_accuracy,
        "recognition_strength": (
            gym.get("recognition_strength")
            or ("Healthy response recognition" if gym_passed else "State clue collection")
        ),
        "missed_pattern": (
            gym.get("missed_pattern")
            or ("Stage pressure" if overall_accuracy < 80 else "Minor refinement only")
        ),
        "ohu_recognition_pattern": (
            gym.get("ohu_pattern")
            or _infer_ohu_pattern(gym_progress if isinstance(gym_progress, dict) else {})
        ),
        "state_movement": (
            gym.get("state_movement")
            or _infer_state_movement(overall_accuracy, gym_passed)
        ),
        "next_path": (
            gym.get("next_path")
            or _next_path(overall_accuracy, gym_passed)
        ),
        "events": session.get("session_events", []),
    }


def _infer_ohu_pattern(gym_progress: Dict[str, Any]) -> str:
    if not gym_progress:
        return "Not yet tested"

    missed: List[str] = []

    for result in gym_progress.values():
        if not isinstance(result, dict):
            continue

        for item in result.get("results", []):
            if isinstance(item, dict) and not item.get("is_correct"):
                missed.append(str(item.get("id", "unknown")))

    if not missed:
        return "OHU shifts recognized cleanly"

    return "Review mixed pressure and OHU response shifts"


def _infer_state_movement(accuracy: int, gym_passed: bool) -> str:
    if gym_passed and accuracy >= 80:
        return "Recognition stabilized under pressure"

    if accuracy >= 60:
        return "Recognition emerging; pressure still changes visibility"

    return "Recognition still depends on guided town clues"


def _next_path(accuracy: int, gym_passed: bool) -> str:
    if gym_passed:
        return "Return Home and run a new state simulation"

    if accuracy >= 60:
        return "Retry Gym after reviewing Reaction Alley"

    return "Return to Explore, collect room flags, then retry Tower/Gym"