# 작업118 — 캡처 프레임의 증거 범위

[검증기](../scripts/analyze_capture118.py), [결과](../qa/reports/capture118_bounds.json), [공식 소스 기록](../work/capture118/source_files_v2.json), [직전 PNG 예외](CART_V7_CURRENT047_ATTEMPT.md).

Mesen 2.1.1 공식 트리와 6개 파일의 Git blob SHA-1을 대조했다. 새 다운로드 4개와 작업107의 LuaApi/NesPpu 2개이며, 기존 VideoDecoder 파일도 새 공식 다운로드와 바이트 동일하다. 태그의 출처를 고정한 정적 조사이고 설치 바이너리의 재빌드 검증은 아니다.

## 확인한 경로

NES SendFrame은 EndFrame 이벤트를 먼저 호출하고 그 뒤 현재 프레임을 VideoDecoder에 제출한다. 일반 실행의 디코딩은 별도 스레드다. Lua TakeScreenshot과 VideoDecoder의 stream 래퍼는 WaitForAsyncFrameDecode를 호출하지 않는다. BaseVideoFilter의 ApplyFilter와 screenshot 버퍼 복사는 같은 mutex 안에 있다. 따라서 이 두 동작의 중첩을 곧바로 찢어진 이미지의 원인이라고 주장하지 않는다. 후속 HUD/필터를 포함한 모든 출력 동작의 원자성을 이 mutex만으로 보증하지도 않는다.

공식 근거: [NES 이벤트 순서](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/NesPpu.cpp#L1182), [Lua 래퍼](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Debugger/LuaApi.cpp#L808), [비동기 디코더와 캡처](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Shared/Video/VideoDecoder.cpp#L172), [잠금과 복사](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Shared/Video/BaseVideoFilter.cpp#L166).

**프레임 이름은 Lua 관측 시점을 나타내며, PNG에 복사된 필터 프레임 번호를 보증하지 않는다.** 스레드 처리 시점은 차이의 가능한 설명이다. 세 예외에 대한 디코더 타임라인이나 출력 프레임 식별자를 저장하지 않았으므로 정확히 N-1/N-2인지, 그 원인이 비동기 지연인지 확정하지 않는다.

## 기존 자료 재확인

1281/2820/4320 각각의 두 실행 PNG·RAM·PPU·OAM·매핑·core-state, 총36파일의 SHA를 실행 환경과 대조했다. raw/core는 각 시점에서 동일하고 PNG의 RGB 차이는 8/7028/10630픽셀로 직전 보고서와 같다. 3장 모두 보존했다. 작업117의 702시점 raw/core 일치 및 699 PNG 일치는 그 기록의 범위로 유지한다. 작업107의 53개 완성 NT/RGB와 작업111의 107개 비교는 각각 실제 대조한 범위에서 유효하며, 모든 캡처가 항상 한 프레임 늦다는 보증으로 확대하지 않는다.

향후 시각 검증은 실제 NT/CHR/팔레트·렌더 읽기 또는 프레임 식별 근거를 화면과 연결해야 한다. 같은 파일 이름과 현재 RAM만으로 전체 PNG 동일성을 전제하지 않는다. 이 작업에서는 새 에뮬레이터 실행이나 임의 sleep 보정, PNG 교체를 하지 않았다.

## 인계

원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지. ROM/CSV/설정/기존 검증본 수정 없음. 정적 소스·기존 파일 검증만 수행했으며 새 CPU 사례·빌드/적용·에뮬레이터·직접 장면 검증은 없다. 전체 자연 완주·전역 corpus·최종 사람 검토·실기/청음·정식 배포는 미완료이고 release_eligible=false다. 카페 완성 작업기는 전체 완료 후 작성한다.

새 변경 파일은 work/capture118 공식 트리/출처/4소스, 분석 스크립트·보고서·본문서·오늘 인계/journal 및 canonical 문서다. 다운로드 첫 메타 저장의 들여쓰기 오류로 1파일 기록 후 다음 반복에서 기존 출력 보호 assert가 발생했다. 부분 source_files.json을 보존하고 v2에 4개를 완성했다. 원본·ROM·QA를 변경한 실패는 아니다. Pillow getdata 경고는 결과에 영향을 주지 않았으며 소비된 스크립트를 바꾸지 않았다.

재현: `python scripts/analyze_capture118.py`는 최초 출력 전용이다. 기존 결과를 덮어쓰지 않으므로 재현 시 출력 경로를 새 이름으로 바꾼 복제 스크립트를 사용한다. [동결 자산](../manifests/capture118_assets.json), 감사 결과 경로 `qa/reports/capture118_session.json`.

다음 작업 하나: 기차 간판·HOW TO CONTROL·PAUSE 정적 후보의 CHR 페이지와 native 폰트 공급 코드를 대조해, 소비가 연결되지 않은 후보의 기술적 범위를 정리한다.
