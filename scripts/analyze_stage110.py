"""Bounded castle background producer and dormant stage-select source investigation."""
from pathlib import Path
import json,hashlib
from verify_dialogue_home import MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/stage110_analysis.json';assert not out.exists()
 meta=json.loads((R/'manifests/source_rom.json').read_text('utf-8'))
 source=R/meta['path'];current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
 assert sha(source)==meta['sha256'] and sha(current)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 s=source.read_bytes();c=current.read_bytes();files={};code=[]
 # Named native entries or explicit adjacent data tables; no linear decode of inline pointers.
 spans=[(0xcd3e,0xcd73),(0xce2e,0xce43),(0xcf9e,0xcfc2),(0xd27a,0xd299),(0xd30d,0xd38f),(0xf5f8,0xf600),(0x965a,0x9821)]
 for a,b in spans:
  so=a-0xc000+0x1c010 if a>=0xc000 else a-0x8000+0x10
  co=so+0x20000;assert s[so:so+b-a]==c[co:co+b-a]
  code.append({'native_CPU_start':f'{a:04X}','native_CPU_end_exclusive':f'{b:04X}','source_file_offset':so,'current047_file_offset':co,'sha256':hashlib.sha256(s[so:so+b-a]).hexdigest(),'source_current_exact':True})
 def memory(rom,fixed):
  m=bytearray(65536);m[0xc000:]=rom[fixed:fixed+0x4000];return m
 predicate=[];default=[]
 for revision,rom,fixed in [('source',s,0x1c010),('047',c,0x3c010)]:
  for value in range(256):
   m=memory(rom,fixed);m[0x79]=value;m[0x34]=0x12;m[0x35]=0x13
   cpu=MPU(memory=m,pc=0xd360)
   for n in range(10):
    if cpu.pc in (0xd36e,0xd389):break
    cpu.step()
   assert cpu.pc==(0xd389 if value<6 else 0xd36e)
   assert (m[0x34],m[0x35])==((0x12,0x13)if value<6 else(64,118))
   predicate.append({'revision':revision,'RAM79':value,'stop_PC':f'{cpu.pc:04X}','cycles':cpu.processorCycles,'head_font':m[0x34],'body_font':m[0x35]})
   # After the unexecuted hardware-facing CBF0 call, execute the actual clear and skip.
   m=memory(rom,fixed);m[:0x800]=bytes([value])*0x800;m[0x18]=3;m[0x19]=0
   m[0x1fe]=0xff;m[0x1ff]=0x3f;cpu=MPU(memory=m,pc=0xcd4c);cpu.sp=0xfd
   for n in range(10000):
    if cpu.pc==0x4000:break
    cpu.step()
   assert cpu.pc==0x4000 and(m[0x18],m[0x19],m[0x54],m[0x79])==(4,0,0,0)
   assert all(x==0 for x in m[0x68:0xe0]) and all(x==0 for x in m[0x400:0x700])
   # Literal LDX BF / DEX / BPL performs one write, not a 192-byte ascending clear.
   assert m[0x7bf]==0 and m[0x700:0x7bf]==bytes([value])*0xbf
   default.append({'revision':revision,'initial_RAM_fill':value,'CPU_instructions':n,'cycles':cpu.processorCycles,'final_root':m[0x18],'final_phase':m[0x19],'final_room':m[0x79]})
 assert s[0x1cd53:0x1cd59]==bytes.fromhex('49cd73cd37ce')
 assert s[0x1cd5f:0x1cd62]==bytes.fromhex('4c37ce')
 assert s[0x1cd67:0x1cd6c]==bytes.fromhex('a909201381')
 pointer=int.from_bytes(s[0x416e+18:0x4170+18],'little');assert pointer==0x81b2
 raw=s[pointer-0x3ff0:pointer-0x3ff0+14]
 assert raw==bytes.fromhex('0a225d5e4b514f005d4f564f4d5e')
 alphabet={0:' ',**{i+75:chr(65+i)for i in range(26)}}
 text=''.join(alphabet[x]for x in raw[2:]);assert text=='STAGE SELECT'
 noentry={pat:sum(s[i:i+len(bytes.fromhex(pat))]==bytes.fromhex(pat)for i in range(0x10,0x20010-len(bytes.fromhex(pat))+1))for pat in ['2052cd','4c52cd','52cd']}
 assert all(n==0 for n in noentry.values())
 # A5 nonnegative reader at 969C indexes four-byte records. 980C starts the next room-property table.
 waypoints=[{'A5':i,'room_RAM79':s[0x178c+4*i],'position_byte1':s[0x178d+4*i],'position_byte2':s[0x178e+4*i],'orientation_A2':s[0x178f+4*i]}for i in range(36)]
 assert waypoints[35]=={'A5':35,'room_RAM79':6,'position_byte1':3,'position_byte2':10,'orientation_A2':0}
 assert set(x['room_RAM79']for x in waypoints)=={0,1,3,4,5,6}
 room_properties=[list(s[0x181c+i*3:0x181f+i*3])for i in range(7)]
 historical=[]
 for dirname in ['gate094_gold4047','gate094_normal50047']:
  directory=R/'qa/dialogue'/dirname;ep=directory/'environment.json';env=json.loads(ep.read_text('utf-8'))
  assert env['exit_code']==0 and env['rom_sha256']==sha(current);files[ep.relative_to(R).as_posix()]=sha(ep)
  rows=[]
  for p in sorted(directory.glob('*_ram.bin')):
   assert sha(p)==env['files'][p.name];ram=p.read_bytes()
   if ram[0x18]==4 and ram[0x25]==4 and ram[0x54]==5:
    rows.append({'frame':int(p.name[6:11]),'RAM79':ram[0x79]});files[p.relative_to(R).as_posix()]=sha(p)
  assert rows and set(x['RAM79']for x in rows)=={0}
  historical.append({'directory':directory.relative_to(R).as_posix(),'environment_sha256':sha(ep),'actual_castle_phase5_samples':len(rows),'room_values':[0],'first_frame':rows[0]['frame'],'last_frame':rows[-1]['frame']})
 report={'work':110,'status':'PASS_BOUNDED_CASTLE_PRODUCER_AND_STAGE_SELECT_ANALYSIS','source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_current_code_spans':code,'native_predicate_CPU_cases':len(predicate),'predicate_cases':predicate,'native_clear_skip_CPU_cases':len(default),'default_cases':default,'castle_binding':{'course_RAM25':4,'native_game_bank_hex':'30','source_game_file_offset':0x10,'current047_game_file_offset':0x20010,'room_change_phase_RAM54':7,'caller_CPU':'F5F8','constructor_CPU':'969C','producer_record_A5':35,'result_room_RAM79':6,'native_NT_pair_hex':['14','16'],'room_properties':room_properties,'constructor_waypoints':waypoints,'bounds':'Four-byte table 977C..980B (36 records); 980C..9820 is separate room-property table. Caller-domain/global all-writers closure remains open.'},'dormant_stage_select':{'initialization_entry_CPU':'CD52','literal_text':text,'asset_index':9,'uncompressed_printer_CPU':'8113','source_file_offset':pointer-0x3ff0,'NT_address_hex':'220A','root3_inline_targets':['CD49','CD73','CE37'],'normal_phase0_path':['CD49','CD4C CF9E','CD4F JMP CE37','CED9 INC18/clear19'],'CD52_direct_word_motifs':noentry,'classification':'New dormant diagnostic text candidate; not ordinary phase1 initialization. Default native path skips it. No global unreachable proof and no extra translated/approved paragraph claim.'},'historical_castle_samples':historical,'frozen_selected_files':files,'new_runtime_or_scene_visual':False,'ROM_CSV_changes':False,'global_corpus_closed':False,'natural_fullplay_passed':False,'release_eligible':False,'limits':['CPU harness begins at D360 or CD4C, does not execute hardware CBF0, mapper FDD3, native NT decoder or IRQ. Not emulator/rendering evidence.','Branch cases cover all byte values, not real-world reachability of all values.','Only named code spans/tables and selected historical phase5 RAM samples; not all indirect A5/79/19 writers.','Debug text outside registered54/graphics33 is separately catalogued and pending consumer/scope decision. No silent blanket exclusion.'],'next_action':'Controlled castle native room-change diagnostic: A5=35 and phase54=7 after seeded entry, log native constructor and NT14/16/CHR/rendering. Separate it from natural progression and preserve current047.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:report[k]for k in ['status','native_predicate_CPU_cases','native_clear_skip_CPU_cases','historical_castle_samples']},ensure_ascii=False))
if __name__=='__main__':main()
