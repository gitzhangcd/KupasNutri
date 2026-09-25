# MNC v0.1 P1-H2｜Exposure Expansion & Applicability Stress Test

## Freeze decision

**P1-H2 v0.1 = PASS with a deliberate semantic kill signal.**

The system admits context-qualified links for protein, calcium, iron, dietary cholesterol and purine, while correctly blocking folate/NTD linkage because the source nutrient field `FolicAcid` is not sufficiently specified to distinguish natural food folate, synthetic folic acid, or DFE.

## Scope and coverage

| Exposure | Field | Coverage | Gate |
|---|---|---:|---|
| Protein | Protein | 100/100 | PASS_WITH_CONTEXT |
| Calcium | Ca | 100/100 | PASS_WITH_CONTEXT |
| Iron | Fe | 100/100 | PASS_WITH_CONTEXT |
| Folate candidate | FolicAcid | 95/100 | HOLD_FOR_FORM_SEMANTICS |
| Dietary cholesterol | Cholesterol | 100/100 | PASS_WITH_UNCERTAINTY |
| Purine | Purine | 95/100 | PASS_GOUT_ONLY |

New candidate slots: **600**  
Observed nutrient edges: **590**  
Evidence-linked H2 edges: **495**  
Blocked for source missingness: **10**  
Blocked for semantic ambiguity: **95**

## Applicability stress results

### Protein
Protein adequacy requires body weight and whole-day intake. Muscle-effect claims additionally require exercise context. Dish protein grams are not converted into a universal adequacy label.

### Calcium
Calcium adequacy and calcium-supplement fracture efficacy are separate evidence objects. Food calcium cannot inherit the effect estimate of a supplement intervention.

### Iron
Total dish iron is not absorbed iron. Sex, pregnancy, baseline status, and heme/nonheme source materially affect applicability. Pregnancy supplementation evidence is kept population-specific.

### Folate — semantic kill signal
Natural food folate, synthetic folic acid, and DFE are distinct measurement objects. The source field `FolicAcid` lacks sufficient semantics. Therefore all 95 observed folate candidate edges are blocked from health claims until the source nutrient dictionary and conversion method are verified.

### Dietary cholesterol
No stand-alone cardiovascular threshold is created. The evidence object preserves uncertainty and requires saturated-fat, food-source, and overall dietary-pattern context.

### Purine
Purine links are admitted only for the gout population. The recommendation is conditional and low-certainty; source type matters and diet generally has modest serum-urate effects.

## Evidence objects added

- 6 ExposureEntities
- 11 ScientificClaims
- 6 EvidenceBundles
- 12 EvidenceUnits

Every admitted H2 edge resolves:

`Dish -> NutrientObservation -> ExposureEntity -> ScientificClaim -> EvidenceBundle -> EvidenceUnit -> Source`

## Task expansion

Each admitted edge generates one T6 and one T7 seed.

New H2 task seeds: **990**  
Cumulative P1-H + P1-H2 task seeds: **1,778**

## Cumulative health graph

After P1-H + P1-H2:

- 100 dishes
- 10 exposure families
- 1,000 candidate dish–exposure slots
- 889 evidence-linked edges
- 95 folate observations deliberately blocked by nutrient-form semantics
- 18 ScientificClaims total
- 10 EvidenceBundles total
- 20 EvidenceUnits total
- 1,778 T6/T7 task seeds

## Acceptance gates

- Protein context preserved: PASS
- Calcium food/supplement distinction preserved: PASS
- Iron population/bioavailability constraints preserved: PASS
- Folate ambiguity triggers a block: PASS
- Cholesterol uncertainty/pattern context preserved: PASS
- Purine restricted to gout: PASS
- Missing != zero: PASS
- No direct Dish -> Disease edge: PASS
- No individualized recommendation: PASS
- No daily-target compliance from unresolved serving/basis: PASS

## Decision

**PASS_APPLICABILITY_STRESS_TEST_WITH_FOLATE_SEMANTIC_KILL_SIGNAL**

Recommended next stage:

**MNC v0.1 P1-H3｜Applicability Object Formalization, Population × Evidence Fixtures, Cross-Exposure Interaction & Health QA Gold-100**
