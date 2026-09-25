#!/usr/bin/env python3
"""MNC v0.1 P1 — reproducible 100-case qualification screen.

The source CSV is headerless with 10 columns:
serial,item_id,name,calorie,category,major_names,list_json,detail_json,created_at,updated_at

This script intentionally treats recipe reconciliation as automated screening rather
than expert adjudication. It preserves four invariants:
  Raw != Normalized
  Missing != Zero
  Source population tag != scientific applicability
  Dish quality != task-specific eligibility
"""
from __future__ import annotations
import argparse,csv,json,re,statistics
from collections import Counter
from pathlib import Path

COLS=["serial","item_id","name","calorie","category","major_names","list_json","detail_json","created_at","updated_at"]
CORE=["Calorie","Protein","Fat","Carbohydrate"]
OILS={"大豆油","色拉油","花生油","猪油","芝麻油","橄榄油","菜籽油","玉米油","葵花籽油","调和油","食用油"}
FIXED={"鸡胗":"鸡肫","牛奶":"牛乳","雪里红":"雪里蕻","花菜":"菜花","玉米粉":"玉米面"}
EXTRA={"料酒","黄酒","香醋","白醋","醋","蚝油","豆瓣酱","八角","花椒","孜然","大蒜","蒜","香菜","芝麻","葱","姜","盐","糖","油","淀粉","清水","饮用水","水","面条","鸡胗","牛奶","雪里红","花菜","玉米粉","青椒","彩椒","肉","肉末","肉丝","肉片","萝卜","蘑菇","滑子菇","绿萝卜","白糖","十三香","姜油"}
AUX_RE=re.compile(r"搓洗|冲洗|清洗|洗净|浸泡|去腥")
POP={"孕妇","乳母","学生餐","老年餐","宝宝辅食"}

def load(path):
    out=[]
    with path.open(encoding="utf-8-sig",newline="") as f:
        for i,r in enumerate(csv.reader(f),1):
            if len(r)!=10: raise ValueError(f"row {i}: expected 10 columns, got {len(r)}")
            x=dict(zip(COLS,r));x["list"]=json.loads(x["list_json"]);x["detail"]=json.loads(x["detail_json"]);out.append(x)
    return out

def nutrients(d):
    return {x["name"]:x for arr in (d.get("nutritionMap") or {}).values() for x in arr if x.get("name")}

def consistency(x):
    d,l=x["detail"],x["list"];flags=[]
    if str(x["item_id"])!=str(l.get("id")) or str(x["item_id"])!=str(d.get("id")):flags.append("id_mismatch")
    if x["name"]!=l.get("name") or x["name"]!=d.get("name"):flags.append("name_mismatch")
    if x["category"]!=l.get("category"):flags.append("category_mismatch")
    if l.get("image")!=d.get("image"):flags.append("image_mismatch")
    sn=[z.get("name") for z in d.get("major",[])]
    ln=[z.strip() for z in (l.get("major") or "").split(",") if z.strip()]
    tn=[z.strip() for z in x["major_names"].split(",") if z.strip()]
    if sn!=ln or sn!=tn:flags.append("major_mismatch")
    n=nutrients(d);dc=n.get("Calorie",{}).get("value")
    if str(x["calorie"])!=str(l.get("calorie")) or (dc is not None and str(x["calorie"])!=str(dc)):flags.append("calorie_mismatch")
    return (not flags),flags

def alias(term,structured):
    S=set(structured)
    if term in S:return term
    if term in FIXED and FIXED[term] in S:return FIXED[term]
    if term=="盐" and "精盐" in S:return "精盐"
    if term in {"葱","葱花","葱末"}:
        z=[s for s in structured if "葱" in s];return z[0] if len(z)==1 else None
    if term in {"姜","姜末","姜丝"}:
        z=[s for s in structured if "姜" in s];return z[0] if len(z)==1 else None
    if term in {"糖","白糖","砂糖"}:
        z=[s for s in structured if "糖" in s];return z[0] if len(z)==1 else None
    if term in {"油","食用油"}:
        z=[s for s in structured if s in OILS];return z[0] if len(z)==1 else None
    if term=="面条":
        z=[s for s in structured if "面" in s and s not in {"面粉","玉米面"}];return z[0] if len(z)==1 else None
    if term in {"肉","肉末","肉丝","肉片"}:
        z=[s for s in structured if "肉" in s]
        if len(z)==1:return z[0]
        marks=("鸡","鸭","鱼","虾","蟹","蛏","排骨","牛","羊","猪","肫","肝","腰","血","火腿","腊")
        z=[s for s in structured if any(m in s for m in marks)];return z[0] if len(z)==1 else None
    if term=="蘑菇":
        z=[s for s in structured if any(k in s for k in ("菇","蘑","菌"))];return z[0] if len(z)==1 else None
    if term=="萝卜":
        z=[s for s in structured if "萝卜" in s];return z[0] if len(z)==1 else None
    if term in {"青椒","彩椒"}:
        z=[s for s in structured if s in {"甜椒","彩椒","青椒","辣椒"}];return z[0] if len(z)==1 else None
    return None

