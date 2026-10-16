# 작업113 — 별도 command printer와 STAGE SELECT 후보

[분석기](../scripts/analyze_printer113.py), [보고서](../qa/reports/printer113_catalog.json), [별도 진단 후보 원장](../workspace/translation/diagnostic_candidates113.json). 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지. 원본·1편·047·CSV·기존 성공/실패 QA 보존.

nativebank32의8113은815E 표에서A×2로 pointer를 읽는다. 뒤8176부터 실제 command 데이터가 시작하므로 그 앞12pointer slot을 한정 목록으로 조사했다. 5개의 고유 pointer가 있으며 같은 palette 데이터를 여러 번 가리키는 별칭을 여러 문단으로 세지 않았다. FE는 다음 주소/segment, FF는 끝이다. 주소는 low/high, 내부 queued 주소는 high/low다. A의 high bit가 ASL carry를 만들면 출력 데이터에 zero mask가 걸린다.

| pointer | 내용과 경계 |
|---|---|
|8176|palette32바이트와 뒤의 빈segment. index0/1/2/3/5/6/7 별칭.|
|8199|위 데이터의 빈command tail. index4.|
|819F|palette16바이트. startup index8.|
|81B2|NT220A의 STAGE SELECT 후보와224E의1 0. index9.|
|81C7|nativeCHRcopy 코드 진입 주소와 겹친다. printer data로 읽으면0086에A9 한 바이트를 queue한다. index10/11의 실제caller는 확인되지 않았다.|

원본/047의 코드·표·위 데이터 바이트가 같다. 각ROM의 index0..11/80..8B, 합계48 CPU 사례에서 실제8113이 작성한 RAM0100 queue와 전개모델이 같았다. 이는 PPU에 queue를 적용한 에뮬레이터/실제 화면 증거가 아니다. index10/11을 일본어 문단이나 사용 그림으로 오인하지 않았다. 12slot 밖의 pointer overflow는 조사 범위가 아니다.

명명한 literalcaller는 title801A의index3 palette, root5 CE5A의index8 palette, root6 CEB8의index5 palette, CD59의index9이다. startup 로고/법무 문구는 별도NT/CHR 원천이며 이palette 명령 자체를 로고 텍스트라고 세지 않는다.

index9은 [작업110](CASTLE_BACKGROUND_STAGE_ANALYSIS.md)의 일반 stage 진입에서 건너뛰는 CD52 초기화 코드다. font124 방식으로 읽은 후보 `STAGE SELECT`와 `1 0`을 원문/raw/address와 함께 별도 후보 원장에 보존하고 한국어 초안 `스테이지 선택`을 적었다. 실제 렌더 font/자연진입은 연결되지 않았다. **ROM에 삽입하지 않았고 54본문/45초안·33그림검토 분모에 합치지 않았다.** 전역미사용·사람 보존/번역 승인·build_eligible는false/pending이다.

이번은 source/current 정적 비교·CPU48 queue 사례다. 새runtime/build/apply/직접 장면 검토 없음. 전역corpus·NT1C/후보그림·자연 전체 완주·최종 사람 검토·실기/PCM청음·정식배포는 남는다. release_eligible=false. 전체 완료 후 카페 작업기를 작성하며 오늘journal에는 조사 근거만 추가했다.

재현 `python scripts/analyze_printer113.py`는 기존 보고서를 거부한다. 변경 파일은 분석기·보고서·진단후보원장·본문서와 오늘 인계·journal·canonical문서다. [동결 manifest](../manifests/printer113_assets.json)에 SHA, source/1편/링크 감사는 `qa/reports/printer113_session.json`에 기록한다.

다음 작업 하나: **카트 3구간 완료 조건과 이전2Fbot의 실패를 source/collision telemetry에 대조해 새로 구분할 수 있는 진행 근거를 얻는다.** 같은 입력/bot을 근거 없이 다시 실행하지 않는다.
