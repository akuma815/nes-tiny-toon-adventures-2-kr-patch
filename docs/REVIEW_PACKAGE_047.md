# 작업93 — 현재047 ROM 없는 검토용 패치 묶음

[검토용 ZIP](../dist/TinyToonAdventures2_KR_Review_047_20261005.zip), [최종 적용 보고서](../qa/reports/review047_package_final.json), [한계/내용](../dist/TinyToonAdventures2_KR_Review_047_20261005/RELEASE_NOTES_KO.md), [사용 안내](../dist/TinyToonAdventures2_KR_Review_047_20261005/README_적용방법.txt).11파일/179814바이트ZIP SHA-2562908cd8e3b29ff7531846c4465884a2686a276f0b65c2620b3f12043384c0756. xdelta SHA99c93bebd94363dcaa3b8424424e5934c551b742e6a0097d60c90728e749d03b. 일본판262160바이트 원본SHAf41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d에서499728바이트047 SHA82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10을 만든다.

패키지/적용: xdelta3.2.0 실행파일·Apache2.0/Galmuri OFL 출처/해시를 1편 검증묶음에서 읽기 전용 복사했고1편 원천 해시 유지. 현재CSV/빌드047/동결 이전런타임 및90/91/92 검증을 확인했다. 한국어·공백 경로의 **Windows apply.cmd 실제8검사**, 최종ZIP추출 후 별도 재적용을 실행하고 ROM 전체 byte exact를 확인했다. 잘못된 원본·이미 적용한ROM·손상된도구/패치·기존출력·원본과동일출력경로 거절을 포함한다. 원본/패치/도구/결과 해시를 적용기가 검사한다. [적용 증거](<../qa/apply/2편 개발047 한글 공백 적용 검증 20261005_093/apply_verification.json>), [제작v2](../scripts/make_review_package047_v2.py). ZIP에는 ROM/폰트 PNG/TTF/에뮬레이터가 없다. 이전043/046패키지는 보존했다.

실패 보존: v1의 버전치환에서 과거80 검증상태상수046이047로 바뀌어 패키지쓰기 전 guard가 실패했다. v1과 [기록](../qa/reports/review047_package_v1_observation.json)을 보존하고v2는 해당 과거상수를046 그대로 확인해 통과했다. 이전게임/현재ROM은 변경하지 않았다.

에뮬레이터·직접게임장면은 이 패키지작업에서 다시 실행하지 않았다. 동일047 ROM의 [91 실제성입구](GATE_EDITORIAL_QA.md)와 [92 검토자료](TRANSLATION_REVIEW_047.md)를 연결했다.046 reset/state는 역사적증거, 신규047 reset/state·전게임완주·전역corpus폐쇄·실기·PCM청음·최종사람검토는 미수행이며 release_report의최종배포자격false를 유지했다. 카트2F 시간초과 실패를 공개용안내에도 숨기지 않았다. 네이버카페작업기는 전체완료후 작성, 외부게시 없음.

재현: `python scripts/make_review_package047_v2.py`는 기존패키지/QA를거부한다. ZIP을 새폴더에 풀고 `apply.cmd "깨끗한 일본판 원본.nes" "새 출력.nes"`를실행한다. [동결manifest](../manifests/package093_assets.json).

다음 작업 하나:현재047에서 골드4/일반50 입장성공과 일반49 거절 분기를 명시적 통화seed로 실행하고046과 비교해 성입구수정/넘김/성플레이 HUD의 회귀를 검증한다. 자연통화획득 증거와구분한다.
