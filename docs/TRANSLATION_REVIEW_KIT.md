# 작업56 — 사용자 최종 검토를 위한54원천/29그림UI/실제9화면 자료

[최신 검토 HTML](../workspace/review/translation043_20261005_v2/review.html), [검토 기록](../workspace/review/translation043_20261005_v2/DECISIONS_PENDING.md), [ROM없는 검토자료 ZIP](../workspace/review/TinyToon2_Translation_Review_043_20261005.zip), [자료 검증](../qa/reports/translation_review056.json).

현재043/SSOT를 수정하지 않았다. 원천54개(본문46+고유macro8),45번역초안과9기술공유 상태를 그대로 복사했다. 각ID의원문/번역/장면/제어토큰/원문SHA와29그림UI항목·실제9개PNG/환경근거를 연결했다. 사람 최종 검토를 자동승인하거나distribution_eligible로 바꾸지 않았다. 카페 공개작업기는 현재작성하지않았으며이자료는사용자검토용이다.

최신V2는3개크레딧의원문영문을이미검증한37 source_lines와원본rawSHA로읽기좋게표시한다. 원래SSOT original_view와제어토큰을JSON에그대로남긴다. 초기검토자료/렌더도보존했다.

기계검증: JSON의모든SSOT보호필드/54ID와45draft상태동일,9inlinePNG는실제QA원본SHA와일치,5파일ZIP 목록/CRC/압축내용은원본과byte동일. ZIP SHA `b9318570ae9ccd21c29e14624a8d0e83b8f63cb19bf417917d96a100434ef93d`. 원본/수정ROM·fontPNG/TTF·에뮬레이터를포함하지않는다.43 ROM SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`, SSOT SHA `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27` 그대로다.

[격리 Edge 렌더 검증](../qa/review/translation043_20261005_v4/render_report.json)은데스크톱1280/모바일390,전체9이미지로딩,외부이미지0,본문/이미지폭넘침0,54원천/29그림행,ID검색1건/초기화54건/펼침,3영문크레딧DOM문자정확성을확인했다. [데스크톱](../qa/review/translation043_20261005_v4/desktop_readable_credits.png)과 [모바일](../qa/review/translation043_20261005_v4/mobile_readable_credits.png)을직접검토했다. 최초V2데스크톱/모바일상단·가격05805 화면도직접검토했으며현재HTML이같고영문크레딧만추가했다.

최초검사기는Edge실행프로세스가유지된다고가정해거절했다. 실제격리브라우저는재실행됐고자기프로필의DevToolsActivePort가뒤늦게준비됐다. [오류자료](../qa/reports/review056_renderer_startup_error.json)와최초QA/검사기를보존하고,그격리브라우저만자기CDP포트로닫았다. 사용자기존브라우저는조작하지않았다. V2이후검사기는독립새프로필의준비를기다린다. 검색초기화의54건재복구를V3에서명시assert했고,영문크레딧의새읽기표시/모바일폭을V4에서검사했다.

정적자료/ZIP/문서UI검증이며이번작업에서새게임플레이를실행했다는주장은하지않는다. [최신 렌더러](../scripts/render_review_kit_v4.py)의재현은 `python scripts/render_review_kit_v4.py --input workspace/review/translation043_20261005_v2/review.html --output qa/review/<새ID>`이다. 기존 경로/프로필/자료를덮어쓰지않는다.

원본·1편·과거성공/실패·QA·검토패키지55를보존했다. 미수행전체자연플레이/모든방/분기·오디오/reset/savestate/실기·최종사람번역/명칭/원문보존결정·전체corpus전역폐쇄를구분한다. 번역검토를기다려야만하는독립기술조사를멈추지않는다.

다음 작업 하나: **현재043의새부팅/놀이기구진입후reset을명시한무세이브실행으로검증하고controller-only장기경로를확장한다.** 자료의미수행항목은수행된범위만갱신하며작업55의검토용패키지는동결한다.
