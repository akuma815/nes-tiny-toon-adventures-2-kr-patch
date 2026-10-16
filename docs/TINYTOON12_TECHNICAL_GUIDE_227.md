# 작업227 — 1·2편 NES 한글화 기술 지침과 게시자료

사용자 요청에 따라1·2편 기술 경험을 후속 한글화 작업자가 참고할 지침으로 작성했다. [Page](https://chatgpt.com/space/page_7e1e9fe45f1881918ff36b3962ea16c0), [게시자료 ZIP](../dist/TinyToon12_NES_Korean_TechnicalGuide_20261009.zip), [오프라인 HTML](../workspace/publication/TinyToon12_TechnicalGuide_20261009/기술_지침.html), [편집 원천](../workspace/publication/TinyToon12_TechnicalGuide_20261009/기술_지침.md). ZIP SHA `bf23e6ccfc8a6e2ea21794bf0c4031bef6868e5dbdef6a47ab814101d7756c50`,8파일/ROM없음. 폰트·ROM·세이브·덤프·private보관본을 넣지 않았다.

15개 기술 항목과 원천 읽기 순서를 포함했다. 두 게임의 매퍼/압축/제어코드 차이, AI타이틀의 PNG/타일/팔레트/압축예산, 주소종류·헤더, 원천 토큰/포인터 그래프, 문단별 작업집합과 글꼴수명,1편당근/2편숫자갱신 충돌,11px 상하타일·위상·숫자54/크레딧106타일,후크ABI/NMI/IRQ,ExpectedWrites,같은조건 시각검사와 실제최종ZIP적용·인계를 설명했다. 설명도2개는 새로 그린 구조도이며 실제 캡처로 표시하지 않았다. ROM없는Python교육예제는 고정2bpp벡터·64왕복·위상·중첩/보호/기대바이트 거부를 포함한다.

정적:16본문제목·주소/수량 근거·UTF8/본문표식·8파일CRC/정확payload/ROMfree PASS. 최종ZIP에서 꺼낸 예제 바이트를 Python표준라이브러리로 실제 실행 PASS. Page는 개인 위치에 생성하고 전체본문을 읽어 공백 정규화 후 원천과 동일함을 확인했다(120blocks/16h2/2mermaid). 공개공유 설정은 바꾸지 않았다. 사용 가능한 브라우저 표면이 없어 네이티브Page 미리보기는 확인하지 못했다.

로컬HTML은 격리headless Edge1280×1000/390×844에서2설명도·16제목·문단폭·목차펼침/링크이동·JS오류0 확인.4스크린샷과2설명도를 직접 열어 검토했다. [렌더](../qa/publication/technical227_final/render_report.json), [최종검증](../qa/reports/technical227_verified.json), [Page영수증](../qa/reports/technical227_page.json), [기술근거](../qa/reports/technical227_sources.json).

1편은 현재원본경로가 없어 verify_source.ps1이 실패했다. 기존footer003 최종ROM 해시는 기록과 같음을 확인했고 원본을 복원하거나 새게임빌드를 실행하지 않았다. 공개주소표는 역사 원본식별값에 한정한다.2편원본 검증은 통과하고최종ROM은062와 같다.1편/2편ROM·번역CSV·패치ZIP·에뮬레이터/세이브는 수정하지 않았다.2편사용자1차화면·완주완료/배포후검증예정은 유지한다. 새플레이·네이버카페 실제게시없음.

변경: build_technical_guide227.py,prepare_technical_renderer227.py,render_technical227.py,seal_technical_guide227.py,작성MD/HTML/복사용본문/게시안내/2PNG/예제/SHA/ZIP와QA·인계. 재현은 build_technical_guide227.py의OUT를 새경로로 지정하고 입력MD/예제를 복사한 뒤 빌드/렌더/봉인한다. 고정결과는 덮어쓰지 않는다. 실패한 무효빈patch호출은 파일변경없음. 기존자료를 재작성하지 않았다.

다음 작업 하나: 사용자가 기술 지침 본문과 설명도2개를 게시 위치에 배치하고 배포 후 제보를 같은 검증 원칙으로 수집한다.
