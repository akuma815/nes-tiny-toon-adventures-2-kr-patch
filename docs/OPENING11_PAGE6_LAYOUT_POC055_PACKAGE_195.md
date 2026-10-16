# 작업195 — 요청6문단 조정055 패키지·Windows 실적용

사용자문단6요청을반영한 [055적용ZIP](../dist/TinyToonAdventures2_KR_Opening11_PoC055_Layout6_20261009.zip) SHA `e160baa0a63a0d9d4b72836837b179c942122401d2dbecae7481e89a2fafd46b`를만들었다. [사용법](../dist/TinyToonAdventures2_KR_Opening11_PoC055_Layout6_20261009/README_적용방법.txt), [053/055 6문단실제비교](../dist/TinyToonAdventures2_KR_Opening11_PoC055_Layout6_20261009/review/review.html), [실적용보고](../qa/reports/opening11_195_package.json). 원본일본판→055전체차분이며기존한글ROM에덧씌우지않는다. ROM SHA `8346499ca4240ffad350e3977f792735563779b8c749744a8d9b413ea0b44086`,원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`. 변경파일전체SHA는 [195매니페스트](../manifests/nonplay195_assets.json).

Windows8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로의최종ZIP추출본apply.cmd→byte-exact055 PASS. ZIP CRC/파일목록/전내용exact/적용후payload불변/ROM-free PASS. 38파일에실제9문단PNG와동일시점053수정전PNG·검증보고·CPU·레이아웃요청·폰트/xdelta라이선스를포함했다.

코드/입력별실제검증은193/194의정확한055에연결한다. 이작업은패키지실적용이며새에뮬레이터/플레이없다. 054홈후보는포함하지않는다. 기준051/053패키지/054후보/원본/1편/CSV/사용자Mesen/세이브보존. 전체11px/사람최종승인/전체플레이/055Start·기차신규검수/하드웨어·오디오·세이브호환미완료다. 원문유지6건그대로,카페완성작업기/외부게시없음.

재현: `python scripts/package_opening_layout195.py`는기존출력을덮어쓰지않는다. 새출력명/QA경로를정한별도복제에서재현한다. 사용자검수는원본을apply.cmd에넣고새055를초기화한뒤타이틀에서기다려6문단을확인한다.

다음 작업 하나: 055패키지·193/194의고정근거·인계링크/원본보존을감사하고재개표지를갱신한다.
