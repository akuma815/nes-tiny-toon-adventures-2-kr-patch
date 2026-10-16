# 작업110 — 성 배경과 건너뛰는 STAGE SELECT 코드

원본·현재047 ROM·번역 CSV를 보존했다. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`.

[분석기](../scripts/analyze_stage110.py), [결과와 사례별 CPU 기록](../qa/reports/stage110_analysis.json). 원본 bank30은 source file0010, 현재047 file20010의 게임 코드이며 공통 D28C 테이블의 course4 항목에 연결된다. source bank32/36과 혼동하지 않는다. fixed C000 코드는 source1C010/current3C010이다. 조사한 8개 코드·인접 데이터 구간이 두 ROM에서 같다.

## 성 배경의 조건

공통 D360은 RAM79를6과 비교한다. 0..5이면 D389, 6..255이면 head CHR64/body CHR118을 정하고 D36E의 native NT14/16 쌍을 선택한다. 원본/047 각각256개의 CPU 사례, 합계512건에서 조건과 결과가 같다. 이 하네스는 decoder 호출 전에 멈추므로 실제 화면이나 모든 수치의 자연 도달을 검증하지 않았다.

성 방 전환의 공통 phase54=7은 F5F8→bank30 선택→969C로 들어간다. A5의 비음수 값을 네 배 해서 977C의 네 바이트 레코드를 읽고 첫 바이트를 RAM79에 쓴다. 977C..980B에는36레코드가 있으며 마지막 A5=35 레코드는 `06 03 0A 00`: 방 번호6, 두 위치 값3/10, 방향0이다. 뒤의980C..9820은 별도의 방 속성 표다. 테이블 뒤를 계속 네 바이트 단위로 읽어 잘못된 방9/10 등의 후보를 만들지 않았다. 모든 A5 생산자·실제 door 진행은 아직 폐쇄하지 않았다.

작업94 현재047 성 플레이 RAM을 당시 environment의 파일 해시에 다시 대조했다. 초기 gold4 경로475장, normal50 경로293장, 합계768개의 root4/course4/phase5 표본은 모두 방0이다. 이 기존 기록은 방6/NT14/16의 실제 관측이 아니다. 당시 티켓 seed를 자연 획득으로 표현하지 않는다.

## 추가 문자열 후보와 일반 경로

원본 CD52의 `LDA #09; JSR 8113`은 nativebank32의 별도 비압축 printer 표에서81B2/source41C2를 선택한다. NT220A의 font124 코드 후보는 `STAGE SELECT`이다. 등록54개 본문이나 그림검토33개에 새 번역 완료 건으로 합치지 않고, 진입이 확인되지 않은 진단 UI 후보로 남겼다.

root3의 실제 inline target은 **CD49, CD73, CE37**이다. CD52는 phase1 초기화 target이 아니다. 일반 phase0은 CD49→CBF0→CF9E→CD4F의 `JMP CE37`→root4/phase0으로 넘어가며 CD52의 printer 초기화를 건너뛴다. CD4C부터 실행한 원본/047 각256 RAM 초기값 사례, 합계512건에서 RAM79=0, root4/phase0/게임phase54=0을 확인했다. CBF0·mapper·IRQ를 실행하지 않은 한정 CPU 검증이다.

CF9E의 literal loop는 ZP68..DF와0400..06FF를 지운다. 뒤의 `LDX #BF; STA 0700,X; DEX; BPL`은 BF가 음수인 초기값이라07BF 한 바이트만 쓴다. 0700..07BF 전체 clear라고 추측하지 않았으며 이번에는 코드를 고치지 않았다. sourcePRG에 CD52 직접 JSR/JMP/word motif는 없지만, 계산 진입·다른 state writer까지 조사한 전역 미사용 증명은 아니다.

## 검증과 인계

정적 코드/표 대조와 한정 CPU1024사례, 동결된 과거047 성 RAM768표본 검토가 이번 검사다. 새 에뮬레이터 실행·빌드/적용·직접 장면 검토는 없다. 최종 사람 검토·자연 전체 완주·전역 corpus·HOWTO/PAUSE/POW 소비폐쇄·실기/PCM청음·정식 배포는 미완료이며 release_eligible=false다. 카페 완성 작업기는 모든 작업 완료 후 작성한다.

재현: `python scripts/analyze_stage110.py`는 기존 보고서 덮어쓰기를 거부한다. 변경 파일은 분석기/보고서/본문서와 오늘 인계·journal·README·조사·계획·HANDOFF다. [동결 manifest](../manifests/stage110_assets.json)에 분석기·보고서·본문서 및 선택한 과거 RAM/환경의 SHA를 기록했다. 원본·1편·로컬 링크 감사 출력은 `qa/reports/stage110_session.json`이다.

다음 작업 하나: **성 입장 후 A5=35/phase54=7을 명시적으로 주입하는 native 방 전환 진단으로 constructor→NT14/16→실제 CHR/표시를 연결한다.** 자연 진행과 구분하고 현재047을 보존한다.
