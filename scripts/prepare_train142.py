from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=R/'scripts/trace_train_reader142.lua';assert not p.exists()
 baseline=R/'qa/dialogue/pages130_tour049/capture_survey_used.lua';s=baseline.read_text('utf-8')
 parent=(R/'scripts/trace_booth_reader141.lua').read_text('utf-8')
 block=parent[parent.index('-- Physical PRG data reads'):parent.index('emu.addEventCallback(function()\n frame=frame+1')]
 marker='emu.addEventCallback(function()\n frame=frame+1';assert marker in s
 s=s.replace(marker,block+'\n'+marker).replace("log:close();save('trace_complete.txt'","textlog:close();log:close();save('trace_complete.txt'")
 p.write_text(s,'utf-8')
 p=R/'work/train142/preparation.json';assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps({'work':142,'scope':'Controller-only train route; no RAM/ROM/state edits. Same physical PRG reader observer as141 added to known seed-free menu observer.','base_observer':baseline.relative_to(R).as_posix(),'base_observer_sha256':sha(baseline),'reader_observer_sha256':sha(R/'scripts/trace_train_reader142.lua'),'inputs_sha256':sha(R/'config/menu_train_001.json')},indent=2)+'\n','utf-8');print('prepared train142 controller-only observer')
if __name__=='__main__':main()
