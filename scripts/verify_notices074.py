"""Compare043/044 notice consumers, preserved pixels/core and live pattern reads."""
import json,csv,hashlib
from collections import Counter
from pathlib import Path
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def rows(p):return list(csv.DictReader(p.open()))
def main():
 rom=(R/'build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes').read_bytes();results=[]
 for name,lo,hi in [('timeup',0xc1,0xcb),('nextround',0xcd,0xdb)]:
  p=R/f'qa/dialogue/notices073_{name}_v2';q=R/f'qa/dialogue/notices074_{name}044_v3';env=json.loads((q/'environment.json').read_text('utf-8'));assert env['exit_code']==0 and env['rom_sha256']==hashlib.sha256(rom).hexdigest();ramchanges=Counter();imagechanges=0;frames=0;ppu_equal=0
  for f in sorted(p.glob('frame_*_ram.bin')):
   a=f.read_bytes();b=(q/f.name).read_bytes();changed=[i for i,(v,w)in enumerate(zip(a,b))if v!=w];assert set(changed)<=set((0x39,0x3f));assert all((a[i],b[i])==(62,220)for i in changed);ramchanges.update(changed)
   tag=f.name[:-8];oa=(p/(tag+'_oam.bin')).read_bytes();ob=(q/(tag+'_oam.bin')).read_bytes();assert oa==ob
   pa=(p/(tag+'_ppu.bin')).read_bytes();pb=(q/(tag+'_ppu.bin')).read_bytes();assert pa[0x2000:]==pb[0x2000:];ppu_equal+=pa==pb
   ia=Image.open(p/(tag+'.png')).convert('RGB');ib=Image.open(q/(tag+'.png')).convert('RGB');box=ImageChops.difference(ia,ib).getbbox()
   if box:
    imagechanges+=1;cells=[tuple(oa[i:i+4])for i in range(0,256,4)if oa[i]<230 and lo<=oa[i+1]<=hi];assert cells;boxes=[(x,y-3,x+8,y+19)for y,t,at,x in cells]
    for y in range(box[1],box[3]):
     for x in range(box[0],box[2]):assert ia.getpixel((x,y))==ib.getpixel((x,y))or any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in boxes),(name,tag,x,y)
   frames+=1
  aa=rows(p/'notice_ports.csv');bb=rows(q/'notice_ports.csv');assert len(aa)==len(bb)
  for a,b in zip(aa,bb):
   for k in a:
    if k in ('latch39','value') and a[k]=='3E' and (k=='latch39'or a['address']in ('0039','D008')):assert b[k]=='DC'
    else:assert a[k]==b[k],(name,k,a,b)
  aa=rows(p/'notice_pattern_reads.csv');bb=rows(q/'notice_pattern_reads.csv');assert len(aa)==len(bb)>0
  for a,b in zip(aa,bb):
   for k in a:
    if k=='CHR_relative':assert int(b[k],16)==int(a[k],16)+0x27800
    elif k=='value':assert int(b[k],16)==rom[0x40010+int(b['CHR_relative'],16)]
    else:assert a[k]==b[k],(name,k,a,b)
  top=rows(q/'notice_top_banks.csv');assert any(z['latch39']=='DC'and z['CHR_1C00']=='37000'for z in top)
  for z in top:
   if z['latch39']=='DC':assert (q/(z['tag']+'_ppu.bin')).read_bytes()[0x1c00:0x2000]==rom[0x77010:0x77410]
  results.append({'name':name,'frames':frames,'changed_screens_within_notice_OAM_boxes':imagechanges,'endframe_PPU_entire_equal':ppu_equal,'all_NT_palette_bytes_equal':True,'all_OAM_equal':True,'RAM_changed_only_notice_latch_and_mapper_cache':dict(ramchanges),'live_PPU_rows_exact_geometry_cycles_and_new_ROM_values':len(bb),'all_native_mapper_writes_same_timing_except_selected_bank':len(rows(q/'notice_ports.csv')),'initial_diagnostic_only_not_naturalclear':True})
 report={'work':74,'status':'PASS','rom_sha256':hashlib.sha256(rom).hexdigest(),'scenes':results,'direct_visual':'Caller must inspect actual game PNG separately; this validator does pixel/core assertions only','scope':'Two declared one-byte phase seeds, no whole-game or finalhuman language approval'}
 out=R/'qa/reports/notices074_runtime.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
