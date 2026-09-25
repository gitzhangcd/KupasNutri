# MNC v0.1 P1-H3 Contract

## Scientific invariants

1. Evidence availability does not imply applicability.
2. Population evidence does not imply personalized recommendation.
3. Interaction evidence must preserve measurement level.
4. A dish composition ratio is not a daily-intake or biomarker ratio unless explicitly validated.
5. Nutrient adequacy and intervention efficacy are different claim classes.
6. Missing context causes downgrade or HOLD; it is never silently imputed.
7. Semantic ambiguity can trigger BLOCK even when a numeric value is present.
8. No claim may be stronger than its EvidenceBundle.

## Health QA Gold object

```yaml
HealthQAGold:
  qa_id:
  dish_id:
  qa_family:
  population_fixture_ref:
  question:
  gold_answer:
  required_claim_refs: []
  required_evidence_refs: []
  scoring_components: []
  prohibited_overclaims: []
  measurement_basis_status:
  personalized_recommendation_allowed: false
  gold_status:
  review_status:
  version:
```

## Gold statuses

- `evidence_locked_gold_candidate`
- `human_reviewed_gold`
- `adjudicated_gold`
- `rejected`

P1-H3 v0.1 produces the first state. P1-H3A is required to freeze the third state.
