# 작업55 — ROM 없는043 검토용 개발판 패키지

[ZIP](../dist/TinyToonAdventures2_KR_Review_043_20261005.zip), [실제 Windows/최종 ZIP 검증](../qa/reports/review043_package_final.json), [패키지 안내](../dist/TinyToonAdventures2_KR_Review_043_20261005/RELEASE_NOTES_KO.md).

**검토용 개발판0.1.0-review043**이며 최종 배포본/릴리즈 후보가 아니다. 작업 범위의 사람이 읽는 최종 번역 검토와 전체 자연 플레이는 아직 끝나지 않았다. 이 패키지는 요청한 사용자의 검토를 위한 로컬 산출물이고 외부 게시하지 않았다. draft를 배포적격으로 바꾸지 않았다.

원본/43 ROM/SSOT는 변경하지 않았다.11파일은 xdelta/apply.cmd/apply.ps1/설명서/상세 안내/release_report/SHA256/tool3파일/Galmuri라이선스다. 원본·수정 ROM, 폰트 PNG/TTF, 에뮬레이터는 포함하지 않는다. 1편 도구/템플릿/검증기를 읽기만 해서 가져왔으며 기존1편 파일은 그대로다. xdelta3 실제버전3.2.0/Apache2.0, 도구와라이선스 출처·SHA는 release_report에 있다.

원본262160바이트 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`. 결과491536바이트 SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`. xdelta SHA `5faa98aba20c3f22808892accfb472d4e1e4877c1350e1e170524c251507e1c0`. ZIP SHA `a9fd6be2bf9d9ba8044c4cef0b0e0aa510d8fde5e0b16c355ee9a3cfb72f3327`. IPS와 xdelta는 다른 표현이며 같은 결과를 만든다.

Windows 실제apply.cmd로8검사했다: 올바른 원본 적용, 기존 결과 거절, 원본=결과 경로 거절, 같은 크기 다른 원본 거절, 이미패치된 원본 거절, 손상 패치 거절, 손상 도구 거절, 인수누락 거절. 한글/공백 경로에서 실제 실행했고 정상 결과는043과 모든 바이트가 같았다. 원본과기존결과는 보존됐다.

최종ZIP의 파일 목록·내용·CRC를 확인하고 별도한글 경로에 풀어 apply.cmd를 다시 실행했다. ZIP에서 푼 결과도043과 정확히 같다. 실행별GUID 임시파일만 정리하며 ROM을 삭제하지 않는다. [상세 적용 검증](<../qa/apply/2편 개발판 한글 공백 적용 검증 20261005_001/apply_verification.json>).

정적/빌드/IPSapply/에뮬레이터/직접화면은 기존43·52·53·54 보고서를 해시로 연결해 유지했다. 새 에뮬레이터 검증을 했다는 주장은 하지 않는다. 이번 결과PASS는 패키지/Windows적용의 결과다. 51 전체보존/54 실제성HUD 증거도 그대로다. 성 HUD 육안 의심은54에서 픽셀·시점으로 해소됐다.

미수행: 전체자연플레이·모든방/분기·오디오/reset/savestate/실기·최종사람번역/명칭검토·전체corpus전역폐쇄. 현재PAUSE/HOW TO CONTROL관측밖소비는 전역미사용으로확정하지않으며 원본을보존했다. 기존PUSH START/법적표시/스태프영문이름/M로고보존결정의최종검토도남는다. 원본·1편·모든실패/QA를보존하며카페공개작업기는최종완료후작성한다.

재현: [패키지 빌더](../scripts/make_review_package.py)와 [적용/ZIP 검증기](../scripts/release_apply_helpers.py)는 기존경로에덮어쓰지않는다. 검증용새이름/QA경로를지정해새패키지만들때에도43/원본SHA를검사한다. 사용자는ZIP전체를풀고 apply.cmd에원본을끌어놓거나 `apply.cmd "원본.nes" "새결과.nes"`를실행한다. Python은필요없다.

다음 작업 하나: **현재54원천·45번역초안과그림/UI명칭·보존결정을장면근거에연결한사람검토자료를만든다.** 개발/PoC는계속하며최종검토를자동승인으로간주하지않는다.
