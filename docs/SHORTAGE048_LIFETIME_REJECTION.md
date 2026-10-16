# 작업127 —048 실제 전환 결함과 채택 보류

048을 일반티켓3 초기seed/동일controller로4200프레임 실행했다. 비교047은 이미 완료된 작업106의 동결실행을 재사용했다. Mesen/Lua/설정/입력/seed가 같고 양쪽 각1821선언파일의SHA를 대조했다. 새실행 exit0이며 원본/047/048/CSV는 보존했다. [읽기전용 정리기](../scripts/observe_shortage127.py), [결과](../qa/reports/shortage127_observation.json), [기준 실행](NORMAL3_CURRENT047_CLOSEOUT.md).

[완성2100](../qa/dialogue/shortage127_normal3048/frame_02100.png)은 ‘아쉽지만 / 티켓이 부족해!’이고 [다음보유량2700](../qa/dialogue/shortage127_normal3048/frame_02700.png)은 기존문구로 복귀한다. 실제PPU 226/227→196/197과티켓3보존을 확인했다. 그러나 [전환2004](../qa/dialogue/shortage127_normal3048/frame_02004.png)의 이전요금과 [복귀2604](../qa/dialogue/shortage127_normal3048/frame_02604.png)의 잔류거절글자가 다른글꼴로 해석되어 깨진다. 직접 실제PNG6장을 보았다. 완성화면만 정상인 후보는 채택하지 않는다. **048거부/채택047 유지**다.

native9F09→9417의 초기화는 clear 전06DF00이고,2000/2001에서226을 즉시활성화한다.2600에서는196을 즉시활성화한다. 동일 native는clear후9A7F→9417(06DF03)을2008/2607에 이미호출하므로 pointer/reader/native clear를 유지하면서 폰트선택만 이시점까지 보류할 수 있다. 기존공유폰트가 가렸던 생명주기 결함으로서 본문·통화·게임진행 조건 오류는 아니다. 캡처번호는 국소증거이며 비동기PNG의 전역시점 동일시를 하지 않는다.

302PNG중259같음/43다름, OAM302exact. RAM차이는선언폰트2바이트와출력glyphbuffer/stack에한정됐지만 이결과를 전환성공으로 표현하지 않는다. row-local차이여도 잔류글꼴혼합은 실제결함이다. 분기native시점/완성NT/정리파일SHA를 기록했으며 새CPU/build/apply는 없다. 자연전체·전역corpus·실기·PCM·사람승인/정식배포 미완료. 카페완성작업기는전체완료후다.

SHA: source `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 채택047 `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, 거부048 `8dc842a4ddb551c9762843a559a878afcd58965b18dc20d7a19d9e60bd6ca4e2`, 개발CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. SSOT문장은개발수정상태로유지하되048을채택하지않고새후보를만든다. 변경은실행QA·정리기·결과·본문서·인계/journal/canonical/manifest다.

재현: `python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_048/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_coaster_001.json --seed config/ride_normal3_seed_001.json`; 실패증거를덮어쓰지않는다. [동결자산](../manifests/shortage127_assets.json), 감사경로 `qa/reports/shortage127_session.json`.

다음 작업 하나: slot29/2B의 native clear 전에는 활성폰트를 유지하고06DF03 초기화 때 새폰트를 선택하는049 후보를 만들며 CPU경로별 사이클/ABI를 검증한다.
