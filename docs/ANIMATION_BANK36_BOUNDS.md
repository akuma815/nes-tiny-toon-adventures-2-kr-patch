# 작업102 — animation bank36 간접 표의 경계

현재047 ROM/CSV/검토패치를 변경하지 않았다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. 원본/1편/기존 증거 보존. [101 후보](PAUSE_SUPPLY_BOUNDS.md), [분석기](../scripts/analyze_animation_bank102.py), [보고서](../qa/reports/animation102_bank36.json).

sourcePRG10010..14010/nativebank38(hex)의803C와9362에서 RAM36으로 공급되는 두 간접표를 연결했다. 현재047에서 같은창은30010..34010이다. 이창의CPU9417은 표데이터이며 대사9417이 있는 다른PRG창과 혼동하면 안 된다.

803C는RAM25가0인지 아닌지로803F pointer 두개8043/804B를 고른다. native8015의0440 AND03 경계로 각4개의2바이트 pose/font쌍을 사용한다.8개 정의는 font8/9/24다. RAM25를0..5,phase0..3으로 native801D→803E를 source/047 각각24조건 실행했다. pose0400·bank36·전체RAM/레지스터/stack/cycles가 같다.

9362는0722 mode0/1의93F0 pointer93F4/9417와0441*5를 사용한다. native92D6은X=1을 지정하고 변신모드0721이 켜지면delay0451의3단계마다0441을 증가한다. CMP07 이전0..6이7record 경계이며 마지막에는0722를EOR01하고mode/phase/delay를 초기화한다.14record의font는12/13/14다. actor1pose·font·actor0pose·좌표 raw 오프셋을 보존했다. native9341→9364의14조건과 전체92D6→RTS의mode2×phase7×delay3=42조건을 source/047 비교했다. 전체80조건쌍 RAM/레지스터/stack/cycles가 같다. 마지막전환에서font를다시쓰지않은인위초기값0도 실제요구font처럼세지 않았다.

이 두 정의된 표는PAUSE120/121을 공급하지 않는다. 같은주소의 다른뱅크·다른indexed표·out-of-range임의caller를 닫지 않았다. CPU P30/Dclear, 비동기IRQ/PPU없음, 실게임에서모든조건도달·표시를 주장하지 않는다. 새runtime/빌드/적용 및 직접실게임그림검토는 없었다. 전역미사용·최종사람보존·전역corpus/자연전체완주/PCM청음/실기/최종번역검토·공식배포/카페완성작업기는 미완료다.

재현 `python scripts/analyze_animation_bank102.py`는 기존 보고서를 거부한다. [동결 자산](../manifests/animation102_assets.json). 정적해석과 nativeCPU 소비/transition의정확한 경계를 함께 남겼다.

다음 작업 하나: sourceC6/C7 IRQ 폰트 래치의 producer와 값범위를 추적해PAUSE120/121 공급 후보를 구분한다.
