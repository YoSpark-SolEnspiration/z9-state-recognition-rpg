# Checkpoint 3 QA — Render System

Checkpoint 3 is a visual routing lock. It does not certify animation yet.

## Required Smoke States

Run these states before deployment:

```text
DD / Stage 1 / Overdeveloped
SD / Stage 6 / Healthy
IC / Stage 2 / Underdeveloped
CI / Stage 5 / Overdeveloped
CC / Stage 7 / Healthy
```

## Screen Checks

For each state, confirm:

- State Selector shows correct character and recognition form.
- Town shows correct active state and visual state card.
- Explore scenes load without broken images.
- Tower keeps the selected character/form visible.
- Gym keeps the selected character/form visible.
- Snapshot includes selected state and visual state data.
- PDF and JSON export still work.
- No raw JSON appears in player-facing screens.
- Developer payloads remain behind developer controls.

## Expected Anchor Matrix

| State | Expected Anchor | Expected Visual Family | Expected Feel |
|---|---|---|---|
| DD / Stage 1 / Overdeveloped | Donte | Red / Action | protection, trust pressure, force risk |
| SD / Stage 6 / Healthy | Samantha | Red / Action | steady closeness with protective initiative |
| IC / Stage 2 / Underdeveloped | Isaac | Blue / Structure | expression filtered through shame/doubt and withdrawal |
| CI / Stage 5 / Overdeveloped | Caleb | Purple / Expression | identity pressure, over-analysis, expressive reasoning risk |
| CC / Stage 7 / Healthy | Caleb | Blue / Structure | precision, standards, contribution, useful clarity |

## Pass Condition

Checkpoint 3 passes when the player can identify the following before reading a question:

```text
Who is the anchor?
Which recognition form is active?
Which DISC visual family is visible?
What scene is teaching the state?
```

## Not Included Yet

Checkpoint 3 does not include:

- animation
- Unity
- live HSIE integration
- full game engine expansion
- final illustrated art for every slot

Those belong after the render system is locked.
