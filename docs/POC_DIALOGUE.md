# 첫 도입 문단 한글 PoC — 2026-10-04

이 문서는 첫 문단002의 당시 입력·검증 기록이다. 최신 통합003은 [홈 대사와 글꼴 수명 문서](POC_DIALOGUE_HOME.md)를 따른다. 현재CSV는2draft이며 아래1draft 표기는002 시점의 상태다.

**타이틀003과 첫 문단 `MAIN_05609`를 합친 `dialogue_kr_poc_002`를 실제 실행 검증했다.** 번역 원천54행 중1행만 초안이며, 전체 대사 한글화나 배포 후보가 아니다.

![실제 첫 문단 화면](../qa/dialogue/poc002_actual_4x.png)

## 문단과 원천

원문은 실제 글꼴/화면에서 다음과 같이 확인했다.

```text
ここはみんながしってる
アクミ・エイカーズ
```

PoC 초안:

```text
여기는 모두가 아는
애크미 에이커스
```

`workspace/translation/text_ja.csv`가 번역 단일 원천이다. 첫 행은 narrator / intro_acme_acres / draft이며 나머지53행은 untranslated다. raw bytes, control tokens, pointer/reference IDs는54행 모두 초기 원천과 같다. 수정 전 CSV는 `backups/translation/text_ja_before_dialogue_001.csv`에 보존했다. 초안을 허용하는 개발 빌드 정책에 한정하며, 이 상태의 배포 빌드는 허용하지 않는다.

관측 일본어 글꼴의 가타카나를 대응시켜 [문자표](../workspace/tables/kana_codes.json)와 [해석 뷰](../extracted/text/kana_mapping_001/resolved_units.json)를 만들었다. 코드53은ミ이며 실제 표기는アクミ다. 가타카나/부호/숫자를 포함해 **등록한 kana profile의 사용 코드 미대응0**이다. 크레딧3원천은 다른 글꼴 프로파일의 가능성이 있어 의미 해석을 확정하지 않았다. 코드 값이 문자표에 있다고 다른 프로파일의 픽셀까지 검증된 것은 아니다.

## 완료 조건과 구현

대사 공급 가능성을 확인하기 위해 원본 저장→네이티브 파서→PPU 네임테이블→실제 CHR 글꼴→화면의 한 문단 경로를 잇는 PoC를 선택했다. 통과 조건은 원문 raw 보존, 번역/글자 왕복, 원본 외 영역 보호, 중간 출력/대기/다음 문단/재진입, 재빌드/적용 동일성이다. 전체 글리프 용량과 다른 소비기의 동등성은 이번 통과 조건 밖에 남긴 별도 설계 과제다.

### 글꼴

- 사용자 `Font/Galmuri7_8x8.png`를 그대로 복사. `workspace/fonts/galmuri7_8x8/`에 PNG, 대응 TTF, OFL, 출처/해시 manifest를 보존했다.
- Galmuri7 버전2.403 / 8×8셀 / PNG512×1400 / Unicode U+AC00부터64열. 확대·축소 없이 원래 셀을 사용한다.
- 첫 문단14글자 모두 같은 TTF의8px/y=-1 렌더와 PNG 셀 픽셀 동일을 확인했다. NES ink는 실제 원본처럼 픽셀값2다.
- 실제 원본 글꼴 `[0x36810,0x37010)` / CHR banks90·91은 수정하지 않는다. 복제2048바이트를 CHR 끝에 추가하고 나머지6144바이트는 명시적0 padding이다. iNES CHR128→136KiB, ROM262160→270352바이트.
- 임시 한글 코드14개: `17 1E 21 36 38 3E 41 42 45 4A 54 62 69 6F`. 등록54원천의 원본 tile code에는 없는 집합이다. 코드`7A`를 빈 비트맵의 **비0 literal 공백**으로 추가한다. 사용된 원본 일본어/숫자와 타일0은 복제본에서도 보존한다.
- 전체 게임의 unused-code/그래픽 공유 부재는 증명하지 않았다. 이 pool은 이번 PoC 전용이다.

