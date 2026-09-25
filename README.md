# KupasNutri — MNC v0.1 P1 + P1-H

This repository contains the executable qualification and first health-evidence linkage passes for the **Multimodal Nutrition Corpus (MNC) v0.1**.

## P1 — 100-case qualification

- Source cases: dish IDs `10000–10099`
- Batch size: 100 contiguous records
- Purpose: schema qualification, source/API semantic audit, recipe–nutrition reconciliation screening, QC fixture estimation, and task-specific eligibility
- Important: this is **not** a representative stratified sample of the full corpus.

### P1 decision

**CONDITIONAL PASS for scale engineering.**

Do not extrapolate this batch's recipe-qualification rate to the full API corpus until a genuinely stratified P1-B batch and a human-reviewed reconciliation subset are completed.

## P1-H — first health-evidence linkage

P1-H adds the first operational:

`Dish -> NutrientObservation -> ExposureEntity -> ScientificClaim -> EvidenceBundle -> EvidenceUnit -> Source`

graph.

First-wave Gold-4 exposures:

- Dietary sodium
- Dietary potassium
- Dietary fibre
- Saturated fatty acids

Current P1-H results:

- 100 dishes
- 400 Dish–Exposure slots
- 394 evidence-linked edges
- 7 frozen ScientificClaims
- 4 EvidenceBundles
- 8 EvidenceUnits
- 788 provisional T6/T7 task seeds
- evidence-lineage errors: 0

### P1-H decision

**PASS for H1 population-level evidence linkage.**

Still blocked:

- serving/dose thresholding;
- dish-level disease labels;
- individualized nutrition/medical recommendations;
- ingredient-specific health attribution without ingredient-contribution modelling.

## Core scientific rules

1. `Raw != Normalized`
2. `Missing != Zero`
3. `Source population tag != evidence-based applicability`
4. `Recipe truth != visually observable truth`
5. `Dish-level quality != task-specific eligibility`
6. `Evidence link != recommendation`
7. `Batch percentile != clinical threshold`
8. Automated reconciliation is screening, not expert adjudication

## Reproduce P1

```bash
python scripts/process_p1_100_cases.py \
  data/raw/dish_samples_100_snapshot.csv \
  data/processed
```

## Reproduce P1-H

```bash
python scripts/build_p1h_health_links.py \
  --nutrients data/processed/nutrient_observations.csv \
  --anchors data/processed/dish_anchors.csv \
  --task-eligibility data/processed/task_eligibility.csv \
  --out data/health/generated
```

## Main outputs

### P1

- `reports/P1_100_case_qualification_report.md`
- `reports/p1_summary.json`
- `data/processed/p1_case_registry_min.csv`
- `scripts/process_p1_100_cases.py`
- `docs/MNC_v0.1_P1_processing_contract.md`

### P1-H

- `reports/P1H_100_case_health_linkage_report.md`
- `reports/p1h_summary.json`
- `data/health/exposure_registry.csv`
- `data/health/scientific_claims.csv`
- `data/health/evidence_bundles.csv`
- `data/health/evidence_units.csv`
- `data/health/health_outcomes.csv`
- `scripts/build_p1h_health_links.py`
- `docs/MNC_v0.1_P1H_health_linkage_contract.md`

Large normalized/generated tables are reproducible outputs and should not be hand-edited.
