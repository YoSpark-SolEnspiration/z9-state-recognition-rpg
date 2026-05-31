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

## Checkpoint 2B Completion Patch

This patch expands the demo content libraries so type, stage, and OHU routing no longer default to Donte/D-pressure language across the full loop.

### Current Public Demo Flow
Home → Manual State Selector → Town → Explore → Battle Tower → Gym → Session Snapshot → PDF/JSON Export → Return Home

### Recognition Anchors
- D routes to Donte: action, direction, urgency, ownership.
- I routes to Isaac: expression, energy, morale, visibility.
- S routes to Samantha: support, stability, pacing, trust.
- C routes to Caleb: precision, standards, accuracy, structure.

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```


### QA
```bash
python -m pytest -q
```

### Commit Run
``` 
git status

git add .

git commit -m "Checkpoint 3A - Images"

git push origin main

git tag -a checkpoint-3A -m "User Flow Locked"
git push origin checkpoint-3A
```

Expected result for this patch: all tests pass, no archive imports, and the Streamlit entrypoint remains `app.py`.
