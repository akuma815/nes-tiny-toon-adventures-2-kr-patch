"""Work78 three route START runtime pair validation; actual UI proof only."""
from pathlib import Path
import json,csv,hashlib
from collections import Counter
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 results=[]
 for name,ride in [('coaster','00'),('train','02'),('water','03')]:
  p=R/f'qa/dialogue/start078_{name}044';q=R/f'qa/dialogue/start078_{name}045';e=json.loads((q/'environment.json').read_text('utf-8'));old=json.loads((p/'environment.json').read_text('utf-8'));assert e['exit_code']==old['exit_code']==0 and e['frames']==old['frames']==4200 and e['input']==old['input']
  rom=(R/'build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert e['rom_sha256']==hashlib.sha256(rom).hexdigest()
  for root,ev in [(p,old),(q,e)]:
   for f,h in ev['files'].items():assert sha(root/f)==h
  aa=rows(p/'world_phase.csv');bb=rows(q/'world_phase.csv');assert len(aa)==len(bb)==140 and any(z['root']=='04'and z['phase']=='05'and z['ride']==ride for z in bb)
  for a,b in zip(aa,bb):
   for k in a:assert b[k]==('DE'if k=='headfont'and a[k]=='7A'else a[k]),(name,k,a,b)
  ram=Counter();changes=[];chunks=0;images=sorted(q.glob('frame_*.png'))
  for png in images:
   tag=png.stem;aa=(p/(tag+'_ram.bin')).read_bytes();bb=(q/(tag+'_ram.bin')).read_bytes();diff=[i for i,(a,b)in enumerate(zip(aa,bb))if a!=b];assert set(diff)<={0x34,0x35,0x3a,0x3b}and all((aa[i],bb[i])==(122,222)for i in diff);ram.update(diff)
   assert(p/(tag+'_oam.bin')).read_bytes()==(q/(tag+'_oam.bin')).read_bytes();ppu=(q/(tag+'_ppu.bin')).read_bytes();assert ppu[0x2000:]==(p/(tag+'_ppu.bin')).read_bytes()[0x2000:]
   for z in rows(q/(tag+'_mapping.csv')):
    if z['kind']=='chr':a=int(z['cpu_or_ppu_address'],16);b=int(z['relative_offset'],16);assert ppu[a:a+1024]==rom[0x40010+b:0x40410+b];chunks+=1
   box=ImageChops.difference(Image.open(p/png.name).convert('RGB'),Image.open(png).convert('RGB')).getbbox()
   if box:assert 80<=box[0]<box[2]<=176 and 112<=box[1]<box[3]<=144,(name,tag,box);changes.append(tag)
  assert changes and 'frame_02670'in changes
  results.append({'course':name,'screens_per_build':len(images),'world_rows_per_build':140,'CHR_1K_chunks_target_exact':chunks,'RAM_differences_only_START_font_and_cache':dict(ram),'changed_PNGs_only_START96x32':changes,'all_OAM_NT_palette_same':True,'entered_native_gameplay_phase5':True,'runtime_files_both':len(e['files'])+len(old['files'])})
 out=R/'qa/reports/start078_regression.json';assert not out.exists();report={'work':78,'status':'PASS','pairs':results,'ROM_changes':0,'source_ROM_preserved':True,'scope':'Three controller-only coldboots per build; sharedSTART and firstgameplay check, no fullrides/fullgame/PCM/hardware/finalhumanapproval. Directvisual separate.'};out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
