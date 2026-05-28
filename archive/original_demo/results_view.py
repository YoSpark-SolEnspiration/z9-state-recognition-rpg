# engine_client.py
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Tuple

JsonDict = Dict[str, Any]


def _find_repo_root(start: Path) -> Path:
    """
    Find repo root by walking upward until we see 'data/' and 'runtime/'.
    This makes imports + pathing stable even if files are moved.
    """
    cur = start.resolve()
    for _ in range(8):
        if (cur / "data").is_dir() and (cur / "runtime").is_dir():
            return cur
        cur = cur.parent
    return start.resolve().parent


REPO_ROOT = _find_repo_root(Path(__file__).resolve())


def _stable_seed(disc_signature: str, course_id: str, session_id: str) -> str:
    raw = f"{disc_signature}|{course_id}|{session_id}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def start_session(
    disc_profile: JsonDict,
    course_id: str,
    townspec_path: str,
    schema_path: str,
) -> Tuple[str, str, JsonDict, JsonDict]:
    # Keep it deterministic-ish but unique: timestamp-based session id
    session_id = f"sess_{int(time.time())}"
    seed = _stable_seed(str(disc_profile.get("signature", "no_sig")), course_id, session_id)

    from runtime.loaders.load_townspec import load_and_validate_townspec  # local import to avoid packaging issues

    townspec = load_and_validate_townspec(townspec_path, schema_path)

    state: JsonDict = {
        "session_id": session_id,
        "seed": seed,
        "course_id": course_id,
        "shards": 0,
        "tower_level": 0,
        "gym_layer": 0,
        "gym_attempts_used": 0,
        "boss": {
            "attempt": 0,
            "q_index": 0,
            "correct": 0,
            "misses": 0,
            "done": False,
            "outcome": None,
            "soft_fail_flag": False,
        },
        "kah_progress": 0,
        "session_over": False,
    }
    return session_id, seed, townspec, state


def _load_question_pool(repo_root: Path, pool_id: str) -> JsonDict:
    pools_path = repo_root / "content" / "registries" / "question_pools.json"
    pools = json.loads(pools_path.read_text(encoding="utf-8"))
    pool = pools.get("pools", {}).get(pool_id)
    if not isinstance(pool, dict):
        available = list(pools.get("pools", {}).keys())
        raise KeyError(f"Question pool '{pool_id}' not found. Available pools: {available}")
    return pool


def _get_gym_boss_rules(townspec: JsonDict) -> JsonDict:
    town = townspec.get("town", {})
    rcn = town.get("runtime_contract_notes", {})
    ui = rcn.get("ui")
    if not isinstance(ui, dict):
        available = list(rcn.keys()) if isinstance(rcn, dict) else []
        raise KeyError(
            "TownSpec missing required path: town.runtime_contract_notes.ui\n"
            f"Available keys under runtime_contract_notes: {available}\n"
            "Fix: add runtime_contract_notes.ui with ui.rules.gymBoss."
        )
    rules = ui.get("rules")
    if not isinstance(rules, dict) or "gymBoss" not in rules:
        available_rules = list(rules.keys()) if isinstance(rules, dict) else []
        raise KeyError(
            "TownSpec missing required path: town.runtime_contract_notes.ui.rules.gymBoss\n"
            f"Available rules: {available_rules}\n"
            "Fix: add ui.rules.gymBoss with pool_id + thresholds."
        )
    gym_boss = rules["gymBoss"]
    if not isinstance(gym_boss, dict):
        raise ValueError("ui.rules.gymBoss must be an object.")
    return gym_boss


def boss_submit_answer(
    repo_root: Path,
    townspec: JsonDict,
    state: JsonDict,
    is_correct: bool,
) -> JsonDict:
    ui_rules = _get_gym_boss_rules(townspec)

    pool_id = str(ui_rules["pool_id"])
    _pool = _load_question_pool(repo_root, pool_id)  # loaded for presence + future deterministic selection

    hard_fail = int(ui_rules["hard_fail_misses"])       # 5
    soft_fail = int(ui_rules["soft_fail_misses"])       # 4
    pass_min = int(ui_rules["pass_correct_min"])        # 12
    total_q = int(ui_rules["questions_per_attempt"])    # 15
    max_attempts = int(ui_rules["max_attempts_per_session"])  # 3

    boss = state["boss"]
    if boss.get("done"):
        return state

    if is_correct:
        boss["correct"] += 1
    else:
        boss["misses"] += 1

    # Hard fail: miss >= 5 => instant blackout/reset
    if boss["misses"] >= hard_fail:
        boss["done"] = True
        boss["outcome"] = "hard_fail_blackout"
        state["gym_attempts_used"] += 1
        # Session ends if we hit max attempts
        if state["gym_attempts_used"] >= max_attempts:
            state["session_over"] = True
        return state

    boss["q_index"] += 1

    # Soft-fail flag: miss >= 4 means run may continue but will be FAIL at end
    if boss["misses"] >= soft_fail:
        boss["soft_fail_flag"] = True

    # Finish run at 15 answers
    if boss["q_index"] >= total_q:
        boss["done"] = True
        if boss["correct"] >= pass_min and boss["misses"] < soft_fail:
            boss["outcome"] = "pass"
        else:
            boss["outcome"] = "fail"
        state["gym_attempts_used"] += 1

        # End session after 3 attempts if not passed
        if state["gym_attempts_used"] >= max_attempts and boss.get("outcome") != "pass":
            state["session_over"] = True

    return state


def finalize_session(disc_profile: JsonDict, state: JsonDict) -> JsonDict:
    mission_result = {
        "version": "v1",
        "session_id": state["session_id"],
        "course_id": state["course_id"],
        "town_id": "town_c10",
        "seed": state["seed"],
        "score": {"total": state["shards"]},
        "tower": {"level": state["tower_level"]},
        "gym": {"attempts_used": state["gym_attempts_used"], "boss": state["boss"]},
        "disc_deltas": {"D": 0.01, "I": 0.0, "S": 0.0, "C": 0.0},
        "shards_earned": state["shards"],
        "kah_progress": 1,
    }

    fairy_snapshot = {
        "version": "v1",
        "session_id": state["session_id"],
        "tone": "lite",
        "summary": "System integrity check complete. Keep the loop holding under pressure.",
        "next_suggestion": "Run the Gym again and reduce misses before attempt 3.",
    }

    report = {
        "version": "v1",
        "session_id": state["session_id"],
        "headline": "Course 10 Demo Report",
        "sections": [
            {"title": "Gym", "body": f"Boss outcome: {state['boss'].get('outcome')}"},
            {"title": "Attempts", "body": f"Attempts used: {state['gym_attempts_used']} / 3"},
            {"title": "Kah", "body": "Progress: 1/5"},
        ],
        "downloads": [],
    }

    return {"mission_result": mission_result, "fairy_snapshot": fairy_snapshot, "report": report}
