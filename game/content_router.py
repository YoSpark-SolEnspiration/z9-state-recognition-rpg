# FILE: game/content_router.py
from __future__ import annotations

import json
import random
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_ROOT = Path("data/state_content")


@lru_cache(maxsize=16)
def _load_json(filename: str) -> Any:
    path = DATA_ROOT / filename
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def get_active_state(session: dict[str, Any]) -> dict[str, Any]:
    state = session.get("active_town_state", {})
    if not isinstance(state, dict):
        return {}
    return state


def get_disc_type(state: dict[str, Any]) -> str:
    value = state.get("disc_type") or state.get("type") or "D"
    return str(value).upper()[:1]


def get_subtype(state: dict[str, Any]) -> str:
    return str(state.get("subtype", f"{get_disc_type(state)}{get_disc_type(state)}")).upper()


def get_stage(state: dict[str, Any]) -> int:
    try:
        return int(state.get("stage", 1))
    except (TypeError, ValueError):
        return 1


def get_ohu(state: dict[str, Any]) -> str:
    return str(state.get("ohu", "Healthy"))


def get_state_label(state: dict[str, Any]) -> str:
    return str(
        state.get(
            "label",
            f"{get_subtype(state)} / Stage {get_stage(state)} / {get_ohu(state)}",
        )
    )


def type_profile(state: dict[str, Any]) -> dict[str, Any]:
    profiles = _load_json("type_profiles.json")
    disc = get_disc_type(state)
    default = profiles.get("D", {})
    return dict(profiles.get(disc, default))


def stage_pressure(state: dict[str, Any]) -> dict[str, Any]:
    stages = _load_json("stage_pressure_templates.json")
    stage_key = str(get_stage(state))
    default = stages.get("1", {})
    return dict(stages.get(stage_key, default))


def ohu_reactions(state: dict[str, Any]) -> dict[str, Any]:
    reactions = _load_json("ohu_reaction_templates.json")
    disc = get_disc_type(state)
    default = reactions.get("D", {})
    return dict(reactions.get(disc, default))


def pillar_templates(state: dict[str, Any]) -> list[dict[str, Any]]:
    templates = _load_json("pillar_market_templates.json")
    disc = get_disc_type(state)
    default = templates.get("D", [])
    return list(templates.get(disc, default))


def explore_templates(state: dict[str, Any]) -> dict[str, Any]:
    templates = _load_json("explore_room_templates.json")
    disc = get_disc_type(state)
    default = templates.get("D", {})
    return dict(templates.get(disc, default))


def selected_npc(state: dict[str, Any]) -> str:
    return str(type_profile(state).get("npc", "Donte"))


def selected_type_language(state: dict[str, Any]) -> str:
    return str(type_profile(state).get("language", "direction and control pressure"))


def deterministic_shuffle(options: list[str], seed: str) -> list[str]:
    shuffled = list(options)
    random.Random(seed).shuffle(shuffled)
    return shuffled


def make_question(
    *,
    qid: str,
    prompt: str,
    answer: str,
    options: list[str],
    state: dict[str, Any],
    lens: str,
) -> dict[str, Any]:
    seed = f"{get_state_label(state)}:{lens}:{qid}"
    shuffled = deterministic_shuffle(options, seed)

    if answer not in shuffled:
        shuffled.append(answer)

    deduped = []
    for option in shuffled:
        if option not in deduped:
            deduped.append(option)

    return {
        "id": qid,
        "prompt": prompt,
        "answer": answer,
        "options": deduped,
        "lens": lens,
    }


