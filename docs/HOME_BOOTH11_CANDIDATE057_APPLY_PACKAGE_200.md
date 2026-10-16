# 작업200 — 홈·매표소11px057 개발 후보 패키지·Windows 실적용

[057 개발검토용 적용ZIP](../dist/TinyToonAdventures2_KR_HomeBooth11_Candidate057_20261009.zip) SHA `774803bb46713d1b12e7f9f381fdfd46539a2c63758224ceb4a3c59a2202f3b2`를 만들었다. [사용법](../dist/TinyToonAdventures2_KR_HomeBooth11_Candidate057_20261009/README_적용방법.txt), [정적 배치](../dist/TinyToonAdventures2_KR_HomeBooth11_Candidate057_20261009/review/review.html), [패키지 검사](../qa/reports/homebooth11_200_package.json). 원본 일본판에서057 전체 차분을 적용한다. ROM SHA `e2e388fe12d97c6a691e17174ba4cd368720788c140f3d60b4eccb70ef45ecef`. 원본·055·051·실패056·CSV·1편·사용자Mesen/세이브는 보존한다.

정적·CPU는 [199](HOME_BOOTH11_CANDIDATE057_TYPED_SKIP_CPU_199.md)의 정확한057에 연결한다. 패키지는 ROM 없이30파일, 폰트·xdelta 라이선스·12개 정적PNG·CPU·소비 배치·적용 도구를 포함한다. 실제 게임 캡처를 포함하지 않았으며057을 ‘CPU/빌드 검증 후 실제 실행 미수행’ 개발 후보로 표시했다. ROM 최종 채택/공개배포/전역11px/사람최종검수 성공으로 취급하지 않는다.

Windows8사례(정상/기존출력/원본=출력/동일크기 타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백 경로의 최종ZIP 추출본apply.cmd 적용이 byte-exact057 PASS. ZIP CRC·정확한 파일목록·전체payload·적용 후payload 불변·ROM-free PASS. 변경·해시는 [200매니페스트](../manifests/nonplay200_assets.json).

새 에뮬레이터·컨트롤러·플레이·실제장면/HTML 렌더 검증 없음. 057 홈/매표소의 실제 출력·대기·소거·선택·교환과2줄 즉시출력 NMI/IRQ 예산 검수가 남는다. 일반21개와 크레딧3개는8px다. HUD·정지 등 그림과 원문유지6건은 그대로다. 카페 완성 작업기/외부 게시 없음.

재현: 패키지 스크립트는 기존 경로를 덮어쓰지 않는다. 새 패키지명/QA 결과경로를 정한 복제에서 재현한다. 사용자 검토는 원본을apply.cmd에 넣고 새057을 초기화하여 홈·매표소 대사의 완성/건너뛰기/지우기/교환을 확인한다. 이를 이미 수행한 것으로 기록하지 않는다.

다음 작업 하나: 나머지21개 일반대사의 실제 창 기하·동적숫자·상단 공유글꼴 용량을 검사해 다음 확대 설계를 고정한다.
