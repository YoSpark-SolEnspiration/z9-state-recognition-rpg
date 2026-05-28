# game_seed_engine/engine/runner.py
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from game_seed_engine.engine.town_state import TownState

JsonDict = Dict[str, Any]


def _grade_rank(g: str) -> int:
    order = ["none", "bronze", "silver", "gold", "platinum"]
    return order.index(g) if g in order else 0


def _award_unlock(state: TownState, key: str, current_grade: str, required: str) -> None:
    if _grade_rank(current_grade) >= _grade_rank(required):
        token = f"unlock:{key}"
        if token not in state.unlocks_awarded:
            state.unlocks_awarded.append(token)


def _index(spec: JsonDict) -> Tuple[Dict[str, str], Dict[str, Any]]:
    """Return node_id->zone_id and zone_id->zone objects."""
    node_to_zone: Dict[str, str] = {}
    zone_by_id: Dict[str, Any] = {}

    town = spec["town"]
    for area in town.get("areas", []):
        for zone in area.get("zones", []):
            zid = zone["zone_id"]
            zone_by_id[zid] = zone
            for node in zone.get("node_specs", []):
                node_to_zone[node["node_id"]] = zid

    return node_to_zone, zone_by_id


def _recompute_zone(spec: JsonDict, state: TownState, zone_id: str) -> None:
    node_to_zone, zone_by_id = _index(spec)
    zone = zone_by_id[zone_id]

    # Average best scores for nodes in this zone
    scores: List[float] = []
    for n in zone.get("node_specs", []):
        nid = n["node_id"]
        if nid in state.node_best_score_pct:
            scores.append(float(state.node_best_score_pct[nid]))

    zone_score = sum(scores) / len(scores) if scores else 0.0
    state.zone_score_pct[zone_id] = float(zone_score)

    # Clear rules from TownSpec
    town = spec["town"]
    rules = town["coverage"]["zone_clear_rules"][zone["zone_type"]]
    min_nodes = int(rules["min_node_completions"])
    min_score = float(rules["min_score_pct"])

    completed_nodes = sum(
        1 for n in zone.get("node_specs", []) if n["node_id"] in state.node_best_score_pct
    )

    state.zone_cleared[zone_id] = (completed_nodes >= min_nodes) and (zone_score >= min_score)


def _recompute_town(spec: JsonDict, state: TownState) -> None:
    town = spec["town"]
    node_to_zone, zone_by_id = _index(spec)

    weights = town["coverage"]["zone_type_weights"]

    # group zones by type
    zones_by_type: Dict[str, List[str]] = {}
    for zid, z in zone_by_id.items():
        zones_by_type.setdefault(z["zone_type"], []).append(zid)

    coverage = 0.0
    for ztype, zids in zones_by_type.items():
        avg = 0.0
        if zids:
            avg = sum(state.zone_score_pct.get(zid, 0.0) for zid in zids) / len(zids)
        coverage += float(weights.get(ztype, 0.0)) * float(avg)

    state.town_coverage_pct = float(coverage)

    # grade
    grade = "none"
    for g in town["grading"]["grades"]:
        if state.town_coverage_pct >= float(g["min_pct"]):
            grade = g["grade"]
    state.town_grade = grade

    # unlocks
    unlock = town["unlock_rules"]
    _award_unlock(state, "next_town", grade, unlock["unlock_next_town_on_grade_at_least"])
    _award_unlock(state, "time_trials", grade, unlock["unlock_time_trials_on_grade_at_least"])
    _award_unlock(state, "open_review", grade, unlock["unlock_open_review_on_grade_at_least"])
    _award_unlock(state, "elite8", grade, unlock["unlock_elite8_on_grade_at_least"])


def complete_node(spec: JsonDict, state: TownState, node_id: str, score_pct: float, time_ms: int) -> None:
    # node stats
    state.node_attempts[node_id] = state.node_attempts.get(node_id, 0) + 1
    prev = float(state.node_best_score_pct.get(node_id, 0.0))
    state.node_best_score_pct[node_id] = max(prev, float(score_pct))

    # update zone + town
    node_to_zone, zone_by_id = _index(spec)
    zid = node_to_zone.get(node_id)
    if zid is None:
        raise KeyError(f"node_id not found in spec: {node_id}")

    _recompute_zone(spec, state, zid)
    _recompute_town(spec, state)
