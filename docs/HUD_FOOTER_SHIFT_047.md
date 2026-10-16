# 작업124 — HUD 하단 두 줄의 실제 소비와 기존 배치 확인

[실행기](../scripts/run_bottom124.py), [읽기전용PPU추적](../scripts/trace_bottom124_v1.lua), [검증기](../scripts/verify_bottom124.py), [결과](../qa/reports/bottom124_validation.json), [기존 HUD040 설계](GAME_HUD_KOREAN.md), [기존 계획](../workspace/translation/game_hud_plan_001.json), [직전 RGB 한계](RIVER_ED_ACTUAL_CONSUMER_047.md).

## 새 실제 PPU 근거

원본/현재047의123과같은6필드진단을각3300프레임실행했다.새관측기는기록render3032의233..239에서PPU읽기각1190행,liveVRAM·NT값·physicalmapping·팔레트를기록했다. 추가게임상태쓰기는없다.동일ROM의기존123 snapshot과RAM/PPU/OAM/매핑·core를대조했고PNG예외여부도분리했다. 원본/047ROM과각읽힌pattern바이트를대조했다.

원본233/234는v=6FA2/7FA2,NT2FA2의공백20을font124에서읽는다.이tile의lowplaneFF/highplane00은색index1이며attributeFF의palette3/color1=0F로검다.235에는v=0402로다음네임테이블2402의tile00으로넘어가고,빈pattern0은universal색07(갈색)을출력한다.

현재235/236이그같은tile20의row6/7을font206에서읽고237에v=0402/NT2402/tile00으로넘어간다.정적font124의tile00/20은206에서도바이트그대로이며NT·팔레트도같다.5행에대해source/current의동일소비가2scanline아래로이동한pattern340행을직접대조했다.기본2C02공식팔레트와첫8픽셀backgroundmask를적용한독립색예측은실제PNG3033의각1792픽셀,합계3584픽셀과맞는다.

## 왜 ROM 수정이 필요하지 않은가

작업40은처음부터HUD소유범위를y190..239로정하고상단한글7행확보를위해2006high2F→0F,즉fineY2→0을변경했다.따라서본문/숫자/틀/하단여백을2픽셀아래로이동하는것이이미계획·검증된배치다.047의해당IRQ두operand도그계획과같다.이번하단235/236은그여백이동의실제소비다.

작업123의HUD제외사각형190..217은원본전체비교에너무좁았다.단순히제외범위를늘려통과시킨것이아니라기존선언소유범위·원본tile보존·livePPU소비·독립RGB모델을대조해이유를확인했다.기존123의50예외보고서는보존한다.상단게임화면동일·ED실소비성공과HUD의의도된배치차이를구분하며새ROM/글꼴/CSV수정은하지않는다.

## 인계

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지.새QA2실행/실행기/추적기/검증기/보고/본문서/인계·journal/canonical/manifest작성.원본/1편/기존실패성공QA보존.이번은실에뮬레이터읽기전용소비·정적기존계획·독립RGB대조이며새CPU사례·build/apply·직접PNG검토는없다.직전123의2실제PNG직접검토는그범위로유지한다.

이진단한프레임/7줄의원인설명이며모든장면·viewport·IRQ/실기를검증하지않았다.자연강후반/전체완주·ED자연팔레트·공통POW·전역corpus·사람최종검토·정식배포는미완료다.카페완성작업기는전체완료후작성한다.

재현은`python scripts/run_bottom124.py --rom <source또는047> --output qa/dialogue/새관측폴더`의새경로를쓴다.검증은복제본에새QA/보고서경로를명시하고기존동결출력을보존한다. [동결 자산](../manifests/bottom124_assets.json), 감사 경로 `qa/reports/bottom124_session.json`.

다음 작업 하나: 등록45본문초안을일본어원문·정확한장면105·현재삽입계획과수동대조해의미/용어/높임말을검토한다.실제수정이필요한문장만별도근거와함께선별하며사람최종승인을자동부여하지않는다.
