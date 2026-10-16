# 작업123 — 강 ED의 실제 OAM·CHR·PNG 소비

[실행기](../scripts/run_river123.py), [추적](../scripts/trace_river123_v1.lua), [검증기](../scripts/verify_river123.py), [결과](../qa/reports/river123_validation.json), [직접장면·RGB범위·좌표정정](../qa/reports/river123_scene_and_RGB_bounds.json), [원본 환경](../qa/dialogue/river123_projection_source/environment.json), [현재047 환경](../qa/dialogue/river123_projection_current047/environment.json).

## 실제 연결

원본/047각3300프레임coldboot에서3000프레임A5C6의69=0B/6D=F0두조건진단후,nativebank36/9582의actor2ED/state2/Y2투영직전에viewport68=01/6B=40/69=0C/6D=80을한번썼다.총6필드쓰기의이전/이후값·PC·실PRG를보존했다.원본이만든actor좌표와체력·시간·금액·phase·PC·ROM/save-state는수정하지않았다.진단카메라로실제소비를검증하며자연후반진행/완주와구분한다.

course3/ED의native9643조립을각1회확인했다.9sprites/36바이트OAM이nativeCPU모델과실제CPUshadow에같다.render_frame라벨3002의실제physicalCHR61 pattern읽기128행/288회는각ED tilepair의예상16회(공유tile은32회)와정확히같다.이는공통18/19 POW 소비가아니며EE/EF조립호출은이번관측0이다.모든선언runtime파일SHA와snapshot의mapped1KiB CHR도각사용ROM과대조했다.

원본/현재3003실제PNG를직접확인했다.9sprite의source패턴과실OAM에서구한518opaque픽셀(좌표범위X128..159/Y1..55)은둘다실제PNG의검정RGB와맞는다.EndFrame의spritepalette2는070F0F0F이며색글자가검정실루엣이된다.실제읽기·OAM·RGB를연결한이표본에서PNG3003이기록render3002와맞는것이고,모든캡처의지연을일반보증하지않는다.의도된자연장면의색상·물체명·POW번역/보존결정은이진단으로확정하지않는다.

## 좌표 정정과 RGB 비교 한계

작업122의RAM01=64/RAM02=144값과CPU조건/cycles는맞았으나sprite_x/y라벨및screen64/144표현의축이뒤바뀌었다.native9643은02를OAMx,01을OAMy에더한다.따라서실제anchor는**X144/Y64**다.기존122보고/문서는보존하고현재정정기록으로연결했다.

3003..3150의50캡처에서상단0..189 RGB는source/current같다.그러나기존HUD190..217만제외한비교는50장모두실패했다. 차이행은190..216과하단235/236이다.이범위를단순히확장해전체정상으로선언하지않는다.518 ED픽셀의성공범위와하단두행의소비조사를분리한다.기존원본/한글HUD차이와다른하단두행의실PPU·NT·scroll문맥은다음조사대상이다.

## 인계

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지.새QA두실행/실행기/추적기/검증기/결과/scene·RGB·정정/본문서/인계·journal/canonical/manifest작성.원본/1편/이전실패성공QA보존.이번은실에뮬레이터진단·3범위actual OAM/CHR/RGB 및제한된CPU조립대조이며새빌드/적용없음.직접검토2실제PNG/최종사람검토아님.전역corpus·자연전체완주·실기/청음·사람최종검토·정식배포는미완료이며카페완성작업기는전체완료후다.

재현은새출력경로로`python scripts/run_river123.py --rom <source또는047> --output qa/dialogue/새진단폴더`를사용한다.동결검증기는기존출력보고서를거부하므로복제본에새경로를명시한다. [동결 자산](../manifests/river123_assets.json), 감사 경로 `qa/reports/river123_session.json`.

다음 작업 하나: 원본/현재047의같은진단에서화면하단235/236의실제PPUpattern읽기·매핑·NT/scroll을추적해,HUD밖차이를정확한소비에연결한다.ROM/CSV변경전에원인을확인한다.
