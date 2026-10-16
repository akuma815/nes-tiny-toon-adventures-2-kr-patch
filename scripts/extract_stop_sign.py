"""Actual STOP train background extraction; top/NMI plus live PPU evidence."""
from pathlib import Path
from collections import Counter
import argparse,csv,json,hashlib
from PIL import Image
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'extracted').resolve());assert not out.exists()
 sm=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/sm['path']).read_bytes();assert sha(source)==sm['sha256'];rom=(R/'build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes').read_bytes();q=R/'qa/dialogue/stop079_train045';e=json.loads((q/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['rom_sha256']==sha(rom)
 for name,h in e['files'].items():assert sha((q/name).read_bytes())==h
 raw=rom[0x51010:0x51810];assert raw==source[0x31010:0x31810];top=(q/'stop_top_03330_ppu.bin').read_bytes();assert top[:2048]==raw;reads=list(csv.DictReader((q/'stop_pattern_reads.csv').open()));assert reads
 for z in reads:p=int(z['CHR_relative'],16);assert 0x11000<=p<0x12000 and rom[0x40010+p]==int(z['value'],16)
 writes=[z for z in csv.DictReader((q/'menu_events.csv').open())if z['kind']=='write'and z['address']=='0034'and z['value']=='44'];assert len(writes)==1 and writes[0]['pc']=='D1C8';assert rom[0x3d21f]==68 and rom[0x3d21b:0x3d225]==bytes.fromhex('4c4e4268444670684068')
 image=Image.open(q/'frame_03330.png').convert('RGB');index=Image.new('L',(24,32));counts={v:Counter()for v in range(4)};codes=[]
 for y in range(12,16):
  for x in range(7,10):codes.append(top[0x2800+y*32+x])
 assert codes==[9,10,11,14,15,16,14,19,20,25,26,27]
 for y in range(32):
  for x in range(24):code=codes[y//8*3+x//8];v=decode(raw[code*16:code*16+16])[y%8*8+x%8];index.putpixel((x,y),v);counts[v][image.getpixel((24+x,96+y))]+=1
 assert all(len(c)==1 for c in counts.values()),counts;colors={v:next(iter(c))for v,c in counts.items()};fields=[]
 for y in range(5,27):
  candidates=[];start=None
  for x in range(8,24):
   if x<21 and index.getpixel((x,y))in(1,2):
    if start is None:start=x
   elif start is not None:candidates.append((start,x));start=None
  candidates=[z for z in candidates if z[1]-z[0]>=6];assert len(candidates)==1 and candidates[0][1]-candidates[0][0]in(6,7),(y,candidates);fields.append({'y':y,'left':candidates[0][0],'right':candidates[0][1]})
 for code in set(codes):assert encode(decode(raw[code*16:code*16+16]))==raw[code*16:code*16+16]
 out.mkdir(parents=True);index.save(out/'stop_indices.png');png=image.crop((24,96,48,128));png.save(out/'stop_original.png');png.resize((192,256),Image.Resampling.NEAREST).save(out/'stop_original_8x.png');(out/'font068_069_original.bin').write_bytes(raw)
 report={'work':79,'status':'PASS_STOP_CONSUMER_RGB_ROUNDTRIP','source_text':'STOP','translation_ko':'정지','translation_status':'draft','source_sha256':sha(source),'rom_sha256':sha(rom),'CHR_banks':[68,69],'source_font_range':[0x31010,0x31810],'current_font_range':[0x51010,0x51810],'native_font_table_D20B_course2_Y4_file_operand':0x3d21f,'native_font_writer':writes[0],'native_loader_entry':'D1BF..D20A','native_loader_code':'LDA25;ASL;TAY;LDA D20B,Y;STA34;LDA D20C,Y;STA35; remaining levelinit fields;RTS','NT_base':0x2800,'NT_box':[56,96,80,128],'actual_box':[24,96,48,128],'empirical_horizontal_offset':32,'NT_tile_codes':codes,'owned_text_tiles':[10,11,15,16,19,20,26,27],'inner_label_fields':fields,'RGB_exact_pixels':768,'palette':{str(k):v for k,v in colors.items()},'live_pattern_read_rows':len(reads),'scope':'Top-beforeHUD CHR68/69 plus natural actual3330; source68..71 live reads verified. Endframe CHR is HUD206/126 and cannot prove STOP. Candidate46 sprites/68..75 atlas guessing rejected, label remains native background.'};(out/'consumer.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in('status','CHR_banks','RGB_exact_pixels','live_pattern_read_rows','owned_text_tiles')},indent=2))
if __name__=='__main__':main()