def tower_questions_for_state(state: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    profile = type_profile(state)
    stage = stage_pressure(state)
    reactions = ohu_reactions(state)
    npc = selected_npc(state)
    disc = get_disc_type(state)

    stage_name = stage.get("name", "Trust vs. Mistrust")
    stage_need = stage.get("core_need", "stable support")
    type_pattern = profile.get("pressure_pattern", "takes control when uncertain")

    healthy = reactions.get("Healthy", "What matters most right now?")
    over = reactions.get("Overdeveloped", "Move. I will handle it myself.")
    under = reactions.get("Underdeveloped", "Forget it. Nobody listens anyway.")

    return {
        "floor1_stage": [
            make_question(
                qid="stage_1",
                prompt=f"{npc} reacts as if {stage.get('shadow', 'support may fail')}. Which stage pressure is most visible?",
                answer=stage_name,
                options=[stage_name, "Trust vs. Mistrust", "Identity vs. Role Confusion", "Generativity vs. Stagnation"],
                state=state,
                lens="stage",
            ),
            make_question(
                qid="stage_2",
                prompt=f"The main need underneath the reaction is {stage_need}. What is the player learning to recognize?",
                answer=stage_need,
                options=[stage_need, "public praise", "perfect performance", "avoidance of feedback"],
                state=state,
                lens="stage",
            ),
            make_question(
                qid="stage_3",
                prompt=f"In Course 10 terms, the healthiest response is to adapt while restoring {stage_need}. Which concept fits?",
                answer="sustainable adaptation",
                options=["sustainable adaptation", "speed at all costs", "emotional bypassing", "static perfection"],
                state=state,
                lens="stage",
            ),
        ],
        "floor2_disc": [
            make_question(
                qid="disc_1",
                prompt=f"{npc} {type_pattern}. Which DISC expression is showing?",
                answer=f"{disc} expression",
                options=["D expression", "I expression", "S expression", "C expression"],
                state=state,
                lens="disc",
            ),
            make_question(
                qid="disc_2",
                prompt=f"Which response shows a healthier {disc} expression?",
                answer=healthy,
                options=[healthy, over, under, "Let's ignore the pressure."],
                state=state,
                lens="disc",
            ),
            make_question(
                qid="disc_3",
                prompt="The goal of this floor is not trivia. What are you practicing?",
                answer="recognizing behavior patterns",
                options=["recognizing behavior patterns", "memorizing labels", "guessing personality", "winning by speed"],
                state=state,
                lens="disc",
            ),
        ],
        "floor3_pillars": [
            make_question(
                qid="pillar_1",
                prompt=f"{npc} says they want progress, but their pressure response blocks it. Which pillar lens best explains the split?",
                answer="Cognitive Dissonance",
                options=["Cognitive Dissonance", "Social Learning", "Zone of Proximal Development", "External Reward"],
                state=state,
                lens="pillar",
            ),
            make_question(
                qid="pillar_2",
                prompt="A player keeps going because the goal is personally meaningful, not because of praise. Which Course 10/Z9 lens is strongest?",
                answer="Intrinsic Motivation",
                options=["Intrinsic Motivation", "External Reward", "Avoidance", "Perfection"],
                state=state,
                lens="pillar",
            ),
            make_question(
                qid="pillar_3",
                prompt=f"{npc} notices pressure rising, pauses, and chooses a clearer response. Which lens is visible?",
                answer="Self-Regulation",
                options=["Self-Regulation", "Public Performance", "Withdrawal", "Role Confusion"],
                state=state,
                lens="pillar",
            ),
        ],
        "floor4_ohu": [
            make_question(
                qid="ohu_1",
                prompt=f"The plan changes and {npc} says, '{over}' Which OHU expression is this?",
                answer="Overdeveloped",
                options=["Overdeveloped", "Healthy", "Underdeveloped", "Neutral"],
                state=state,
                lens="ohu",
            ),
            make_question(
                qid="ohu_2",
                prompt=f"The plan changes and {npc} says, '{healthy}' Which OHU expression is this?",
                answer="Healthy",
                options=["Overdeveloped", "Healthy", "Underdeveloped", "Avoidant"],
                state=state,
                lens="ohu",
            ),
            make_question(
                qid="ohu_3",
                prompt=f"The plan changes and {npc} says, '{under}' Which OHU expression is this?",
                answer="Underdeveloped",
                options=["Overdeveloped", "Healthy", "Underdeveloped", "Balanced"],
                state=state,
                lens="ohu",
            ),
        ],
    }


def gym_questions_for_state(state: dict[str, Any]) -> list[dict[str, Any]]:
    profile = type_profile(state)
    stage = stage_pressure(state)
    reactions = ohu_reactions(state)
    npc = selected_npc(state)
    disc = get_disc_type(state)

    stage_name = stage.get("name", "Trust vs. Mistrust")
    stage_need = stage.get("core_need", "stable support")
    type_pattern = profile.get("pressure_pattern", "takes control when uncertain")

    healthy = reactions.get("Healthy", "What matters most right now?")
    over = reactions.get("Overdeveloped", "Move. I will handle it myself.")
    under = reactions.get("Underdeveloped", "Forget it. Nobody listens anyway.")

    raw = [
        ("gym_01", f"Pressure rises and {npc} {type_pattern}. What is the visible pressure pattern?", f"{disc} pressure pattern"),
        ("gym_02", f"{npc} behaves as if the missing resource threatens {stage_need}. Which stage pressure is active?", stage_name),
        ("gym_03", "The healthiest Course 10 move is to adjust without abandoning the goal. Which concept is strongest?", "cognitive flexibility"),
        ("gym_04", f"{npc} says, '{over}' Which OHU expression is showing?", "Overdeveloped"),
        ("gym_05", f"{npc} says, '{healthy}' Which OHU expression is showing?", "Healthy"),
        ("gym_06", f"{npc} says, '{under}' Which OHU expression is showing?", "Underdeveloped"),
        ("gym_07", "Which lens notices belief and behavior moving in opposite directions?", "Cognitive Dissonance"),
        ("gym_08", "Which lens notices the person pausing before choosing a response?", "Self-Regulation"),
        ("gym_09", "Which lens notices the person learning from modeled behavior in the room?", "Social Learning"),
        ("gym_10", "Which lens notices the next reachable skill with support?", "Zone of Proximal Development"),
        ("gym_11", f"Which action best stabilizes {npc}'s selected state?", healthy),
        ("gym_12", f"Which response shows the most rigid expression of {disc} pressure?", over),
        ("gym_13", f"Which response shows collapsed or resigned expression of {disc} pressure?", under),
        ("gym_14", "What is the real skill being tested?", "recognition under pressure"),
        ("gym_15", "What should happen after recognition?", "choose a stabilizing next response"),
    ]

    option_bank = {
        f"{disc} pressure pattern": [f"{disc} pressure pattern", "random mood swing", "only a content preference", "unrelated behavior"],
        stage_name: [stage_name, "Integrity vs. Despair", "Identity vs. Role Confusion", "Autonomy vs. Shame & Doubt"],
        "cognitive flexibility": ["cognitive flexibility", "perfection", "avoidance", "speed"],
        "Overdeveloped": ["Overdeveloped", "Healthy", "Underdeveloped", "Neutral"],
        "Healthy": ["Overdeveloped", "Healthy", "Underdeveloped", "Avoidant"],
        "Underdeveloped": ["Overdeveloped", "Healthy", "Underdeveloped", "Balanced"],
        "Cognitive Dissonance": ["Cognitive Dissonance", "External Reward", "Public Performance", "Avoidance"],
        "Self-Regulation": ["Self-Regulation", "Public Performance", "Withdrawal", "Role Confusion"],
        "Social Learning": ["Social Learning", "Perfection", "Avoidance", "Speed"],
        "Zone of Proximal Development": ["Zone of Proximal Development", "Fixed Trait Labeling", "Random Guessing", "External Reward"],
        healthy: [healthy, over, under, "Ignore the pressure."],
        over: [over, healthy, under, "Pause and ask for context."],
        under: [under, healthy, over, "Name the next useful step."],
        "recognition under pressure": ["recognition under pressure", "memorizing labels", "speed clicking", "personality judgment"],
        "choose a stabilizing next response": ["choose a stabilizing next response", "assign blame", "hide the state", "increase pressure"],
    }

    questions = []

    for qid, prompt, answer in raw:
        questions.append(
            make_question(
                qid=qid,
                prompt=prompt,
                answer=answer,
                options=option_bank.get(answer, [answer, "D", "I", "S"]),
                state=state,
                lens="gym",
            )
        )

    return questions


def build_vocab_room_content(active_state: dict[str, Any] | None) -> dict[str, Any]:
    state = active_state or {}
    profile = type_profile(state)
    stage = stage_pressure(state)
    npc = selected_npc(state)

    return {
        "title": "Vocab Hall",
        "kicker": "Course 10 Language",
        "source": "state_content/explore_room_templates.json",
        "body": (
            f"{npc}'s state is expressed through {selected_type_language(state)}. "
            f"The developmental need is {stage.get('core_need', 'stability')}."
        ),
        "cards": [
            {"heading": "Sustainability", "body": "What can keep going after the first spark fades?"},
            {"heading": "Self-Regulation", "body": "What response stabilizes the state before pressure takes over?"},
            {"heading": "Adaptive Continuity", "body": "How does the goal continue without forcing the old pattern?"},
            {"heading": profile.get("name", "DISC Expression"), "body": profile.get("language", "state language loaded from profile")},
        ],
    }


def build_story_room_content(active_state: dict[str, Any] | None) -> dict[str, Any]:
    state = active_state or {}
    profile = type_profile(state)
    stage = stage_pressure(state)
    npc = selected_npc(state)

    return {
        "title": "Story Square",
        "kicker": "Recognition Scene",
        "source": "state_content/explore_room_templates.json",
        "npc": npc,
        "body": (
            f"{npc} enters a scene where {stage.get('shadow', 'pressure is active')}. "
            f"The player watches for {profile.get('pressure_pattern', 'the selected pressure pattern')} "
            f"without reducing the character to a label."
        ),
        "recognition_prompt": "What state pattern is becoming visible in the scene?",
        "correct_pattern": profile.get("pressure_pattern", "selected state pressure"),
    }


def build_reaction_room_content(active_state: dict[str, Any] | None) -> dict[str, Any]:
    state = active_state or {}
    reactions = ohu_reactions(state)

    return {
        "title": "Reaction Alley",
        "kicker": "OHU Comparison",
        "source": "state_content/ohu_reaction_templates.json",
        "scenario": "The plan changes at the last minute.",
        "npc": selected_npc(state),
        "reactions": {
            "Overdeveloped": reactions.get("Overdeveloped", "Move. I will handle it myself."),
            "Healthy": reactions.get("Healthy", "What matters most right now?"),
            "Underdeveloped": reactions.get("Underdeveloped", "Forget it. Nobody listens anyway."),
        },
    }


def build_pillar_room_content(active_state: dict[str, Any] | None) -> dict[str, Any]:
    state = active_state or {}
    npc = selected_npc(state)
    pillars = pillar_templates(state)

    if not pillars:
        pillars = [
            {"pillar": "DISC Identity", "reading": f"{npc}'s selected state shows as a recognizable behavior pattern."},
            {"pillar": "Stage Pressure", "reading": "The same behavior changes meaning when developmental pressure changes."},
            {"pillar": "Self-Regulation", "reading": "Recognition creates the pause needed for a healthier response."},
        ]

    return {
        "title": "Pillar Market",
        "kicker": "9 Pillar State Reading",
        "source": "state_content/pillar_market_templates.json",
        "npc": npc,
        "pillars": pillars,
    }