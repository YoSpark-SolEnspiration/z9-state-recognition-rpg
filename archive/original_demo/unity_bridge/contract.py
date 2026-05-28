from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class ScreenModel:
    screen_id: str
    title: str
    icon_ids: List[str]
    north_exit: Optional[str]
    south_exit: Optional[str]

def build_screen_model(town_ui: Dict[str, Any], screen_id: str) -> ScreenModel:
    screens = {s["id"]: s for s in town_ui["screens"]}
    s = screens[screen_id]
    return ScreenModel(
        screen_id=s["id"],
        title=s.get("title", s["id"]),
        icon_ids=list(s.get("icons", [])),
        north_exit=s.get("north_exit"),
        south_exit=s.get("south_exit"),
    )

def serialize_screen_model(sm: ScreenModel) -> Dict[str, Any]:
    return {
        "screen_id": sm.screen_id,
        "title": sm.title,
        "icon_ids": sm.icon_ids,
        "north_exit": sm.north_exit,
        "south_exit": sm.south_exit,
    }
