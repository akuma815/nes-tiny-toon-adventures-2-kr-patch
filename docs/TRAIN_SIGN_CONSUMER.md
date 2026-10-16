# 기차 간판 실제 소비와 PNG 추출 — 작업50

이번 작업에서 원본·042 ROM·IPS·번역 CSV는 유지했다. 기차의 실제 간판을 원본 타일·네임테이블·팔레트·화면 RGB와 연결해 [PNG](../extracted/graphics/train_sign_001/source_label_4x.png)로 추출했다. [소비 명세·해시](../extracted/graphics/train_sign_001/consumer.json), [검증 코드](../scripts/survey_train_sign.py), [실제 확대 화면](../work/train_engine_002/source14700_actual_4x.png)을 보존했다.

## 원문과 한글 초안

실제 표기는 **MONTY'S / 큰 M 문양 / LAND R.R.**다. 작업47·49의 정적 목록에서 MONTANA LAND로 읽었던 것은 후보 해석이었으며 실제 화면으로 정정한다. 가운데는 큰 장식 M이다. 별도 문양으로 보존한다. 번역 초안은 **몬타나의 / M 문양 유지 / 랜드 철도**다. Monty의 별칭은 프로젝트의 몬타나 명칭으로 통일했고 R.R.는 기차의 철도 표기로 풀었다. 최종 사람 문구 검토는 남아 있다.

원래 글자 영역은40×8/24×8/16×8이며 NT22C2/22C9/22CC의5/3/2셀, 코드2D..31·34..36·67..68이다. 글자는 index1, 검정 바탕은 index2다. 총640픽셀과 전체128×16 추출 영역2,048픽셀이 실제 RGB와 정확히 같다. 큰 M의32/33·3A..3D, 아래 행과 테두리는 편집 범위에서 제외한다.

## 실제 경로와 시각

앞선 두 컨트롤러 경로는 체력 소진으로 간판 전에 지도에 돌아왔다. 이번에는 **체력 보충을 명시한 진단 경로**를 사용했다. 정상 최대 체력3을 RAM07C0에만 썼으며 root4/phase5/course2/55=0 조건일 때만 적용했다. 2800..17840을120프레임 간격으로 검사한126회 중126회 보충했고 실제로 값이 바뀐 것은24회다. 매 쓰기마다 전체 RAM의 다른 주소가 그대로임을 검사하고 PC·cycle·이전/이후값·조건을 기록했다. 위치·시간·phase·PC·ROM·save state를 바꾸지 않았다. **자연 플레이나 클리어 검증은 아니다.** [실행 환경](../qa/dialogue/world042_train_life3/environment.json), [매 보충 기록](../qa/dialogue/world042_train_life3/life_seed_writes.csv), [입력](../config/world_train_controller_003.json), [진단 정의](../config/train_life3_diagnostic_001.json).

18,000프레임 실행에서 IRQ5의 FBE3→FBEE/FBF7→FC1C가 실제72..75 뱅크를15,252회 선택했다. 중간 IRQ의4KiB508표본은 원본32010..33010과 전체 바이트가 같다. active 확장 ROM의 IRQ 즉시값 위치는3FBFF/3FC08이며 현재72/74다.

14700 PNG는 직전14699 IRQ의 scroll C3에 대응한다. 당시 scan128·fineY2와 horizontal scroll195를 근거로 NT 좌표를 x+61/y−2에 표시한다. 현재14700의 scroll C4를 사용하면 한 픽셀 틀리므로 이전 실제 IRQ를 사용했다. 임의 허용 오차가 아니라 정확한 이전 기록과 전체 RGB 대조다. 14700의 NT 글자 순서와 팔레트도 검사했다. 14550/14700/14850/15000 등 실제 접근 화면과 추출 PNG를 직접 검토했다. [접근 실제 화면 묶음](../work/train_engine_002/actual_engine_approach.png)은 실제 PNG를 배열한 자료이며 정적 임의 색 분석도와 구분한다.

## 재현·검증·한계

`run_world_life_seed_qa.py --rom build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes --output <새QA경로> --frames 18000 --inputs config/world_train_controller_003.json --script scripts/trace_world_life_seed_v1.lua --seed config/train_life3_diagnostic_001.json`. 공식 Mesen API로 이미 사용하던 RAM write를 제한한 진단이며 모든 입력과 실행 파일·결과 해시는 environment에 있다. `survey_train_sign.py`는 최초 추출 경로 전용으로 덮어쓰기를 거절한다. 재현은 새 경로를 지정하는 복제본을 별도로 기록한다.

원본 SHA256 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d, 042 SHA256 f4b4aa288e03bb30fd9532d95f823e34c4c620b20438feb2e1de0f67845cfc7b, IPS ebd250d9f9750a52f8720850c78cc13a86506e866e3fe834106bf42364221ef8. [작업 자산](../manifests/train_sign_source_assets.json), [이번 조사 보존 감사](../qa/reports/train_sign050_session.json).

정적 원문/타일·native IRQ/NT·진단 실행·실제 RGB·직접 장면 검토까지 완료했다. 새 한글 ROM 빌드·CPU 시점·패치 적용·회귀는 아직 하지 않았다. PAUSE120/121과 HOW TO CONTROL의 관측 밖 소비, 전체 corpus/자연 플레이/오디오/실기/최종 사람 검토는 남아 있다. 기존 타이틀 PUSH START·법적 표시와 크레딧 영어 이름의 유지 결정을 계승한다.

다음 작업 하나: **72..75를 전용216..219로 복제하고 Galmuri7로 세 영역만 편집한 뒤 IRQ5 두 즉시값을 바꾸는 043을 빌드·검증한다.** 큰 M·테두리·세계 그림·플레이 상태·기존 한글 영역·IRQ/NMI 시점을 보호한다. 계속한다.
