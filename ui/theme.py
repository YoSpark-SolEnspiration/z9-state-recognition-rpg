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
  --z9-panel-3: #20242d;
  --z9-line: rgba(232, 201, 122, 0.42);
  --z9-line-soft: rgba(201, 168, 76, 0.26);
  --z9-gold: #c9a84c;
  --z9-gold-soft: #f0d789;
  --z9-cream: #fff8ea;
  --z9-text: #f5f0e8;
  --z9-muted: #d2c8b6;
  --z9-muted-2: #b9ae9a;
  --z9-success: #d7f5cf;
  --z9-warning: #ffe6a8;
}

.stApp {
  background:
    radial-gradient(circle at top left, rgba(201,168,76,.14), transparent 32rem),
    linear-gradient(135deg, #070809 0%, #101216 52%, #070809 100%);
  color: var(--z9-text);
}

.block-container {
  padding-top: 2.2rem;
  padding-bottom: 3rem;
  max-width: 1180px;
}

h1, h2, h3, h4 {
  color: var(--z9-cream);
  letter-spacing: .02em;
}

p, li, span, label, div[data-testid="stMarkdownContainer"] {
  color: var(--z9-text);
}

.z9-shell {
  border: 1px solid var(--z9-line);
  background: rgba(16,18,22,.92);
  border-radius: 24px;
  padding: 1.45rem;
  box-shadow: 0 18px 50px rgba(0,0,0,.40);
}

.z9-hero {
  border: 1px solid rgba(232,201,122,.48);
  border-radius: 28px;
  padding: 2rem;
  background:
    linear-gradient(145deg, rgba(32,36,45,.98), rgba(7,8,9,.96));
  box-shadow: inset 0 0 0 1px rgba(255,248,234,.035);
}

.z9-card {
  border: 1px solid rgba(232,201,122,.34);
  border-radius: 20px;
  padding: 1.12rem 1.2rem;
  background: rgba(245,240,232,.07);
  min-height: 100%;
  box-shadow: inset 0 0 0 1px rgba(255,248,234,.025);
}

.z9-card strong,
.z9-card b {
  color: var(--z9-cream);
}

.z9-card p,
.z9-card li,
.z9-card div[data-testid="stMarkdownContainer"] {
  color: var(--z9-text);
}

.z9-kicker {
  color: var(--z9-gold-soft);
  text-transform: uppercase;
  letter-spacing: .18em;
  font-size: .76rem;
  font-weight: 800;
}

.z9-muted { color: var(--z9-muted); }
.z9-gold { color: var(--z9-gold-soft); }
.z9-small { color: var(--z9-muted-2); font-size: .92rem; }

.z9-status-bar {
  border: 1px solid var(--z9-line-soft);
  border-radius: 18px;
  background: rgba(7,8,9,.40);
  padding: .75rem .9rem;
  margin-bottom: 1rem;
}

.z9-state-pill {
  display: inline-block;
  border: 1px solid rgba(232,201,122,.50);
  border-radius: 999px;
  padding: .34rem .78rem;
  color: var(--z9-cream);
  background: rgba(201,168,76,.13);
  font-weight: 800;
  letter-spacing: .02em;
}

.stCaption,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
  color: var(--z9-muted) !important;
}

.stButton > button {
  border-radius: 999px;
  border: 1px solid rgba(232,201,122,.62);
  background: linear-gradient(135deg, rgba(201,168,76,.34), rgba(201,168,76,.14));
  color: var(--z9-cream);
  font-weight: 800;
  min-height: 2.65rem;
}

.stButton > button:hover {
  border-color: rgba(240,215,137,.90);
  color: #ffffff;
  background: linear-gradient(135deg, rgba(201,168,76,.44), rgba(201,168,76,.20));
}

.stDownloadButton > button {
  border-radius: 999px;
  border: 1px solid rgba(232,201,122,.62);
  background: linear-gradient(135deg, rgba(201,168,76,.30), rgba(201,168,76,.12));
  color: var(--z9-cream);
  font-weight: 800;
}

div[data-testid="stMetric"] {
  border: 1px solid rgba(232,201,122,.25);
  border-radius: 16px;
  padding: .75rem .85rem;
  background: rgba(245,240,232,.055);
}

div[data-testid="stMetricLabel"] p {
  color: var(--z9-muted) !important;
}

div[data-testid="stMetricValue"] {
  color: var(--z9-gold-soft);
}

.stTabs [data-baseweb="tab-list"] {
  gap: .4rem;
}

