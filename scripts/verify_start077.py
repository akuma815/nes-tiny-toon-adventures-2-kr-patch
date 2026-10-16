"""045 START build/apply/rebuild and natural20k regression vs044."""
from pathlib import Path
import hashlib,json,csv
from collections import Counter
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 b=R/'build/dialogue_kr_poc_045';rom=(b/'TinyToon2_dialogue_kr_poc.nes').read_bytes();q=R/'qa/dialogue/start077_cart045';p=R/'qa/dialogue/notices075_natural044';e=json.loads((q/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==20000 and e['rom_sha256']==hashlib.sha256(rom).hexdigest()
 for name,h in e['files'].items():assert sha(q/name)==h
 for name in ('TinyToon2_dialogue_kr_poc.nes','start_font.bin','start_graphics_plan_used.json','expected_writes.json','build_report.json','builder_used.py','draft_used.json','start_indices.png','start_kr.png','start_kr_8x.png'):assert(b/name).read_bytes()==(R/'build/dialogue_kr_poc_045_rebuild077'/name).read_bytes()
 assert rom==(R/'qa/patch/start077_적용 검증/검증 결과.nes').read_bytes()
 aa=rows(p/'cart_round_policy.csv');bb=rows(q/'cart_round_policy.csv');assert aa==bb and len(bb)==19999
 aa=rows(p/'world_phase.csv');bb=rows(q/'world_phase.csv');assert len(aa)==len(bb)
 for a,z in zip(aa,bb):
  for k in a:assert z[k]==('DE'if k=='headfont'and a[k]=='7A'else a[k])
 ram=Counter();changes=[];chunks=0;images=sorted(q.glob('frame_*.png'))
 for png in images:
  tag=png.stem;rr=(p/(tag+'_ram.bin')).read_bytes();ss=(q/(tag+'_ram.bin')).read_bytes();diff=[i for i,(a,z)in enumerate(zip(rr,ss))if a!=z];assert set(diff)<={0x34,0x35,0x3a,0x3b}and all((rr[i],ss[i])==(122,222)for i in diff);ram.update(diff)
  assert(p/(tag+'_oam.bin')).read_bytes()==(q/(tag+'_oam.bin')).read_bytes();pp=(q/(tag+'_ppu.bin')).read_bytes();assert pp[0x2000:]==(p/(tag+'_ppu.bin')).read_bytes()[0x2000:]
  for z in rows(q/(tag+'_mapping.csv')):
   if z['kind']=='chr':a=int(z['cpu_or_ppu_address'],16);x=int(z['relative_offset'],16);assert pp[a:a+1024]==rom[0x40010+x:0x40410+x];chunks+=1
  ia=Image.open(p/png.name).convert('RGB');ib=Image.open(png).convert('RGB');box=ImageChops.difference(ia,ib).getbbox()
  if box:
   assert 80<=box[0]<box[2]<=176 and112<=box[1]<box[3]<=144,(tag,box);changes.append(tag)
 assert 'frame_02670'in changes
 report={'work':77,'status':'PASS_START045_NATURAL_CART','ROM_sha256':hashlib.sha256(rom).hexdigest(),'IPS_sha256':sha(b/'TinyToon2_dialogue_kr_poc.ips'),'rebuild_all10_files_byte_exact':True,'real_Windows_Python_IPS_CLI_Korean_space_path_byte_exact':True,'runtime_files':len(e['files']),'frames':20000,'screens':len(images),'CHR_1K_chunks_exact':chunks,'controller_rows_exact044':19999,'world_rows_equal_except_START_font':len(bb),'all_OAM_NT_palette_unchanged':True,'RAM_only_START_font_and_mapper_cache':dict(ram),'changed_PNGs_only_START96x32':changes,'scope':'Natural cart first-round clear/timeup/home preserved; not full3 rounds/fullgame or other3 start routes yet. Directvisual separate; finalhumanapproval pending.'}
 out=R/'qa/reports/start077_validation.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
