# 작업126 — 일반 티켓 부족 안내의048 후보 빌드

[작업125 수동 선택](PROSE_FIDELITY_REVIEW_125.md)에 따라 MAIN_0590C만 **아쉽지만 / 티켓이 부족해!**로 수정했다. [단일편집기](../scripts/prepare_prose126.py), [새 계획](../workspace/translation/shortage_editorial_plan_126.json), [CSV 이전 백업](../backups/translation/text_ja_before_shortage126.csv). 원문·raw·reference·status를 포함한 나머지53항목과 해당 항목의 다른 필드는 보존했다. translation_ko/notes 두 필드만 바뀌며45draft/9기술공유 상태다. 사람 최종 승인은 아니다.

공유196/197과 macro88은 그대로다. 예약0 영역226/227을 전용 lower 폰트로 쓰며 slot29의 tag만196→226으로 지정했다. 두 행의20바이트 본문 범위2590C..25920, tag5762 한 바이트, 새2KiB폰트78810..79010 안에서만 기존047 대비839바이트가 바뀐다. 헤더·ROM크기499728·PRG256KiB·CHR232KiB·다른 글꼴·매퍼코드·제어/매크로 토큰을 보존했다. 새폰트의 고정macro코드39..42는 티/켓/이/공백이고 그 외 대사의 티/켓/을/공백과 독립적이다.

[빌더v2](../scripts/build_shortage126_v2.py), [빌드보고](../build/dialogue_kr_poc_048/build_report.json), [독립 검증](../qa/reports/shortage126_validation.json). page setup1152모델사례/reader23호출의 cycles/cursor가047과 같고 IRQ의 모든 주소/시점이 같다. 의도된두글꼴값 A000196→226(317cycles), A008197→227(323cycles)만 바뀐다. 초기[v1](../scripts/build_shortage126.py)은 IRQ에서 두 번째 폰트 쓰기를 허용하지 않은 guard로 출력 전에 실패했다. [관찰](../qa/reports/shortage126_v1_observation.json)을 보존하고 두 멤버를 명시하는 v2로 수정했다.

원본부터9개 Expected Writes·원본 기대바이트·비중첩·전체재구성을 확인했다. 별도048재빌드9파일이 byte exact다. 한국어/공백 경로에서 Windows Python IPS CLI를 실제 실행하여 원본에 적용한 결과도 후보048과 byte exact였다. 이는 새정식 배포묶음/apply.cmd검증은 아니다.

원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 이전채택047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, 후보048 SHA `8dc842a4ddb551c9762843a559a878afcd58965b18dc20d7a19d9e60bd6ca4e2`, IPS SHA `694597914a35d17946ee94a8fee3e466509dde36dcd468038bb22fc80d3feaa3`, 새CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 원본/1편/기존검증물은 보존한다. 현재 채택본047의 문구는 동결translation_used.csv에서 읽으며 SSOT는048 후보의 한 문장을 담는다. 과거047 검토자료는 과거문구로 보존한다.

변경은 새편집기/빌더v1,v2/검증기/계획/CSV백업과SSOT/048·재빌드9파일/한글경로적용3파일/검증·실패관찰/본문서·인계·journal·canonical/manifest다. 정적·CPU모델·build/apply까지만 검증했으며 실제048 runtime/직접장면은 다음 작업이다. 따라서 **048은 후보, 채택본은 아직047**이다. 전역corpus·전체자연게임·실기·PCM·사람검토/정식배포와카페완성작업기는 미완료다.

재현: `python scripts/build_shortage126_v2.py --output build/새폴더`; `python scripts/dialogue_ips.py apply --source "원본.nes" --patch build/dialogue_kr_poc_048/TinyToon2_dialogue_kr_poc.ips --output "새 결과.nes"`. 기존출력을덮어쓰지않는다. [동결 자산](../manifests/shortage126_assets.json), 감사 경로 `qa/reports/shortage126_session.json`.

다음 작업 하나: 047/048을 동일한 일반티켓3 seed·입력으로 실행해 slot29의 부분출력·완성·넘김·다음2B 보유량 대사에서226→196 복귀와 보호화면을 검증한다.
