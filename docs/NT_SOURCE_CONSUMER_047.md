# 작업109 — native NT20 원천과 실제 호출 기록 연결

현재047 ROM/CSV/원본을변경하지않았다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`, 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`. [분석기v2](../scripts/analyze_nt_consumers109_v2.py), [보고서](../qa/reports/nt109_consumers.json), [원본 NT20 전개셀](../work/nt_consumers109/source_nt_cells.json).

원본catalog의selector00..26hex,짝수20개를원본pointer표와실제저장주소에대조했다.00..1C는PRG nativebank32의80C1표,1E..26은CHR bank18을읽는8233표다. 후자의08 같은copy-local index와globalNTselector26을혼동하지않는다. 모든원본encodedSHA와unpack종료위치/전개셀수는catalog와일치했다. 단순font124 ASCII후보는실제텍스트로확정하지않았다.

## 현재 얻은 연결과 남은 경계

기존97개환경중성공95개에있는native_NT_calls.csv의실제파일SHA/사용LuaSHA/당시ROM전체SHA를확인했다. 비정상종료2개는관측분모에서제외하고보고서rejected_environments에그이유를보존했다. 정상95환경의1829행은8025/물리PRG4025또는24025의정확한진입점기록이다.20개중15selector에이진입점호출이있다. 과거여러ROM/seed/리셋경로를같은047새실행처럼표현하지않고각environment의해시·개입·프레임을그대로연결했다.

| 해당로그에서8025 호출이없는selector | 다른근거 또는남은조건 |
|---|---|
|0E| 이미한글화한매표소: [실제압축literal/header소비](../extracted/graphics/booth_001/consumer.json)의5label 원본주소가0E스트림안에있다. 일반8025로그부재는표시부재가아니다.|
|26| 이미한글화한보너스: [실제154bytecopy와font/NT/RGB](../extracted/graphics/results_001/consumer.json)의source24A0B는globalNT26이며copy-local08이다. 다른소비진입점이다.|
|14/16| 원본fixed D36E/D373의직접producer쌍이있다. RAM79>=6일때34=64/35=118과두NT를선택한다. 해당selected로그에서는실제호출미관측. 진행문맥을추적해야한다.|
|1C| 정상원본pointer와99byte전개스트림이있다. sourcePRG에adjacent LDX#1C motif는없지만계산/indexed/간접공급은미폐쇄다. 미사용으로확정하지않는다.|

14/16 producer 원본file1D37E/1D383을CPU fixed D36E/D373에연결했다. D360 LDA79→D362 CMP06→D364 BCC D389의정확한raw와font64/118선택을확인했다. 이것은소스정적조건이며RAM79의게임상뜻이나그림의텍스트여부/도달가능성을아직확정하지않는다. sourcePRG와CPU윈도우를혼동하지않고 sourcebank36의9362/9417데이터처럼다른문맥을끌어오지않는다.

각selector에는실제call/root/ride/head_font문맥과현재047개별call수, 대표원천을기록했다. 호출시점head_font/CHR0는초기화전일수있으므로실제glyph가그font로렌더됐다는증거가아니다. PNG/PPU/IRQ의draw시점과연결하기전에는글자/그림/제외결정을하지않는다. 등록54/그림검토33/NT20의분모를합쳐전체게임완료율을만들지않는다.

## 검증과 인계

이번은정적sourcepointer/codec전개및동결과거로그재검토다. 새CPU실행/에뮬레이터/build/apply/직접장면시각검토는없다. 원본·1편·현재047·CSV·기존성공/실패증거를보존했다. 분석기v1은정확한BCC상대바이트를1B로잘못기록해guard에서실패했고source/disassembly가23임을확인한v2에서해결했다. [실패관찰](../qa/reports/nt109_v1_observation.json)과v1은보존했다. 게임오류가아니다.

재현 `python scripts/analyze_nt_consumers109_v2.py`는기존보고서/전개출력을거부한다. 변경파일은분석기2버전/실패관찰/보고서/NT20전개셀/본문서/오늘인계·journal/README·조사·계획/HANDOFF다. 파일별SHA는 [동결manifest](../manifests/nt109_assets.json), source/1편/링크감사는 `qa/reports/nt109_session.json`이다. 과거환경의나머지수천RAM/PNG파일을이번에다시전체검증했다는뜻이아니며선택한CSV/Lua/환경과당시ROM이검사범위다.

전역corpus·원본후보HOWTO/PAUSE/POW실제소비폐쇄·자연전체완주·최종사람검토·실기/청음·정식배포는미완료다. 카페완성작업기는전체완료후작성하며현재는오늘근거journal만추가했다.

다음 작업 하나: **fixed D347의RAM79 생산자/호출자를역추적해 NT14/16의조건부선택을실제stage진행문맥에연결한다.** 강제phase진입이나동일카트2Fbot반복을대신근거로삼지않는다. 계속진행한다.
