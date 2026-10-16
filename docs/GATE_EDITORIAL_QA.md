# 작업91 — 성 입구047 실제 출력 검증과 채택

현재 채택본은 **dialogue_kr_poc_047**이다. [ROM](../build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes)/[IPS](../build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.ips), ROM499728바이트 SHA-25682ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10, IPS3709578b0b4a211588ee254943dbd639643e82b39af07a295cacc6979aa20f70, CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556. 원본SHAf41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d와1편참고파일 유지. 이전046과 모든 증거를 보존했다.

정적/빌드·적용: [작업90](GATE_EDITORIAL_BUILD.md)의129바이트/문장36바이트·전용175176폰트2KiB 범위,9 Expected Writes 전체 출력과원본바이트를 다시 확인했다. **작업90 재빌드 파일수 정정:8개가 아니라9개**다. 실제 build/rebuild 폴더와 동결 검증JSON의9파일 모두 byte exact다. 이전 동결 문서·기록을 수정하지 않았다. Windows IPS CLI 적용 근거는90에 있고,047 검토용xdelta 묶음은 아직 없다.

에뮬레이터: 같은 Mesen2.1.1/실행파일/Lua/설정/입력으로046과047 각각5400frames 실행, RAM 수정·상태로드 없이controller만 사용했다.396표본 중360화면 전체pixel exact,36표본의 변경은 성 입구 두 줄에 한정된다. OAM/전체상태txt/PRG·CHR주소매핑은396표본 모두 byte exact. 보호 PPU 패턴·NT/속성/팔레트도 일치하고,175176의실제PPU37표본은 각ROM폰트와 exact다. 메뉴로그2889행 전필드/실행24행 동일하다. 게임RAM 차이는 native937C reader151회 재현에서 나온scratch·buffer glyph쌍에 한정되며 스택103의4차이도 관측glyph A와같고 native IRQ/NMI의PHA를 확인했다. 스택 전체를 무조건 제외하지 않았다. [독립검증v2](../scripts/verify_gate091_v2.py), [보고서](../qa/reports/gate091_validation.json), [양쪽환경046](../qa/dialogue/gate091_castle046/environment.json)/[047](../qa/dialogue/gate091_castle047/environment.json).

직접 장면: [출력 도중1812](../qa/dialogue/gate091_castle047/frame_01812.png), [완성1920](../qa/dialogue/gate091_castle047/frame_01920.png), [첫행 지우기2106](../qa/dialogue/gate091_castle047/frame_02106.png), [다음 문단2130](../qa/dialogue/gate091_castle047/frame_02130.png)을 직접 보았다. ‘골드 티켓 4장이 있으면 / 입장할 수 있어요’의native NT 전체코드와 actual RGB 두행을 폰트비트에서 독립재구성해 exact 확인했다. font175가남아있는데 선택slot이24로 바뀐 대기·넘김도 실제검증에 포함되며 폰트수명을 slot변수 하나로 추정하지 않았다.

실패·해결: [v1 검증기](../scripts/verify_gate091.py)는 PNG 비교에서 양쪽을047 디렉터리로 지정한 실수로 변경개수 guard에 실패했다. PASS보고서는 생성되지 않았다. [실패 기록](../qa/reports/gate091_verifier_v1_observation.json)과v1을 보존하고v2에서046기준경로를 명시해 통과했다. ROM/게임실행 실패가 아니다.

미수행: 이 실행은 골드0/일반티켓10의 자연 입장불가 경로다. 자연적으로골드4를 획득한성공입장·전게임완주·전역corpus폐쇄·047신규리셋/저장상태·실기·PCM청음·최종사람검토는 주장하지 않는다. 046 검토ZIP/검토패치는 그당시CSV의 역사적자료로 남는다. 공개게시·카페완성작업기 없음.

재현: `python scripts/run_world_qa.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새046폴더 --frames 5400 --inputs config/menu_castle_001.json`;047도 같은입력/새폴더로 **순차**실행한다. 동결검증은 `python scripts/verify_gate091_v2.py`이며 보고서가이미존재하면쓰기거부한다. [동결manifest](../manifests/gate091_assets.json).

다음 작업 하나: 현재047 CSV와 실제성입구화면을 반영한 ROM 없는 사람검토HTML/ZIP을 새버전으로 만들고 데스크톱·모바일 렌더링을 검증한다.
