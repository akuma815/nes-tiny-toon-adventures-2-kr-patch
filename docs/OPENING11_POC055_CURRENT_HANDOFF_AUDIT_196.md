# 작업196 — 요청6문단 수정055 패키지·근거·최신 인계 감사

사용자 요청인 6문단 줄바꿈과 서명 오른쪽 정렬을 반영한 **055**를 최신 오프닝 검토본으로 정리했다. [실제 수정 화면](../workspace/review/opening11_194/page06_11px.png), [053/055 비교](../workspace/review/opening11_194/review.html), [ROM 없는 적용 ZIP](../dist/TinyToonAdventures2_KR_Opening11_PoC055_Layout6_20261009.zip).

6문단은 `친구들도 데려와!` / `깜짝 놀랄 거다!` / 빈 줄 / 오른쪽 정렬 `의문의 대부호로부터`로 배치했다. Galmuri11 글자 모양은 유지했다. 원문·번역 CSV는 바꾸지 않았다. 053 대비 변경은 해당 문단의 전용 문자열·글꼴에 속한 508바이트이며 다른 8문단과 코드가 동일하다. 홈054는 CPU 검증 후보로 보존하며 055에 포함하지 않았다.

정적·빌드·CPU: [193](OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md)의 독립 ROM/IPS 재빌드와 9문단 최종6502 검증 PASS. 이번196에서는188~195의 고정 매니페스트를 전부 대조했다. [무결성 보고](../qa/reports/opening11_196_integrity.json), [변경 파일/해시 목록](../manifests/nonplay196_assets.json).

실제 에뮬레이터·장면: [194](OPENING11_PAGE6_LAYOUT_POC055_RUNTIME_194.md)의 새055 오프닝9000프레임에서9문단 각3회, 출력·대기·지우기2167 RGB표본과3024 상하타일 소비·30회 소거 PASS. 같은 프레임의053/055 비교2318쌍 중2086 전체PNG 동일,232는6문단 글자 영역 안에서만 달라졌다. 실제6문단 PNG를 직접 확인했다. 이 보고196의 새 에뮬레이터 실행은 없다.

패키지·적용: [195](OPENING11_PAGE6_LAYOUT_POC055_PACKAGE_195.md)의38파일 ROM 없는 ZIP, 실제Windows 적용8사례·최종ZIP 추출 후 적용 byte-exact PASS. ROM SHA `8346499ca4240ffad350e3977f792735563779b8c749744a8d9b413ea0b44086`, ZIP SHA `e160baa0a63a0d9d4b72836837b179c942122401d2dbecae7481e89a2fafd46b`. [195 감사](../qa/reports/opening11_195_audit.json)는46개 고정 파일·2573 유효 링크·원본/1편 보존 PASS. 과거 외부3.3 스킬 캐시 링크1건 만료는 별도 보고했으며 프로젝트 로컬 누락 링크는 없다.

기준 개발본051, 이전053/054, 원본, CSV, 1편, 기존 검증 자료, 사용자Mesen 설정·세이브를 보존했다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 사용자 결정대로 원문 유지다. README·최신 HANDOFF·작업 계획의 재개 위치를055로 갱신하고 오늘 인계/journal을 추가했다.

제한: 전체 텍스트11px 전환·최종 사람의 글꼴/문체 승인·전체 플레이·오디오/하드웨어/저장 호환·전역 도달성은 미완료다. 055 Start/기차 검증은 새로 실행하지 않았고053 기록을055 결과로 간주하지 않는다. 홈054 실제 실행과 HTML 브라우저 렌더 QA는 미수행이다. 카페 완성 작업기 및 외부 게시도 아직 진행하지 않았다.

재현: `python scripts/audit_project_links184.py --manifest manifests/nonplay196_assets.json --output qa/reports/<new-audit-name>.json`. 기존 고정 보고를 덮어쓰지 않는다. 재개 기준은 아래 최신 HANDOFF를 따른다.

다음 작업 하나: 055를 기준으로 홈 대표 한 줄의 11px 후보를 재구성하고, 실제 소비 경로와 연결해 검증한다.
