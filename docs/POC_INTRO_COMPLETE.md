# 관측 도입부 1~9 한글 삽입 — 014

2026-10-05 작업15의 [ROM](../build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes) / [IPS](../build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.ips)는 타이틀003·관측된 자연 도입부9문단·홈 초안을 포함한다. [다섯 문단 실제 화면](../qa/dialogue/intro014_actual_pages.png), [검증](../qa/reports/intro014_validation.json), [자산 식별](../manifests/intro_complete_assets.json), [현재 인계](HANDOFF.md)를 따른다. 54원천 중10draft/44untranslated이며 전체 게임 한글화 완료가 아니다.

넷째 이후의 네 줄 초대장, 익명 대부호의 서명, 버스터와 친구들의 반응, 악당의 웃음과 함정 예고를 원본 장면 및 인접 문단과 연결해 초안 번역했다. 글자수 때문에 의미를 삭제하지 않았으며 이름은 앞선 버스터 표기를 유지한다. おれさま/してやる를 근거로 초대장을 거만한 말투로 옮겼다. 서명에서 발신자의 정체는 밝혀 쓰지 않았다. 웃음은「후후후」, 마지막은「함정과 장치가 가득한 / 놀이공원에서 너희를 기다리마!」다. 최종 사람의 번역·명칭·말투 검토는 별도다.

## 원천과 구조 보존

추가된5원천은 MAIN_0568B/056C1/056EE/0570D/05718이다. 원문/raw/tokens/hash/reference/포인터와 이전49행은 보존했다. 단일 원천의 텍스트와 [삽입 계획](../workspace/translation/intro_complete_plan_001.json)이 일치해야 빌드한다. 전역 이름 macro81와 모든macro table/payload는 원본 그대로다. 각 문단의 전용font에서macro의5타일을한글또는빈칸으로대응한다. 첫편지에서는「버스터, 안녕」중터/쉼표/공백/안/녕을macro5타일에대응하고,반응문단에서는macro앞쪽여백과버/스를공급한다. 같은코드에다른글자를요구하면빌드가실패한다.

원래본문바이트수·모든FE/FD/FF/macro의위치와FD인수·줄별전개칸·literal00개수를유지한다. 공백의빠른분기횟수와원본reader호출별cycle/cursor/buffer_cursor도같다. 서명의FD0E는그대로유지하며의문의/대부호로부터를우측영역에놓는다. 물음표·느낌표·「」와숫자의원본glyph는보존한다. 쉼표만기존Galmuri7.ttf의8px/좌표(0,-1)에서명시적으로그렸다. 모든한글은기존atlas/TTF픽셀일치와NES2bpp왕복을검사한다. 빠진글자대체는없다.

| 원천 | 원래 줄별 전개 칸 | reader 호출/사이클 |
|---|---|---|
| MAIN_0568B |7/17/11/19|58/5959|
| MAIN_056C1 |24/18/24|69/5619|
| MAIN_056EE |23/16|41/3716|
| MAIN_0570D |16|17/1371|
| MAIN_05718 |15/24|41/4323|

기존CHR144KiB의6KiB padding에138~143,font3개를넣고추가8KiB중4KiB에144~147,font2개를넣었다. CHR152KiB/header13,PRG256KiB/ROM417808바이트다. 새font전체파일62810..65010,예약4KiB65010..66010(16진/끝제외). 013의기존font/타이틀/IRQ/ASM107바이트/helper bootstrap은불변이고font table의5바이트만추가로등록했다.48슬롯시간은013/008과정확히같다.

## 분리한 검증

immutable source에서6비중첩Expected Write를적용해전체ROM을재구성했다. 독립verifier는013전체에서5본문·table5값·font5개·CHR길이와padding만바꿔014전체와비교했다. 이밖변경0,전역macro변경0,새5행외CSV변경0이다. 이전첫째/둘째/셋째/넷째/홈의reader호출시간도원본과같다.

CPU1408조건에는13종C6 seed의624조건,공식6502 151opcode/mode·604벡터,ABI/flags/RAM/stack/mapper/2B복귀와고장004control거부가포함된다. Mesen콜드부팅에부트·원본변조없이controller만넣었다. 013/014 동일Lua/config/exe/input 비교2334표본에서현재문단의실제행밖차이0,홈492전체일치,palette/OAM/id/pointer동일이다. 각font실제PPU일치표본은138:271,140:289,142:340,144:139,146:153이다. 처음과자연반복의완성네임테이블을확인했고20초기화복귀의SP/mapper/2B가같다. 각새문단의초기화가자연반복에서2회씩관측됐다. 실제IRQ진입/쓰기41034시점은013과같으며1996값변경은font5A/5B→해당한글font만이다. Start1950(편지)와2760(마지막악당)경로를비교했다. 직접5원본장면과현재1980/2160/2400/2640/2760의한글을검토했다.

재빌드와깨끗한원본에IPS를한글·공백경로로실제적용한결과가014전체와같다. 정적과CPU검사가실행/시각검사를대체하지않는다. 모든검사는관측도입부범위이며게임전체플레이/오디오/실기/reset/savestate/RNG22영향을입증하지않는다.

## 재현

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_intro_complete.py --output build/dialogue_kr_poc_014_NEW
python scripts/verify_intro_hooks.py --build build/dialogue_kr_poc_014
python scripts/verify_intro_complete.py
python scripts/audit_intro_complete_session.py
python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/intro014_NEW --frames 6000 --script scripts/capture_intro_complete.lua
python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/intro014_IRQ_NEW --frames 2850 --script scripts/trace_intro_irq.lua
python scripts/dialogue_ips.py apply --source "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --patch build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.ips --output "qa/dialogue/한글 적용 014_NEW/intro_applied.nes"
```

새QA/빌드폴더이름을쓴다. Start경로는동일capture script에720/3000,1950/3600,2760/3600을지정한다. baseline은013이다. Mesen설정파일을공유하므로실행은순차로한다. 과거003/008/012/013검증과manifest는그때의CSV에묶였으므로현재10draft로재실행하지않는다. 역사적build/QA/스크립트/보고서와원본/1편을보존한다.

## 다음 작업과 계속 진행

도입font latch만으로홈/매표소/놀이기구대사를번역하지않는다. 실제홈IRQ는매프레임06EA profile을읽고FB34/FB35의fontpair로C6/C7을덮어쓴다. 다음은controller만으로메뉴/매표소/입장조건/스테이지설명에서원천ID와profile을연결한뒤한글font작업집합과공급방식을정한다. 44원천뿐아니라크레딧별도font와MONTANA LAND 등추가픽셀문자도전게임인벤토리에서확인한다.

2026-10-05사용자는별도지침이없으면멈추지말고계속진행하도록지시했다. 매작업인계와검증을마친뒤기록한한가지다음작업을곧바로이어간다. dist는비어있고외부게시/최종카페작업기는아직없다.
