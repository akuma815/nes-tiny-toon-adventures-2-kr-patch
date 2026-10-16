# 작업69 — 카트 구간 완료 분기·포인터

[원본CPU 검증보고](../qa/reports/cart_clear069_validation.json), [검증기V2](../scripts/verify_cart_clear069_v2.py), [명령/분리된포인터표](../work/cart_clear_001/native_branch_and_tables.json), [이전 actual타입읽기](../qa/reports/cart_enemy068_validation.json). ROM/SSOT변경0이며이번에는실제에뮬레이터/RAM 개입을하지 않았다.

native9540은042D/042E/042F를OR하고모두0일때만플레이어0430=5·0550=0·56/0725 증가를실행한다. 세슬롯에0/1/2D/2E/2F와상태0/3/4/5를대입한오프라인원본CPU500사례를검증했다. 이미state5이면중복증가하지 않는다. 실제타입읽기루틴은작업68에서관찰됐으나allzero분기는아직자연플레이하지 않았다.

9564 JSR CFC2 다음9567의12바이트는6개포인터데이터다. state5는9CD0이고,그곳9CD3 CFC2 다음9CD6의8바이트는4개하위상태포인터9CDE/9D3F/9D74/9D8F다. 데이터부분은명령으로판독하지않았다.9D8F는0306의80/AC command 대기가끝나면79 구간값을증가시키고0→1/1→2에phase0E(hex),2→3에phase14(hex)로넘긴다. 보고서JSON phase_after의14/20은십진수값이며hex0E/14와같다. 즉3구간모두끝나야최종phase14에들어간다. 최종bonus phase20(hex)와혼동하지 않는다. 구간전환3사례와command80/AC 대기6사례를원본CPU로검사했다.

첫검증의disassembly끝9DB6은9DB5 LDA #C5 중간이었다. 경계assertion으로거부했으며 [실패기록](../qa/reports/cart_clear069_disassembly_boundary_error.json), [첫스크립트](../scripts/verify_cart_clear069.py)를보존했다. V2는9DBA RTS 다음9DBB까지이고통과했다. 실제ROM수정이나관찰오류회피가아니다.

재현: `python scripts/verify_cart_clear069_v2.py`(고정출력은재실행으로덮어쓰지않는다). native동일bank38/39 코드모델을사용했다. CPU모델은실제PPU/NMI/게임완주가아니며오프라인fixture와실제게임seed를구분한다. sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

새빌드/적용·runtime·직접시각·PCM/청음·실기·자연클리어/완주·최종사람검토없음. 원본/1편/기존성공·실패/검토패키지보존·외부게시없음.

다음 작업 하나: **구간별원본지형을추출하고남은적을향한완전충전/예측조작으로실제구간전환을시험한다.**
