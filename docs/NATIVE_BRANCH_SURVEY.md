# 정상 조건 분기 조사 — 작업30

028 c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e과25draft/29미번역 SSOT는 변경하지 않았다. [조사 보고](../qa/reports/branch028_native_survey.json), [원래 숫자 판정 CPU24건](../qa/reports/branch028_native_cpu.json), [실제 화면](../qa/dialogue/branch028_actual_contact.png)을 보존한다.

입장권을 모으는 긴 플레이를 대체한 진단이다. coldboot frame1000에서 지정 RAM만 한 번 변경한 뒤 기록된 컨트롤러 입력을 공급했다. 일반 플레이·자연 수집·전체 플레이의 증거로 주장하지 않는다. 새로운 run_branch_seed_qa.py/trace_branch_seed_v1.lua는 seed 원천·해시·주소·시점·PC·CPU cycle·변경 전/후값을 저장하고 c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e쓰기/상태로드를 하지 않는다. 기존 controller-only runner와 분리했다. API는 [Mesen2.1.1 공식 Lua 문서](https://github.com/SourMesen/Mesen2/blob/2.1.1/UI/Debugger/Documentation/LuaDocumentation.json)의 write(address,value,memoryType), nesDebug를 확인했다.

| 조건 | 원래 게임의 결과 |
|---|---|
| 골드07E0=4 | 2107에1C 입장 허가, 일반10장 유지, 골드4장 유지 |
| 일반07D0..2=[0,5,0] | 3007에1C 입장 허가, 50장→0장 차감 |
| 일반07D0..2=[9,4,0] | 부족18로 돌아감,49장 유지,1C 없음 |
| 포인트07F2..6=[3,0,0,0,0] | 3점→0점, 일반10→11장, 성공 인사15, 부족14 없음 |

원본9A48은 성 요금50을 일반 티켓 3자리에서 차감한다. 원본9A1D는 포인트3점을 판정한다. 0/1/2/3/9/10/49/50/51/99/100/999의24개 CPU호출에서 원본과028의 cycle/register/flags/결과가 같다. 골드 분기는 A0A2의 CMP4가 정확히4인지 검사하는 코드다. 선형 disassembly JSON에는 데이터/중간 instruction 시작도 포함되므로 유효 코드의 증명으로 전체를 쓰지 않았다.

성 입장 뒤22규칙/28제목/23잔여숫자/2A출발이 소비된다. 골드4 QA의6000 프레임에서는 성 내부와 조작 캐릭터·HUD를 확인했다. 이것은 seed 후 진입한 게임 상태의 화면이며 공략·완주 검증은 아니다. 가격1A의 FA는 두 자리 원래 숫자50을 출력한다. 일반50 QA의3060 화면은 입장 허가 후 암전이며 허가 글리프의 시각 증명으로 사용하지 않았다. 허가1C 실행 이벤트와3024완성 NT를 별도로 확인했다. 골드 허가2160과 매표소 성공1920의 실제 일본어를 직접 확인했다.

원본 SHA256 `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`;028 c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e `c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e`;2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8 `2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8`. 새 원본·빌드·IPS 수정은 없으며 새 재빌드/적용 검증을 수행했다고 주장하지 않는다. 모든 기존 산출물 보존. 추가입력/seed/환경/결과는 [보고서](../qa/reports/branch028_native_survey.json)와 [자산](../manifests/branch_native_assets.json)에 연결했다.

```powershell
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_028/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/branch028_gold4_repro_next --frames 6000 --inputs config/menu_castle_001.json --seed config/gate_gold4_seed_001.json
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_028/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/branch028_points3_repro_next --frames 4500 --inputs config/menu_ticket_001.json --seed config/booth_points3_seed_001.json
```

다음 행동 하나: 원래 FA 숫자를 유지하는 컴파일러로 성 가격1A와 허가1C를 한글 삽입하고 부족/충족/성 카드 복귀를 비교한다. 바로 진행한다.
