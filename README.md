# KupasNutri — MNC v0.1 P1 + P1-H + P1-H2

This repository contains the executable qualification and health-evidence linkage pipeline for the **Multimodal Nutrition Corpus (MNC) v0.1**.

## P1 — 100-case qualification

- Source cases: dish IDs `10000–10099`
- 100/100 structurally parseable
- 156 unique structured ingredients
- 643 ingredient lines
- Recipe screening: 23 provisional recipe-qualified, 77 HOLD
- Decision: **CONDITIONAL PASS for scale engineering**

This contiguous batch is not representative of the full corpus and must not be used as a corpus-wide admission-rate estimate.

## P1-H — first population-level health linkage

Frozen Gold-4:

- Sodium
- Potassium
- Dietary fibre
- Saturated fatty acids

Results:

- 400 candidate Dish–Exposure slots
- 394 evidence-linked edges
- 7 ScientificClaims
- 4 EvidenceBundles
- 8 EvidenceUnits
- 788 provisional T6/T7 task seeds
- evidence-lineage errors: 0

Decision: **PASS for H1 population-level evidence linkage.**

## P1-H2 — Exposure Expansion & Applicability Stress Test

Added:

- Protein
- Calcium
- Iron
- Folate / source `FolicAcid`
- Dietary cholesterol
- Purine

Results:

- 600 new candidate Dish–Exposure slots
- 590 observed nutrient edges
- 495 new evidence-linked edges
- 95 folate observations deliberately blocked by nutrient-form semantics
- 10 source-missing edges
- 11 new ScientificClaims
- 6 new EvidenceBundles
- 12 new EvidenceUnits
- 990 new T6/T7 task seeds

Cumulative health graph:

- 100 dishes
- 10 exposure families
- 1,000 candidate slots
- 889 evidence-linked edges
- 18 ScientificClaims
- 10 EvidenceBundles
- 20 EvidenceUnits
- 1,778 structured T6/T7 task seeds

Decision: **PASS_APPLICABILITY_STRESS_TEST_WITH_FOLATE_SEMANTIC_KILL_SIGNAL**

The folate block is intentional: the source field `FolicAcid` does not establish whether values represent natural food folate, synthetic folic acid, or dietary folate equivalents. The system therefore refuses to map those dish values to periconceptional NTD-prevention claims until source semantics are verified.

## Core scientific rules

1. `Raw != Normalized`
2. `Missing != Zero`
3. `Source population tag != evidence-based applicability`
4. `Recipe truth != visually observable truth`
5. `Dish-level quality != task-specific eligibility`
6. `Evidence link != recommendation`
7. `Batch percentile != clinical threshold`
8. `Population evidence != personalized advice`
9. `Food folate != folic acid != DFE`
10. Automated reconciliation is screening, not expert adjudication

## Reproduce

### P1

```bash
python scripts/process_p1_100_cases.py \
  data/raw/dish_samples_100_snapshot.csv \
  data/processed
```

### P1-H

```bash
python scripts/build_p1h_health_links.py \
  --nutrients data/processed/nutrient_observations.csv \
  --anchors data/processed/dish_anchors.csv \
  --task-eligibility data/processed/task_eligibility.csv \
  --out data/health/generated
```

### P1-H2

```bash
python scripts/build_p1h2_applicability_links.py \
  --nutrients data/processed/nutrient_observations.csv \
  --anchors data/processed/dish_anchors.csv \
  --out data/health/generated_h2
```

## Main P1-H2 assets

- `reports/P1H2_exposure_expansion_applicability_report.md`
- `reports/p1h2_summary.json`
- `data/health/exposure_registry_h2.csv`
- `data/health/scientific_claims_h2.csv`
- `data/health/evidence_bundles_h2.csv`
- `data/health/evidence_units_h2.csv`
- `data/health/applicability_stress_matrix.csv`
- `docs/MNC_v0.1_P1H2_applicability_contract.md`
- `scripts/build_p1h2_applicability_links.py`
- `data/health/P1H2_GENERATED_ARTIFACTS.md`

Large per-dish generated tables are deterministic build outputs and should not be hand-edited.