.stTabs [data-baseweb="tab"] {
  border: 1px solid rgba(232,201,122,.26);
  border-radius: 999px;
  background: rgba(245,240,232,.045);
  color: var(--z9-muted);
  padding: .35rem .8rem;
}

.stTabs [aria-selected="true"] {
  border-color: rgba(232,201,122,.72);
  color: var(--z9-cream);
  background: rgba(201,168,76,.16);
}

.streamlit-expanderHeader {
  color: var(--z9-cream) !important;
  font-weight: 800;
}

.stRadio label,
.stSelectbox label,
.stToggle label {
  color: var(--z9-cream) !important;
  font-weight: 700;
}

hr {
  border-color: rgba(232,201,122,.22);
}

.z9-visual-frame {
  border: 1px solid rgba(232,201,122,.34);
  border-radius: 22px;
  padding: .75rem;
  background:
    linear-gradient(145deg, rgba(245,240,232,.075), rgba(7,8,9,.34));
  box-shadow: inset 0 0 0 1px rgba(255,248,234,.025);
  margin: .75rem 0 1rem 0;
}

.z9-visual-frame img {
  border-radius: 16px;
  border: 1px solid rgba(232,201,122,.22);
}

.z9-scene-row {
  border-left: 3px solid rgba(201,168,76,.75);
  padding-left: .85rem;
  margin: .7rem 0;
}


.z9-asset-slot {
  border: 1px solid rgba(232,201,122,.38);
  border-radius: 24px;
  padding: .85rem;
  background:
    radial-gradient(circle at top, rgba(201,168,76,.12), transparent 65%),
    linear-gradient(145deg, rgba(16,18,22,.96), rgba(7,8,9,.82));
  box-shadow: 0 14px 36px rgba(0,0,0,.32), inset 0 0 0 1px rgba(255,248,234,.025);
  margin: .75rem 0 1rem 0;
}

.z9-asset-slot img {
  border-radius: 18px;
  border: 1px solid rgba(232,201,122,.20);
  background: rgba(7,8,9,.35);
}

.z9-form-grid-note {
  border-left: 3px solid rgba(201,168,76,.75);
  padding: .8rem 1rem;
  background: rgba(245,240,232,.045);
  border-radius: 0 16px 16px 0;
}

.z9-recognition-card {
  border: 1px solid rgba(232,201,122,.42);
  border-radius: 24px;
  padding: .95rem;
  background:
    radial-gradient(circle at top, rgba(201,168,76,.13), transparent 64%),
    linear-gradient(145deg, rgba(16,18,22,.98), rgba(7,8,9,.86));
  box-shadow: 0 16px 42px rgba(0,0,0,.35), inset 0 0 0 1px rgba(255,248,234,.025);
  margin: .75rem 0 1rem 0;
}

.z9-recognition-card img {
  border-radius: 18px;
  border: 1px solid rgba(232,201,122,.24);
  background: rgba(7,8,9,.42);
}

.z9-form-title {
  color: var(--z9-cream);
  font-size: 1.08rem;
  font-weight: 900;
  letter-spacing: .02em;
  margin-top: .65rem;
}

.z9-form-meta {
  color: var(--z9-gold-soft);
  font-size: .9rem;
  font-weight: 800;
  margin-top: .12rem;
}

.z9-form-desc {
  color: var(--z9-text);
  margin-top: .45rem;
  margin-bottom: .25rem;
}

.z9-empty-visual {
  min-height: 210px;
  border: 1px dashed rgba(232,201,122,.34);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: var(--z9-gold-soft);
  font-size: 2.2rem;
  font-weight: 900;
  background: rgba(245,240,232,.045);
}

