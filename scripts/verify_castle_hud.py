"""Native castle gameplay HUD, actual before/after pixel protection; source039/current043."""
from verify_game_hud import R,read,j,sha,rows,SPECS,decode,Image,ImageChops
import json,csv
def verify_pair(ref,new,oldrom,rom,labels=True):
 a,b=j(f'qa/dialogue/{ref}/environment.json'),j(f'qa/dialogue/{new}/environment.json');assert a['exit_code']==b['exit_code']==0 and a['rom_sha256']==sha(oldrom) and b['rom_sha256']==sha(rom)
 for key in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'):assert a[key]==b[key],(new,key)
 if 'seed' in a:assert a['seed']==b['seed'] and a['seed_file_sha256']==b['seed_file_sha256']
 allold=sorted((R/f'qa/dialogue/{ref}').glob('frame_*.png'));allnew=sorted((R/f'qa/dialogue/{new}').glob('frame_*.png'));assert [f.name for f in allold]==[f.name for f in allnew];oldfiles=[];newfiles=[]
 for aa,bb in zip(allold,allnew):
  aRAM=read(f'qa/dialogue/{ref}/{aa.stem}_ram.bin');bRAM=read(f'qa/dialogue/{new}/{bb.stem}_ram.bin')
  if aRAM[0x18]==4 and aRAM[0x54]==5 and aRAM[0x25]==4:
   assert bRAM[0x18]==4 and bRAM[0x54]==5 and bRAM[0x25]==4;oldfiles.append(aa);newfiles.append(bb)
 assert oldfiles and [f.name for f in oldfiles]==[f.name for f in newfiles];changed=label_pixels=number_pixels=0;codes=set(c for spec in SPECS for c in spec[2]);anchors=set();anchor_by_frame={}
 irqref=ref.replace('_survey','_irq').replace('_native','_irq');irqref=irqref+'_irq' if ref.endswith('_pause') else irqref
 if labels:
  for row in rows(f'qa/dialogue/{ref}/castle_hud_irq.csv'):
   if row['kind']=='write' and row['pc']=='FCF1' and row['address']=='A008':assert row['value']=='7D';anchor_by_frame[int(row['frame'])]=int(row['scanline'])+1
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
 return {'ref':ref,'new':new,'screens':len(newfiles),'HUD_changed':changed,'whole_unchanged':len(newfiles)-changed,'native_header_anchor_y':sorted(anchors),'anchor_source':'Actual source castle FCB6/FCCF, FCF1/A008 scanline+1 at preceding frame','Korean_label_pixels_exact':label_pixels,'native_heart_number_multiplier_pixels_exact_after2px_shift':number_pixels,'RAM_OAM_NT_palette_equal':True,'outside_HUD190_240_changed_pixels':0}

def main():
 out=R/'qa/reports/castle_hud054_validation.json';assert not out.exists()
 old=read('build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes');rom=read('build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes')
 result=verify_pair('castle039_hud_reference','castle043_hud_consumer',old,rom)
 # IRQ streams come from the same observers/inputs/seed; changed values only.
 aa=rows('qa/dialogue/castle039_hud_reference/castle_hud_irq.csv');bb=rows('qa/dialogue/castle043_hud_consumer/castle_hud_irq.csv');assert len(aa)==len(bb);changed=0
 for x,y in zip(aa,bb):
  for k in x:
   if k!='value':assert x[k]==y[k],(k,x,y)
  want=x['value']
  if x['kind']=='write'and(x['pc'],x['address'])in [('FCED','A000'),('FCF1','A008')]:want={'7C':'CE','7D':'CF'}[want]
  elif x['kind']=='write'and(x['pc'],x['address'])==('FCDB','2006'):assert want=='2F';want='0F'
  assert y['value']==want,(x,y);changed+=x['value']!=want
 report={'work':54,'status':'PASS','status_scope':'Actual native castle gameplay HUD labels/hearts/score/time/currency and IRQ timing','ROM_sha256':sha(rom),'ROM_SSOT_changes':0,'visual':result,'IRQ_rows_exact':len(aa),'permitted_values_changed':changed,'work53_visual_suspicion':'Resolved: full7 Hangul rows present exactly; no clipping. Earlier report retained with supplemental erratum.','limits':['Initialnormal50 seed not naturally earned; actual native gameplay starts by controller thereafter','Only captured castle interval, not all castle rooms or naturalclear','Previous broad51 evidence reused; no new ROM rebuild/apply required for read-only investigation','Full naturalplay/audio/reset/savestate/hardware/finalhuman language review notperformed'],'next_action':'Create ROM-free verified development xdelta/apply package; preserve current43 and clearly state QA boundaries.'}
 out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in ('status','ROM_SSOT_changes','visual','IRQ_rows_exact','permitted_values_changed')},indent=2))
if __name__=='__main__':main()
