# FILE: config.py
from __future__ import annotations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
APP_TITLE = "Z9 State Recognition RPG"
COURSE_ID = "course10"
DEFAULT_TOWN_ID = "course10_lockstep_district"
SNAPSHOT_EXPORT_DIR = REPO_ROOT / "exports"

STATE_TYPES = ["D", "I", "S", "C"]
SUBTYPES = {
    "D": ["DD", "DI", "DS", "DC"],
    "I": ["ID", "II", "IS", "IC"],
    "S": ["SD", "SI", "SS", "SC"],
    "C": ["CD", "CI", "CS", "CC"],
}
STAGES = list(range(1, 9))
OHU_OPTIONS = ["Overdeveloped", "Healthy", "Underdeveloped", "All"]
