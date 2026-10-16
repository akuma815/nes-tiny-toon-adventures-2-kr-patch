# 작업106 — 일반 티켓3 부족 분기 검증과 종료 인계

2026-10-05 사용자가 “여기까지 마무리 하자”라고 지시했다. 이미 시작한 비교본046과 현재047의 실행이 끝난 결과만 정리했다. **작업106까지 종료하며 재개 지시 전에는 자동으로 작업하지 않는다.** 새 에뮬레이터 실행이나 CPU 재검증을 시작하지 않았다. 이전 우선순위 질문은 미응답 상태로 보류하며 선택이나 승인으로 해석하지 않는다.

현재 채택본은 **dialogue_kr_poc_047**이다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`. 원본·1편·047 ROM/CSV·과거 성공 및 실패 자료를 보존했다. 새 ROM, 번역 수정, 패치 생성은 없다.

## 완료 결과와 증거

동일 입력으로046/047을 각각4200프레임 실행했다. 초기1000프레임에 일반 티켓 `07D0=3`, 나머지 `07D1=0`, `07D2=0`만 설정한 통제 실험이다. 이후에는 controller 입력을 사용했다. 자연 플레이로 티켓3장을 얻었다는 뜻이 아니다. 양쪽 실행 exit0이며, 저장된 환경원장의 각1821파일을 실제SHA와 다시 대조했다. 공통1820파일과302개 전체PNG가 byte exact다. stdout.txt만 다르며, 두 ROM의 File/PRG/PRG+CHR CRC32 세 줄 차이로 확인했다. 나머지 로그 줄은 같다.

| 실제047 프레임 | 표시 원천 / native slot | 확인한 표시 |
|---|---|---|
| [1800](../qa/dialogue/context106_normal3047/frame_01800.png) | MAIN_05833 / 1D | 요금은 티켓 4장 / 티켓을 내줘! |
| [2100](../qa/dialogue/context106_normal3047/frame_02100.png) | MAIN_0590C / 29 | 아쉽지만 / 티켓을 더 모아줘! |
| [2700](../qa/dialogue/context106_normal3047/frame_02700.png) | MAIN_05929 / 2B | 지금 3장의 / 티켓을 갖고 있어 |

위 세 장면을 assistant가 직접 확인했다. PPU22A8/22E8의 실제 코드열을 기존196글리프 표로 해석하고 예상 문자와 공백까지 대조했다. 실제PPU 글꼴2KiB는 현재047 ROM의 font196과 같았다. FA 요금은 두 자리 `blank,4`, F8 보유량은 세 자리 `blank,blank,3`으로 출력되어 자연스러운 간격을 만든다. 기술적 leading blank를 오탈자로 취급하지 않는다. 세 장면과 마지막4200프레임의 티켓값은3 그대로다. 마지막은 보유량 대사이며 입장 성공·홈 복귀·게임 완료를 주장하지 않는다.

RAM06CF는 문단을 읽은 뒤 다음 번호로 증가한다. 2100의 값2A만 보고 “출발!”이 표시됐다고 해석하면 틀리며 실제 출력은 거절29다. 성공 시작2A의 정확한 문맥은 [작업105 원장](../workspace/translation/scene_context_105.json)을 따른다. MAIN057AC=매표소15와 MAIN05920=놀이기구2A 정정은 보충 원장에만 있으며 동결CSV를 변경하지 않았다.

## 검증 구분과 재현

- 정적/보존: 원본·046·047·CSV SHA, 양쪽 캡처 전 파일, Mesen 실행파일/Lua/설정/입력/seed SHA를 검증했다. 기존 glyph JSON과 실제PPU/NT를 대조했다.
- 빌드/적용: 이번에는 새 빌드·패치 적용을 하지 않았다. [기존047 패키지](REVIEW_PACKAGE_047.md) 검증은 당시 기록으로 보존한다.
- 실행: 이미 시작한 초기 티켓 seed 실험 두 회를 완료했다. controller-only 자연 플레이나 전게임 완주가 아니다.
- 직접 장면: 위 실제047 PNG3장을 확인했다. 독립RGB raster 재구성, 최종 사람 승인, 실기, PCM 청음은 수행하지 않았다.

[읽기 전용 정리기v2](../scripts/close_context106_v2.py), [검증 보고서](../qa/reports/context106_closeout.json), [동결 manifest](../manifests/context106_assets.json). v1은 PowerShell 파이프 인코딩 때문에 예상 한글 리터럴이 물음표로 바뀌어 문자열 guard에서 실패했다. 실제NT 해석은 정상이었고 ROM/CSV/캡처 변경은 없었다. [실패 관찰](../qa/reports/context106_v1_observation.json)과 [v1](../scripts/close_context106.py)을 보존하고 UTF8 v2로 해결했다.

완료한 실행의 재현 명령은 아래와 같다. **사용자 재개 지시 후 새 출력 폴더를 지정할 때만 실행한다.** 기존 QA/보고서 경로는 덮어쓰지 않는다. 정리기는 기존 보고서가 있으면 실행을 거부한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/context106_normal3046 --frames 4200 --inputs config/menu_coaster_001.json --seed config/ride_normal3_seed_001.json
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/context106_normal3047 --frames 4200 --inputs config/menu_coaster_001.json --seed config/ride_normal3_seed_001.json
python scripts/close_context106_v2.py
```

Mesen2.1.1 SHA `d2eb03c2590c648bf329f127ebcfefd70130e7690a9e2ccdba8616faea1fe96b`; private 설정 SHA `cee81286ae23bd0b4fa417a9429b63dcf645ce2bdd122db5aa1d572990803621`. 기존 사용자 에뮬레이터 설정은 변경하지 않았다. 캡처환경 원장에 실행명령·입력·seed·사용Lua와 파일별 해시가 있다. manifest는 이 문서, 정리기 두 버전, 실패/통과 보고서, 두 캡처 폴더, 입력/seed와 기존 glyph 표를 동결한다. 최신 README/조사/계획/날짜 인계/journal/HANDOFF를 종료 상태로 갱신했다.

## 남은 일과 공개 작업기

등록54원천은45번역초안+9기술공유다. 최종 문체·명칭·그림 사람검토, HOWTO/PAUSE/POW의 남은 소비 경로, 전역corpus, 자연 전체3구간 완주, 실기/청음/정식배포는 미완료다. [본문/그림047 검토](TRANSLATION_REVIEW_047.md), [그림 후보 보충자료](../workspace/review/consumer047_104_20261005/review.html)를 유지한다. 합성JSON 다운로드 검사는 사람 의견이나 승인이 아니다.

네이버 카페 완성 작업기는 모든 작업이 끝난 뒤 작성한다는 최초 요청을 유지한다. 현재는 [근거 journal](journal/2026-10-05.md)만 보존했고 완성 작업기나 외부 게시를 하지 않았다.

다음 작업 하나: **사용자가 재개를 지시한 뒤 현재047 놀이기구 성공입장 후 slot2A “출발!”의 실제 표시를 문맥원장과 대조한다. 지금은 실행하지 않는다.**