인트로 IRQ의 CPU `$FBCE: LDX #$5A; STX $A000; INX; STX $A008`에서 immediate 한 바이트(ROM`0x1FBDF`)를`80`으로 바꾼다. 원래 명령과 주기는 유지하고 banks128·129를 선택한다. 첫 문단 완성 frame1080의 PPU2048바이트가 ROM 추가 글꼴과 정확히 같고 실제 mapping.csv가 CHR 상대`0x20000/0x20400`을 기록한다. 홈 등 다른 소비기를 한글화한 것은 아니다.

### 원래 슬롯과 진행 시간

원래 데이터는 `[0x5609,0x5625)`의28바이트, pointer는 CPU`95F9`. 새 데이터도28바이트로 고정하고 모든 기존 주/매크로 포인터 및 나머지 문단 데이터는 보존한다.

글자는 NT2000의15/17행에 표시되며, 시작 원점은 column4, 줄 간격은64바이트다. 실제 화면은 논리 NT y보다4픽셀 위다. 관측 창 너비24칸 안에서 한글을 가운데 배치한다.

| 줄 | 원래 FD prefix | 추가 앞 literal 공백 | 문구 길이 | 뒤 literal 공백 | 총 전개 칸 |
|---|---:|---:|---:|---:|---:|
| 첫 줄 | 6 | 1 | 10 | 1 | 18 |
| 둘째 줄 | 7 | 1 | 8 | 1 | 17 |

문구 안 공백도7A를 쓴다. FD 인수, FE/FF 위치, 읽는 길이, 각 줄의 전개 칸 수를 원본과 맞추고 문단 대기96프레임 및 줄 대기7프레임은 수정하지 않는다. 문장을 억지로 줄이거나 공백을 의미 있는 글자로 치환하지 않았다.

## 실패를 분리해 고친 과정

001은 한글 완성 화면과 다음 문단이 정상이어도, 프레임별 비교에서 출력 중 풍경 오른쪽 끝 **y92/x240..250에3~9픽셀 차이**가 있었다. 보호 영역을 넓혀 숨기지 않고 채택을 보류했다.

1. 원래 문단+한글 추가 글꼴의 진단 ROM은 검사한1100프레임 표본에서 타이틀003과 픽셀 동일했다. 글꼴 복제 자체의 그래픽 공유 문제는 해당 경로에서 배제했다.
2. 번역 문단+원래 글꼴의 별도 진단 ROM을 보존해 문자 데이터/파서 쪽으로 원인을 좁혔다. 진단 ROM은 올바른 한글 제품이 아니므로 채택하지 않는다.
3. 001은 가운데 배치를 위한 FD 인수를 바꾸고 실제0 공백을 썼다. 기본 파서의0 공백 빠른 반환과 비0 문자 경로가 달라 읽기 시간/커서가 원본과 달랐다.
4. 002는 기존FD6/7을 유지하고, 동일한 비0/<7F 문자 처리 경로를 타는 빈 glyph7A로 앞/뒤/단어 공백을 표현했다. 데이터 길이/FE·FF 위치도 원본과 같다.
5. 원래 `$937C` 루틴을 py65 CPU로 실행해37회 각각의 사이클/커서가 동일임을 확인했다. 총3282사이클. 이는 CPU harness 증거이며 실제 IRQ/NMI 검증을 대신하지 않는다.
6. 실제 실행을 다시 비교해 풍경 끝 차이0을 확인했다. 001과 진단본은 채택 제외 상태로 보존했다.

001의 최초 비트맵 프리뷰는 순수 글자 그림이며 y 위치를4픽셀 보정하기 전이었다. 최종002 프리뷰와 실제 캡처를 기준으로 삼는다. 타이틀 manifest의 문구가 과거 PowerShell 파이프 인코딩으로`???`가 된 것도 발견해 메타데이터만 교정했다. 타이틀 ROM/PNG는 바뀌지 않았다.

## 검증 결과와 한계

