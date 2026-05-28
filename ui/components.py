# FILE: ui/components.py
"""Reusable Streamlit UI components for the Z9 game demo."""
from __future__ import annotations

from typing import Iterable, Optional

import streamlit as st


def hero(title: str, subtitle: str, kicker: str = "State made visible") -> None:
    st.markdown('<div class="z9-hero">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="z9-muted">{subtitle}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def card(title: str, body: str, kicker: Optional[str] = None) -> None:
    st.markdown('<div class="z9-card">', unsafe_allow_html=True)
    if kicker:
        st.markdown(f'<div class="z9-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.subheader(title)
    st.markdown(body)
    st.markdown("</div>", unsafe_allow_html=True)


def section_card(title: str, body: str, kicker: Optional[str] = None) -> None:
    """Compact card used by gameplay screens for state summaries and room briefs."""
    st.markdown('<div class="z9-card">', unsafe_allow_html=True)
    if kicker:
        st.markdown(f'<div class="z9-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f"**{title}**")
    st.markdown(body)
    st.markdown("</div>", unsafe_allow_html=True)


def progress_steps(steps: Iterable[str], active_index: int = 0) -> None:
    labels = list(steps)
    if not labels:
        return
    cols = st.columns(len(labels))
    for index, label in enumerate(labels):
        with cols[index]:
            marker = "◆" if index == active_index else "◇"
            st.caption(f"{marker} {label}")
