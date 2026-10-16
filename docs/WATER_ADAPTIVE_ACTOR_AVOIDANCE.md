# 작업157 — 급류 후반 장애물 회피와 실패 경계

[검증](../qa/reports/water157_controller_validation.json), [36쌍 CPU 모델](../qa/reports/water157_bbox_model.json), [계획/재현 명령](../work/water157/run_plan.json), [입력 전수 기록](../qa/dialogue/water157_controller049/adaptive_inputs.csv), [v1 준비 오류](../qa/reports/water157_v1_preflight_error.json), [입력 시점 가정 오류](../qa/reports/water157_input_phase_assumption_error.json).

native 충돌상자 계산은 원본/049 36쌍 CPU 결과로 한정 검증했다. 이후 일정 속도의 미래 겹침 예측은 컨트롤러 가설이다. 고정156 입력을 3300까지 유지하고 이후 실제 컨트롤러만 조작했다. 메모리·ROM·저장상태 개입은 없다. 이전156의 1794개 스냅샷 자료가 같다. 8999회 최종 입력 요청과 native A 점프 2800/2890/3499/3607/3835를 관측했다. 객체 피해 0, 마지막 플레이 기록4023까지 체력3을 유지했으나 root8로 끝났고 자연 clear는 없다. 화면하단 이탈 원인은 다음 실제 코드 관측으로 검증한다.

RAM52와 이전 프레임 라벨 요청의 비교는1237 일치/8 불일치다. 이전 라벨이 항상 실제 입력이라는 가정을 폐기했고 입력 요청과 native 소비 시점의 완전한 대응은 미검증으로 남긴다. 실패한 v1 검증·준비 스크립트와 보고는 보존했다. 역사 CSV의 vertical_hi/lo는 RAM69/6D이며 축 이름 오류를 다음 작업에서 코드와 대조해 정정한다. 이번 시각 검토는 frame03990 실제 급류/HUD와 frame04050 전환 검은 화면 두 PNG에 한정하며 성공 장면 근거가 아니다.

변경 파일: prepare_water_controller157.py/v2.py, trace_water_controller157.lua, verify_water_controller157.py/v2.py, seal_water_controller157.py, work/water157, qa/dialogue/water157_controller049, qa/reports/water157_* 및 이 상세문서·날짜별인계·journal·README/SURVEY/PLAN/HANDOFF·manifest/audit. 원본/1편/기존실패 보존. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 각 산출물 SHA는 scoped manifest에 기록한다.

정적/CPU/실행/입력요청 기록 검증 PASS(각 한정범위). 자연완주와 요청-소비 타이밍 증명은 FAIL/미완료. 새 빌드/적용·reset/state·청음/실기·사람 최종 검토는 미수행. 전체corpus/HOWTO/PAUSE/POW/자연 전체게임/정식배포 미완료. 카페 원고·게시 없음. 재현은 계획의 명령에 새 QA 경로를 사용하고 동결 검증 스크립트의 출력도 새 이름으로 복제한다.

다음 작업 하나: 157과 같은 입력으로 native 화면하단 이탈 코드·4016 읽기/쓰기·RAM52 소비를 직접 관측하고, 카메라 축 이름을 원본 소비 코드로 정정한다.
