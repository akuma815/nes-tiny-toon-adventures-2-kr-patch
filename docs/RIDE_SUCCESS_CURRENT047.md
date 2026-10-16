# 작업107 — 현재047 입장 성공과 출발 대사 검증

2026-10-06 사용자 “진행” 지시로 작업106 이후를 재개했다. 이번 작업은 초기 일반 티켓4를 설정한 현재047 롤러코스터 입장 성공 경로를 확인했다. 현재047 ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`, 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d` 그대로다. 원본·1편·과거 증거·동결 CSV/검토자료는 보존했다.

## 입장 성공의 실제 문맥

1000프레임에07D0=4/07D1=0/07D2=0만 설정한 통제 실험이다. 이후에는 기존 controller 입력만 사용했고 ROM·PC·체력·상태로드를 조작하지 않았다. 자연적으로 티켓4를 얻은 증거나 완주가 아니다.

- 요금4장 안내 뒤2000에 native 차감 분기로4→0이 됐다. F9 alias23 뒤2001/2008의 실제 글꼴 초기화 기록은 slot2A/포인터9910/font196이다.
- [2004](../qa/dialogue/context107_normal4047/frame_02004.png)는 이전 요금 문장이 남아 있으며, [2010](../qa/dialogue/context107_normal4047/frame_02010.png)은 두 행을 지우는 중이다. 전환 동안 공유font196을 유지한다.
- [2040](../qa/dialogue/context107_normal4047/frame_02040.png), [2100](../qa/dialogue/context107_normal4047/frame_02100.png)의 “출발!”은 실제 MAIN_05920/slot2A다. NT22A8의 `0037386c7a7a7a7a`와 원본 pointer/현재 ROM body를 대조했다. 두 번째 행은 비어 있어 이전 요금 두 번째 행이 남지 않는다.
- [3000](../qa/dialogue/context107_normal4047/frame_03000.png)은 root4/phase5의 롤러코스터 플레이다.4200까지 해당 플레이 상태를 확인했으며 코스 클리어를 주장하지 않는다.

위5PNG를 assistant가 직접 확인했다. [정확한 문맥원장105](../workspace/translation/scene_context_105.json)의 MAIN05920=놀이기구 시작2A와 일치한다. 매표소 MAIN057AC/15와 별개다. [부족 분기106](NORMAL3_CURRENT047_CLOSEOUT.md)의 RAM06CF=2A는 이전 거절29를 읽은 뒤 다음 번호였지만, 이번에는 실제9910 소비와 완성NT가 있으므로 출발 대사 표시를 확인할 수 있다. 최종 사람 문체/명칭 승인은 아니다.

## 기계·실행 검증과 캡처 시점

기본 실행과 읽기 전용 팔레트 probe를 각각4200프레임 실행했고 exit0이다. 기본1821파일 전부/추가 probe 전부의SHA를 확인했다. Lua만 제외한 공통1820파일과302전체PNG는 byte exact라 관측을 추가해 게임 상태를 변경하지 않았다. 기본302캡처의2416개1KiB CHR 조각도 현재 ROM과 일치한다. 같은047의 과거 작업97 기록 중 추가6100 입력 전 공통302PNG를 포함한1812파일도 byte exact다. 이것은 같은 ROM의 동일 입력 구간 비교이며 원작 전체플레이 동등성은 아니다.

현재endframe1578..2631의 하단font196과 실제PPU2KiB를 확인했다.2634는 native root3/phase0에서 C6/6F3가0으로 초기화된 전환으로 별도 기록했다. NT에 이전 코드가 잠시 남아 있어도 화면은 검고 이전2633 실제읽기는196이다. 대사 번호만으로 font를 강제하지 않는다.

완성NT2019..2634의53캡처를 기존glyph와 native읽기 팔레트로512pixel씩 독립RGB 재구성해 모두 일치했다. probe는 실제glyph37/38의19888 PPU읽기 행을 수집했다. PNG N은 이전 렌더N−1의 팔레트와 대조했다. 사용 중인 Mesen2.1.1 NES는 EndFrame 이벤트 뒤에 VideoDecoder.UpdateFrame을 호출하고 Lua takeScreenshot은 기존 필터버퍼를 사용한다. [NES SendFrame 원천](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/NesPpu.cpp), [Lua screenshot 원천](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Debugger/LuaApi.cpp), [VideoDecoder 원천](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Shared/Video/VideoDecoder.cpp). 이 정렬은 본 캡처 환경의 검증 범위이며 다른 에뮬레이터/모든 이벤트에 일반화하지 않는다.

초기 검증기v1/v2는 페이드palette10/00을 누락했고, v3는 Mesen00색과 프레임시점을 잘못 가정했으며, v4는2634의 native latch 초기화 경계를 포함해 거절됐다. 네 실패 관찰과 v1..v4를 보존하고 [v5](../scripts/verify_context107_v5.py)에서 해결했다. 해당 실패는 ROM 오류가 아니므로 새 ROM/번역 수정 없이 현재047을 유지했다. 색은 [Mesen2.1.1 2C02 표](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/NesDefaultVideoFilter.cpp)의00=102/102/102,10=173/173/173,20=255/254/255,0F=0/0/0을 사용했다. 실기 색상 검증은 아니다. 해당 원천 파일을 work/context107에 버전·SHA와 함께 보존했다.

[검증보고서](../qa/reports/context107_validation.json), [기본 환경](../qa/dialogue/context107_normal4047/environment.json), [probe환경](../qa/dialogue/context107_palette047/environment.json), [동결자산](../manifests/context107_assets.json). SHA의 검사 범위와 결과는 별도 종료 감사 `qa/reports/context107_session.json`을 따른다.

## 재현과 인계

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/context107_normal4047 --frames 4200 --inputs config/menu_coaster_001.json --seed config/world_coaster_ticket4_seed_001.json
python scripts/run_context107_palette.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/context107_palette047 --frames 4200 --inputs config/menu_coaster_001.json --seed config/world_coaster_ticket4_seed_001.json
python scripts/verify_context107_v5.py
```

기존 출력은 거부한다. 재현은 새 QA/보고서 경로로 해야 한다. Mesen2.1.1 exe SHA `d2eb03c2590c648bf329f127ebcfefd70130e7690a9e2ccdba8616faea1fe96b`, private 설정 SHA `cee81286ae23bd0b4fa417a9429b63dcf645ce2bdd122db5aa1d572990803621`. 기존 사용자 에뮬레이터 설정은 변경하지 않았다.

정적은 보호파일/캡처/원천/폰트·포인터·NT 해시와 구조 대조다. 빌드/적용은 이번에 새로 하지 않았다. 실행은 초기 티켓 seed 두 회, 직접장면은 실제PNG5장, 독립RGB는53캡처다. 자연 전체3구간 완주/전역corpus/실기/PCM청음/최종사람검토/정식배포는 미완료다. 카페 완성 작업기는 모든 작업 완료 후 작성하며 [오늘 근거journal](journal/2026-10-06.md)을 쌓는다. 외부 게시 없음.

변경 파일은 context107 검증기v1..v5·실패관찰4·보고서, probeLua/실행기, 두 캡처 폴더와 pinned 원천, 본문서·날짜인계·journal·README/조사/계획/HANDOFF다. 파일별SHA는 manifest에 있다.

다음 작업 하나: **현재047의 본문·그림·소비경로·자연플레이 미완료 범위를 기존 동결 증거로 정리하고, 반복 검증이 아닌 다음 기술 조사 한 건을 선택한다.** 별도 중단 지시가 없으면 이어간다.
