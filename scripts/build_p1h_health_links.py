#!/usr/bin/env python3
"""Build MNC v0.1 P1-H health-evidence links from P1 nutrient observations.

Scientific invariants:
  * Dish -> Exposure -> Claim -> Evidence, never Dish -> Disease directly.
  * Missing != Zero.
  * Batch percentile != clinical threshold.
  * Population evidence != personalized recommendation.
  * Daily guideline targets are not applied until serving/nutrition basis is resolved.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

EXPOSURES = [
    dict(exposure_id="EXP-SODIUM", canonical_name="Dietary sodium",
         nutrient_name="Na", canonical_unit="mg",
         claim_refs="CLM-SOD-BP-001;CLM-SOD-REC-002",
         evidence_bundle_ref="EB-SODIUM-001"),
    dict(exposure_id="EXP-POTASSIUM", canonical_name="Dietary potassium",
         nutrient_name="Kalium", canonical_unit="mg",
         claim_refs="CLM-POT-BP-001",
         evidence_bundle_ref="EB-POTASSIUM-001"),
    dict(exposure_id="EXP-FIBER", canonical_name="Dietary fibre",
         nutrient_name="DietaryFiber", canonical_unit="g",
         claim_refs="CLM-FIBER-NCD-001;CLM-FIBER-REC-002",
         evidence_bundle_ref="EB-FIBER-001"),
    dict(exposure_id="EXP-SFA", canonical_name="Saturated fatty acids",
         nutrient_name="Sfa", canonical_unit="g",
         claim_refs="CLM-SFA-CVD-001;CLM-SFA-REC-002",
         evidence_bundle_ref="EB-SFA-001"),
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--nutrients", required=True, type=Path)
    p.add_argument("--anchors", required=True, type=Path)
    p.add_argument("--task-eligibility", type=Path)
    p.add_argument("--out", required=True, type=Path)
    args=p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    nut=pd.read_csv(args.nutrients)
    anchors=pd.read_csv(args.anchors)

    links=[]
    for e in EXPOSURES:
        sub=nut[nut["nutrient_name"]==e["nutrient_name"]].copy()
        frame=anchors[
            ["dish_id","source_dish_id","canonical_name",
             "source_population_tags","global_qc_status"]
        ].merge(
            sub[["dish_id","value","unit","observation_status",
                 "measurement_basis","derivation_status"]],
            on="dish_id",how="left"
        )
        vals=pd.to_numeric(frame["value"], errors="coerce")
        pct=vals.rank(pct=True, method="average")

        for i,row in frame.iterrows():
            reported=pd.notna(row["value"])
            q=float(pct.loc[i]) if reported and pd.notna(pct.loc[i]) else None
            links.append({
                "dish_id":row["dish_id"],
                "source_dish_id":row["source_dish_id"],
                "dish_name":row["canonical_name"],
                "exposure_id":e["exposure_id"],
                "nutrient_name":e["nutrient_name"],
                "observed_value":row["value"] if reported else "",
                "unit":row["unit"] if reported else e["canonical_unit"],
                "observation_status":row["observation_status"] if reported else "not_reported",
                "measurement_basis":row["measurement_basis"] if reported else "not_reported",
                "batch_percentile":round(q,4) if q is not None else "",
                "batch_relative_level":(
                    "upper_quartile" if q is not None and q>=.75 else
                    "lower_quartile" if q is not None and q<=.25 else
                    "middle_half" if q is not None else "not_reported"),
                "claim_refs":e["claim_refs"] if reported else "",
                "evidence_bundle_ref":e["evidence_bundle_ref"] if reported else "",
                "health_linkage_status":"evidence_linked_composition_only"
                    if reported else "blocked_missing_observation",
                "threshold_interpretation_status":"BLOCKED_UNRESOLVED_NUTRITION_BASIS",
                "personalized_recommendation_status":"NOT_ALLOWED_P1H",
                "source_population_tags":row["source_population_tags"],
                "dish_global_qc_status":row["global_qc_status"],
                "linkage_version":"P1-H-v0.1"
            })

    links=pd.DataFrame(links)
    links.to_csv(args.out/"dish_exposure_links.csv", index=False, encoding="utf-8-sig")

    per_dish=(links.groupby(["dish_id","source_dish_id","dish_name"])
        .agg(
            exposure_slots=("exposure_id","count"),
            linked_exposures=("health_linkage_status",
                lambda s:(s=="evidence_linked_composition_only").sum()),
            blocked_missing_exposures=("health_linkage_status",
                lambda s:(s!="evidence_linked_composition_only").sum()),
            claim_refs=("claim_refs",
                lambda s:";".join(sorted(set(
                    x for v in s for x in str(v).split(";")
                    if x and x!="nan")))),
            evidence_bundles=("evidence_bundle_ref",
                lambda s:";".join(sorted(set(
                    x for x in s if pd.notna(x) and x))))
        ).reset_index())
    per_dish["health_linkage_level"]="H1_population_evidence_linked"
    per_dish["personalization_status"]="not_allowed"
    per_dish.to_csv(args.out/"dish_health_summary.csv",index=False,encoding="utf-8-sig")

    seeds=[]
    names={e["exposure_id"]:e["canonical_name"] for e in EXPOSURES}
    admitted=links[links.health_linkage_status=="evidence_linked_composition_only"]
    for _,link in admitted.iterrows():
        base=dict(
            dish_id=link.dish_id,
            source_dish_id=link.source_dish_id,
            dish_name=link.dish_name,
            exposure_id=link.exposure_id,
            target_claim_refs=link.claim_refs,
            target_evidence_bundle_ref=link.evidence_bundle_ref,
            gold_status="provisional_gold_v0.1")
        seeds.append({
            **base,
            "task_seed_id":f"T6-{link.source_dish_id}-{link.exposure_id.replace('EXP-','')}",
            "task_family":"T6_evidence_retrieval",
            "input_intent":f"Retrieve evidence relevant to {names[link.exposure_id]} observed in this dish.",
            "allowed_output_scope":"population-level evidence; uncertainty/applicability; no individualized recommendation"})
        seeds.append({
            **base,
            "task_seed_id":f"T7-{link.source_dish_id}-{link.exposure_id.replace('EXP-','')}",
            "task_family":"T7_health_QA",
            "input_intent":f"Explain population-level evidence relevant to {names[link.exposure_id]} in this dish without a dish-level disease or personalized recommendation.",
            "allowed_output_scope":"claim-bounded explanation; no dose threshold while nutrition basis unresolved"})
    pd.DataFrame(seeds).to_csv(
        args.out/"health_task_seed_instances.csv",index=False,encoding="utf-8-sig")

    if args.task_eligibility:
        te=pd.read_csv(args.task_eligibility)
        te["T6_evidence_retrieval"]="Q*"
        te["T7_health_QA"]="Q*"
        te["T6_T7_scope"]="population_evidence_only;no_personalized_recommendation;no_dose_thresholding_until_basis_resolved"
        te.to_csv(args.out/"task_eligibility_p1h.csv",index=False,encoding="utf-8-sig")

if __name__=="__main__":
    main()
