# FILE: tests/smoke_test.py
from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path


def test_core_non_ui_modules_import() -> None:
    modules = [
        "game.content_router",
        "game.tower_engine",
        "game.gym_engine",
        "game.session_summary",
        "reports.session_snapshot_builder",
    ]
    for module in modules:
        importlib.import_module(module)


def test_streamlit_entrypoint_is_declared() -> None:
    app_file = Path("app.py")
    assert app_file.exists()
    text = app_file.read_text(encoding="utf-8")
    assert "def main()" in text
    assert "st.set_page_config" in text
    assert "SCREEN_RENDERERS" in text


def test_requirements_include_streamlit() -> None:
    requirements = Path("requirements.txt").read_text(encoding="utf-8").lower()
    assert "streamlit" in requirements


def test_no_archive_imports_in_runtime_files() -> None:
    runtime_roots = [Path("app.py"), Path("app_state.py"), Path("game"), Path("ui"), Path("runtime"), Path("reports")]
    for root in runtime_roots:
        files = [root] if root.is_file() else list(root.rglob("*.py"))
        for file in files:
            text = file.read_text(encoding="utf-8")
            assert "archive." not in text
            assert "from archive" not in text
