# Asset Drop Guide — Checkpoint 3

This project now supports a placeholder-to-final-art pipeline. The app should not need code changes when final art is ready.

## Drop Rule

Replace or add PNG files at the registered final asset paths. Keep file names exact.

## Core Character Slots

Place base character renders here:

```text
assets/core/donte.png
assets/core/isaac.png
assets/core/samantha.png
assets/core/caleb.png
```

## Recognition Form Slots

Place the 16 final recognition form renders here:

```text
assets/recognition_forms/DD.png
assets/recognition_forms/DI.png
assets/recognition_forms/DS.png
assets/recognition_forms/DC.png
assets/recognition_forms/ID.png
assets/recognition_forms/II.png
assets/recognition_forms/IS.png
assets/recognition_forms/IC.png
assets/recognition_forms/SD.png
assets/recognition_forms/SI.png
assets/recognition_forms/SS.png
assets/recognition_forms/SC.png
assets/recognition_forms/CD.png
assets/recognition_forms/CI.png
assets/recognition_forms/CS.png
assets/recognition_forms/CC.png
```

## Scene Slots

Optional final scene art may be added here:

```text
assets/scenes/default_scene.png
assets/scenes/vocab_hall.png
assets/scenes/story_square.png
assets/scenes/reaction_alley.png
assets/scenes/pillar_market.png
assets/tower/tower_gate.png
assets/tower/recognition_gate.png
assets/gym/gym_arena.png
assets/gym/gym_leader.png
assets/town/default.png
```

## Validation

Before committing final art, run:

```bash
python scripts/validate_assets.py
python -m pytest -q
```

When every final art slot is intentionally filled, run:

```bash
python scripts/validate_assets.py --strict-final
```

## Important Rule

Do not rename registry keys to match art. Rename art to match the registry. The routing logic depends on stable codes such as `DD`, `IC`, and `CC`.
