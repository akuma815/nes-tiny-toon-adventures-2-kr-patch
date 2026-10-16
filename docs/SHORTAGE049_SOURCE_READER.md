# 작업150 — 수정된 부족 문구 실제읽기·폰트 수명

[검증](../qa/reports/shortagereader150_validation.json), [직접 화면](../qa/reports/shortagereader150_visual.json), [실행 계획](../work/shortagereader150/run_plan.json), [실행](../scripts/run_shortage_reader150.py), [검증 코드](../scripts/verify_shortage_reader150.py).

일반티켓3장 초기seed의 동일입력 경로에서 새047/현재049 각각4200프레임을 실행했다. 원본·ROM·CSV는 수정하지 않았다. 동결141관측기를 사용해 이전129에 없던 실제 물리PRG 읽기를 추가했다. 새로운047/049의 각1812개 snapshot 산출물(RAM/PPU/OAM/mapping/state/RGB)은 각각 역사106/129와 완전히 같다. 동결129 보고서의SHA 및 환경에 선언된 모든파일을 확인했다. 따라서 기존129의 보호영역·RNG차이·지우기 결론을 같은 실행값에 연결할 수 있다.

PRG 읽기190건씩의 주소·PC·순서·프레임·포인터·nativeID는 같다. 각값은 해당 ROM의 바이트와 직접 대조했다. 의도된 바이트차이10건은 MAIN0590C만이며 다른 원천값은 보호했다. 폰트 차이41건은 native29 또는 다음2B의clear 중196→226만이다. 실제읽기PC의 B1 06 및 물리offset→unit 귀속을 확인했다. MAIN0590C/MAIN05929/MACRO061FA 각각 원천 전체바이트를 읽었다. cycle차134건0/41건38/15건76은 보존하며 전역CPU/IRQ/RNG 동일성을 주장하지 않는다.

현재ROM의20바이트 body 및 native-reader 확장10/11타일은126/049 mapping과 같다. 실제NT22A8/22E8의 모든줄과 활성226을 연결했다. 2416 actualCHR조각이 현재ROM과 같고 font226/227 공급을 확인했다.302PNG 중261전체일치/41개의 의도한 둘째줄만 차이가 있다.2004폰트196(이전요금clear),2100·2604폰트226(부족 완성/다음clear),2700폰트196(보유안내)과티켓3장유지를 확인했다.5개실제PNG에서 이전요금·출력중·완성·clear·다음보유안내를 직접 검토했다.

변경: run/verify/seal_shortage_reader150.py, work/shortagereader150 계획/log, 새047/049QA, 검증/시각보고서, 상세·datedhandoff·journal·README·SURVEY·PLAN·HANDOFF·manifest/audit. SHA: ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`, 동결129보고서 `553b16b4d7e442cf2781f997dcda7dc1df25b09bd90ac3da8d1253ac40c80ea0`. 기존역사·원본·1편 보존.

재현: `python scripts/run_shortage_reader150.py`, `python scripts/verify_shortage_reader150.py` (기존출력거부, 새ID/경로필요). 정적/동결SHA·명시seedruntime·actualreader/CHR/전줄NT·과거snapshot·보호RGB·직접5PNG PASS. 신규build/apply/reset/state/실기/청음 없음. 자연획득·자연전체완주·global corpus·HOWTO/PAUSE/POW 소비·사람최종·정식배포 미완료. 카페 완성기사·외부게시 없음.

다음 작업 하나: 145 이후의 실제 reader 보고서146/147/149/150을 등록 원천별로 합쳐 누락과 서로 다른 검증 범위를 재평가하고, 남은 작업을 실제 결함 또는 새 소비경로 근거에 따라 선택한다.
