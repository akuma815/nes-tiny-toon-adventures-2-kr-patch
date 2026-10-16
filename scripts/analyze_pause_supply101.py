"""Work101 PAUSE supply bounds: literal motifs, constant IRQ ports, unknown data producers."""
from pathlib import Path
import hashlib,json
from verify_dialogue_home import MPU
from verify_gate_font_tag_hooks import Memory
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def main():
 out=R/'qa/reports/pause101_supply_bounds.json';assert not out.exists();meta=j('manifests/source_rom.json');src=(R/meta['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(src)==meta['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256'];motifs=[]
 for zp in range(0x34,0x3a):
  for op,load in((0x85,0xa9),(0x86,0xa2),(0x84,0xa0)):
   for offset in range(16,0x2000e):
    if src[offset:offset+2]!=bytes([op,zp]):continue
    adjacent=src[offset-2]==load;value=src[offset-1]if adjacent else None
    motifs.append({'source_file_offset':offset,'software_ZP':zp,'store_opcode':op,'context_hex':src[max(16,offset-8):offset+2].hex(),'immediate_load_adjacent':adjacent,'adjacent_bank_value':value,'classification':'Literal byte motif, not automatic executable-code or reachability proof'})
 literal=[x for x in motifs if x['immediate_load_adjacent']];assert not[x for x in literal if x['adjacent_bank_value']in(119,120,121)]
 # Native IRQ constant two-pair groups. Start/end are instruction boundaries;
 # recorded ports/values come from CPU stores, not disassembled table bytes.
 specs=[(0x1fad4,0x1fae6),(0x1fb7e,0x1fb90),(0x1fbde,0x1fbf0),(0x1fbfe,0x1fc10),(0x1fc65,0x1fc77),(0x1fcf8,0x1fd0a),(0x1fcab,0x1fcc5)]
 groups=[]
 for start,end in specs:
  begin=0xc000+start-0x1c010;stop=0xc000+end-0x1c010;records=[]
  for name,data in(('source',src),('current047',rom)):
   m=Memory(data);c=MPU(memory=m);m.cpu=c;c.pc=begin;c.p=0x30;steps=0
   while c.pc!=stop:c.step();steps+=1;assert steps<100
   writes=[(a,v,t)for a,v,t in m.writes if a in(0xa000,0xa008,0xb000,0xb008,0xc000,0xc008,0xd000,0xd008)];assert not{v for a,v,t in writes}&{120,121};records.append({'artifact':name,'writes':writes,'cycles':c.processorCycles,'instructions':steps})
  assert records[0]['cycles']==records[1]['cycles']and records[0]['instructions']==records[1]['instructions']and[(a,t)for a,v,t in records[0]['writes']]==[(a,t)for a,v,t in records[1]['writes']];groups.append({'source_start':start,'source_end_exclusive':end,'CPU_start':begin,'records':records})
 # At FB1F/FB2A the source IRQ separately reads dynamic latches C6/C7. This is
 # not a constant group; record it as an outstanding supply, not unused proof.
 dynamic=[{'source_file_offset':i,'address':a,'load_ZP':'C6'if a==0xa000 else'C7','raw_hex':src[i-2:i+3].hex()}for i,a in((0x1fb31,0xa000),(0x1fb3a,0xb000))];assert[src[x['source_file_offset']-2:x['source_file_offset']]for x in dynamic]==[bytes.fromhex('a6c6'),bytes.fromhex('a6c7')]
 candidates=[]
 for op in(0xa9,0xa2,0xa0):
  for value in(120,121):
   for offset in range(16,0x2000e):
    if src[offset:offset+2]==bytes([op,value]):candidates.append({'offset':offset,'load_opcode':op,'value':value,'raw_hex':src[offset:offset+14].hex()})
 explicit={'0x12d0f':'Native LDA78/STA0530; actor animation state, not direct CHR store','0x141f5':'Native81E5 passes78 toAC32 distance comparison using06/07, not direct CHR store','0x1547d':'Native946D compares78 with04AF position, not direct CHR store','0x1ef29':'NativeEF19 stores78 in11 for geometric consumer, not direct CHR store','0x1f725':'NativeF715 stores78 in04A5, verified work97 flag X coordinate120'}
 for x in candidates:x['bounded_role']=explicit.get(hex(x['offset']),'Raw A0xx in data-looking rows; not established as a CPU load or bank producer')
 unresolved=[{'source_file_offset':0x1004c,'CPU':0x803c,'source_PRG16K_base':0x10010,'producer':'LDA($01),Y / STA36 from native animation pair table','context_hex':src[0x10034:0x1004e].hex()},{'source_file_offset':0x11372,'CPU':0x9362,'source_PRG16K_base':0x10010,'producer':'LDA($00),Y / STA36 from player/action descriptor','context_hex':src[0x11363:0x11379].hex()}]
 assert rom[0x5e010:0x5e810]==src[0x3e010:0x3e810]
 result={'work':101,'status':'PASS_BOUNDED_PAUSE_SUPPLY_INVENTORY','source_sha256':sha(src),'ROM047_sha256':sha(rom),'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'software_CHR34_39_raw_store_motifs':motifs,'raw_store_motif_count':len(motifs),'adjacent_immediate_motif_count':len(literal),'adjacent119120121_count':0,'native_constant_IRQ_groups':groups,'source047_IRQ_slice_cases':14,'dynamic_IRQ_font_latch_consumers_not_closed':dynamic,'raw_load120121_motifs':candidates,'native_indirect_animation_bank36_producers_not_closed':unresolved,'PAUSE_original_2KiB_preserved':True,'ROM_CSV_edited':False,'limits':['Byte motif inventory is not whole executable code/reachability census; data false matches retained explicitly','Absence of adjacent119120121 does not exclude generic indexed/indirect/computed supply or register aliases','Seven constant IRQ groups exclude PAUSE banks, but dynamicC6/C7 and native player bank36 pointer tables remain unclosed','Background paired registers34/35 and independent sprite registers36..39 have distinct mapping, from nativeFD67/work96','No new runtime/build/apply; no global-unused/final human preserve/full gameplay/corpus/release claim'],'next_action':'Trace source player/action bank36 indirect table pointers at803C/9362 and verify bounded descriptor font values before selecting a PAUSE edit.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in('software_CHR34_39_raw_store_motifs','native_constant_IRQ_groups','raw_load120121_motifs')},indent=2))
if __name__=='__main__':main()