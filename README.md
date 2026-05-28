# FILE: README.md
# Z9 State Recognition RPG

Clean rebuild repo for the Z9 demo as a self-contained video-game-style state-recognition experience.

## Core rule
The game is the center. Every screen must help the player recognize the selected state.

## Locked loop
1. Home Screen
2. Manual State Selector
3. Town
4. Explore
5. Battle Tower
6. Gym
7. Session Snapshot
8. PDF Download
9. Reset Home

## Batch 1 scope
This package creates the clean gameplay-first repo structure, preserves required deterministic/data files from the previous demo, and isolates debug/developer material away from the player flow.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
