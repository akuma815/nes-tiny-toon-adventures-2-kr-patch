# 작업101 — PAUSE 공급 후보의 정적 경계

현재047 ROM/CSV/검토패치를 변경하지 않았다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. 원본/1편/기존 검증본을 보존했다. [분석기 v2](../scripts/analyze_pause_supply101_v2.py), [보고서](../qa/reports/pause101_supply_bounds.json).

software CHR34..39의 raw STA/STX/STY ZP motif190개를 목록화했다. immediate load가 인접한166 motif에는119/120/121이 없다. 이는 raw byte 목록으로 모든항목의 실행 코드/경로를 자동 증명하지 않으며 데이터처럼 보이는 STY motif도 보존한다. 34/35는 다음1KiB bank도 지정하고36..39는 독립 sprite bank인 nativeFD67 구조를 유지했다.119가 pair의120을 만들 수 있으므로119도 후보 값에 포함했다. 이 값들의 인접 부재만으로 computed/indexed/indirect 공급이 닫히지는 않는다.

원본 IRQ의 고정 CHR port write7그룹을 native CPU slice로 실행했다. 6그룹은 A000/A008/B000/B008을24cycles, blank1그룹은8port를34cycles에 쓴다. 이 그룹의 원본 값에는120/121이 없다. 현재047에서 여전히 상수인6그룹의 명령수·cycle·포트쓰기 시점은 원본과 같다. train72..75→216..219와 결과124/125→206/207 같은 기존 변경은 기록했다. sourceFBCE의 LDX#5A는 현재047 LDXC6로 바뀐 기존 폰트 hook이므로 현재의 고정상수 그룹으로 분류하지 않았다. source의 별도C6/C7 IRQ 소비도 미해결 공급으로 남겼다. 짧은 그룹 비교를 전체 IRQ timing 검증이라고 부르지 않는다.

raw LDA#78 다섯곳은 nativeSTA0530, AC32의 거리비교, CMP04AF 위치비교, STA11 기하 계산, STA04A5(97에서 실제 확인한깃발X120) 문맥이다. 이들로 직접CHR 쓰기를 주장하지 않는다. A078/A079처럼 보이는 데이터 행도 CPU 명령으로 확정하지 않았다. PAUSE 그림이 있는 [원본 페이지 확대](../work/candidate_font099/CHR_page_1E_6x_static.png)를 직접 보았다. 캐릭터와 함께 있는 정적CHR 설명그림이며 실제 게임 표시가 아니다. source120/121 2KiB는047에서도 그대로다.

남은 구체적 후보는 bank36의 native803C LDA($01),Y→STA36 및9362 LDA($00),Y→STA36이다. 이들은 animation pair/action descriptor에서 font값을 받아 단순 immediate 검색으로 닫을 수 없다. 또한 source/current C6/C7 공급 및 generic indexed/indirect 다른alias는 별도로 남는다.

v1은 source상수5A→현재LDXC6 부분 slice까지 cycle equality를 잘못 요구해 report 전에중단했다. [실패 기록](../qa/reports/pause101_v1_observation.json)/[v1](../scripts/analyze_pause_supply101.py)을 보존했다. v2는 source7/current6 상수그룹을 구분하고 현재동적소비를 명시했다. 재현 `python scripts/analyze_pause_supply101_v2.py`는 이미 존재하는 보고서를 거부한다. [동결 자산](../manifests/pause101_assets.json).

정적/CPU 관측만 추가했으며 새 runtime/build/apply는 없다. 실제 pause/resume4경로는 [49](PAUSE_WORLD_SURVEY.md)의 한정된 기존 증거다. 전역 미사용·최종 사람 보존 승인·전역corpus/자연전체완주/PCM청음/실기/최종 번역검토·공식배포/카페완성작업기는 미완료다.

다음 작업 하나: native803C/9362의 player/action pointer table을 연결하고 정의된 descriptor의 bank36 값을 경계와 함께 검증한다.
