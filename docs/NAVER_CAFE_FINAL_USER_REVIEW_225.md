# 작업225 — 사용자1차 검수 완료 반영 카페 작업기

사용자062 실제 화면·완주1차 검수 완료 보고를 공개 본문·선두 안내·검증표·이미지08·업로드안내에 반영했다. 배포 이후 추가 검증 예정은 유지했다. [최종 작업기 ZIP](../dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip) SHA `32ac4f3938ea0659216e1fae61a6ad6463ed2091c8470a0af5db360a686e1e9c`,13파일/8PNG/ROM없음. [오프라인 HTML](../workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009/작업기.html), [카페 복사용 본문](../workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009/카페_복사용_본문.txt).

이미지01/03/04/05/06은 과거 빌드의 실제 캡처,02는 제작 원천,07은062 정적 복원,08은 설명 표다. 새 완주 캡처를 만든 것으로 표기하지 않는다. 사용자 완료 보고는 [224 영수증](../qa/reports/user_review224.json)과 연결하고 이전221 당시 미기록 상태는 역사 근거로 유지한다. 공개 글은 사용자가 올릴 작업기 어조로1차 검수 완료를 썼다. 등록45문단을 전게임100%로 확대하지 않았고 원문 유지6원천도 명시했다.

UTF8·8마커 순서·내장PNG바이트·CRC·13파일 정확payload/ROM-free 통과. 격리 headless Edge 1280×1000 및390×844: 이미지8개 디코딩, 가로 넘침 없음, 확대/Escape 통과. 수정된08그림 및PC/모바일 선두 렌더를 직접 확인했다. [최종 검증](../qa/reports/publication225_verified.json), [렌더](../qa/publication/render225_final/render_report.json), [원천](../qa/reports/publication225_sources.json). 네이버카페 실제 게시나 배포 이후 게임 검증은 수행하지 않았다.

재현: python -B scripts/publication225_review_update.py, render_publication221.py --input <새HTML> --output <새QA경로>, seal_publication225.py. 고정 출력은 덮어쓰지 않으므로 새 경로를 지정한 복제에서 실행한다. 기존003 공개 원천은 이 갱신의 재현 입력으로 유지한다. 게임ROM과CSV는 수정하지 않았다.

다음 작업 하나: 최종 배포 파일명을 명확히 정리하고 임시 적용 사본·렌더 캐시를 삭제한 뒤 최종 인계를 갱신한다.
