"""Confirm booth numeric slot23 replaces resident intent font with shared196."""
from pathlib import Path
import csv,json
from seal_nonplay171 import R,sha,seal

def main():
    report=R/'qa/reports/issue176_diagnosis.json';assert not report.exists()
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';b=rom.read_bytes()
    p=R/'qa/dialogue/issue176_slot11_049';e=json.loads((p/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['ROM_sha256']==sha(rom)
    for f,h in e['files'].items():assert sha(p/f)==h
    ram=(p/'frame_003_ram.bin').read_bytes();ppu=(p/'frame_003_ppu.bin').read_bytes()
    assert ram[0x25]==6 and ram[0x6f3]==ram[0xc6]==196 and ram[0x34]==204
    intent=json.loads((R/'build/dialogue_kr_poc_022/ui_korean_page_mapping.json').read_text('utf-8'))
    intent=next(x for x in intent if x['profile']['entry_id']=='MAIN_05782')
    assert b[0x25782:0x25794]==bytes.fromhex(intent['body_hex'])
    assert ppu[0x22a8:0x22a8+11]==bytes.fromhex('2b2c2d2e7a2f2728292a7a')
    assert ppu[0x22e8:0x22e8+8]==bytes.fromhex('30317a323334357a')
    assert b[0x5710+2*0x13]==162 and b[0x5710+2*0x23]==196
    maps=list(csv.DictReader((p/'frame_003_mapping.csv').open(encoding='utf-8')))
    lower=next(x for x in maps if x['kind']=='chr' and x['address']=='0000');assert int(lower['relative_offset'],16)==196*1024
    assert ppu[:0x800]==b[0x40010+196*1024:0x40010+198*1024]
    assert b[0x25cd9:0x25ce6]==bytes.fromhex('a9 23 8d cf 06 a9 04 20 17 94 4c 5e 92')
    assert b[0x25d73:0x25d76]==bytes.fromhex('20 c9 9c')
    result={'work':176,'status':'CONFIRMED049_BOOTH_NUMERIC_REFRESH_FONT_COLLISION_FIX_PENDING',
        'ROM_sha256':sha(rom),'user_host_sha256':e['exe_sha256'],'scope':'Copied user saved booth state in identical private host; user live memory unavailable.',
        'visible_text_source':'MAIN_05782','expected_font_pair':[162,163],'actual_font_pair':[196,197],
        'expected_text':['포인트를 티켓으로','바꿔 드릴게요'],'observed_garbled_text':['요금은장 내티켓을','줘아 쉽지만더'],
        'resident_NT_intent_codes_preserved':True,'mapped_CHR_matches_ROM196':True,'ticket_count':16,'score_display':30,
        'pending_dialogue_ID_hex':'15','active_pointer_hex':'98E0','booth_course_value':6,
        'native_numeric_caller':'bank32 9CC9: slot23, arg4, JSR9417, JMP925E; invoked by9D63 after exchange',
        'cause':'Global font table tags shared F9 numeric slot23 as196. Booth upper numeric refresh calls same initializer and overwrites resident lower intent font162, while old NT text remains.',
        'proposed_fix':'For numeric slot23 on booth course6, preserve resident lower font; reuse fixed-cycle selection padding so other consumers/timing remain unchanged.',
        'needs_validation':['actual native cold-entry/exchange numeric caller trace','matched cycle/ABI and other slots/ride contexts','same exchange reproduction after fix','adjacent booth and shared ride lower paths'],
        'original_ROM_SSOT_or_user_session_modified':False,'human_final_review':False,'release_eligible':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자가 티켓교환 후 대사 깨짐을 신고했고 실제 스크린샷을 제공했다. 실행프로세스22308/H:\\Mesen\\Mesen.exe/MesenCE, 최근ROM경로와 파일SHA는현재049임을 확인했다. Computer Use native pipe 연결2회실패(os error2), emucap 미연결로 현재live메모리/화면을 직접읽지는못했다. CLI의script-only 전달은원문소스에서기존게임에즉시실행되지않으므로사용하지않았다. 대신 사용자MesenCE2.2.1 exe/DLL을격리복사하고해당게임저장상태1/11을프로젝트QA에복사해12프레임씩재현했다. 사용자프로세스/ROM/설정/세이브는수정하지않았다. MSS포맷4는ROM SHA를내장하지않으므로현재파일SHA·사용자신고·같은원천이름/장면으로귀속하며저장상태자체의해시증명과구분한다.

[진단](../qa/reports/issue176_diagnosis.json): 복사한문제장면에서도티켓16/점수30과같은깨진문구를확인했다. 하단NT는 MAIN_05782 ‘포인트를 티켓으로 / 바꿔 드릴게요’의정상코드인데RAM C6/06F3=196, 실제PPU CHR=196/197(놀이기구요금공유폰트)다. 원래이문장의폰트는162/163이다. 그래서그코드가‘요금은장 내티켓을 / 줘아 쉽지만더’로읽힌다. 깨진번역바이트가아니라폰트선택충돌이다.

native bank32 9D63→9CC9는slot23/arg4를9417에넣어925E로상단소지숫자를갱신한다. 전역font table의slot23=196이현재하단폰트를바꾸지만하단NT는기존문구를유지한다. 저장상태의pending15와실제pointer98E0를확정표시15본문으로혼동하지않는다. 다음수정은매표소course6의숫자slot23에서거주하단폰트를보존하는것이며, 기존helper padding을같은cycle 분기로대체해공통요금/다른본문동작을보존한다. 실제cold-entry/교환콜러trace와수정후회귀가완료돼야fixed로닫는다.

[준비/귀속](../qa/issue176_user_booth/provenance.json), [읽기용Lua](../scripts/trace_issue176.lua), [재현runner](../scripts/run_issue176.py). 재현: `python scripts/run_issue176.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --state qa/issue176_user_booth/user_slot11.mss --output qa/dialogue/issue176_slot11_049` (기존출력보호,사본에서새경로사용). 정적코드/바이트·저장상태격리복원/12프레임raw/실제PNG PASS, 현재사용자live직접읽기및교환caller새재생은아직미수행이다. 새게임전장면QA/빌드/적용/청음/최종사람승인 없음. 현재049 ROM `{sha(rom)}`/CSV불변. 변경:176준비/observer/runner/진단/인계·사용자상태복사/격리host·QA/environment/manifest·canonical. 이전175의‘확인한기록의새수정없음’은당시한계며이번자연사용자신고로현범위결함을추가했다. 카페완성글/외부게시없음.

포맷/CLI근거: [MesenCE SaveStateManager](https://github.com/nesdev-org/MesenCE/blob/master/Core/Shared/SaveStateManager.cpp), [CLI Script 분류](https://github.com/nesdev-org/MesenCE/blob/master/UI/Utilities/CommandLineHelper.cs), [기존인스턴스 인자처리](https://github.com/nesdev-org/MesenCE/blob/master/UI/Windows/MainWindow.axaml.cs). 이번포맷값과복원성공은별도로실측했다. 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay176_assets.json --output qa/reports/nonplay176_session.json`.'''
    files=[Path(__file__),R/'scripts/prepare_issue176.py',R/'scripts/run_issue176.py',R/'scripts/trace_issue176.lua',report,rom,R/'workspace/translation/text_ja.csv',
        R/'workspace/asm/dialogue_page_font_009.asm',R/'build/dialogue_kr_poc_022/ui_korean_page_mapping.json',R/'build/dialogue_kr_poc_036/ui_stage_lower_shared_font.json']
    for d in [R/'qa/issue176_user_booth',R/'tools/mesence_user176',R/'qa/dialogue/issue176_slot1_049',p]:files.extend(q for q in d.iterdir() if q.is_file())
    seal(176,'BOOTH_EXCHANGE_FONT_COLLISION_176.md','사용자 티켓교환 대사 깨짐 재현·진단',body,
        '사용자자연신고를동일2.2.1격리host/복사상태로재현. 정상MAIN05782 NT가162대신196폰트에표시됨. 상단F9 slot23 초기화가하단폰트를덮는결함등록; 수정전.',
        '매표소 숫자slot23에서 기존 하단폰트를 같은 사이클로 보존하는050 후보를 만들고, 교환 caller와 인접경로의 원인/수정 회귀를 검증한다.',files)
    p=R/'docs/HANDOFF.md';text=p.read_text('utf-8');text=text.replace('확인한 기록에서 새 수정 요구는 없으며 사용자 플레이/최종 문구·명칭·그림 결과를 기다린다.',
        '작업176에서 사용자 자연 티켓교환 후 대사깨짐을 접수·재현했다. 매표소 숫자갱신 slot23이하단162폰트를196으로바꾸는현범위결함이며수정/회귀전이다.175의새수정없음은그당시확인기록에한정된다.',1);p.write_text(text,'utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
