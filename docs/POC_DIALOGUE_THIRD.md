# 셋째 도입 문단과 글꼴 등록 — 012

이 문서는 작업13 당시012 기준을 보존한 기록이다. 작업14 현재 개발본은 [넷째013](POC_DIALOGUE_FOURTH.md), 재개는 [HANDOFF](HANDOFF.md)를 따른다.

2026-10-05 작업13의 현재 개발본은 [012 ROM](../build/dialogue_kr_poc_012/TinyToon2_dialogue_kr_poc.nes) / [IPS](../build/dialogue_kr_poc_012/TinyToon2_dialogue_kr_poc.ips)다. [실제 화면](../qa/dialogue/pages012_actual_4x.png), [검증](../qa/reports/dialogue_third012_validation.json), [자산 식별](../manifests/dialogue_third_assets.json), [현재 인계](HANDOFF.md)를 따른다. 이전 [008 구현](POC_DIALOGUE_PAGES.md)은 당시의 기반으로 보존했다.

MAIN_0564D의 원문은 `みんなが そのわだいでもちきりのなか`다. 놀이공원 이야기로 모두 떠들썩한 가운데 다음 편지 장면으로 이어지는 내레이션이다. 초안은 **모두가 그 얘기로 떠들썩할 때**이며 이름이나 매크로가 없는 한 줄이다. 다음 일본어 장면의 `バスター・バニー`를 확인해 원천 notes의 잘못된 Babs 표기를 Buster Bunny로 정정했다. 한글 본문은 바뀌지 않았고 최종 사람 검토는 대기 중이다.

## 삽입과 보호 범위

원래24바이트/23전개칸/FF끝/00 세 개를 유지했다.24칸 폭에서16칸 본문 앞에4칸,뒤에3칸을 두고 마지막 한 칸은 native 빈칸이다. 처음3칸은00,추가여백/단어공백은 빈 타일7A다. reader24호출/2502사이클과 모든 호출의커서/사이클이 원본과 같다. 원문·raw tokens·참조·포인터와 다른53행은 변경하지 않았다. 현재54원천 중4draft/50untranslated다.

Galmuri7 2.403의12한글을 atlas와 TTF8px에서 픽셀단위로 비교하고 NES2bpp 왕복을 검사했다. 원본90/91font의clone을CHR134/135에 넣고 필요한12glyph와7A만 변경했다. ROM파일 범위는16진 `61810..62010`이며 끝 제외다. 기존padding의 마지막2KiB를 써서 PRG256KiB/CHR136KiB/총401424바이트는008과 같다. 다음font에는 추가 CHR 공간 설계가 필요하다.

첫째128/129·둘째132/133·홈130/131·원본CHR·타이틀003·고정IRQ를 그대로 보존했다. 독립 verifier가008 전체바이트를 기준으로 helper2/양쪽bootstrap/셋째24바이트/셋째2KiB 합성 변경만 적용해012 전체와 비교한다. immutable 원본으로부터6 Expected Write를 다시 적용해 전체일치/중첩0도 확인한다. 전체diff는264943바이트이며 대부분은 기존PRG확장/CHR파일위치 이동이다.

## 글꼴 수명과 처리 시간

완성pointer95F9→C6=80,9615→84에963D→86을 추가했다. 나머지는5A로 복귀한다. 문단번호06CF의 FF 선행증가로 즉시font를 바꾸지 않는다. 기존helper2/canonical18의동일bootstrap,2B·SP·mapper복구를 유지했다.

셋째 FF 처리 후 snapshot1492의ID는4이지만pointer963D/font86을 유지한다. snapshot1623에문자행이비고1629까지font86을 유지한뒤,다음native초기화callback1629가pointer9655/font5A를선택한다. snapshot1630부터새pointer이며1680의PPUfont는원본90/91과같다.4280에서는자연반복의셋째문단이동일하게출력된다. Start1530은원래대기/전환을거쳐1680에ID0/C6=0으로건너뛰고도입으로재진입한다. Start1300 경로도1440에ID0/C6=0을확인했다.

009는새선택경로의추가162사이클이19주기에맞지않아CPU gate에서기각했다.010은171사이클로정렬했으나008보다19사이클이길어전환중실제IRQ시점13개가달랐다.화면차이는대사안에한정되었지만,더강한일치조건을달성할수있어미채택했다. 이미A에있는pointer하위바이트를재사용하고기존padding을줄여,145바이트helper의모든48슬롯초기화시간을008과정확히같게만들었다. 첫133/나머지152·setup114 추가사이클은기존과같다. BIT의Z에의존해font를선택하지않도록셋째경로는JMP를사용한다.

