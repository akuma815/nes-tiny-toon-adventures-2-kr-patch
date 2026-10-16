# 작업173 — 보존6건 확정·검토/실제적용 반영

사용자가 남은 RYO51·NT1C·진단 STAGE SELECT도 **‘이번 범위에서는 원문 유지’**로 답했다. [173 원본 결정](../workspace/translation/scope_decisions_20261008_173.json)에 질문·답변·현재ROM/CSV·172근거SHA와 세 원천ID를 기록했다.169의 HOWTO·PAUSE·POW 결정은 그대로 보존했다. [새 원장](../workspace/translation/nonplay_inventory049_173.json)은 명시적 사용자 보존6건과 기존 타이틀 PUSH START 소비연결1건을 구분한다. 발견7건의 추가 번역 범위 미결정은0이다. 소비 미연결6건의 기술 상태와 전역 원천 목록 완결성·최종 문구/명칭/그림/플레이/배포 승인 미완료는 유지한다. 미사용 증명이나 전역 영어 보존 정책으로 확대하지 않는다.

[검토HTML](../workspace/review/nonplay049_20261008_173/review.html)과10파일 검토ZIP은 원본 결정169/173 두 파일과 읽기용 합본을 포함한다.54원천의 번역/상태/토큰/원천SHA,33그림 및25내장PNG(기존실제21/정적4)의 바이트SHA가 기존 원천과 일치했다. PC1280/모바일390의 검색·상세열기·크레딧3건·이미지 로드·너비 검사 PASS. 모바일NT1C 결정 카드를 직접 보았다. 실제게임 PNG는 이전 증거 재사용이며 신규 게임 장면이 아니다.

[새 적용ZIP](../dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008.zip)은23파일 ROM 없는 개발 검토 패키지다. 기존171을 보존했고 패치·apply.cmd/ps1·xdelta3·도구/글꼴 라이선스는171과 바이트 동일하다. 검수안내/알려진한계/적용안내/릴리스보고를6건 결정으로 동기화했다. [최종검증](../qa/reports/nonplay173_final.json): CRC/내용/SHA22항목 검증 후 최종ZIP을 새 한글·공백 경로에 풀어 실제 Windows apply.cmd를 실행했다. exit0이며 결과499728바이트 전체가 현재049와 일치했다. 원본/ROM/CSV/패치/도구/ZIP 불변이다. 같은 도구의132 오류8사례는 기존 근거를 재사용했다.

이번 검증은 정적 기록·문서 브라우저·압축/해시 및 실제 Windows 적용이다. 신규ROM빌드/CPU실험/에뮬레이터/플레이/PCM청음/사람 최종검수 없음. 실제 플레이는 사용자 담당이다.38cycles/page의 idle RNG/CPU/IRQ 차이,163 frame04410 PNG7326픽셀 차이와 원인 미확정, 모든 분기/상태/실기/PCM 및 최종 문구/그림 승인은 남는다. 카페 완성 작업기는 전체 작업 완료 후이며 외부 게시 없음.

ZIP SHA `55a4785270b52ead8e5bbc4b62b9584a5dd23da4c58e823f16bdac09d87f2acb`, 현재ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 변경:173 결정·원장·검토10파일/ZIP·적용23파일/ZIP/해시·생성/렌더/검증스크립트·렌더PNG/보고·실제적용QA·인계/계획/조사/journal/canonical·manifest/audit. 재현: `python scripts/make_closed_scope173.py`; `python scripts/render_scope173.py --input workspace/review/nonplay049_20261008_173/review.html --output qa/review/nonplay049_173_render`; `python scripts/package_scope173.py`; `python scripts/verify_seal_scope173.py`; `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay173_assets.json --output qa/reports/nonplay173_session.json`. 출력보호가 있으므로 재실행은 별도 경로에서 한다. 파일별SHA는manifest다. 감사는 프로젝트 내부 링크/원본/기존 고정증거를 엄격히 검사하고 역사3.3외부캐시 링크1개 소실은 별도 표시한다.

다음 작업 하나: 보존된162/163 종료 자료만 사용해 frame04410 PNG 차이의 캡처 출처를 오프라인 대조하고, 확인 가능한 원인과 확인 불가한 한계를 구분한다.
