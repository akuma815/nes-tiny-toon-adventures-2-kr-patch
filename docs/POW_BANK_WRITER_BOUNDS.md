# 작업98 — bank38 직접 writer와 잘못된 그래픽 뱅크 후보 배제

현재047 ROM/CSV/검토패치를바꾸지않았다. ROM82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10/CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556, 원본/1편/과거증거유지. [분석기](../scripts/analyze_pow_bank_writers098.py)/[보고서](../qa/reports/pow098_bank_writers.json).

원본PRG의STA/STX/STY zero-page38 literal motif15곳을모았고각site에서앞선고정load/연속store를정확히재현했다. source/04730개CPU slice는레지스터·전체RAM·cycles/최종bank값이같다.15곳모두고정값이며61은이미확인한3site뿐이다. 한site는LDA7E→STA36→STA37→STA38 연속열이라직전2바이트만load로가정하지않았다. exact absolute/indexed base34/38 motif4개는없었다. 이것은generic indexed/indirect writer·다른base alias·전체코드reachability 폐쇄가아니다.

후보배제: 기존96에서bank61을가정하면POW조각으로보이는common frame9C..A3가있었다. native마지막장면BC68 constructor는RAM34..39를56/58/52/53/**54**/55로만든다(source04730cycles exact). nativeBBBA의counter0..5/CMP6→ADC9D→STA0400,X는9D..A2를출력한다. actor0..11×counter0..5/source047144CPUcase로frame·delay8·counter+1·전체RAM/cycles exact를확인했다. 실제caller는bank54 불꽃이며bank61 POW의증거가아니다.9C초기와A3깜박임단계는구분했다. [원본같은pose/다른bank 정적그림](../work/pow_writer_098/bank54_61_same_pose_static.png)을직접봤다. 인위팔레트/좌표의설명그림이고실제게임화면이아니다. [재현렌더러](../scripts/render_pow_bank_alias098.py)/[독립동일PNG](../work/pow_writer_098/bank54_61_same_pose_rebuild.png)는byte exact다. 마지막장면의실제역사적소비는 [52](ENGINE_CLOSURE.md)에한정한다.

menu8F/stage가설course0-ED/게임오버3E의native조립source047 비교도cycles/OAM이같다.8F는69/6B,ED는47/51/73등다른타일이며3E는81/83깃발이다. 스테이지C0..FF에는96의common-only descriptor표를쓰면안되고native다른selector로검증했다. 초기배치만으로스테이지전수actor/실제POW미사용을증명하지않았다.

새게임runtime/재빌드/apply없음. 실제source61깃발positive control은 [97](BANK61_POSITIVE_CONTROL.md)이며POW소비는아직미연결이다. 같은조건의zero실행을추가로반복하지않고다른미해결영문후보의consumer분석으로옮긴다. POW전역미사용·번역/보존최종사람결정·전게임완주·전역corpus·실기·PCM청음·최종사람검토·카페완성작업기·외부게시를주장하지않는다.

재현: `python scripts/analyze_pow_bank_writers098.py`는기존보고서를거부하며 `python scripts/render_pow_bank_alias098.py --output work/새그림.png`로설명그림을재현한다. [동결manifest](../manifests/pow098_assets.json).

다음 작업 하나: source HOW TO CONTROL116117/PAUSE120121의소프트웨어bank producer와nativeNT 참조를역추적해실제표시가능한분기·문자tile주소를좁힌다.
