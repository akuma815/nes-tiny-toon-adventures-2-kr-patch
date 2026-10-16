from pathlib import Path
import hashlib,json,csv,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/water153_probe_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water153_jump049_v2';e=json.loads((d/'environment.json').read_text('utf-8'))
 assert e['exit_code']==0 and e['frames']==6000 and (d/'trace_complete.txt').read_text()=='6000'
 assert e['intervention']=='controller input only; no state loading or RAM/ROM writes'
 assert e['input']['sequence'][-1]=={'frame':2800,'duration':8,'button':'a'}
 assert all(x['frame']<=2800 for x in e['input']['sequence'])and all(x['button']not in ['right','up','down','b']for x in e['input']['sequence'])
 for f,h in e['files'].items():assert sha(d/f)==h
 lua=(d/'capture_survey_used.lua').read_text('utf-8');assert 'emu.write('not in lua and 'loadSavestate'not in lua
 rom=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert hashlib.sha256(rom).hexdigest()==e['rom_sha256']
 rows=lambda p:list(csv.DictReader(p.open(encoding='utf-8',newline='')))
 player=[{k:int(v)for k,v in x.items()}for x in rows(d/'water_player.csv')]
 native=rows(d/'water_native.csv');jump=[x for x in native if x['pc']=='A80E'];assert len(jump)==1 and jump[0]['pressed']=='128'and jump[0]['jump']=='0'
 gameplay=[x for x in player if x['phase']==5];assert gameplay
 changes=[];prev=None
 for x in gameplay:
  key=(x['state'],x['jump'],x['supportC1'],x['supportC9'])
  if key!=prev:changes.append(x);prev=key
 chunks=0
 for p in d.glob('frame_*_mapping.csv'):
  pp=(d/(p.name[:-12]+'_ppu.bin')).read_bytes()
  for x in rows(p):
   if x['kind']!='chr':continue
   a=int(x['cpu_or_ppu_address'],16);off=int(x['relative_offset'],16);assert pp[a:a+1024]==rom[0x40010+off:0x40410+off];chunks+=1
 finish=[x for x in native if x['pc']in ['A68E','B873']]
 result={'work':153,'status':'PASS_BOUNDED_CONTROLLER_ONLY_WATER_JUMP_OBSERVATION','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'frames':6000,'actual_jump_entry':jump,'native_event_counts':dict(collections.Counter(x['pc']for x in native)),'gameplay_first_last':[gameplay[0]['frame'],gameplay[-1]['frame']],'maximum_vertical_hi':max(x['vertical_hi']for x in gameplay),'state_support_jump_transitions':changes,'natural_clear_observed':bool(finish),'finish_events':finish,'actual_CHR_chunks_match_ROM':chunks,'final_root':(d/'frame_06000_ram.bin').read_bytes()[0x18],'final_phase':(d/'frame_06000_ram.bin').read_bytes()[0x54],'human_approved':False,'release_eligible':False,'limits':['One A press8 frames at2800; no subsequent inputs or RAM intervention','Native jump/terrain discrimination only, not whole game or natural full route pass','Current049 only; no new old/source pair,build/apply,hardware/audio/human approval']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
