# MNC v0.1 P1-H｜100-Case Nutrition–Health Evidence Linkage Report

## Freeze decision

**P1-H v0.1 = PASS for H1 population-level evidence linkage.**

This does not authorize dish-level disease labels, clinical recommendations, or serving-based threshold judgments.

Frozen lineage:

`Dish -> NutrientObservation -> ExposureEntity -> ScientificClaim -> EvidenceBundle -> EvidenceUnit -> Source`

and explicitly not:

`Dish -> Disease`.

## Executed scope

- Dishes: **100**
- Gold exposure families: **4**
- Scientific claims: **7**
- Evidence bundles: **4**
- Evidence units: **8**
- Dish–Exposure slots: **400**
- Evidence-linked edges: **394**
- Missing-observation edges: **6**
- Provisional T6/T7 task seeds: **788**
- Evidence-lineage validation errors: **0**

First-wave exposures:

- Dietary sodium (`Na`): 100/100
- Dietary potassium (`Kalium`): 100/100
- Dietary fibre (`DietaryFiber`): 100/100
- Saturated fatty acids (`Sfa`): 94/100

Six dishes have SFA as `not_reported`, not zero:
10050 盐菜蒸腊肉; 10055 腌嫩姜; 10070 鸭肉炒茭白; 10083 雪梨黄瓜汁; 10084 雪梨百合粥; 10086 雪湖玉藕.

## Why health linkage can run before recipe Gold

P1-H v0.1 is anchored to source-reported dish nutrient observations, not reconstructed complete recipes.

A case HOLD for `Recipe -> Nutrient` can therefore still enter:

`Dish -> reported nutrient observation -> population-level evidence`

when the nutrient is present and provenance is retained.

Recipe incompleteness still blocks ingredient-attribution statements such as "ingredient X caused this dish sodium value".

## Evidence freeze

### Sodium

`CLM-SOD-BP-001`: reducing dietary sodium lowers blood pressure in adults with dose-response evidence.

Sources:
- WHO sodium guideline: https://www.who.int/publications/i/item/9789241504836
- BMJ 2020, PMID 32094151: https://pubmed.ncbi.nlm.nih.gov/32094151/

`CLM-SOD-REC-002`: WHO recommends reducing sodium intake and <2 g/day sodium in adults as a population-level target.

**Restriction:** current dish values are not compared with the 2 g/day threshold while API nutrient basis/serving semantics remain unresolved.

### Potassium

`CLM-POT-BP-001`: potassium is blood-pressure relevant, but the relationship is conditional/nonlinear; higher is not automatically better.

Sources:
- WHO potassium guideline: https://www.who.int/publications/i/item/9789241504829
- JAHA 2020, PMID 32500831: https://pubmed.ncbi.nlm.nih.gov/32500831/

**Restriction:** a higher dish potassium value is not converted into an unrestricted supplementation or clinical recommendation.

### Dietary fibre

`CLM-FIBER-NCD-001`: higher fibre intake is associated with lower risks of several NCD outcomes, with complementary randomized evidence for selected risk factors.

`CLM-FIBER-REC-002`: WHO recommends at least 25 g/day naturally occurring dietary fibre for adults.

Sources:
- WHO carbohydrate guideline: https://www.who.int/publications/i/item/9789240073593
- Lancet 2019, PMID 30638909: https://pubmed.ncbi.nlm.nih.gov/30638909/

**Restriction:** no "% of daily target supplied by this dish" is calculated until denominator/serving semantics are confirmed.

### Saturated fatty acids

`CLM-SFA-CVD-001`: sustained saturated-fat reduction can reduce combined cardiovascular events; all-cause/CVD mortality effects are less clear.

`CLM-SFA-REC-002`: WHO recommends no more than 10% of total energy from SFA and emphasizes appropriate replacement nutrients.

Sources:
- WHO SFA/TFA guideline: https://www.who.int/publications/i/item/9789240073630
- Cochrane 2020, PMID 32827219: https://pubmed.ncbi.nlm.nih.gov/32827219/

**Restriction:** SFA grams are not converted into % energy while nutrition basis is unresolved.

## Hard semantic rules

- Evidence link != recommendation.
- Population evidence != patient-specific advice.
- Batch percentile != clinical threshold.
- High/low within this batch != healthy/unhealthy.
- Source population tag != evidence-based applicability.
- Nutrient observation != nutrient contribution by a specific ingredient.
- Missing != zero.
- Guideline daily target != dish-level compliance while serving/basis is unresolved.

## T6/T7 activation

After P1-H:

- T6 Evidence-aware retrieval: **100/100 Q***
- T7 Nutrition–Health QA: **100/100 Q***

Scope is limited to population-level evidence + uncertainty + applicability.

A total of **788 structured task seeds** were generated: one T6 and one T7 seed per evidence-linked Dish–Exposure edge.

## Evidence-lineage QC

All 7 ScientificClaims resolve to a valid EvidenceBundle.
All 4 EvidenceBundles resolve to valid EvidenceUnits.
All 394 admitted edges resolve to valid claim/bundle lineage.

`LineageCompleteness = 1.0`.

## Still blocked

### H2 dose-aware dish interpretation

Requires confirmed nutrition denominator, stable serving semantics and daily-intake comparison rules.

### H3 personalized nutrition / medical recommendation

Out of scope for P1-H.

### Ingredient-specific health attribution

Requires complete recipes and/or ingredient-level nutrient contribution models.

## Decision

**PASS_FOR_H1_POPULATION_EVIDENCE_LINKAGE**

**HOLD_FOR_DOSE_THRESHOLDING_AND_PERSONALIZED_RECOMMENDATION**

The first operational graph is:

`100 Dishes -> 394 exposure edges -> 4 ExposureEntities -> 7 ScientificClaims -> 4 EvidenceBundles -> 8 EvidenceUnits`.
