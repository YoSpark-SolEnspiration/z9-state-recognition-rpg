# FILE: reports/visual_report_helpers.py
"""Report-safe visual identity helpers for Checkpoint 3 snapshots.

The UI render system owns screen presentation, but reports need the same
selected character/form metadata so PDF and JSON exports prove the same visual
state that appeared during play.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from ui.visual_registry import visual_payload_for_state

_ROOT = Path(__file__).resolve().parents[1]


def resolve_report_asset(*paths: str | None) -> str | None:
    """Resolve the first existing project asset for report rendering."""
    for raw in paths:
        if not raw:
            continue
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = _ROOT / candidate
        if candidate.exists():
            return str(candidate)
    return None


def build_visual_snapshot(state: Dict[str, Any] | None) -> Dict[str, Any]:
    """Return export-safe visual metadata for the active session state."""
    visual = visual_payload_for_state(state)
    asset_path = resolve_report_asset(
        visual.get("form_final_asset"),
        visual.get("form_placeholder_asset"),
        visual.get("character_base_asset"),
    )
    return {
        "character": visual.get("character_name", "Unknown"),
        "form": visual.get("form_code", "--"),
        "disc_family": visual.get("disc_family", "Recognition Form"),
        "disc_family_color": visual.get("disc_family_color", "Gold"),
        "form_label": visual.get("form_label", "Selected recognition form"),
        "visual_rule": visual.get("visual_rule", "Same person. Different visible state expression."),
        "asset_path": asset_path,
        "asset_status": "resolved" if asset_path else "missing_placeholder_fallback",
    }


def visual_snapshot_lines(visual: Dict[str, Any]) -> list[str]:
    """Create compact text lines for PDF rendering and plain-text exports."""
    return [
        f"Visual State: {visual.get('character', 'Unknown')} / {visual.get('form', '--')}",
        f"DISC Family: {visual.get('disc_family_color', 'Gold')} / {visual.get('disc_family', 'Recognition Form')}",
        f"Form Meaning: {visual.get('form_label', 'Selected recognition form')}",
        f"Visual Rule: {visual.get('visual_rule', 'Same person. Different visible state expression.')}",
    ]
