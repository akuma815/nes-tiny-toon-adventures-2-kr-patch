"""Freeze moving STOP diagnosis/fix evidence; preserve all earlier versions."""
from pathlib import Path
import json,shutil
from seal_nonplay171 import R,sha,seal

def files(*paths):
    return [f for p in paths for f in (p.rglob('*') if p.is_dir() else [p]) if f.is_file()]

def main():
    report=json.loads((R/'qa/reports/moving_stop182_validation.json').read_text('utf-8'))
    assert report['status']=='PASS_MOVING_STOP051_NATIVE_GLYPH_ONLY_FIX'
    build=R/'build/dialogue_kr_poc_051'
    extracted=R/'extracted/graphics/moving_stop182';workspace=R/'workspace/graphics/moving_stop182'
    extracted.mkdir();workspace.mkdir()
    shutil.copyfile(build/'moving_stop_original_indices.png',extracted/'source_indices.png')
    shutil.copyfile(build/'moving_stop_kr_indices.png',workspace/'kr_indices.png')
    consumer={'work':181,'asset_id':'MOVING_STOP_SPRITE46','scope':'New moving variant; does not rewrite historical33-asset inventory.','source_rom_sha256':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d','source_bank':46,'source_bank_file_offset':0x2b810,'expanded_bank_file_offset':0x4b810,'local_tiles':list(range(40,52)),'oam_8x16_codes':['69','6B','6D','6F','71','73'],'ppu_pattern_range':['1680','173F'],'consumer_evidence':'qa/dialogue/moving_stop181_050/sprite_top_mapping.csv frame4200 PPU1400->CHR0B800; six OAM cells and actual frame4200 image.','source_png_sha256':sha(extracted/'source_indices.png'),'original_font46_equal050':True,'separate_from_fixed_bg_font224225':True,'human_final_approved':False}
    (extracted/'consumer.json').write_text(json.dumps(consumer,ensure_ascii=False,indent=2)+'\n','utf-8')
    shutil.copyfile(build/'moving_stop_plan.json',workspace/'insertion_plan.json')
    diagnosis='''사용자 설명: “처음 정지 표지판이 몇개 지나간 후 위 아래로 움직이는 표지판이 Stop으로 번역 안되어 있었다.” 라운드 분기 문제가 아니라 **고정 배경과 움직이는 스프라이트의 서로 다른 소비 경로**다. 고정 STOP은 이미224/225에 ‘정지’가 있으며050의 첫 세 표지판 실제 화면에서도 확인했다. 움직이는 표지판은별도CHR46 원문 STOP을 사용한다.

실제 소비: OAM 8×16 코드69/6B/6D/6F/71/73,24×32의6셀. native frame4200의 PPU1400→CHR0B800(46), PPU1680..173F→local40..51, 원본 파일2B810/확장파일4B810의같은원문그림. [소비 기록](../extracted/graphics/moving_stop182/consumer.json), [050 실제 화면](../qa/dialogue/moving_stop181_050/frame_04200.png). RAM36의 일반캐릭터폰트만으로Sprite1000..1FFF 전부를추정했던CHR22 후보는오판이며분석PNG로만보존했다.

조사/실패: 최초runner181은고정176 host SHA 불일치로실행전중단. 현재사용자host를새전용tools/mesence_user181로복사해V2로재현했다. 사용자세이브복사11 재생은다른카트미니게임(root4/course1)이라STOP 재현에쓰지않았다. 첫고정표지판용cold run도오른쪽이동이없어움직이는구간까지가지않았다. 기존042 캡처는후보발견에만쓰고현재수정검증에는쓰지않았다. 실패/오관측파일을그대로보존했다. 저장상태사용여부의기존질문은사용자의움직이는표지판설명으로대체됐으며원인을사용자세이브로돌리지않는다.

HUD: “전체 놀이기구 화면에서같다”는사용자검수결과로기록. [작업180 원본 비교](HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md)의왼쪽띠/아래여백 원본구성,한글HUD2픽셀이동을구분한다. 새전놀이기구실행검증으로확대하지않으며이번HUD수정은없다.

정적: source/050 CHR46 동일,고정표지판224/225 보존. 실행:5000frame controller-only coldboot,오른쪽+B 및점프,강제상태복원/생명seed/PC/RAM/ROM쓰기없음. frame4134..의움직이는원문 STOP 확인. 원본과050 첫고정표지판은별도cold실행으로관측. 전체플레이나직접사용자Mesen 메모리접속은하지않았다. 사용자실행중Mesen/설정/원본/세이브/1편은수정하지않았다.

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`;050 SHA `49b8e869a232657f88c1810c3319d0f79b0ee23dd1ed993cf2bfc1f48726dc25`. host/상태SHA와복사출처는qa/issue181_user_stop/provenance.json 및host_provenance.json,전체QA 해시는manifests/nonplay181_assets.json 참조.

재현: `python scripts/run_moving_stop181.py --rom build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/NEW_STOP050 --frames 5000 --inputs config/moving_stop181_train5000.json --script scripts/trace_moving_stop181.lua`. 출력은새경로를쓴다. 사용자신고대상집중재현이며자동완주실험은아니다.'''
    seal(181,'MOVING_STOP_CONSUMER_DIAGNOSIS_181.md','움직이는 STOP 별도소비 진단',diagnosis,'고정정지와다른CHR46 스프라이트원문 STOP 확인. 사용자HUD 전놀이기구관측은별도기록. 잘못된CHR22 추정/host가드실패/다른카트세이브 관측을보존했다.','CHR46 움직이는표지판의글자영역만정지로삽입하고동일입력재현을비교한다.',files(R/'qa/issue181_user_stop',R/'qa/dialogue/stop181_user050',R/'qa/dialogue/stop181_train050',R/'qa/dialogue/stop181_train_source',R/'qa/dialogue/moving_stop181_050',R/'work/stop181',R/'tools/mesence_user181',extracted,*[R/'scripts'/n for n in ['run_stop181.py','run_stop181_v2.py','run_stop181_cold.py','run_moving_stop181.py','trace_moving_stop181.lua']],R/'config/moving_stop181_train5000.json',Path(__file__)))
    body=f'''[개발051 ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes) SHA `{report['ROM_sha256']}` / [IPS](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.ips) SHA `{sha(build/'TinyToon2_dialogue_kr_poc.ips')}`. [정적/빌드계획](../build/dialogue_kr_poc_051/build_report.json), [최종검증](../qa/reports/moving_stop182_validation.json). builder의runtime Pending는作成당시기록으로보존하고이최종검증으로051을채택한다.

수정:24×32 표지판의기울어진내부글자영역에고정표지판과같은Galmuri7 ‘정지’를삽입했다. CHR46의6타일42/43/45/48/49/50 총58바이트만050에서변경. 1↔2의녹색/검정글자픽셀만바꾸고투명/빨강·외곽/기둥은보존했다. PRG/헤더/IRQ/타이밍/고정224225/다른CHR/CSV는050과동일. [추출원천](../extracted/graphics/moving_stop182/source_indices.png), [편집원천](../workspace/graphics/moving_stop182/kr_indices.png), [삽입계획](../workspace/graphics/moving_stop182/insertion_plan.json). 기존33그림원장을고쳐전역완료로만들지않고이번추가소비를별도기록한다. 원문유지6건의선택도바꾸지않았다.

빌드:원본Expected Write/기대원본/중첩금지/전체model검사,PNG인덱스↔CHR왕복,원본IPS적용 PASS. 별도폴더독립ROM/IPS재빌드 byte-exact PASS. CSV SHA `{report['CSV_sha256']}`.

에뮬레이터:같은전용Mesen/설정/입력/observer로050·051 각5000frame.734 paired화면의RAM/OAM/매퍼/CPU·PPU상태및HUD-time PPU덤프 byte-exact.644전체PNG 동일;90화면의7451변경픽셀은각표지판의정확한원문/번역글자쌍(녹색/검정)에서만변경. 상단실제매퍼288 CHR청크를각ROM과일치검사했다. HUD전체RGB,고정정지표지판,움직임/게임상태 보존. 전체게임/기차완주나최종사람그림승인은아니다.

직접화면: [4200 수정전](../qa/dialogue/moving_stop181_050/frame_04200.png)/[수정후](../qa/dialogue/moving_stop182_051/frame_04200.png)에서원문 STOP→정지 확인.4272의두표지판장면도수정후확인. 첫검증V1은endFrame의다음OAM과완료이미지사이에단일공통offset을요구해4272에서실패했다. 각각움직이는두표지판의시차를별도로취급한V2에서모든변경픽셀의정확한글자쌍을검증했다(객체별offset±2). 실패V1도보존하며넓은사각형허용으로덮지않았다.

재빌드: `python scripts/build_moving_stop182.py --output build/NEW_051`. 실행은181 명령의ROM/출력을051/새폴더로바꾼다. `python scripts/verify_moving_stop182_v2.py`는고정증거를다시쓰기방지하므로기존보고를재생성하지않는다. 변경파일/전체SHA:manifests/nonplay182_assets.json. 사용자원본/1편/Mesen/세이브/이전build/검증자료보존. 카페완성작업기/게시없음.'''
    seal(182,'MOVING_STOP_GLYPH_FIX_051_182.md','움직이는 STOP 한글화051·동일조건 검증',body,'051채택:CHR46 58바이트 글자만정지로수정.734 paired화면/상태 exact;90화면 글자픽셀만변경,644전체화면동일.독립ROM/IPS재빌드PASS.','원본일본판에적용하는051 ROM없는검수ZIP을만들고실Windows 적용검증한다.',files(build,R/'build/moving_stop182_rebuild051',workspace,R/'qa/dialogue/moving_stop182_051',R/'qa/reports/moving_stop182_validation.json',*[R/'scripts'/n for n in ['build_moving_stop182.py','verify_moving_stop182.py','verify_moving_stop182_v2.py']],Path(__file__)))
    print('PASS handoffs181/182; adopted051 pending package183')

if __name__=='__main__':main()
