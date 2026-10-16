"""Adopt verified050 with exact task handoff and frozen evidence."""
from pathlib import Path
import json,re
from seal_nonplay171 import R,sha,seal

def main():
    v=R/'qa/reports/issue177_validation.json';d=json.loads(v.read_text('utf-8'));assert d['status']=='PASS_FOCUSED_BOOTH_FONT_FIX_AND_ADJACENT_REGRESSION'
    rom=R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)==d['ROM_sha256']
    body=f'''사용자 신고176의 같은 폰트 충돌을 cold boot/controller로 재현하고050에서 수정했다. 변경은 [helper010](../workspace/asm/dialogue_page_font_010.asm)의 매표소course6/숫자slot23 글꼴 선택과 intro_setup 재배치 호출주소다. 숫자 초기화에서 기존 하단06F3를 보존한다. 일반 놀이기구slot23은 전역196을 사용한다. native text/숫자 caller, 번역CSV, CHR, 전역폰트표, IRQ 코드는 불변이다.009의30cycle padding을 세30cycle 분기로 교체하여049 대비 추가시간0이다. 변경PRG179바이트, 크기499728바이트, helper217바이트이며9700폰트표와 겹치지 않는다. [빌더](../scripts/build_booth177.py)는 source Expected Writes9개를 다시 검증하며 허용5영역 밖의 변경을 거부한다.

정적/CPU: 48slot×7course×5phase×8resident-font×4flag=53,760사례의 A/X/Y/P/SP·은행·시간 동등성 및 비대상RAM 보존 PASS. boothslot23 보존160사례, intro16사례 PASS. IRQ코드/쓰기시간 불변. [독립 재빌드](../build/issue177_rebuild050/build_report.json) ROM/IPS byte-exact PASS. source→IPS→050 exact PASS. ROM SHA `{sha(rom)}`; CSV SHA `{d['CSV_sha256']}`. 기존049/실패048/원본/1편/사용자실행본은 보존한다.

실행: [분기 runner](../scripts/run_booth177.py)는 사용자 MesenCE2.2.1과 동일한176 격리복사 host에서 실행했다. initial currency seed만frame1000에 기록하고 native controller 입력을 재생했다. 강제PC/ROM쓰기/저장상태복원은 없다. [검증](../qa/reports/issue177_validation.json): 049/050 각각 exchange/zero-point booth/ride3/ride4 네분기, paired EndFrame1116개. 실제9417→9445 콜러/ID/타이밍·pointer·CPU/PPU상태는 선택CHR 외 동등하고RNG22도 전부같다. 교환native9CC9의9CD2 return을12회 확인: initialwelcome1회 + 교환갱신10회 + 마지막숫자갱신1회.049는162→196,050는162 유지. tickets6→16과초기seed된points 소진, 이후15 farewell188 정상. zero-point14 shortage164, ride3의29 clear-phase0 retain/phase3 shortage226→2B possession196, ride4의23/2A success196 경로 PASS. ride 두경로 모든NT/PPU/OAM/PNG byte-exact, liveCPU/PPU serialized값동일(비활성stack반환주소만허용). booth 모든NT/OAM과 상단숫자/점수/테두리/캐릭터 RGB 동일; 차이는 대상 lower CHR와 exchange26PNG의문장그림이다.

실제 PNG 직접 확인: [기존 깨짐1710](../qa/dialogue/issue177_exchange_049/frame_01710.png), [수정1710](../qa/dialogue/issue177_exchange_050/frame_01710.png), [환영1560](../qa/dialogue/issue177_exchange_050/frame_01560.png), [작별1920](../qa/dialogue/issue177_exchange_050/frame_01920.png), [포인트부족1920](../qa/dialogue/issue177_booth0_050/frame_01920.png), [요금1680](../qa/dialogue/issue177_ride3_050/frame_01680.png), [티켓부족2220](../qa/dialogue/issue177_ride3_050/frame_02220.png), [소지2730](../qa/dialogue/issue177_ride3_050/frame_02730.png), [성공출발2220](../qa/dialogue/issue177_ride4_050/frame_02220.png). 고장문구가 ‘포인트를 티켓으로 / 바꿔 드릴게요’로 정상표시됨을 확인했다. 전게임완주/청음/사용자최종문구승인은 이검증에 포함하지 않는다.

050를 현재개발본으로 채택한다. 이미깨진049 저장상태를050에 불러와도 해당상태의CHRmappings가자동복구되지는 않는다. 새ROM을 열어 reset/일반진행으로 매표소에 재진입하는 방법으로 검수한다. 원문유지6건의 사용자선택은 그대로이며 CHR/등록본문/후보원천바이트 불변이다. 카페완성작업기/게시없음. 현재사용자Mesen은 그대로두었다. 재현 명령예: `python scripts/run_booth177.py --rom build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/NEW_050 --frames 2700 --inputs qa/dialogue/booth141_points3_049/inputs_used.json --script scripts/trace_booth_reader141.lua --seed config/issue177_booth_points30_tickets6.json` (기존출력보호).'''
    files=[Path(__file__),R/'scripts/build_booth177.py',R/'scripts/run_booth177.py',R/'scripts/verify_booth177.py',R/'scripts/trace_booth_reader141.lua',R/'workspace/asm/dialogue_page_font_010.asm',R/'workspace/translation/text_ja.csv',v,R/'config/issue177_booth_points0.json',R/'config/issue177_booth_points30_tickets6.json']
    for folder in [R/'build/dialogue_kr_poc_050',R/'build/issue177_rebuild050',*[R/f'qa/dialogue/issue177_{k}_{n}' for k in ['exchange','booth0','ride3','ride4'] for n in ['049','050']]]:files.extend(p for p in folder.iterdir() if p.is_file())
    seal(177,'BOOTH_EXCHANGE_FONT_FIX_050_177.md','티켓교환 폰트충돌 수정050 채택',body,'사용자신고의 교환숫자갱신 폰트충돌을050에서수정.53,760 CPU사례·독립재빌드·네분기 paired1116실제화면/상태 PASS.050채택, 전체플레이/최종사람검수는별도.','050 ROM없는 적용묶음을 만들고 한글·공백 경로에서 실제 Windows 적용을 검증한다.',files)
    p=R/'README.md';s=p.read_text('utf-8');i=s.index('작업51 당시');s=f'''> **2026-10-08 현재개발050 / 작업177 완료 / 티켓교환 대사깨짐 수정.** [최신 인계](docs/HANDOFF.md)

# 현재 개발본 — 작업177 / 050

[교환 수정·네분기 검증](docs/BOOTH_EXCHANGE_FONT_FIX_050_177.md), [ROM](build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes), [IPS](build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.ips).049의숫자초기화가하단글꼴을덮던문제를050에서수정했다. 등록45본문초안/9기술공유·33그림·원문유지6건은그대로다. 전체플레이/최종사람검수/정식배포는미완료다.

이전 [049 적용ZIP173](dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008.zip), [049 검토HTML173](workspace/review/nonplay049_20261008_173/review.html), [049 사용자 연결표175](workspace/review/user049_20261008_175/USER_QA_KO.md)는 역사자료이며050 적용묶음은 다음작업에서 만든다. 아래번호별기록은각당시증거다.

'''+s[i:];p.write_text(s,'utf-8')
    p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');i=s.index('[작업107 실제');s=f'''# 진행 중 — 2026-10-08, 작업177 완료

현재 **dialogue_kr_poc_050**, ROM SHA `{sha(rom)}`, CSV SHA `{d['CSV_sha256']}`. 사용자티켓교환 대사깨짐을 [작업177](BOOTH_EXCHANGE_FONT_FIX_050_177.md)에서 수정했다.049/050 동일cold입력으로원인·수정과인접네분기 paired1116시점 PASS,53,760 CPU사례와독립ROM/IPS재빌드 PASS. 사용자실행Mesen/원본/1편/기존049·048은보존했다.

[049 검수연결표175](../workspace/review/user049_20261008_175/USER_QA_KO.md)와검토HTML173은이전049기준이다. 원문유지6건은사용자결정대로 유지하고CSV/CHR는동일하다. 새050는강제저장상태복원 없이reset/매표소재진입으로검수한다. 전체플레이는사용자담당이며최종문구/명칭/그림 승인·전역원천완결·소비미확정6건은여전히닫지않았다. 이번신고수정을위한집중runtime재현만 수행했다. 전체완료후카페완성작업기를작성하며게시없음.

'''+s[i:];p.write_text(s,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업177','현재 개발050 / 작업177',1);s=s.replace('현재175:','현재177: 사용자티켓교환 대사깨짐 수정050 채택. [수정/검증](BOOTH_EXCHANGE_FONT_FIX_050_177.md). 아래175기준은이전검토자료다. 당시175:',1);p.write_text(s,'utf-8')
    print('PASS adopted050 and sealed177')
if __name__=='__main__':main()
