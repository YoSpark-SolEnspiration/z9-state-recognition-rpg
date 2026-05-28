# FILE: tests/smoke_test.py
from __future__ import annotations

import importlib


def test_core_modules_import() -> None:
    modules = [
        "app",
        "app_state",
        "game.content_router",
        "game.tower_engine",
        "game.gym_engine",
        "game.session_summary",
        "ui.screens.home",
        "ui.screens.state_selector",
        "ui.screens.town",
        "ui.screens.explore",
        "ui.screens.battle_tower",
        "ui.screens.gym",
        "ui.screens.session_snapshot",
    ]

    for module in modules:
        importlib.import_module(module)
