"""Verify one V7 natural controller experiment, reporting its actual outcome."""
from pathlib import Path
import json,csv,hashlib,collections
from verify_cart_geometry066 import classify
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/cart117_validation_v2.json';assert not out.exists()
 q=R/'qa/dialogue/cart117_headinghold047';old=R/'qa/dialogue/cart115_v6collision047';ep=q/'environment.json';env=json.loads(ep.read_text('utf-8'));oe=json.loads((old/'environment.json').read_text('utf-8'))
 rom=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes()
 assert env['exit_code']==0 and env['frames']==36000 and(q/'trace_complete.txt').read_text()=='36000'
 assert sha(rom)==env['rom_sha256']=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 files={}
 for n,h in env['files'].items():assert sha(q/n)==h;files[(q/n).relative_to(R).as_posix()]=h
 files[ep.relative_to(R).as_posix()]=sha(ep)
 assert(q/'capture_survey_used.lua').read_bytes()==(R/'scripts/trace_cart_rounds_v7.lua').read_bytes()
 policy=rows(q/'cart_round_policy.csv');baseline=rows(old/'cart_round_policy.csv');assert sha(old/'cart_round_policy.csv')==oe['files']['cart_round_policy.csv']
 before={int(x['frame']):x for x in baseline}
 first=min(int(x['frame'])for x in policy if int(x['frame'])in before and x['mask']!=before[int(x['frame'])]['mask'])
 assert first==16220
 prefix=[x for x in policy if int(x['frame'])<first];assert prefix==[x for x in baseline if int(x['frame'])<first]
 same=0;png_exceptions=[];state_exact=0
 for p in sorted(q.glob('frame_*.png')):
  if int(p.name[6:11])>=first:continue
  for suffix in ['.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv']:
   n=p.stem+suffix;assert sha(old/n)==oe['files'][n]
   if(q/n).read_bytes()==(old/n).read_bytes():same+=1
   else:
    assert suffix=='.png'
    from PIL import Image,ImageChops
    aa=Image.open(q/n).convert('RGB');bb=Image.open(old/n).convert('RGB')
    png_exceptions.append({'frame':int(p.name[6:11]),'name':n,'current_sha256':sha(q/n),'baseline_sha256':sha(old/n),'RGB_difference_bbox':ImageChops.difference(aa,bb).getbbox(),'RGB_different_pixels':sum(x!=y for x,y in zip(aa.getdata(),bb.getdata()))})
  n=p.stem+'_state.txt';assert(q/n).read_bytes()==(old/n).read_bytes()and sha(old/n)==oe['files'][n];state_exact+=1
 assert {x['frame']for x in png_exceptions}=={1281,2820,4320}
 assert state_exact==702
 records={int(x['frame']):x for x in policy};release=rows(q/'cart2F_release_policy.csv');until=0;locked=0;bursts=[];lock_samples=0;pit_exempt=0
 for x in release:
  f=int(x['frame']);r=records[f]
  if x['eligible']=='true'and f>=until:until=f+16;locked=int(r['mask'],16)&15;bursts.append({'start':f,'end_exclusive':until,'direction_mask':f'{locked:02X}'})
  assert int(x['burst_until'])==until
  if f<until:
   assert int(r['mask'],16)&128==0
   if r['mode']=='pit_avoid':pit_exempt+=1
   else:assert int(r['mask'],16)&15==locked;lock_samples+=1
  mask=int(r['mask'],16);assert not(mask&1 and mask&2)and not(mask&4 and mask&8)
 # Native queries only within the declared3floor levels; later result actors are another domain.
 cache={};queries=rows(q/'cart_tile_queries.csv');query_levels=collections.Counter();excluded=[]
 for x in queries:
  level=int(x['level']);query_levels[level]+=1
  if level not in [0,1,2]:excluded.append(x);continue
  key=tuple(int(x[k])for k in ['x_page','x_low','y_page','y_low','level'])
  if key not in cache:cache[key]=classify(blob,*key)
  assert cache[key]==int(x['class'])
 chunks=0;screens=list(q.glob('frame_*.png'))
 for image in screens:
  raw=(q/(image.stem+'_ppu.bin')).read_bytes()
  for m in rows(q/(image.stem+'_mapping.csv')):
   if m['kind']!='chr':continue
   a=int(m['cpu_or_ppu_address'],16);b=int(m['relative_offset'],16);assert raw[a:a+1024]==blob[0x40010+b:0x40410+b];chunks+=1
 world=rows(q/'world_phase.csv');play=[x for x in policy if x['root']=='04']
 levels=sorted({int(x['level'])for x in play if x['phase']=='05'})
 round3=[x for x in play if x['level']=='3'and x['phase']=='14']
 history_changes=sorted({x['history']for x in world});gold_changes=sorted({x['gold']for x in world})
 result={'work':117,'status':'PASS_V7_CONTROLLER_EXPERIMENT_'+('THREE_SEGMENT_COMPLETION_OBSERVED'if round3 else'NO_NATURAL_THREE_SEGMENT_CLEAR'),'ROM047_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_sha256':env['source_sha256'],'frames':36000,'runtime_files':len(env['files']),'first_controller_divergence_from_V6':first,'same_V6_prefix_rows':len(prefix),'same_V6_prefix_PNG_RAM_PPU_OAM_mapping_files':same,'prefix_core_state_files_exact':state_exact,'prefix_PNG_full_equality':False,'prefix_PNG_exception_count':len(png_exceptions),'prefix_PNG_exceptions':png_exceptions,'direction_locked_release_bursts':bursts,'direction_lock_verified_samples':lock_samples,'pit_avoid_exempt_samples':pit_exempt,'native_tile_query_levels':dict(query_levels),'native_queries_levels0_2_exact':len(queries)-len(excluded),'native_unique_query_inputs':len(cache),'native_queries_outside_levels0_2_unvalidated_count':len(excluded),'screens':len(screens),'mapped_1KiB_CHR_chunks_exact':chunks,'native_phase5_play_levels':levels,'native_round3_phase14_samples':len(round3),'native_three_segment_completion_observed':bool(round3),'history_values':history_changes,'gold_values':gold_changes,'last_world':world[-1],'last_phase5_play':([x for x in play if x['phase']=='05']or[None])[-1],'ROM_CSV_changes':False,'new_build_apply':False,'direct_assistant_scene_visual':False,'full_game_playthrough':False,'human_approved':False,'release_eligible':False,'frozen_selected_files':files,'limits':['Onecontroller experiment with existingV6plus16frame2Fdirectionhold; no health/time/state/RAM/ROM/PC/currency edit. Actualcontroller-frame decisions logged.','New trajectory/outcome must not be inferred from frozen116times or117PASSintegrity label. Actual native outcome fields separate.','Native tilequery comparison only levels0..2; other later domains explicitly not validated by this classifier.','ThreeprefixPNGexceptions retained despite702exactcore-state and allrawRAM/PPU/OAM/mapping; no fullPNGprefix equality or proven timing diagnosis.','AllmappedCHR/fileSHA checks do not imply allscreensdirectvisualreview or fullgame/hardware/audio/humanapproval.'],'next_action':'Close equivalentV7timeout policy stream; investigate threePNGprefixexceptions against pinnedMesen2.1.1 async capture implementation and preserve boundedactual107/111verification, without rerunning thiswinningbot.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:result[k]for k in ['status','first_controller_divergence_from_V6','same_V6_prefix_PNG_RAM_PPU_OAM_mapping_files','direction_lock_verified_samples','native_phase5_play_levels','native_round3_phase14_samples','history_values','gold_values','last_world']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
