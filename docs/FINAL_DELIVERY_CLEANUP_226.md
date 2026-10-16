# 작업226 — 최종 배포·작업기·정리와 인계 완료

[최종 배포 ZIP](../dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip) SHA `0e470e45968cb388f296a3103c0004641ede834f14872921d087250d9f0c0aaa`·14파일, [카페 작업기 ZIP](../dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip) SHA `32ac4f3938ea0659216e1fae61a6ad6463ed2091c8470a0af5db360a686e1e9c`·13파일/8PNG. 모두 ROM 없다. v1.0 게임 데이터는 사용자1차 실제 화면·완주 검수를 마친062와 같고, 배포 이후 추가 검증은 예정 상태다. 새로운 플레이나 카페 업로드는 수행하지 않았다.

224의 ZIP 이름 생성에서 Path.with_suffix가 버전명 .0 뒤를 확장자로 해석하여 v1.zip이 됐다. 원래 기대한 전체 이름에 .zip을 덧붙여 같은 ZIP 바이트를 복사하고 다시 추출·실제 apply.cmd를 실행하여062와 byte-exact 일치를 확인했다.224 당시 증거를 수정하지 않고 [226 적용 기록](../qa/reports/release226_apply.json)에 교정을 남겼다. 이전220/221 ZIP 및224 짧은 이름 ZIP6파일은 SHA·CRC 검사 후 private 보관226에 넣고 live 중복을 삭제했다.

224/226의 적용 임시폴더와 종료된 격리225 렌더 프로필도 정확 경로로 삭제했다. QA 보고·렌더 PNG·원천은 유지한다.226은282파일/23,255,642바이트를 정리했고 보관본은1,069,617바이트다.222/223/226 정리 합계110,831파일, 순2,492,519,456바이트(약2.32GiB) 절감. 원본·번역CSV·051·062·최종ROM해시 불변이다. [최종 감사](../qa/reports/final_delivery226_audit.json)는197~225의 봉인 근거를 live 또는214/222/223/226 보관에서 확인한다.

재현 입력인212 패키지,220 패키지 원천,221의003 작업기 원천은 유지했다. 최종 업로드는 최신 두 ZIP만 사용한다. 복원: python -B scripts/restore_superseded226.py --file <보관된 상대경로>. 기존214/222/223 복원 도구와 인계도 유지한다. private QA 보관본은 업로드하지 않는다. 이전 삭제 거부 폴더는 손대지 않았다.

변경: prepare_final226.py, execute_final226.ps1, restore_superseded226.py, finalize_release226.py, 새 이름 최종ZIP/해시·private보관·적용/정리/감사보고, 정본README/HANDOFF/SURVEY/PLAN/AGENTS. Windows 적용과 오프라인 작업기 UI 확인은 실제 게임 추가 검증을 대신하지 않는다. 날짜별 인계와 journal에 사용자 보고 및 다음 조치를 연결한다.

다음 작업 하나: 배포 이후 접수되는 제보의 ROM 해시·에뮬레이터 버전·직전 행동·장면을 기록하고 해당 경로의 추가 검증을 진행한다.
