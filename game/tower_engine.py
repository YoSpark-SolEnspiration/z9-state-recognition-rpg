# FILE: game/tower_engine.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from game.scoring import accuracy_percent

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "tower"

FLOOR_FILES = {
    "stage": DATA_DIR / "floor1_stage.json",
    "disc": DATA_DIR / "floor2_disc.json",
    "pillars": DATA_DIR / "floor3_pillars.json",
    "ohu": DATA_DIR / "floor4_ohu.json",
}


def _load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def get_tower_floors() -> List[Dict[str, Any]]:
    floors: List[Dict[str, Any]] = []
    for key, path in FLOOR_FILES.items():
        data = _load_json(path, {})
        floors.append({
            "key": key,
            "title": data.get("title", key.title()),
            "purpose": data.get("purpose", "Recognition practice."),
            "questions": data.get("questions", []),
            "required_correct": data.get("required_correct", 2),
        })
    return floors


def get_floor(floor_key: str) -> Dict[str, Any]:
    for floor in get_tower_floors():
        if floor["key"] == floor_key:
            return floor
    return get_tower_floors()[0]


def evaluate_floor(floor_key: str, selected_answers: Dict[str, str]) -> Dict[str, Any]:
    floor = get_floor(floor_key)
    results = []
    for q in floor.get("questions", []):
        qid = q.get("id")
        chosen = selected_answers.get(qid)
        correct = q.get("answer")
        results.append({
            "id": qid,
            "chosen": chosen,
            "answer": correct,
            "is_correct": chosen == correct,
            "hint": q.get("hint", "Return to Explore and collect more recognition clues."),
        })
    correct_count = sum(1 for r in results if r["is_correct"])
    total = len(results)
    required = int(floor.get("required_correct", 2))
    return {
        "floor_key": floor_key,
        "correct": correct_count,
        "total": total,
        "required": required,
        "passed": correct_count >= required,
        "results": results,
    }


def tower_summary(progress: Dict[str, Any]) -> Dict[str, Any]:
    floors = get_tower_floors()
    correct = 0
    total = 0
    cleared: List[str] = []

    for floor in floors:
        key = floor["key"]
        result = progress.get(key, {}) if isinstance(progress, dict) else {}
        if isinstance(result, dict):
            correct += int(result.get("correct", 0))
            total += int(result.get("total", 0))
            if result.get("passed"):
                cleared.append(key)

    return {
        "correct": correct,
        "total": total,
        "accuracy": accuracy_percent(correct, total),
        "passed": len(cleared) >= len(floors),
        "floors_total": len(floors),
        "floors_cleared": len(cleared),
        "cleared_keys": cleared,
        "qualified_for_gym": len(cleared) >= len(floors),
    }
