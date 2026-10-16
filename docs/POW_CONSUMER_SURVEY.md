# 작업84 — POW 정적 후보와 제한된 실제 소비 조사

원본 CHR61에는 회전하는 POW 그림이 있다. [원본8×16 목록](../work/pow_consumer_084/bank61_8x16_static.png)은 임의 설명 팔레트로 추출한 정적 자료이며 실제 게임 화면이 아니다. 메뉴의 CPU9E37 LDA #$3D /9E39 STA $38은 실제1574프레임에서 실행됐다. 추적 PC9E3B는 store 후 다음 명령 주소이며 실제 PRG 상대25E3B와 연결했다. 현재046의 bank61(file4F410..4F810)은 원본과 바이트 동일하다.

[검증 보고서](../qa/reports/effect084_survey.json). 이미 보존한5경로의 end-frame 매핑을 검사하니 bank61이 선택된 표본은 있었으나, 그 표본의 OAM에서 POW 후보 글자를 표시한 항목은 없었다. end-frame은 HUD IRQ 이후 맵핑일 수 있어 이 검사만으로 결론 내리지 않았다.

새 runtime: [4200프레임 롤러코스터](../qa/dialogue/effect084_coaster046/environment.json)와 [1900프레임 메뉴](../qa/dialogue/effect084_menu046/environment.json)를 컨트롤러만으로 실행했다. v1은2400프레임 이후, v2는1400프레임 이후 실제 PPU 패턴 읽기와 NMI top 매핑/OAM을 관측했다. 두 실행의 native61 실제 패턴 읽기0행, top POW OAM0개였다. 메뉴에서 bank61 지정은 확인했으나 그림 소비는 이 구간에서 확인되지 않았다. 새 관측과 기존046 같은 시점 화면/RAM/OAM/PPU/매핑 총2095파일은 byte exact다. [메뉴 실제 화면](../qa/dialogue/effect084_menu046/frame_01680.png)을 직접 확인했다.

이 결과는 전역 미사용 증명이 아니며 POW 번역 또는 보존의 최종 사람 결정을 뜻하지 않는다. 원본·046·번역 CSV·기존 패키지는 변경하지 않았다. 선언 범위 밖의 코스 후반/아이템·효과, 전체 자연 플레이·실기·청음·최종 사람 검토는 남아 있다. 그림을 소비 루틴에 연결하기 전에 추측으로 삽입하지 않았다.

재현: `python scripts/run_effect61_qa.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_coaster_001.json`; 메뉴는 [v2](../scripts/run_effect61_qa_v2.py)/1900프레임/[전용 입력](../config/effect084_menu_001.json). [검증기](../scripts/verify_effect084.py), [동결 파일/SHA](../manifests/effect084_assets.json).

다음 작업 하나: 현재046 기차 정지 표지 장면에서 reset/save-state의 뱅크224/225 복원 및 한글 표시를 검사한다. 과거043의 상태 검증을 현재046의 검증으로 확대하지 않는다.
