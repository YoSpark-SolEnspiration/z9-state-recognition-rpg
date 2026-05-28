# app/results_view.py
from __future__ import annotations

from typing import Any, Dict

import streamlit as st

JsonDict = Dict[str, Any]


def render_results(results: JsonDict) -> None:
    st.subheader("Session Results")

    st.json(results.get("mission_result", {}))

    st.markdown("### Fairy Lite Snapshot")
    st.json(results.get("fairy_snapshot", {}))

    st.markdown("### Report")
    st.json(results.get("report", {}))

    st.markdown("### Upsell")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("Upgrade to Pro (Consumer)")
    with c2:
        st.button("Upgrade to Pro (Professional)")
    with c3:
        st.button("Book 1:1 Coaching")
