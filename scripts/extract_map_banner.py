"""Bind actual map NT cells, NMI font80..83, source CHR and exact native pixels."""
import json,csv,hashlib,sys
from pathlib import Path
from PIL import Image
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def main():
 d=R/'extracted/graphics/map_banner_001';m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert hashlib.sha256(source).hexdigest()==m['sha256'];folder=R/'qa/dialogue/credits037_coaster';ppu=(folder/'frame_01080_ppu.bin').read_bytes();im=Image.open(folder/'frame_01080.png').convert('RGB');colors={0:(0,0,0),1:(192,223,255),2:(255,254,255),3:(181,49,32)};canvas=Image.new('RGB',(144,16));indices=bytearray(144*16);cells=[]
 irq=list(csv.DictReader((R/'qa/dialogue/stage_lower036_coaster_irq/irq_phase.csv').open(encoding='utf-8')))
 nmi=[x for x in irq if x['frame']=='1079' and x['pc'] in ('FD77','FD92') and x['address'] in ('A000','A008','B000','B008')];assert [(x['address'],x['value']) for x in nmi]==[('A000','50'),('A008','51'),('B000','52'),('B008','53')]
 for y in range(2):
  for x in range(18):
   addr=0x2000+(3+y)*32+7+x;tile=ppu[addr];bank=80+tile//64;off=0x20010+bank*0x400+(tile%64)*16;raw=source[off:off+16];assert raw==rom[off+0x20000:off+0x20000+16];bits=decode(raw);assert encode(bits)==raw
   attr=ppu[0x23c0+((3+y)//4)*8+(7+x)//4];shift=((3+y)%4//2)*4+((7+x)%4//2)*2;pal=(attr>>shift)&3;assert pal==1,(addr,pal)
   # Header has palette1; native indices0=universal black,1=blue,2=white,3=red.
   occurrences=[0x2000+row*32+col for row in range(19) for col in range(32) if ppu[0x2000+row*32+col]==tile];assert occurrences==[addr],(tile,occurrences)
   for yy in range(8):
    for xx in range(8):v=bits[yy*8+xx];canvas.putpixel((x*8+xx,y*8+yy),colors[v]);indices[(y*8+yy)*144+x*8+xx]=v
   cells.append({'NT':addr,'tile':tile,'source_file_offset':off,'expanded_file_offset':off+0x20000,'source_raw_hex':raw.hex(),'CHR_bank':bank,'mapped_top_occurrences':occurrences})
 assert canvas.tobytes()==im.crop((56,24,200,40)).tobytes();assert canvas.tobytes()==Image.open(d/'map_banner_source_native.png').convert('RGB').tobytes();(d/'source_indices.bin').write_bytes(indices)
 out={'status':'PASS','work':39,'adopted_build_unchanged':'dialogue_kr_poc_037','source_sha256':m['sha256'],'ROM_sha256':hashlib.sha256(rom).hexdigest(),'actual_capture':'qa/dialogue/credits037_coaster/frame_01080.png','native_box':[56,24,200,40],'size':[144,16],'palette':colors,'NMI_actual_register_rows':nmi,'cells':cells,'source_tiles_decode_encode_exact':True,'actual_native_pixels_exact':True,'tile_unique_in_actual_map_top':True,'scope':'Observed home map only; other bank80..83 consumers require separate inventory; no patch made','next_action':'Generate Korean map banner and compile only in-image lettering, preserve native frame/palette and verify all bank consumers'};(d/'consumer.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k not in ('cells','NMI_actual_register_rows','palette')},indent=2))
if __name__=='__main__':main()
