# 작업206 — 일반대사11px059 개발 후보 패키지·Windows 실적용

[059 개발검토용 적용ZIP](../dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009.zip) SHA `53dde1ae35286b498d5e3f578ab80e39b0f55d9810e11faacfbfe7ddc5f8888d`를 만들었다. [사용법](../dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009/README_적용방법.txt), [정적 배치와 카드 모형](../dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009/review/review.html), [패키지 검사](../qa/reports/ordinary11_206_package.json). 원본 일본판에서059 전체 차분을 적용한다. ROM SHA `8b44d79b19c490dc6c5e2f3dcf73d08d1716ab981b62878067043a5600f59930`. 원본·055·051·057·실패056/058·CSV·1편·사용자Mesen/세이브는 보존한다.

정적·CPU는 [204](ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md)의 정확한059에 연결한다. 패키지는 ROM 없이56파일, 폰트·xdelta 라이선스·33개 정적문자PNG·5개 상단창 모형·CPU·소비 배치·적용 도구를 포함한다. 실제 게임 캡처를 포함하지 않았으며059을 ‘CPU/빌드 검증 후 실제 실행 미수행’ 개발 후보로 표시했다. ROM 최종 채택/공개배포/전역11px/사람최종검수 성공으로 취급하지 않는다.

Windows8사례(정상/기존출력/원본=출력/동일크기 타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백 경로의 최종ZIP 추출본apply.cmd 적용이 byte-exact059 PASS. ZIP CRC·정확한 파일목록·전체payload·적용 후payload 불변·ROM-free PASS. 변경·해시는 [206매니페스트](../manifests/nonplay206_assets.json).

새 에뮬레이터·컨트롤러·플레이·실제장면/HTML 렌더 검증 없음. 059 실제 출력·대기·소거·선택·교환·상단창 테두리/동시거주·CHR256 매핑·NMI/IRQ 예산 검수가 남는다. 크레딧3개는8px다. HUD·정지 등 그림과 원문유지6건은 그대로다. 카페 완성 작업기/외부 게시 없음.

재현: 패키지 스크립트는 기존 경로를 덮어쓰지 않는다. 새 패키지명/QA 결과경로를 정한 복제에서 재현한다. 사용자 검토는 원본을apply.cmd에 넣고 새059을 초기화하여 홈·매표소 대사의 완성/건너뛰기/지우기/교환을 확인한다. 이를 이미 수행한 것으로 기록하지 않는다.

다음 작업 하나: 197~206 고정근거와 원본/링크를 감사하고 최신059 후보와 남은 크레딧을 정본 인계에 반영한다.
