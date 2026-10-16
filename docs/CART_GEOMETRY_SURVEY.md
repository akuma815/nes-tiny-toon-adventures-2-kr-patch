# 작업66 — 카트 구멍 판정 소비기 연결

[검증 보고](../qa/reports/cart_geometry066_validation.json), [실제입력/바닥관찰 실행기](../scripts/run_cart_geometry_qa.py), [관찰Lua](../scripts/trace_cart_geometry_v1.lua), [검증기V2](../scripts/verify_cart_geometry066_v2.py), [원본 소비기](../work/cart_geometry_001/native_consumers.json), [level0 분류표](../work/cart_geometry_001/native_level0_classes_v2.json). ROM/SSOT 변경0.

6,000프레임의새043 부팅에서 작업65와같은controller-only 정책을 실행하고, A274 실제 tile query 반환과16객체의좌표/타입/상태를 읽었다.12,105 실제질의의7,630 고유입력을 원본 DE91→DE26→DDC2·DE5E분류 코드의 오프라인CPU 실행과 비교해 전부 일치했다. 관찰된 level은0 하나다. 오프라인CPU의 scratch RAM 쓰기는 실제게임 개입이 아니다.

DE91는월드좌표를16픽셀 단위로 바꾸고 course1(level79) 테이블을 읽는다. level0의 class0F 구멍은 x112..143/y240..271, 중심128/256이며 네개의16×16타일이다. native9869..988D는중심주변 ±8 좌표 네곳이 모두0F일때0430=4 낙하상태로 전환한다. A051은구멍판정이 아니라속도0 여부검사다. 실제0430 상태4도 관측했다. 바깥영역도class0이므로 class0만보고임의좌표를바닥으로 간주하면 안 된다. 벽 안 연결성·관성·돌출물도 필요하다.

B입력은native970F의a1로보존되며9EFF 계열에서감쇠파라미터를8배로바꾸는 코드와 연결된다. 공식조작설명의명칭과 실제전체효과는 확정하지 않았다. 다른카트의최종제거/남은수·stage클리어 소비기와 자연클리어는 아직해결되지 않았다. 대상2E/2F 타입과제거판정은혼동하지 않는다.

첫검증은텍스트분류표의다자리값을눈으로읽어구멍열을한칸잘못예상한 assertion에서실패했다. [최초오류](../qa/reports/cart_geometry066_pit_coordinate_error.json)와 [최초검증기](../scripts/verify_cart_geometry066.py), [최초표](../work/cart_geometry_001/native_level0_classes.json)를보존했다. 실제질의 비교는 이미통과했고 V2에서정확한좌표로수정했다. 일회성disassembly끝9F31은STA중간임을경계검사로거부했고9F39 RTS까지로고쳤다. RTS 뒤의데이터표를명령으로채택하지 않는다.

재현: `python scripts/run_cart_geometry_qa.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 6000 --inputs config/menu_cart_001.json`. 고정runtime2,184파일·완료마커/환경SHA·actualquery와오프라인정적소비기연결을검증했다. 새scene육안검토·빌드/적용·청음/PCM·실기·자연완주·최종사람검토는 하지 않았다.

sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 원본·1편·모든이전성공/실패·검토패키지를보존하며외부게시없음.

다음 작업 하나: **확인된level0 벽 안의 구멍을 피하고 다른카트의 구멍 반대편으로 접근하는 관성 제어 controller-policy를 시험한다.**
