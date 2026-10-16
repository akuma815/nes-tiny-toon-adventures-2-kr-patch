"""Seal opening-only paired-row implementation; stable051 remains adopted."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R,sha

def main():
    records.DATE='2026-10-09'
    build=R/'build/opening11_poc_053';report=json.loads((build/'build_report.json').read_text('utf-8'))
    proof=R/'qa/reports/opening11_cpu186.json'
    failure=R/'qa/reports/opening11_186_development_attempts.json'
    assert not failure.exists()
    failure.write_text(json.dumps({'work':186,'status':'DEVELOPMENT_ATTEMPTS_PRESERVED','attempts':[
        {'stage':'Before output','issue':'Static CPU/file address assertion missed16-byte iNES header','resolution':'Correct CPU-to-file mapping; source untouched'},
        {'stage':'Before output','issue':'PRG6 range overlapped native_gameover_low_bank06_compatibility ExpectedWrite','resolution':'Choose disjoint physical PRG8/9 private overlay; no PRG6 overwrite'},
        {'stage':'Rejected build052, never run in emulator','issue':'Canonical wrapper written at255F9 instead of25609; CPU test rejected','resolution':'053 corrected mapping, immutable052 preserved'},
        {'stage':'CPU harness model, corrected053','issue':'Harness failed to mask VRC7 PRG values to5bits; restore50/51 read out of range','resolution':'Final harnessv2 models bank mask; exact final6502 passes'}
    ],'production051_retained':True,'failed_emulator_execution_of052':False},ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자 요청 ‘오프닝 부분 적용해서 PoC’에 대응했다. **기준051은 유지하고, 053은 오프닝 전용 11px 시험판**이다. 원문 유지6건과 번역CSV는 변경하지 않았다.

구현: 오프닝root7의9문단만 Galmuri11 v2.40.4를EM12로 그려 한글 실획 높이11px·12×16셀로 변경했다. 폭192px/최대16문자·4행이며 기존 어휘를 보존한 줄바꿈이다. 문단별8×8 상하타일을 중복제거해128슬롯 안에 넣고, 같은8px열의 상하를 한 번에 PPU큐에 추가한다. 작업185의192타일 용량 문제는 문단별 중복제거로 해결했다. 가로 타이핑은8px열 단위다.

기존18/19를 복제한 전용PRG8/9와 오프닝 전용7호출부를 이용한다. 태그/복귀뱅크·플래그/스택을 보존하며 다른root/ID는 기존93E1을 사용한다. 기존 행간64·FE/FF·9행지우기를 이용했다. 공통IRQ/헤더/다른화면CHR는051과 같다. 오프닝 타이핑 시간은 열 수와 줄바꿈에 따라 달라지므로 기존과 동일한 시간은 보장하지 않는다.

변경 파일과 전체해시: [매니페스트](../manifests/nonplay186_assets.json). [ROM053](../build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes) SHA `{report['output_sha256']}` / [IPS](../build/opening11_poc_053/TinyToon2_Opening11_PoC053.ips) SHA `{report['IPS_sha256']}`. 원본SHA `{report['source_sha256']}`, CSV SHA `{report['CSV_sha256']}`, 폰트SHA `{report['font_sha256']}`. 051과24,223바이트 차이이며 선언범위 내다.

정적/빌드: 원본ExpectedWrite·중첩·전체diff/원본에서IPS실제적용/독립재빌드 동일 PASS. [배치와ASM](../build/opening11_poc_053/opening11_plan.json), [빌드 시점 기록](../build/opening11_poc_053/build_report.json). CPU: [최종6502검사](../qa/reports/opening11_cpu186.json)에서9문단525출력단위/1008상하타일 기록, 복귀18/19·스택·기존 제어 PASS. 실패는 [시행착오](../qa/reports/opening11_186_development_attempts.json)로 분리하고052·이전스크립트를 보존했다. 052는Mesen미실행이다.

작업186의 확정범위는 정적/빌드/CPU다. 실제Mesen의 출력도중·대기·지우기·3회반복·Start건너뛰기·재진입은 작업187로 분리한다. 고정build_report의runtime=PENDING은 작성시점 기록이며187의 확정보고가 이를 덮어쓰지 않고 보충한다. 전체게임11px화/전체플레이/전역PRG8도달성/사람의 최종폰트승인은 미실시다.

재현은 새 빈출력경로에 `python scripts/build_opening11_186_v2.py --output build/<new-directory>`를 사용하고 `python scripts/verify_opening11_cpu186_v2.py`로 검사한다. 기존053/독립재빌드/QA는 덮어쓰지 않는다.'''
    records.seal(186,'OPENING11_PAIRED_ROW_POC053_BUILD_186.md','오프닝 9문단 11px 전용 출력·빌드',body,'오프닝9문단053 삽입·독립ROM/IPS재빌드·최종6502 PASS. 기존051/번역CSV/다른화면 유지; 실제표시검증은187에서 분리.', '053의9문단 표시·지우기·3회반복·Start분기를 실제Mesen자료로 검증한다.',[
        Path(__file__),R/'scripts/build_opening11_186.py',R/'scripts/build_opening11_186_v2.py',R/'scripts/verify_opening11_cpu186.py',R/'scripts/verify_opening11_cpu186_v2.py',failure,proof,
        *[p for folder in ('build/opening11_poc_052','build/opening11_poc_053','build/opening11_186_rebuild053') for p in (R/folder).rglob('*') if p.is_file()],
        R/'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf',R/'workspace/fonts/galmuri11_candidate185/LICENSE.txt',R/'workspace/fonts/galmuri11_candidate185/font_source.json'
    ])

if __name__=='__main__':main()
