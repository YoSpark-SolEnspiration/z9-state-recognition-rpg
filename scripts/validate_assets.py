"""Validate Checkpoint 3 visual asset registries and fallback images.

This script is intentionally lightweight: it checks that every registered visual
slot has a usable fallback placeholder and reports which final art drops are
still missing. Missing final art is a warning, not a failure, until the final
render pass replaces placeholders.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_FORMS = [
    "DD", "DI", "DS", "DC",
    "ID", "II", "IS", "IC",
    "SD", "SI", "SS", "SC",
    "CD", "CI", "CS", "CC",
]
REQUIRED_CORE = ["donte", "isaac", "samantha", "caleb"]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_png(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    try:
        with path.open("rb") as handle:
            return handle.read(8) == PNG_SIGNATURE
    except OSError:
        return False


def relative_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).exists()


def validate_registry(root: Path, strict_final: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    visual_dir = root / "data" / "visual"
    character_registry = load_json(visual_dir / "character_registry.json")
    form_registry = load_json(visual_dir / "recognition_form_registry.json")
    slot_manifest = load_json(visual_dir / "asset_slot_manifest.json")

    characters = character_registry.get("characters", {})
    for key in REQUIRED_CORE:
        record = characters.get(key)
        if not record:
            errors.append(f"Missing core character registry record: {key}")
            continue
        base_asset = record.get("base_asset")
        if not base_asset or not relative_exists(root, base_asset):
            errors.append(f"Missing fallback/base asset for {key}: {base_asset}")

    forms = form_registry.get("forms", {})
    for code in REQUIRED_FORMS:
        record = forms.get(code)
        if not record:
            errors.append(f"Missing recognition form registry record: {code}")
            continue
        placeholder = record.get("placeholder_asset")
        final_slot = record.get("final_asset_slot")
        if not placeholder or not relative_exists(root, placeholder):
            errors.append(f"Missing placeholder asset for {code}: {placeholder}")
        elif not is_png(root / placeholder):
            errors.append(f"Placeholder is not a valid PNG for {code}: {placeholder}")
        if final_slot and not relative_exists(root, final_slot):
            message = f"Final art not dropped yet for {code}: {final_slot}"
            if strict_final:
                errors.append(message)
            else:
                warnings.append(message)

    seen_slots: set[str] = set()
    for slot in slot_manifest.get("slots", []):
        slot_id = slot.get("slot_id")
        if not slot_id:
            errors.append("Asset slot without slot_id")
            continue
        if slot_id in seen_slots:
            errors.append(f"Duplicate asset slot_id: {slot_id}")
        seen_slots.add(slot_id)

        fallback = slot.get("fallback_path")
        expected = slot.get("expected_path")
        if not fallback or not relative_exists(root, fallback):
            errors.append(f"Missing slot fallback for {slot_id}: {fallback}")
        if expected and not relative_exists(root, expected):
            message = f"Expected final slot is empty for {slot_id}: {expected}"
            if strict_final:
                errors.append(message)
            else:
                warnings.append(message)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Z9 Checkpoint 3 asset registries.")
    parser.add_argument(
        "--strict-final",
        action="store_true",
        help="Fail if final art slots are still empty. Default only requires placeholders.",
    )
    args = parser.parse_args()

    errors, warnings = validate_registry(repo_root(), strict_final=args.strict_final)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Asset validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"Asset validation passed: 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
