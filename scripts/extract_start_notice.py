"""Work76 read-only full source8x16 population and native START consumer PNG."""
from pathlib import Path
import argparse,json,hashlib,csv
from collections import Counter
from PIL import Image,ImageDraw
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'extracted').resolve());assert not out.exists()
 m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();assert sha(source)==m['sha256'];rom=(R/'build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes').read_bytes();q=R/'qa/dialogue/notices075_natural044';env=json.loads((q/'environment.json').read_text('utf-8'));assert env['rom_sha256']==sha(rom)
 for name in ('frame_02670.png','frame_02670_ppu.bin','frame_02670_mapping.csv','menu_events.csv'):assert sha((q/name).read_bytes())==env['files'][name]
 writes=[z for z in csv.DictReader((q/'menu_events.csv').open())if z['kind']=='write'and z['address']=='0034'and z['value']=='7A'];assert len(writes)==1 and writes[0]['pc']=='A5FA'and writes[0]['frame']=='2636';assert rom[0x26606:0x2660e]==bytes.fromhex('a97a8534a97a8535')
 ppu=(q/'frame_02670_ppu.bin').read_bytes();raw=rom[0x5e810:0x5f010];assert raw==source[0x3e810:0x3f010] and ppu[:2048]==raw and ppu[2048:4096]==raw
 image=Image.open(q/'frame_02670.png').convert('RGB');index=Image.new('L',(96,32));counts={v:Counter()for v in range(4)};codes=[]
 for y in range(112,144):
  for x in range(80,176):
   code=ppu[0x2000+y//8*32+x//8];v=decode(ppu[code*16:(code+1)*16])[y%8*8+x%8];index.putpixel((x-80,y-112),v);counts[v][image.getpixel((x,y))]+=1
 for c in counts.values():assert len(c)==1
 colors={v:next(iter(c))for v,c in counts.items()}
 for y in range(14,18):
  for x in range(10,22):codes.append(ppu[0x2000+y*32+x])
 assert sorted(codes)==list(range(130,178))
 for code in codes:tile=ppu[code*16:(code+1)*16];assert encode(decode(tile))==tile==raw[(code&127)*16:(code&127)*16+16]
 out.mkdir(parents=True);index.save(out/'start_indices.png');png=image.crop((80,112,176,144));png.save(out/'start_original.png');png.resize((768,256),Image.Resampling.NEAREST).save(out/'start_original_8x.png');(out/'font122_123_original.bin').write_bytes(raw)
 report={'work':76,'status':'PASS_NATIVE_START_RGB_ROUNDTRIP','source_text':'START!','translation_ko':'시작!','translation_status':'draft','source_sha256':sha(source),'rom_sha256':sha(rom),'runtime_frame':2670,'native_writer':writes[0],'CHR_banks':[122,123],'source_font_range':[0x3e810,0x3f010],'current_font_range':[0x5e810,0x5f010],'producer_operands':[0x26607,0x2660b],'screen_box':[80,112,176,144],'NT_tile_codes':codes,'font_tile_codes':[x&127 for x in codes],'RGB_exact_pixels':3072,'palette':{str(k):v for k,v in colors.items()},'scope':'Natural controller-only original044 preplay START screen. Distinct from retained title PUSH START. Full128 source8x16 contact sheet is static arbitrarypalette only.'};(out/'consumer.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
 population=[]
 for bank in range(128):
  aa=source[0x20010+bank*1024:0x20410+bank*1024];bb=rom[0x40010+bank*1024:0x40410+bank*1024];population.append({'bank':bank,'source_sha256':sha(aa),'current_sha256':sha(bb),'changed_bytes':sum(v!=w for v,w in zip(aa,bb))})
 (out/'native_CHR_preservation_population.json').write_text(json.dumps({'work':76,'banks':population,'source_vs044_changed_banks':[z['bank']for z in population if z['changed_bytes']],'scope':'Original128bank population mapping, historic title/asset storage changes, not fullruntime or unusedcode proof'},indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
