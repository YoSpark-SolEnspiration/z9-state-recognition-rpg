from pathlib import Path

from scripts.validate_assets import REQUIRED_CORE, REQUIRED_FORMS, load_json, validate_registry

ROOT = Path(__file__).resolve().parents[1]


def test_visual_asset_registry_has_required_core_and_forms():
    characters = load_json(ROOT / "data" / "visual" / "character_registry.json")["characters"]
    forms = load_json(ROOT / "data" / "visual" / "recognition_form_registry.json")["forms"]

    assert set(REQUIRED_CORE).issubset(characters.keys())
    assert set(REQUIRED_FORMS).issubset(forms.keys())


def test_all_placeholder_assets_resolve_without_final_art():
    errors, warnings = validate_registry(ROOT, strict_final=False)

    assert errors == []
    assert warnings  # final art slots are allowed to be empty during placeholder phase


def test_strict_final_mode_detects_empty_final_art_slots():
    errors, _warnings = validate_registry(ROOT, strict_final=True)

    assert errors
    assert any("Final art not dropped yet" in error or "Expected final slot is empty" in error for error in errors)
