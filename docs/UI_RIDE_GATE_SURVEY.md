# 기차·급류타기·성입구 소비기 — 작업24

ROM022와SSOT18draft36미번역은 변경하지 않았다. [조사보고](../qa/reports/ui_consumers022_survey.json),[실제화면](../qa/dialogue/consumers022_actual_contact.png),[성 오류 비교](../qa/dialogue/consumers022_gate_failure.png)를 보존한다.

홈 방향표9B94에서 이동경로를 읽고 controller-only coldboot로 방문했다. 왼쪽은급류타기,왼쪽/위는기차,위/위는성이다. 기차는slot20규칙/26제목/1D요금2,급류타기는21규칙/27제목/1D요금3이다.2000입력에서 티켓10→8/7차감/23숫자/2A출발을거쳐2600입력으로 진입절차를진행했다.2760의black/fade는플레이가능성이나완료증거가아니다.

성16환영/17골드4장/18부족/1A일반50장/1B질문/18부족/19인사의정상부족경로를관측했다. 성공분기는미검증이다. 상단fontRAM34=90과하단06F3=148의인코딩불일치를발견했다.017 native일본어와 비교한186표본의오류는실제대사행y168..191에있다. 정확한IRQ분할위치는다음실행시점trace로확인한다. 성문구는상단NMI font도고려해야한다.019/022이전QA는성미방문이며당시범위의PASS를전게임보증으로확대하지않는다.

v3 trace는phase/ride/headfont/activefont/caller를추가했으나숫자열3종의이름이틀렸다. 자료는보존하고보고서는rawRAM/native주소로해석했다. gold_tickets열=07F0(의미미확정),normal_tickets열=07F2(포인트일의자리),points0..2열=07D0..2(일반티켓)이다. 실제골드는07E0,일반티켓07D0..2,포인트07F2..6이다. 후속v4에서읽기주소/이름을수정한다. RAM/ROM쓰기나상태로드는없었다.

## 식별·재현

ROM022 `88dada01f379ca25abb9cee08793b372fbe9508ba6d1581b131c9d07ff90ba08`,CSV `1528501efb8983ff77b9514fd859a7a7cca91eb23eb5ca752132cd645c3fbcd6`,원본SHA불변이다. [기차 환경](../qa/dialogue/consumers022_train/environment.json),[급류 환경](../qa/dialogue/consumers022_water/environment.json),[성 환경](../qa/dialogue/consumers022_castle/environment.json),[017성 환경](../qa/dialogue/consumers017_castle/environment.json)은exe/Lua/config/입력/결과별SHA를담는다.

```powershell
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_022/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/consumers022_train_repro_next --frames 4200 --inputs config/menu_train_001.json --script scripts/trace_ui_consumers_v3.lua
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_022/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/consumers022_water_repro_next --frames 4200 --inputs config/menu_water_001.json --script scripts/trace_ui_consumers_v3.lua
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_017/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/consumers017_castle_repro_next --frames 4500 --inputs config/menu_castle_001.json --script scripts/trace_ui_consumers_v3.lua
```

원본/1편/이전산출물보존. 새CPU hook/빌드/적용변경검증은없다. 전체놀이기구/플레이·오디오/reset/savestate/실기·최종번역검토는미수행이다. dist비어있고외부게시없음.

다음 행동 하나: native9FF7 성상단font를148로맞추고017성전체화면/022다른경로/실제IRQ시점으로검증한다. 바로이어간다.
