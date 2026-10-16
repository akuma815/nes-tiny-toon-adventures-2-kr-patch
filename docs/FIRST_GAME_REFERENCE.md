# 1편에서 확인한 최신 참고 기준

2026-10-04에 실제 파일을 읽었다. 메모리의 2026-10-01 타이틀 PoC 상태보다 이후 작업이 존재했다. 1편은 읽기 참고만 했으며 문서·ROM·번역·도구·설정·QA를 수정하지 않았다.

- [1편 현재 재개 문서](<../../Tiny Toon Adventures/docs/HANDOFF.md>): 작업18 카페용 작업기까지 작성, 실제 업로드는 미수행.
- [1편 날짜별 인계](<../../Tiny Toon Adventures/docs/HANDOFF_2026-10-04.md>): 작업17 v1.0.1, 작업18 공개 자료.
- [당근 교환 대기 중 폰트 오류](<../../Tiny Toon Adventures/docs/HAMTON_FONT_FIX_2026-10-04.md>): 공통 작별 직전 대기가 건너뛴 페이지의 폰트를 선택했다. 직전 폰트를 대기 중 유지하도록 수정.
- [카페 작업기 문서](<../../Tiny Toon Adventures/docs/PUBLIC_WORKLOG_2026-10-04.md>): 실제 캡처/구조도16장과 복사용 본문·HTML·업로드 안내, 증거 범위 구분.

2편에서 계승할 것은 원본 보존·작업 원천/빌드/QA 분리·Expected Write·실제 적용·근거가 연결된 작업기다. 특히 문장 완성 외에 폰트 수명의 중간 상태를 확인한다. 1편 22문단·26root·mapper23 주소·폰트 후크·창 크기·영문 유지·다른 AI 담당 결정은 2편에 자동 적용하지 않는다.

이 문서가 참조한 파일의 현재 SHA-256은 [초기 세션 감사](../qa/reports/initial_session_20261004.json)의 `first_game_references`에 기록한다. 1편 배포 ZIP도 읽기 해시만 확인했다.

## 타이틀 구현을 위한 추가 참고

1편 `docs/POC_TITLE.md`, `scripts/extract_title.py`, `scripts/build_title.py`, `scripts/title_ips.py`를 읽었다. 생성형 PNG를 동결해 색상/타일로 변환하는 흐름을 계승하고 범용 IPS 적용기를2편 scripts에 복사했다. 2편 타이틀은 CHR17/19의 화면 중간 전환, CHR 내부 배치 스트림, 별도 숫자2 스프라이트를 쓰므로1편 주소·RLE를 사용하지 않았다. 확인 결과는 [2편 타이틀 문서](POC_TITLE.md)에 기록했다. 이번 작업 후 초기 감사의1편 문서·원본·배포 ZIP 해시도 그대로임을 검사했다.
