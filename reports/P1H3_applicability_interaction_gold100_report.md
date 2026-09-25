# MNC v0.1 P1-H3｜Applicability Object Formalization, Population × Evidence Fixtures, Cross-Exposure Interaction & Health QA Gold-100

## Freeze decision

**P1-H3 v0.1 = PASS for executable applicability formalization and evidence-locked Gold-100 construction.**

**Human Gold Freeze = HOLD pending independent human adjudication.**

The project now moves from free-text applicability notes to executable objects:

`DishObservation -> Exposure -> Interaction/Claim -> ApplicabilityObject -> PopulationEvidenceFixture -> Gold QA`

## 1. ApplicabilityObject formalization

A JSON Schema is frozen and **23/23** instantiated ApplicabilityObjects validate against it.

Each object separates:

- population;
- disease/physiological/activity context;
- nutrient form / denominator / interacting-exposure requirements;
- allowed inference level;
- evidence strength;
- uncertainty;
- context-missing behavior;
- semantic-block behavior;
- prohibited inferences.

The central rule is:

`EvidenceAvailable != EvidenceApplicable`

and:

`PopulationEvidence != IndividualRecommendation`.

## 2. Population × Evidence fixtures

Frozen fixtures: **8**

1. Adult blood-pressure context
2. Adult cardiovascular-prevention context
3. General iron-bioavailability context
4. Pregnancy iron context
5. Periconceptional folic-acid context
6. Community-dwelling older-adult calcium/vitamin-D context
7. Healthy adult resistance-exercise protein context
8. Gout-specific purine context

Each fixture defines allowed claims and explicit blocked inferences.

## 3. Cross-exposure interactions

Frozen interaction objects: **5**

### INT-NAK-BP-001
Sodium × potassium / blood pressure.

Population evidence supports joint sodium-potassium interpretation, including lower 24-h urinary Na:K being associated with lower BP. A dish composition ratio is **not** a 24-h urinary ratio or daily-intake ratio.

### INT-SFA-CHOL-001
Saturated fat × dietary cholesterol / cardiovascular interpretation.

Dietary cholesterol cannot be interpreted as a stand-alone cardiovascular threshold; SFA and the overall dietary pattern are constitutive context.

### INT-FE-VC-001
Iron × vitamin C / nonheme iron absorption.

Vitamin C can enhance nonheme iron absorption, but total dish iron does not reveal heme/nonheme fractions, inhibitors or individual iron status.

### INT-FOL-B12-001
Folate × vitamin B12 / semantic-safety stress.

High folate can correct megaloblastic anemia associated with B12 deficiency without correcting neurologic damage. The current dish `FolicAcid` field remains semantically unresolved and therefore cannot be promoted into supplement/DFE claims.

### INT-CA-VD-001
Calcium × vitamin D / fracture intervention context.

Nutrient presence in food is separated from the effectiveness of calcium/vitamin-D supplementation for fracture prevention in a specific older population.

## 4. Health QA Gold-100

Exactly **100 unique dishes** are represented once each.

| QA family | n |
|---|---:|
| Sodium × Potassium | 20 |
| SFA × Cholesterol | 15 |
| Iron × Vitamin C | 15 |
| Folate × B12 semantic block | 10 |
| Calcium × Vitamin D conflict | 10 |
| Protein × resistance exercise | 10 |
| Purine × gout | 10 |
| Iron × pregnancy | 10 |
| **Total** | **100** |

Each item contains:

- dish identity;
- actual source nutrient values;
- population fixture;
- question;
- evidence-locked gold answer;
- required claim refs;
- required evidence refs;
- scoring components;
- prohibited overclaims;
- measurement-basis status;
- personalized-recommendation prohibition.

## 5. Gold scoring

Each item is scored on five 0/1 components:

1. composition fidelity;
2. evidence fidelity;
3. applicability;
4. measurement boundary;
5. overclaim rejection.

Maximum score:

`5 / item`.

A superficially fluent answer that violates a hard scientific constraint cannot receive full credit.

## 6. Automated conformance results

- 100 QA items
- 100 unique dishes
- 8 QA families
- 23/23 ApplicabilityObjects schema-valid
- missing claim refs: 0
- missing evidence refs: 0
- personalized recommendation allowed: 0
- all items retain unresolved source nutrition-basis flag

## 7. Scientific kill fixtures now present

P1-H3 deliberately contains cases where a model must refuse an apparently attractive inference:

- dish Na/K -> not daily/urinary Na:K;
- cholesterol number -> not heart-health label;
- Fe + vitamin C -> not guaranteed absorption/treatment;
- `FolicAcid` -> not automatically folic-acid supplementation / DFE;
- Ca + vitamin D -> not fracture-prevention efficacy;
- protein grams -> not muscle-building without activity context;
- purine -> not universally unhealthy;
- dish iron -> not pregnancy treatment.

This is a core feature, not missing functionality.

## 8. Gold status

The current 100 items are:

`evidence_locked_gold_candidate`

because the answer keys are deterministically restricted by frozen claims and applicability objects.

They are **not yet dual-human-adjudicated**.

Therefore:

- Dataset construction gate: PASS
- Scientific lineage gate: PASS
- Schema gate: PASS
- No-added-claim gate: PASS
- Human adjudication gate: HOLD

## 9. Next execution stage

Recommended:

**MNC v0.1 P1-H3A｜Gold-100 Independent Human Adjudication, Inter-Rater Reliability, Error Taxonomy & Final Gold Freeze**

in parallel with:

**P1-B｜Recipe Gold-50 Human Calibration**

After those two human calibration gates, the corpus can safely scale health QA generation beyond the current 100 dishes.
