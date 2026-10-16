# 작업119 — 미연결 NT1C와 화면 후보의 경계

[분석기](../scripts/analyze_nt_candidate119.py), [결과](../qa/reports/candidate119_NT1C.json), [기존 NT 공급 조사](NT_SELECTOR_SUPPLIER_BOUNDS.md), [후보 검토 자료](CONSUMER_REVIEW_047_SUPPLEMENT.md).

기존 HOWTO·PAUSE 공급 조사99..103은 이미 직접 상수·등록 player/action 표·IRQ latch의 지정 범위를 확인했다. 같은 부재 관측을 반복해 전역 미사용으로 바꾸지 않았다. 기차 간판은 이미 별도 소비·번역 근거가 있으므로 원본 정적 후보와 동일 상태로 되돌리지 않았다. 이번 새 검증 대상은 native NT20개 중 소비 연결이 남은 selector1C의 데이터다.

## 새 정적·CPU 검증

원본 table file40ED의 pointer8BF9 → source4C09/current24C09의 압축99바이트를 대조했다. 네임테이블2000..23FF의1024셀, 즉 tile960/attribute64셀을 복원했다. 원본과현재047에 동일 pointer를 명시적으로 공급한 native803F→80BE의 D-clear128조건쌍에서1024개2007 주소·값·cycle과 전체RAM/레지스터/명령수 일치다. 이것은 자연 caller나 실제 PPU 실행이 아니다.

높은 tile 값은B0..B9이며48셀이다. source116이background0800에 있을 때의 HOWTO90..96, source120이background0800에 있을 때의 PAUSE24타일8A..8F/9A..9F/AA..AF/BA..BF와 각각 겹치는 셀은0이다. **폰트 매핑을 가정한 제한된 결과**다. NT1C의 실제 font 공급은 미연결이므로 나머지 그림을 장식 또는 문자로 확정하지 않는다. 다른폰트·스프라이트·별도PPU command의 소비도 이 계산으로 제외하지 않는다.

기존99/101/102/103/112 및104후보 자료의 SHA를 재확인·연결했다. HOWTO·PAUSE 최종 보존/번역 결정은pending이며 registered본문54/그림33 분모와CSV를 변경하지 않았다.1C의 소비 부재는 전역corpus 완료나 unreachable 증명이 아니다.

## 인계

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지。새 스크립트·보고서·본문서·오늘인계/journal/canonical/manifest만 작성했다. ROM/CSV/원본/1편/기존 QA 보존. 새 빌드/적용·에뮬레이터·직접 장면 검증은 없고 정적·제한된CPU만 추가했다. 자연전체완주·실기/청음·전역corpus·최종사람검토·정식배포는 미완료다. 카페 완성 작업기는 전체 완료 후 작성한다.

조사 도중 Memory가 Python slice를 지원한다고 가정한 읽기가TypeError로 중단됐다. 정수주소 읽기로 수정해 코드 문맥을 조사했으며 ROM·출력 수정 없음. 존재하지 않는 조사 문서명을 읽으려던 호출은 실제 파일 목록으로 교정했다. 이 읽기 오류를 새로운 게임 결함으로 취급하지 않는다.

재현: `python scripts/analyze_nt_candidate119.py`는 최초 보고서용이며 기존 출력은 거부한다. 복제 검증 시 보고서 경로를 새 이름으로 바꿔 실패/성공을 보존한다. [동결 자산](../manifests/candidate119_assets.json), 감사 경로 `qa/reports/candidate119_session.json`.

다음 작업 하나: native bank38의 A5C6→A5FD에서 CHR61과 actor ED를 설정하는 조건·호출 문맥을 연결해, POW 후보와 다른 실제 소비인지 구분한다.
