# CHECKPOINT 2A QA — State Differentiation Validation

## Purpose

This QA pass confirms that the browser demo no longer behaves like one DD/Donte content path with different labels.

Checkpoint 2A is complete when selected states produce different:

- NPC anchor
- DISC type language
- stage pressure
- OHU tone
- Tower prompts
- Gym pressure scenes

## Required test states

1. DD / Stage 1 / Overdeveloped
2. SD / Stage 6 / Healthy
3. IC / Stage 2 / Underdeveloped
4. CI / Stage 5 / Overdeveloped

## Manual browser test

For each state:

1. Start at Home.
2. Select the state.
3. Enter Town.
4. Enter Explore.
5. Confirm the room content matches the selected type/NPC.
6. Enter Tower.
7. Confirm Tower prompts use the correct NPC and type language.
8. Enter Gym.
9. Confirm Gym prompts use the correct NPC and type language.
10. Export Snapshot.

## Expected NPC routing

- D routes to Donte
- I routes to Isaac
- S routes to Samantha
- C routes to Caleb

## Python test command

Run this from repo root:

python -m pytest tests

If pytest is not installed:

python -m pip install pytest
python -m pytest tests

## Checkpoint 2A pass condition

Checkpoint 2A passes when:

- all tests pass
- no Donte/DD leakage appears in S/I/C test paths unless deliberately used as a supporting NPC later
- Tower and Gym metrics carry into Snapshot
- Explore, Tower, and Gym all reflect the selected state
