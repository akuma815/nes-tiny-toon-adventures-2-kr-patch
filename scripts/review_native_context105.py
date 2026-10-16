"""Work105 manual per-unit semantic notes, exact native slot/raw provenance; no prose edits."""
from pathlib import Path
import csv,json,hashlib,re
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
NOTES={
'MAIN_05609':'Acme Acres와 알려진 마을 소개의 의미를 유지. 애크미 에이커스 표기는 최종 사람 명칭 검토 대상.',
'MAIN_05625':'어느 날/마을 변두리/거대한 놀이공원이라는 세 정보가 남아 있다. 서술 반말은 다른 내레이션과 일치.',
'MAIN_0564D':'みんながそのわだいでもちきり의 떠들썩한 화제와 다음 편지 문단으로 이어지는 때 연결을 유지.',
'MAIN_05665':'source macro81 バスター와 뒤의バニー를 버스터 바니로 문맥 치환. global macro 정의 변경은 아님.',
'MAIN_0568B':'악당의おれさま/しょうたいしてやる는 내 놀이공원/초대하마의 우쭐한 초대 말투로 남음.',
'MAIN_056C1':'동료 동반/놀랄 것이다/의문의 대부호 서명 세 내용을 유지. 대부호로부터는 서명에 대응.',
'MAIN_056EE':'편지를 읽은 버스터 일행의 기쁨과 narration 말투가 일치.',
'MAIN_0570D':'악당 웃음의 세 반복과 원래 인용 부호를 보존.',
'MAIN_05718':'함정/장치가 가득한 놀이공원에서 기다리겠다는 위협. 기다리마가 letter sender 말투와 일치.',
'MAIN_05741':'선택 질문どれにする를 놀이기구 선택 문맥의 어디로 갈까로 옮김.',
'MAIN_0574D':'macro84 제트코스터 계열을 채택된 롤러코스터 명칭으로 일관되게 표시.',
'MAIN_05750':'macro85 쇼킹카트 계열의 선택명. 규칙/타이틀의 같은 한국어와 일치.',
'MAIN_05753':'macro86 Speed Train 계열을 짧은 기차로 옮긴 기존 초안. 공식/긴 이름을 최종 승인하지 않음.',
'MAIN_05756':'macro87 water slider 계열을 게임의 급류 통나무 놀이에 맞춘 급류타기 초안. 명칭 검토는 남음.',
'MAIN_05759':'なぞのおしろ의 수수께끼 성 의미. 원문문구와 카드타이틀의 이름 일치.',
'MAIN_05762':'ticket 판매장소를 매표소로 번역. ticket macro를 인명처럼 오해하지 않음.',
'MAIN_05769':'またあとであおうね의 다시/나중에 만남을 나중에 또 보자로 유지. 뒤 빈 행은 native지우기용.',
'MAIN_05777':'매표소 인사의 환영과 서비스 존댓말. 실제 booth 문맥과 연결.',
'MAIN_05782':'포인트를 티켓과 교환한다는 방향/대상 유지. 한국어 서비스 약속 형태가 자연스럽다.',
'MAIN_05794':'포인트 부족을 티켓 부족과 혼동하지 않음. 아쉽지만/부족해요로 원래 부드러운 거절 유지.',
'MAIN_057AC':'いつでもきてね의 재방문 권유/서비스 존댓말. slot15 교환 후 매표소 대사이며 slot2A 출발 대사와 별개.',
'MAIN_057B8':'일반적인 입장 환영. gate attendant의 정확한 캐릭터 정체는 미확정으로 유지.',
'MAIN_057C1':'입장 조건 골드 티켓4장과 가능이라는 정보가047 두 행에 남음. 문장 다듬기는90/91에서 실제 검증됨.',
'MAIN_057E5':'たりませんね를 해당 문맥의 티켓 부족으로 명시. 숫자 부족량을 임의로 추가하지 않음.',
'MAIN_057F7':'再訪 요청의 다시 오세요. 소거용 빈 줄을 의미 있는 번역행으로 세지 않음.',
'MAIN_05805':'일반 티켓 variableFA장도 가능하다는 대안. 현재 가능해요는 조건을 전달하지만 도를 넣을지 스타일 검토 여지가 있음; 원문/초안 그대로 보존.',
'MAIN_0581B':'おもちですか의 소지 여부 질문. 갖고 계세요는 앞에서 설명한 티켓 조건을 가리킴.',
'MAIN_05824':'허용 이후의 입장 권유. 들어오세요는 허용 분기/출입 흐름과 맞음.',
'MAIN_05833':'놀이에 variableFA장 티켓이 필요하다는 요금 의미 유지. 티켓을 내줘는 기존 직접 권유식 초안이며 원문보다 명령이 강한지는 사람 말투 검토 대상.',
'MAIN_05849':'하이스피드 코스터와 장애물 통과를 고속 질주/모두 피하자로 플레이 목적에 맞춰 옮긴 기존 초안.',
'MAIN_05867':'적 카트를 튕겨 구멍에 떨어뜨리는 목표가 유지. 적을 직접 처치하는 다른 조건으로 번역하지 않음.',
'MAIN_05882':'기차 위 전진/맨 앞 보스 목표 유지. 도전하자는 기다린다는 원문의 게임목표식 전환. 내부3공백은 macro86 폭 제약이며 단순 prose 띄어쓰기 수정으로 제거하면 안 됨.',
'MAIN_058A6':'통나무 균형과 급류 하강 두 행동이 남아 있다. 통나무 균형/통나무의 균형은 선택적 문체 검토.',
'MAIN_058CD':'마지막 스테이지와 여러 장치 주의. 피해는 조심하라는 지시의 게임적 표현.',
'MAIN_058F2':'상단 롤러코스터 타이틀이 선택명과 일치. native중앙배치 공백과 번역의 의미를 분리.',
'MAIN_058F6':'상단 쇼킹카트 타이틀이 선택명/규칙과 일치.',
'MAIN_058FA':'상단 기차 타이틀이 선택명과 일치. 긴 고유 놀이기구명 채택 여부는 사람 검토 대상.',
'MAIN_058FE':'상단 급류타기 타이틀이 선택명과 일치. 원래 water slider 장르명과 관계는 명칭 검토 대상.',
'MAIN_05902':'상단 수수께끼의 성이 마지막-stage 선택명과 일치.',
'MAIN_0590C':'티켓 부족의 실패 안내. 더 모아줘는 플레이 목표에 맞춘 기존 명령식 초안으로 조건/통화종류를 바꾸지 않음.',
'MAIN_05920':'いっくよーん의 가자/출발 감탄을 출발로 요약. slot2A 놀이기구 시작이며 매표소 재방문인사 slot15와 별개.',
'MAIN_05929':'현재 variableF8장의 티켓 소지라는 정보 유지. nativeF8는 세 자리/leadingzero blank를 생성하므로 placeholder앞 공백을 단순문자열만보고 추가하지 않음.',
'MAIN_05939':'게임명/제작진/프로그램/그래픽 직함은 한글, YAMASHITA/MIYAOKA/ISHIHARA/FUKUDA 인명은 sourceASCII 대로 유지한 기존 결정.',
'MAIN_05999':'사운드/패키지그림/팀 직함을 한글로 표시하며 TAKEYASU/KENKEN/YATAKA/SUMIDA/PONPOKORIN 철자는 source대로 보존.',
'MAIN_059E7':'PRESENTED BY를 제공으로 옮기고 KONAMI/ALL RIGHTS RESERVED는 source표시 보존. 공백행은 native스크롤/소거 범위.'}

