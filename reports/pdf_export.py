# FILE: reports/pdf_export.py
from __future__ import annotations

from io import BytesIO
from typing import Any, Dict

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from reports.session_snapshot_builder import build_snapshot_payload, snapshot_lines
from reports.templates.snapshot_styles import GOLD, SLATE, CREAM


def build_snapshot_pdf(summary: Dict[str, Any]) -> bytes:
    """Create a simple branded PDF from the gameplay snapshot summary."""

    payload = build_snapshot_payload(summary)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    margin = 0.72 * inch
    y = height - margin

    c.setFillColor(SLATE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, y, payload.get("title", "Session Snapshot"))
    y -= 22

    c.setFillColor(CREAM)
    c.setFont("Helvetica", 11)
    c.drawString(margin, y, payload.get("subtitle", "Gameplay proof report"))
    y -= 28

    c.setStrokeColor(GOLD)
    c.line(margin, y, width - margin, y)
    y -= 26

    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, f"State: {payload.get('state_label', '')}")
    y -= 22

    c.setFont("Helvetica", 10)
    for line in snapshot_lines(payload)[3:]:
        if y < margin:
            c.showPage()
            c.setFillColor(SLATE)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            c.setFillColor(CREAM)
            y = height - margin
        if not line:
            y -= 8
            continue
        if len(line) > 92:
            chunks = _wrap(line, 92)
        else:
            chunks = [line]
        for chunk in chunks:
            c.drawString(margin, y, chunk)
            y -= 14

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        test = " ".join(current + [word])
        if len(test) > width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines
