# KupasNutri — MNC v0.1 P1 100-Case Qualification

This repository contains the first executable qualification pass for the **Multimodal Nutrition Corpus (MNC) v0.1**.

## Current batch

- Source cases: dish IDs `10000–10099`
- Batch size: 100 contiguous records
- Purpose: schema qualification, source/API semantic audit, recipe–nutrition reconciliation screening, QC fixture estimation, and task-specific eligibility
- Important: this is **not** a representative stratified sample of the full corpus.

## Core scientific rules

1. `Raw != Normalized`
2. `Missing != Zero`
3. `Source population tag != evidence-based applicability`
4. `Recipe truth != visually observable truth`
5. `Dish-level quality != task-specific eligibility`
6. Automated reconciliation is screening, not expert adjudication

## Reproduce

```bash
python scripts/process_p1_100_cases.py   data/raw/dish_samples_100_snapshot.csv   data/processed
```

The raw snapshot is versioned separately from generated outputs. Place the original 10-column headerless CSV at `data/raw/dish_samples_100_snapshot.csv` and rerun the processor.

## Main outputs

- `reports/P1_100_case_qualification_report.md`
- `reports/p1_summary.json`
- `data/processed/p1_case_registry.csv`
- `scripts/process_p1_100_cases.py`
- `docs/MNC_v0.1_P1_processing_contract.md`

Large normalized tables are generated deterministically by the processor and should not be hand-edited.

## Current decision

**CONDITIONAL PASS for scale engineering.** Do not extrapolate the observed qualification rates to the full API corpus until a genuinely stratified P1-B batch and a human-reviewed reconciliation subset are completed.
