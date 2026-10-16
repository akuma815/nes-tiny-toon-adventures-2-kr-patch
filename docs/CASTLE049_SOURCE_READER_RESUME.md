# 작업149 — 성 입장 실제 읽기 검증 재개

[실행 계획](../work/gatereader149/resume_plan_20261007.json), [검증 보고서](../qa/reports/gatereader149_validation.json), [직접 화면](../qa/reports/gatereader149_visual.json), [재개 실행](../scripts/resume_gate_reader149.py), [검증 코드](../scripts/verify_gate_reader149.py).

2026-10-07 사용자 “다시 진행”으로 작업을 재개했다. 완료된148 normal49/047의 동결 환경 및3154개 선언 파일 해시를 다시 확인해 재사용했다. 중단된049의685개 파일은 보존하고 새049_resume에6000프레임을 실행했다. 아직 없던 gold4/047·049는 각9000프레임 새로 실행했다. 동결094 입력과1000프레임 초기 통화 seed를 사용했으며 자연 획득이나 자연 성 완주 검증이 아니다.

normal49는524개, gold4는786개 whole PNG·PPU·OAM·mapping 일치. 실제CHR10480개1KiB 조각은 현재ROM과 같다. actual PRG 읽기222/179건의 주소·값·PC·프레임·문맥·순서가 각각047과 일치했다. 모든읽기PC의 B1 06 명령과 물리주소→원천unit를 검증했다. normal49의 cycle차는184건0/9건1/29건2; gold4는134건0/35건38/10건76이다. 전체CPU·IRQ·RNG·오디오 동일성을 주장하지 않으며 RAM22/IRQstack·CPU/bus차이는 보고서에 유지했다.

성명0F·주의16·골드요금17·부족18·작별19·일반50제안1A·질문1B·환영1C·설명22·제목28의 원천 전체바이트를 실제읽기로 확인했다. 고정/매크로 native reader가 확장한13개 경로별 페이지의 모든줄과 font154/173/175/177/179/181/185/193/196 실제NT를 연결했다. 1A는 FA 동적숫자가 있어 zero-RAM reader의 전줄NT 주장에서 제외했다. 실제PNG에는 일반티켓50장 제안이 읽히며 원천읽기는 완전하다. normal49/골드0 그대로 지도복귀(root8), gold4/normal10 그대로 성게임(root4/phase5/course4)이 확인됐다.

7개 실제PNG에서 골드요금·부족·50장제안·작별·환영·제목/설명/출발·게임HUD를 직접 검토했다. 사람 문체·명칭·그림 최종승인은 false이다.

변경: resume_gate_reader149.py, verify_gate_reader149.py, seal_gate_reader149.py, work/gatereader149 계획/log, 새QA3폴더, 최종·시각보고서, 상세·날짜별인계·journal·README·SURVEY·PLAN·HANDOFF, manifest/audit. 원본·1편·중단148·역사증거·ROM·CSV 보존. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`.

재현: `python scripts/resume_gate_reader149.py` 후 `python scripts/verify_gate_reader149.py`. 실행계획과QA가 존재하면 거부하므로 재현시 새작업ID/출력을 지정해야 한다. 원본 검증 `powershell -File scripts/verify_source.ps1` PASS. 정적/동결SHA·명시seed runtime·실제reader/CHR/NT·whole화면대조·직접7PNG PASS. 신규build/apply/state/reset/청음/실기 미수행. 자연전체완주·global corpus·HOWTO/PAUSE/POW 소비·사람최종·정식배포 미완료. 카페용 완성기사나 외부게시 없이 근거를 journal에 기록한다.

다음 작업 하나: 현재049 티켓부족 경로를 실제 PRG 읽기 관측기로 실행하여 변경한 MAIN0590C의 원천 바이트·전용226/227 폰트·완성문·clear를 연결한다.
