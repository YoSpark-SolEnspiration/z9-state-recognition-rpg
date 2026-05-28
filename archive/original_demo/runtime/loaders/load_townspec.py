# game_seed_engine/engine/town_loader.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import jsonschema

JsonDict = Dict[str, Any]


def _load_json(path: str) -> JsonDict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {p.resolve()}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_and_validate_town(town_path: str, schema_path: str) -> JsonDict:
    spec = _load_json(town_path)
    schema = _load_json(schema_path)
    jsonschema.validate(instance=spec, schema=schema)
    return spec
