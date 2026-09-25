# MNC v0.1 P1-H2 Applicability Contract

## Allowed linkage states

- `evidence_linked_applicability_constrained`
- `evidence_linked_population_restricted`
- `blocked_missing_observation`
- `blocked_semantic_ambiguity`

A missing or ambiguous source value must never be converted into a negative health assertion.

## Applicability object

```yaml
ApplicabilityConstraint:
  population:
  physiological_state:
  disease_state:
  activity_context:
  nutrient_form:
  source_form:
  denominator_required:
  interacting_exposures:
  contraindication_context:
  evidence_certainty:
  residual_uncertainty:
```

## Stress-test rule

An exposure passes P1-H2 only if the system can preserve the factors needed to stop a true population-level evidence statement from becoming an invalid dish-level or patient-level claim.

## Exposure-specific invariants

### Protein
Requires body-weight / whole-day intake context for adequacy. Exercise context is constitutive for muscle-effect claims.

### Calcium
Food adequacy and supplement intervention claims are different evidence objects.

### Iron
Requirements vary by sex/pregnancy; total iron and absorbed iron are different objects.

### Folate
Food folate, folic acid and DFE are different measurement objects. The current `FolicAcid` source field is unresolved.

### Cholesterol
No stand-alone disease threshold is created. Dietary pattern and SFA context are mandatory.

### Purine
Health linkage is restricted to gout. Total purine does not erase source-type heterogeneity or treatment context.
