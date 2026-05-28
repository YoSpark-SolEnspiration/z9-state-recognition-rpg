# app/disc_profile.py
from __future__ import annotations

import hashlib
from typing import Dict, Any

import streamlit as st

JsonDict = Dict[str, Any]


def _stable_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def render_disc_builder() -> JsonDict:
    st.subheader("DISC Builder (Demo)")

    mode = st.radio("Choose profile mode", ["Preset (fast)", "Manual weights"], horizontal=True)

    if mode == "Preset (fast)":
        preset = st.selectbox("Preset", ["D", "I", "S", "C"])
        weights = {"D": 0.0, "I": 0.0, "S": 0.0, "C": 0.0}
        weights[preset] = 1.0
    else:
        d = st.slider("D", 0.0, 1.0, 0.25, 0.01)
        i = st.slider("I", 0.0, 1.0, 0.25, 0.01)
        s = st.slider("S", 0.0, 1.0, 0.25, 0.01)
        c = st.slider("C", 0.0, 1.0, 0.25, 0.01)
        total = max(0.0001, d + i + s + c)
        weights = {"D": d / total, "I": i / total, "S": s / total, "C": c / total}

    primary = max(weights, key=weights.__getitem__)
    signature = _stable_hash(f"{primary}:{weights}")

    st.caption(f"Primary: {primary} | signature: {signature}")

    return {
        "weights": weights,
        "primary": primary,
        "signature": signature,
    }
