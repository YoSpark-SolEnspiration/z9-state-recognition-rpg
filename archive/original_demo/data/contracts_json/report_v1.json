# runtime/validators/validate_townspec.py
from __future__ import annotations

from typing import Any, Dict

import jsonschema

JsonDict = Dict[str, Any]


def validate_townspec(townspec: JsonDict, schema: JsonDict) -> None:
    """
    Fail-closed TownSpec validation.

    1) Validate against the authoritative JSON schema (TownSpec.schema.json).
    2) Enforce demo's additional contract requirement:
       town.runtime_contract_notes.ui.rules.gymBoss must exist.

    Raises:
      - jsonschema.ValidationError on schema failure
      - ValueError on missing required contract paths
    """
    jsonschema.validate(instance=townspec, schema=schema)

    # Extra contract requirement for demo loop
    if not isinstance(townspec, dict):
        raise ValueError("TownSpec must be a JSON object at root.")

    town = townspec.get("town")
    if not isinstance(town, dict):
        raise ValueError("TownSpec missing required object: town")

    rcn = town.get("runtime_contract_notes")
    if not isinstance(rcn, dict):
        raise ValueError("TownSpec missing required object: town.runtime_contract_notes")

    ui = rcn.get("ui")
    if not isinstance(ui, dict):
        raise ValueError("TownSpec missing required object: town.runtime_contract_notes.ui")

    rules = ui.get("rules")
    if not isinstance(rules, dict):
        raise ValueError("TownSpec missing required object: town.runtime_contract_notes.ui.rules")

    gym_boss = rules.get("gymBoss")
    if not isinstance(gym_boss, dict):
        raise ValueError("TownSpec missing required object: town.runtime_contract_notes.ui.rules.gymBoss")