def mentions(text,lexicon):
    cand=[]
    for term in lexicon:
        start=0
        while True:
            p=text.find(term,start)
            if p<0:break
            cand.append((p,p+len(term),term));start=p+1
    cand.sort(key=lambda z:(z[0],-(z[1]-z[0]),z[2]));used=[];out=[]
    for a,b,t in cand:
        if any(not(b<=x or a>=y) for x,y in used):continue
        used.append((a,b));out.append((t,text[max(0,a-18):min(len(text),b+18)]))
    return out

def reconcile(x,global_ing):
    d=x["detail"];structured=[z["name"] for z in d.get("major",[]) if z.get("name")]
    steps=d.get("dishCooksteps") or [];body=" ".join(z.get("content","") for z in (steps[1:] if len(steps)>1 else steps))
    lex=sorted(set(global_ing)|EXTRA|set(FIXED),key=lambda s:(-len(s),s))
    aliases=[];consumed=[];aux=[];water=[]
    for term,ctx in mentions(body,lex):
        if term in structured:continue
        a=alias(term,structured)
        if a:aliases.append((term,a));continue
        if term in {"水","清水","饮用水"}:water.append(term);continue
        if term in {"淀粉","盐","精盐","面粉"} and AUX_RE.search(ctx):aux.append(term);continue
        if term in {"鸡","鸭"}:continue
        consumed.append(term)
    aliases=list(dict.fromkeys(aliases));consumed=list(dict.fromkeys(consumed));aux=list(dict.fromkeys(aux));water=list(dict.fromkeys(water))
    conflicts=[]
    mush=[s for s in structured if any(k in s for k in ("菇","蘑","菌"))]
    specific=[t for t in consumed if any(k in t for k in ("菇","蘑","菌"))]
    for t in specific:
        if mush:conflicts.append(f"{','.join(mush)}↔{t}")
    consumed=[t for t in consumed if not any(c.endswith("↔"+t) for c in conflicts)]
    status="MAJOR_CONFLICT" if conflicts else ("HOLD" if consumed else ("PASS_WARN" if aliases or aux or water else "PASS"))
    return {"status":status,"aliases":aliases,"consumed":consumed,"aux":aux,"water":water,"conflicts":conflicts}

def sanity(d):
    n=nutrients(d);missing=[k for k in CORE if k not in n or n[k].get("value") in (None,"")]
    rel=None
    if not missing:
        E,P,F,C=[float(n[k]["value"]) for k in CORE];rel=abs((4*P+9*F+4*C)-E)/E if E else None
    return missing,rel

