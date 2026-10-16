"""Read-only consumer-backed 8x16 sprite notice extraction (043)."""
import csv,json,hashlib
from collections import Counter
from pathlib import Path
from PIL import Image
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));original=(R/source['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(original)==source['sha256'];raw=rom[0x4f810:0x4fc10];assert raw==original[0x2f810:0x2fc10]
 out=R/'extracted/graphics/notices_002';assert not out.exists();records=[];outputs={}
 for name,text,ko,start,strips,phase,pc in [('timeup','TIME UP!','시간 초과!',0,6,16,'F812'),('nextround','NEXT ROUND!','다음 라운드!',12,8,14,'F7C2')]:
  p=R/f'qa/dialogue/notices073_{name}_v2';before=(p/'seed_before_ram.bin').read_bytes();after=(p/'seed_after_ram.bin').read_bytes();assert len(before)==len(after)==2048 and [i for i,(a,b) in enumerate(zip(before,after)) if a!=b]==[0x54] and before[0x54]==5 and after[0x54]==phase
  ports=list(csv.DictReader((p/'notice_ports.csv').open()));assert any(x['address']=='0039' and x['value']=='3E' and x['pc']==pc for x in ports)
  reads=list(csv.DictReader((p/'notice_pattern_reads.csv').open()));assert reads
  for z in reads: a=int(z['CHR_relative'],16);assert 0xf800<=a<0xfa00 and rom[0x40010+a]==int(z['value'],16)
  o=(p/'frame_03360_oam.bin').read_bytes();screen=Image.open(p/'frame_03360.png').convert('RGB');codes=set(0xc1+start+2*i for i in range(strips));cells=[tuple(o[i:i+4]) for i in range(0,256,4) if o[i]<230 and o[i+1] in codes];assert len(cells)==strips and {x[1] for x in cells}==codes and len({x[2] for x in cells})==1
  counts={v:Counter() for v in (1,2,3)}
  for y,t,a,x in cells:
   assert not a&0xc0
   for yy in range(16):
    bits=decode(raw[((t&254)-0xc0+yy//8)*16:((t&254)-0xc0+yy//8+1)*16])
    for xx in range(8):
     v=bits[yy%8*8+xx]
     if v:counts[v][screen.getpixel((x+xx,y+yy+(1 if name=='nextround' else 0)))]+=1
  assert all(len(c)==1 for c in counts.values() if c),counts
  colors={v:next(iter(c)) for v,c in counts.items() if c};indices=Image.new('L',(strips*8,16));png=Image.new('RGBA',indices.size)
  for i in range(strips*2):
   tile=raw[(start+i)*16:(start+i+1)*16];bits=decode(tile);assert encode(bits)==tile
   for yy in range(8):
    for xx in range(8):
     v=bits[yy*8+xx];xy=(i//2*8+xx,i%2*8+yy);indices.putpixel(xy,v);png.putpixel(xy,(*colors[v],255) if v else (0,0,0,0))
  outputs[f'{name}_original.png']=png;outputs[f'{name}_indices.png']=indices;outputs[f'{name}_original_8x.png']=png.resize((png.width*8,128),Image.Resampling.NEAREST)
  records.append({'name':name,'source_text':text,'translation_ko':ko,'status':'draft','tile_start':start,'tiles':strips*2,'size':list(png.size),'OAM':cells,'palette':{str(k):v for k,v in colors.items()},'actual_RGB_nontransparent_exact':sum(sum(c.values()) for c in counts.values()),'empirical_PNG_OAM_y_delta':1 if name=='nextround' else 0,'PPU_live_read_rows':len(reads),'producer_next_PC':pc,'phase_hex':f'{phase:02X}','source_png':f'{name}_original.png'})
 out.mkdir(parents=True);(out/'bank062_original.bin').write_bytes(raw)
 for name,im in outputs.items():im.save(out/name)
 report={'work':73,'status':'PASS_CONSUMER_RGB_ROUNDTRIP','source_sha256':sha(original),'rom_sha256':sha(rom),'CHR_bank':62,'expanded_file_range':[0x4f810,0x4fc10],'producer_operands':[0x3f81f,0x3f7cf],'owned_notice_tiles':28,'preserve_tiles':[28,64],'labels':records,'scope':'One explicit RAM54 seed per scene; not naturalclear. Render pixel y is empirical PNG/OAM alignment, not NES hardware timing claim.'}
 (out/'consumer.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
