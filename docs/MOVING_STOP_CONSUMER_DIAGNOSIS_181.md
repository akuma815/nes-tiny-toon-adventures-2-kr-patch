# 작업181 — 움직이는 STOP 별도소비 진단

사용자 설명: “처음 정지 표지판이 몇개 지나간 후 위 아래로 움직이는 표지판이 Stop으로 번역 안되어 있었다.” 라운드 분기 문제가 아니라 **고정 배경과 움직이는 스프라이트의 서로 다른 소비 경로**다. 고정 STOP은 이미224/225에 ‘정지’가 있으며050의 첫 세 표지판 실제 화면에서도 확인했다. 움직이는 표지판은별도CHR46 원문 STOP을 사용한다.

실제 소비: OAM 8×16 코드69/6B/6D/6F/71/73,24×32의6셀. native frame4200의 PPU1400→CHR0B800(46), PPU1680..173F→local40..51, 원본 파일2B810/확장파일4B810의같은원문그림. [소비 기록](../extracted/graphics/moving_stop182/consumer.json), [050 실제 화면](../qa/dialogue/moving_stop181_050/frame_04200.png). RAM36의 일반캐릭터폰트만으로Sprite1000..1FFF 전부를추정했던CHR22 후보는오판이며분석PNG로만보존했다.

조사/실패: 최초runner181은고정176 host SHA 불일치로실행전중단. 현재사용자host를새전용tools/mesence_user181로복사해V2로재현했다. 사용자세이브복사11 재생은다른카트미니게임(root4/course1)이라STOP 재현에쓰지않았다. 첫고정표지판용cold run도오른쪽이동이없어움직이는구간까지가지않았다. 기존042 캡처는후보발견에만쓰고현재수정검증에는쓰지않았다. 실패/오관측파일을그대로보존했다. 저장상태사용여부의기존질문은사용자의움직이는표지판설명으로대체됐으며원인을사용자세이브로돌리지않는다.

HUD: “전체 놀이기구 화면에서같다”는사용자검수결과로기록. [작업180 원본 비교](HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md)의왼쪽띠/아래여백 원본구성,한글HUD2픽셀이동을구분한다. 새전놀이기구실행검증으로확대하지않으며이번HUD수정은없다.

정적: source/050 CHR46 동일,고정표지판224/225 보존. 실행:5000frame controller-only coldboot,오른쪽+B 및점프,강제상태복원/생명seed/PC/RAM/ROM쓰기없음. frame4134..의움직이는원문 STOP 확인. 원본과050 첫고정표지판은별도cold실행으로관측. 전체플레이나직접사용자Mesen 메모리접속은하지않았다. 사용자실행중Mesen/설정/원본/세이브/1편은수정하지않았다.

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`;050 SHA `49b8e869a232657f88c1810c3319d0f79b0ee23dd1ed993cf2bfc1f48726dc25`. host/상태SHA와복사출처는qa/issue181_user_stop/provenance.json 및host_provenance.json,전체QA 해시는manifests/nonplay181_assets.json 참조.

재현: `python scripts/run_moving_stop181.py --rom build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/NEW_STOP050 --frames 5000 --inputs config/moving_stop181_train5000.json --script scripts/trace_moving_stop181.lua`. 출력은새경로를쓴다. 사용자신고대상집중재현이며자동완주실험은아니다.

다음 작업 하나: CHR46 움직이는표지판의글자영역만정지로삽입하고동일입력재현을비교한다.
