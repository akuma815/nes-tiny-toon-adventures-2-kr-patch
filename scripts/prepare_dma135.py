from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'scripts/run_dma135.py';assert not p.exists();s=(R/'scripts/run_dmc_qa_v2.py').read_text('utf-8')
s=s.replace("a.script.name=='trace_dmc_v2.lua'","a.script.name=='trace_dma135.lua'").replace('TTA2_DMC062_','TTA2_DMA135_')
s=s.replace("'scope':'Native world boundary investigation with explicitly recorded continuous controller intervals; no full-playthrough claim.'","'scope':'Natural first home page924 instruction/DMC window920..926 discrimination only. No currency/RAM/state writes, new scene/fullplay/PCM claim.'")
p.write_text(s,'utf-8')
p=R/'config/first_home135.json';assert not p.exists();p.write_text(json.dumps([{'frame':720,'duration':8,'button':'start'}],indent=2)+'\n','utf-8')
