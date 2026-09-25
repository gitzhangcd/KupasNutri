# MNC v0.1 P1｜100-Case Qualification Report

## 1. Batch identity

- Records: **100**
- Source IDs: **10000–10099**
- Contiguous ID slice: **yes**
- Unique structured ingredients: **156**
- Ingredient lines: **643**
- Images present: **100/100**
- Ingredient source-code coverage: **100%**
- Ingredient `ingrId` coverage: **100%**

> This batch is a qualification batch, not a population-representative stratified sample. The rates below are batch rates and must not yet be generalized to the full API corpus.

## 2. Sampling composition

Food-category tags:

- 畜肉类: 47
- 禽肉类: 25
- 蛋奶豆类: 18
- 水产品类: 16
- 汤羹类: 8
- 主食类: 8
- 素菜类: 6

Source population tags:

- 孕妇: 99
- 乳母: 97
- 学生餐: 94
- 老年餐: 67
- 宝宝辅食: 3

Dish names containing “羊”: **29/100**.

This contiguous slice is strongly enriched for meat/lamb dishes. It is suitable for pipeline qualification, but not for estimating corpus-wide prevalence.

## 3. Source/API semantic audit

- Internal top/list/detail consistency: **99/100 PASS**
- One internal inconsistency: **10086 雪湖玉藕** has a list/detail image mismatch.
- Unique portion/unit patterns: **17**
- Snapshot portion records use `unit + value`.
- P0 showed the live endpoint may instead expose `weight + calorie`.
- Therefore portion semantics remain **HOLD** until endpoint/version semantics are frozen.
- Nutrient measurement basis remains **UNRESOLVED_API_BASE_PROFILE**.

## 4. Nutrient audit

- Nutrient union: **47**
- Nutrient intersection: **19**
- Nutrient fields per dish: **22–47**, median **43**
- `missing != zero` is explicitly preserved.
- Macro-energy sanity check uses `4P + 9F + 4C` only as a QC heuristic, not as the source of truth.
- Median relative difference: **1.91%**
- Maximum relative difference: **10.60%** in **10055 腌嫩姜**.

## 5. Recipe–nutrition reconciliation

Automated screening:

- `PASS`: **2**
- `PASS_WARN`: **21**
- `HOLD`: **76**
- `MAJOR_CONFLICT`: **1**

The single specific identity-conflict fixture is **10004 阳春面**:

- structured ingredient: **草菇**
- cooking text: **滑子菇**
- cooking text additionally mentions **绿萝卜**, absent from the structured major list.

The dominant failure mode is not parser failure. It is **recipe incompleteness relative to cooking text**: 77 records contain a likely consumed ingredient/seasoning in the steps that is absent from the structured `major` list.

Common examples include 姜、葱、料酒、蒜、花椒 and other seasonings/aromatics. This strongly suggests that `major` should be treated as a **major-ingredient list**, not automatically as a complete recipe.

All reconciliation results are **automated screening**, not expert adjudication.

## 6. Global QC

- `PASS_WARN`: **23**
- `HOLD`: **77**

Review priority:

- HIGH: **78**
- MEDIUM: **20**
- LOW: **2**

High-priority reasons:

- step-only consumed ingredient: **77**
- ingredient identity conflict: **1**
- macro-energy sanity >10%: **1**
- internal payload inconsistency: **1**

The counts overlap because a case can trigger more than one reason.

## 7. Task eligibility

`Q` = qualified; `Q*` = provisional; `H` = hold; `NA` = layer not yet instantiated.

| Task | Q | Q* | H | NA |
|---|---:|---:|---:|---:|
| T1 Image → Dish | 100 | 0 | 0 | 0 |
| T2 Image → Ingredient | 0 | 99 | 1 | 0 |
| T3a Image + Dish name → Nutrient | 0 | 100 | 0 | 0 |
| T3b Image + Recipe → Nutrient | 0 | 23 | 77 | 0 |
| T4 Recipe → Nutrient | 0 | 23 | 77 | 0 |
| T5 Portion reasoning | 0 | 0 | 100 | 0 |
| T6 Evidence-aware retrieval | 0 | 0 | 0 | 100 |
| T7 Nutrition–Health QA | 0 | 0 | 0 | 100 |
| T8 Counterfactual recipe reasoning | 0 | 23 | 77 | 0 |

### Interpretation

The dataset is already strong for **dish-level multimodal anchoring** and provisional **image/name → nutrient** experiments.

It is not yet ready to treat every row as complete Recipe→Nutrient Gold because the structured `major` field is incomplete relative to cooking text in most records.

T5 remains blocked because portion semantics are unresolved.

T6/T7 are not failures; the Health Evidence Layer has simply not yet been instantiated.

## 8. Population-tag warning

The source labels nearly every case as suitable for pregnancy/lactation/student meals. These labels therefore have weak discriminatory value and must remain:

`source_population_tag`

rather than:

`evidence_based_applicability`.

No medical recommendation label is generated from them.

## 9. 100K feasibility decision

**CONDITIONAL PASS for scale engineering.**

Why it passes:

1. 100/100 records are structurally parseable.
2. Source-coded ingredient identity is complete in this batch.
3. Dish images and nutrient vectors are broadly available.
4. Recipe disagreements can be made explicit rather than silently ignored.
5. Task-specific eligibility prevents a weak recipe record from contaminating tasks for which it is not valid.

Why it remains conditional:

1. Portion semantics are not frozen.
2. Nutrient denominator/API-base semantics are not source-confirmed.
3. This 100-case batch is not stratified.
4. Image-level ingredient observability has not been annotated.
5. Recipe reconciliation is automated screening and requires a human calibration subset.
6. Health-evidence linkage is not yet instantiated.

## 10. Next gate

Proceed to:

**MNC v0.1 P1-B｜Stratified Expansion, Human Review Calibration & Gold-50 Reconciliation**

Recommended next unit:

- 200–500 deliberately stratified dishes;
- balance food categories and recipe complexity;
- include multiple portion-system strata;
- include low/high nutrient-completeness strata;
- construct a **Gold-50** human-reviewed recipe reconciliation subset;
- use Gold-50 to estimate precision/recall of the automated QC rules before applying them to 100K.

The key question for P1-B is no longer “can we download 100K?”, but:

> **what proportion of the source corpus can be safely admitted to each downstream multimodal nutrition task, under explicit scientific and semantic constraints?**
