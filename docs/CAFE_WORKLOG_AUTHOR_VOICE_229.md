# 인계 2026-10-09

## 작업229 — 네이버 카페 작업기 작성자 말투 적용

- 요청/목표: 사용자가 제공한 ‘1편에 이어2편 공개·어린 시절 티켓을 몰랐던 기억·이번 작업 중 엔딩을 본 소감’의 말투를 작업기 전체에 적용한다.
- 현재 기준 원본·빌드·완료 조건: 최종 게임 릴리즈는 기존 v1.0 그대로다. 내부 빌드 번호 제거본을 독자용 원천으로 삼고 문서·이미지 설명·HTML·게시ZIP만 개정한다. 사용자 실제화면·완주1차 완료 보고와 배포후 검증 예정 상태를 유지한다.
- 완료 결과: 도입부4문단과8개 본문 섹션을 작성자1인칭으로 다듬었다. ‘했습니다’를 기본으로 ‘처음엔/그런데/더라고요/네요’를 섞고, ㅠㅠ·ㅎㅎ·:)는 소감에 소량 사용했다. 원문 ‘1편에 이에’는 ‘1편에 이어’로 교정했다. 검수 설명의 제3자 문서식 표현을 작성자 시점으로 바꿨다. 어린시절 경험과 엔딩 소감은 이번 사용자 제공 내용이다.
- 변경 파일·산출물·SHA-256: [작업기HTML](../workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html), [카페 복사본문](../workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/카페_복사용_본문.txt), MD·업로드안내·공개 출처JSON·검증표PNG와 게시ZIP. [게시 ZIP](../dist/TinyToon2_KR_Worklog_AuthorVoice_20261009.zip)은 ROM없는14파일, SHA `91aa811d1ac61fb3ecb2c049936c9a8b6336840c22c8fda75ee6f7a8a76a3a5a`. 원본2편 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`; 전체 변경파일·개별 SHA는 `manifests/nonplay229_assets.json`.
- 재현 명령·환경: Windows PowerShell/Python/격리headless Edge. `python -B scripts/publication229_author_voice.py`는 출력에SHA256봉인이 있으면 거부한다. 기존 봉인에 덮어쓰지 않는다. 리더 재검사는 새QA경로로 `python -B scripts/render_publication229.py --input workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html --output qa/publication/author_voice_recheck`.
- 정적 검증: 도입부가TXT/MD/HTML에 반영됐고 공개 본문·캡션에서 내부 빌드번호가 없는지 검사했다. 그림01~07은이전PNG와같다. 그림08은작성자시점 설명표만 다시 구성했다. 실제 캡처 원천·정적복원 원천SHA는 같다. HTML내장8PNG가파일PNG와같고 ZIP CRC·목록·모든추출바이트 비교PASS. 이전228봉인49파일·이전공개ZIP·원본·번역CSV·최종ROM·게임배포ZIPSHA유지PASS.
- 빌드/패치 적용 검증: 새 게임 빌드·패치적용은 미수행. 기존 결과의해시보존만 검사했다.
- 에뮬레이터 실행 검증: 미수행. 실제플레이는사용자담당이며새자동플레이를하지않았다.
- 직접 장면 시각 검증: 게임장면을새로실행·검수하지않았다. 문서리더PC1280×1000/모바일390×844 렌더PASS;8이미지로드·본문폭·확대/Escape닫기·JS오류없음PASS. PC·모바일첫화면과수정검증표를직접확인했다. 모바일제목은단어단위로줄바꿈하고ㅠㅠ·ㅎㅎ가갈라지지않도록처리했다.
- 미수행·미해결·기각한 설명: 작업기는카페편집말투이며1·2편기술지침의별도교육문서는수정하지않았다. 카페계정접속·실제게시는미수행. 렌더수정후첫재검사에서DevTools포트파일잠금으로실패했다. 실패한자체격리프로필의Edge프로세스11개만종료하고포트파일준비대기를보완한새렌더러로재검사PASS. 사용자의브라우저·Mesen은조작하지않았다. 처음렌더는수정전표시근거,최종근거는author_voice229_verified다. 자체렌더프로필3개만검증된절대경로로삭제했고기존자료는보존했다.
- 작업기용 근거: `qa/reports/publication229_sources.json`, `publication229_verified.json`, `publication229_cache_cleanup.json`, `qa/publication/author_voice229_verified/render_report.json`과4PNG. 과거실제캡처·제작원천·크레딧정적복원·설명표의구분을유지한다. HOWTO·PAUSE·POW·서명·미연결배경·진단STAGE SELECT원문유지결정은같다.
- 다음 작업 하나: 사용자가 본문·그림을 카페 편집기에 배치하고, 배포 이후 제보의 ROM 해시·환경·직전 행동·화면을 수집한다.
