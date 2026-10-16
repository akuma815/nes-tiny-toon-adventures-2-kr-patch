# 작업164 — 자연 손잡이 소비 조건

[48CPU 검증](../qa/reports/water164_rope_model.json), [분석 재현](../scripts/analyze_seal_water164.py), [실제8430 RAM](../qa/dialogue/water163_held_jump049/frame_08430_ram.bin).

실제type2/ED 구조물은통나무가아니라로프/손잡이다. nativeB701은 playerVy비음수와target2의 X F0..10/Y EE..F4 충돌상자를검사한다. 성공은B749 INC C9와B74D STA0541=1이다.48원본/049 CPU쌍에서양성/음성을검증했다. 합성player좌표는CPU만사용했고실제QA RAM변경없다. 붙잡은뒤nativeB774는UP held에서상향,기본하향이며가로C0/256으로이동한다. 실제붙잡기/그후clear는미관측이다.163의type1-only 갈아타기조건은이손잡이를제외했다.

변경:164분석/보고/상세/인계/journal/canonical·manifest/audit.원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`,ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변.각산출물SHA는manifest. 정적/48CPU/실제fixtureSHA PASS.새runtime/직접PNG/build/apply/reset/state/청음/실기/사람최종없음.163 PNG비교실패/자연급류clear/全corpus/HOWTO/PAUSE/POW/정식배포미완료.재현은스크립트출력경로새이름으로복제.카페원고/게시없음.

다음 작업 하나: 실제type2 손잡이를 향한 A/우측 도약을 컨트롤러에 추가하고 C9/0541 native쓰기·입력전수·후반진행을 새049 실행에서 확인한다.