.z9-empty-visual span {
  color: var(--z9-muted);
  font-size: .95rem;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.z9-visual-strip {
  border: 1px solid rgba(232,201,122,.30);
  border-radius: 18px;
  padding: .75rem .95rem;
  background: rgba(245,240,232,.055);
  margin: .65rem 0 1rem 0;
  display: flex;
  flex-wrap: wrap;
  gap: .5rem 1rem;
  align-items: baseline;
}

.z9-visual-strip strong {
  color: var(--z9-cream);
}

.z9-visual-strip span:last-child {
  color: var(--z9-muted);
}


.z9-recognition-facts {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .5rem;
  margin: .75rem 0 .45rem 0;
}

.z9-recognition-facts span {
  border: 1px solid rgba(232,201,122,.22);
  border-radius: 14px;
  padding: .55rem .62rem;
  background: rgba(245,240,232,.045);
  color: var(--z9-text);
  font-size: .88rem;
}

.z9-recognition-facts b {
  display: block;
  color: var(--z9-gold-soft);
  font-size: .68rem;
  text-transform: uppercase;
  letter-spacing: .14em;
  margin-bottom: .16rem;
}

.z9-recognition-compact .z9-empty-visual {
  min-height: 150px;
}

.z9-recognition-snapshot {
  border-color: rgba(240,215,137,.62);
}

@media (max-width: 780px) {
  .z9-recognition-facts,
  .z9-scene-meta {
    grid-template-columns: 1fr;
  }
}


.z9-scene-card {
  border: 1px solid rgba(232,201,122,.38);
  border-radius: 24px;
  padding: 1rem;
  background:
    radial-gradient(circle at top left, rgba(201,168,76,.12), transparent 55%),
    linear-gradient(145deg, rgba(16,18,22,.98), rgba(7,8,9,.86));
  box-shadow: 0 14px 40px rgba(0,0,0,.34), inset 0 0 0 1px rgba(255,248,234,.025);
  margin: .75rem 0 1rem 0;
}

.z9-scene-card h3 {
  margin: .22rem 0 .75rem 0;
  color: var(--z9-cream);
}

.z9-scene-card img {
  border-radius: 18px;
  border: 1px solid rgba(232,201,122,.24);
  background: rgba(7,8,9,.42);
}

.z9-scene-placeholder {
  min-height: 220px;
  border: 1px dashed rgba(232,201,122,.34);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: var(--z9-gold-soft);
  font-size: 1.8rem;
  font-weight: 900;
  background: rgba(245,240,232,.045);
  text-transform: uppercase;
  letter-spacing: .05em;
}

.z9-scene-placeholder span {
  color: var(--z9-muted);
  font-size: .92rem;
  letter-spacing: .08em;
  margin-top: .4rem;
}

.z9-scene-meta {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .5rem;
  margin: .75rem 0 .45rem 0;
}

.z9-scene-meta span,
.z9-scene-beat,
.z9-scene-node {
  border: 1px solid rgba(232,201,122,.22);
  border-radius: 16px;
  padding: .72rem .78rem;
  background: rgba(245,240,232,.045);
  color: var(--z9-text);
}

.z9-scene-meta b {
  display: block;
  color: var(--z9-gold-soft);
  font-size: .68rem;
  text-transform: uppercase;
  letter-spacing: .14em;
  margin-bottom: .16rem;
}

.z9-scene-rule {
  border-left: 3px solid rgba(201,168,76,.78);
  padding: .72rem .9rem;
  background: rgba(245,240,232,.045);
  border-radius: 0 16px 16px 0;
  color: var(--z9-muted);
  margin-top: .7rem;
}

.z9-scene-beat,
.z9-scene-node {
  min-height: 100%;
  margin-bottom: .65rem;
}

.z9-scene-beat strong,
.z9-scene-node strong {
  color: var(--z9-cream);
  display: block;
  margin-top: .18rem;
}

.z9-scene-beat p,
.z9-scene-node p {
  color: var(--z9-text);
  margin: .45rem 0 .35rem 0;
}

.z9-scene-beat span {
  color: var(--z9-muted);
  font-size: .9rem;
}

.z9-tower-gate,
.z9-gym-arena {
  border: 1px solid rgba(232,201,122,.42);
  border-radius: 26px;
  padding: 1rem;
  background:
    radial-gradient(circle at top right, rgba(201,168,76,.14), transparent 58%),
    linear-gradient(145deg, rgba(16,18,22,.98), rgba(7,8,9,.86));
  box-shadow: 0 16px 44px rgba(0,0,0,.36), inset 0 0 0 1px rgba(255,248,234,.025);
  margin: .75rem 0 1.1rem 0;
}

.z9-tower-gate h3,
.z9-gym-arena h3 {
  margin: .22rem 0 .75rem 0;
  color: var(--z9-cream);
}

.z9-tower-gate img,
.z9-gym-arena img {
  border-radius: 18px;
  border: 1px solid rgba(232,201,122,.24);
  background: rgba(7,8,9,.42);
}

.z9-tower-signal,
.z9-round-brief {
  border: 1px solid rgba(232,201,122,.25);
  border-radius: 16px;
  padding: .72rem .82rem;
  background: rgba(245,240,232,.05);
  color: var(--z9-text);
  margin: .65rem 0 .85rem 0;
}

.z9-round-brief strong {
  color: var(--z9-cream);
}

.z9-round-brief span {
  color: var(--z9-muted);
}


</style>
"""

def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
