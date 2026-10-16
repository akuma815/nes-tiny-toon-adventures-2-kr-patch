# 작업169 — 보존 범위 확정·PUSH START 타이틀 소비 연결

사용자가 후보 HOWTO·PAUSE·POW 범위 질문에 **‘이번 범위에서는 원문 유지’**라고 답했다. [명시적 결정 원장](../workspace/translation/scope_decisions_20261007_169.json)에 세 후보의 현재 한글화 범위 원문 유지만 승인으로 기록했다. 이세건의 범위 작업은 닫고, 미사용 증명·소비 폐쇄·전역 영어 보존·전체 사람 검수는 승인으로 처리하지 않는다. 원본 픽셀을 이미 보존했으므로 ROM을 새로 고칠 필요가 없다.

추가 기술 진전: CHR0F PUSH START는 별도 미연결 문구가 아니라 현재 타이틀의 기존 보존 시작 안내였다. native CC89/CC8B→RAM37=63, CCAE/CCB0→actor8E, bank36/9643 descriptorA19C의8개8x16 sprite41..4F 경로를 연결했다. 원본/현재049의5course CPU조건쌍에서 OAM/레지스터/cycle이 동일했다. 기존 [049 타이틀130 PNG](../qa/dialogue/pages130_intro049/frame_00720.png) 및 종료된QA의RAM/PPU/OAM/mapping/환경SHA를 확인했다. frame720에서 bank63→PPU1400의1024바이트와8개 OAM(y156,x96..152,attr2)을 확인했다. 기존 실제 PNG를 직접 열어 PUSH START 표시를 확인했으며 새게임 실행은 하지 않았다. 기존 타이틀 POC의 PUSH START 보존 범위와 연결하고 신규 번역 건으로 중복 집계하지 않는다.

RYO51 포함 CHR17 마지막 행은 bank95 local48..63이다. 타이틀 숫자2의 actor31은local0..21만 사용하며 지정된720 OAM도 동일하다. 해당타이틀 조건에서 서명행을 사용하지 않는다는 제한된 근거다. 전역 미사용/서명 작성자를 확정하지 않는다. 나머지 미해결은 RYO51, NT1C, 진단STAGE SELECT의3건이다. [현재 원장](../workspace/translation/nonplay_inventory049_169.json)은 발견7=사용자보존3+기존타이틀연결보존1+미해결3으로 정리했다. 전역원천완결성과전체사람검수는false.

[검증 보고](../qa/reports/nonplay169_scope_title_consumer.json), 재현 `python scripts/resolve_scope169.py`는기존출력을보호한다. 신규정적/한정CPU와기존완료QA해시·PPU/OAM·PNG 직접확인만수행했다. 신규ROM빌드/적용/게임런타임/플레이/청음없음. ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 변경은결정원장/현재inventory/분석기/보고/인계문서/manifest이며사용근거SHA를고정한다. 실제플레이검수는사용자담당이다.

다음 작업 하나: 사용자 원문 유지 결정과 타이틀 소비 연결을 비플레이 검토자료·검수용 적용 패키지의 새 버전에 반영하고 현재 상태를 인계한다.
