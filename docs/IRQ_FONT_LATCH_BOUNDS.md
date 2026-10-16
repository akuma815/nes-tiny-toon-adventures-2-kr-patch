# 작업103 — IRQ 폰트 래치의 원본/047 공급

현재047 ROM/CSV/검토패치를 변경하지 않았다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. 원본/1편/과거 증거 보존. [101 경계](PAUSE_SUPPLY_BOUNDS.md), [v2 분석기](../scripts/analyze_irq_latch103_v2.py), [보고서](../qa/reports/latch103_supply.json).

원본C6/C7 direct STA/STX/STY motif5곳 중 실제IRQ writer는source1FB25/1FB2A(nativeFB15/FB1A) 두 곳이다. source495C/4C9A는selector18/20의압축NT stream 내부이며1024셀 codec 경계와 함께 구분했다. source1037B의raw84C6은JMP84F1의 마지막operand84와다음DEC94의 opcodeC6이겹친것으로 instruction boundary가 아니다. 이는전체generic alias/실행CFG 폐쇄가아니다.

native06EA profile producer4곳을source/047 CPU로실행했다.9AF0 clear loop는profile0,9C90→9C95는1,9E0E→9E13은2,9FEA→9FEF는0이다. 각각전체RAM/레지스터/cycles가같다. 원본FB34의3쌍은5A3A/5A66/5A74, C6=90/C7=58·102·116이다.119/120/121이 없다. current047 table의첫바이트는과거003 home5A→82를보존한legacy값이다. 현재FB12는표의C6바이트를읽는대신AD F3 06으로active6F3를읽으며C7은원본표를유지한다.

현재047 등록48page의init9417을 인위prior latch0/120/121/255로실행한192조건에서C6=6F3=각slot font표의값으로초기화됐다.31개고유한글폰트값(128..201 중정의된값)에는119/120/121이없다. 이것은등록48 init경로범위이며임의state loading이나다른entry를전부검증한것은아니다.

source/current FB0D→FB31의IRQ slice를profile0..2×유효31font와fallback90=96조건쌍으로비교했다.52cycles·레지스터·A000/A008/B000/B008쓰기시점이같으며RAM차이는C6의90→active뿐이다. C7값과뒷배경2포트는원본같다. 전체IRQ/PPU/비동기실행을추가증명했다고부르지않는다. 기존전체IRQ/실제NMI시간검증은각동결작업에한정한다.

v1은현재표전체가원본같다고잘못가정해report전에중단했다. [실패기록](../qa/reports/latch103_v1_observation.json)/[v1](../scripts/analyze_irq_latch103.py)을보존하고v2는known003 legacy82와actual6F3소비를구분했다.원본/ROM/CSV수정없음. 재현 `python scripts/analyze_irq_latch103_v2.py`는기존보고서를거부한다. [동결자산](../manifests/latch103_assets.json).

이번은정적/CPU이며새runtime/build/apply/직접게임그림은없다. 여기까지한정된공급경로에서PAUSE를찾지못했으나다른indexed/indirect/computed공급·다른프로필·전역미사용/최종사람보존은미확정이다. 전역corpus/자연전체완주/PCM청음/실기/최종번역검토·공식배포/카페완성작업기도미완료다. 동등한부재관측을계속늘리기보다이근거를검토가능한결정자료로묶고다른완료조건을진행한다.

다음 작업 하나: HOWTO/PAUSE/POW의최신소비근거와정확한미해결범위를현재047 별도ROM없는검토보충자료로작성한다.
