#!/usr/bin/env python3
"""MNC v0.1 P1-H2 builder.

Builds applicability-constrained health links for:
Protein, Calcium, Iron, Folate/FolicAcid, Dietary Cholesterol, Purine.

Key invariant: a link may be BLOCKED because scientific semantics are insufficient.
"""
from __future__ import annotations
import argparse,csv
from pathlib import Path

EXPOSURES = [
    ("EXP-PROTEIN","Protein","EB-PROTEIN-001","CLM-PROT-RDA-001;CLM-PROT-RE-002","context"),
    ("EXP-CALCIUM","Ca","EB-CALCIUM-001","CLM-CA-BONE-001;CLM-CA-SUPP-002","context"),
    ("EXP-IRON","Fe","EB-IRON-001","CLM-FE-REQ-001;CLM-FE-PREG-002","context"),
    ("EXP-FOLATE","FolicAcid","EB-FOLATE-001","CLM-FOL-FORM-001;CLM-FOL-NTD-002","semantic_hold"),
    ("EXP-CHOLESTEROL","Cholesterol","EB-CHOLESTEROL-001","CLM-CHOL-CVD-001","uncertainty"),
    ("EXP-PURINE","Purine","EB-PURINE-001","CLM-PUR-GOUT-001;CLM-PUR-FLARE-002","gout_only"),
]

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def write_csv(p,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not rows:return
    with open(p,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nutrients",type=Path,required=True)
    ap.add_argument("--anchors",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()

    nutrients=read_csv(a.nutrients)
    anchors=read_csv(a.anchors)
    by={(r["dish_id"],r["nutrient_name"]):r for r in nutrients}
    links=[]

    for anchor in anchors:
        for exposure_id,nutrient,bundle,claims,mode in EXPOSURES:
            n=by.get((anchor["dish_id"],nutrient))
            if not n or n.get("value","")=="":
                status="blocked_missing_observation"
                out_bundle=out_claims=""
            elif mode=="semantic_hold":
                status="blocked_semantic_ambiguity"
                out_bundle=out_claims=""
            elif mode=="gout_only":
                status="evidence_linked_population_restricted"
                out_bundle,out_claims=bundle,claims
            else:
                status="evidence_linked_applicability_constrained"
                out_bundle,out_claims=bundle,claims
            links.append({
                "dish_id":anchor["dish_id"],
                "source_dish_id":anchor["source_dish_id"],
                "dish_name":anchor["canonical_name"],
                "exposure_id":exposure_id,
                "nutrient_name":nutrient,
                "observed_value":n.get("value","") if n else "",
                "unit":n.get("unit","") if n else "",
                "observation_status":n.get("observation_status","not_reported") if n else "not_reported",
                "claim_refs":out_claims,
                "evidence_bundle_ref":out_bundle,
                "health_linkage_status":status,
                "threshold_interpretation_status":"BLOCKED_UNRESOLVED_NUTRITION_BASIS",
                "personalized_recommendation_status":"NOT_ALLOWED_P1H2",
                "linkage_version":"P1-H2-v0.1",
            })
    write_csv(a.out/"dish_exposure_links_h2.csv",links)

if __name__=="__main__":
    main()
