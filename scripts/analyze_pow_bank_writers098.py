"""Work98 bounded direct RAM38 writers; eliminate wrong-bank fireworks poses."""
from pathlib import Path
import json,hashlib
from verify_dialogue_home import MPU
from analyze_pow_metasprites096 import run
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def memory(rom,source_base):
 m=bytearray(65536);current=len(rom)!=262160;base=source_base+(0x20000 if current else 0);window=0xc000 if source_base==0x1c010 else 0x8000;m[window:window+0x4000]=rom[base:base+0x4000];return m,window
def cpu(rom,base,start,end,X=0,seed=0):
 m,window=memory(rom,base);m[0x38]=0x5a;m[0x500+X]=seed;m[0x1fe:0x200]=bytes.fromhex('ff c0');c=MPU(memory=m);c.pc=start;c.sp=0xfd;c.x=X;c.p=0x30;n=0
 while c.pc!=end:c.step();n+=1;assert n<5000
 return c,m

def main():
 output=R/'qa/reports/pow098_bank_writers.json';assert not output.exists();source_meta=j('manifests/source_rom.json');source=(R/source_meta['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(source)==source_meta['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256']
 motifs={};records=[]
 for op,load,register in((0x85,0xa9,'a'),(0x86,0xa2,'x'),(0x84,0xa0,'y')):
  hits=[i for i in range(16,0x20010-2)if source[i:i+2]==bytes([op,0x38])];motifs[f'{op:02X}38']=hits
  for offset in hits:
   base=(offset-16)//0x4000*0x4000+16;window=0xc000 if base==0x1c010 else 0x8000;pc=window+offset-base
   if offset==0x4f91:start=pc-6;assert source[offset-6:offset-4]==bytes([load,126]);value=126
   else:start=pc-2;assert source[offset-2]==load;value=source[offset-1]
   a,m=cpu(source,base,start,pc+2);b,n=cpu(rom,base,start,pc+2);assert m[0x38]==n[0x38]==value and(a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles)
   assert m[:2048]==n[:2048];records.append({'source_writer_file_offset':offset,'source_PRG16K_base':base,'CPU_writer':pc,'native_slice_start':start,'register':register,'constant_bank':value,'CPU_cycles_source_current_equal':a.processorCycles,'raw_slice_hex':source[base+(start-window):offset+2].hex()})
 assert len(records)==15 and len([x for x in records if x['constant_bank']==61])==3
 # Fixed final-scene constructor chooses bank54, then the staged animation
 # derives art9D..A2 from a bounded0..5 counter. Same sprite frames are not proof
 # that bank61 POW graphics are consumed by this unrelated native route.
 a,m=cpu(source,0x10010,0xbc68,0xbc80);b,n=cpu(rom,0x10010,0xbc68,0xbc80);assert m[0x34:0x3a]==n[0x34:0x3a]==bytes.fromhex('38 3a 34 35 36 37')and a.processorCycles==b.processorCycles==30
 cases=[]
 for actor in range(12):
  for count in range(6):
   a,m=cpu(source,0x10010,0xbbba,0xc100,actor,count);b,n=cpu(rom,0x10010,0xbbba,0xc100,actor,count);assert m[0x400+actor]==n[0x400+actor]==0x9d+count and m[0x450+actor]==n[0x450+actor]==8 and m[0x500+actor]==n[0x500+actor]==count+1
   assert(a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles)and m[:2048]==n[:2048];cases.append({'actor':actor,'counter':count,'art_id':0x9d+count,'cycles':a.processorCycles})
 current_identical=[]
 for course,art,name in((1,0x8f,'menu_card_immediate_actor14'),(0,0xed,'stage_initializer_actor2_hypothesis'),(4,0x3e,'verified_gameover_flag')):
  a,c,d,steps=run(source,art,course);b,e,f,s=run(rom,art,course);assert d==f and c.processorCycles==e.processorCycles;current_identical.append({'role':name,'course_selector':course,'art_id':art,'OAM_hex':d.hex(),'pattern_tiles':list(d[1::4]),'cycles':c.processorCycles})
 # Candidate context98 points to a valid init slice; its native runtime role is
 # still a hypothesis. StageC0..FF cannot use work96's common-only descriptor.
 lexical={pat:[i for i in range(16,0x20010-len(bytes.fromhex(pat)))if source[i:i+len(bytes.fromhex(pat))]==bytes.fromhex(pat)]for pat in('8d3800','9534','9538','9634')};assert not any(lexical.values())
 old=j('qa/reports/engine_closure052.json');image=R/'work/pow_writer_098/bank54_61_same_pose_static.png';assert image.is_file()
 result={'work':98,'status':'PASS_BOUNDED_DIRECT_BANK38_WRITERS','source_sha256':sha(source),'ROM047_sha256':sha(rom),'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'direct_ZP_writer_motifs':motifs,'validated_constant_slices':records,'source_current_CPU_slices':30,'bank61_constant_sites':3,'searched_exact_indexed_absolute_motifs_absent':lexical,'ending_BC68_constructor_CHR_banks':[56,58,52,53,54,55],'ending_BC68_CPU_cycles':30,'fireworks_BBBA_counter_cases_source_current':144,'fireworks_counter_records':cases,'same_pose_wrong_bank_eliminated':'Native9D..A2 branch is paired with final-scene bank54, not bank61. Counter range0..5 derived from nativeCMP6; other9C/A3 blink stages kept distinct.','constructor_sprite_candidates':current_identical,'historical_root9_work52_report_sha256':sha((R/'qa/reports/engine_closure052.json').read_bytes()),'static_comparison_image':image.relative_to(R).as_posix(),'static_comparison_image_sha256':sha(image.read_bytes()),'consumer_connected_for_POW':False,'ROM_CSV_edited':False,'scope':'15 literal direct STA/STX/STY ZP38 motif sites and native slices only. Generic indexed/indirect writes, path reachability, whole sprite population and all caller actor states not closed. No global-unused/final-human claim.'}
 output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in('validated_constant_slices','fireworks_counter_records','constructor_sprite_candidates','direct_ZP_writer_motifs')},indent=2))
if __name__=='__main__':main()