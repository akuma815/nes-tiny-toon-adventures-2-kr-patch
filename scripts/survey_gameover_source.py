"""Native failure -> GAME OVER, source logo/labels, producer/read/NMI proof."""
import argparse,json,csv,hashlib
from pathlib import Path
from PIL import Image
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def csvrows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=R/'extracted/graphics/gameover_001');a=ap.parse_args();out=a.output.resolve();out.relative_to(R/'extracted');assert not (out/'consumer.json').exists();out.mkdir(exist_ok=True)
 manifest=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));src=(R/manifest['path']).read_bytes();assert sha(src)==manifest['sha256'];b=(R/'build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(b)=='535fa114952587dfc0a6394ddff21b1aede053ade3dc0d3d9dfda77ed5888eae';qa=R/'qa/dialogue/world041_coaster_ticket4';ppu=(qa/'frame_06000_ppu.bin').read_bytes();image=Image.open(qa/'frame_06000.png').convert('RGB');raw=b[0x5ec10:0x5f010];assert raw==src[0x3ec10:0x3f010]==ppu[0xc00:0x1000];colors={};bits=[]
 for y in range(32):
  for x in range(128):
   code=ppu[0x20e8+(y//8)*32+x//8];assert code==0xc0+(y//8)*16+x//8;idx=decode(raw[(code-0xc0)*16:(code-0xbf)*16])[(y%8)*8+x%8];bits.append(idx);colors.setdefault(idx,set()).add(image.getpixel((64+x,56+y)))
 assert all(len(v)==1 for v in colors.values());colors={k:next(iter(v)) for k,v in colors.items()};pred=Image.new('RGB',(128,32));pred.putdata([colors[v] for v in bits]);assert pred.tobytes()==image.crop((64,56,192,88)).tobytes()
 for name,im in [('source_logo.png',pred),('source_logo_4x.png',pred.resize((512,128),Image.Resampling.NEAREST))]:
  if (out/name).exists():assert Image.open(out/name).convert('RGB').tobytes()==im.tobytes()
  else:im.save(out/name)
 if (out/'source_bank123.bin').exists():assert (out/'source_bank123.bin').read_bytes()==raw
 else:(out/'source_bank123.bin').write_bytes(raw)
 font=b[0x5f010:0x5f810];assert font==src[0x3f010:0x3f810];chars={0:' ',**{i+0x41:str(i) for i in range(10)},**{i+0x4b:chr(65+i) for i in range(26)},0x65:'?',0x66:'!',0x67:'.',0x68:'“',0x69:'”'};labels=[]
 for f,nt,n,pc,ko in [(0xd4e8,0x226b,10,'9430','계속할까요?'),(0xd4f2,0x22b0,6,'945B','“예!”'),(0xd4f8,0x22f0,5,'9486','“아니요”')]:
  body=src[f:f+n];assert body==b[f+0x20000:f+0x20000+n]==ppu[nt:nt+n];x=(nt-0x2000)%32*8;y=(nt-0x2000)//32*8;cs={}
  for py in range(8):
   for px in range(n*8):
    v=decode(font[body[px//8]*16:body[px//8]*16+16])[py*8+px%8];cs.setdefault(v,set()).add(image.getpixel((x+px,y+py)))
  assert all(len(v)==1 for v in cs.values());labels.append({'source':''.join(chars[c] for c in body),'translation_ko':ko,'source_hex':body.hex(),'length':n,'source_file_offset':f,'expanded_file_offset':f+0x20000,'NT':nt,'screen_box':[x,y,x+n*8,y+8],'read_callback_pc':pc,'native_colors':{k:next(iter(v)) for k,v in cs.items()}})
 native=[]
 for choice in ('yes','no'):
  d=R/f'qa/dialogue/gameover041_{choice}_consumer';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['rom_sha256']==sha(b) and (d/'trace_complete.txt').read_text()=='8000';rows=csvrows(d/'gameover_consumers.csv');writes=[z for z in rows if z['kind']=='write' and z['frame']=='5034'];assert [(z['pc'],z['address'],z['value'],z['PRG_relative']) for z in writes]==[('93B0','0034','7C','2D3B0'),('93B4','0035','7A','2D3B4')]
  readcases=0
  for p in labels:
   observed=[z for z in rows if z['kind']=='read' and z['frame']=='5034' and z['pc']==p['read_callback_pc']];rawhex=bytes.fromhex(p['source_hex']);assert len(observed)==p['length']
   for i,z in enumerate(observed):assert int(z['address'],16)==p['source_file_offset']-0x4010+i and int(z['value'],16)==rawhex[i] and z['root']=='04' and z['phase']=='0B'
   readcases+=len(observed)
  fonts=csvrows(d/'gameover_top_fonts.csv')
  for z in fonts:
   assert (z['font0'],z['font1'],z['font2'],z['font3'])==('1F000','1F400','1E800','1EC00');p=(d/(z['tag']+'_ppu.bin')).read_bytes();assert p[:4096]==b[0x5f010:0x5f810]+b[0x5e810:0x5f010]
  assert fonts;final=(d/'frame_08000_ram.bin').read_bytes();assert final[0x18]==(8 if choice=='yes' else 7);native.append({'choice':choice,'native_glyph_reads':readcases,'postNMI_font4KiB_samples':len(fonts),'final_root':final[0x18],'scope':'NO passes startup/title then attractroot7, YES returnsnativehome withnormal10; notnatural initialcurrency'})
 result={'work':47,'status':'PASS','source_sha256':sha(src),'reference_build_SHA':sha(b),'actual_frame':6000,'QA':qa.relative_to(R).as_posix(),'logo_box':[64,56,192,88],'logo_NT_first':0x20e8,'logo_NT_rows':4,'logo_cells':64,'logo_codes':[0xc0,0xff],'source_logo_bank':123,'source_logo_file_range':[0x3ec10,0x3f010],'expanded_logo_file_range':[0x5ec10,0x5f010],'source_logo_pixels_exact':4096,'logo_native_colors':colors,'labels':labels,'label_source_pixels_exact':1344,'producer':{'CPU':'93AC/bank36','source_immediates':[0xd3bd,0xd3c1],'expanded_immediates':[0x2d3bd,0x2d3c1],'source_fonts':[124,122],'observed_frame':5034},'native_routes':native,'source_files':{p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file()},'limits':['Initialnormal4 seed, actualnativefailure thereafter, notnaturalinitialcurrency/fullgame','PAUSE120/121 remainsstaticcandidate; observedpause hadnoletter, notwholegameabsenceproof','Newtranslations build/runtimeunperformed','Raw NO length5, adjacent94ED A5 iscode, excluded; quote glyph69 separatelyvalidated']}
 (out/'consumer.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
