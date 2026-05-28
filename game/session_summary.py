# FILE: game/session_summary.py
from __future__ import annotations

from typing import Any, Dict, List

from game.gym_engine import gym_summary
from game.tower_engine import tower_summary
from game.scoring import accuracy_percent


def _count_true_flags(flags: Dict[str, Any]) -> int:
    return sum(1 for value in flags.values() if bool(value))


def _safe_state_label(state: Dict[str, Any] | None) -> str:
    if not state:
        return "No state selected"
    return state.get("label") or f"{state.get('subtype', 'DD')} / Stage {state.get('stage', 1)} / {state.get('ohu', 'Overdeveloped')}"


def build_session_summary(session: Dict[str, Any]) -> Dict[str, Any]:
    """Build the gameplay proof object used by the snapshot screen and PDF exporter."""

    state = session.get("active_town_state") or {}
    explore_flags = session.get("explore_flags") or {}
    tower_progress = session.get("tower_progress") or {}
    gym_progress = session.get("gym_progress") or session.get("gym_results") or {}

    tower = tower_summary(tower_progress) if isinstance(tower_progress, dict) else {
        "correct": 0,
        "total": 0,
        "accuracy": 0,
        "floors_cleared": 0,
        "floors_total": 4,
        "passed": False,
    }
    gym = gym_summary(gym_progress) if isinstance(gym_progress, dict) else {
        "correct": 0,
        "total": 0,
        "accuracy": 0,
        "passed": False,
        "required_correct": 12,
    }

    rooms_found = _count_true_flags(explore_flags) if isinstance(explore_flags, dict) else 0
    rooms_total = 4

    total_correct = int(tower.get("correct", 0)) + int(gym.get("correct", 0))
    total_prompts = int(tower.get("total", 0)) + int(gym.get("total", 0))
    overall_accuracy = accuracy_percent(total_correct, total_prompts)

    missed_pattern = "Stage pressure" if overall_accuracy < 80 else "Minor refinement only"
    recognition_strength = "Healthy response recognition" if gym.get("passed") else "State clue collection"

    return {
        "selected_state": state,
        "state_label": _safe_state_label(state),
        "rooms_explored": rooms_found,
        "rooms_total": rooms_total,
        "tower": tower,
        "gym": gym,
        "recognition_accuracy": overall_accuracy,
        "recognition_strength": recognition_strength,
        "missed_pattern": missed_pattern,
        "ohu_recognition_pattern": _infer_ohu_pattern(gym_progress),
        "state_movement": _infer_state_movement(overall_accuracy, bool(gym.get("passed"))),
        "next_path": _next_path(overall_accuracy, bool(gym.get("passed"))),
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
