# MNC v0.1 P1 Processing Contract

## Scope

P1 converts each source dish into a traceable `DishScientificObject` and assigns task-specific eligibility. It does not convert source audience tags into medical recommendations and does not assume the nutrition denominator is known when the API does not explicitly define it.

## Status vocabulary

### Recipe reconciliation
- `PASS`: no detected mismatch requiring normalization.
- `PASS_WARN`: aliases, water/process media, or other non-fatal ambiguity detected.
- `HOLD`: a likely consumed ingredient appears in cooking steps but is absent from the structured `major` list.
- `MAJOR_CONFLICT`: a candidate specific ingredient identity substitution is detected.

### Task eligibility
- `Q`: qualified.
- `Q*`: provisional / qualified with caveat.
- `H`: hold pending semantic or human review.
- `NA`: required layer not yet instantiated.

## Frozen QC fixtures

- source/list/detail consistency
- source record version drift
- missing-vs-zero preservation
- ingredient alias normalization
- step-only consumed ingredient
- processing auxiliary
- ingredient identity conflict
- portion semantic ambiguity
- visual observability mismatch
- source health-tag overreach

## Known unresolved semantics

1. Snapshot `unit + value` semantics are not yet source-confirmed.
2. Live API may return a different portion representation (`weight + calorie`).
3. Dish-level nutrition values are stored as `unresolved_api_base_profile` until denominator semantics are confirmed.
4. In this batch, `major` behaves like a major-ingredient list in many records and should not be treated as a complete recipe without reconciliation.
5. Source population tags (pregnancy, lactation, older adult, etc.) are retained only as source annotations.
6. Recipe-grounded quantitative tasks remain provisional until the API nutrient denominator is confirmed.

## Human-review boundary

Automated lexical reconciliation creates candidate flags. It cannot decide final scientific identity or consumption amount when source text is ambiguous. High-priority cases must be adjudicated before entering strict Recipe→Nutrient Gold or counterfactual Gold datasets.
