# FILE: reports/templates/snapshot_sections.py
from __future__ import annotations

from typing import Any, Dict, List


def build_snapshot_sections(summary: Dict[str, Any]) -> List[Dict[str, str]]:
    return [
        {
            "heading": "Recognition Strength",
            "body": str(summary.get("recognition_strength", "State recognition in progress")),
        },
        {
            "heading": "Missed Pattern",
            "body": str(summary.get("missed_pattern", "No missed pattern recorded")),
        },
        {
            "heading": "OHU Recognition",
            "body": str(summary.get("ohu_recognition_pattern", "Not yet tested")),
        },
        {
            "heading": "State Movement",
            "body": str(summary.get("state_movement", "No movement recorded")),
        },
        {
            "heading": "Next Path",
            "body": str(summary.get("next_path", "Return Home and run another state simulation")),
        },
    ]
