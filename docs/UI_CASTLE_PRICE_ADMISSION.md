# 성 가격·입장 허가 — 031 / 작업31

성 입구의 일반 티켓 가격 안내와 입장 허가 문구를 한글로 삽입했다. 등록54개 원천 중27draft/27미번역이며 전체 게임 완료율은 아니다.

| 원천/별칭 | 초안 | 글꼴 |
|---|---|---|
| MAIN_05805 / slots1A,2C | 일반 티켓 {variable_FA}장으로 / 입장 가능해요 | 183/184 |
| MAIN_05824 / slot1C | 어서 들어오세요 | 185/186 |

FA는 원래 숫자 출력 제어코드 그대로다. 가격50을 한글 글꼴이나 본문에 고정 문자열로 넣지 않았다. compile_ui_variable.py는 원본 CPU9370의 두 자리 가격 표와 실제 reader 결과의 출력 순서를 연결하고 변수 토큰과 숫자 비트맵을 보존한다. 임의 글꼴 대체 없이 Galmuri7 PNG/TTF를 대조했다. 본문 raw 길이, FE/FF/FD, literal00, macro88의 위치, 두 별칭의 원본 pointer를 보존했다. 한글화 시 literal00의 위치에 문자가 놓인 초기 배치와 숫자 순서가 반대인 초기 모델을 정적 검사에서 차단하고 고쳤다. 8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19을 내보내기 전에 발견한 오류다.

029에서는 검사 건수를192로 적었으나 실제로는 문구마다48개 숫자·offset·ride 조합이었다. 별칭2C를 등록하는 과정에서 가격 문구 메타데이터도 중복했다. 030에서 건수를,031에서 별칭 중복을 고쳤다. 029/030/031의 8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19 바이트는 모두 같고 해당 빌드·재빌드·기존 QA를 보존했다. 공식 기록은 두 원천과 각48개 조합을 검증한031이다.

## 검증

[독립 검증](../qa/reports/variable031_validation.json): 원본 ExpectedWrites7/중첩0 및028 전체 이미지의 본문2개·폰트표3개·전용폰트·CHR확장 외 보존. 이전25개 초안·타이틀·도입부·helper008·macros·원본 숫자 불변. 두 문구 각각48개 입력 조합에서 native reader 호출별cycle/cursor와 숫자 출력이 같았다. 가격26호출2652cycles, 허가15호출1599cycles. [ABI1504/초기폰트720](../qa/reports/variable031_hooks1504.json), 재빌드 및 한글·공백 경로 실제 3c5a6b88e040064ab664b93bd6cefc030f580d974a05dd8012ef769100febf2a 적용이 같았다.

029 hash의 실제 실행 캡처와031이 전체 바이트 동일함을 입증해 사용했다. controller-only 부족 경로474장과 명시적인 RAM seed 골드4/일반50 각524장, 총1522장을028과 비교했다.192장은 현재 성 대사 행만 바뀌고1330장은 전체 픽셀이 같았다. 행 밖 픽셀 변화0, 보호 PPU/OAM/게임RAM 동일, 출력 버퍼 차이는 원래 reader replay로 제한했다. 입장 성공 후 성 상단 설명 카드와 게임 내부 화면으로 복귀한 상태도 같다. 성공 경로는 지정 RAM seed이며 자연 수집·완주의 근거가 아니다.

실제 IRQ/NMI/PPU/mapper299240개 시점(부족69714/골드121231/일반108295)이 정확히 같고 글꼴 선택값2764개만 달랐다. [실제 문구2개](../qa/dialogue/variable031_actual_pages.png)는 NT 완성을 확인한 가격2436/허가2124를 정수4배 확대하여 직접 검토했다. 실제029 성 카드2610/게임상태6000도 확인했다. 새 도입부 실행은 반복하지 않았다.

8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19458768바이트, CHR192KiB, 예약6KiB(bank170의1KiB 및187..191의5KiB). 상단 설명 카드·매표소 성공 인사15·출발2A·다른 게임 문구/그림·크레딧·전체 corpus, 전체 플레이/오디오/reset/savestate/실기/최종명칭·번역 검토 및 기존 PRG·난수 영향은 남는다. dist는 비어 있고 외부 게시도 없다.

## 해시·재현

- 원본 SHA256: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 031 8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19 / 동일029·030 / 재빌드 / 실제 적용 SHA256: `8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19`
- 031 3c5a6b88e040064ab664b93bd6cefc030f580d974a05dd8012ef769100febf2a SHA256: `3c5a6b88e040064ab664b93bd6cefc030f580d974a05dd8012ef769100febf2a`
- 979325a40d12762c62d27ec4a70edc33646ae780dedf2e787bbca4c498e67462 SHA256: `979325a40d12762c62d27ec4a70edc33646ae780dedf2e787bbca4c498e67462`

[자산·해시](../manifests/ui_gate_variable_assets.json), [세션 감사](../qa/reports/ui_gate_variable_session_20261005.json). 변경 파일은 prepare_ui_gate_variable.py, compile_ui_variable.py, build_ui_gate_variable.py, verify_ui_gate_variable.py, verify_ui_gate_variable_hooks.py, make_gate_variable_evidence.py, trace_branch_seed_irq_v1.lua 및 연결된 plan/backup/빌드/QA/문서다.

```powershell
python scripts/build_ui_gate_variable.py --output build/variable031_repro_next
python scripts/verify_ui_gate_variable_hooks.py --build build/dialogue_kr_poc_031 --report qa/reports/variable031_hooks_repro_next.json
python scripts/verify_ui_gate_variable.py
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_031/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/variable031_gold4_repro_next --frames 6000 --inputs config/menu_castle_001.json --seed config/gate_gold4_seed_001.json
```

고정 빌더/검증은 당시27draft SSOT와 명시한 빌드에 적용한다. 다음 행동 하나: 관측한 매표소 교환 완료 인사15와 놀이기구 출발2A를 한글 삽입·검증한다. 바로 이어간다.
