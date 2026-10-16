# 작업180 — 상태창 왼쪽·아래 원본비교 조사

사용자가 실행화면 상태창 왼쪽과 아래가채워지지않는다고원본/패치여부확인을요청했다. 기술결론: 왼쪽8픽셀배경색띠/창아래검은여백은원본에존재한다.050새결함이아니다. 한글HUD를처음삽입한44에서fineY2→0으로내용을2픽셀아래로옮긴차이는별도로남아있다. 그래서아래끝배경색띠높이는이관측시점원본5픽셀/0503픽셀이며이전의큰여백을새로만든것은아니다. 글자높이7행확보용기존변경을누락이나완전동일로표현하지않는다.

[정적/실행 보고](../qa/reports/hud180_geometry.json), [실제 원본/050 확대 비교](../workspace/review/hud180/compare.html), [원본3000PNG](../qa/dialogue/hud180_coaster_source/frame_03000.png), [0503000PNG](../qa/dialogue/hud180_coaster_050/frame_03000.png). 같은격리MesenCE2.2.1·설정·controller로각3600프레임coldboot, seed/강제PC/세이브로드/RAM·ROM쓰기없음. 첨부이미지의후반갈색지형정확시점을복원한것은아니며같은롤러코스터HUD경로의서로동일한장면을대조했다.2880..3600간실제HUD7시점의왼쪽8픽셀RGB동일,全NT/attribute/palette동일,HUD위게임화면全RGB동일. 원본의검은여백20픽셀(y215..234)이050에서같은20픽셀(y217..236)이고bottomRGB가2픽셀shift로exact. 실제PPUMASK쓰기1896행의프레임/PC/값/scanline/dot도모두동일. source/current PPUMASK18·leftbg/spr disabled를확인했다. [NESdev PPU programmer reference](https://www.nesdev.org/wiki/PPU_programmer_reference#PPUMASK)는왼쪽8픽셀을숨길때배경색을표시함을설명한다. 해당지형이갈색이면띠도갈색으로보이는것은같은mask조건의palette에대한해석이며첨부프레임RAM은읽지않았다.

정적source HUD template D182..D281은050와동일. 원본fixed-bank fineY operand1FCE5=2F/current3FCE5=0F, fonte1FCF9=124/current3FCF9=206; 이는기존 [HUD44 검증](../qa/reports/game040_validation.json)의7행/2픽셀설계다. 현재ROM SHA `49b8e869a232657f88c1810c3319d0f79b0ee23dd1ed993cf2bfc1f48726dc25`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. [050적용ZIP178](../dist/TinyToonAdventures2_KR_Review_050_BoothFix_20261008.zip)도변경없음. 조사/보고/HTML만생성하며이요청으로원본디자인변경이나추가패치를하지않았다.

관측기록: 첫menu_cart경로와넓은2000..2006 observer는두실행모두exitFFFFFFFF/완료기록없음으로보존했다.원인확정이나게임결함으로닫지않는다. 첨부화면의롤러코스터경로로대상을명확히하고2001만관측하는v2에서두실행exit0/3600완료확인. 구사본을수정하지않고 [v2 runner](../scripts/run_hud180_v2.py)와 [v2 observer](../scripts/trace_hud180_v2.lua)를신규생성했다. 재현: `python scripts/run_hud180_v2.py --rom "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --output qa/dialogue/NEW_HUD_SOURCE --frames 3600 --inputs config/menu_coaster_001.json --script scripts/trace_hud180_v2.lua`;050는rom인자를현재050로바꾼다.기존출력보호. 시작source검증은ExecutionPolicy거절후별도 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1`로PASS했다. 정책영구변경없음.

변경:4runner/observer·verifyseal·네실행QA·HTML/JSON·dated/journal/SURVEY/PLAN/README/canonical/manifest. 정적/두v2에뮬레이터/직접실제PNG비교PASS. 새빌드/적용/청음/전게임완주/실제사용자live조회/최종사람검수/HTML브라우저시각검증 없음. 원본·1편·기존QA/현재Mesen·세이브는수정하지않았다.44의오래된증거는현050실행과구분했다. 카페완성글/게시없음.

다음 작업 하나: 사용자 실제 플레이 검수를 이어가며 새로 발견한 표시 문제를 해당 장면과 함께 기록한다.
