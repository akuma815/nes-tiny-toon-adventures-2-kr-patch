# 문단별 글꼴 공급과 둘째 도입 문단 — 008

이 문서는 작업12의008과 당시3draft 입력에 대한 기록이다. 현재 통합 기준은 [012와 셋째 문단](POC_DIALOGUE_THIRD.md)이며4draft/50untranslated다. 아래 역사적검사를 현재CSV로 재실행하지 않는다.

2026-10-05 작업12의 개발 검증본이다. [ROM](../build/dialogue_kr_poc_008/TinyToon2_dialogue_kr_poc.nes), [IPS](../build/dialogue_kr_poc_008/TinyToon2_dialogue_kr_poc.ips), [실제 둘째 문단](../qa/dialogue/pages008_attract/frame_01320.png), [검증 보고서](../qa/reports/dialogue_pages008_validation.json), [자산 manifest](../manifests/dialogue_pages_assets.json)를 따른다. 타이틀003·첫 문단·홈003은 보존했다. 번역 원천54행 중3행draft/51행untranslated이며 정식 배포 단계는 아니다.

둘째 문단 MAIN_05625는 초안 **어느 날 마을 변두리에 / 커다란 놀이공원이 생겼어**다.18개 한글을 Galmuri7에서 공급한다. 원본40바이트, FD3/4,21/20전개칸, FE위치20/FF위치39와 literal00 횟수2/1을 유지한다. 추가 여백은 비0 빈 타일7A로 처리해 원본 reader의43호출/4245사이클을 호출별로 보존했다. 원천 entry/raw/tokens/pointer 필드는 변경하지 않았다.

## 초기화와 글꼴 수명

원본9417 초기화는 줄 위치를 정한 뒤06CF의 테이블에서06CD/06CE와06/07을 완성하고06C3/06C4를0으로 만든다.942B의 인덱스 설정은 유지하고9430부터 헬퍼를 호출한다. 헬퍼는 완성pointer에 따라 C6를95F9→80,9615→84,나머지→5A로 고정한다. 도입 시작8E88에도80을 초기화한다. FF가06CF를 먼저 늘려도 현재 글꼴은 유지된다. 홈은 기존06EA profile0→FB34→C6→FB1F 경로에서82를 따로 공급한다.

| 문단/소비기 | CHR banks (10진) | 현재 ROM 파일 범위 |
|---|---|---|
| 원래 일본어 글꼴 |90/91|36810에서56810..57010으로 위치 이동; 바이트 동일|
| 첫 문단 |128/129|60010..60810|
| 홈 profile0 |130/131|60810..61010|
| 둘째 문단 |132/133|61010..61810|

주소 범위는16진이며 끝 주소는 제외한다. PPU0000의 actualfont를544표본에서ROM의 해당2KiB와 직접 비교했다. 둘째1320/4040의 native NT21E4/2224 각24칸은 실제reader 전개값과 남는0칸에 정확히 일치한다. NT29E4/2A24는 관측된 mirror이며 별도 화면 영역이 아니다.

실행 callback 기준: 첫 FF1002 이후 font80 유지,1103에 두행 비움,1107 초기화 중 완성pointer9615로84선택,1244에 반복 초기화,둘째완성1320에는id3이지만pointer9615/font84 유지,1431에 셋째pointer963D/font5A 복귀. endFrame snapshot은1107까지 이전pointer,1108부터 새pointer다. callback과snapshot 번호의 차이를 처리 지연으로 해석하지 않는다. 자연반복에서는3681 첫초기화/3830 둘째초기화/4154 일본어복귀를 관측했다. Start1300 입력 경로는1440 snapshot에id0/C6=0이며 장면이 실제로 건너뛰어졌다.

## PRG 확장과 코드 소유권

E158..E248의0영역은 여러 포인터가 공유하는 빈 데이터여서 코드 공간으로 기각했다. 대신 PRG128→256KiB를 사용한다. CHR136KiB는 크기를 유지하고 파일 위치만+20000 이동한다. ROM401424바이트,6개의 합성 Expected Write, 전체diff264929바이트다. 큰 extension write의 내부도 verifier가 각mirror/코드/글꼴/보호영역으로 분해해 검사한다.

