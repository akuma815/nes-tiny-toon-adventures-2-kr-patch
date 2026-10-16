# 작업219 추가 검증·재현 명령 정정

`python -B scripts/verify_resume219.py`로215~219 봉인45파일, 원본/CSV/051/062/IPS/ZIP6파일, 신규 인계 링크와 현재219 인계를 확인했다. 모두 통과했다. [최종 보고](../qa/reports/resume219_final_verification.json).

218의`seal_irq218.py --verify`는218 당시 통과했으나219 인계 후 다시 실행하면 현재 헤더를218로 고정한 마지막 assert에서 실패한다. 파일 해시나 링크가 바뀐 실패는 아니다. 봉인218 스크립트를 보존하고 위 최신 검사기를 추가했다. [219 수치 정정 문서](TEXT11_IRQ_STACK_GAP_CORRECTION_219.md)의 이전 재현 명령보다 이 추가 문서의 명령을 사용한다. 검사기/보고/문서 SHA는 [추가 봉인](../manifests/nonplay219_resume_verification_assets.json)에 있다.

062는 수정하지 않은11px 개발후보다. 모델의 한정 NMI/IRQ 검사만 통과했고 실제 화면 검수는 사용자 담당이다. 다음 작업 하나: 사용자062 재현 장면 하나의 결과를 받아 조사한다.
