# MNC v0.1 P1-H Health-Linkage Contract

## Core linkage

`Dish -> NutrientObservation -> ExposureEntity -> ScientificClaim -> EvidenceBundle -> EvidenceUnit -> Source`

Direct `Dish -> Disease` edges are prohibited in P1-H.

## Linkage levels

- H0: composition only.
- H1: composition + population-level evidence linkage. **P1-H v0.1 target.**
- H2: dose-aware dish interpretation. HOLD until nutrition denominator + serving semantics are confirmed.
- H3: personalized recommendation. Out of scope.

## Exposure admission rule

An exposure family can enter P1-H Gold only if all are satisfied:

1. source coverage is sufficient for the pilot;
2. source nutrient identity and unit are explicit;
3. a defensible population-level scientific claim can be frozen;
4. at least one high-authority guideline or equivalent synthesis exists;
5. evidence uncertainty/applicability can be represented;
6. the exposure can be linked without turning a single dish into a disease label.

## First-wave Gold-4

- EXP-SODIUM
- EXP-POTASSIUM
- EXP-FIBER
- EXP-SFA

## Hard semantic constraints

- Missing != Zero.
- Batch percentile != clinical threshold.
- Higher/lower within the batch != healthy/unhealthy.
- Population evidence != individualized advice.
- Source audience tags != evidence-based applicability.
- Guideline daily target != dish-level compliance until denominator/serving is confirmed.
- Recipe ingredient != causal source of a dish nutrient unless contribution is separately modeled.
- Claim wording may not be strengthened beyond its EvidenceBundle.

## Evidence lineage

Every linked edge must resolve:

`DishExposureLink -> ScientificClaim -> EvidenceBundle -> EvidenceUnit -> Source`

P1-H v0.1 requires lineage completeness = 1.0 for admitted links.

## Task qualification

P1-H activates provisional:

- T6 evidence-aware retrieval
- T7 nutrition–health QA

Both are restricted to population-level, claim-bounded explanations with explicit uncertainty/applicability.

Personalized intake targets, treatment recommendations, contraindication decisions, and clinical thresholding are not part of P1-H.
