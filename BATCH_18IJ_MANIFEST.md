# Batch 18I/18J Manifest — Asset Drop Pipeline + Checkpoint 3 QA Lock

## UPDATED

- None

## NEW

- `ASSET_DROP_GUIDE.md`
- `ASSET_NAMING_CONVENTIONS.md`
- `CHECKPOINT_3_QA.md`
- `FINAL_RENDER_SYSTEM_LOCK.md`
- `BATCH_18IJ_MANIFEST.md`
- `scripts/validate_assets.py`
- `tests/asset_registry_test.py`
- `assets/core/.gitkeep`
- `assets/recognition_forms/.gitkeep`
- `assets/scenes/.gitkeep`
- `assets/town/.gitkeep`
- `assets/tower/.gitkeep`
- `assets/gym/.gitkeep`

## PURPOSE

Batch 18I establishes the final art drop pipeline.
Batch 18J establishes the Checkpoint 3 QA/final render system lock.

## QA

Run:

```bash
python scripts/validate_assets.py
python -m pytest -q
```

Expected before final art is dropped:

```text
Asset validator passes with warnings for empty final art slots.
Pytest passes.
```

## UNCHANGED

Everything not listed above.
