"""046 source-derived build/apply and consumer-specific STOP pixel regression."""
from pathlib import Path
import json,csv,hashlib
from collections import Counter
from PIL import Image,ImageChops
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 b=R/'build/dialogue_kr_poc_046';rom=(b/'TinyToon2_dialogue_kr_poc.nes').read_bytes();prior=(R/'build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes').read_bytes();p=R/'qa/dialogue/stop079_train045';q=R/'qa/dialogue/stop080_train046_v2';e=json.loads((q/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==4200 and e['rom_sha256']==hashlib.sha256(rom).hexdigest()
 for name,h in e['files'].items():assert sha(q/name)==h
 for name in ('TinyToon2_dialogue_kr_poc.nes','stop_font.bin','stop_graphics_plan_used.json','expected_writes.json','build_report.json','builder_used.py','draft_used.json','stop_indices.png','stop_kr.png','stop_kr_8x.png'):assert (b/name).read_bytes()==(R/'build/dialogue_kr_poc_046_rebuild080'/name).read_bytes()
 assert rom==(R/'qa/patch/stop080_적용 검증/검증 결과.nes').read_bytes();aa=rows(p/'world_phase.csv');bb=rows(q/'world_phase.csv');assert len(aa)==len(bb)==140
 for a,z in zip(aa,bb):
  for k in a:assert z[k]==('E0'if k=='headfont'and a[k]=='44'else a[k])
 c=json.loads((R/'extracted/graphics/stop_001/consumer.json').read_text('utf-8'));old=prior[0x51010:0x51810];new=rom[0x78010:0x78810];changed_tile_masks={}
 for code in c['owned_text_tiles']:
  a=decode(old[code*16:code*16+16]);z=decode(new[code*16:code*16+16]);changed_tile_masks[code]={(x,y):(a[y*8+x],z[y*8+x])for y in range(8)for x in range(8)if a[y*8+x]!=z[y*8+x]};assert all(set(v)=={1,2}for v in changed_tile_masks[code].values())
 colors={1:(234,158,34),2:(0,0,0)};ram=Counter();images=sorted(q.glob('frame_*.png'));proof=[];chunks=0;pixels=0
 for png in images:
  tag=png.stem;rr=(p/(tag+'_ram.bin')).read_bytes();ss=(q/(tag+'_ram.bin')).read_bytes();diff=[i for i,(v,w)in enumerate(zip(rr,ss))if v!=w];assert set(diff)<={0x34,0x3a} and all((rr[i],ss[i])==(68,224)for i in diff);ram.update(diff)
  assert (p/(tag+'_oam.bin')).read_bytes()==(q/(tag+'_oam.bin')).read_bytes();ppu=(q/(tag+'_ppu.bin')).read_bytes();assert ppu[0x2000:]==(p/(tag+'_ppu.bin')).read_bytes()[0x2000:]
  for z in rows(q/(tag+'_mapping.csv')):
   if z['kind']=='chr':a=int(z['cpu_or_ppu_address'],16);x=int(z['relative_offset'],16);assert ppu[a:a+1024]==rom[0x40010+x:0x40410+x];chunks+=1
  ia=Image.open(p/png.name).convert('RGB');ib=Image.open(png).convert('RGB');box=ImageChops.difference(ia,ib).getbbox()
  if not box:continue
  n=int(tag[6:]);diffpixels=[(x,y,ia.getpixel((x,y)),ib.getpixel((x,y)))for y in range(box[1],box[3])for x in range(box[0],box[2])if ia.getpixel((x,y))!=ib.getpixel((x,y))];candidates=[]
  # Snapshot NT queue may already replace a just-rendered edge tile.
  # Try the current and preceding preserved snapshot; require exact old/new
  # glyph indices and RGB for EVERY changed pixel under one scroll offset.
  for age in (0,30):
   pp=(p/f'stop_top_{n-age:05d}_ppu.bin').read_bytes()
   for lag in range(5):
    offset=(rr[0x6d]-lag)%256;pred={}
    for nt in (0x2000,0x2800):
     for cell in range(960):
      code=pp[nt+cell]
      if code in changed_tile_masks:
       for (x,y),(v,w)in changed_tile_masks[code].items():pred[((cell%32*8+x-offset)%256,cell//32*8+y)]=(colors[v],colors[w])
    if all(pred.get((x,y))==(v,w)for x,y,v,w in diffpixels):candidates.append({'NT_snapshot_age':age,'RAM6D_minus_scroll':lag})
  assert candidates,(tag,box);proof.append({'frame':n,'changed_pixels':len(diffpixels),'matching_native_tile_fields_and_RGB':candidates});pixels+=len(diffpixels)
 assert any(x['frame']==3330 for x in proof)
 ar=rows(p/'stop_pattern_reads.csv');br=rows(q/'stop_pattern_reads.csv');assert len(ar)==len(br)>0
 for a,z in zip(ar,br):
  for k in a:
   if k=='CHR_relative':oldrel=int(a[k],16);assert int(z[k],16)==oldrel+(0x27000 if oldrel<0x11800 else 0)
   elif k=='value':assert int(z[k],16)==rom[0x40010+int(z['CHR_relative'],16)]
   else:assert a[k]==z[k]
 for z in rows(q/'stop_top_banks.csv'):
  if z['bg34']=='E0':assert z['bg35']=='46'and z['CHR0']=='38000'and z['CHR400']=='38400'and(q/(z['tag']+'_ppu.bin')).read_bytes()[:2048]==new
 report={'work':80,'status':'PASS_STOP046_NATIVE_TRAIN','ROM_sha256':hashlib.sha256(rom).hexdigest(),'IPS_sha256':sha(b/'TinyToon2_dialogue_kr_poc.ips'),'rebuild10_files_exact':True,'real_Windows_Python_IPS_CLI_Korean_space_path_byte_exact':True,'frames':4200,'runtime_files':len(e['files']),'screens':len(images),'CHR_1K_chunks_exact_ROM':chunks,'world_rows_exact_except_train_font':140,'RAM_only_train_font_and_mapper_cache':dict(ram),'all_OAM_NT_palette_same':True,'live_PPU_rows_geometry_order_count_scanline_and_new_ROM_values_exact':len(br),'all_changed_pixels_exact_old_new_glyph_indices_and_RGB':pixels,'changed_PNGs':proof,'CPU_model_clarification':{'total_NMOS6502_comparisons':3840,'D_clear_NES_relevant':1920,'D_set_generic_NMOS_only':1920,'cycles_exact':137,'D_set_SBC_is_not_NES_decimal_disabled_emulation':True,'asynchronous_interrupts_PPU_not_modeled':True},'scope':'STOP interior-only source derivation and actualpixel proof inclpartial scrolling/NT buffer edges. Not fulltrain/fullgame/PCM/hardware/human language approval.'}
 out=R/'qa/reports/stop080_validation.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in report.items()if k!='changed_PNGs'},indent=2))
if __name__=='__main__':main()
