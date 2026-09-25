#!/usr/bin/env python3
"""Build MNC v0.1 P1-H3 Health QA Gold-100.

Inputs are P1 canonical tables plus a frozen one-dish-one-family assignment.
The builder is deterministic and intentionally refuses personalized medical advice,
clinical thresholding from unresolved serving/basis semantics, and semantic upgrades.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

ANIMAL_KW = ['猪','牛','羊','鸡','鸭','鹅','鱼','虾','蟹','蛏','贝','蚝','肉','肝','肫','腰','血','蛋','奶','火腿','腊','鳕','青鱼','黄鱼','鱿鱼','排骨']
PLANT_KW = ['豆','菜','菠菜','韭','椒','萝卜','菇','藕','花生','谷','燕麦','米','面','玉米','梨','桃','瓜','豆芽','山药','土豆','芹','葱','姜','蒜']

FAMILY_META = {
'SODIUM_POTASSIUM_INTERACTION': ('PEF-ADULT-BP','CLM-SOD-BP-001;CLM-POT-BP-001;INT-NAK-BP-001','EV-BMJ-SOD-2020;EV-JAHA-POT-2020;EV-ADV-NAK-2021','joint_exposure_with_measurement_boundary'),
'SFA_CHOL_INTERACTION': ('PEF-ADULT-CVD','CLM-SFA-CVD-001;CLM-CHOL-CVD-001;INT-SFA-CHOL-001','EV-COCHRANE-SFA-2020;EV-AHA-CHOL-2020','pattern_context_reject_single_nutrient_label'),
'IRON_VITC_INTERACTION': ('PEF-IRON-GENERAL','CLM-FE-REQ-001;INT-FE-VC-001','EV-ODS-FE-CURRENT;EV-ODS-VC-CURRENT','bioavailability_context'),
'FOLATE_B12_SEMANTIC': ('PEF-PRECONCEPTION-FOLATE','CLM-FOL-FORM-001;CLM-FOL-NTD-002;INT-FOL-B12-001','EV-ODS-FOL-CURRENT;EV-ODS-B12-CURRENT;EV-COCHRANE-FOL-2015','semantic_block_and_safety'),
'CALCIUM_VITD_CONFLICT': ('PEF-OLDER-CA-VD','CLM-CA-BONE-001;CLM-CA-SUPP-002;INT-CA-VD-001','EV-ODS-CA-CURRENT;EV-JAMA-CA-2017','adequacy_vs_intervention_conflict'),
'PROTEIN_ACTIVITY': ('PEF-HEALTHY-RE','CLM-PROT-RDA-001;CLM-PROT-RE-002','EV-NASEM-PROT-DRI;EV-JCSM-PROT-2022','activity_context'),
'PURINE_GOUT': ('PEF-GOUT','CLM-PUR-GOUT-001;CLM-PUR-FLARE-002','EV-ACR-PUR-2020;EV-JHPN-PUR-2025','disease_specific_low_certainty'),
'IRON_PREGNANCY': ('PEF-PREG-IRON','CLM-FE-REQ-001;CLM-FE-PREG-002','EV-ODS-FE-CURRENT;EV-JAMA-FE-2024','population_specific_reject_dish_treatment'),
}

def fmt(x):
    return f'{float(x):g}'

def source_context(names):
    has_animal=any(any(k in n for k in ANIMAL_KW) for n in names)
    has_plant=any(any(k in n for k in PLANT_KW) for n in names)
    if has_animal and has_plant:return 'mixed_heme_nonheme_possible'
    if has_animal:return 'heme_and_nonheme_possible'
    if has_plant:return 'predominantly_nonheme_possible'
    return 'unknown'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--nutrients',type=Path,required=True)
    p.add_argument('--anchors',type=Path,required=True)
    p.add_argument('--ingredients',type=Path,required=True)
    p.add_argument('--assignment',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    nut=pd.read_csv(a.nutrients); anchors=pd.read_csv(a.anchors); ing=pd.read_csv(a.ingredients); assn=pd.read_csv(a.assignment)
    lookup={(r.dish_id,r.nutrient_name):(r.value,r.unit) for r in nut.itertuples()}
    ingmap=ing.groupby('dish_id')['source_name'].apply(list).to_dict()
    rows=[]
    for i,r in assn.iterrows():
        dish=r.dish_id; name=r.dish_name; fam=r.qa_family
        pop,claims,evidence,aclass=FAMILY_META[fam]
        v=lambda n:lookup.get((dish,n),(None,''))
        if fam=='SODIUM_POTASSIUM_INTERACTION':
            na,una=v('Na'); k,uk=v('Kalium'); ratio=float(na)/float(k)
            q=f'菜肴“{name}”的源营养画像报告钠 {fmt(na)} {una}、钾 {fmt(k)} {uk}。能否据此判断它适合高血压人群，或把该菜的 Na/K={ratio:.2f} 直接解释为每日/24小时钠钾比？'
            ans='不能。可做的结论是：这道菜的同一源营养画像同时报告了钠和钾；人群层面证据支持钠降低、钾摄入及较低24小时尿钠/钾比与血压相关。但当前菜肴营养 basis/serving 尚未确认，菜肴组成 Na/K 不是24小时尿钠钾比，也不是个体每日摄入比，因此不能据此给出“适合高血压患者”或个体化降压建议。'
            req=['准确读取Na与K','指出Na/K仅为菜肴组成层描述','调用Na/K与血压的人群证据','明确basis/serving边界','拒绝个体适宜性判断']; forb=['将菜肴Na/K当作24小时尿Na/K','直接判断适合/不适合高血压患者','宣称钾可抵消钠']
        elif fam=='SFA_CHOL_INTERACTION':
            s,u=v('Sfa'); c,uc=v('Cholesterol'); q=f'“{name}”报告饱和脂肪 {fmt(s)} {u}、胆固醇 {fmt(c)} {uc}。能否仅凭胆固醇数值把这道菜标记为“心血管不健康”？应如何联合解释 SFA 与胆固醇？'; ans='不能仅凭胆固醇数值做心血管健康标签。膳食胆固醇与CVD的独立关系不适合简化成单一阈值，需结合饱和脂肪和整体膳食模式；长期随机试验证据支持持续降低SFA可减少综合心血管事件，但对死亡等终点更不确定。这里最多做联合暴露和证据背景解释，不能预测单道菜会导致心血管事件。'; req=['读取SFA与胆固醇','区分胆固醇证据与SFA证据','加入整体膳食模式/替代营养素背景','保留终点不确定性','拒绝单菜疾病标签']; forb=['胆固醇高=心血管不健康','SFA降低一定降低死亡率','预测单道菜的心血管事件风险']
        elif fam=='IRON_VITC_INTERACTION':
            fe,ufe=v('Fe'); vc,uvc=v('VitaminC'); src=source_context(ingmap.get(dish,[])); q=f'“{name}”报告铁 {fmt(fe)} {ufe}、维生素C {fmt(vc)} {uvc}，配料来源初筛为“{src}”。能否因此断言这道菜铁吸收率高，或可用于治疗缺铁？'; ans='不能。维生素C可以促进非血红素铁吸收，因此 Fe×Vitamin C 是有意义的生物利用度交互；但当前记录只有总铁和菜肴维生素C，不能确定血红素/非血红素铁的比例、植酸/多酚等抑制因素、实际摄入量或个体铁状态。故只能说明存在可能有利于非血红素铁吸收的组成背景，不能量化吸收率，更不能把菜肴当作缺铁治疗。'; req=['读取Fe与VitaminC','指出VitaminC促进nonheme铁吸收','区分总铁与吸收铁','要求heme/nonheme与个体状态','拒绝治疗结论']; forb=['铁含量=实际吸收量','维生素C保证高吸收','菜肴治疗缺铁性贫血']
        elif fam=='FOLATE_B12_SEMANTIC':
            fol,uf=v('FolicAcid'); b,ub=v('VitaminB12'); q=f'“{name}”源字段报告 FolicAcid {fmt(fol)} {uf}、Vitamin B12 {fmt(b)} {ub}。能否把该 FolicAcid 数值直接连接到围受孕期叶酸预防神经管缺陷证据，或据此判断 B12 安全性？'; ans='不能。当前源字段 FolicAcid 尚未说明它代表天然食物叶酸、强化/补充剂中的合成叶酸，还是DFE；而神经管缺陷预防证据针对围受孕期 folic acid supplementation。此外，高量叶酸可能纠正B12缺乏所致巨幼细胞性贫血而不能纠正神经损害，但这是个体状态/补充剂层面的安全问题，不能由一道菜的两个营养字段推断。此条应保持 semantic block。'; req=['识别folate/folic acid/DFE语义差异','指出NTD证据的剂型与时机限定','指出B12安全问题属于个体/高摄入背景','保持BLOCK而非强行连边']; forb=['FolicAcid字段=DFE','该菜预防NTD','根据菜肴B12/folate判断个人神经安全']
        elif fam=='CALCIUM_VITD_CONFLICT':
            ca,uca=v('Ca'); vd,uvd=v('VitaminD'); q=f'“{name}”报告钙 {fmt(ca)} {uca}、维生素D {fmt(vd)} {uvd}。是否可以据此向社区居住老年人宣称这道菜能够预防骨折？'; ans='不能。钙和维生素D与骨健康具有明确生理意义，但“食物中同时含有两种营养素”与“补充剂干预能否降低骨折”是不同科学问题。针对社区居住老年人的随机试验Meta-analysis并未显示常规钙、维生素D或联合补充可降低骨折发生率。因此这道菜最多可描述其营养组成，不能升级为骨折预防功效。'; req=['区分营养素生理作用与干预疗效','区分食物与补充剂','正确处理社区老年人RCT null evidence','拒绝骨折预防宣称']; forb=['钙+维D菜肴预防骨折','RCT补充剂结果直接外推到食物','钙对骨健康无意义']
        elif fam=='PROTEIN_ACTIVITY':
            pr,up=v('Protein'); q=f'“{name}”报告蛋白质 {fmt(pr)} {up}。能否仅凭这个数值把它标记为“增肌菜”或声称可预防肌少症？'; ans='不能。健康成人蛋白质需求是按体重和全天摄入定义的；关于瘦体重/力量的随机试验证据显示，增加蛋白质摄入的额外获益主要出现在阻力训练等特定背景，且效应总体较小、部分功能结局不明确。当前单道菜又缺少确认的 serving/basis、体重、全天摄入和运动信息，因此不能建立“增肌”或“预防肌少症”标签。'; req=['识别体重/全天摄入需求','加入阻力训练上下文','保留效应大小/功能不确定性','拒绝增肌/防肌少症标签']; forb=['高蛋白菜=增肌','蛋白质代替阻力训练','单菜预防肌少症']
        elif fam=='PURINE_GOUT':
            pu,up=v('Purine'); q=f'“{name}”报告嘌呤 {fmt(pu)} {up}。能否把它标记为“对所有人不健康”？对于痛风患者，能否仅凭该数值直接给出禁食建议？'; ans='都不能。嘌呤的健康关联在本数据层限定于痛风人群；限制嘌呤属于条件性且证据确定性较低的生活方式建议，饮食对血尿酸的影响通常有限，且动物/植物等嘌呤来源可能具有不同意义。因此可将该菜的总嘌呤作为痛风场景下的一个暴露特征，但不能外推到普通人群，也不能仅凭单菜数值替代总体饮食评估和临床降尿酸治疗决策。'; req=['限定痛风人群','指出指南为conditional/低确定性','说明来源类型和总体管理重要','拒绝一般人群不健康标签','拒绝以饮食替代ULT']; forb=['嘌呤对所有人有害','单菜嘌呤直接决定痛风发作','饮食可替代降尿酸药物']
        else:
            fe,ufe=v('Fe'); q=f'“{name}”报告铁 {fmt(fe)} {ufe}。能否因此标记为“适合孕妇补铁”，或者认为它可以替代孕期铁补充/缺铁筛查？'; ans='不能。孕期铁需要与普通成人不同，且菜肴总铁并不等于吸收铁；是否充分还取决于全天摄入、铁来源、生物利用度和个体铁状态。随机试验证据支持孕期铁补充降低足月时缺铁和缺铁性贫血，但对更下游母婴临床结局的证据有限。单道菜的铁值不能替代孕期筛查、补充剂方案或临床治疗。'; req=['限定孕期需求','区分总铁/吸收铁','调用孕期补充的血液学证据','保留临床终点不确定性','拒绝替代筛查/补充']; forb=['该菜适合所有孕妇补铁','菜肴替代补充剂/筛查','从单菜铁值推断孕期结局']
        rows.append(dict(qa_id=f'HQA-{i+1:03d}',dish_id=dish,source_dish_id=r.source_dish_id,dish_name=name,qa_family=fam,population_fixture_ref=pop,question=q,gold_answer=ans,required_claim_refs=claims,required_evidence_refs=evidence,answer_class=aclass,scoring_components=json.dumps(req,ensure_ascii=False),prohibited_overclaims=json.dumps(forb,ensure_ascii=False),measurement_basis_status='unresolved_api_base_profile',personalized_recommendation_allowed=False,gold_status='evidence_locked_gold_candidate',review_status='pending_human_adjudication',version='P1-H3-v0.1'))
    out=pd.DataFrame(rows)
    if out.source_dish_id.nunique()!=100 or len(out)!=100:
        raise RuntimeError('Gold-100 must contain exactly 100 unique source dishes')
    out.to_csv(a.out/'health_qa_gold100.csv',index=False,encoding='utf-8-sig')
    with open(a.out/'health_qa_gold100.jsonl','w',encoding='utf-8') as f:
        for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')

if __name__=='__main__': main()
