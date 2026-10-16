# 작업52 — 자동 시연·마지막 엔진 경로와 등록 본문 호출 범위

ROM/SSOT 수정 없이 현재043으로 두 경로를 조사했다. [검증 보고](../qa/reports/engine_closure052.json), [실제5화면](../qa/dialogue/engine052_actual_pages.json), [원본 보존 감사 검사기 정정](../qa/reports/train051_link_parser_error.json).

- 무입력18,000프레임은 키 입력·RAM/ROM 수정·세이브 로딩 없이 타이틀/도입 자동 반복을 확인했다. [실행 환경](../qa/dialogue/closure043_attract/environment.json).
- 별도 마지막 엔진12,000프레임은 홈에서1000프레임에06DE=0,19=0,18=9만 설정했다. 홈의 기존 root8/step1/subphase2와F886의 카메라/화면 전제 조건을 검사하고, 다른2KiB RAM이 모두 동일한지 확인했다. [전체 기록](../qa/dialogue/closure043_root9/environment.json), [정확한3쓰기](../qa/dialogue/closure043_root9/root9_seed.csv).
- native CF49→CEF5 초기화→BC3A/BC60의 마지막 성 앞 장면→A41E 크레딧으로 진행했다. 전체 클리어를 대신하는 진단이다. 장면에 추가 번역 문구는 관측하지 않았고 크레딧은 기존201/202 한글을 사용했다. [유효 진입점 역어셈블](../work/engine_closure_001/native_root9_disassembly.json)은 CFC2 인라인 포인터를 코드로 해석하지 않았다.

정적 범위와 runtime 범위를 구분한다. 후보 HOW TO CONTROL116/117과 PAUSE120/121은 원본 byte를 그대로 유지했다. 두 실행에서 후보116..121을 선택한 CHR 포트 쓰기는0이었다. 앞선 네 놀이기구 pause와 합쳐 관측 범위를 넓혔지만 전체 코드에서 미사용이라는 증명은 아니다.

실행 종료·모든 파일 SHA·맵핑·실제1,027PNG의8,216개1KiB CHR 조각을 ROM의 현재 맵핑과 비교해 통과했다. 이것은 맵핑/자료 검증이고 모든 장면을 사람이 검토한 결과는 아니다. 직접 확인한5장면은 위 별도 목록을 따른다.

이전 등록 조사38의 native 호출 증거와 현재043의 검증된 로그를 합치면 **등록46개 고유 본문 전부에 실제9417 호출 기록**이 있다. 슬롯0과44는 미관측이지만 각각23 및1A와 같은 원천의 alias다. 54원천=본문46+고유 macro8이며 전체 corpus 완료율로 쓰지 않는다. macro82 Montana는 등록 본문에서 참조하지 않는 기존 범위 판단을 유지한다. 이전 빌드의 호출 기록과043의 화면 검증을 혼동하지 않는다.

검증기 첫 선택은 최신 매표소 로그를 누락해 MAIN_05794(slot14)에서 거절했다. [정정 자료](../qa/reports/engine052_coverage_model_error.json)를 남기고 이미 검증된043 매표소1887프레임 호출을 포함해 모든 로그 해시를 확인했다. ROM 변경은 없다.

재현: `python scripts/run_closure_qa.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새이름> --frames 18000 --inputs config/closure_noinput_001.json`. 마지막 엔진은 frames12000, inputs closure_root9_init_001.json, `--root9-frame 1000`이다. [실행기](../scripts/run_closure_qa.py), [Lua](../scripts/trace_closure_v1.lua), [검증기](../scripts/verify_engine_closure.py)는 최초 경로를 덮어쓰지 않는다.

현재043 ROM SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`, IPS SHA `4337ba28119d88135a8f3cca7f3a0a6d32a3e183e92e40aa3bfff84b2a45f1bb`, SSOT SHA `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27` 그대로다. CPU/재빌드/apply는 작업51 증거를 유지하고 이번 조사에서 재실행했다고 주장하지 않는다. 자연 엔딩/전체 플레이·오디오/reset/savestate/실기/사람 최종 번역 검토는 미수행이다. 원본·1편·모든 과거 성공/실패 자료를 보존했다.

다음 작업 하나: **현재043의 성 입장 일반 티켓50장 허용/49장 거절 경로를 실제 native 대사·차감·화면으로 확인한다.** 중단 지시가 없으면 이어간다.
