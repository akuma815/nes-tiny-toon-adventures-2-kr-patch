# 작업174 — 기존PNG 차이 오프라인 출처 대조

새 실행 없이 종료된162/163 자료의 frame04410 PNG를 대조했다. 양쪽 environment exit0·trace_complete(10500/18000)·현재049 ROM/개인Mesen SHA·사용Lua/설정/입력 파일을 확인했다. 같은 초기 입력과 적응입력4644행이 같고 첫 입력 차이는4645다.4410의 RAM/PPU/OAM/매핑/core상태5쌍은 바이트 동일하며 native frameCount/ppu.frameCount는4410이다.

종료 environment에 고정된 각343장, 총686개의4645이전 PNG SHA를 확인한 뒤 RGB를 비교했다.342쌍 동일,4410한쌍만7326픽셀/bbox[8,0,256,189] 차이로163결과와 같다. y189..239는 양쪽RGB동일이다. 두 대상마다 자기자신을 제외한685개 저장PNG에서 동일한 복사본은 없었다. 따라서 다른 **저장된** 인접 PNG를 그대로 잘못 저장한 경우는 이 검색 범위에서 연결되지 않는다. 저장하지 않은 사이 프레임의 동일성이나 정확한 지연량을 뜻하지 않는다. 두 PNG는 CRC정상·256×240 RGB이며 메타데이터/출력프레임 식별자를 갖지 않는다. 원본PNG를 보존했다.

양쪽Lua의 snapshot 함수는 동일하고 EndFrame에서 frame을 증가시킨 뒤 PNG를 먼저 캡처하고 debug메모리를 읽는다. 작업118의2.1.1 공식소스6개는 고정트리 Git blob/SHA와 재대조했다. EndFrame 이벤트는 현재프레임 제출보다 먼저이고 screenshot 래퍼는 비동기 디코더 완료를 기다리지 않는다. 필터 복사와ApplyFilter 잠금은118의 제한대로 유지한다. 이 소스 경로는 정확한 출력 프레임 식별/스케줄 기록을 대신하지 않으며 설치바이너리 재빌드 일치 증명도 아니다. 비동기 처리 시점은 가능한 설명일 뿐 이 PNG 차이의 확정 원인이 아니다.

[보고](../qa/reports/nonplay174_capture_provenance.json), [분석기](../scripts/analyze_capture174.py). 결론: 전체prefix RGB동일 판정은 계속FAIL, 원인은미확정이다. 같은native상태만으로 시각 회귀PASS로 바꾸지 않는다.049 번역/패치 결함이 입증된 것도 아니다. 정확한 원인은 기존자료만으로 닫을 수 없으므로 유사 캡처 반복/임의sleep/PNG교체는 진행하지 않는다. 실제 플레이와 최종 품질은 사용자 담당이다.

변경은174분석스크립트·보고·인계/계획/조사/journal/canonical·manifest/audit뿐이다. ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`,173ZIP 및 모든 기존증거 불변. 정적소스/종료자료/PNG프로브 검증만 수행했고 신규ROM빌드/적용/CPU/에뮬레이터/플레이/청음/최종사람검수 없음. 재현 `python scripts/analyze_capture174.py`; 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay174_assets.json --output qa/reports/nonplay174_session.json`. 기존출력은 보호되므로 새경로를 쓰는복제로 재현한다. 사용파일SHA는manifest와실행environment에고정했다. 카페완성작업기/게시없음.

다음 작업 하나: 사용자 검수 결과를 연결할 현재049 점검표와 배포 전 남은 조건을 한 문서로 정리하고, 추가 기술 작업과 사용자 판단 항목을 구분한다.
