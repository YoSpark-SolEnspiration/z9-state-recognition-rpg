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


def _as_option_text(value: Any, fallback: str = "selected pattern") -> str:
    if value is None:
        return fallback
    return str(value)


def _pressure_pack() -> dict[str, Any]:
    pack = _load_json("pressure_variation_templates.json")
    return dict(pack) if isinstance(pack, dict) else {}


def _tower_template_pack() -> dict[str, Any]:
    pack = _load_json("tower_question_templates.json")
    return dict(pack) if isinstance(pack, dict) else {}


def _gym_leader_pack(state: dict[str, Any]) -> dict[str, Any]:
    pack = _load_json("gym_leader_scene_templates.json")
    disc = get_disc_type(state)
    default = pack.get("D", {}) if isinstance(pack, dict) else {}
    return dict(pack.get(disc, default)) if isinstance(pack, dict) else {}


def tower_questions_for_state(state: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    profile = type_profile(state)
    stage = stage_pressure(state)
    reactions = ohu_reactions(state)
    templates = _tower_template_pack()
    pressure_pack = _pressure_pack()

    npc = selected_npc(state)
    disc = get_disc_type(state)
    subtype = get_subtype(state)
    ohu = get_ohu(state)

    stage_name = _as_option_text(stage.get("name"), "Trust vs. Mistrust")
    stage_need = _as_option_text(stage.get("core_need"), "stable support")
    stage_question = _as_option_text(stage.get("question"), "Can I trust what is around me?")
    stage_pressure_label = _as_option_text(stage.get("pressure"), "stage pressure")
    stage_shadow = _as_option_text(stage.get("shadow"), "support may fail")
    healthy_move = _as_option_text(stage.get("healthy_move"), "choose the next useful step")
    type_pattern = _as_option_text(profile.get("pressure_pattern"), "takes control when uncertain")
    language = _as_option_text(profile.get("language"), "state language")
    doorway = _as_option_text(profile.get("doorway"), f"{disc} doorway")

    healthy = _as_option_text(reactions.get("Healthy"), "What matters most right now?")
    over = _as_option_text(reactions.get("Overdeveloped"), "Move. I will handle it myself.")
    under = _as_option_text(reactions.get("Underdeveloped"), "Forget it. Nobody listens anyway.")

    stage_frames = templates.get("floor1_stage", {}).get("frames", [])
    disc_frames = templates.get("floor2_disc", {}).get("frames", [])
    pillar_frames = templates.get("floor3_pillars", {}).get("frames", [])
    ohu_frames = templates.get("floor4_ohu", {}).get("frames", [])

    def frame(frames: list[str], idx: int, fallback: str) -> str:
        template = frames[idx] if idx < len(frames) else fallback
        return template.format(
            npc=npc,
            disc=disc,
            subtype=subtype,
            ohu=ohu,
            language=language,
            doorway=doorway,
            pressure=stage_pressure_label,
            stage_name=stage_name,
            stage_question=stage_question,
            shadow=stage_shadow,
            type_pattern=type_pattern,
            stage_need=stage_need,
        )

    return {
        "floor1_stage": [
            make_question(
                qid="stage_1",
                prompt=frame(stage_frames, 0, f"{npc} is reacting through {stage_pressure_label}. Which stage pressure is most visible?"),
                answer=stage_name,
                options=[stage_name, stage_question, "Identity vs. Role Confusion", "Integrity vs. Despair"],
                state=state,
                lens="stage",
            ),
            make_question(
                qid="stage_2",
                prompt=frame(stage_frames, 1, f"The scene asks: {stage_question}. What core need is underneath it?"),
                answer=stage_need,
                options=[stage_need, "public praise", "perfect performance", "avoidance of feedback"],
                state=state,
                lens="stage",
            ),
            make_question(
                qid="stage_3",
                prompt=frame(stage_frames, 2, f"The shadow cue is {stage_shadow}. What healthy move stabilizes it?"),
                answer=healthy_move,
                options=[healthy_move, "speed at all costs", "emotional bypassing", "static perfection"],
                state=state,
                lens="stage",
            ),
        ],
        "floor2_disc": [
            make_question(
                qid="disc_1",
                prompt=frame(disc_frames, 0, f"{npc}'s first move shows {language}. Which DISC expression is showing?"),
                answer=f"{disc} expression",
                options=["D expression", "I expression", "S expression", "C expression"],
                state=state,
                lens="disc",
            ),
            make_question(
                qid="disc_2",
                prompt=frame(disc_frames, 1, f"Under pressure, {npc} {type_pattern}. Which pattern is being rendered?"),
                answer=type_pattern,
                options=[type_pattern, "random mood swing", "only a preference", "unrelated behavior"],
                state=state,
                lens="disc",
            ),
            make_question(
                qid="disc_3",
                prompt=frame(disc_frames, 2, f"Which response shows a healthier {disc} expression under {stage_pressure_label}?"),
                answer=healthy,
                options=[healthy, over, under, "Let's ignore the pressure."],
                state=state,
                lens="disc",
            ),
        ],
        "floor3_pillars": [
            make_question(
                qid="pillar_1",
                prompt=frame(pillar_frames, 0, f"{npc} wants progress, but the pressure response blocks it. Which pillar explains the split?"),
                answer="Cognitive Dissonance",
                options=["Cognitive Dissonance", "Social Learning", "Zone of Proximal Development", "External Reward"],
                state=state,
                lens="pillar",
            ),
            make_question(
                qid="pillar_2",
                prompt=frame(pillar_frames, 1, "The next step must stretch without breaking the player. Which pillar gives that scaffolding?"),
                answer="Zone of Proximal Development",
                options=["Zone of Proximal Development", "External Reward", "Avoidance", "Perfection"],
                state=state,
                lens="pillar",
            ),
            make_question(
                qid="pillar_3",
                prompt=frame(pillar_frames, 2, f"{npc} learns from a visible model in the room. Which pillar is active?"),
                answer="Social Learning",
                options=["Social Learning", "Self-Regulation", "Public Performance", "Role Confusion"],
                state=state,
                lens="pillar",
            ),
        ],
        "floor4_ohu": [
            make_question(
                qid="ohu_1",
                prompt=f"{ohu_frames[0] if ohu_frames else 'Which line is overdeveloped?'} Scene cue: {pressure_pack.get('mixed_ohu', {}).get('prompt', 'The same state shifts expression.')}",
                answer=over,
                options=[over, healthy, under, "Name the next useful step."],
                state=state,
                lens="ohu",
            ),
            make_question(
                qid="ohu_2",
                prompt=ohu_frames[1] if len(ohu_frames) > 1 else "Which line is healthy?",
                answer=healthy,
                options=[over, healthy, under, "Avoid the scene completely."],
                state=state,
                lens="ohu",
            ),
            make_question(
                qid="ohu_3",
                prompt=ohu_frames[2] if len(ohu_frames) > 2 else "Which line is underdeveloped?",
                answer=under,
                options=[over, healthy, under, "Force the answer."],
                state=state,
                lens="ohu",
            ),
        ],
    }


def gym_questions_for_state(state: dict[str, Any]) -> list[dict[str, Any]]:
    profile = type_profile(state)
    stage = stage_pressure(state)
    reactions = ohu_reactions(state)
    pressure_pack = _pressure_pack()
    leader = _gym_leader_pack(state)

    npc = selected_npc(state)
    disc = get_disc_type(state)
    subtype = get_subtype(state)
    ohu = get_ohu(state)

    stage_name = _as_option_text(stage.get("name"), "Trust vs. Mistrust")
    stage_need = _as_option_text(stage.get("core_need"), "stable support")
    stage_pressure_label = _as_option_text(stage.get("pressure"), "stage pressure")
    stage_question = _as_option_text(stage.get("question"), "Can I trust what is around me?")
    healthy_move = _as_option_text(stage.get("healthy_move"), "choose the next useful step")
    type_pattern = _as_option_text(profile.get("pressure_pattern"), "takes control when uncertain")
    doorway = _as_option_text(profile.get("doorway"), f"{disc} doorway")
    language = _as_option_text(profile.get("language"), "state language")

    healthy = _as_option_text(reactions.get("Healthy"), "What matters most right now?")
    over = _as_option_text(reactions.get("Overdeveloped"), "Move. I will handle it myself.")
    under = _as_option_text(reactions.get("Underdeveloped"), "Forget it. Nobody listens anyway.")

    leader_name = _as_option_text(leader.get("leader_name"), f"{npc} Mirror")
    leader_pressure = _as_option_text(leader.get("opening_pressure"), type_pattern)
    false_win = _as_option_text(leader.get("false_win"), "force the outcome")
    defeat_condition = _as_option_text(leader.get("defeat_condition"), "recognition, not strength")
    leader_resolution = _as_option_text(leader.get("healthy_resolution"), healthy)

    warm_prompt = pressure_pack.get("warm_pressure", {}).get("prompt", "The room is supportive, but {npc}'s pattern still appears.").format(
        npc=npc, doorway=doorway, pressure=stage_pressure_label
    )
    story_prompt = pressure_pack.get("story_pressure", {}).get("prompt", "{npc} carries {stage_name} across contexts.").format(
        npc=npc, stage_name=stage_name
    )

    raw = [
        ("gym_01", f"{warm_prompt} What is the visible type pressure?", f"{disc} pressure pattern"),
        ("gym_02", f"{npc} reacts as if {stage_need} is at risk. Which stage is active?", stage_name),
        ("gym_03", f"The selected stage asks, '{stage_question}' Which move keeps the state adaptive?", healthy_move),
        ("gym_04", f"Mixed OHU cue: '{over}' Which expression is showing?", "Overdeveloped"),
        ("gym_05", f"Mixed OHU cue: '{healthy}' Which expression is showing?", "Healthy"),
        ("gym_06", f"Mixed OHU cue: '{under}' Which expression is showing?", "Underdeveloped"),
        ("gym_07", f"{npc} says the goal matters, but the pressure behavior blocks it. Which pillar catches that contradiction?", "Cognitive Dissonance"),
        ("gym_08", f"{npc} pauses before reacting and chooses the next clean response. Which skill is visible?", "Self-Regulation"),
        ("gym_09", f"The room sees {npc} model a healthier {disc} response. Which learning lens is active?", "Social Learning"),
        ("gym_10", f"The next step supports {subtype} without forcing collapse. Which pillar fits?", "Zone of Proximal Development"),
        ("gym_11", f"{story_prompt} Which line stabilizes the selected state?", healthy),
        ("gym_12", f"{leader_name} {leader_pressure}. What false win is tempting the player?", false_win),
        ("gym_13", f"Which response shows the selected state dropping into resignation or withholding?", under),
        ("gym_14", f"What defeats {leader_name} in this demo?", defeat_condition),
        ("gym_15", f"After the player recognizes {npc}'s {language}, what transformation completes the Gym?", leader_resolution),
    ]

    option_bank = {
        f"{disc} pressure pattern": [f"{disc} pressure pattern", "random mood swing", "only a content preference", "unrelated behavior"],
        stage_name: [stage_name, "Integrity vs. Despair", "Identity vs. Role Confusion", "Autonomy vs. Shame & Doubt"],
        healthy_move: [healthy_move, "speed at all costs", "avoid the signal", "wait for certainty forever"],
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
        false_win: [false_win, leader_resolution, healthy, "slow down and recognize the state"],
        defeat_condition: [defeat_condition, "memorizing labels", "speed clicking", "personality judgment"],
        leader_resolution: [leader_resolution, false_win, under, "increase pressure"],
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
    reactions = ohu_reactions(state)
    scene_templates = _load_json("ptype_scene_templates.json")
    scene_index = _load_json("narrative_scene_index.json")

    disc = get_disc_type(state)
    subtype = get_subtype(state)
    ohu = get_ohu(state)
    npc = selected_npc(state)
    contexts = scene_templates.get("room_order", ["Individual", "Personal", "Professional", "Leader"])
    shapes = scene_templates.get("scene_shapes", {})
    index = scene_index.get(disc, {})

    scene_cards = []
    for context in contexts:
        scene_cards.append({
            "context": context,
            "cue": shapes.get(context, "The selected state becomes visible in a new context."),
            "visible_state": profile.get("pressure_pattern", "selected pressure pattern"),
            "recognition_move": profile.get("healthy_pattern", reactions.get("Healthy", "Name the state and choose the next useful response.")),
        })

    return {
        "title": "Story Square",
        "kicker": f"{npc} Recognition Scene",
        "source": "state_content/ptype_scene_templates.json + narrative_scene_index.json",
        "npc": npc,
        "subtype": subtype,
        "stage": get_stage(state),
        "ohu": ohu,
        "body": (
            f"{npc} carries {subtype} through {stage.get('name', 'the selected stage')} pressure. "
            f"The scene asks the player to spot {profile.get('language', 'the selected state language')} "
            f"as it shifts through {ohu} expression, not to judge the character."
        ),
        "recognition_prompt": f"Where does {npc}'s {index.get('anchor', profile.get('doorway', disc))} state become visible first?",
        "correct_pattern": profile.get("pressure_pattern", "selected state pressure"),
        "healthy_resolution": profile.get("healthy_pattern", reactions.get("Healthy", "Choose the stabilizing response.")),
        "scene_cards": scene_cards,
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