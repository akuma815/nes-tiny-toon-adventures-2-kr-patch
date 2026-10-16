# 작업146 — 현재049 쇼킹 카트 실제 reader

[최종 검증](../qa/reports/cart146_validation.json), [직접 화면](../qa/reports/cart146_visual.json), [실행계획](../work/cart146/run_plan.json), [검증](../scripts/verify_cart146.py).

현재049/새047을각4500프레임기존짧은menu_cart 입력으로실행했다. 동결142 reader관측기와검증기반을재사용했고RAM seed/state load/ROM write가없다. 기본티켓10장에서요금1장차감으로9장이되며현재root4/phase5/course1의첫카트구간플레이를확인했다. 실제게임스냅샷85개다. 117에서닫은winningbot/완주/후반구간실험을재개한작업이아니다.

339 wholePNG/PPU/OAM/mapping exact/2712CHR chunks currentROM exact. PRG data read142건씩의주소·값·PC·프레임·순서·문맥동일.100 cycle동일/27건+38/15건+76. helper18 writePC의같은STA byte확인·RAM22/IRQstack/A·flags·bus차이유지. 전체CPU/매IRQ시각/RNG/오디오동일성은주장하지않는다.

main1F(MAIN05867)설명/main25(MAIN058F6)제목/macro85(MACRO061DE)카트명전체원천byte를실제읽기주소로연결했다. native0C선택→1F/25상단→1D요금→2A출발과정의font193/196수명이유지된다. native-reader모델의titleNT20A6/rules2125·2165/depart22A8전체줄완성확인.1710설명/요금1·2070출발·2790초기게임·4500첫구간4PNG를직접검토했다. 현재RAW입력원천은기존130에서쓰던문구/그림과같고,이번차별점은실제reader·원천byte·font·NT연결이다.

변경: prepare_cart146.py/run_cart146.py/verify_cart146.py/seal_cart146.py,work/cart146계획·log,qa/dialogue새047/현재049,최종/직접시각보고서,상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README·manifest/audit. 실제재사용142 observer/verifier및config/menu_cart_001.json도동결SHA에포함. 신규실패없음·원본/1편/역사증거/ROM/CSV보존. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`.

정적/해시/controller-only runtime/실제reader/whole영상/선택4PNG 직접 PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_cart146.py`, `python scripts/run_cart146.py`, `python scripts/verify_cart146.py`;기존출력거부. 첫카트구간이상/자연전체완주/globalcorpus/HOWTO·PAUSE·POW/사람문체·명칭·그림최종/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

다음 작업 하나: 현재049/새047에서RAM seed 없는기본10장 롤러코스터메뉴·요금·출발경로를실행해,MAIN05849(rule1E)/MAIN058F2(title24)의실제reader/전줄NT완성과초기게임폰트수명을연결한다.
