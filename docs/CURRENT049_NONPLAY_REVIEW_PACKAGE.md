# 작업167 — 현재049 비플레이 통합 검토 묶음

현재049의 [비플레이 검토 HTML](../workspace/review/nonplay049_20261007_167/review.html)와 [ROM 없는 ZIP](../workspace/review/TinyToon2_Nonplay_Review_049_20261007.zip)를 작성했다. 기존131 자료와 이전104 소비 보충 자료는 그대로 보존했다. 새 묶음은 등록54원천/33그림, 미연결7후보, 21기존 실제 PNG 및4정적 원본CHR 페이지를 포함한다. 실제 PNG21장은 이전 기록을 재사용한 것으로 이번에 게임을 새로 실행한 자료가 아니다.4타일 아틀라스에는 정적 자료 표기를 붙여 게임 장면과 구분했다.

저장상태/리셋을 미완료로 적었던 옛 검토 본문을 작업133의 제한된049 상태복원/리셋 후 재입장 검증으로 갱신했다. 모든 저장상태나 이전빌드 호환성으로 확대하지 않는다. 사용자 플레이 소유권, 38cycle page/idle 난수·CPU 차이, 작업163 PNG4410의7326픽셀 차이/전체RGB FAIL을 명시했다. 문구·이름·생성형 그림·원문 보존 범위 승인과 전역 원천 완결성은 보류다. 빈 JSON 응답 양식은 승인이 아니다.

[최종 검증 보고](../qa/reports/nonplay167_final.json):54원천의 번역·토큰·상태·원천SHA와33그림 보존, HTML에 내장된25PNG 각각의 원본SHA, ZIP7파일/CRC/내용 동일성 PASS. [브라우저 보고](../qa/review/nonplay049_167_render_v2/render_report.json)는 PC1280/모바일390에서 넘침없음·검색·상세열기·이미지로드·크레딧 표시3건·후보7건을 확인했다. PC상단/모바일PAUSE 후보의 문서 렌더를 직접 보았다. 첫 render167은 새 한국어 검증 문자열의 PowerShell 파이프 인코딩 때문에 실패했다. 스크립트·실패출력·보고를 보존하고UTF8을 명시한v2가 통과했다. 검토HTML/ROM 내용의 결함은 아니었으며 실패를 삭제하지 않았다.

ZIP SHA `c935d8b3fde13be8660f1cb5d2680e31f9d9d7157aa116bef0ab9bd3f26910e7`. ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 재현 생성: `python scripts/make_nonplay_review167.py`; 브라우저 검사: `python scripts/render_nonplay167_v2.py --input workspace/review/nonplay049_20261007_167/review.html --output qa/review/nonplay049_167_render_v2`; 봉인: `python scripts/seal_nonplay167.py`. 모든 출력은 덮어쓰기 보호이며 기존 증거를 재실행으로 덮지 않는다. 신규 정적/패키지·문서 브라우저 검증만 수행했다. 신규ROM빌드/적용/게임런타임/플레이/청음/사람최종검수 없음. 변경과 사용 근거의SHA는manifest에 고정했다.

다음 작업 하나: 검수용049 적용 패키지에 최신 지원 범위·사용자 검수 안내·알려진 한계를 반영한 새 ROM 없는 묶음을 만들고 최종 ZIP의 실제 Windows 적용을 확인한다.
