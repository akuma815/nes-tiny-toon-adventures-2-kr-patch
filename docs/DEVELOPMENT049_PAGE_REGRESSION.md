# 작업130 — 다른 page 경로 회귀와 개발049 채택

[실행원장/실행기](../scripts/run_pages130.py), [추가tour기준선](../work/pages130/tour047_supplement.json), [검증기](../scripts/verify_pages130.py), [결과](../qa/reports/pages130_validation.json), [직접 실제장면기록](../qa/reports/pages130_direct_scene.json). 작업128의재빌드/실제IPS적용과129부족·성공분기를바탕으로다른font소비경로를검증해 **dialogue_kr_poc_049를현재개발본으로채택**한다. 정식배포나사람승인은아니다.

새실행7회:049 title/intro6000·gate5400·tour3600·booth4500·credits9000,현재047 intro6000/tour3600 새기준선이다. 성입구047은동결091을, 매표소/크레딧은동결043을명시적으로재사용했다. 각짝의동일Lua/입력/seed/설정/에뮬레이터와모든선언파일SHA를확인했다. 크레딧은기존root18=7/19=1/selector07DF=1/phase06DE=0 네필드진단이며자연게임완료가아니다. 나머지는입력만이다. 모두exit0/원본·1편·실패성공산출물보존.

|경로|기준|같은 전체PNG/PPU/OAM/매핑|
|---|---|---:|
|타이틀/9도입문단|새현재047|51|
|홈선택/상단카드|새현재047|390|
|성입구|동결현재047|396|
|매표소|동결역사043|339|
|크레딧|동결역사043|327|

합계1503캡처에서전체픽셀/PPU/OAM/매핑이같고실제mappedCHR12024조각은049 ROM과같다. Intro의9font128/132..146과반복도입, 다른native slot/포인터/화자창, credits2D/2E/2F소비를확인했다. 직접실제PNG8장을봤다. 타이틀720·도입부분1680/완성1800·성입구1920·매표소1860·크레딧2400/4500을확인했다. 7500은실제검정화면일뿐이며엔딩완주로해석하지않는다.

처음tour기준039와의그림/OAM은같았지만rawPPU19개가달랐다. 이전빌드차이를제외범위로숨기지않고새047tour를한번만추가해,현재047과049의PPU전체가같음을확인했다. 기존039비교/원장을보존하고최종tour분모에는새047만쓴다. 매표소/크레딧의043증거도현재047로이름을바꾸지않았다.

RAM22와idleCPU A/flags·저장stack/bus는변경된다. 성16/tour1 snapshot의cpu.pc와저장1FE값차이는동일nativeFE53..FE5E 대기loop의opcode/operand microcycle과그loop의IRQ복귀주소로한정된다. 나머지state키(총cycle·SP/X/Y·PPU/APU/mapper 등)·보호RAM은같다. 이는정확한전체CPU상태또는모든실IRQ쓰기timestamp동일성이아니다.38cycle추가/19주기와가중counter모델은128/129의한정근거로유지하며자연전게임RNG동일성을주장하지않는다.

현재049 ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, IPS `01a78be85a8a3a007ba45d039275b0f5fd231b0096b830e75ac28f33f66edbc9`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`.049 499728B/PRG256/CHR232/45초안·9기술공유.047은역사개발본,048은전환거부본으로보존하며검토047자료는그때문구와이미지다.

변경은실행기/원장·7실행QA·검증/직접시각기록·본문서/인계/journal/canonical/manifest다. 정적/실runtime·보호state/CHR/pixel·직접시각검증이며새build/apply/CPU사례는이번없다.128의11파일재빌드/실제한글경로IPS적용을연결한다. 전역corpus/HOWTO·PAUSE·POW남은소비/자연전체·실기·PCM·최종사람문체명칭그림/정식배포미완료.카페완성작업기는전체작업후작성한다.

재현은실행기의새경로복제원장으로각동결Lua/입력/seed를그대로쓴다. `python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새intro --frames 6000 --start -1`. 기존QA/보고서출력거부. [동결자산](../manifests/pages130_assets.json), 감사경로 `qa/reports/pages130_session.json`.

다음 작업 하나: 채택049의단일본문수정·새실제화면·검증한계를반영한ROM없는검토자료를새폴더에작성하고047자료는역사본으로보존한다.
