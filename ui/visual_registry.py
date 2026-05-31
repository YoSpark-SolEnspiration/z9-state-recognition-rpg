# FILE: ui/visual_registry.py
"""Checkpoint 3 visual registry helpers.

This module keeps the State Recognition Render System separate from gameplay
logic. It reads the current selected state and resolves the visual identity that
should be shown in player-facing screens.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
_VISUAL_DATA = _ROOT / "data" / "visual"

FORM_TO_CHARACTER = {
    "DD": "donte", "DI": "donte", "DS": "donte", "DC": "donte",
    "ID": "isaac", "II": "isaac", "IS": "isaac", "IC": "isaac",
    "SD": "samantha", "SI": "samantha", "SS": "samantha", "SC": "samantha",
    "CD": "caleb", "CI": "caleb", "CS": "caleb", "CC": "caleb",
}

CHARACTER_DISPLAY_NAMES = {
    "donte": "Donte",
    "isaac": "Isaac",
    "samantha": "Samantha",
    "caleb": "Caleb",
}

DISC_FAMILY_LABELS = {
    "D": "Action / Fire Sword",
    "I": "Expression / Magic",
    "S": "Support / Wood Green",
    "C": "Structure / Blue Hood",
}

DISC_FAMILY_COLORS = {
    "D": "Red",
    "I": "Purple",
    "S": "Green",
    "C": "Blue",
}


@lru_cache(maxsize=8)
def _load_registry(filename: str) -> dict[str, Any]:
    path = _VISUAL_DATA / filename
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def get_character_registry() -> dict[str, Any]:
    return _load_registry("character_registry.json")


def get_form_registry() -> dict[str, Any]:
    return _load_registry("recognition_form_registry.json")


def normalize_form_code(state: dict[str, Any] | None) -> str:
    if not state:
        return "DD"
    subtype = str(state.get("subtype") or state.get("code") or "").upper().strip()
    if len(subtype) == 2 and subtype in FORM_TO_CHARACTER:
        return subtype

    primary = str(state.get("disc_type") or state.get("type") or "D").upper()[:1]
    if primary == "D":
        return "DD"
    if primary == "I":
        return "II"
    if primary == "S":
        return "SS"
    if primary == "C":
        return "CC"
    return "DD"


def visual_payload_for_state(state: dict[str, Any] | None) -> dict[str, Any]:
    """Return player-facing visual identity for the active state."""
    form_code = normalize_form_code(state)
    form_registry = get_form_registry()
    character_registry = get_character_registry()

    form = dict(form_registry.get("forms", {}).get(form_code, {}))
    anchor_key = form.get("anchor_character") or FORM_TO_CHARACTER.get(form_code, "donte")
    character = dict(character_registry.get("characters", {}).get(anchor_key, {}))

    primary_disc = form.get("primary_disc") or form_code[:1]
    overlay_disc = form.get("overlay_disc") or form_code[-1:]
    family = form.get("family") or DISC_FAMILY_LABELS.get(overlay_disc, "Recognition Form")

    return {
        "form_code": form_code,
        "character_key": anchor_key,
        "character_name": character.get("display_name") or CHARACTER_DISPLAY_NAMES.get(anchor_key, anchor_key.title()),
        "primary_disc": primary_disc,
        "overlay_disc": overlay_disc,
        "disc_family": family,
        "disc_family_color": DISC_FAMILY_COLORS.get(overlay_disc, "Gold"),
        "form_label": form.get("label") or f"{form_code} recognition form",
        "character_base_asset": character.get("base_asset"),
        "form_final_asset": form.get("final_asset_slot"),
        "form_placeholder_asset": form.get("placeholder_asset"),
        "visual_rule": form.get("visual_rule") or "Same person. Different visible state expression.",
    }
