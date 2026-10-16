# 작업187 — 오프닝11px 실제9문단·반복·분기 검증과 오늘중단

사용자 요청 ‘오프닝 부분 적용해서 PoC’의 개발시험판 **053**을 만들고 실제 Mesen의9문단11px 표시를 확인했다. **2026-10-09 ‘오늘은 여기까지’ 지시로 중단**한다. 추가 빌드/실행/패키지는 진행하지 않는다.

[실제8px/11px 비교HTML](../workspace/review/opening11_187/review.html), [확정검증보고](../qa/reports/opening11_187_validation.json), [구현/CPU 인계186](OPENING11_PAIRED_ROW_POC053_BUILD_186.md). 비교18PNG는 각 빌드의 해당 문단 완성시점에서 복사한 실제Mesen 화면이며 같은 프레임 번호의 시간비교가 아니다. HTML은 검토자료이고 브라우저 렌더 검증은 미실시다. 원본9문단 어휘/CSV는 그대로, 긴 문장 줄바꿈만 변경했다. 한글 실획11px, 출력셀12×16이다.

정적/빌드/CPU: 작업186의원본ExpectedWrite·IPS실적용·독립ROM/IPS재빌드·최종6502검사 PASS를 그대로 연결한다. [ROM053](../build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes) SHA `d27a78ddfd0f8b3d6d46bf1b9db85dbd1d1051bde99ea7eb65a46c5656b53e3c` / [IPS](../build/opening11_poc_053/TinyToon2_Opening11_PoC053.ips) SHA `770ef875775921f62fa2ea0a06166dced640946fe1028a83d6be27df5043f557`. 원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`와 기준051/번역CSV는 보존했다.

에뮬레이터: 사용자와 동일한 고정실행파일을 별도181호스트에서 사용했다. 사용자가 열어 둔Mesen/설정/세이브는 수정하지 않았다. 원본ROM·RAM·PC·생명수·강제세이브 주입 없이 콜드부트 및 명시적컨트롤러입력만 사용했다. 9000프레임의9문단각3회,1575출력호출/3024상하타일의 다음vblank 실제PPUNT기록 PASS. 글자기록은scanline248/249,최대큐10바이트. 30회문단초기화 직전의9행이모두0으로 지우기를 확인했다.

현재VRAM은write로그N−1과 같고 실제PNG는N−2 및 이전EndFrame의CHR/팔레트를 소비한다. 고정시점으로페이드까지RGB전체를비교해2167출력도중/대기/소거캡처·29,956,608픽셀exact PASS. 비폰트CHR가전환에남는순간에는4팔레트모두검정임을확인하고정확한RGB를비교했다. 넓은픽셀마스크나프레임별임의허용량은사용하지않았다. 검증기실패/수정은 [별도기록](../qa/reports/opening11_187_verifier_attempts.json)에보존했으며053ROM은변경없다.

Start1000/1900의건너뛰기는root1이아니라기존타이틀root0으로돌아갔다. 각8표본의전체PNG/PPU/OAM/매핑은051과같고 이후오프닝재진입을관측했다. 입력동일기차5000프레임의734쌍은전체PNG/RAM/PPU/OAM/매핑/CPU상태가051과byte-exact였다. 이전교환대사수정050·움직이는정지표지판051은보존됐다. 이검사는한정회귀이며전놀이기구/자연완주검수는아니다.

직접장면시각확인: 오프닝9문단의11px실제화면을열어읽힘과4행편지·마지막3행이맞는것을확인했다. 사람의최종폰트/줄바꿈승인은아직받지않았다. 전체텍스트11px전환은이오프닝PoC이후별도이며타화면은8px다. 타이핑열수차이로장면시간이달라지고PRG8/9의전역미사용/하드웨어/오디오/다른버전세이브호환을보장하지않는다. 전체플레이검수는사용자담당이다.

변경파일/하위runtime환경매니페스트해시: [187매니페스트](../manifests/nonplay187_assets.json). QA환경JSON에각캡처/로그의전체SHA를보존했다. 원문유지HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT 결정은그대로다. 카페완성작업기/외부게시/ROM없는053ZIP·Windows8사례및최종ZIP실적용은아직진행하지않았다.

재현은새빈경로로 `python scripts/run_opening11_186.py --rom build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes --output qa/dialogue/<new-directory> --frames 9000 --inputs config/intro_no_inputs144.json --script scripts/trace_opening11_187_v3.lua`. 검사기 `scripts/verify_opening11_187_v4.py`는기존187결과보존을위해재실행시assert가걸리므로복제후새출력경로로설정한다. **오늘추가실행하지않는다.**

다음 작업 하나: 사용자가 작업을 재개하면 오프닝11px PoC053의 ROM 없는 적용 패키지를 만들고 실제Windows 적용을 검증한다.