CPU ABI1072조건에는A/P변형과C6초기값00/01/5A/80/84/FF의288조건이포함된다. 완성pointer에맞는font선택,register/flags/SP/RAM/mapper복귀,008과동일한초기화시간을검사했다. strict py651.2.0의공식NMOS6502 151opcode/mode·604벡터도통과했다. 공식IRQ본문FB97→FD13의342사이클과쓰기offset은변경하지않았다.

011은위코드로실행검증했다.012는CSV의인물notes만정정해동봉한build로,011/012 ROM은전체바이트가같다.012 보고서와동봉translation_used.csv는현재SSOT에맞는다.011의runtime/CPU증거를ROM SHA와전체바이트동일성검사로012에연결했고,별도012재빌드/실제IPS적용도수행했다.009/010/011과해당QA·동봉source/이전notes는역사적기록으로보존한다.

## 검증 분류

| 분류 | 확인한 결과 |
|---|---|
| 정적 |54원천 보호,다른53행 동일,6합성write/중첩0,008 보호바이트/원본CHR/기존font/공유0asset 동일,12glyph 미등록0 |
| CPU |1072 ABI조건,48슬롯 초기화시간008과동일,reader24/2502 호출별원본동일,ISA604벡터,IRQ본문시간/쓰기offset 동일 |
| 빌드/적용 |012 재빌드와깨끗한원본에실제IPS적용결과동일;한글/공백경로 실행 |
| 에뮬레이터 |1998화면비교에서셋째한줄밖차이0,홈407전체일치,palette/OAM/id/pointer 동일;actualfont527표본과19초기화복귀 확인 |
| IRQ trace |frame1430..1650 진입/PPU/CHR쓰기8973시점동일;기대font레지스터5A/5B→86/87 치환394개만다름 |
| 직접시각 |셋째1560/4배확대와반복4280,다음일본어1680,홈1080을확인;최종사람번역/디자인검토대기 |

자연5400프레임777표본,Start720/3000프레임407표본,Start1530/3000프레임407표본,Start1300/3000프레임407표본을각각008과같은Lua/설정/입력으로비교했다.새캡처는pages011_*이고기준008 캡처의폴더명은pages010_reference_*다.폴더명보다environment.json의실제ROM경로/해시/command가실행대상을정한다. RAM/ROM수정과savestate로드는없다.

## 재현과 미해결

프로젝트루트PowerShell/새출력경로에서실행한다. 아래마지막두검사는고정된012/011증거를검사하며새캡처를원래증거로덮어쓰지않는다.

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_source.ps1
python .\scripts\build_dialogue_third.py --output .\build\third_repro_next
python .\scripts\dialogue_ips.py create --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --target .\build\third_repro_next\TinyToon2_dialogue_kr_poc.nes --patch .\build\third_repro_next\TinyToon2_dialogue_kr_poc.ips --scope 'Development third-page reproduction'
python .\scripts\dialogue_ips.py apply --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --patch .\build\third_repro_next\TinyToon2_dialogue_kr_poc.ips --output '.\qa\dialogue\한글 셋째 재현 다음\TinyToon2_third_applied.nes'
python .\scripts\run_dialogue_qa.py --rom .\build\third_repro_next\TinyToon2_dialogue_kr_poc.nes --output .\qa\dialogue\third_repro_next --frames 5400 --script .\scripts\capture_dialogue_third.lua
python .\scripts\verify_dialogue_third_hooks.py --build .\build\dialogue_kr_poc_012
python .\scripts\verify_dialogue_third.py
python .\scripts\audit_dialogue_third_session.py
```

Start 경로는 `--start 720`, `--start 1530`, `--start 1300` 중해당입력과 `--frames 3000`을사용한다. 모든캐릭터/놀이기구/교환/엔딩장면,전체플레이,오디오,reset/savestate,실기와최종번역검토는남는다. 기존PRG확장과RNG22 대기루프반복수관련미방문gameplay 제한은유지한다. CPU model은비동기인터럽트/실제PPU를대신하지않는다. dist는비어있고외부게시없음.

**다음 작업 하나: 넷째 MAIN_05665를 이름 매크로81과 추가 글꼴 공간 예산을 확인하며 한글화한다.**
