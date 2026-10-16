# 공개 작업기·기술 지침 독자용 개정 — 2026-10-09

## 변경 범위

공개 작업기에서 내부 빌드·작업 번호를 제거하고 타이틀 제작, 출력기 조사, 티켓 교환 오류, HUD·움직이는 정지, 11px 확대, 검증과 배포 순서로 본문을 다시 썼다. 비교 그림8개는 보호된 실제 캡처·제작 원천·정적 복원에서 다시 구성하고 제목·부제·라벨·캡션을 수정 전/후 또는 목적 이름으로 바꿨다. 원래 게임 캡처 픽셀은 수정하지 않았다.

1·2편 기술 지침의 후보번호·번호 포함 빌더 명령·내부 문서 파일명도 독자에게 필요한 설명과 최신 인계 조회 방법으로 바꿨다. 주소·폰트 크기·문단 수·공식 릴리즈 버전·SHA는 기술 근거로 보존했다. Page는 해시를 지킨6개 블록 패치를 적용하고 전체 저장 본문120블록을 로컬 원천과 공백 정규화 대조했다. 교육 코드와 설명도는 동일하다.

## 독자용 산출물

- [수정 작업기 HTML](../workspace/publication/TinyToon2_KR_Worklog_Reader_20261009/작업기.html), [카페 본문](../workspace/publication/TinyToon2_KR_Worklog_Reader_20261009/카페_복사용_본문.txt)
- [작업기 ZIP](../dist/TinyToon2_KR_Worklog_Reader_20261009.zip), SHA `354358c75ae71f4403215fa4e9a8f98e16aee58d04ccd7104d13a5dd6292aa5b` — ROM없음,14파일.
- [기술 지침 Page](https://chatgpt.com/space/page_7e1e9fe45f1881918ff36b3962ea16c0), [기술 지침 HTML](../workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html)
- [기술 지침 ZIP](../dist/TinyToon12_TechnicalGuide_Reader_20261009.zip), SHA `5b7458d2f6b603868f457ab59142ea849f9995cc2d7b08863cb426c539a7622f` — ROM없음,8파일.

## 검증 구분

정적: 공개 TXT/MD/HTML(내장이미지 제외)/JSON에서 내부 빌드·작업 번호와 번호 있는 문서/스크립트 참조가 없는지 검사했다. 공개 출처 JSON에 원천 경로·내부 빌드ID는 넣지 않았으며 비공개 원천 보고서에는 경로·해시를 유지했다. HTML내장8PNG와 파일PNG가 같은 바이트이고 ZIP CRC·목록·모든 추출 바이트가 원천 파일과 같다.

문서 시각·UI: 두 HTML을 격리 headless Edge로1280×1000 및390×844에서 렌더했다. 이미지8개/설명도2개 로드, 본문 잘림·가로넘침 없음, 작업기 확대와Escape닫기, 기술 지침 목차 이동을 확인했다. 그림8개와 각PC·모바일 첫화면을 직접 확인했다. native Page의 실제 미리보기는 사용할 수 없어 저장 Markdown 대조만 확인했고 로컬HTML의 시각 확인과 구분했다.

게임: 새 빌드·에뮬레이터·CPU·패치 적용·자연 플레이를 실행하지 않았다. 기존 사용자 실제 화면·완주1차 완료 보고와 배포 후 추가 검증 예정 상태를 그대로 유지했다. 과거 실제 캡처와 크레딧 정적 복원을 구분했다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT의 원문 유지 결정은 같다.

보존: 원본2편·CSV·최종로컬ROM·최종게임배포ZIP 및 이전 두 게시자료ZIP 해시가 같다. 이전 봉인 공개 파일21개를 manifest SHA와 대조했다. 1편 파일은 읽기참조하며 수정·빌드·복원을 하지 않았다. 현재 작업의 격리 렌더 프로필2개만 명시적 절대경로 검증 후 삭제했다. 최초 인라인 삭제 호출은 정책차단되어 실행되지 않았고, 삭제범위를 고정한 검사 스크립트는 승인·완료됐다.

## 재현과 근거

`scripts/publication228_reader_revision.py`는 새 출력폴더를 요구한다. 기존 봉인 폴더에 재실행하지 않는다. `scripts/build_technical_guide228.py`는 새 기술지침 리더를 생성한다. 원천·변환은 `qa/reports/publication228_sources.json`, Page 대조는 `technical228_page.json`, 전체 검증은 `publication228_verified.json`, 캐시삭제는 `publication228_cache_cleanup.json`과 현재 manifest를 따른다.

리더 재검사(기존QA를 덮어쓰지 않는 새 경로 사용):

```powershell
python -B scripts/render_publication221.py --input workspace/publication/TinyToon2_KR_Worklog_Reader_20261009/작업기.html --output qa/publication/reader_revision_recheck
python -B scripts/render_technical227.py --input workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html --output qa/publication/guide_revision_recheck
```

모든 해시와 변경파일 목록은 `manifests/nonplay228_assets.json`에 보관한다. 실제 카페 게시는 수행하지 않았다.

다음 작업 하나: 사용자가 수정된 작업기·기술 지침을 게시하고, 배포 후 제보의 ROM 해시·환경·직전 행동·장면을 수집한다.
