"""Independent glyph reconstruction; actual pairwise HUD labels/values/IRQ ABI."""
import json,csv,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from extract_title_png import encode,decode
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_bytes()
def j(p):return json.loads(read(p).decode('utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
SPECS=[('LIFE','체력',[0x22,0x23,0x24],24,190,3),('SCORE','점수',list(range(0x27,0x2c)),80,190,3),('TIME','시간',[0x7c,0x7d,0x7e],176,190,3),('PTS.','점',[0x7a,0x7b],152,195,2),('TICKET','티켓',[0x30,0x31,0x32],88,203,2),('G.TICKET','금티켓',[0x3c,0x3d,0x3e,0x3f],176,203,3)]
def verify_pair(ref,new,oldrom,rom,labels=True):
 a,b=j(f'qa/dialogue/{ref}/environment.json'),j(f'qa/dialogue/{new}/environment.json');assert a['exit_code']==b['exit_code']==0 and a['rom_sha256']==sha(oldrom) and b['rom_sha256']==sha(rom)
 for key in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'):assert a[key]==b[key],(new,key)
 if 'seed' in a:assert a['seed']==b['seed'] and a['seed_file_sha256']==b['seed_file_sha256']
 oldfiles=sorted((R/f'qa/dialogue/{ref}').glob('frame_*.png'));newfiles=sorted((R/f'qa/dialogue/{new}').glob('frame_*.png'));assert oldfiles and [f.name for f in oldfiles]==[f.name for f in newfiles];changed=label_pixels=number_pixels=0;codes=set(c for spec in SPECS for c in spec[2]);anchors=set();anchor_by_frame={}
 irqref=ref.replace('_survey','_irq').replace('_native','_irq');irqref=irqref+'_irq' if ref.endswith('_pause') else irqref
 if labels and ref.startswith('game039_'):
  for row in rows(f'qa/dialogue/{irqref}/irq_phase.csv'):
   if row['pc']=='FCF1' and row['address']=='A008':assert row['value']=='7D';anchor_by_frame[int(row['frame'])]=int(row['scanline'])+1
 for f in newfiles:
  tag=f.stem;ram=read(f'qa/dialogue/{ref}/{tag}_ram.bin');assert ram==read(f'qa/dialogue/{new}/{tag}_ram.bin');assert read(f'qa/dialogue/{ref}/{tag}_oam.bin')==read(f'qa/dialogue/{new}/{tag}_oam.bin');p=read(f'qa/dialogue/{ref}/{tag}_ppu.bin');np=read(f'qa/dialogue/{new}/{tag}_ppu.bin');assert p[0x2000:]==np[0x2000:];old=Image.open(R/f'qa/dialogue/{ref}/{f.name}').convert('RGB');image=Image.open(f).convert('RGB');diff=ImageChops.difference(old,image);box=diff.getbbox()
  if not box:continue
  assert labels and box[1]>=190 and box[3]<=240,(new,tag,'outsideHUD',box);assert ram[0x18]==4,(new,tag,'gameplay root');changed+=1;frame=int(tag[6:]);anchor=anchor_by_frame[frame-1] if anchor_by_frame else 190;anchors.add(anchor);dy_anchor=anchor-190
  assert old.crop((0,0,256,anchor)).tobytes()==image.crop((0,0,256,anchor)).tobytes()
  # Same field pixels and therefore same visible values, after intentional2px shift.
  for key,(x0,y0,x1,y1) in {'hearts':(24,195,72,211),'score':(88,195,152,203),'time':(176,195,232,203),'ticket_x_number':(112,203,144,211),'gold_x_number':(208,203,224,211)}.items():
   y0+=dy_anchor;y1+=dy_anchor;assert old.crop((x0,y0,x1,y1)).tobytes()==image.crop((x0,y0+2,x1,y1+2)).tobytes(),(new,tag,key);number_pixels+=(x1-x0)*(y1-y0)
  colors={}
  for source,ko,cs,x0,y0,ink in SPECS:
   header=source in ('LIFE','SCORE','TIME');start=3 if header else 0;height=5 if header else 8
   for cy in range(height):
    for cx in range(len(cs)*8):
     v=decode(oldrom[0x5f010+cs[cx//8]*16:0x5f020+cs[cx//8]*16])[(start+cy)*8+cx%8];rgb=old.getpixel((x0+cx,y0+cy+dy_anchor));colors.setdefault(v,set()).add(rgb)
  assert all(len(v)==1 for v in colors.values()),(new,tag,'native label palette consistency');assert all(v in colors for v in (1,2,3));colors={v:next(iter(rgb)) for v,rgb in colors.items()}
  for source,ko,cs,x0,y0,ink in SPECS:
   header=source in ('LIFE','SCORE','TIME');start=1 if header else 0;height=7 if header else 8;ny=(y0 if header else y0+2)+dy_anchor;predicted=Image.new('RGB',(len(cs)*8,height))
   for cy in range(height):
    for cx in range(len(cs)*8):
     v=decode(rom[0x73810+cs[cx//8]*16:0x73820+cs[cx//8]*16])[(start+cy)*8+cx%8];predicted.putpixel((cx,cy),colors[v])
   assert image.crop((x0,ny,x0+len(cs)*8,ny+height)).tobytes()==predicted.tobytes(),(new,tag,'Korean native label pixels',source);label_pixels+=len(cs)*8*height
  # Within observed visible HUD NT, changed glyphs belong only to these labels.
  allowed=set()
  for source,ko,cs,x0,y0,ink in SPECS:
   row=24 if source in ('LIFE','SCORE','TIME') else 25 if source=='PTS.' else 26
   for c,code in enumerate(cs):addr=0x2c00+row*32+x0//8+c;assert p[addr]==code;allowed.add(addr)
  for addr in range(0x2f00,0x2fc0):
   if p[addr] in codes:assert addr in allowed,(new,tag,'unowned HUD glyph use',hex(addr))
  # Full post-frame CHR data belongs to recorded bank mapping, including controls.
  ma,mb=rows(f'qa/dialogue/{ref}/{tag}_mapping.csv'),rows(f'qa/dialogue/{new}/{tag}_mapping.csv');assert len(ma)==len(mb)
  for aa,bb in zip(ma,mb):
   for k in ('kind','cpu_or_ppu_address','mem_type'):assert aa[k]==bb[k]
   if aa['relative_offset']!=bb['relative_offset']:assert aa['kind']=='chr' and (aa['relative_offset'],bb['relative_offset']) in (('1F000','33800'),('1F400','33C00'))
   if bb['kind']=='chr':
    start=int(bb['cpu_or_ppu_address'],16);off=int(bb['relative_offset'],16);assert np[start:start+1024]==rom[0x40010+off:0x40410+off];oldoff=int(aa['relative_offset'],16);assert p[start:start+1024]==oldrom[0x40010+oldoff:0x40410+oldoff]
 return {'ref':ref,'new':new,'screens':len(newfiles),'HUD_changed':changed,'whole_unchanged':len(newfiles)-changed,'native_header_anchor_y':sorted(anchors),'anchor_source':'source actual FCF1/A008 IRQ scanline+1 at preceding frame; coaster probe actual independent IRQ survey','Korean_label_pixels_exact':label_pixels,'native_heart_number_multiplier_pixels_exact_after2px_shift':number_pixels,'RAM_OAM_NT_palette_equal':True,'outside_HUD190_240_changed_pixels':0}
def verify_irq(ref,new,oldrom,rom):
 a,b=j(f'qa/dialogue/{ref}/environment.json'),j(f'qa/dialogue/{new}/environment.json');assert a['exit_code']==b['exit_code']==0 and a['rom_sha256']==sha(oldrom) and b['rom_sha256']==sha(rom)
 for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'):assert a[k]==b[k]
 if 'seed' in a:assert a['seed']==b['seed']
 aa,bb=rows(f'qa/dialogue/{ref}/irq_phase.csv'),rows(f'qa/dialogue/{new}/irq_phase.csv');assert len(aa)==len(bb);font=fine=0
 for x,y in zip(aa,bb):
  for k in ('frame','kind','pc','address','scanline','dot','cycles'):assert x[k]==y[k],(new,k,x,y)
  wanted=x['value']
  if x['pc']=='FCED' and x['address']=='A000':assert x['value']=='7C';wanted='CE';font+=1
  elif x['pc']=='FCF1' and x['address']=='A008':assert x['value']=='7D';wanted='CF';font+=1
  elif x['pc']=='FCDB' and x['address']=='2006':assert x['value']=='2F';wanted='0F';fine+=1
  assert y['value']==wanted,(new,x,y)
 assert font and fine;return {'new':new,'timing_rows_exact':len(aa),'font_write_values_only':font,'fineY_write_values_only':fine}
def main():
 manifest=j('manifests/source_rom.json');source=read(manifest['path']);assert sha(source)==manifest['sha256'];old=read('build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes');rom=read('build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes');plan=j('build/dialogue_kr_poc_040/hud_plan_used.json');assert rom==read('build/dialogue_kr_poc_040_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 040/TinyToon2_hud040_applied.nes');font=bytearray(old[0x5f010:0x5f810]);face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);used=set()
 for name,text,cs,x0,y0,ink in SPECS:
  w=len(cs)*8;field=[1]*(w*8);left=(w-len(text)*8)//2;dy=1 if name in ('LIFE','SCORE','TIME') else 0
  for i,c in enumerate(text):
   im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);bits=[int(v>127) for v in im.get_flattened_data()];assert any(bits) and not any(bits[56:])
   for y in range(7):
    for x in range(8):
     if bits[y*8+x]:field[(y+dy)*w+left+i*8+x]=ink
  for i,code in enumerate(cs):assert code not in used;used.add(code);font[code*16:(code+1)*16]=encode(bytes(field[y*w+i*8+x] for y in range(8) for x in range(8)))
 assert bytes(font)==rom[0x73810:0x74010] and bytes(font).hex()==plan['font_hex'];expected=bytearray(old);expected[0x73810:0x74010]=font;assert old[0x3fce4:0x3fce7]==b'\xa9\x2f\xa2' and old[0x3fcf8:0x3fcfb]==b'\xa2\x7c\x8e';expected[0x3fce5]=15;expected[0x3fcf9]=206;assert expected==rom;expected=bytearray(source);owned=set()
 for w in j('build/dialogue_kr_poc_040/expected_writes.json'):
  p,n=w['file_offset'],w['length'];assert not owned.intersection(range(p,p+n));owned.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==rom and read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_040/translation_used.csv');assert all(font[c*16:(c+1)*16]==old[0x5f010+c*16:0x5f020+c*16] for c in range(128) if c not in used)
 checks=[];irqs=[]
 for ride in ('coaster','cart','train','water'):
  new=f'game040_{ride}_survey_v2' if ride=='coaster' else f'game040_{ride}_survey';checks.append(verify_pair(f'game039_{ride}_survey',new,old,rom));irqs.append(verify_irq(f'game039_{ride}_irq',f'game040_{ride}_irq',old,rom))
 checks.append(verify_pair('game039_castle_native','game040_castle_native',old,rom));irqs.append(verify_irq('game039_castle_irq','game040_castle_irq',old,rom));checks.append(verify_pair('booth039_native','game040_booth_regression',old,rom,False));checks.append(verify_pair('booth039_intro','game040_intro_regression',old,rom,False));checks.append(verify_pair('booth039_credits','game040_credits_regression',old,rom,False));checks.append(verify_pair('game039_coaster_pause','game040_coaster_pause',old,rom));irqs.append(verify_irq('game039_coaster_pause_irq','game040_coaster_pause_irq',old,rom))
 report={'work':44,'status':'PASS','ROM_sha256':sha(rom),'IPS_sha256':sha(read('build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.ips')),'rebuild_and_real_CLI_apply_exact':True,'independent_TTF_native_font_reconstruction_exact':True,'all_prior_bytes_except_two_fixed_IRQ_operands_and_reserved_font206_207_unchanged':True,'CPU_ABI_cases':j('build/dialogue_kr_poc_040/build_report.json')['IRQ_CPU_ABI_cases'],'screens':sum(x['screens'] for x in checks),'checks':checks,'actual_IRQ_rows_exact':sum(x['timing_rows_exact'] for x in irqs),'IRQ':irqs,'geometry':'FineY2→0 provides7 visible Korean header rows; all native body pixels/values2px lower, black bottom margin also2px lower. IRQ scanline/dot/CPU cycles unchanged. Owned HUD y190..239. Gameplay y0..189 unchanged.','limits':['Castle access uses declared initial gold4 seed; not naturally earned/cleared','Four controller-only ride paths are not full playthroughs; results consumer remains unresolved','Static source-registered45draft/9technical counts exclude separate graphics; whole corpus coverage remains unresolved','Whole audio/reset/savestate/physicalconsole/finalhumanreview unperformed'],'next_action':'Inspect native results initialization and CHR24A0B consumer'}
 (R/'qa/reports/game040_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ('checks','IRQ')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
