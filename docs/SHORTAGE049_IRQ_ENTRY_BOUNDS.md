# 작업136 — 부족 분기의 IRQ 진입 전 시점 차이

[최종검증](../qa/reports/irq136_validation.json), [읽기전용 관측](../scripts/trace_irq136.lua), [입력/실행계획](../work/irq136/run_plan.json).047/049 각2400프레임,기존과같은1000 티켓3 seed/Start·오른쪽·A입력을실행했다.1999..2002의nativeIRQ vector FA5B,body~FD18,매퍼ack/reload,대기FE53..FE5E를추적했다.원본vectorFFFE=FA5B/RTI FD18을실행전정적확인했다.각2400counter행이134의해당prefix와전부같아추가관측에따른진행변경이없음을대조했다.

두실행각4IRQ·133명령씩총532명령의PC/opcode/순서·X/Y/SP가같다.각body의순수402/실제406cycles(FD18실행직전까지)는같으며각각단하나4cyclegap이있다.실제PPU read응답을버스callback에서기록해모델에순서대로공급했고각실제opcode/A/X/Y/SP/6실행flags가각자CPU모델과일치했다.B/U표현normalize는행별기록하며현재/047의A와overflow차이를정확한전체CPU동일로표현하지않는다.이번4cyclegap은DMC타입을아직관측하지않았으므로원인을추정확정하지않는다.

2001의모든133 IRQ명령은현재049에서1cycle빠르지만entry기준상대시각은같다.현재/047의타입동일144 port값·순서중19행(F000/F008 ack/reload2 +134의매퍼/PPU17)이해당IRQ전체와함께1cycle/3dot빠르다.다른3IRQ는절대시각도같다.하나의명령만PPUscanline경계를넘어도절대PPUclock=scanline×341+dot로3dot차이가같음을검사했다.

**차이는IRQ handler 진입전부터있다.**2001양쪽의마지막대기opcode는FE58 ADC RAM1B,저장복귀PC는FE5A다.047 ADC시작59608335→vector59608345,04959608334→59608344로각10cycles다.현재대기명령이미1cycle빠르고opcode에서IRQvector까지같은간격이므로1cycle빠른IRQ handler/새로바뀐interrupt수락지연이라고부르지않는다.IRQ발생신호의정확한assert시각을직접관측한것은아니다.그이전대기의3/4cycle짧은지연은다음DMC/PCM-CDL 관측으로구분한다.

원본/1편/현재049/CSV불변,ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`.새build/apply/PNG·장면직접육안·실기/청음없음.129130화면회귀·135첫홈DMC 경계정정은각범위에서계승한다.

인계v1 작성기의triplequote종료누락으로문서쓰기전SyntaxError가발생했고바로뒤감사는manifest부재로중단했다. v1과관측을보존하고v2에서종료인용을교정했다. 검증/runtime자료변경없음.

변경:scripts/trace_irq136.lua,prepare_irq136.py,run_irq136.py,run_irq_pair136.py,verify_irq136.py,seal_irq136.py;config/coaster_before2400_136.json;qa/dialogue두실행의IRQ RAM/읽기/opcode/port/idle/counter와환경;work/irq136계획/log;qa/reports/irq136_validation.json;상세/정본인계·README·오늘journal.새실행/검증은모두첫시도완료했으며기존실패스트림보존.개별SHA는동결manifest.

재현:`python scripts/run_irq_pair136.py`, `python scripts/verify_irq136.py`는기존출력거부.단일새출력은run_irq136.py에ROM,2400frames,config/coaster_before2400_136.json,config/ride_normal3_seed_001.json,trace_irq136.lua를지정한다.사람검토false/현재개발049 유지/배포승인false.전역CPU·IRQ·게임난수동일성/모든경로·자연전체·전역corpus·HOWTO/PAUSE/POW·실기/PCM·최종사람검토 미완료.카페완성작업기·외부게시없음.

다음 작업 하나: 1999..2002 대기opcode의3/4cycle 지연을 실제DMC cursor/read·새PCM-CDL로구분하고,2001의IRQ이전1cycle위상차이에기여한같은sample읽기를대조한다. ROM변경없이같은티켓3 입력을사용한다.