| 구분 | 이번 결과 |
|---|---|
| 정적 | Expected Writes248개/추가8192 포함 전체diff11425바이트. 중첩/설명 없는 변경0. 번역 슬롯 왕복, raw 원천/포인터/나머지 문단/원본 글꼴 보호, 타이틀003 CHR 동일 |
| CPU 검사 | 네이티브 reader37호출 모두 사이클/커서 동일. opcode/동작 확장 없이 IRQ immediate만 변경 |
| 재빌드/적용 | 재빌드와 별도 CLI IPS 실제 적용이 같은SHA. 적용 경로에 한글/공백 포함 |
| 실제 실행 | Mesen2.1.1 무입력5400프레임과Start720..727의3000프레임, 둘 다 종료0. 동일 조건 타이틀003을 기준으로165표본 비교 |
| 화면 비교 | 한글 문단66표본만 변경,99표본 전체 동일. 문단 허용2행 밖 차이0픽셀.165표본의 문단ID/팔레트/OAM 동일 |
| 실제 소비 | frame1080의 PPUfont2048바이트=추가한ROMfont, NT15/17행=새 스트림 전개 결과 |
| 직접 시각 | 실제1080 확대, 출력도중976/완성대기1080/다음일본문단1320/두번째도입3840 비교표 확인 |

[실제 원본/수정 비교표](../qa/dialogue/poc002_comparison.png), [검증](../qa/reports/dialogue_poc002_validation.json), [CPU 검사](../qa/reports/dialogue_parser_cycles002.json), [첫 글꼴 추적](../qa/dialogue/font_trace_001/font_registers.csv).

직접 시각에서 큰 그림 보호, 한글 획과 두 줄, 다음 일본어 페이지/기존 타이틀/홈 진입을 확인했다. 두번째 도입의 한글 재출력 frame3720도 기계 비교로 확인했다. 사용자 최종 번역·폰트 미감 승인과 모든 프레임 직접 시각 검토는 아니다.

전장면/분기/전체 완주/실기/오디오 청취/별도reset·savestate 복구/크레딧 글꼴/전체한글 corpus의용량/최종번역승인/배포·카페업로드는 미수행이다. 타이틀 보조8픽셀문구의 최종 디자인 검토도 별도로 남는다.

## 산출물과 재현

채택: [002 ROM](../build/dialogue_kr_poc_002/TinyToon2_dialogue_kr_poc.nes), [통합 IPS](../build/dialogue_kr_poc_002/TinyToon2_dialogue_kr_poc.ips). IPS는 **깨끗한 일본어 원본에 적용**하며 타이틀003도 포함한다. 이미 수정된 타이틀 ROM에 덧씌우지 않는다.

ROM SHA-256: `7261596d059e50afafaba12252c6b41320f9f4c18190e53a82e528a421323598`.
IPS SHA-256: `3da895d640dc4dd7a6aff7960fd050e1048b1390ea75b9e8812237ee42c4ce39`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_source.ps1
python .\scripts\build_dialogue_poc.py --output .\build\dialogue_repro_next
python .\scripts\dialogue_ips.py apply --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --patch .\build\dialogue_kr_poc_002\TinyToon2_dialogue_kr_poc.ips --output '.\qa\dialogue\한글 적용 다음\TinyToon2_dialogue_applied.nes'
python .\scripts\run_dialogue_qa.py --rom .\build\dialogue_kr_poc_002\TinyToon2_dialogue_kr_poc.nes --script .\scripts\capture_dialogue_poc.lua --output .\qa\dialogue\dialogue_attract_next --frames 5400
python .\scripts\run_dialogue_qa.py --rom .\build\dialogue_kr_poc_002\TinyToon2_dialogue_kr_poc.nes --output .\qa\dialogue\dialogue_start_next --frames 3000 --start 720
python .\scripts\verify_dialogue_parser_cycles.py
python .\scripts\verify_dialogue_poc.py
```

`prepare_dialogue_poc.py`는 최초 원천 이행용이며 기존 추출/백업을 덮어쓰지 않으므로 다시 실행하면 실패한다. 재빌드는 현재CSV/폰트와 동결 title003을 입력해 원본부터 통합한다. 검증 스크립트는 채택002/동결 캡처를 검사하며 새 경로를 자동 채택하지 않는다.

예전`verify_title.py`/`audit_title_session.py`는 초기 CSV해시를 검사하는 **당시 세션 감사**다. 이번에 승인 범위 안에서 초안을 추가했으므로 현재 통합 검증은`verify_dialogue_poc.py`를 사용한다. 옛 검증 결과는 당시 기록으로 보존한다.

**다음 작업 하나:** 문단별 한글 글꼴 공급과 전환 수명을 설계하고, 도입부 둘째 문단·홈 대사의 서로 다른 소비 경로를 조사한다.
