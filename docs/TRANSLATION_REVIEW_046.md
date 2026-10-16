# 작업82 — 현재 빌드046 사람 검토 자료

본문 원천 54개(45개 번역 초안과 9개 기술 공유 항목), 그래픽 문구 33개, 실제 화면 13개를 [검토 HTML](../workspace/review/translation046_20261005/review.html)에 모았다. 추가한 문구는 시작!, 다음 라운드!, 시간 초과!, 정지다. 기존 번역 CSV와 원본, 빌드046은 변경하지 않았다. 사람의 최종 번역·명칭 검토는 아직 완료되지 않았다.

[5파일 ROM 없는 ZIP](../workspace/review/TinyToon2_Translation_Review_046_20261005.zip)의 SHA-256은 ef818bdcdc65bc8a961fadd83de5d4d7110f4cf806ad92f1c9da549eb19c11b7이다. PNG는 HTML 내부에 포함했다. 실제 과거043 화면 9개, 045의 자연 진행 안내 2개, 046의 시작·기차 정지 화면 2개이며, 각각 촬영 빌드·환경·개입 범위를 기록했다. 045 안내를 046에서 다시 촬영했다고 주장하지 않는다. 기술 공유 항목 9개는 미번역 일본어 문장 9개라는 뜻이 아니다.

정적·패키징 검증: [자료 생성기](../scripts/make_translation_review046.py), [자료 검증 보고서](../qa/reports/review046_records.json)에서 원천·사진 해시, 항목 수, ZIP 내부 파일 일치 및 손상 여부를 확인했다. 당시 기술 메모와 지금의 기술 검증 범위를 구분했고, POW 후보와 PAUSE/HOW TO CONTROL은 소비 경로 미연결 상태로 명시했다. 과거 자료는 보존했다.

브라우저 검증: [046 전용 렌더 스크립트](../scripts/render_review_kit046.py)와 [보고서](../qa/review/translation046_082/render_report.json)가 PASS다. 격리된 headless Edge에서 1280px/390px 화면, 13개 내장 이미지 디코딩, 검색·펼치기·검색 초기화, 원문 크레딧 3개의 정확한 표시, 가로 넘침 및 JavaScript 오류를 확인했다. [데스크톱](../qa/review/translation046_082/desktop_top.png), [모바일 크레딧](../qa/review/translation046_082/mobile_readable_credits.png)을 직접 확인했다. 사용자 브라우저와 에뮬레이터 설정은 변경하지 않았다.

이번 작업에서 게임을 새로 실행하거나 새 패치를 적용하지 않았다. 전체 자연 플레이, 모든 분기, 실기, PCM 청음, 최종 사람 검토, 전역 corpus 폐쇄는 미수행이다. 이 자료는 네이버 카페 작업기가 아니며 외부 게시하지 않았다.

재현: 고정 출력이 없는 복제 작업공간에서 `python scripts/make_translation_review046.py`; 렌더는 `python scripts/render_review_kit046.py --input workspace/review/translation046_20261005/review.html --output qa/review/새폴더`. [동결 파일/SHA](../manifests/review082_assets.json).

다음 작업 하나: 빌드046용 ROM 없는 검토 패치 묶음을 새 이름으로 만들고, 한국어·공백 경로의 실제 Windows 적용 8개 검사와 최종 ZIP 재적용을 검증한다.
