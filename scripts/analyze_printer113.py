"""Native8113 queued commands, palette aliases and dormant diagnostic text."""
from pathlib import Path
import json,hashlib
from verify_dialogue_home import MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/printer113_catalog.json';assert not out.exists()
 source=next((R/'original/rom').glob('*.nes'));current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
 s=source.read_bytes();c=current.read_bytes()
 assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'and sha(current)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 assert s[0x4123:0x41db]==c[0x24123:0x241db]
 ptrs=[int.from_bytes(s[0x416e+2*i:0x4170+2*i],'little')for i in range(12)]
 assert ptrs==[0x8176]*4+[0x8199]+[0x8176]*3+[0x819f,0x81b2,0x81c7,0x81c7]
 def decode(rom,index):
  a=ptrs[index]-0x3ff0;start=a;segments=[];queue=[]
  while True:
   lo,hi=rom[a:a+2];a+=2;seg={'address_hex':f'{hi*256+lo:04X}','values':[]};queue.extend([1,hi,lo])
   while True:
    v=rom[a];a+=1
    if v in [0xfe,0xff]:queue.append(0xff);segments.append(seg);break
    seg['values'].append(v);queue.append(v)
   if v==0xff:break
   assert a-start<100
  return{'encoded_length':a-start,'source_offset':start,'source_sha256':hashlib.sha256(rom[start:a]).hexdigest(),'segments':segments,'queue':queue}
 catalog=[];cases=[]
 for i in range(12):
  z=decode(s,i);assert decode(c[0x20000:],i)==z
  addresses=[int(x['address_hex'],16)for x in z['segments']if x['values']]
  kind='NT text diagnostic'if i==9 else('Palette'if addresses and all(0x3f00<=x<0x4000 for x in addresses)else('Empty command tail'if not addresses else'Pointer to nativeCHRcopy code prefix'))
  catalog.append({'index':i,'pointer_CPU':f'{ptrs[i]:04X}','classification':kind,**z})
  for revision,rom,base in [('source',s,0x4010),('047',c,0x24010)]:
   for clear in [False,True]:
    m=bytearray(65536);m[0x8000:0xc000]=rom[base:base+0x4000];m[0x1fe]=0xff;m[0x1ff]=0x3f
    cpu=MPU(memory=m,pc=0x8113);cpu.a=i+(128 if clear else 0);cpu.sp=0xfd
    for n in range(3000):
     if cpu.pc==0x4000:break
     cpu.step()
    assert cpu.pc==0x4000
    expected=[]
    for x in z['segments']:
     a=int(x['address_hex'],16);expected.extend([1,a>>8,a&255,*([0]*len(x['values'])if clear else x['values']),255])
    assert m[0x1e]==len(expected)and list(m[0x100:0x100+len(expected)])==expected
    cases.append({'revision':revision,'input_A':i+(128 if clear else 0),'clear_mask':clear,'queue_length':len(expected),'CPU_instructions':n,'cycles':cpu.processorCycles,'queued_bytes_exact':True})
 native_callers=[{'source_file_offset':0x402a,'CPU':'801A','index':3,'context':'Nativebank32 title tail jump, palette8176.'},{'source_file_offset':0x1ce6a,'CPU':'CE5A','index':8,'context':'Root5 startup logo, palette819F.'},{'source_file_offset':0x1cec8,'CPU':'CEB8','index':5,'context':'Root6 legal startup, palette8176 alias.'},{'source_file_offset':0x1cd69,'CPU':'CD59','index':9,'context':'Dormant CD52 stage-select initialization, skipped by default root3 phase0; not phase1 dispatcher target.'}]
 for x in native_callers:
  a=x['source_file_offset'];assert s[a-2:a]==bytes([0xa9,x['index']])and s[a:a+3]==bytes.fromhex('4c1381'if a==0x402a else'201381')
  assert s[a-2:a+3]==c[a+0x20000-2:a+0x20000+3]
 letters={0:' ',**{i+65:chr(48+i)for i in range(10)},**{i+75:chr(65+i)for i in range(26)}}
 text=[{'NT_address_hex':x['address_hex'],'font124_candidate':' '.join([])if not x['values']else''.join(letters[v]for v in x['values'])}for x in catalog[9]['segments']]
 assert text==[{'NT_address_hex':'220A','font124_candidate':'STAGE SELECT'},{'NT_address_hex':'224E','font124_candidate':'1 0'}]
 report={'work':113,'status':'PASS_BOUNDED_NATIVE8113_COMMAND_CATALOG','source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'table_boundary_CPU_hex':['815E','8176'],'pointer_indices':12,'unique_pointers':5,'source_current_code_table_data_exact':True,'catalog':catalog,'native_literal_call_sites':native_callers,'native_CPU_command_queue_cases':cases,'native_CPU_command_queue_cases_passed':len(cases),'new_text_candidate':{'ID':'DIAGNOSTIC_STAGE_SELECT_110','source_text_candidates':text,'source_preserved':True,'draft_translation_candidates':['스테이지 선택','1 0'],'translation_inserted':False,'actual_rendering_font_consumer_connected':False,'human_scope_or_preservation_approved':False,'reason':'Only declared callerCD52 is skipped by normal stage entry; actual rendering consumer is not established. Technical text extraction is separate from scope approval.'},'shared_palette_alias_warning':'Indices0/1/2/3/5/6/7 share8176; index4 starts at its empty command tail8199. Do not count aliases as seven separate dialogue paragraphs.','indices10_11_warning':'Pointer81C7 overlaps nativeCHRcopy entry code; as8113 data it queues oneA9 byte to0086. No named direct caller observes these entries; not an extra Japanese paragraph or proven used artwork.','ROM_CSV_changes':False,'new_emulator_or_direct_scene':False,'global_corpus_closed':False,'release_eligible':False,'limits':['12pointer slots bounded by following data8176, not all256possible A values or arbitrary pointer-table overflow. Tested0..11 and80..8B only.','CPUqueue execution has no PPU write/emulator/visible result; code-prefix command interpretation does not prove real display.','Font124 decode is a candidate; actual live font for dormant stage-select remains unconnected.','No hidden UI automatically enabled, no static candidate patched without rendering consumer.','No human approval or ROM release/wholeplay claim'],'next_action':'Inspect native cart third-round completion condition and old2Fbot failure against source/collision telemetry to obtain a new discriminating route before attempting another natural3-segment run.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in ['status','pointer_indices','unique_pointers','native_CPU_command_queue_cases_passed','new_text_candidate']},ensure_ascii=False))
if __name__=='__main__':main()
