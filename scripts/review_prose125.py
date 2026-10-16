"""Work125: freeze assistant manual fidelity decisions, not human approval."""
from pathlib import Path
import csv, hashlib, io, json, re
R = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads((R/p).read_text('utf-8'))
def main():
    out = R/'workspace/translation/prose_review_125.json'
    assert not out.exists()
    csvpath = R/'workspace/translation/text_ja.csv'
    assert sha(csvpath) == 'ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556'
    rows = list(csv.DictReader(io.StringIO(csvpath.read_text('utf-8-sig'))))
    prior = load('qa/reports/context105_review.json')
    old = {x['entry_id']:x for x in prior['manual_records']}
    ctx = load('workspace/translation/scene_context_105.json')
    overrides = {x['entry_id']:x['exact_context'] for x in ctx['context_overrides']}
    source_meta = load('manifests/source_rom.json')
    source = R/source_meta['path']; assert sha(source) == source_meta['sha256']
    rom = R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
    assert sha(rom) == ctx['ROM047_sha256']
    records=[]; technical=[]
    notes = {
        'MAIN_05805':'も의 대안 강조는 현재 가능해요에 축약돼 있다. 조건/금액은 유지되며 이번 단일 수정 대상은 아니다. 최종 문체 선택은 보류.',
        'MAIN_05833':'원문 요금 안내를 티켓을 내줘로 끝내는 기존 목적식 표현을 유지한다. 비용 변수와 통화를 바꾸지 않는다. 높임말/명령 강도는 최종 검토 대상.',
        'MAIN_05882':'맨 앞 보스가 기다린다는 문장을 도전하자로 바꾼 목적식 초안을 유지. macro86을 위한 내부3공백은 native 출력 제약이므로 보존.',
        'MAIN_0590C':'원문은 티켓이 모자란다는 실패 안내다. 기존 더 모아줘는 추가된 수집 지시다. 이번에는 부족 상태를 직접 전달하는 아쉽지만 / 티켓이 부족해!로 개발 초안을 좁혀 수정한다. 기존 조건/통화/반말/두 행 유지. 사람 최종 승인이 아니다.',
        'MAIN_05999':'원문 PACKAGE D.의 D를 근거 없이 풀지 않는다. 기존 패키지 그림의 직함 선택은 사람 검토 대상으로 남긴다. 인명/팀 철자는 유지.'}
    for row in rows:
        raw=bytes.fromhex(row['raw_hex']);a,b=int(row['file_offset']),int(row['end_exclusive'])
        assert source.read_bytes()[a:b] == raw
        assert hashlib.sha256(raw).hexdigest()==row['raw_sha256']
        if row['status']!='draft':
            technical.append({'entry_id':row['entry_id'],'status':row['status'],'source_tokens':row['source_tokens'],'reason':'native dynamic dispatcher' if row['entry_id']=='MAIN_058F0' else 'shared native macro; inline Korean consumers use their own fonts; not an independent unfilled prose draft','human_approved':False})
            continue
        prev=old[row['entry_id']]
        assert prev['translation_ko']==row['translation_ko'] and prev['original_view']==row['original_view']
        assert re.findall(r'\{variable_[A-F0-9]+\}',row['source_tokens']) == re.findall(r'\{variable_[A-F0-9]+\}',row['translation_ko'])
        records.append({'entry_id':row['entry_id'],'slots_hex':row['reference_ids'].split(','),'original_view':row['original_view'],'translation_before':row['translation_ko'],'source_raw_sha256':row['raw_sha256'],'exact_context':overrides.get(row['entry_id'],row['scene']),'speaker_from_CSV':row['speaker'],'prior_manual_note':prev['manual_note'],'manual_decision_125':notes.get(row['entry_id'],'원문과 표시 문맥을 다시 대조했다. 기존 의미와 말투를 유지하는 개발 초안으로 보존하며, 고유명사와 최종 문체는 사람 검토 대상으로 남긴다.'),'development_action':'single_sentence_revision' if row['entry_id']=='MAIN_0590C' else 'retain_draft','human_approved':False})
    assert len(records)==45 and len(technical)==9
    plan=load('workspace/translation/ui_stage_lower_plan_001.json')
    target=next(p for p in plan['profiles'] if p['entry_id']=='MAIN_0590C')
    blob=rom.read_bytes(); assert target['font_bank']==blob[0x5710+2*0x29]==196
    assert not any(blob[0x40010+226*1024:0x40010+228*1024])
    candidate={'entry_id':'MAIN_0590C','native_slot_hex':'29','source_expanded_JA':'ざんねんだけど\nチケットがたりないよ','translation_before':'아쉽지만\n티켓을 더 모아줘!','translation_candidate':'아쉽지만\n티켓이 부족해!','reason':'Explicit shortage statement replaces the added collection instruction; ordinary ride rejection, not gold-ticket gate or booth point shortage. Deliberate assistant development fidelity choice, not a claim that the historical adaptation broke the game.','native_evidence':'docs/NORMAL3_CURRENT047_CLOSEOUT.md; native ordinary-ticket3 versus cost4 rejection and current47 NT/font196 verified in work106','implementation_constraint':'font196/197 is shared with cost/F9/start/possession. macro88 expands four fixed codes 39..42; changing 을 to 이 globally would corrupt another paragraph. Use a dedicated lower-only even font226/227 from the explicitly reserved zero range, retag only slot29; preserve shared196/197 and native macro/control bytes.','candidate_status':'development draft selected; not yet inserted','human_approved':False}
    result={'work':125,'status':'ASSISTANT_MANUAL_FIDELITY_REVIEW','source_sha256':sha(source),'ROM047_sha256':sha(rom),'CSV_sha256':sha(csvpath),'drafts_reread':45,'technical_shared_records':9,'single_selected_revision':candidate,'manual_records':records,'technical_records':technical,'prior_context_review':'qa/reports/context105_review.json','prior_context_review_sha256':sha(R/'qa/reports/context105_review.json'),'context_ledger_sha256':sha(R/'workspace/translation/scene_context_105.json'),'human_approved':False,'ROM_CSV_edited':False,'release_eligible':False,'limits':['Assistant manual review; no human approval or official Korean names inferred','No new build/apply/runtime/direct game-image QA','Registered inventory is not global corpus closure; natural whole game/hardware/PCM and graphics decisions remain open','No rule-based batch prose rewriting; only the individually grounded shortage sentence is selected'],'next_action':'Implement only MAIN_0590C draft in a new048 candidate with private226/227 font; validate source writes, native timing and reproducibility before actual rejection/next-paragraph QA.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('manual_records','technical_records')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
