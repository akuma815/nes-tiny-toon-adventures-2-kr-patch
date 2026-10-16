# 작업115 — 현재047의 V6 실제 충돌 순간

[검증 보고](../qa/reports/cart115_validation.json), [실행 환경](../qa/dialogue/cart115_v6collision047/environment.json), [실행기](../scripts/run_cart_collision115.py), [Lua](../scripts/trace_cart_collision115_v1.lua), [검증기](../scripts/verify_cart115.py). ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`, source SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d` 유지.

[작업114](CART_CONTACT_MOMENT_ANALYSIS.md)의 새 접촉 가설을 확인하기 위해 현재047을20000프레임 실행했다. Lua는 동결V6 전체 바이트 prefix에 읽기전용2F/player exec/RAM 관측을 덧붙였다. controller 이외의 게임RAM·ROM·PC·state·시간·체력·금액 쓰기는 없다. 새winning정책이나클리어성공을주장하지않는다.

기존89 현재046의 입력19999행과 해제4763행이 같다. 같은 시점의PNG/RAM/PPU/OAM/매핑4140파일도 같다. ROM별 SHA와 실제 환경을 따로 기록했다. 새 환경의 선언 파일 SHA를 전부 확인했다. native bank3A/3B의 CPU 주소9C9C/9D53 등과 PRGrelative `34000+(PC%2000)`을 guard해 UI·다른bank의 같은주소를 제외했다.

14000..19000의 실제 pair 검사4543회 중4375회는거리분기에서거절됐다. 실제168쌍은전후2KiB RAM과A를local D-clear CPU9D53..9D93으로재생해모두일치했으며두카트의X/Y8.8속도교환을확인했다. 작은zero fallback은2회실행됐다. NMI/IRQ/PPU전체재생은아니다.

올바른level1구멍중심224,464에대한168개의실제전달속도는구멍쪽77/반대88/0은3이다. 선언한20개16프레임해제창안의18충돌은구멍쪽11/반대7이다. NativeRAM52에서실제A해제상태도관찰됐다. 창시작의heading/충전량이접촉순간의속도와동일하지않음을확인했으며단일실패원인으로단정하지않는다.

특히18404..18420해제창에서player/2F의접촉이이어지며positive/negative속도를다시교환했다.17416..17432창의17421접촉은처음과달리기본방향벡터도반대였다. 저장된16프레임A해제는방향키를고정하지않고매프레임경로를다시계산한다. 이두현상을구분해다음단일정책수정여부를판단한다.

종료는기존89와같이첫구간통과/둘째마지막2F잔존/시간초과후홈이며Gold/history0이다. 자연전체3구간완주미달을그대로유지한다. 새빌드·적용·직접장면시각검토없음. 과거89의실제실패화면과같은시점PNG가byteexact라는범위이며이번에모든화면을육안검토했다는뜻이아니다. 원본/1편/047/CSV/기존증거보존,전역corpus·사람최종검토·실기·PCM청음·정식배포미완료/release_eligible=false다. 카페완성작업기는전체완료후작성한다.

재현은기존출력덮어쓰기없음:

```powershell
python scripts/run_cart_collision115.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/cart115_v6collision047 --frames 20000 --inputs config/menu_cart_001.json
python scripts/verify_cart115.py
```

변경파일은실행기/Lua/검증기/QA/보고서/본문서와오늘인계·journal·canonical문서다. [동결 manifest](../manifests/cart115_assets.json)에 SHA,source/1편/로컬링크감사는 `qa/reports/cart115_session.json`에기록한다.

다음 작업 하나: **실제18개burst 접촉의입력·기본방향·재충돌을시계열로분리해,첫구간을보존한단일방향유지수정이타당한지판정한다.** 새근거없이V6를다시실행하지않는다.
