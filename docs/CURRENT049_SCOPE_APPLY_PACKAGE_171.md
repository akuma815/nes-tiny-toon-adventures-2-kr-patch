# 작업171 — 원문 보존 결정 반영·최신 적용 패키지171

2026-10-08 사용자의 **‘다시 진행’**으로 비플레이 작업을 재개했다. 전날170 마감 지시는 이 재개 지시로 해제됐다. 실제 플레이 검수 사용자 담당과 자동 플레이 실험 금지는 그대로다.

[새 검토용171 ZIP](../dist/TinyToonAdventures2_KR_Review_049_Scope171_20261008.zip)에169의 HOWTO·PAUSE·POW 이번 범위 원문 유지 결정과 최신170 검토자료를 반영했다. 기존168/170 자료를 보존했다. 패치·apply.cmd/ps1·xdelta3·도구/글꼴 라이선스는168과 바이트 동일하다. 등록54원천/45본문초안·9기술공유/33그림, 기존실제21PNG·정적4아틀라스를 변경하지 않았다. 발견7=명시적보존3+기존타이틀보존연결1+소비/의미 미확정3이다. 최종 전체문구/명칭/그림/배포승인은false다.

[최종 검증 보고](../qa/reports/nonplay171_final.json): ZIP21파일 CRC/압축전후 내용과20파일 SHA목록을 검증했다. 최종ZIP을 새 한글·공백경로에 풀어 실제 Windows apply.cmd를 실행한 결과 exit0,499728바이트 전체가 현재049와 동일했다. 원본·패치·도구·ZIP·CSV 불변. 내장170 검토자료8파일이 기존 검증본과 바이트 동일하므로170의 PC/모바일 표시 근거를 재사용하며 브라우저 검사도 반복하지 않았다.

171v1의 원장/검토JSON raw SHA 동일 가정은 preflight에서 실패했다. 원장169는CRLF, 검토170의 파생 파일은LF였고 전체 JSON은 동일했다. 기존파일은 수정하지 않았다. v1스크립트/실패보고를 보존하고v2에서 원장SHA와검토manifest/SHA를각각확인한뒤 전체JSON동일성을 검사했다. 패키지의SHA는 실제 내장된검토파일을 가리키며 원장SHA는별도보존한다. 실패는게임/번역결함이 아니다.

정적/패키지 검증과 실제적용만 수행했다. 신규ROM재빌드·CPU하네스·에뮬레이터·직접게임장면·플레이·청음·사람최종검수 없음. 38cycles/page idle/RNG/CPU차이·163 RGB7326픽셀 실패/원인미확정, 전역원천폐쇄와미연결3후보, 전체플레이/최종말투·명칭·그림/실기·PCM은잔여다. HOWTO/PAUSE/POW 추가번역은이번범위원문유지결정으로닫았다. 카페완성작업기는전체완료후이며외부게시없음.

ZIP SHA `64dd178a91eeff024ea38519fef65e8d8cdf74b34b5373703a4692d4149a3d81`, ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 재현생성 `python scripts/package_scope171_v2.py`; 최종ZIP실제적용/봉인 `python scripts/verify_scope171.py`; 감사 `python scripts/audit_scoped_work.py --manifest manifests/nonplay171_assets.json --output qa/reports/nonplay171_session.json`. 기존출력을보호하므로재실행복제는새출력경로를사용한다. 변경:새171패키지/해시사이드카·생성/검증/날짜별봉인기·실패/성공보고·적용QA·인계/조사/계획/journal/canonical·manifest/audit. 각사용파일SHA는manifest다.

다음 작업 하나: 미연결 RYO51/NT1C/진단STAGE SELECT의 현재 정적 근거와 범위 선택지를 묶고, 실제 소비 연결 또는 원천 보존에 필요한 결정 근거를 정리한다.
