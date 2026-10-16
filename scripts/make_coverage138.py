"""Exact registered-source ledger; initialization is never promoted to text reads."""
from pathlib import Path
import collections,csv,hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'workspace/translation/coverage049_138.json';assert not out.exists()
 catalog=R/'extracted/text/table_20261004_001/text_tokens.json'
 cat=json.loads(catalog.read_text('utf-8'))
 csvpath=R/'workspace/translation/text_ja.csv'
 ssot=list(csv.DictReader(csvpath.open(encoding='utf-8-sig',newline='')))
 rompath=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';rom=rompath.read_bytes()
 assert sha(rompath)=='31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa'
 assert len(ssot)==54 and {x['entry_id']for x in ssot}=={x['entry_id']for x in cat['units']}
 sources={catalog.relative_to(R).as_posix():sha(catalog),csvpath.relative_to(R).as_posix():sha(csvpath),rompath.relative_to(R).as_posix():sha(rompath)}
 slots={x['index']:x['unit_id']for x in cat['tables'][0]['slots']}
 units={x['entry_id']:{'entry_id':x['entry_id'],'kind':x['kind'],'reference_ids':x['reference_ids'],'translation_ko':x['translation_ko'],'SSOT_status':x['status'],'current_initializations':[],'current_font_snapshots':[],'historical047_initializations':[],'actual_source_byte_reads':'Not separately captured by these observers; no inferred count','complete_text':'No new complete-text assertion in138; linked scene reports retain their bounded conclusions','human_approved':False}for x in ssot}
 runs=['pages130_intro049','pages130_gate049','pages130_tour049','pages130_booth049','pages130_credits049','clear129_normal3049','clear129_normal4049']
 historical=['gate094_gold4047','gate094_normal50047','gate094_normal49047']
 for name in runs+historical:
  d=R/'qa/dialogue'/name;ep=d/'environment.json';e=json.loads(ep.read_text('utf-8'));assert e['exit_code']==0
  current=name in runs
  assert e['rom_sha256']==(sha(rompath)if current else '82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10')
  sources[ep.relative_to(R).as_posix()]=sha(ep)
  # Recheck frozen telemetry, not files from active emulator runs.
  p=d/'menu_events.csv'
  if p.exists():
   assert sha(p)==e['files'][p.name];sources[p.relative_to(R).as_posix()]=sha(p)
   for row in csv.DictReader(p.open(encoding='utf-8')):
    if row['kind']!='exec' or row['address']!='9445':continue
    slot=int(row['id'],16);assert slot in slots
    ptr=int.from_bytes(rom[0x255a9+2*slot:0x255ab+2*slot],'little')
    assert int(row['pointer'],16)==ptr
    tag=rom[0x5710+2*slot]
    item={'run':name,'frame':int(row['frame']),'slot_hex':f'{slot:02X}','pointer_hex':f'{ptr:04X}','active_font':int(row['active_font'],16),'table_font_tag':tag,'phase_hex':row['phase'],'font_tag_applied':int(row['active_font'],16)==tag,'file':p.relative_to(R).as_posix()}
    units[slots[slot]]['current_initializations'if current else 'historical047_initializations'].append(item)
  if current:
   for filename,h in e['files'].items():
    if not filename.endswith('_ram.bin'):continue
    rp=d/filename;assert sha(rp)==h
    ram=rp.read_bytes();font=ram[0x6f3]
    # Unique main font tags identify only font presence, not completed output or reader execution.
    candidates=[s for s in slots if rom[0x5710+2*s]==font and font!=193]
    if len(candidates)!=1:continue
    slot=candidates[0];mp=d/filename.replace('_ram.bin','_mapping.csv')
    if not mp.exists():continue
    mapping=list(csv.DictReader(mp.open(encoding='utf-8')))
    matches=[z for z in mapping if z['kind']=='chr' and z['cpu_or_ppu_address']=='0000']
    if not matches or int(matches[0]['relative_offset'],16)!=font*1024:continue
    assert sha(mp)==e['files'][mp.name]
    sources[rp.relative_to(R).as_posix()]=h;sources[mp.relative_to(R).as_posix()]=sha(mp)
    units[slots[slot]]['current_font_snapshots'].append({'run':name,'frame':int(filename[6:11]),'font':font,'RAM':rp.relative_to(R).as_posix(),'mapping':mp.relative_to(R).as_posix(),'scope':'RAM tag plus real mapped CHR bank; completion and actual reader bytes remain separate'})
 for u in units.values():
  u['coverage_class']=('current_init_and_font'if u['current_initializations']and u['current_font_snapshots']else 'current_init_only'if u['current_initializations']else 'current_font_only'if u['current_font_snapshots']else 'historical047_init_only'if u['historical047_initializations']else 'not_linked_in_selected_runs')
  if u['kind']=='macro':u['coverage_class']='shared_macro_requires_reader_link';u['complete_text']='Macro use cannot be established from font/page initialization alone'
 result={'work':138,'status':'PASS_SCOPED_REGISTERED_SOURCE_LEDGER','registered_unique_units':54,'main_slots':48,'scope':'Seven completed049 runs plus three explicitly historical047 branch runs. This is a bounded evidence index, not exhaustive corpus coverage or an unused-text search.','ROM_sha256':sha(rompath),'CSV_sha256':sha(csvpath),'classes':dict(collections.Counter(u['coverage_class']for u in units.values())),'units':list(units.values()),'verified_inputs':sources,'linked_completion_reports':['qa/reports/clear129_validation.json','qa/reports/pages130_validation.json','qa/reports/state133_validation.json'],'next_action':'Run current049 gold4 castle branch using frozen094 input/seed/observer, compare to historical047 and verify slot1C plus header22/28 and departure2A lifecycle; this is newly covered current049 branch, not another shortage replay.','human_approved':False,'release_eligible':False}
 assert not units['MAIN_05824']['current_initializations'] and units['MAIN_05824']['historical047_initializations']
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({'status':result['status'],'classes':result['classes'],'selected_gap':'MAIN_05824 slot1C; gold4 castle'},ensure_ascii=False))
if __name__=='__main__':main()
