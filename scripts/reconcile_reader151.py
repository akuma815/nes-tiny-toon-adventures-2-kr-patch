"""Reconcile new source evidence without equating registered coverage to game completion."""
from pathlib import Path
import collections,copy,hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'workspace/translation/coverage049_151.json';assert not out.exists()
 pp=R/'workspace/translation/coverage049_145.json';prior=json.loads(pp.read_text('utf-8'))
 catp=R/'extracted/text/table_20261004_001/text_tokens.json';cat=json.loads(catp.read_text('utf-8'))
 slots={z['index']:z['unit_id']for z in cat['tables'][0]['slots']};sources={z['entry_id']:z for z in cat['units']}
 units={u['entry_id']:copy.deepcopy(u)for u in prior['units']};inputs={pp.relative_to(R).as_posix():sha(pp),catp.relative_to(R).as_posix():sha(catp)}
 for name in ['cart146','coaster147','gatereader149','shortagereader150']:
  p=R/f'qa/reports/{name}_validation.json';v=json.loads(p.read_text('utf-8'));assert v['status'].startswith('PASS_')and v['CSV_sha256']==prior['CSV_sha256']
  mp=R/f'manifests/{name}_assets.json';m=json.loads(mp.read_text('utf-8'));assert m['files'][p.relative_to(R).as_posix()]==sha(p)
  ap=R/f'qa/reports/{name}_session.json';audit=json.loads(ap.read_text('utf-8'));assert audit['status']=='PASS'and audit['asset_manifest_sha256']==sha(mp)
  for z in [p,mp,ap]:inputs[z.relative_to(R).as_posix()]=sha(z)
  for route in v.get('routes',[v]):
   assert route['ROM_sha256']==prior['ROM_sha256']
   for unit,events in route['actual_read_units'].items():
    offsets={e['source_relative_offset']for e in events};s=sources[unit];size=s['end_exclusive']-s['file_offset']
    units[unit]['actual_PRG_reader_evidence'].append({'work':v['work'],'report':p.relative_to(R).as_posix(),'route':route.get('route',name),'read_count':len(events),'unique_source_byte_offsets':sorted(offsets),'source_bytes':size,'whole_unit_bytes_observed':offsets==set(range(size)),'active_fonts':sorted({e['active_font']for e in events}),'PCs':sorted({e['reader_PC']for e in events}),'scope':'Physical PRG data reads checked against current049; no inferred whole-game coverage'})
   for key,t in route.get('complete_NT_targets',{}).items():units[slots[t['slot']]]['completed_NT_evidence'].append({'work':v['work'],'report':p.relative_to(R).as_posix(),'route':route.get('route',name),'target':key,'NT':t['NT'],'font':t['font'],'first_verified_snapshot':t['complete_frames'][0],'sample_count':len(t['complete_frames']),'scope':'All native-expanded lines matched actualNT/font; frame bounds118 retained'})
  if v['work']==150:units['MAIN_0590C']['completed_NT_evidence'].append({'work':150,'report':p.relative_to(R).as_posix(),'NT':0x22a8,'font':226,'first_verified_snapshot':v['complete_shortage_NT_frames'][0],'sample_count':len(v['complete_shortage_NT_frames']),'scope':'Full native10/11tile lines matched actualNT;196→226→196 lifetime separately checked'})
 for u in units.values():
  u['actual_source_byte_reads']='Linked actual PRG records'if u['actual_PRG_reader_evidence']else 'Not linked in selected actual-reader runs'
  u['actual_reader_full_unit']=any(z['whole_unit_bytes_observed']for z in u['actual_PRG_reader_evidence'])
 read=[u['entry_id']for u in units.values()if u['actual_PRG_reader_evidence']];missing=sorted(set(units)-set(read))
 assert len(read)==49 and missing==['MACRO_061C9','MAIN_05794','MAIN_05939','MAIN_05999','MAIN_059E7']
 count=collections.Counter(u['kind']for u in units.values()if u['actual_PRG_reader_evidence'])
 result={'work':151,'status':'PASS_REGISTERED_SOURCE_EVIDENCE_RECONCILIATION','ROM_sha256':prior['ROM_sha256'],'CSV_sha256':prior['CSV_sha256'],'registered_units':54,'actual_reader_units':len(read),'actual_reader_main':count['main'],'actual_reader_macro':count['macro'],'actual_reader_full_unit':sum(u['actual_reader_full_unit']for u in units.values()),'per_unit_all_line_NT_units':sum(bool(u['completed_NT_evidence'])for u in units.values()),'actual_reader_not_yet_linked':missing,'units':list(units.values()),'verified_inputs':inputs,'human_approved':False,'release_eligible':False,'scope':'49/54 is registered-source reader evidence, never game completion percentage. Zero-RAM models exclude dynamic MAIN05805 expansion. Historical credit diagnostics do not prove natural ending.','decision':'Do not replay equivalent pages just to increase counts. Review water ride native death/segment/clear consumers and existing controller failures before selecting a new natural completion route. Winningbot cart stream remains closed.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 nxt='급류타기의 기존 자연입력 실패와 native 죽음·구간완료·입력 소비 루틴을 읽어, 전체플레이 미해결을 줄일 수 있는 새로운 관측 또는 입력 경로 하나를 설계한다. 카트 winningbot 재실행은 하지 않는다.'
 detail=f'''# 작업151 — 실제읽기 원장과 남은 작업 재평가

[새원장151](../workspace/translation/coverage049_151.json), [보존원장145](../workspace/translation/coverage049_145.json), [재현](../scripts/reconcile_reader151.py).

동결146/147/149/150 보고서·manifest·PASS audit를 검증하고145에 합쳤다. 등록54개 중 실제읽기는49개(main42+macro7), 원천 전체바이트가 읽힌unit도49개이다. native 전줄NT 근거는{result['per_unit_all_line_NT_units']}개unit에 연결됐다. 등록표54는 전역corpus의 분모도 전체게임 완료율도 아니다. 실제읽기·글꼴존재·완성출력·직접PNG·자연플레이를 구분한다.

남은 실제reader 미연결은 매표소부족 MAIN05794, credits MAIN05939/05999/059E7, MACRO061C9다. 이들은 기존장면/정적자료를 보존하며 새reader 판정을 추정해 붙이지 않았다. macro82 해당경로 미관측은 전역미사용 증명이 아니다. dynamic MAIN05805의 숫자 출력은 실제PNG/원천읽기와 zero-RAM 전줄모델을 구분했다. 크레딧의 명시적진단은 자연엔딩이 아니다.

아직 중요한 완료조건은 자연놀이기구 진행·전체경로, global corpus, HOWTO/PAUSE/POW 실제소비, 실기/청음/사람최종이다. 동일한기존페이지를 읽기수만 늘리려고 재실행하지 않는다. 다음에는 짧은메뉴 회귀와 별개의 급류 자연진행 실패 및 실제입력/장애물/구간 소비를 조사해 새로운 판별근거를 만든다.117에서닫은 카트 winningbot의 유사재시도는 하지 않는다.

변경: reconcile_reader151.py, coverage049_151.json, 본문·datedhandoff·journal·README·SURVEY·PLAN·HANDOFF, manifest/audit. 기존145와所有 QA/ROM/CSV 보존. ROM SHA `{result['ROM_sha256']}`, CSV SHA `{result['CSV_sha256']}`. 참조파일SHA는 새원장에 기록했다. 재현 `python scripts/reconcile_reader151.py` (기존출력거부). 정적·동결보고서/manifest/audit·unit분류 PASS. 새runtime/build/apply/직접PNG/reset/state/audio/실기 없음. 사람승인false·정식배포불가·카페완성기사/외부게시 없음.

다음 작업 하나: {nxt}
'''
 doc=R/'docs/READER049_REASSESSMENT.md';assert not doc.exists();doc.write_text(detail,'utf-8')
 entry='\n\n## 작업151 — 실제reader 원장·다음불확실성 재평가\n\n등록54중 실제읽기49(main42/macro7), 전체byte49.미연결5정확목록 유지·전역완료율 아님.동일페이지증거수 반복을 피하고 급류 자연진행의 새판별근거를 조사한다.\n\n[상세 변경·SHA·검증구분·재현·한계](READER049_REASSESSMENT.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;s=p.read_text('utf-8')
  if n=='LOCALIZATION_WORK_PLAN.md':s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-07 현재개발049 / 작업151 완료.**',s,count=1)
  p.write_text(s+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text(p.read_text('utf-8')+entry.replace('(READER049_REASSESSMENT.md)','(../READER049_REASSESSMENT.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[등록원천 실제읽기 재평가151](docs/READER049_REASSESSMENT.md):49개읽기·미연결5, 전체게임완료율아님.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업150 완료','작업151 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files={**inputs}
 for p in [out,doc,Path(__file__),R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv']:files[p.relative_to(R).as_posix()]=sha(p)
 m=R/'manifests/reader151_assets.json';assert not m.exists();m.write_text(json.dumps({'work':151,'files':files},indent=2)+'\n','utf-8')
 print(json.dumps({k:v for k,v in result.items()if k not in ['units','verified_inputs']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
