# 작업214 — 불필요한 펼친 산출물·캐시 정리와 검증 보관

사용자 요청으로 **2편 프로젝트 내부**의 불필요한 펼친 산출물과 임시 캐시를 정리했다. 1편 프로젝트·사용자 Mesen·브라우저 프로필·세이브는 건드리지 않았다. 원본 ROM, 번역 CSV, 폰트/그래픽/작업기 원천, 스크립트/도구/라이선스, 인계/보고/매니페스트, 기준051, 현재062 및 재현 체인, 기존 배포ZIP은 보존했다. 번역·ROM 수정이나 새 플레이는 없다.

| 구분 | 결과 |
|---|---:|
| 과거 산출물 압축 보관 경로 | 565개 실행 폴더 |
| 보관 인덱스 | 1,026,906개 파일 / 원래 9,164,302,503바이트 |
| 중복 제거 후 고유 바이트 객체 | 147,740개 |
| 압축 보관본 | 729,260,032바이트 |
| 문서 링크·실행 설정 등 원래 경로에 복원 | 25,935개 / 694,163,991바이트 |
| 펼친 과거 파일 제거 | 1,000,970개 |
| 재생성 가능한 캐시 제거 | 3,593개 / 291,032,336바이트 |
| 위 두 구분 제거 합계 | 1,004,563개 |
| 대상 파일 바이트 절감(보관본 포함·새 원장/스크립트 용량 제외) | 8,031,908,734바이트 / 7.48GiB |

**정리 예외1개:** [복원 검증 PNG](../qa/dialogue/booth039_font_probe/frame_00030.png)는 복원 도구로 실제 생성해 SHA 일치/기존 동일 파일 처리까지 확인했다. 검증 후 이 사본의 직접 `Remove-Item` 삭제 명령은 정확한 경로를 지정해도 도구 정책에 차단됐다(`blocked by policy`, 상세 사유 미제공). 다른 방식으로 이 거부를 우회하지 않았으며 이 파일 하나는 남겼다. 위 제거 수량/절감 바이트에서 제외했다. [복원 검증·차단 기록](../qa/reports/cleanup214_restore_smoke_completed.json).

별도로 검증이 끝난 임시 전체목록/계획과 복원용 스테이징을 제거했다. 실제 디스크 할당량은 작은 파일의 클러스터 크기 때문에 표의 논리적 바이트와 다를 수 있다. 모든 제거 경로는 절대경로가 2편 프로젝트 경계 안에 있는지 확인했다. 링크/재분석 지점과 변경된 캡처 폴더는 제거를 거부하도록 했다.

처음 PowerShell `Remove-Item` 방식과 단일 디렉터리 삭제는 대량 소파일 처리에 느려 정리 프로세스만 중단하고 이어받았다. 완료 원장은 유지했고, 두 중단 지점의 남은5,199개/3,428개 파일은 보관 인덱스와 SHA를 다시 비교했다. [첫 재개 검증](../work/cleanup214/resume_verified.json)과 [병행 재개 검증](../work/cleanup214/resume_parallel_verified.json)을 통과한 뒤 같은 PowerShell 안에서 경계 검증된 절대경로를 Windows/.NET으로 삭제했다. 최종 방식은 서로 겹치지 않는 실행 폴더 최대4개만 병행 삭제하고, 완료 기록/원래 경로 복원은 순서대로 처리했다. 사용자 Mesen이나 다른 프로세스는 중단하지 않았다.

**과거 개발 ROM과 프레임의 유일한 바이트는 삭제하지 않았다.** [비공개 압축 보관본](../qa/archive/cleanup214_history.sqlite) SHA `19f0f4739c4f89548325747fbc9f5b8415172ef315aa2f07bc9ff576595035e1`에 파일 경로→SHA→zlib 객체로 보존했다. 모든 고유 객체를 풀어 SHA/크기를 검사하고 SQLite 무결성을 확인한 뒤 펼친 폴더를 정리했다. 이 파일에는 개발 ROM이 있으므로 **카페 배포 패키지에 넣지 않는다.** 카페용 공개 배포자료는 기존 ROM 없는 `dist` ZIP이다.

필요한 과거 경로를 복원한다. 다른 내용의 기존 파일에는 덮어쓰기를 거부한다.

```powershell
python -B scripts/restore_archive214.py --file build/dialogue_kr_poc_037/ui_korean_page_mapping.json
python -B scripts/restore_archive214.py --prefix build/text11_candidate_060
python -B scripts/restore_archive214.py --verify
python -B scripts/audit_cleanup214.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
```

두 번째 명령은 거부 후보060을 조사할 때만 사용하는 예다. 보관 경로는 `entries.path` 인덱스에서 검색할 수 있다. [삭제 실행 원장](../qa/reports/cleanup214_deletion.json), [간결한 계획](../work/cleanup214/deletion_plan.json), [임시파일 정리](../qa/reports/cleanup214_temporary_removed.json), [원래 경로의 보존 해시](../manifests/cleanup214_retained_live.json)를 남겼다. 실행 스크립트는 이미 완료된 삭제를 다시 실행하지 않는다.

**검증:** [보관 검증](../qa/reports/cleanup214_archive.json)은 고유 객체 전수 디코딩/해시·스테이징 해시 검증이다. [정리 후 감사](../qa/reports/cleanup214_audit.json)는 197~213 고정근거를 현재 파일 또는 검증된 보관 인덱스에 연결해 검사했고, 원래 경로에 복원한 25,935개 해시, 원본2편/CSV/051/062/IPS/독립재빌드와 ZIP 해시, ZIP CRC·68개 페이로드, 프로젝트 문서/리뷰 링크를 확인했다. 과거 고정 보고/매니페스트는 바꾸지 않았다. 예전 물리적 경로를 요구하는 감사는 관련 경로를 복원한 뒤 실행한다. 현재 보관 상태 검사는 `audit_cleanup214.py`를 사용한다. 이 감사는 원본 바이트 검증이며 새 빌드·새 패치 적용·새 CPU 실행·실제 게임 실행 결과는 아니다. 기존 211/212의 빌드/CPU/Windows 적용 결과와 실제062 미검수 상태는 유지된다.

일반 플레이·062 장면/가독성/비동기NMI·IRQ 검수는 사용자 담당이다. 062는 미채택 개발 후보이며 기준051은 유지한다. 기존 HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT 원문 유지 결정은 같다. 프로젝트 외부의 만료된 과거 스킬 캐시 링크와 1편의 예전 원본 경로 부재는 정리 전부터 있었던 사항이며 이번 삭제 대상이 아니다.

변경 파일: 정리 조사·계획·보관·복원·삭제·감사·인계 스크립트, 비공개 SQLite 보관본, 새 정리 원장/보존 해시, 정본 README/HANDOFF/계획/AGENTS와 날짜별 인계·journal. 종전 근거의 물리적 일부 경로가 보관 상태가 된 것을 정본에 반영했다. 현재062의 ROM 해시 `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`, 배포ZIP 해시 `377b16522c31f3516869c9eb14acb925799ceeefa1051d06508570770bc19575`는 그대로다.

다음 작업 하나: 사용자의 새062 실제 화면 검수 결과를 받아 보고된 글꼴·줄바꿈·소거·전환 결함을 별도 새 빌드로 수정한다.
