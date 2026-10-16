"""Work99 bounded bank35 producers and native HOWTO panel tile consumer."""
from pathlib import Path
import json,hashlib,csv
from verify_dialogue_home import MPU
from verify_booth_native_decoder import Ports
from title_codec import unpack
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def main():
 out=R/'qa/reports/candidate099_bank_nt.json';assert not out.exists();meta=j('manifests/source_rom.json');src=(R/meta['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(src)==meta['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256']
 hits=[i for i in range(16,0x2000e)if src[i:i+2]==bytes.fromhex('8535')];literal=[];tables=[]
 for offset in hits:
  assert src[offset-2]in(0xa9,0xd2,0xf6),(hex(offset),src[offset-4:offset+2].hex())
  if src[offset-2]==0xa9:
   value=src[offset-1];base=(offset-16)//0x4000*0x4000+16;window=0xc000 if base==0x1c010 else 0x8000;start=window+offset-base-2;states=[]
   for data,delta in ((src,0),(rom,0x20000)):
    m=bytearray(65536);m[window:window+0x4000]=data[base+delta:base+delta+0x4000];c=MPU(memory=m);c.pc=start;c.p=0x30;c.step();c.step();assert m[0x35]==data[offset-1+delta] and c.processorCycles==5;states.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,m[:2048]))
   assert states[0][1:3]==states[1][1:3] and states[0][4:6]==states[1][4:6] and (states[0][3]&0x7d)==(states[1][3]&0x7d) and (states[0][3]&0x82)==(0x80 if value>=128 else 0) and (states[1][3]&0x82)==(0x80 if rom[offset-1+0x20000]>=128 else 0) and [i for i,(a,b)in enumerate(zip(states[0][6],states[1][6]))if a!=b]==([]if value==rom[offset-1+0x20000]else[0x35]);assert value==rom[offset-1+0x20000]or(offset,value,rom[offset-1+0x20000])in((0x660c,122,222),(0xd3c2,122,212));literal.append({'source_file_offset':offset,'CPU':start+2,'bank_decimal':value,'current_bank_decimal':rom[offset-1+0x20000],'raw_hex':src[offset-2:offset+2].hex(),'cycles_source047':5})
  else:tables.append(offset)
 assert tables==[0x1d1db,0x1f64f];assert len(literal)==12 and [x['source_file_offset']for x in literal if x['bank_decimal']==116]==[0x5e3e]and not any(x['bank_decimal']==120 for x in literal)
 table_specs=[(0x1d1db,0xd20b,10,2,1),(0x1f64f,0xf642,4,1,0),(0x1f64f,0xf646,4,1,0)];indirect=[]
 for writer,addr,length,step,start in table_specs:
  off=0x1c010+addr-0xc000;raw=src[off:off+length];assert rom[off+0x20000:off+0x20000+length]==raw;values=list(raw[start::step]);assert not set(values)&{116,120};indirect.append({'literal_writer':writer,'CPU_table':addr,'native_selector_range':'course0..4 forD20B; direction0..3 forF642/F646','table_hex':raw.hex(),'bank35_values_decimal':values,'scope':'Native indexed table entries only; no arbitrary out-of-range Y proof'})
 pointer=int.from_bytes(src[0x40d1+16:0x40d3+16],'little');assert pointer==0x87a2;off=0x4010+pointer-0x8000;nt,n=unpack(src[off:0x8010]);assert n==282 and set(nt)==set(range(0x2000,0x2400));nt2,n2=unpack(rom[off+0x20000:0x28010]);assert nt==nt2 and n==n2
 cases=[]
 for flags in range(256):
  if flags&8:continue
  states=[]
  for data in (src,rom):
   m=Ports(data);c=MPU(memory=m);m.cpu=c;c.pc=0x803f;c.p=flags;c.sp=0xfd;m.ram[:2]=pointer.to_bytes(2,'little');steps=0
   while c.pc!=0x80be:c.step();steps+=1;assert steps<50000
   assert len(m.nt)==1024 and {a:v for a,v,t in m.nt}==nt;states.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,steps,m.ram,m.banks,m.nt))
  assert states[0][:8]==states[1][:8]and states[0][9]==states[1][9];cases.append({'flags':flags,'cycles':states[0][5],'instructions':states[0][6]})
 label=list(range(0x90,0x97));high=[{'NT':a,'tile':v,'CHR_bank':116+(v-128)//64,'source_file_offset':0x20010+(116+(v-128)//64)*0x400+v%64*16}for a,v in nt.items()if a<0x23c0 and v>=128];assert len(high)==267 and not[a for a,v in nt.items()if a<0x23c0 and v in label]
 q=R/'qa/dialogue/cards033_coaster';e=j('qa/dialogue/cards033_coaster/environment.json');assert e['exit_code']==0
 selected=[q/f'frame_01800{x}'for x in ('.png','_ram.bin','_ppu.bin','_mapping.csv','_state.txt')]
 for p in selected:assert sha(p.read_bytes())==e['files'][p.name]
 ram=(q/'frame_01800_ram.bin').read_bytes();ppu=(q/'frame_01800_ppu.bin').read_bytes();assert ram[0x35]==116 and ppu[0x800:0x1000]==src[0x3d010:0x3d810]
 actual_high={a:ppu[a]for a in range(0x2000,0x23c0)if ppu[a]>=128};assert actual_high=={x['NT']:x['tile']for x in high}and not set(actual_high.values())&set(label)
 # Native background shares this bank with panel decoration, while the label
 # tiles are unreferenced in this particular panel; residency is not usage.
 assert rom[0x5d010:0x5d810]==src[0x3d010:0x3d810]and rom[0x5e010:0x5e810]==src[0x3e010:0x3e810]
 result={'work':99,'status':'PASS_BOUNDED_HOWTO_BANK_AND_PANEL_NT','source_sha256':sha(src),'ROM047_sha256':sha(rom),'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'bank35_literal_sites':literal,'source047_literal_CPU_cases':24,'bank35_indexed_tables':indirect,'native_NT_selector_hex':'10','native_stream_CPU_pointer':pointer,'source_stream_file_offset':off,'stream_bytes':n,'NT_cells':1024,'native_decoder_D_clear_source047_case_pairs':len(cases),'native_decoder_records':cases,'HOWTO_label_source_tiles_local':list(range(16,23)),'HOWTO_label_bg_tiles_hex':['%02X'%v for v in label],'label_source_span':[0x3d110,0x3d180],'panel_label_occurrences':0,'panel_bank116117_decor_cells':267,'panel_high_cells':high,'historical_actual_033_frame':1800,'historical_actual_CHR0800_bank116117_exact':True,'historical_actual_high_NT_cells_exact':True,'historical_QA_ROM_sha256':e['rom_sha256'],'historical_environment_sha256':sha((q/'environment.json').read_bytes()),'historical_selected_files':{p.relative_to(R).as_posix():sha(p.read_bytes())for p in selected},'ROM_CSV_edited':False,'limits':['Direct literal bank35 writes and three bounded indexed tables only; no all indirect/indexed aliases or global reachability closure','HOWTO tiles are unreferenced in selector10 panel and historical033 coaster1800 only; sourcebank116 is used for decoration, not globally unused','PAUSE120121 has no producer in these direct bank35 constants/tables; sprite or other software register supply not globally closed','128Dclear NMOS CPU flag pairs; asyncIRQ/NMI/PPU and Dset excluded; actual historic033 evidence is not new047 run','No final human preserve approval/full natural play/all corpus/PCM listening/hardware/release claim'],'next_action':'Observe current047 ordinary ride panel with read-only bank35/top/physical116 label PPU tracing, compare against baseline controller path.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in('bank35_literal_sites','native_decoder_records','panel_high_cells','historical_selected_files')},indent=2))
if __name__=='__main__':main()