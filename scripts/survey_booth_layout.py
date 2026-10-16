"""Native booth compressed literal consumers and exact header pixels."""
import json,csv,hashlib
from pathlib import Path
from PIL import Image
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def main():
 manifest=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/manifest['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert hashlib.sha256(source).hexdigest()==manifest['sha256'];folder=R/'qa/dialogue/booth038_native';env=json.loads((folder/'environment.json').read_text('utf-8'));assert env['exit_code']==0;records=list(csv.DictReader((folder/'booth_layout_reads.csv').open(encoding='utf-8')));irq=list(csv.DictReader((R/'qa/dialogue/booth038_native_irq/irq_phase.csv').open(encoding='utf-8')));ppu=(folder/'frame_01500_ppu.bin').read_bytes();screen=Image.open(folder/'frame_01500.png').convert('RGB');out=R/'extracted/graphics/booth_001';out.mkdir(parents=True,exist_ok=True);ascii_map={0:' ',**{0x4b+i:chr(65+i) for i in range(26)}};labels=[]
 for name,off,nt,count,ko in [('NUMBER OF',0x4691,0x2106,9,'현재 소지한'),('REMAINING TICKETS',0x46a9,0x2129,17,'티켓 수'),('TICKETS',0x46d5,0x2173,7,'장'),('YOUR POINTS',0x46f1,0x21a6,11,'보유 점수'),('POINTS',0x471a,0x21f3,6,'점')]:
  raw=source[off:off+count];assert ''.join(ascii_map[v] for v in raw)==name;assert rom[off+0x20000:off+0x20000+count]==raw and ppu[nt:nt+count]==raw
  calls=[]
  for x in records:
   if x['kind']!='prg_read':continue
   addr=int(x['address'],16);pc=int(x['pc'],16);mapped=int(x['mapped_prg'],16)
   # Mesen callback address is CPU address, not the requested physical range.
   # Both data and executing806E are in the same8000/8KiB mapped bank18.
   physical=(mapped-(pc%0x2000))+(addr%0x2000)+16
   if off+0x20000<=physical<off+0x20000+count:assert int(x['value'],16)==rom[physical] and x['pc']=='806E';calls.append({'frame':int(x['frame']),'CPU_data_address':addr,'physical_file_offset':physical,'value':int(x['value'],16)})
  assert len(calls)==count,(name,len(calls));labels.append({'source':name,'translation_ko':ko,'source_file_offset':off,'expanded_file_offset':off+0x20000,'length':count,'source_hex':raw.hex(),'NT':nt,'actual_reads':calls,'status':'draft_plan'})
 nmi=[x for x in irq if x['frame']=='1499' and x['pc'] in ('FD77','FD92') and x['address'] in ('A000','A008','B000','B008')];assert [(x['address'],x['value']) for x in nmi]==[('A000','7C'),('A008','7D'),('B000','66'),('B008','67')];assert any(x['kind']=='RAM34_write' and x['frame']=='1473' and x['value']=='7C' and x['pc']=='9C99' for x in records)
 header=screen.crop((80,32,176,48));header.save(out/'header_source_native.png');header.resize((768,128),Image.Resampling.NEAREST).save(out/'header_source_8x.png');cells=[];indices=bytearray(96*16);rgb_by_index={}
 for y in range(2):
  for x in range(12):
   addr=0x2000+(4+y)*32+10+x;tile=ppu[addr];assert 128<=tile<=255;bank=102+(tile-128)//64;off=0x20010+bank*0x400+tile%64*16;raw=source[off:off+16];assert rom[off+0x20000:off+0x20000+16]==raw;bits=decode(raw);assert encode(bits)==raw
   attr=ppu[0x23c0+((4+y)//4)*8+(10+x)//4];shift=((4+y)%4//2)*4+((10+x)%4//2)*2;pal=attr>>shift&3
   occurrences=[0x2000+row*32+col for row in range(19) for col in range(32) if ppu[0x2000+row*32+col]==tile];assert occurrences==[addr]
   for yy in range(8):
    for xx in range(8):
     v=bits[yy*8+xx];indices[(y*8+yy)*96+x*8+xx]=v;rgb_by_index.setdefault(v,set()).add(header.getpixel((x*8+xx,y*8+yy)))
   cells.append({'NT':addr,'tile':tile,'CHR_bank':bank,'source_file_offset':off,'expanded_file_offset':off+0x20000,'source_raw_hex':raw.hex(),'palette_group':pal,'mapped_booth_top_occurrences':occurrences})
 assert all(len(v)==1 for v in rgb_by_index.values());colors={k:next(iter(v)) for k,v in rgb_by_index.items()};check=Image.new('RGB',(96,16));check.putdata([colors[v] for v in indices]);assert check.tobytes()==header.tobytes();(out/'header_source_indices.bin').write_bytes(indices);screen.resize((1024,960),Image.Resampling.NEAREST).save(out/'booth_source_actual_4x.png')
 result={'status':'PASS','work':41,'adopted_build_unchanged':'dialogue_kr_poc_038','source_sha256':manifest['sha256'],'ROM_sha256':hashlib.sha256(rom).hexdigest(),'scope':'New controller-only booth native consumer survey, no ROM/SSOT changes','labels':labels,'header_box':[80,32,176,48],'header_cells':cells,'header_native_pixels_exact':True,'header_palette':colors,'actual_NMI_rows':nmi,'native_font_producer':{'CPU':0x9c95,'source_file_offset':0x5ca5,'source_bytes':'a97c8534a9668535','next_LDA66_overwrites_NZ_before_any_branch':True},'callback_address_semantics':'callback CPU address; physical data derived from same8000 bank mapping of executing806E, not from callback argument alone','limits':['Observed booth only, no global corpus/no other bank consumers absence assertion','Old source labels are native compressed literals, not registered dialogue reader paragraphs','No new build/apply/CPU translation/emulator translation yet; source actual direct review separate'],'next_action':'Create Korean booth label font204/205 and generated header, preserve numeric/font/code/layout controls and actual timing'};(out/'consumer.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('labels','header_cells','actual_NMI_rows')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
