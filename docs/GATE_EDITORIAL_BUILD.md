# 작업90 — 원문 문맥 검토와 성 입구 문장 수정

등록54원천과33그림 문구를 원문/변수/매크로/명칭/크레딧 유지 관점에서 수동 대조했다. [항목별 검토 기록](../workspace/review/editorial090/source_context_review.json). 사람의 최종 검토 승인과는 구분한다. 자동 규칙 기반 일괄 문구 변경은 하지 않았다. 기차 설명의 내부3공백은 native macro폭을 유지하기 위한 것이므로 제거하지 않았고, 동적 FA/F8/F9와 공유macro 원천·크레딧 영문 이름·법적 표시는 보존했다. HUD 금티켓과 본문 골드 티켓은 짧은 HUD 폭의 표기 차이로 기록했다.

한 문장의 어색한 조건절을 수동 수정했다. MAIN_057C1 원문은 ‘골드 티켓4장이 있으면 들어갈 수 있다’는 의미다. 이전 ‘입장 조건은 골드 티켓4장 / 있으면 입장할 수 있어요’를 **골드 티켓4장이 있으면 / 입장할 수 있어요**로 다듬었다. 정확한 공백과 줄바꿈은 [새 계획](../workspace/translation/gate_editorial_plan_001.json) 및 CSV에 보존했다. [기존CSV백업](../backups/translation/text_ja_before_gate_editorial_001.csv), 과거 모든 ROM/검토ZIP 유지. 변경 필드는 이 한 항목의 translation_ko와 notes뿐이며 나머지53항목 원문/초안/상태는 그대로다.

후보047: ROM499728바이트/SHA-25682ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10. IPS SHA-2563709578b0b4a211588ee254943dbd639643e82b39af07a295cacc6979aa20f70. CSV SHA-256ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556.45draft/9기술공유 상태 유지.

정적/빌드: [빌더](../scripts/build_gate_editorial.py), [빌드 보고서](../build/dialogue_kr_poc_047/build_report.json), [독립 검증 보고서](../qa/reports/gate090_validation.json). 기존046 대비129바이트가 한 문장36바이트 및 그 전용폰트175/176의2KiB 안에서만 바뀌었다. 추가 뱅크/헤더/CPU코드/매퍼 표는 바꾸지 않았다. Galmuri7 atlas/TTF와 native 숫자4를 확인했다. 제어/매크로/원래00 위치,39회 reader의 call별 cycles/cursor,960개 page setup ABI와 IRQ 쓰기시점은046과 같다. 원본부터9개 Expected Writes/원본 바이트/비중첩/전체 출력도 검증했다.

독립재빌드8파일 byte exact, 한국어·공백 경로에서 실제 Windows Python IPS CLI 적용도 후보047과 byte exact다. 이 적용은 아직 새 xdelta/apply.cmd 배포 묶음 검증이 아니다.

에뮬레이터/직접 장면: 아직미수행. 채택본은046이며047은 후보로만 보존한다. 번역CSV는 새후보의 문장을 담으므로046·과거검토자료의 번역은 각build translation_used/동결자료에서 읽는다. 자연전체완주·전역corpus·실기·PCM청음·최종사람검토는 남는다. 공개게시/카페완성작업기 없음.

재현: `python scripts/build_gate_editorial.py --output build/새폴더`; IPS는 `python scripts/dialogue_ips.py apply --source "일본판 원본.nes" --patch build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.ips --output "새 결과.nes"`. [동결 파일/SHA](../manifests/gate090_assets.json).

다음 작업 하나:046/047의 실제 성 입구 대사를 같은controller로 실행해 출력 도중·완성·넘김·다음 대사와 폰트 수명/원문 조건절 및 다른화면 보존을 검증한다.
