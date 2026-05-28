# FILE: game/gym_engine.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from game.scoring import accuracy_percent, gym_passed

ROOT = Path(__file__).resolve().parents[1]
GYM_DIR = ROOT / "data" / "gym"
COURSE_DIR = ROOT / "data" / "course10"

ROUND_FILES = {
    "warm_pressure": GYM_DIR / "pressure_scenarios.json",
    "mixed_ohu": COURSE_DIR / "gym_questions.json",
    "story_pressure": COURSE_DIR / "jordan_scenarios.json",
    "gym_leader": GYM_DIR / "boss_sequences.json",
}


def _load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def get_gym_rules() -> Dict[str, Any]:
    return _load_json(GYM_DIR / "evaluation_rules.json", {"total_prompts": 15, "required_correct": 12})


def get_gym_rounds() -> List[Dict[str, Any]]:
    rounds: List[Dict[str, Any]] = []
    for key, path in ROUND_FILES.items():
        data = _load_json(path, {})
        rounds.append({
            "key": key,
            "title": data.get("title", key.replace("_", " ").title()),
            "purpose": data.get("purpose", "Recognize the selected state under pressure."),
            "questions": data.get("questions", []),
        })
    return rounds


def get_gym_round(round_key: str) -> Dict[str, Any]:
    for gym_round in get_gym_rounds():
        if gym_round["key"] == round_key:
            return gym_round
    return get_gym_rounds()[0]


def evaluate_gym_round(round_key: str, selected_answers: Dict[str, str]) -> Dict[str, Any]:
    gym_round = get_gym_round(round_key)
    results = []
    for q in gym_round.get("questions", []):
        qid = q.get("id")
        chosen = selected_answers.get(qid)
        answer = q.get("answer")
        results.append({
            "id": qid,
            "chosen": chosen,
            "answer": answer,
            "is_correct": chosen == answer,
            "hint": q.get("hint", "Return to Explore or Battle Tower and review the recognition clue."),
        })
    correct = sum(1 for item in results if item["is_correct"])
    return {
        "round_key": round_key,
        "correct": correct,
        "total": len(results),
        "passed": len(results) > 0 and correct >= max(1, round(len(results) * 0.67)),
        "results": results,
    }


def gym_summary(progress: Dict[str, Any]) -> Dict[str, Any]:
    rules = get_gym_rules()
    correct = 0
    total = 0
    for result in progress.values():
        if isinstance(result, dict):
            correct += int(result.get("correct", 0))
            total += int(result.get("total", 0))
    required = int(rules.get("required_correct", 12))
    return {
        "correct": correct,
        "total": total,
        "required_correct": required,
        "accuracy": accuracy_percent(correct, total),
        "passed": gym_passed(correct, total, required),
        "rounds_completed": len([v for v in progress.values() if isinstance(v, dict) and v.get("total", 0) > 0]),
        "rounds_total": len(get_gym_rounds()),
    }
