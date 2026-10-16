# 작업76 — 원본8×16 재검토 / 실제 START! 누락 확인

[정적 모든128뱅크 도해](../work/graphics_population_003/source_all_8x16_static_2x.png)는 임의 분석색/스프라이트 배열이며 실제 게임 화면이 아니다. 기존8×8 도해와 함께 직접 재검토했다. [128뱅크 SHA/044보존 목록](../extracted/graphics/start_001/native_CHR_preservation_population.json)은 원본대비 기존 변경bank18/80/81/82/92/93/94/100/101/102를 기록하며 이미 채택된 타이틀/그림/CHR자료 변경이다. 이 목록만으로 소비나 전역미사용을 증명하지 않는다.

새로 START!를 확인했고 [actual2670](../qa/dialogue/notices075_natural044/frame_02670.png)를 직접 보니 놀이기구 시작 전 중앙 안내다. 타이틀 PUSH START 유지결정과 별개다. [소비/추출](../extracted/graphics/start_001/consumer.json), [원본 PNG](../extracted/graphics/start_001/start_original_8x.png): natural2636 RAM34에7A를 쓰는 nextPC A5FA/return_bank32,2670 actualPPU의0..7FF 및800..FFF가bank122/123 원본2KiB와 일치했다. 네임테이블48셀/48타일과3,072전체RGB 픽셀/인코딩왕복을 연결했다. 화면영역80,112..176,144이다. 번역 초안은 ‘시작!’이다.

native A5DB는6DE를읽어CFC2 인라인4포인터(A5E9,A600,A622,A628)를 사용한다. 포인터표를 코드를보듯선형해석했던 console 초반 출력은 기각했다. 실제 글꼴 생산자는 A5F6 LDA#7A/STA34, A5FA LDA#7A/STA35, BNE A61E/INC6DE/RTS. Expanded 두operand26607/2660B. 등록 본문45draft/9기술공유는 그대로이고 새 실제 그림 안내가 발견된 것이므로 전역완료를 주장하지 않는다.

기존 HOW TO CONTROL116/117·PAUSE120/121은 이전관측범위에서 소비미연결인 후보로 유지한다. **START는122/123**이며 이전116..121 ‘선택0회’ 검사가 START까지 포함한 것은 아니다. POW 효과/법적문구/사명이 기존 그림에 존재하지만 본문 번역과 구분하며 전역보존결정/미사용증명으로 확대하지 않는다. 알려진 실제 번역 안내는 타이틀/지도/매표소/HUD/보너스/게임오버/기차/시간초과/다음라운드, 새 START 대기다.

재현: `python scripts/extract_start_notice.py --output extracted/graphics/새폴더`는 보호된044/75 증거 SHA를 확인하고 read-only 재추출한다. [파일/해시 manifest](../manifests/start076_assets.json). ROM/기존CSV 변경0, 새빌드/적용/추가에뮬레이터실행은 이번작업에서없다. 자연 실행75 자료를 재사용했다.

다음 작업 하나: nativebitmap ‘시작!’과 새222/223뱅크/두 글꼴 상수로 빌드045를 만들고 실행·보호 범위를 확인한다.
