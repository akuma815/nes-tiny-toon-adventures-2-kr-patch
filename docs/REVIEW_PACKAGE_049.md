# 작업132 — 현재049 ROM 없는 검토용 패치

[검토용 ZIP](../dist/TinyToonAdventures2_KR_Review_049_20261006.zip), [적용 보고서](../qa/reports/review049_package_final132.json), [내용·한계](../dist/TinyToonAdventures2_KR_Review_049_20261006/RELEASE_NOTES_KO.md), [Windows 안내](../dist/TinyToonAdventures2_KR_Review_049_20261006/README_적용방법.txt). 11파일/179350바이트 ZIP SHA `27404b77f6afc4a6ad8e1e51e357a89aba804b0c5631fbac5193862acb2de42e`. xdelta SHA `a2604bcddcf9b3d365218c73dc7bef9b5691e6fee539976729893b529a7de856`. 원본262160바이트 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`에서049499728바이트 SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`를 만든다.

포장/실제적용: 1편의 검증된 xdelta3.2.0/Apache2.0/Galmuri OFL 파일을 읽기 전용 복사하고 원천SHA를 보존했다. [v2 제작기](../scripts/make_review_package049_132_v2.py)와 [132 적용 검증 helper](../scripts/release_apply_helpers132.py)는 기존 helper와 같은검사를 사용하며 ZIP의 고정 타임스탬프만2026-10-06으로 기록한다. 한국어·공백 경로에서 Windows apply.cmd8검사(정상·기존출력·동일입출력·같은크기의잘못된원본·이미적용한ROM·손상패치·손상도구·무인수)와 최종ZIP 추출 재적용을 실행했다. 정상/최종ZIP 결과 모두 전체ROM 바이트가049와 같다. 도구·패치·원본·결과SHA를 적용기가 확인하고 기존파일을 덮어쓰지 않는다.

ROM/폰트PNG·TTF/에뮬레이터/검토HTML이 없는ZIP이다. 개발검토용으로 distribution_eligible=false/human_final_review=false를 유지했다. 현재049의 한문장수정/실패048/009폰트수명 해결·page38cycles/idleRNG·CPU차이/129130의 bounded runtime 범위를 설명했다. 별도 [049검토자료](TRANSLATION_REVIEW_049.md)가 있다. 정식배포·카페작업기·외부게시 없음.

시행착오: v1은 기존 검증보고서의 세부 PASS 상태를 단순PASS로 가정해 출력 전 실패했다. [관측](../qa/reports/review049_package132_v1_observation.json)과 v1을 보존하고 v2가 정확한 기존상태상수를 검사했다. 준비용inline Python은 PowerShell인용오류로 파일쓰기전 중단했고 파일 기반 prepare_package132_v2.py로 전환했다. 실패로 생긴패키지나ROM은 없다.

새게임실행/직접장면은 수행하지 않고 동일SHA049의128정적CPU·빌드/실제IPS,129부족/성공,130다른page,131검토자료 근거를 연결했다. 자연전체플레이·모든분기·전역corpus·HOWTO/PAUSE/commonPOW 실제소비·현재049reset/state·실기·PCM·사람최종검토는 미완료다. 기존047ZIP을 변경하지 않았다.

변경 파일: 새dist폴더11파일/ZIP/ZIP.sha256; qa/apply의각적용검사·실패용복사·추출재적용결과; qa/reports 최종보고서/v1관측; scripts/make_review_package049_132.py/v2,prepare_package132_v2.py,release_apply_helpers132.py,seal_package132.py; 상세/정본 인계·README·오늘journal. 원본/1편/현재ROM/CSV 보존. 개별SHA는동결manifest에기록한다.

재현: `python scripts/make_review_package049_132_v2.py`는기존출력을거부한다. ZIP을새폴더에풀고 `apply.cmd "깨끗한 일본판 원본.nes" "새 결과.nes"`를실행한다. 원본과결과SHA를위값과대조한다.

다음 작업 하나: 현재049의 전용226/227 부족 대사 도중 같은 빌드 저장·복원과 console reset 후 재진입을 별도 실행해 글꼴 복귀와 native 출력 계약을 검증한다.
