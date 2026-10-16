from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'config/intro_no_inputs144.json';assert not p.exists();p.write_text('[]\n','utf-8')
 p=R/'work/intro144/preparation.json';assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
 script=R/'scripts/trace_train_reader142.lua'
 p.write_text(json.dumps({'work':144,'scope':'Cold boot no-input title/intro two loops6000. Frozen142 physical PRG reader observer; no RAM/ROM/state edits.','observer_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'input':[]},indent=2)+'\n','utf-8');print('prepared intro144 no-input route')
if __name__=='__main__':main()
