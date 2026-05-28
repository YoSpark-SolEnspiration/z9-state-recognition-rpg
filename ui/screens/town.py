# FILE: ui/screens/town.py

import streamlit as st

from runtime.route_state import go_to
from runtime.session_flags import get_flag


ROOMS = [
    {
        "id": "vocab_hall",
        "title": "📘 Vocab Hall",
        "flag": "vocab_complete",
        "description": "Learn the Course 10 language that defines the selected state.",
    },
    {
        "id": "story_square",
        "title": "🎭 Story Square",
        "flag": "story_complete",
        "description": "Watch the state appear through NPC behavior and pressure.",
    },
    {
        "id": "reaction_alley",
        "title": "🧠 Reaction Alley",
        "flag": "reaction_complete",
        "description": "Compare Overdeveloped, Healthy, and Underdeveloped reactions.",
    },
    {
        "id": "pillar_market",
        "title": "🛒 Pillar Market",
        "flag": "pillar_complete",
        "description": "Recognize how the same state appears across the 9 pillars.",
    },
]


def render_town_screen(app_state):
    active = app_state.get("active_town_state", {})

    st.title("The Lockstep District")
    st.caption("Recognition Village")

    st.markdown(
        f"""
**Active State**
- Type: `{active.get("type", "D")}`
- Subtype/Wing: `{active.get("subtype", "DD")}`
- Stage: `{active.get("stage", 1)}`
- OHU: `{active.get("ohu", "Overdeveloped")}`
"""
    )

    st.divider()

    st.subheader("Explore the Town")

    cols = st.columns(2)

    for index, room in enumerate(ROOMS):
        with cols[index % 2]:
            completed = get_flag(app_state, room["flag"])

            with st.container(border=True):
                st.markdown(f"### {room['title']}")
                st.write(room["description"])

                if completed:
                    st.success("Completed")

                if st.button(
                    "Enter Room",
                    key=f"enter_{room['id']}",
                    use_container_width=True,
                ):
                    app_state["explore_room"] = room["id"]
                    go_to("explore")
                    st.rerun()

    st.divider()

    completed_count = sum(
        1 for room in ROOMS if get_flag(app_state, room["flag"])
    )

    st.subheader("Recognition Progress")
    st.progress(completed_count / len(ROOMS))
    st.write(f"{completed_count} / {len(ROOMS)} rooms explored")

    if completed_count == len(ROOMS):
        st.success("Battle Tower unlocked.")

        if st.button("Enter Battle Tower", use_container_width=True):
            go_to("battle_tower")
            st.rerun()
    else:
        st.info("Explore all four town areas to unlock the Battle Tower.")

    st.divider()

    if st.button("Return Home"):
        go_to("home")
        st.rerun()