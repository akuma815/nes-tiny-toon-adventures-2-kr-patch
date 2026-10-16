"""Record completed exact-path cleanup and tested lossless recovery."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R,sha
records.DATE='2026-10-09'
audit=json.loads((R/'qa/reports/final_release222_audit.json').read_text('utf-8'))
assert audit['status']=='PASS_FINAL_RELEASE_PUBLICATION_LOSSLESS_CLEANUP'
files=[R/p for p in ('scripts/prepare_cleanup222.py','scripts/execute_cleanup222.ps1',
 'scripts/close_failed_renderer222.py','scripts/resume_cleanup222.ps1','scripts/restore_history222.py',
 'scripts/audit_final_release222.py','qa/archive/release222_history.sqlite',
 'qa/reports/cleanup222_predelete.json','qa/reports/cleanup222_deletion.json',
 'qa/reports/final_release222_audit.json','work/cleanup222/deletion_plan.json',
 'work/cleanup222/final_plan.json','work/cleanup222/deletion_progress.jsonl',
 'qa/dialogue/moving_stop182_051/frame_04272.png')]
body='''불필요한 과거 QA 펼친 사본·대형 중간 보고·실패 초안·임시 적용 사본·격리 렌더 캐시를 정확한 프로젝트 내부 경로로 정리했다. 원본, CSV, 재현 스크립트, 현재 빌드, 공개 이미지 원천 및 현재 검증 근거는 보존했다. 삭제 전 파일별 SHA 검증과 손실 없는 private 보관을 완료했다. 이미214에 있는 바이트는 중복 저장하지 않고 참조하고 새 자료는222 SQLite에 압축했다.

첫 삭제는 격리 브라우저 캐시의 파일 목록 변화 때문에 안전하게 중단했다. 실패 렌더가 만든 자체 headless 브라우저만 종료한 후 세 캐시만 다시 조사하여 마무리했다. 사용자 브라우저와 Mesen은 조작하지 않았다. 이전 삭제 거부 이력이 있는 booth039_font_probe 폴더는 계속 보존했다.

복원: python -B scripts/restore_history222.py --file qa/dialogue/moving_stop182_051/frame_04272.png. 이 파일은 실제로 없는 상태에서 복원하고 SHA 일치를 확인했으며 작은 검증 표본으로 유지한다. 기존214 복원 도구도 유지했다. private 보관본은 ROM을 포함할 수 있어 공개 ZIP에 넣지 않는다.

[최종 감사](../qa/reports/final_release222_audit.json)는 원본·CSV·051·062·패키지, 과거 봉인 파일의 live/214/222/223 바이트를 확인했다.222와223 합계110,549파일, 순2,470,333,431바이트를 절약했다. 실제 플레이 검사는 수행하지 않았고 공개 글의 브라우저 렌더와 게임 검증을 구분한다. 삭제 상세는 cleanup222_deletion.json 및 final_plan.json에 있다.'''
records.seal(222,'LOSSLESS_RELEASE_CLEANUP_222.md','과거 QA·중간물 손실 없는 정리',body,
 '정확 경로 정리 완료.214/222 보관 SHA와 실제 복원 통과.원본·현재 빌드·재현원천 보존.',
 '이전 배포 묶음223 보관과 정리 근거를 봉인한다.',[Path(__file__),*files])
files=[R/p for p in ('scripts/obsolete_distribution223.py','scripts/execute_obsolete223.ps1',
 'qa/archive/obsolete_distribution223.zip','qa/reports/obsolete_distribution223_archive.json',
 'qa/reports/obsolete_distribution223_deletion.json')]
body='''과거 Review·Opening11·HomeBooth11·Ordinary11 배포 묶음199파일(3,982,216바이트)을 정확 경로로 정리했다. [private ZIP](../qa/archive/obsolete_distribution223.zip)에 원래 상대 경로·바이트를 보관하고 CRC·각 SHA를 확인했다. 배포 원천으로 쓰이는212와 현재220/221는 유지했다.

복원: python -B scripts/obsolete_distribution223.py --restore <보관 목록의 상대 경로>. 다른 바이트의 기존 파일은 덮어쓰지 않는다. [보관 목록](../qa/reports/obsolete_distribution223_archive.json), [삭제 결과](../qa/reports/obsolete_distribution223_deletion.json). 삭제 전 경계·reparse·예상 외 자식을 검사했고 프로젝트 밖 파일과 원본은 삭제하지 않았다. private 보관본은 업로드하지 않는다.'''
records.seal(223,'SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md','이전 배포 묶음 정리',body,
 '이전 묶음199파일을 SHA·CRC 확인 보관 후 삭제.212 재현입력과 현재 배포 유지.',
 '사용자062 실제 화면·완주1차 완료 보고를 최종 릴리즈와 작업기에 반영한다.',[Path(__file__),*files])
print('PASS sealed cleanup222 and223')
