from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
for b in ['047','049']:
 rom=(R/f'build/dialogue_kr_poc_{b}/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert rom[0x4000e:0x40010]==bytes.fromhex('5b fa') and rom[0x3fd28]==0x40
p=R/'scripts/run_irq136.py';assert not p.exists();s=(R/'scripts/run_branch_seed_qa.py').read_text('utf-8').replace("('trace_branch_seed_v1.lua','trace_branch_seed_irq_v1.lua')","('trace_irq136.lua',)");s=s.replace("'scope':'Controlled ticket/point branch QA. Numerical state intentionally seeded; direct visual review separate; no full playthrough.'","'scope':'Narrow1999..2002 nativeIRQ entry/body/idle discrimination; declared initial1000 ticket3 seed only, no ROM/state/PC changes or screenshot/PCM/fullplay claim.'");p.write_text(s,'utf-8')
p=R/'config/coaster_before2400_136.json';assert not p.exists();events=json.loads((R/'config/menu_coaster_001.json').read_text('utf-8'));p.write_text(json.dumps([e for e in events if e['frame']<2400],indent=2)+'\n','utf-8')
