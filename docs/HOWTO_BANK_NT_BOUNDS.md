# 작업99 — HOW TO CONTROL 뱅크와 안내 화면 타일 참조

현재047 ROM/CSV/검토패치를 변경하지 않았다. 원본/1편/과거 증거를 보존했다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. [검증기 v5](../scripts/analyze_candidate_fonts099_v5.py), [상세 보고서](../qa/reports/candidate099_bank_nt.json).

원본 literal STA35 motif14곳 중12곳은 LDA immediate이며 source/047 두 명령 slice24개를 검사했다. 116은 source5E3E/CPU9E2E의 한 곳이다. 120은 없었다. 다른 두 writer의 D20B course0..4 및 F642/F646 direction0..3 표에도116/120은 없다. arbitrary selector나 다른 indexed/indirect alias까지 닫은 결과는 아니다. START122→222·게임오버122→212는 기존 변경이다. 두 명령에서 A/N은 그 값에 맞게 달라지며 X/Y/SP/다른flags/cycles와 RAM35 외 보존을 검사했다. train D20B의 bank34 68→224는 기존 STOP 변경이고 bank35 표는 같다. 이 짧은 slice에서 전체 downstream ABI를 새로 증명했다고 주장하지 않는다.

HOW TO CONTROL은 source bank116 local16..22, background0800 기준 tile90..96, source3D110..3D180에 있다. 확대 [원본 CHR 설명그림](../work/candidate_font099/CHR_page_1D_6x_static.png)을 직접 확인했다. 임의 회색 타일 접촉판으로 실제 화면이 아니다. [PAUSE 포함 다음 페이지](../work/candidate_font099/CHR_page_1E_6x_static.png)도 원본 추출의 정수 확대이며 게임 표시를 뜻하지 않는다.

일반 놀이기구 안내 producer9DFF는35=116을 지정하고 selector10(hex), pointer87A2/source47B2,282바이트 압축 NT를 사용한다. 디코더803F→80BE를 source/047 각128 D-clear flags로 실행했으며1024개2007 주소/값/cycle, CPU레지스터/전체RAM/명령수가 같다. 비동기 IRQ/NMI/실제PPU·D-set은 이 CPU모델에서 제외한다. 완전한 NT에는bank116/117의 장식267셀을 사용하지만 label90..96은0개다. 따라서 이 뱅크 전체가 미사용이라고 부르면 틀린다.

역사적033 롤러코스터1800의 environment 동결SHA와 PNG/RAM/PPU/mapping/state5파일을 재검사했다. RAM35=116, PPU0800..1000이source bank116/117과 같고 높은 NT267셀은 디코더와 정확히 같다. 실제033 화면도 직접 보았다. label90..96은 이 실제표본에 없다. 새047 실행이나 모든 시점·모든 consumer의 부재증명은 아니다. sourceHOWTO/PAUSE 두2KiB는 현재047에도 원본과 같다.

실패는 outputs 전 guard에서 중단됐으며 원본/CSV/ROM 수정은 없었다. v1은 기존 START/게임오버 변경을 누락, v2는 그 N플래그까지 같다고 잘못 검사, v3는 absolute,Y 주소 바이트 guard를 잘못 지정, v4는 기존 train bank34 변경까지 같다고 검사했다. [v1](../qa/reports/candidate099_v1_observation.json), [v2](../qa/reports/candidate099_v2_observation.json), [v3](../qa/reports/candidate099_v3_observation.json), [v4](../qa/reports/candidate099_v4_observation.json)와 실패 스크립트를 보존하고 v5에서 정확한 기존 변경만 허용했다.

빌드/적용 및 새 에뮬레이터 실행은 없었다. PAUSE·HOWTO·POW의 전역 미사용, 최종 사람 보존 승인, 전역 corpus, 자연 전게임 완주, 실기/PCM청음, 최종 번역 검토, 공식 배포/카페 완성 작업기는 미완료다. 재현 명령 `python scripts/analyze_candidate_fonts099_v5.py`는 이미 존재하는 보고서를 거부한다. [동결 자산](../manifests/candidate099_assets.json).

다음 작업 하나: 현재047 일반 놀이기구 안내를 baseline/probe 동일 입력으로 실행하고 RAM35·FD9E top mapping·HOWTO 실제 pattern읽기와 장식 positive control을 연결한다.
