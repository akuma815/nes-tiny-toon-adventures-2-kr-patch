"""Resolve native RTS byte from actual trampoline before starting new probe."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
for build in ['047','049']:
 b=(R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert b[0x25455]==0x60 and b[0x25458]==0xea
p=R/'scripts/trace_live_page134_v2.lua';assert not p.exists();s=(R/'scripts/trace_live_page134.lua').read_text('utf-8').replace('0x25448','0x25445').replace('0x9448,0x9448','0x9445,0x9445');p.write_text(s,'utf-8')
p=R/'scripts/run_live134_v2.py';assert not p.exists();s=(R/'scripts/run_live134.py').read_text('utf-8').replace("('trace_live_page134.lua',)","('trace_live_page134_v2.lua',)");p.write_text(s,'utf-8')
p=R/'scripts/run_pair134_v2.py';assert not p.exists();s=(R/'scripts/run_pair134.py').read_text('utf-8').replace("'work/live134'","'work/live134_v2'").replace("scripts/run_live134.py","scripts/run_live134_v2.py").replace("live134_normal{seed}_{build}","live134v2_normal{seed}_{build}").replace("scripts/trace_live_page134.lua","scripts/trace_live_page134_v2.lua");p.write_text(s,'utf-8')
obs=R/'qa/reports/live134_v1_observation.json';assert not obs.exists();obs.write_text(json.dumps({'work':134,'status':'FAILED_RETURN_CALLBACK_TARGET','reason':'9448 is padding NOP, not page RTS. Native verified RTS is9445/file25455. Pending page pair therefore did not close; owned hidden private Mesen PID22116 was stopped after verifying executable and live134 commandline. No user emulator touched. First pair failed; other3 were not executed.','v2_static_guard':'Both047/049 ROM RTS9445=60 and padding9448=EA confirmed before new runs','environment_sha256':hashlib.sha256((R/'qa/dialogue/live134_normal3_047/environment.json').read_bytes()).hexdigest()},indent=2)+'\n','utf-8')
