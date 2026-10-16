# 홈·매표소·스테이지 글꼴 소비기 조사 — 작업16

2026-10-05 현재014 ROM은 변경하지 않았다. [조사보고](../qa/reports/ui_consumers014_survey.json)와기록된controller경로로대사원천/IRQprofile/화면을연결했다. [메뉴입력](../config/menu_tour_001.json),[매표소입력](../config/menu_ticket_001.json),[메뉴trace](../qa/dialogue/menu_survey014_tour001/menu_events.csv),[매표소trace](../qa/dialogue/menu_survey014_ticket001/menu_events.csv)를따른다. 원본/ROM/RAM변조없음. 과거coldbootwrapper는Start한번만기록하므로새run_menu_qa.py로전체button시퀀스와hash를환경에동봉했다.

홈profile00은C6font130/131과C7그림58/59,매표소profile01은90/91과102/103,카트설명profile02는90/91과116/117을사용한다. 도입부helper가9445에C6를5A로바꿔도홈IRQ가매프레임FB34/FB35를읽어C6/C7을다시쓴다. 도입table만확장해서는다른문단전용font가유지되지않는다.

| 원천/인덱스 | 실제관측맥락 |
|---|---|
|05741/0A|홈의자,어디로갈까?|
|0574D/0B|롤러코스터선택|
|05750/0C|쇼킹카트선택|
|05759/0F|수수께끼성선택|
|05762/10|매표소선택|
|05769/11|홈을떠나는인사|
|05777/12|매표소환영|
|05782/13|포인트를입장권으로바꾸겠다는안내|
|05794/14|포인트부족|
|05867/1F|카트적을튕겨구멍에떨어뜨리라는설명|
|058F6/25|카트제목|
|05833/1D|카트입장에입장권1장이필요하다는FA숫자|
|058F0/23|순수F9숫자출력|
|05920/2A|출발인사|

매표소의ポイントがたりないわ와보유0 POINTS를확인했다. A를누른13안내는교환성공증거가아니다. 초기10 TICKETS 표시,카트입장가격1은실제PPU문자와화면에서확인했으나모든가격/정상·골드보유조건을검증하지않았다. [매표소1620](../qa/dialogue/menu_survey014_ticket001/frame_01620.png),[부족2190](../qa/dialogue/menu_survey014_ticket001/frame_02190.png),[카트설명2310](../qa/dialogue/menu_survey014_tour001/frame_02310.png). 화자는보이는캐릭터와기능으로정하며임의의고유명을추가하지않는다.

## 글꼴 공급 설계와 소유권

C8는원본PRG에native read/write가있어새latch로쓰지않는다. 06F3은PRG의주소바이트F306자체가없으나indexed/indirect접근가능성을남기고실측했다. [tour v2](../qa/dialogue/ui_scratch014_tour_v2/menu_events.csv),[ticket v2](../qa/dialogue/ui_scratch014_ticket_v2/menu_events.csv)는read/write와PC를모두기록한다. 두경로에서frame2의FE40,frame3/261/592의CFB4 RAMclear/dummy-read만있고UI·카트진입후의접근은없다. 최초probe는같은값쓰기를필터링해clear-write를숨겼으므로v2에서06F3만전부기록하도록정정했다. 최초자료도보존하고v2를소유권판단근거로쓴다. 모든미방문게임코드의부재증명은아니다.

설계후보는native완성pointer의font를06F3에XOR5A로저장해0이원본90으로복귀하도록하는것이다. IRQ에서LDA FB34,Y를absolute latch load로바꾸고EOR5A로복원하며C7은06EA와원래table을유지한다. 중복PPU2002읽기직전에2006과2005두쓰기의latch상태가0임을확인한뒤그읽기를EOR/NOP시간으로재배치하면최종CHR쓰기시점을같게맞출수있다. 추가page/setup처리시간은기존padding을줄여동일하게맞춘다. 이설계는아직구현검증전이며PPUstatus/open-bus/latch side effects와실제IRQ시점·화면을새빌드에서확인해야한다. 원본고정bank의공유zeroasset을free cave로사용하지않는다.

## 남은 인벤토리

자연도입부뿐아니라MONTANA LAND,매표소TICKET BOOTH/NUMBER OF REMAINING TICKETS/YOUR POINTS/TICKETS/POINTS의별도그림문자도발견했다. 크레딧은Latin profile을실제연결해야한다.54원천중10draft/44untranslated는현재등록table기준이며전게임문자량완료를의미하지않는다. 03/04의기차·급류선택,정상/골드ticket부족·충족·성입장·교환성공,나머지스테이지와크레딧은계속관측한다.

```powershell
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/menu_NEW --frames 3600 --inputs config/menu_tour_001.json --script scripts/capture_menu_survey.lua
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/ticket_NEW --frames 3000 --inputs config/menu_ticket_001.json --script scripts/capture_menu_survey.lua
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/scratch_NEW --frames 3600 --inputs config/menu_tour_001.json --script scripts/trace_ui_scratch_v2.lua
```

**다음 작업 하나: 06F3 encoded font latch와홈IRQ복원코드를같은시간으로구현하고014와도입/홈/매표소/카트경로를비교검증한다. 사용자지시에따라곧바로진행한다.**
