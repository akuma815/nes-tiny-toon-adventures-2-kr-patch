# 작업188 — 오프닝11px PoC053 적용패키지·Windows 검증

사용자 ‘다시 진행’에따라187인계의패키지작업을재개했다. [053 적용ZIP](../dist/TinyToonAdventures2_KR_Opening11_PoC053_20261009.zip) SHA `13c044ee3c67d979799b44a21eb1d26f3a58fc346ce702dd12af607f125e0f43`, [사용법](../dist/TinyToonAdventures2_KR_Opening11_PoC053_20261009/README_적용방법.txt), [패키지내실제8px/11px 비교](../dist/TinyToonAdventures2_KR_Opening11_PoC053_20261009/review/review.html), [Windows/ZIP검증](../qa/reports/opening11_188_package.json). 원본일본판→오프닝11px PoC053 전체차분이며기존한글ROM에덧씌우지않는다. [대상ROM](../build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes) SHA `d27a78ddfd0f8b3d6d46bf1b9db85dbd1d1051bde99ea7eb65a46c5656b53e3c`; 원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`. 변경파일/해시는 [188매니페스트](../manifests/nonplay188_assets.json) 및패키지SHA256.txt.

빌드/적용: 실Windows apply.cmd8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로의최종ZIP추출본실적용→byte-exact053 PASS. ZIP CRC/정확한파일목록·모든내용/적용후payload불변/ROM-free PASS. 36파일에 실제18PNG·HTML·CPU/최종runtime보고·9문단배치·폰트출처·xdelta도구/라이선스·기존Galmuri및새Galmuri11 OFL을포함했다.

정적/빌드/CPU/실제장면검증은 [186](OPENING11_PAIRED_ROW_POC053_BUILD_186.md)·[187](OPENING11_POC053_RUNTIME_HANDOFF_187.md)의동일053SHA에귀속된다. 이작업188은실적용검증이며새Mesen/자동플레이/전체놀이기구실험없음. HTML브라우저렌더검증은미실시. 9문단3회·2167RGB·3024상하소비·30소거·Start분기·734기차동일근거를재사용한다.

기준051/CSV/원본/1편/이전dist와실패자료/사용자Mesen설정·세이브는유지한다. 053은오프닝한글실획11px·12×16셀의PoC이고다른화면8px,전체11px전환미완료다. 타이핑시간차이·전역PRG8도달성·오디오/하드웨어/다른버전강제저장호환·전체플레이/사람의최종폰트승인은남아있다. 원문유지6건그대로,카페완성작업기/외부게시없음.

재현: `python scripts/package_opening11_188.py`. 기존확정출력덮어쓰기방지로현재경로재실행은거부한다. 별도환경에서출력명/QA경로를새롭게설정해동일입력으로재현한다. 원본ROM을apply.cmd에드래그하거나명시적결과이름을지정한후새053을열어초기화하고타이틀에서기다린다.

다음 작업 하나: 188패키지와186/187인계의해시·프로젝트링크·원본/1편보존을확인하고 전체11px의다음적용범위를정리한다.
