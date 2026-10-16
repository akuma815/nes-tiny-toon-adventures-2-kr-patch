# 작업75 — 두 한글 안내의 자연 진입

빌드044/SSOT 변경 없이 새coldboot Mesen에서 controller-only20,000프레임을 실행했다. [실행 환경](../qa/dialogue/notices075_natural044/environment.json)과 [검증 보고서](../qa/reports/notices075_natural.json). RAM/ROM/PC/시간/체력/화폐/세이브는 수정하지 않았다.

첫 구간 자연완료 후 [actual5010 다음 라운드](../qa/dialogue/notices075_natural044/frame_05010.png), 두번째 구간 시간초과의 [actual19110 한글 안내](../qa/dialogue/notices075_natural044/frame_19110.png), [actual20000 홈 복귀](../qa/dialogue/notices075_natural044/frame_20000.png)를 직접 확인했다. 첫구간 클리어와 실패 안내의 자연소비 증거이며 전체3구간 클리어 증거가 아니다. 최종체력3/Gold·history0이다.

19,999개 입력 정책 행과666개 world 행이 기존043/작업72의 같은 구간과 완전히 같았다. 829PNG/6,632개 실제1KiB CHR매핑이044 ROM과 일치한다. 같은시점828PNG의 OAM/네임테이블/팔레트가같고 RAM 차이는39/3F의62→220만이다. 13개 바뀐 PNG는 두 안내의 기존 스프라이트 사각형 안에만 변화가 있다. 나머지 화면은 byte/pixel 일치.

첫 검증기 V1은 frame5130에서 현재OAM이 이미 clear된 경우를 거절했다. 화면에는 마지막 NEXT ROUND가 남아 있으며 사각형(96,113)-(160,129)은 기존5010..5100의 안정된 안내 위치와 일치한다. V2는 이 한 표본에만 보존된5100 OAM 영역을 사용했다. renderer가 정확히 몇cycle/프레임 늦는지는 주장하지 않는다. 실패 검사기를 덮어쓰지 않았다.

변경 파일/해시는 [manifest](../manifests/notices075_assets.json). 정적044변경없음/새빌드·apply 미재실행/실제20k·직접3장면 검증을 구분한다. [044 빌드/적용 검증](NOTICES_KOREAN.md)을 유지한다. ROM SHA58db7fa14239ecd71c0454c097293a3037bb3ce841ef455213b02530b521dbdf, 본문 CSV SHA26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

재현: `python scripts/run_cart_rounds_qa_v4.py --rom build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 20000 --inputs config/menu_cart_001.json`; `python scripts/verify_notices075_v2.py` (고정 출력이 없는 복제 작업공간).

미수행: 전체3구간/전게임 완주, 최종 사람 번역/명칭 승인, 실기/PCM청음. 043의 검토용 패키지는 과거자료로 보존한다. 실제2F 승리 bot 개선은 반복 실패가 있어 UI누락 검사보다 후순위다.

다음 작업 하나: 원본 모든128 CHR뱅크를8×16 스프라이트 배치로 재검토하고 기존번역·보존·소비미연결 후보를 목록화한다.