def write_csv(path,rows):
    if not rows:return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("input_csv",type=Path);ap.add_argument("output_dir",type=Path);a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
    rows=load(a.input_csv);global_ing=sorted({z["name"] for x in rows for z in x["detail"].get("major",[]) if z.get("name")})
    registry=[];qc=[];tasks=[];recons=[];all_n=set();common_n=None;unit_patterns=Counter();cats=Counter();pops=Counter();internal_pass=0;ing_lines=0;macro=[]
    for x in rows:
        sid=x["item_id"];d=x["detail"];ok,flags=consistency(x);internal_pass+=ok
        r=reconcile(x,global_ing);missing,rel=sanity(d);macro += [rel] if rel is not None else []
        ns=set(nutrients(d));all_n|=ns;common_n=ns if common_n is None else common_n&ns
        unit_patterns[tuple((u.get("unit"),u.get("value"),u.get("weight"),u.get("calorie")) for u in d.get("unit",[]))]+=1
        ing_lines+=len(d.get("major",[]))
        source=[z.strip() for z in x["category"].split(",") if z.strip()];food=[z for z in source if z not in POP];pop=[z for z in source if z in POP]
        for z in food:cats[z]+=1
        for z in pop:pops[z]+=1
        review=[]
        if r["conflicts"]:review.append("ingredient_identity_conflict")
        if r["consumed"]:review.append("step_only_consumed_ingredient")
        if missing:review.append("missing_core_nutrient")
        if rel is not None and rel>.10:review.append("macro_energy_sanity_gt_10pct")
        if not ok:review.append("internal_payload_inconsistency")
        priority="HIGH" if review else ("MEDIUM" if r["status"]=="PASS_WARN" else "LOW")
        fatal={"ingredient_identity_conflict","step_only_consumed_ingredient","missing_core_nutrient","internal_payload_inconsistency"}
        global_status="HOLD" if any(z in fatal for z in review) else "PASS_WARN"
        recipe_ok=r["status"] in {"PASS","PASS_WARN"};image=bool(d.get("image"));core_ok=not missing
        t={
          "T1_image_to_dish":"Q" if image else "H",
          "T2_image_to_ingredient":"Q*" if image and not r["conflicts"] else "H",
          "T3a_image_name_to_nutrient":"Q*" if image and core_ok else "H",
          "T3b_image_recipe_to_nutrient":"Q*" if image and core_ok and recipe_ok else "H",
          "T4_recipe_to_nutrient":"Q*" if core_ok and recipe_ok else "H",
          "T5_portion_reasoning":"H","T6_evidence_retrieval":"NA","T7_health_QA":"NA",
          "T8_counterfactual":"Q*" if core_ok and recipe_ok else "H"
        }
        rec={"source_dish_id":sid,"name":x["name"],"recipe_status":r["status"],"aliases_resolved":";".join(f"{u}→{v}" for u,v in r["aliases"]),"step_only_consumed_terms":";".join(r["consumed"]),"identity_conflict_terms":";".join(r["conflicts"])};recons.append(rec)
        q={"source_dish_id":sid,"name":x["name"],"internal_consistency":"PASS" if ok else "FAIL","internal_flags":";".join(flags),"macro_energy_relative_diff":"" if rel is None else round(rel,6),"recipe_status":r["status"],"global_status":global_status,"review_priority":priority,"review_reasons":";".join(review)};qc.append(q)
        tasks.append({"source_dish_id":sid,"name":x["name"],**t})
        registry.append({"source_dish_id":sid,"name":x["name"],"source_categories":";".join(food),"source_population_tags":";".join(pop),"ingredient_count":len(d.get("major",[])),"nutrient_count":len(ns),**{k:rec[k] for k in ("recipe_status","aliases_resolved","step_only_consumed_terms","identity_conflict_terms")},**{k:q[k] for k in ("internal_consistency","internal_flags","macro_energy_relative_diff","global_status","review_priority","review_reasons")},**t})
    write_csv(a.output_dir/"p1_case_registry.csv",registry);write_csv(a.output_dir/"qc_cases.csv",qc);write_csv(a.output_dir/"task_eligibility.csv",tasks);write_csv(a.output_dir/"recipe_reconciliation.csv",recons)
    rc=Counter(z["recipe_status"] for z in registry);gc=Counter(z["global_status"] for z in registry);pc=Counter(z["review_priority"] for z in registry);tc={k:Counter(z[k] for z in registry) for k in tasks[0] if k.startswith("T")}
    summary={"n_cases":len(rows),"id_range":[rows[0]["item_id"],rows[-1]["item_id"]],"contiguous_ids":all(int(rows[i]["item_id"])==int(rows[0]["item_id"])+i for i in range(len(rows))),"unique_ingredients":len(global_ing),"ingredient_lines":ing_lines,"ingredient_code_coverage":sum(bool(z.get("code")) for x in rows for z in x["detail"].get("major",[]))/ing_lines,"ingredient_id_coverage":sum(z.get("ingrId") is not None for x in rows for z in x["detail"].get("major",[]))/ing_lines,"nutrient_union":len(all_n),"nutrient_intersection":len(common_n or set()),"nutrient_count_min":min(z["nutrient_count"] for z in registry),"nutrient_count_median":statistics.median(z["nutrient_count"] for z in registry),"nutrient_count_max":max(z["nutrient_count"] for z in registry),"internal_consistency_pass":internal_pass,"unit_pattern_count":len(unit_patterns),"recipe_status_counts":dict(rc),"global_status_counts":dict(gc),"review_priority_counts":dict(pc),"task_eligibility_counts":{k:dict(v) for k,v in tc.items()},"macro_energy_median_rel_diff":statistics.median(macro),"macro_energy_max_rel_diff":max(macro),"food_category_counts":dict(cats),"population_tag_counts":dict(pops),"dish_name_contains_lamb":sum("羊" in x["name"] for x in rows),"decision":"CONDITIONAL_PASS_SCALE_ENGINEERING_NOT_CORPUS_WIDE_ESTIMATE"}
    (a.output_dir/"p1_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"
",encoding="utf-8")

if __name__=="__main__":main()
