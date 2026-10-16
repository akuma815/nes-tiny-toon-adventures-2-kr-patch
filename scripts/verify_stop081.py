"""Three046 other courses match preserved045 visible/core/mapping exactly."""
from pathlib import Path
import hashlib,json,csv
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 results=[];rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes'
 for course in ('coaster','cart','water'):
  p=R/('qa/dialogue/start077_cart045'if course=='cart'else f'qa/dialogue/start078_{course}045');q=R/f'qa/dialogue/stop081_{course}046';e=json.loads((q/'environment.json').read_text('utf-8'));prior=json.loads((p/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==4200 and e['rom_sha256']==sha(rom)and e['input']==prior['input']
  for n,h in e['files'].items():assert sha(q/n)==h
  pictures=sorted(q.glob('frame_*.png'));checked=0
  for png in pictures:
   tag=png.stem
   for ending in ('.png','_ram.bin','_oam.bin','_ppu.bin','_mapping.csv'):assert(q/(tag+ending)).read_bytes()==(p/(tag+ending)).read_bytes(),(course,tag,ending);checked+=1
  ww=rows(q/'world_phase.csv');assert ww==rows(p/'world_phase.csv')[:len(ww)] and len(ww)==140
  if course=='cart':policy=rows(q/'cart_round_policy.csv');assert policy==rows(p/'cart_round_policy.csv')[:len(policy)] and len(policy)==4199
  assert any(z['root']=='04'and z['phase']=='05'for z in ww)
  results.append({'course':course,'screens_exact':len(pictures),'PNG_RAM_OAM_PPU_mapping_files_byte_exact':checked,'world_rows_exact':140,'target_runtime_files':len(e['files']),'natural_gameplay_entry':True,'baseline':p.relative_to(R).as_posix()})
 report={'work':81,'status':'PASS','ROM_changes':0,'target_ROM_sha256':sha(rom),'courses':results,'scope':'046 CHR expansion other3 course coldboots preserve complete capturedvisible/core/mapping files; not whole rides/game/PCM/hardware/finalhumanapproval'};out=R/'qa/reports/stop081_regression.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
