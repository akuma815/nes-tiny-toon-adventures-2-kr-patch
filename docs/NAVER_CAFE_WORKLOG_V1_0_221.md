# 작업221 — 네이버 카페 업로드용 작업기·8PNG·HTML

[카페 업로드용 작업기 ZIP](../dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009.zip) SHA `75e05b9150fd49ec5fd41274d630fe3ee82b4d3932507d0e03257455192bfed3`,ROM없이13파일/8PNG다. [오프라인 읽기](../workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009_003/작업기.html), [카페복사용본문](../workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009_003/카페_복사용_본문.txt), [업로드안내](../workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009_003/업로드_안내.txt). 적용용v1.0 ZIP은별도첨부한다.

타이틀추출/AI원천/NES변환·문단과그림·매표소050·HUD원본비교·움직이는정지051·오프닝05511px·062크레딧·범위별검증·적용법을작업기로완성했다. 이미지01/03/04/05/06은과거실제캡처,02는제작원천,07은062정적복원,08은설명표다. 각이미지/본문/공개출처구분JSON에서같은경계를명시한다. 이전캡처를062전체성공으로옮기지않는다. 표본seed와동일프레임아닌055비교도설명했다.

정적:8순번마커·내장PNG바이트·UTF8대체문자없음·13파일ZIP CRC/정확payload/ROM-free PASS. 렌더:격리headless Edge의1280×1000/390×844에서8이미지디코딩·가로넘침없음·확대/Escape PASS. PNG8개와데스크톱/모바일스크린샷을직접열어검토했다. [렌더보고](../qa/publication/render221_final/render_report.json), [원천추적](../qa/reports/publication221_sources.json), [최종검증](../qa/reports/publication221_verified.json).

시행착오: 첫생성은과거main_nes.png가펼친경로에없어실패했다. 검증된214보관본에서그1파일을원래경로로복원했다. 최초reader런처는정상exit0뒤브라우저자식이뜨는경우를실패로오인했고포트생성대기를수정하여v2와최종렌더가통과했다. 초안figure06은전체8px실제캡처를정적문자그림처럼다뤄비교배율/분류가맞지않아철회했다. 최종003폴더의6번그림은기존8px/05511px 실제캡처쌍이며크레딧만062정적으로표기한다. 이전초안은공개하지않는다.

원본·CSV·게임ROM/ZIP·사용자Mesen/세이브·1편은수정하지않았다. 새게임/컨트롤러/완주·카페접속/실제게시없음. 사용자최종게임검수를추정하지않았고본문에미기록상태를표시했다. 브라우저렌더는작업기 UI에한정되며네이버카페실제편집기/서버렌더확인은아니다. 카페계정외부게시권한은이요청에포함됐다고추정하지않는다.

변경: publication221.py/renderer준비·렌더·봉인스크립트,공개본문/HTML/안내/PNG/출처JSON,ZIP·해시,QA렌더·보고와인계. 재현: python -B scripts/publication221.py와render_publication221.py --input <새공개HTML> --output qa/publication/<새ID>,seal_publication221.py. 고정출력은덮어쓰지않으며새경로복제에서실행한다. 봉인SHA는 [221매니페스트](../manifests/nonplay221_assets.json).

다음 작업 하나: 최종배포·공개작업기·재현원천·QA핵심을보존하고대량펼친보관중복과실패초안·임시적용사본·렌더캐시를정리한다.
