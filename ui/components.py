# FILE: ui/components.py
"""Reusable Streamlit UI components for the Z9 game demo."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
from typing import Any, Iterable, Optional

import streamlit as st

from runtime.route_state import go_to


_ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets"
_SUPPORTED_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")

_DATA_ROOT = Path(__file__).resolve().parents[1] / "data"


def load_visual_registry(name: str) -> dict[str, Any]:
    """Load a Checkpoint 3 visual registry safely for player-facing rendering."""
    path = _DATA_ROOT / "visual" / name
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def resolve_asset_slot(expected_path: str | None, fallback_path: str | None = None) -> Optional[str]:
    """Resolve final art first, then placeholder art, without exposing broken paths."""
    for raw_path in (expected_path, fallback_path):
        if not raw_path:
            continue
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = Path(__file__).resolve().parents[1] / candidate
        if candidate.exists():
            return str(candidate)
    return None


def render_asset_slot(title: str, expected_path: str | None, fallback_path: str | None = None, *, caption: str | None = None) -> bool:
    """Render final art or its placeholder inside a consistent Z9 visual frame."""
    asset = resolve_asset_slot(expected_path, fallback_path)
    if not asset:
        return False
    st.markdown('<div class="z9-asset-slot">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{escape(title)}</div>', unsafe_allow_html=True)
    st.image(asset, caption=caption, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return True


def recognition_form_asset(form_code: str) -> tuple[str | None, str | None, dict[str, Any]]:
    """Return expected/fallback asset paths for a 16-form recognition code."""
    registry = load_visual_registry("recognition_form_registry.json")
    form = registry.get("forms", {}).get(str(form_code).upper(), {})
    return form.get("final_asset_slot"), form.get("placeholder_asset"), form


def render_recognition_form(form_code: str, *, title: str | None = None) -> bool:
    """Render the selected 16-form recognition asset, falling back to its silhouette slot."""
    expected, fallback, form = recognition_form_asset(form_code)
    label = title or f"{str(form_code).upper()} Recognition Form"
    caption = form.get("label") if isinstance(form, dict) else None
    return render_asset_slot(label, expected, fallback, caption=caption)


def find_asset(folder: str, *stems: str) -> Optional[str]:
    """Return the first existing visual asset path, or None when assets are absent."""
    asset_dir = _ASSET_ROOT / folder
    if not asset_dir.exists():
        return None
    clean_stems = [stem.strip().lower().replace(" ", "_") for stem in stems if stem]
    for stem in clean_stems:
        for ext in _SUPPORTED_IMAGE_EXTS:
            candidate = asset_dir / f"{stem}{ext}"
            if candidate.exists():
                return str(candidate)
    for ext in _SUPPORTED_IMAGE_EXTS:
        matches = sorted(asset_dir.glob(f"*{ext}"))
        if matches:
            return str(matches[0])
    return None


def visual_asset(folder: str, *stems: str, caption: str | None = None, width: str = "stretch") -> bool:
    """Render an optional image without surfacing broken paths in the player flow."""
    asset = find_asset(folder, *stems)
    if not asset:
        return False
    st.image(asset, caption=caption, use_container_width=(width == "stretch"))
    return True


def visual_frame(title: str, folder: str, *stems: str, caption: str | None = None) -> bool:
    """Luxury image container for scene, room, and NPC visuals."""
    asset = find_asset(folder, *stems)
    if not asset:
        return False
    st.markdown('<div class="z9-visual-frame">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{escape(title)}</div>', unsafe_allow_html=True)
    st.image(asset, caption=caption, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return True


def state_anchor_key(state: dict | None) -> str:
    """Map the active primary DISC type to the public anchor character key."""
    if not state:
        return "z9"
    disc = str(state.get("disc_type") or state.get("type") or "").upper()[:1]
    return {"D": "donte", "I": "isaac", "S": "samantha", "C": "caleb"}.get(disc, "z9")


def hero(title: str, subtitle: str, kicker: str = "State made visible") -> None:
    st.markdown('<div class="z9-hero">', unsafe_allow_html=True)
    st.markdown(f'<div class="z9-kicker">{escape(kicker)}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="z9-muted">{escape(subtitle)}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def card(title: str, body: str, kicker: Optional[str] = None) -> None:
    st.markdown('<div class="z9-card">', unsafe_allow_html=True)
    if kicker:
        st.markdown(f'<div class="z9-kicker">{escape(kicker)}</div>', unsafe_allow_html=True)
    st.subheader(title)
    st.markdown(body)
    st.markdown("</div>", unsafe_allow_html=True)


def section_card(title: str, body: str, kicker: Optional[str] = None) -> None:
    """Compact card used by gameplay screens for state summaries and room briefs."""
    st.markdown('<div class="z9-card">', unsafe_allow_html=True)
    if kicker:
        st.markdown(f'<div class="z9-kicker">{escape(kicker)}</div>', unsafe_allow_html=True)
    st.markdown(f"**{title}**")
    st.markdown(body)
    st.markdown("</div>", unsafe_allow_html=True)


def state_pill(label: str) -> None:
    """Readable inline state label for player-facing screens."""
    st.markdown(f'<span class="z9-state-pill">{escape(label)}</span>', unsafe_allow_html=True)


def status_bar(left: str, right: str | None = None) -> None:
    """Small contrast-safe status strip for current screen and active state."""
    right_markup = f'<span class="z9-small">{escape(right)}</span>' if right else ""
    st.markdown(
        f'<div class="z9-status-bar"><span class="z9-kicker">{escape(left)}</span><br>{right_markup}</div>',
        unsafe_allow_html=True,
    )


def progress_steps(steps: Iterable[str], active_index: int = 0) -> None:
    labels = list(steps)
    if not labels:
        return
    cols = st.columns(len(labels))
    for index, label in enumerate(labels):
        with cols[index]:
            marker = "◆" if index == active_index else "◇"
            tone = "z9-gold" if index == active_index else "z9-small"
            st.markdown(f'<span class="{tone}">{marker} {escape(label)}</span>', unsafe_allow_html=True)


def nav_buttons(*, back_label: str | None = None, back_screen: str | None = None,
                next_label: str | None = None, next_screen: str | None = None,
                home: bool = True) -> None:
    """Consistent browser-demo navigation buttons for player-facing screens."""
    buttons = []
    if back_label and back_screen:
        buttons.append((back_label, back_screen))
    if next_label and next_screen:
        buttons.append((next_label, next_screen))
    if home:
        buttons.append(("Return Home", "home"))
    if not buttons:
        return

    cols = st.columns(len(buttons))
    for col, (label, screen) in zip(cols, buttons):
        with col:
            if st.button(label, use_container_width=True, key=f"nav_{label}_{screen}"):
                go_to(screen)


def developer_payload_toggle(label: str = "Show developer payloads") -> bool:
    """Explicit toggle used only where developer payload visibility is intentional."""
    if not st.session_state.get("developer_mode", False):
        return False
    return st.toggle(label, value=bool(st.session_state.get("show_developer_payloads", False)), key="show_developer_payloads")


def recognition_context_note(title: str, body: str) -> None:
    """Small companion note for recognition-card context without duplicating state payloads."""
    st.markdown(
        f'<div class="z9-form-grid-note"><strong>{escape(title)}</strong><br>{escape(body)}</div>',
        unsafe_allow_html=True,
    )
