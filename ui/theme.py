# FILE: ui/theme.py
"""Visual theme for the Z9 State Recognition RPG."""
from __future__ import annotations

import streamlit as st

CSS = """
<style>
:root {
  --z9-bg: #070809;
  --z9-panel: #101216;
  --z9-panel-2: #171a20;
  --z9-line: rgba(201, 168, 76, 0.28);
  --z9-gold: #c9a84c;
  --z9-gold-soft: #e8c97a;
  --z9-cream: #f5f0e8;
  --z9-muted: #a7a093;
}
.stApp {
  background:
    radial-gradient(circle at top left, rgba(201,168,76,.10), transparent 32rem),
    linear-gradient(135deg, #070809 0%, #101216 52%, #070809 100%);
  color: var(--z9-cream);
}
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }
h1, h2, h3 { color: var(--z9-cream); letter-spacing: .02em; }
.z9-shell {
  border: 1px solid var(--z9-line);
  background: rgba(16,18,22,.88);
  border-radius: 24px;
  padding: 1.4rem;
  box-shadow: 0 18px 50px rgba(0,0,0,.35);
}
.z9-hero {
  border: 1px solid rgba(201,168,76,.34);
  border-radius: 28px;
  padding: 2rem;
  background: linear-gradient(145deg, rgba(23,26,32,.96), rgba(7,8,9,.94));
}
.z9-card {
  border: 1px solid rgba(201,168,76,.24);
  border-radius: 20px;
  padding: 1.1rem 1.2rem;
  background: rgba(245,240,232,.045);
  min-height: 100%;
}
.z9-kicker {
  color: var(--z9-gold-soft);
  text-transform: uppercase;
  letter-spacing: .18em;
  font-size: .76rem;
  font-weight: 700;
}
.z9-muted { color: var(--z9-muted); }
.z9-gold { color: var(--z9-gold-soft); }
.stButton > button {
  border-radius: 999px;
  border: 1px solid rgba(201,168,76,.42);
  background: linear-gradient(135deg, rgba(201,168,76,.22), rgba(201,168,76,.08));
  color: var(--z9-cream);
  font-weight: 700;
}
.stButton > button:hover { border-color: rgba(232,201,122,.75); color: #fff; }
div[data-testid="stMetricValue"] { color: var(--z9-gold-soft); }
</style>
"""

def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