def main():
 out=R/'qa/reports/context105_review.json';ledger=R/'workspace/translation/scene_context_105.json';assert not out.exists()and not ledger.exists();meta=j('manifests/source_rom.json');src=(R/meta['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();before=(R/'workspace/translation/text_ja.csv').read_bytes();rows=list(csv.DictReader(before.decode('utf-8-sig').splitlines(keepends=True)));assert sha(src)==meta['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256'];assert len(rows)==54 and len(NOTES)==45;by_off={int(r['file_offset']):r for r in rows};slots=[]
 for i in range(48):
  pointer=int.from_bytes(src[0x55a9+i*2:0x55ab+i*2],'little');offset=0x4010+pointer-0x8000;r=by_off[offset];assert src[0x55a9+i*2:0x55ab+i*2]==rom[0x255a9+i*2:0x255ab+i*2];assert f'{i:02X}'in r['reference_ids'].split(',');slots.append({'slot_hex':f'{i:02X}','CPU_pointer':pointer,'source_file_offset':offset,'entry_id':r['entry_id']})
 assert len({x['entry_id']for x in slots})==46
 reviewed=[];variables=0
 for r in rows:
  a,b=int(r['file_offset']),int(r['end_exclusive']);raw=bytes.fromhex(r['raw_hex']);assert src[a:b]==raw and sha(raw)==r['raw_sha256']and r['source_sha256']==meta['sha256'];assert r['status']in('draft','untranslated')
  if r['status']!='draft':continue
  assert r['entry_id']in NOTES
  source_variables=re.findall(r'\{variable_[A-F0-9]+\}',r['source_tokens']);target_variables=re.findall(r'\{variable_[A-F0-9]+\}',r['translation_ko']);assert source_variables==target_variables,(r['entry_id'],source_variables,target_variables);variables+=len(target_variables)
  reviewed.append({'entry_id':r['entry_id'],'slots_hex':r['reference_ids'].split(','),'original_view':r['original_view'],'translation_ko':r['translation_ko'],'scene_as_frozen047_CSV':r['scene'],'speaker_as_frozen047_CSV':r['speaker'],'raw_sha256':r['raw_sha256'],'manual_note':NOTES[r['entry_id']],'human_approved':False,'draft_retained':True})
 assert len(reviewed)==45 and variables==3
 overrides=[{'entry_id':'MAIN_057AC','native_slots_hex':['15'],'exact_context':'Ticket booth after successful point→ticket exchange; Babs/attendant invites return. Native slot2A is a different source paragraph MAIN_05920.','frozen_CSV_group_context_erratum':'scene and notes mention shared ride lower start/2A as a grouped description. This is not a reference or consumer of this paragraph.','ROM_or_translation_defect':False},{'entry_id':'MAIN_05920','native_slots_hex':['2A'],'exact_context':'Ordinary ride lower start encouragement, Buster; separate from booth farewell MAIN_057AC slot15.','frozen_CSV_group_context_erratum':'scene includes booth successful exchange as a grouped QA description. Source reference2A belongs to ride start only.','ROM_or_translation_defect':False}]
 data={'work':105,'source_sha256':sha(src),'ROM047_sha256':sha(rom),'CSV_sha256':sha(before),'scope':'Correct native source→slot context ledger supplements historical grouped CSV notes; prose/raw/reference IDs/status remain frozen. Use row-specific exact_context for these two records.','context_overrides':overrides,'native48_slots':slots,'human_approved':False};ledger.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
 result={'work':105,'status':'PASS_NATIVE_SOURCE_CONTEXT_AND_MANUAL_DRAFT_REVIEW','source_sha256':sha(src),'ROM047_sha256':sha(rom),'CSV_sha256':sha(before),'source54_raw_ranges_hashes_equal':True,'native48_pointer_entries_original047_equal':True,'native_unique_main_sources':46,'manual_drafts_reviewed':45,'technical_or_shared_units_not_retranslated':9,'variable_placeholders_source_target_order_equal':variables,'context_metadata_errata':overrides,'single_prose_change_required_by_this_pass':False,'style_or_name_human_review_pending':['Acme Acres/Buster Bunny/ride names','alternative-also nuance in MAIN_05805','direct request tone MAIN_05833/MAIN_0590C','train boss objective paraphrase and fixed macro-width spacing MAIN_05882','F8 rendered numeric spacing rather than placeholder-only edits MAIN_05929'],'manual_records':reviewed,'ledger':ledger.relative_to(R).as_posix(),'ledger_sha256':sha(ledger.read_bytes()),'ROM_CSV_edited':False,'human_approved':False,'limits':['Assistant manual source/context check, not final human wording/terminology approval','No final globalcorpus/full natural game/all scene visual/hardware/PCM claim','Metadata corrections are explicit supplemental exact-context records; frozen047 CSV/build/review source metadata preserved','No rule-based batch prose transformation and no new ROM/build/apply/runtime'],'next_action':'Verify current047 ordinary ride insufficient-normal3 branch and real FA/F8 numeric output/continuation context, using declared initial ticket seed.'};assert(R/'workspace/translation/text_ja.csv').read_bytes()==before;out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k!='manual_records'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()