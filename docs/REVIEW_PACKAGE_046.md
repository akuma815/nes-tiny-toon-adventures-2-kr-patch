# 작업83 — 빌드046 ROM 없는 검토 패치

[11파일 ZIP](../dist/TinyToonAdventures2_KR_Review_046_20261005.zip)을 만들고 [실제 적용 보고서](../qa/reports/review046_package_final.json)를 동결했다. ZIP SHA-256은 7c3811a2a0ba53490ad9654eed637f98b46ca8e6abcadf7b32df9fc8aa66308d, xdelta SHA-256은 d7ab73e7347aef3bb99a0c81c47c7fa7d5c33646af0f97e75845c7c94c4127ea다. 대상046은 499728바이트이며 ROM SHA-256은 a58a28bcb1449ad44b02cccbf6503af0e2792cbf96c9b9409bcc05025552a0f8다. 원본과 ROM은 ZIP에 포함하지 않았다.

변경: 새 xdelta, 한국어 적용 안내, 원본/패치/도구/결과 해시 검사, 046의 현재 검증 범위와 한계를 담은 개발본 설명. [사람 검토 자료](TRANSLATION_REVIEW_046.md)는 별도 ZIP이다. 과거043 패키지는 보존했다. xdelta3 3.2.0 실행 파일과 Apache2.0, Galmuri OFL 등은 1편 검증 묶음에서 읽기 전용으로 복사하고 출처 파일 해시의 보존을 검사했다. 1편 파일은 변경하지 않았다.

정적·패키징: ZIP 내부11파일·각 바이트 일치, CRC, 라이선스·체크섬, ROM 없는 구성 PASS. 빌드 자체는 작업80의 원본부터 재빌드/Expected Writes 증거를 계승한다.

실제 Windows 적용: 한국어·공백 경로에서 apply.cmd를 실행했다. 정상 적용은046과 byte exact이며, 기존 출력/원본과 같은 출력 경로/동일 크기의 다른 원본/이미 적용한 원본/손상 패치/손상 도구/인수 없음 등7개 거부 검사도 통과했다. 최종 ZIP을 다시 풀어 실제 적용한 결과 역시046과 byte exact다. 원본 해시와 패키지 내용은 보존됐다. [8개 상세 검사](<../qa/apply/2편 개발046 한글 공백 적용 검증 20261005_083/apply_verification.json>).

시행착오: [최초 생성기](../scripts/make_review_package046.py)가 보고서 상태를 모두 단순 PASS로 가정하여 출력 생성 전 중단했다. 실제 상태 PASS_STOP046_NATIVE_TRAIN 등 정확한 세 상태를 확인한 [v2](../scripts/make_review_package046_v2.py)로 수정했으며 성공/실패 버전을 모두 보존했다. 검증 상태를 임의로 PASS로 바꾸지 않았다.

이번에 게임을 새로 실행하지 않았다. 현재046 기차와 다른3코스의 제한된 회귀는 작업80/81, 새 안내의 자연 진행은044/045 동결 자료를 계승한다. 전체 자연 플레이·모든 분기·실기·PCM 청음·현재046 reset/save-state 회귀·최종 사람 번역/명칭 검토·전역 corpus 폐쇄는 미수행이다. distribution_eligible와 human_final_review는 false이며 외부 게시 없음. 네이버 카페 완성 작업기는 아직 작성하지 않는다.

재현: 고정 출력이 없는 복제 작업공간에서 `python scripts/make_review_package046_v2.py`. 사용자 적용은 ZIP 전체 추출 후 `apply.cmd "일본판 원본.nes" "새 결과.nes"`. [동결 파일/SHA](../manifests/package083_assets.json).

다음 작업 하나: 원본 CHR61의 POW 문자 후보를 현재 실제 게임 소비 경로 및 PPU 읽기와 연결해 조사하고, 수정 전에 사용 여부와 편집 범위를 확정한다.
