from __future__ import annotations

from typing import Any

from game.content_router import build_reaction_room_content


def build_reaction_alley_room(
    active_state: dict[str, Any] | None,
) -> dict[str, Any]:
    room = build_reaction_room_content(active_state)

    room.setdefault(
        "source",
        "state_content/ohu_reaction_templates.json",
    )

    return room