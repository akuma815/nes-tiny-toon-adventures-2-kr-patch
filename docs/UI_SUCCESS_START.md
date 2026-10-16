# 교환 완료 인사·출발 — 032 / 작업32

매표소의 성공 교환 인사를 “언제든 오세요”, 놀이기구 시작을 “출발!”로 삽입했다. 등록54개 원천 중29draft/25미번역이며 전체 게임 완료율은 아니다. 원래15의 FD20 빈 둘째 행과2A의 맨 앞 literal00을 유지했다. 이전27개 초안·타이틀·성의 FA·숫자/포인터/제어코드/매크로/008 코드를 보존했다.

각 문구의 전용 font188/189 및190/191은 짝수 시작이므로 하단만 바꾸고 상단 RAM34에는 영향을 주지 않는다. 따라서 이미 화면에 있는 일본어 놀이기구 제목·설명 카드의 글리프는 그대로다. 새 prepare_ui_success_start.py/build_ui_success_start.py/verify_ui_success_start.py/verify_ui_success_start_hooks.py/make_success_start_evidence.py, plan/SSOT backup/032·재빌드/실제 0eb0c8328e9196bf8c1e008b4d8ce080d0cb9794112f3097d002b835331c4ada 적용/매표소·성 gold4 캡처와 IRQ 및 직접 화면을 보존했다.

## 검증과 한계

[독립 검증](../qa/reports/success032_validation.json)은 원본 ExpectedWrites7/중첩0,031 전체 이미지의 본문2개·font표2개·폰트4KiB 외 보존을 확인했다. font PNG/TTF 대조와 숫자 글리프 불변, native reader의 모든 호출별cycle/cursor 불변을 확인했다. 인사는30호출1932cycles, 출발은9호출919cycles다. [ABI1504/초기font720](../qa/reports/success032_hooks1504.json), 재빌드/한글·공백 경로 실제 0eb0c8328e9196bf8c1e008b4d8ce080d0cb9794112f3097d002b835331c4ada 적용도 통과했다. 최종 원본 식별 verify_source.ps1 역시 원본262160바이트와 기준 SHA256을 확인했다.

실제863화면(매표소339/성524)의 하단 현재 행 밖 픽셀 변화0,833전체화면 동일,30장 해당 행만 변경. 보호 PPU/팔레트/OAM/게임RAM 동일, 출력 버퍼 차이는 native reader replay 값 쌍으로 제한했다. 상단34/NMI 캐시3A는 원본과 같다. IRQ/NMI/PPU/mapper215827시점(매표소94596/성121231)이 정확히 같고 font값522개만 다르다. 성 참조는 전체 byte가031과 같은029 고정 실행이며 해시를 확인했다.

[실제 두 문구](../qa/dialogue/success032_actual_pages.png)는 완성 네임테이블과 frame1899/2580를 확인하고 정수4배로 직접 검토했다. 성 내부6000 상태도 직접 확인하고 이전 화면과 같았다. 두 성공 경로는 지정 RAM seed이며 자연 수집·완주의 근거가 아니다. 상단 설명 카드·다른 문구/변수·영문 그림/크레딧·전 corpus·전체 플레이·오디오/reset/savestate/실기/최종 번역·명칭 검토 및 기존 PRG·난수 영향은 남는다. 새032 도입부는 재실행하지 않았고 바이트 보존/이전027 실행 근거만 있다.

c4b40639bafba6a25a1c186c82005963ec4fecdf8d3a22308eaf1ab6643a7d67458768바이트/CHR192KiB, 분산 예약2KiB는 bank170과187의 각1KiB이다. 원본/1편/모든 이전 산출물 보존, dist비어있고 외부 게시도 없다.

## 해시·재현

- 원본 SHA256: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 032 c4b40639bafba6a25a1c186c82005963ec4fecdf8d3a22308eaf1ab6643a7d67 / 재빌드 / 실제 적용 SHA256: `c4b40639bafba6a25a1c186c82005963ec4fecdf8d3a22308eaf1ab6643a7d67`
- 0eb0c8328e9196bf8c1e008b4d8ce080d0cb9794112f3097d002b835331c4ada SHA256: `0eb0c8328e9196bf8c1e008b4d8ce080d0cb9794112f3097d002b835331c4ada`
- ba881bbffdaf4f5fa84d43f941d9166914e156358a7337c3b1bb66be8af33c86 SHA256: `ba881bbffdaf4f5fa84d43f941d9166914e156358a7337c3b1bb66be8af33c86`

[자산](../manifests/ui_success_start_assets.json), [세션 감사](../qa/reports/ui_success_start_session_20261005.json).

```powershell
python scripts/build_ui_success_start.py --output build/success032_repro_next
python scripts/verify_ui_success_start_hooks.py --build build/dialogue_kr_poc_032 --report qa/reports/success032_hooks_repro_next.json
python scripts/verify_ui_success_start.py
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_032/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/success032_points3_repro_next --frames 4500 --inputs config/menu_ticket_001.json --seed config/booth_points3_seed_001.json
```

고정 빌더/검증은 당시29draft SSOT와 명시한 빌드에 적용한다. 다음 행동 하나: 놀이기구별 상단 제목·규칙·요금 문구를 공통 상단 font로 구성하고 실제 다섯 경로를 검증한다. 바로 이어간다.