Mesen의 VRC7 구현은 PRG 선택값의 하위6비트와 마지막 fixed bank를 사용한다. [공식 소스](https://raw.githubusercontent.com/SourMesen/Mesen2/master/Core/NES/Mappers/Konami/VRC7.h)를 참고했고, 실제 실행에서 변환 주소를 확인했다. 원래16개의8KiB PRG banks를16..31에 복제해 native30..3F의 alias를 보존했다. 기존native32/33은 새18/19를 선택하며 E000은31이다. source marker32는 canonical18에 유지한다. 저위 physical2의 marker는02이고131바이트 헬퍼를95F9부터 둔다. native 문장 데이터는canonical18에 남기며 둘째40바이트만 수정한다.

FDD3/FDDB를 통해02/03으로 들어갔다가 native32/33으로 복귀한다. bank 전환 직후 반환 PC가 새 뱅크에 있으므로9430..9449와8E88..8EA3 bootstrap을physical2/canonical18 모두 동일하게 둔다. 전역2B를 스택에 보관·복구하고A/X/Y/P/SP와 원래 RAM 효과를 보존한다. CPU model784조건과 실제19회 페이지 초기화의SP/8000/A000/2B복귀를 각각 검사했다. 관측한 헬퍼 실행은 도입setup scan239,문단초기화 scan19..26 근처로 한정한다. 모든 미방문 장면의 비동기 인터럽트 안전성을 증명한 것은 아니다.

## 픽셀 경계 오류와 사이클 교정

004는 새 뱅크에 bootstrap continuation이 없어 검은 화면으로 실패했다.005는 문단/복귀가 표시됐지만 경계 픽셀이 달랐다.006은IRQ 총 시간만 맞추며 중간PPU 쓰기를 늦춰 실패했다.007은 모든IRQ PPU/CHR 쓰기 상대시점과 총342사이클을 복원했지만 헬퍼 실행 뒤IRQ 진입 위상이 달랐다. 이 실험본은 모두미채택이며 QA와 build report를 보존한다.004의helper_bank=16 메타데이터는 오류이며 실제코드/실행은02였다.008은02로 바로잡았다.

원본FE53..FE5C 대기 루프는19사이클이다. 헬퍼 추가시간을page133/152,setup114처럼19의 배수로 맞추니 경계 차이가 없어졌다. 신규 IRQ는76바이트를 유지한다. 첫delay 뒤 이미Y=0인LDY#0을NOP로 대체하고, paired2006/2005 이후 scan94의 중복2002읽기를2NOP로 바꿔 자리와 시간을 확보했다.47카운터8회+PHA/PLA가70사이클이고LDX C6의1사이클 증가를 상쇄한다.47최종0·stack균형·IRQ끝복원과 모든PPU/CHR쓰기offset을 유지한다. 기존003과 새008의frame938..1005 실제IRQ 진입/쓰기2820개 시점도 동일하다. 차이검사의 마스크는 원래 대사두줄만 사용했고 y92풍경 경계를 숨기지 않았다.

도구는1편의 strict asm6502.py를 읽어서 복사했으며1편을 수정하지 않았다. py65 1.2.0의공식NMOS6502 151opcode/mode·604벡터 roundtrip을 통과한다. 새코드는 decimal 연산과 비공식 opcode를 쓰지 않는다. py65는[기존 도구 폴더](../tools/python/py65-1.2.0)에 있는 BSD3 라이선스를 따른다. Galmuri7 2.403은[폰트 원천](../workspace/fonts/galmuri7_8x8/font_source.json)의 SIL OFL1.1이며 atlas/TTF8px 픽셀동일성·타일왕복을 확인했다.

## 검증과 제한

| 검증 분류 | 결과 |
|---|---|
| 정적 | 원본·54원천·sourceCHR·title003·기존clone·mirror·공유0asset 보호,미등록glyph0,Expected Write 중첩0 |
| CPU | ABI784조건,깨진004 control기각,ISA604벡터,first37/3282·second43/4245·home12/1246 호출별원본동일,IRQ342사이클/쓰기offset동일 |
| 빌드/적용 | 재빌드와 깨끗한원본에 실제IPS적용 모두008해시동일; 한글/공백 경로 실행 |
| 에뮬레이터 | 5400자연도입384표본,Start720 3000프레임233표본,Start1300 3000프레임233표본; 총850,텍스트밖차이0,홈233전체일치,palette/OAM/id/pointer 동일 |
| 직접 시각 | 실제1320·1560·4040·홈1080 확인; 둘째두줄·일본어복귀·재진입 정상,최종사람번역/디자인승인대기 |

동적 등록은두도입pointer만 구현했다. 나머지51원천/장면 대응과 전체플레이는 남는다.19사이클 정렬은 IRQ위상을 보존하지만 추가코드 때문에 RNG22 대기루프 반복수는 달라질 수 있어 미방문 gameplay의 난수 동작 동일성을 주장하지 않는다. 놀이기구/교환/엔딩·오디오·reset·savestate·실기QA는 미수행이다. dist는 비어있다.

## 재현

프로젝트루트/PowerShell,새 출력 경로를 사용한다. 아래첫명령은원본식별,그다음build/apply,마지막두명령은이미고정된008 QA 검증이다. 현재builder는008과 같은바이트를 재생성하며 추가한주석/동봉source때문에보고서의asm파일해시는원래008과다르다.008에는원래당시해시에맞는page_font_used.asm이보존되어있다.

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_source.ps1
python .\scripts\build_dialogue_pages.py --output .\build\dialogue_pages_repro_next
python .\scripts\dialogue_ips.py create --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --target .\build\dialogue_pages_repro_next\TinyToon2_dialogue_kr_poc.nes --patch .\build\dialogue_pages_repro_next\TinyToon2_dialogue_kr_poc.ips --scope 'Development pages008 reproduction'
python .\scripts\dialogue_ips.py apply --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --patch .\build\dialogue_pages_repro_next\TinyToon2_dialogue_kr_poc.ips --output '.\qa\dialogue\한글 재현 다음\TinyToon2_pages_applied.nes'
python .\scripts\run_dialogue_qa.py --rom .\build\dialogue_pages_repro_next\TinyToon2_dialogue_kr_poc.nes --output .\qa\dialogue\pages_repro_next --frames 5400 --script .\scripts\capture_dialogue_pages.lua
python .\scripts\verify_dialogue_hooks.py --build .\build\dialogue_kr_poc_008
python .\scripts\verify_dialogue_pages.py
```

Start 경로는run_dialogue_qa.py에 `--start 720` 또는 `--start 1300`과 `--frames 3000`을 추가한다. 기준003도 같은Lua·프레임·입력으로 별도출력에서 실행해야 비교한다. 새로운 재현QA를 원래008 캡처로 오인하지 않으며 원래report를 덮어쓰지 않는다. reset/save로드/RAM개입은 없다.

**다음 작업 하나: MAIN_0564D를 번역하고 페이지 글꼴 등록을 확장해 출력·대기·지우기·다음 문단·재진입을 검증한다.**
