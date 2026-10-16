# 지도 간판 PNG 추출 — 작업39 / 037 유지

실제037 코스터 경로frame1080의지도 MONTANA LAND를144×16 native PNG와정수8배PNG로추출했다. 이전036의동일장면직전1079 NMI FD77/FD92가A000/A008/B000/B008에50/51/52/53을쓰는기록과037그림/타일바이트불변을연결했다. 프레임끝mapping은이미하단IRQ글꼴이라그값을상단글꼴이라고해석하지않았다.

[원래PNG](../extracted/graphics/map_banner_001/map_banner_source_native.png), [8배](../extracted/graphics/map_banner_001/map_banner_source_8x.png), [NT/CHR/팔레트·바이트·실제픽셀근거](../extracted/graphics/map_banner_001/consumer.json) SHA256 `cb9cda562901159b4a57b9ead649772b0384f3d8169ce1a494a2560946f5fcf1`.36개셀은현재지도상단에서각타일이한번만사용된다.32×19 지도 NT 내부만검사했으며전게임다른CHR80~83소비가없다는증명이아니다.

정적 decode→encode 및실제캡처RGB전체일치PASS. 별도새ROM/빌드/적용/CPU실행/에뮬레이터없음. 실제원래간판을직접검토했다. 변경파일extract_map_banner.py/consumer JSON/source PNG2/indices bin/문서·인계·journal. 원본ROM/CSV/037변경0,모든이력보존. 재현 `python scripts/extract_map_banner.py`.

다음행동하나:imagegen으로몬타나랜드글자를생성하고간판틀을보존한타일변환과모든관측뱅크소비경로를검증한다. 계속한다.
