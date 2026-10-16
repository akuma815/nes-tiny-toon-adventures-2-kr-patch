"""Work103 bounded source IRQ latches and current047 registered-page latch consumers."""
from pathlib import Path
import hashlib,json
from verify_gate_font_tag_hooks import Memory,MPU,run
from title_codec import unpack
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def irq(rom,profile,active):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xfb0d;c.p=0x30;m.ram[0x6ea]=profile;m.ram[0x6f3]=active
 while c.pc!=0xfb31:c.step();assert c.processorCycles<100
 return c,m

def main():
 out=R/'qa/reports/latch103_supply.json';assert not out.exists();meta=j('manifests/source_rom.json');src=(R/meta['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(src)==meta['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256'];table=src[0x1fb44:0x1fb4a];assert table==bytes.fromhex('5a3a5a665a74')and rom[0x3fb44:0x3fb4a]==table
 raw=[]
 for zp in(0xc6,0xc7):
  for op in(0x85,0x86,0x84):
   for offset in range(16,0x2000e):
    if src[offset:offset+2]==bytes([op,zp]):raw.append({'offset':offset,'zp':zp,'opcode':op,'context_hex':src[offset-8:offset+2].hex()})
 assert len(raw)==5
 owners=[]
 for offset,stream,native in((0x495c,0x48cc,18),(0x4c9a,0x4c6c,20)):
  nt,count=unpack(src[stream:0x8010]);assert stream<=offset<stream+count and len(nt)==1024;owners.append({'offset':offset,'native_NT_selector_decimal':native,'source_stream':stream,'source_stream_bytes':count,'role':'compressed nametable data, not native standalone store instruction'})
 assert src[0x10379:0x1037c]==bytes.fromhex('4cf184')and src[0x1037c:0x10380]==bytes.fromhex('c694d004');owners.append({'offset':0x1037b,'role':'STY C6 raw motif overlaps last JMP84F1 operand84 and next DEC94 opcodeC6; not instruction boundary','native_JMP_file_offset':0x10379})
 assert src[0x1fb22:0x1fb27]==bytes.fromhex('b934fb85c6')and src[0x1fb27:0x1fb2c]==bytes.fromhex('b935fb85c7')
 # Four explicit profile producers; initializer's zero survives the clear loop.
 profiles=[]
 for start,stop,value in((0x9af0,0x9b09,0),(0x9c90,0x9c95,1),(0x9e0e,0x9e13,2),(0x9fea,0x9fef,0)):
  results=[]
  for data in(src,rom):
   m=Memory(data);c=MPU(memory=m);m.cpu=c;c.pc=start;c.p=0x30
   while c.pc!=stop:c.step();assert c.processorCycles<1000
   assert m.ram[0x6ea]==value;results.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,m.ram[:2048]))
  assert results[0]==results[1];profiles.append({'CPU_start':start,'CPU_end_exclusive':stop,'profile':value,'cycles_source047_equal':results[0][5]})
 page_cases=[];fonts=set()
 for seed in(0,120,121,255):
  for slot in range(48):
   c,m=run(rom,0x9417,slot=slot,p=0x30,initial_font=seed);font=m.ram[0x6f3];assert m.ram[0xc6]==font and font==rom[0x5710+slot*2]and font not in(119,120,121);fonts.add(font);page_cases.append({'prior_latch':seed,'slot':slot,'font':font,'cycles':c.processorCycles})
 assert len(page_cases)==192 and len(fonts)==31
 irq_cases=[]
 for profile in range(3):
  for active in sorted(fonts|{90}):
   a,x=irq(src,profile,active);b,y=irq(rom,profile,active);bank=table[profile*2+1];assert x.ram[0xc6]==90 and y.ram[0xc6]==active and x.ram[0xc7]==y.ram[0xc7]==bank;assert(a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles)and a.processorCycles==52
   expected=[(0xa000,90),(0xa008,91),(0xb000,bank),(0xb008,bank+1)];wa=[(z,v)for z,v,t in x.writes if z>=0xa000];wb=[(z,v)for z,v,t in y.writes if z>=0xa000];assert wa==expected and wb==[(0xa000,active),(0xa008,active+1),(0xb000,bank),(0xb008,bank+1)];assert[(z,t)for z,v,t in x.writes]==[(z,t)for z,v,t in y.writes]
   changed=[i for i,(u,v)in enumerate(zip(x.ram[:2048],y.ram[:2048]))if u!=v];assert changed==([]if active==90 else[0xc6]);irq_cases.append({'profile':profile,'current_active':active,'source_bankC6':90,'bankC7':bank,'port_write_cycles':[t for z,v,t in y.writes if z>=0xa000]})
 assert len(irq_cases)==96
 result={'work':103,'status':'PASS_BOUNDED_IRQ_FONT_LATCH_SUPPLY','source_sha256':sha(src),'ROM047_sha256':sha(rom),'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'raw_C6_C7_store_motifs':raw,'raw_data_or_misaligned_owners':owners,'native_profile_producers':profiles,'source_profile0_2_table_hex':table.hex(),'sourceC6_bank':90,'source_currentC7_banks':[58,102,116],'current_FB12_load_hex':rom[0x3fb22:0x3fb25].hex(),'current_FB12_role':'LDA06F3 instead of source LDAFB34,Y; 4cycles both for profile0..2','current_registered_page_font_values':sorted(fonts),'registered48_times_poison4_C6_6F3_initialization_CPU_cases':192,'registered_page_records':page_cases,'source_current_IRQ_slice_case_pairs':96,'IRQ_slice_cycles_equal':52,'IRQ_slice_records':irq_cases,'source_current_profile_initializer_pairs':4,'119120121_absent_from_tested_font_latch_supply':True,'ROM_CSV_edited':False,'limits':['Profile0..2/indexed table and explicit four profile producers only; generic indexed/indirect alias writes and arbitrary invalid profiles not globally closed','48registered pages/fonts and four artificial prior latches only, not all entry paths/state loads or corpus','96IRQ slicepairs stopFB31; no asyncIRQ/PPU model or fullIRQ/hardware claim; prior fullIRQ/runtime timing evidence remains separate','Raw byte motifs are distinguished from their known native NT data and JMP operand owners, not declared a full execution CFG','No new runtime/build/apply/global-unused/human preservation/full natural game/final release claim'],'next_action':'Update a separate current047 graphics-consumer review supplement with HOWTO/PAUSE/POW evidence, scope limits and human decision fields, then tackle another completion-critical QA gap.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in('raw_C6_C7_store_motifs','raw_data_or_misaligned_owners','native_profile_producers','registered_page_records','IRQ_slice_records')},indent=2))
if __name__=='__main__':main()