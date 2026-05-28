# FILE: reports/session_snapshot_builder.py
from __future__ import annotations

from typing import Any, Dict, List

from reports.templates.snapshot_sections import build_snapshot_sections


def build_snapshot_payload(summary: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize the session summary into a report-ready payload."""

    return {
        "title": "Z9 State Recognition Session Snapshot",
        "subtitle": "Gameplay proof report",
        "state_label": summary.get("state_label", "No state selected"),
        "selected_state": summary.get("selected_state", {}),
        "metrics": {
            "rooms_explored": f"{summary.get('rooms_explored', 0)} / {summary.get('rooms_total', 4)}",
            "tower": f"{summary.get('tower', {}).get('correct', 0)} / {summary.get('tower', {}).get('total', 0)}",
            "gym": f"{summary.get('gym', {}).get('correct', 0)} / {summary.get('gym', {}).get('total', 0)}",
            "accuracy": f"{summary.get('recognition_accuracy', 0)}%",
        },
        "sections": build_snapshot_sections(summary),
    }


def snapshot_lines(payload: Dict[str, Any]) -> List[str]:
    lines = [payload.get("title", "Session Snapshot"), payload.get("subtitle", "")]
    lines.append(f"State: {payload.get('state_label', '')}")
    lines.append("")
    for key, value in payload.get("metrics", {}).items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")
    lines.append("")
    for section in payload.get("sections", []):
        lines.append(section.get("heading", ""))
        lines.append(section.get("body", ""))
        lines.append("")
    return lines
