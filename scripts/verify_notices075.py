"""044 natural controller-only route vs preserved043 work72 trajectory."""
from pathlib import Path
import hashlib,json,csv
from collections import Counter
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 q=R/'qa/dialogue/notices075_natural044';p=R/'qa/dialogue/cart072_body_v4';e=json.loads((q/'environment.json').read_text('utf-8'));rom=(R/'build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert e['exit_code']==0 and e['frames']==20000 and e['rom_sha256']==hashlib.sha256(rom).hexdigest()
 for name,h in e['files'].items():assert sha(q/name)==h,name
 old=rows(p/'cart_round_policy.csv');new=rows(q/'cart_round_policy.csv');assert len(new)==19999 and new==old[:len(new)]
 old=rows(p/'world_phase.csv');new=rows(q/'world_phase.csv');assert new==old[:len(new)] and new[-1]['root']=='08'and new[-1]['life']=='03'and new[-1]['history']==new[-1]['gold']=='00'
 images=list(q.glob('frame_*.png'));chunks=0;ram=Counter();compared=0;changedimages=[]
 for png in sorted(images):
  tag=png.stem;ppu=(q/(tag+'_ppu.bin')).read_bytes()
  for z in rows(q/(tag+'_mapping.csv')):
   if z['kind']=='chr':a=int(z['cpu_or_ppu_address'],16);b=int(z['relative_offset'],16);assert ppu[a:a+1024]==rom[0x40010+b:0x40410+b];chunks+=1
  if not(p/png.name).exists():assert tag=='frame_20000';continue
  a=(p/(tag+'_ram.bin')).read_bytes();b=(q/(tag+'_ram.bin')).read_bytes();diff=[i for i,(v,w)in enumerate(zip(a,b))if v!=w];assert set(diff)<={0x39,0x3f} and all((a[i],b[i])==(62,220)for i in diff);ram.update(diff)
  oam=(p/(tag+'_oam.bin')).read_bytes();assert oam==(q/(tag+'_oam.bin')).read_bytes();assert(p/(tag+'_ppu.bin')).read_bytes()[0x2000:]==ppu[0x2000:]
  ia=Image.open(p/png.name).convert('RGB');ib=Image.open(png).convert('RGB');box=ImageChops.difference(ia,ib).getbbox()
  if box:
   changedimages.append(tag);cells=[tuple(oam[i:i+4])for i in range(0,256,4)if oam[i]<230 and 0xc1<=oam[i+1]<=0xdb];assert cells;boxes=[(x,y-3,x+8,y+19)for y,t,at,x in cells]
   for y in range(box[1],box[3]):
    for x in range(box[0],box[2]):assert ia.getpixel((x,y))==ib.getpixel((x,y))or any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in boxes),(tag,x,y)
  compared+=1
 assert 'frame_05010'in changedimages and 'frame_19110'in changedimages
 report={'work':75,'status':'PASS_NATURAL_NOTICES_AND_HOME_RETURN','ROM_sha256':e['rom_sha256'],'frames':20000,'runtime_files':len(e['files']),'input_policy_rows_exact043':19999,'world_snapshots_exact043':len(new),'screens':len(images),'compared_screens':compared,'CHR_1K_chunks_exact_ROM':chunks,'all_OAM_NT_palette_preserved':True,'RAM_only_notice_bank_latch_mapper_cache':dict(ram),'changed_PNGs_only_within_notice_sprite_boxes':changedimages,'natural_next_round_frame':5010,'natural_timeup_frame':19110,'final_world':new[-1],'scope':'Coldboot controller-only, no RAM/ROM/PC/life/currency/state changes. First round naturally cleared and second round timed out. Not all3 rounds/fullgame/human language approval; directvisual performed separately.'}
 out=R/'qa/reports/notices075_natural.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
