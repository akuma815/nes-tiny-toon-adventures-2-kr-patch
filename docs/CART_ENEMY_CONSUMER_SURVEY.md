# 작업68 — 적 카트 낙하·제거 소비기

[검증 보고](../qa/reports/cart_enemy068_validation.json), [기본 관찰기](../scripts/run_cart_enemy_qa.py), [좁은실행추적V2](../scripts/run_cart_enemy_qa_v2.py), [타입읽기V3](../scripts/run_cart_enemy_qa_v3.py), [검증기](../scripts/verify_cart_enemy068.py), [실제로실행된명령](../work/cart_enemy_001/executed_native_instructions.json). 세새부팅6,000/4,200/4,200프레임 모두같은A충전controller 경로이고 실제RAM/ROM/PC/state/reset개입은없다.

slot14/type2E가4033프레임 canonical3A/9B43에서043E=4로낙하한다.4065에는996B JMP AE3F가실제실행되고 AE3F 이하에서0400/0410/0420/0430 및좌표/속도배열을초기화한다.042E=0 쓰기와이후비활성·type0이연결돼 실제제거임을확인했다. slot15/type2F는남는다. 스프라이트040E/F=0만으로제거를판정하면안 된다. 여러animation writer가type·활성상태를유지한채sprite만0으로만들기때문이다. 앞선작업67의한적제거관찰은이번타입·활성·전체clear연결로확인했다.

3,451쓰기의9D STAabsX/99 STAabsY/FE INCabsX/DE DECabsX opcode·피연산자·실제X/Y주소를검증했다. RMW old값 dummy쓰기와최종±1은구분했다. frame4030..4070/X14의4,520실행주소는463고유명령으로보존했다. 이는실제CPU실행주소이므로CFC2 inlinepointer 데이터를선형명령으로판독한것과다르다.

5,961고정runtime파일과기존66의2,898 RAM/PPU/OAM 파일바이트가같다. rawmemory 보존이며오디오/모든PNG 동등성 주장은아니다. 타입영역bus read를51집계행으로기록했다. 이중absolute/indexed LDA/ORA의실제피연산자소비와dummy bus read를구분해야한다. 일부RMW/다른배열index의dummy주소도0420영역에온다.

실제bank38/9540은042D LDA,042E/042F ORA로남은세슬롯타입을검사하고모두0일때플레이어0430=5·0550=0·56/0725증가로이어진다. 이읽기는본경로에서관찰됐다. 다만allzero분기와그뒤stage/보너스는아직자연실행하지않았다. 전ROM의042F 정적검색에는다른성/boss후보 BF0E도나오므로카트consumer로채택하지않았다. 다음은이 실제cart소비기의branch와CFC2 pointer를별도해석한다.

재현:각실행기에 `--rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 6000`(V2/V3는4200) `--inputs config/menu_cart_001.json`. 기존출력덮어쓰기금지. `python scripts/verify_cart_enemy068.py`는세환경/SHA/실제op·rawmemory를검증한다. 중간로그를너무많이출력한일회성조회는이후집계/개수로제한했다. 조사중CFC2 다음inlinepointer를일회성console에서명령형태로출력한부분은채택하지않았다.

ROM/SSOT변경0. sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 정적·actualread/write/exec·corememory검증을구분한다. 새직접시각검토·빌드/적용·PCM/청음·실기·자연클리어/완주·최종사람검토는없다. 원본·1편·이전성공/실패·검토패키지보존/외부게시없음.

다음 작업 하나: **실제9540 남은적 분기와state5→stage/보너스소비기를 원본코드로검증한다.**
