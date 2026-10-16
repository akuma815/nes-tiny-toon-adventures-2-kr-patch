# 성 문단별 상단 글꼴 공급 — 027 / 작업28

성 대사를 문단별 한글font로 표시할 기반을 구현했다. 아직 성문구의 한국어는 추가하지 않았으며20draft34미번역/타이틀·도입·홈·선택·매표소는 그대로다. 새helper008은홀수번호로배정한custom font pair를상단RAM34에도공급한다. 기존원본/default/도입/홈·하단용font는모두짝수다. 성의일본어fallback은동일bitmap의171/172복제이며slots16..1C와alias2C에등록했다. 글꼴뱅크수에대한태그이지사용자화면에표시하는정보가아니다.

005의기존대기10cycles를각분기에서줄이고저장한동일pointer high07을사용해1cycle을줄였다. 글꼴번호복원·조건분기는양경로11cycles이며초기화총시간은모든48slots에서024와정확히같다. source매크로/본문/숫자/글리프·기존코드는보존하며helper전용으로이미할당한PRG bank2범위만사용했다. 새scratch RAM이나원본asset을빈코드영역으로간주하지않았다.

025/026의007은성+19cycles가NMI1077시점2cycles차이를만들어기각했다. [기각근거](../qa/reports/commit026_rejection.json)와실패ASM/빌드/모든캡처를보존했다.027은시간증가가없고실제시점비교도통과했다.

## 검증

[독립검증](../qa/reports/tag027_validation.json):원본ExpectedWrites7/중첩0와024전체이미지의helper135bytes·bootstrap/8tablefont·Japaneseclone2KiB외불변. CSV/원문/모든본문/기존font/제어/숫자불변. CPU1728phase·active·screenmode조건과[1504 ABI/720초기seed](../qa/reports/tag027_hooks1504.json),official6502 ISA604벡터/이전004실패대조가통과했다. 모든page정확히같은시간·레지스터/flags/SP/mapper를확인했다. 재빌드/실제한글·공백경로IPS적용동일.

실행2001전체화면픽셀/PPU/OAM같음:성474/자연도입848/메뉴390/매표소289. 게임RAM은fontlatch/상단34/NMI캐시3A와helper복귀주소가남은stack외같으며그font변경은성171↔148만허용했다. 도입·메뉴·매표소참조는022고정캡처이며현재본문/폰트동일성을정적으로입증하고새027을실행했다. 성참조는024새v4캡처다. v4는작업24의숫자명명오류를바로잡았다.

실제IRQ/NMI/PPU/mapper185067시점정확히일치(성69714/도입41034/메뉴37173/매표소37146),성font선택값3508만동일glyphclone으로달라졌다. [실제3장면](../qa/dialogue/tag027_actual_scenes.png)에서성1920/편지1980/매표소1680가독성을검토했다. 전체플레이·골드/일반충족·교환성공·성한글/상단card·영문그림/크레딧·전체corpus·오디오/reset/savestate/실기/최종번역검토는남는다. dist비어있고외부게시없음.

## 식별·재현

- 원본: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 027 ROM/재빌드/실제적용: `d9db24539a021723c42dd40c9b65d45bb59878226cc10349a862b5c06ffcd513`
- 027 IPS: `eb1e23c591bf5fc7cfdb94073bf469e3b26819ca293ce3be33bbbd3265e5fd21`
- 현재CSV: `d57b739152817572a0f1833572ca7991eb7684a77a1c00a2ef44931ee2c228fe`

ROM442384/CHR176KiB,분산된padding4KiB:bank170의1KiB와bank173..175의3KiB. [자산/해시](../manifests/gate_font_tag_assets.json),[세션감사](../qa/reports/gate_font_tag_session_20261005.json).

```powershell
python scripts/build_gate_font_tag.py --output build/tag027_repro_next
python scripts/verify_gate_font_tag_hooks.py --build build/dialogue_kr_poc_027 --report qa/reports/tag027_hooks_repro_next.json
python scripts/verify_gate_font_tag.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_027/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/tag027_castle_repro_next --frames 4500 --inputs config/menu_castle_001.json --script scripts/trace_ui_consumers_v4.lua
python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_027/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/tag027_intro_repro_next --frames 6000 --script scripts/capture_intro_complete.lua
```

고정verifier는현재20draft입력/027/명시된참조에적용하며후속SSOT변경후과거검사를그대로실행하지않는다. 기존PRG확장·난수의전게임동일성은보장하지않는다.

다음 행동 하나: 관측성16/17/18/19/1B의환영·골드4장조건·부족·인사·질문5문구를전용홀수font173..181로한글삽입하고일본어1A복귀/지우기/홈복귀를검증한다. 즉시진행한다.
