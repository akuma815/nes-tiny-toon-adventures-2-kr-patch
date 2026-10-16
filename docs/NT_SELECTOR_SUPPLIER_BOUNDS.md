# 작업112 — native NT selector의 공급 경계

[분석기](../scripts/analyze_nt112.py), [보고서](../qa/reports/nt112_supplier_bounds.json). 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지. 원본·1편·047·CSV·기존 QA 보존.

원본PRG의10개 직접 JSR8025 지점은 nativebank32 코드 또는 fixed 코드에 있으며 해당 지점의 원본/현재 바이트가 같다. 8곳은 LDX immediate, 두 곳은 CC18에서06D0, F982에서06E5를 읽는다. 동일 CPU8025의 다른 bank 코드를 decoder로 간주하지 않는다. JSR8023의 두 clear 경로는 native LDX00에서 decoder로 이어진다.

CC10의 직접 call5개를 조사했다. 네 곳은 호출 직전06D0에0C/0E/10/12를 쓰고, 도입부8F4B helper의 확인한 literal 진입은04/06/08/0A다. CC02는 decoder 호출 후 X04로CC18에 분기한다. F97A 직접 call2개는 직전에06E5를18/1A로 쓴다. 이 명명한 공급 경로의 selector 집합은 `00 02 04 06 08 0A 0C 0E 10 12 14 16 18 1A 1E 20 22 24 26`이며1C는 없다.

06D0는 도입부90B3/90D2 등에서 프레임 카운터로도 쓰인다. RAM에1C가 있었다는 사실만으로 decoder가1C를 받았다고 판단하지 않는다. 이번 이름 붙인 call 경로에서는 selector 값이 먼저 저장되며, 모든 인터럽트·간접/indexed writer와 계산 jump까지 닫은 전역 증명은 아니다. raw motif 개수만으로 임의 bytes를 명령어로 분류하지 않았다.

[작업109](NT_SOURCE_CONSUMER_047.md)의 동결 보고와 [작업111](CASTLE_ROOM6_NATIVE_QA.md)의 실제 native 로그/환경 해시를 연결했다. source NT20 중8025 관측selector17개, 별도 기존 실제 소비0E/26, 미연결1C 한 개다. 이는 이20목록의 연결 상태이며 전게임 번역 완료율이 아니다. 1C의8BF9/source4C09/99byte 스트림은 보존하고 미사용·자동 제외·사람 보존 승인으로 정하지 않았다.

이번은 정적 코드/명명한 caller byte 대조와 동결 기록 재검토다. 새CPU/에뮬레이터/build/apply/직접 장면 검토 없음. 미완료는1C의 다른 공급, 별도 STAGE SELECT 소비, HOWTO/PAUSE/POW 전역 공급, 자연 전체 완주, 최종 사람 검토, 실기·PCM청음·정식 배포다. release_eligible=false. 완성 카페 작업기는 전체 완료 후 작성한다.

재현: `python scripts/analyze_nt112.py`는 기존 보고서 덮어쓰기를 거부한다. 변경 파일은 분석기·보고서·본문서/오늘 인계·journal·canonical 문서다. [동결 manifest](../manifests/nt112_assets.json)에 파일별 SHA, source/1편/링크 감사는 `qa/reports/nt112_session.json`에 기록한다.

다음 작업 하나: **native8113의 별도 비압축 command 표와 실제 literal 입력을 전개해 STAGE SELECT/팔레트-only 별칭을 등록 대사·NT20과 구분하고 새로운 문구 소비 여부를 조사한다.**
