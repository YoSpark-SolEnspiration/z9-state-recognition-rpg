# unity_bridge/stub_runtime.py
from __future__ import annotations

from typing import Any, Dict

JsonDict = Dict[str, Any]


def get_screen_model(townspec: JsonDict, state: JsonDict, screen_id: str) -> JsonDict:
    """
    Minimal Unity stub: returns a 'screen model' derived from town.runtime_contract_notes.ui
    so Unity (later) can render without the engine owning layout.
    """
    ui = townspec.get("town", {}).get("runtime_contract_notes", {}).get("ui", {})
    screens = {s.get("id"): s for s in ui.get("screens", []) if isinstance(s, dict)}
    screen = screens.get(screen_id, {"id": screen_id, "title": screen_id, "icons": []})

    return {
        "screen_id": screen.get("id"),
        "title": screen.get("title"),
        "icons": screen.get("icons", []),
        "north_exit": screen.get("north_exit"),
        "south_exit": screen.get("south_exit"),
        "state": {
            "shards": state.get("shards", 0),
            "tower_level": state.get("tower_level", 0),
            "gym_attempts_used": state.get("gym_attempts_used", 0),
            "boss": state.get("boss", {})
        }
    }


def submit_click_event(state: JsonDict, icon_id: str) -> JsonDict:
    """
    Stub click handler. For now, just record last clicked icon.
    Engine transitions happen in engine_client/runner, not here.
    """
    state["last_click"] = icon_id
    return state
