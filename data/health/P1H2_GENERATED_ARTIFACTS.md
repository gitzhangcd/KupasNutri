# P1-H2 Generated Artifact Manifest

The following large tables are deterministic generated outputs and are distributed in the P1-H2 execution ZIP rather than hand-edited in GitHub:

- `data/health/dish_exposure_links_h2.csv` — 600 dish–exposure rows
- `data/health/health_task_seed_instances_h2.csv` — 990 new T6/T7 task seeds

Regenerate them with:

```bash
python scripts/build_p1h2_applicability_links.py \
  --nutrients data/processed/nutrient_observations.csv \
  --anchors data/processed/dish_anchors.csv \
  --out data/health/generated_h2
```

Frozen source registries, claims, evidence units, evidence bundles, the applicability matrix, processing contract, script, and report are committed to `main`.

The full execution package also preserves the exact generated tables for audit/replay.
