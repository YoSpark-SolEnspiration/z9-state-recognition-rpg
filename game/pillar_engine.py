from __future__ import annotations

from typing import Any

from game.content_router import build_pillar_room_content


def build_pillar_market_room(
    active_state: dict[str, Any] | None,
) -> dict[str, Any]:
    room = build_pillar_room_content(active_state)

    room.setdefault(
        "source",
        "state_content/pillar_market_templates.json",
    )

    return room