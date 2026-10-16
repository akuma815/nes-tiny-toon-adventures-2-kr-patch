# 작업129 —049 부족·성공 분기의 실제 폰트 수명

[검증기v2](../scripts/verify_clear129_v2.py), [실행 결과](../qa/reports/clear129_validation.json), [049 build](LOWER_FONT_POST_CLEAR_049_BUILD.md). 새049 일반티켓3/4 초기seed 실행을각4200프레임완료했다. 비교는동결106/107의현재047 실행을재사용했으며각1821파일/설정·Lua·입력·seedSHA를확인했다. 원본·1편·ROM·CSV·실패048은보존했다.

부족분기는native2000/2001 pre-clear(phase00)에서196을유지하고2008 post-clear(phase03)에226으로선택했다. [2004 이전요금](../qa/dialogue/clear129_normal3049/frame_02004.png)이047과byte exact이고, [2025 부분출력](../qa/dialogue/clear129_normal3049/frame_02025.png)·[2100 완성](../qa/dialogue/clear129_normal3049/frame_02100.png)은정상이다.2600 pre-clear때226을유지해 [2604 남은글자](../qa/dialogue/clear129_normal3049/frame_02604.png)가올바르게지워지고2607 이후196으로복귀한다. [2700 보유량](../qa/dialogue/clear129_normal3049/frame_02700.png)은047과byte exact다. NT두행은아쉽지만/티켓이부족해로공백까지확인했고티켓3을보존했다.048에서보였던이전/다음글꼴혼합을해결했다.

성공분기는4→0차감/slot2A포인터9910 ‘출발!’/root18=4·phase54=5 실제진입을유지한다. [2100 출발](../qa/dialogue/clear129_normal4049/frame_02100.png), [3000 플레이](../qa/dialogue/clear129_normal4049/frame_03000.png)를확인했다. 자연적으로초기4티켓을얻거나전체코스를완주한증거는아니다.

부족302PNG중261같음/41변경은수정된둘째행(x80..151,y179..186)만이다. 첫행·티켓접두16픽셀·기존그림/몸체/팔레트를보호했다. 성공302전체PNG/PPU/OAM은047과같다. 두경로의OAM604·mappedCHR4832조각·native init호출의ID/포인터/실제프레임/분기/금액 등은같다. 직접실제PNG7장을봤으며사람최종검토가아니다. 비동기PNG한계와국소비교시점을구분한다.

RAM22·idleCPU A/flags·IRQ저장stack/bus 값은같다고주장하지않는다. 고정bankFE53의19cycle loop는매반복22에1+1B를더한다. page마다38cycles추가로두반복을덜돌며다음완료snapshot의1B와국소EndFrame라벨을사용해호출시counter값을추론했다. 이가중차이모델은양쪽302표본,604개22차이에맞았다. 이는새helper-entry의직접1B/cycle telemetry가아닌스냅샷추론이다. 실제PC/totalcycle/SP/X/Y와기타state키·보호RAM은명시된범위에서같고,출력buffer/font와idle연관값만다르다. 전게임/RNG결과가동일하다는증명은아니다.

v1검증기는coldboot전체에SP255를강제하여거절됐다. [관찰](../qa/reports/clear129_v1_observation.json)/[v1](../scripts/verify_clear129.py)보존, v2에서는짝SP동일성을검증했다. 실제캡처/ROM은바뀌지않았다. 정적·실runtime·PPU/NT/CHR·pixel·직접장면검증이고이번새build/apply는없다. globalhelper변경의다른pageQA전**049후보/채택047**유지다.

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 후보049SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 변경은실행QA2폴더·검증v1,v2/실패관찰·보고·본문서/인계/journal/canonical/manifest다. 자연전체·전역corpus·실기·PCM·사람검토/배포와카페완성작업기는미완료다.

재현: `python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_coaster_001.json --seed config/ride_normal3_seed_001.json`; 성공은`config/world_coaster_ticket4_seed_001.json`을사용한다. 새출력만지정한다. [동결자산](../manifests/clear129_assets.json), 감사경로 `qa/reports/clear129_session.json`.

다음 작업 하나: 049의 타이틀/9도입문단·홈선택/매표소·성입구·크레딧을동결된각기준실행과대조해 global helper 회귀를검증한뒤개발채택여부를결정한다.
