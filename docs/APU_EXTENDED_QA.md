# 작업61 — 급류 APU 동기화 범위 확대와 위상 차이

[검증 보고](../qa/reports/audio_sync061_validation.json), [두 실행 환경](../qa/reports/audio_sync061_runs.json), [작업60 보존 감사](../qa/reports/audio_phase060_session.json). 원본/043을9,030프레임씩 실행하고4200..9000의161개 시점에 작업60과 같은 명시적 비버스debugPeek4015를 수행했다. 기존157개 raw차이 시점을 모두 포함한다. controller/peek 외 임의RAM/PC/ROM/체력/금액/phase 쓰기나savestate는 없다.

두 새 실행은 각각 자기 작업59 기준의9,000프레임까지 audio 쓰기 시점/값/순서와world 모든 필드, 화면시점RAM/PPU/OAM이byteexact다.161회읽기 전후CPUcycle·non-APU상태·RAM/PPU/OAM도 같다. 관찰개입을 일반controller-only와 혼동하지 않는다.7,832실행파일SHA를 확인했다. 새 빌드/패치적용·직접육안검토·청음은 수행하지 않았다.

동기화 후APU4관찰은 모두 같고 나머지157은 내부위상이 다르다.143관찰의DMC는무음/bytesRemaining0,14관찰은재생중이다. **161관찰 중146개는 하나 이상의채널 출력값도 다르다.** DMC분류는DMC활동상태일 뿐이고, 무음DMC분류에서도triangle/noise출력위상은다를 수 있다. 첫11관찰의 작업60결과를후속전체구간으로확대하지 않는다. 삼각파/노이즈/DMC의 위상과출력차이 전체를 보고에 보존했다. 오디오가byte단위로동일하다거나 음질결함이발생했다고 단정하지 않는다. 실제PCM/청음은 미수행이다.

원본music engine/nativebank3C/3D16KiB(file18010..1C010)와04338,010..3C,010, native3E DMC/data8KiB(1C010..1E010→3C010..3E010)를 전체byteexact/SHA로 비교했다. **음악 엔진과효과음 데이터24KiB는 그대로다.** 작업59의88,164쌍 오디오쓰기 값/순서/프레임보존도유효하다. 이것은PCM/파형 동일성을 뜻하지 않는다. 번역작업에 따른instruction/NMI시점차이와관찰갱신모델의 영향을 기록하며 원인모두를증명한것으로표현하지 않는다. 이확인만으로ROM타이밍을수정하지 않았다.

재현: [순차 실행기](../scripts/run_audio_phase_extended_suite.py), [단일 실행기](../scripts/run_audio_phase_extended_qa.py) `--rom <원본 또는043> --output qa/dialogue/<새ID> --frames 9030 --inputs config/menu_water_001.json`, [V2 관찰Lua](../scripts/trace_audio_phase_v2.lua), [검증기](../scripts/verify_audio_sync061.py). 오래된보고/폴더를덮어쓰지않는다. sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a, SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. ROM/SSOT변경0이다.

미수행/미해결: 실제DMCfetch 바이트/PCM/청음/모든음향/전체자연완주/실기/최종사람검토. 오디오확인상태는‘레지스터와데이터보존 통과, 출력위상차이 기록, 음질미확정’이다. 개발판55와사람검토56은동결해보존하고외부게시하지않았다.

다음 작업 하나: **새 ROM 식별명과초기PCM-CDL0인실행에서 실제DMC샘플읽기와typed PCM-CDL을연결해 소비바이트보존을확인한다.** 위상차이·청음미수행한계는계속유지한다.
