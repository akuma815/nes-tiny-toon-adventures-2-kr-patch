# 작업60 — 급류 복귀 첫 APU 차이의 관찰 모델

[최종 V3 검증](../qa/reports/audio_phase060_validation_v3.json), [PNG 동일성 가정 오류](../qa/reports/audio_phase060_png_model_error.json), [NMI 개수 가정 오류](../qa/reports/audio_phase060_NMI_count_model_error.json), [고정2.1.1 CPU/APU 소스·SHA](../work/audio_phase_001/source.json). ROM/SSOT 변경0이다. [작업59 보존 감사](../qa/reports/audio059_session.json)도 통과했다.

Mesen2.1.1 NesApu Serialize의Map 형식은EndFrame/catchup을 건너뛴다. Run은 경과한 AP Ucycle을 채널에 반영한다. CPUdebugPeek4015는PeekRam/GetStatus이고 현재 에뮬레이션 스레드에서는Run을 호출한다. 일반 bus ReadRam4015의IRQ clear와 다르다. 이 비버스 디버그 읽기를 명시적 관찰 개입으로 환경에 기록했다. RAM/PC/ROM 쓰기·seed·savestate는 없다. source에는 별도ApuFrameCounter.cpp가 없고 header 구현을 보존했다.

원본/043 급류를 같은 controller로4,800프레임 새로 실행했다.4200..4500의11개 시점에서 raw state를 기록하고 디버그peek으로APU를 현재CPU시점까지 갱신한 뒤 같은 상태를 다시 기록했다. 읽기 전후 CPUcycle·모든non-APU상태·RAM/PPU/OAM은 같다. 두 실행은 각각 작업59 자기 기준의 모든audio 쓰기(시점까지 포함)와world 필드 및 화면시점RAM/PPU/OAM이 정확히 같다.

동기화 후11관찰의 사각파·삼각파·노이즈·DMC outputLevel/lastOutput 등 출력 값은 모두 같았다. 첫4관찰의APU는 모든키가 같고4320부터7관찰은DMCtimer/bitsRemaining만 다르다. 해당 관찰 모두silenceFlag=true·bytesRemaining=0이다. 이전 raw의noise/triangle/output 차이를 그대로 실제 출력 결함으로 해석할 수 없음을 확인했다. 무음 DMC 내부위상이 남아 있으므로 미래 PCM 또는 모든 시점의완전동등성을 주장하지 않는다. 이 근거만으로 ROM 타이밍을 수정하지 않았다.

4000..4600에서실제FE83 NMI를600쌍 기록했다.4255에는양쪽 모두NMI 실행이없다. 창의601개 프레임에NMI가매번있다는초기검증기 가정은 오류였고 V2/SHA/실패를보존한후 V3는실제600쌍을 확인했다.4299부터진입cycle이달라졌고 NMI가중단한PC는양쪽모두FE53..FE5C의동일한native RNGidleloop다. FE52..FE5E의13바이트도같다. CPU가다른명령어경계에서NMI에들어가는사실을확인했으나모든나중cycle차이의인과를완전히증명했다고하지않는다.

처음 검증기는 모든PNG가 자기 기준과byteexact라고가정해 실패했다. 일본판2장/0433장만 다르며 모두peek을시작하기전(1113/1167,3000/3180/3240)이다. 해당시점의RAM/PPU/OAM은모두byteexact다. 각 차이의픽셀과bbox를 별도오류보고에 보존했고 이실행에서는별도렌더프레임 관계를확정하지않았다. 전체PNG동일성이나직접시각검토통과를주장하지않는다. 관찰 이후에는PNG도 자기기준과같다.

총3,740실행파일 SHA를검증했다. 이 작업은정적APU/CPU소스확인·새에뮬레이터실행·관찰개입이벤트·자기기준음향/기계데이터 비교다. 새ROM 빌드/적용·실제청음·새장면직접육안검토는수행하지않았다. [실행기](../scripts/run_audio_phase_qa.py) `--rom <원본 또는043> --output qa/dialogue/<새ID> --frames 4800 --inputs config/menu_water_001.json`, [Lua](../scripts/trace_audio_phase_v1.lua), [V3](../scripts/verify_audio_phase060_v3.py), 기각한[V1](../scripts/verify_audio_phase060.py)/[V2](../scripts/verify_audio_phase060_v2.py)를보존한다.

현재043ROM SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a, SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 미수행: 이전157개 raw차이 모두의동기화, 미래DMC실제fetch/PCM/청음, 자연전체완주/실기/최종사람검토. 개발판55/사람검토56/원본/1편/모든실패·증거를보존하며외부게시하지않았다.

다음 작업 하나: **기존급류9,000프레임의157개 raw차이를포함하는모든후속관찰을동기화해, 동일음향이벤트와출력상태의보존범위를확장한다.** 계속한다.
