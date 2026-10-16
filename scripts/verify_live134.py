"""Direct entry counters distinguish CPU-model cycles from real elapsed time."""
from pathlib import Path
import csv,collections,hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/live134_validation.json';assert not out.exists();result={}
 prior=json.loads((R/'qa/reports/clear129_validation.json').read_text('utf-8'))
 for seed in [3,4]:
  dirs=[R/f'qa/dialogue/live134v2_normal{seed}_{b}' for b in ['047','049']];envs=[json.loads((d/'environment.json').read_text('utf-8'))for d in dirs]
  for d,e,b in zip(dirs,envs,['047','049']):
   assert e['exit_code']==0 and e['frames']==4200 and e['rom_sha256']==sha(R/f'build/dialogue_kr_poc_{b}/TinyToon2_dialogue_kr_poc.nes')
   for f,h in e['files'].items():assert sha(d/f)==h
  for k in ['exe_sha256','lua_sha256','config_sha256','input','seed','seed_file_sha256']:assert envs[0][k]==envs[1][k]
  pp=[rows(d/'page_cycles.csv') for d in dirs];assert len(pp[0])==len(pp[1]) and len(pp[0])%3==0
  calls=[]
  for i in range(0,len(pp[0]),3):
   a,b=pp[0][i:i+3],pp[1][i:i+3]
   assert [x['kind']for x in a]==[x['kind']for x in b]==['entry','helper','before_rts']
   for x,y in zip(a,b):
    for k in ['frame','kind','pc','PRG_relative','id','phase','RAM1B','sp','a','x','y','ps']:assert x[k]==y[k],(seed,i,k)
   da=int(a[-1]['cycle'])-int(a[0]['cycle'])+6;db=int(b[-1]['cycle'])-int(b[0]['cycle'])+6
   delta=db-da;assert delta==(42 if i==0 else 38),(seed,i,delta)
   assert int(a[1]['cycle'])-int(a[0]['cycle'])==int(b[1]['cycle'])-int(b[0]['cycle'])==87
   calls.append({'frame':int(b[0]['frame']),'id':b[0]['id'],'phase':b[0]['phase'],'live_RAM1B':int(b[0]['RAM1B'],16),'047_elapsed_including_RTS':da,'049_elapsed_including_RTS':db,'elapsed_delta':delta,'entry_cycle_delta':int(b[0]['cycle'])-int(a[0]['cycle']),'idle_counter_model_delta_mod256':(-2*(int(b[0]['RAM1B'],16)+1))%256})
  assert len(calls)==(12 if seed==3 else 10)
  inferred=prior['routes'][f'normal{seed}']['inferred_counter_records'];assert len(inferred)==len(calls)
  for x,y in zip(inferred,calls):assert x['frame_label']==y['frame'] and x['inferred_RAM1B']==y['live_RAM1B']
  snaps=[rows(d/'frame_counters.csv')for d in dirs];assert len(snaps[0])==len(snaps[1])==4200
  for a,b in zip(*snaps):
   for k in ['frame','cycle','RAM1B','root','phase','ride']:assert a[k]==b[k]
   delta=sum(c['idle_counter_model_delta_mod256']for c in calls if c['frame']<int(b['frame']))%256
   assert (int(b['RAM22'],16)-int(a['RAM22'],16))%256==delta
  ports=[rows(d/'port_writes.csv')for d in dirs];assert len(ports[0])==len(ports[1]);timing=[];value=[]
  for a,b in zip(*ports):
   for k in ['frame','pc','address','scanline']:assert a[k]==b[k]
   dc=int(b['cycle'])-int(a['cycle']);dd=int(b['dot'])-int(a['dot'])
   if dc or dd:
    assert seed==3 and a['frame']=='2001' and dc==-1 and dd==-3
    timing.append({'047':a,'049':b})
   if a['value']!=b['value']:
    assert seed==3 and 2008<=int(a['frame'])<=2606 and (a['address'],a['value'],b['value'])in [('A000','C4','E2'),('A008','C5','E3')]
    value.append({'frame':int(a['frame']),'address':a['address'],'047':a['value'],'049':b['value']})
  assert len(timing)==(17 if seed==3 else 0) and len(value)==(1198 if seed==3 else 0)
  during={}
  for d,p in zip(dirs,ports):during[d.name]=[x for x in p if int(pp[dirs.index(d)][0]['cycle'])<=int(x['cycle'])<=int(pp[dirs.index(d)][2]['cycle'])]
  assert all(not x for x in during.values())
  result[f'normal{seed}']={'live_calls':calls,'direct_counters_match_inferred129':True,'EndFrame_counter_model_exact_cases':4200,'ports_compared':len(ports[0]),'port_sequence_addresses_PC_scanline_equal':True,'changed_bank_values':value,'one_cycle_advanced_port_writes':timing,'no_logged_mapper_PPU_port_during_first_call':True,'scope':'42-cycle first call is real elapsed time, not the38-cycle pure CPU model. Additional4 source unclassified. All port times exact in success; shortage17 writes advance1cycle. No blanket IRQ timing identity.'}
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 v={'work':134,'status':'PASS_BOUNDED_DIRECT_COUNTER_MODEL_WITH_ELAPSED_AND_IRQ_DIFFERENCES','ROM049_sha256':sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'routes':result,'pure_CPU_model_extra_cycles':38,'real_first_home_call_extra_cycles':42,'unclassified_extra_first_call_cycles':4,'human_final_review':False,'new_screenshots_or_ROM_changes':False,'limits':['Exact whole CPU/gameplay or allIRQ timing identity not proved','First-call4 extra elapsed cycles require independent bus/DMC discrimination; no cause guessed','New actual live timing/counters, not new scene visual or audio listening QA','Same seed/controller paths only; global corpus/wholeplay/hardware/PCM/human review pending']}
 out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':v['status'],'summary':{k:{'calls':len(z['live_calls']),'counter_cases':4200,'ports':z['ports_compared'],'one_cycle_shifts':len(z['one_cycle_advanced_port_writes'])}for k,z in result.items()}},indent=2))
if __name__=='__main__':main()
