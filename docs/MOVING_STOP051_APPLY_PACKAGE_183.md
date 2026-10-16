# 작업183 — 수정051 ROM없는 적용묶음·실Windows 검증

[051 적용ZIP](../dist/TinyToonAdventures2_KR_Review_051_MovingStop_20261008.zip) SHA `ad3e033fd7094d6af57115e821386b01dfbbec13023bbca04fef102676e5a0bb` / [ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes) SHA `b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24`. 원본일본판→051 xdelta이며기존패치본에덧씌우지않는다. [사용법](../dist/TinyToonAdventures2_KR_Review_051_MovingStop_20261008/README_적용방법.txt), [19파일/적용검증](../qa/reports/moving_stop183_package.json). 변경파일의전체해시는manifests/nonplay183_assets.json 및묶음SHA256.txt 참조.

실Windows apply.cmd8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로 최종ZIP 추출본의apply.cmd→byte-exact051 PASS. ZIP CRC/파일목록/모든내용exact/적용후payload불변/ROM-free PASS. 원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d` 보존. 사용자적용050 ROM을포함한이전dist/원본/1편/사용자Mesen/설정/세이브는수정하지않았다.

moving_stop/의050/051 frame4200/4272 실제같은입력PNG,소비기록,최종집중검증보고를포함했다. tools/licenses/apply.cmd는173 고정기록의SHA와일치복사. PS1은패치명·패치SHA·결과SHA·버전표시만갱신했다. 기존049검토HTML은현재051로재명명하지않으며이ZIP에넣지않았다. scope_policy051은169/173의6원문유지선택을그대로보존하되전체CHR동일주장은이번수정에맞게제거했다. 글자58바이트외에는050 동일하며티켓교환수정177의PRG를그대로포함한다.

현재채택051. [작업182](MOVING_STOP_GLYPH_FIX_051_182.md)의정적/빌드/실제Mesen/직접장면검증과이작업의적용검증을구분한다. 사용자전체플레이/최종문구·명칭·그림검수는남는다. HUD 전놀이기구동일은사용자관측이고새전놀이기구실행검증을의미하지않는다. 카페완성작업기/외부게시없음.

실행: ZIP을풀고원본.nes를apply.cmd에드래그.051을새로열고초기화한뒤기차의고정정지뒤움직이는표지판을검수한다. 다른버전강제저장상태의호환/자동복구는검증범위아니다. 재현package: `python scripts/package_moving_stop183.py`는기존최종산출물재작성방지가있어현재경로에서재실행하지않는다.

다음 작업 하나: 사용자가 새051 ROM을 열고 초기화/기차 재진입 후 위아래로 움직이는 정지 표지판을 검수한다.
