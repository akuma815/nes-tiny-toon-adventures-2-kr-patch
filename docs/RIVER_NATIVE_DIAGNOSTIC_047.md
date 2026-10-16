# 작업121 — 강 native 후반 조건 진단, 실제 표시 미연결

[실행기](../scripts/run_river121.py), [추적](../scripts/trace_river121_v1.lua), [검증](../scripts/verify_river121.py), [결과](../qa/reports/river121_validation.json), [직접 장면 확인](../qa/reports/river121_scene_check.json), [원본 환경](../qa/dialogue/river121_source/environment.json), [현재047 환경](../qa/dialogue/river121_current047/environment.json).

원본과현재047을각4000프레임coldboot했다.3000프레임의physicalnativeA5C6에서root04/course03/phase05/actor2state0을확인하고RAM69의00→0B와6D의F5→F0을한번주입했다. 두쓰기·PC·실PRG·이전/이후값을기록했다.체력·시간·금액·진행phase·PC·ROM·save-state는수정하지않았다. **명시적조건진단이며자연강후반진행/완주가아니다.**

## 확인한 결과와 미달

두실행모두nativeA5FD1회/A6421회가실행됐고bank38=3D·actor2state2/artED를생성했다. physicalPRG차이를보정한native435행은source/current동일하다.그러나관측300프레임창의9643조립기에는ED/EE/EF호출0,physicalCHR61 actualpattern읽기0이다.생성직후소멸하는상태를확인했으므로**실제그림소비·표시성공으로보고하지않는다.** 이는POW전역미사용이나번역불필요판정이아니다.

현재047의개입전100시점(3000EndFrame포함)은역사적046/stop081_water046의RAM/PPU/OAM/매핑400파일·core100파일·전체PNG100장이정확히같다. 실제개입은3000EndFrame캡처뒤의A5C6callback에서일어났다.원본/현재각1083declared runtime파일SHA를검사했고모든snapshot의mapped1KiB CHR를각ROM과대조했다.해시/mapper일치는모든PNG의직접시각검토를뜻하지않는다.

현재047의3003/3030실제PNG를직접봤다.조건필드조작뒤강배경이이동한화면과현재게임HUD를관찰했다.정적120의ED/EE/EF그림이표시됐다고확정하지않았다. 이실험의조건쓰기만으로완전한후반게임문맥이재현됐다는주장도하지않는다.

## 인계

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`,현재047SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`,CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지.새QA/실행기/추적기/검증기/결과/scene기록/본문서/오늘인계·journal/canonical/manifest작성.원본/1편/이전성공실패QA보존.빌드/패치적용없음.이번은실에뮬레이터진단·기존정적근거대조이며새CPU사례는없다.직접검토는2PNG범위이고사람최종검토가아니다.전역corpus·자연전체완주·실기/청음·사람최종검토·정식배포는미완료며카페완성작업기는전체완료후다.

처음verify_source.ps1직접호출은로컬실행정책으로차단됐다.사용자정책을바꾸지않고별도프로세스의`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1`로원본검증PASS를받았다.원본/현재QA두실행은exit0이고Lua/assert실패가없다.

재현은새출력경로를사용한다:

```powershell
python scripts/run_river121.py --rom "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --output qa/dialogue/새원본폴더
python scripts/run_river121.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새047폴더
```

검증기는현재동결경로와보고서를사용하며기존출력을거부한다.재검증시복제본에새QA/보고서경로를명시한다. [동결 자산](../manifests/river121_assets.json), 감사 경로 `qa/reports/river121_session.json`.

다음 작업 하나: 현재047에서같은두조건진단에읽기전용actor2상태쓰기관측을추가해,ED생성후0422/0402를지우는정확한native명령·조건을찾는다. 위치·체력·시간·ROM추가조작없이기존121의동일시점RAM/PPU/OAM/매핑을대조한다.
