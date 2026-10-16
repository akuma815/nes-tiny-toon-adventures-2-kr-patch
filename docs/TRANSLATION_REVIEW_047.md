# 작업92 — 현재047 사람 검토자료 갱신

[검토 HTML](../workspace/review/translation047_20261005/review.html), [ROM 없는 ZIP](../workspace/review/TinyToon2_Translation_Review_047_20261005.zip), [항목별 JSON](../workspace/review/translation047_20261005/review_records.json), [검토 대기사항](../workspace/review/translation047_20261005/DECISIONS_PENDING.md). ZIP SHA-256454dd77553092fea3d974ee520d249d956e969a82fa099a4cb8674c6857150aa. 현재047 ROM82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10과 CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556 기준이다. 이전046 자료와 모든 증거는 보존했다.

정적/패키지: 54본문 원천·33그림 문구·14실제사진을 보존했다. MAIN_057C1 한 항목의 새 문장/메모만 CSV에서 갱신하고 나머지53항목/그림33의 유지·원문token/상태를 확인했다. 29native 계획 해시,4AI 그림label을 포함한 기존046 manifest 및14사진 해시를 검증했다. 과거043/045/046 실제사진13장은 사진별 빌드와 제한을 명시하고,047 성 입구 실제사진1장을 추가했다. ROM/패치/폰트/에뮬레이터가 없는5파일ZIP은 무결성과 추출 byte exact를 확인했다. [제작v3](../scripts/make_translation_review047_v3.py), [검증](../qa/reports/review047_records.json).

렌더/직접 보기: 별도 headless Edge profile에서1280폭/390폭 렌더링, 이미지14장 decode·본문54·그림33·외부이미지0, 가로넘침 없음, 검색/접기/검색초기화와 크레딧3원문 표시 exact, JavaScript 오류0. 현재성입구 DOM문구 및 마지막사진047 표기를 확인했다. [렌더러](../scripts/render_review_kit047.py), [렌더 보고서](../qa/review/translation047_092/render_report.json), [데스크톱](../qa/review/translation047_092/desktop_top.png)/[모바일 성 입구](../qa/review/translation047_092/mobile_gate047.png)를 직접 보았다. 사용자브라우저/게임설정은 수정하지 않았다.

실패 보존: v1은 여러gate항목에서 공유하는 삽입메모의 전역 유일성을 가정해 파일쓰기 전 실패했다. v2는 한 항목 안으로 범위를 좁혔으나 native계획키가 없는4AI label의 스키마 차이에서 파일쓰기 전 실패했다. 두 스크립트와 [v1 기록](../qa/reports/review047_builder_v1_observation.json)/[v2 기록](../qa/reports/review047_builder_v2_observation.json)을 보존했다. v3는 기존manifest 검증 후29계획과 정확히4개AI label을 구분해 통과했다. 임의 새 label을 생략하지 않았다.

이 작업은 검토자료 UI/ZIP 검증이며 게임을 재실행한 결과가 아니다. 게임047 실제 출력은 [91](GATE_EDITORIAL_QA.md) 근거다. 번역/명칭/디자인 최종사람검토는 미완료이고 자동 승인·전역corpus폐쇄·전체완주·실기·PCM청음·외부게시·카페완성작업기를 주장하지 않는다. 046 state/reset 근거도 역사적범위로 표시했다.

재현: `python scripts/make_translation_review047_v3.py`는 기존출력을 거부한다. 렌더는 `python scripts/render_review_kit047.py --input workspace/review/translation047_20261005/review.html --output qa/review/새폴더`. [동결 파일/SHA](../manifests/review092_assets.json).

다음 작업 하나: 현재047의 ROM 없는 xdelta 검토패키지를 만들고 한국어·공백 경로에서 Windows apply.cmd8검사 및최종ZIP재적용을 실행한다.
