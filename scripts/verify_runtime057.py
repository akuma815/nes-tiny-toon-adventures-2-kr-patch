"""Bounded reset comparison andfour controller-only longworld traces; no wholeclear claim."""
from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/runtime057_validation.json';assert not out.exists();rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';data=rom.read_bytes();rh=sha(rom);src=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/src['path'])==src['sha256'];runs=[];frozen=0;chunks=0;images=0
 names=['reset039_coaster_reference','reset043_coaster']+[f'world043_{ride}_controller'for ride in ('coaster','cart','train','water')]
 for name in names:
  q=R/'qa/dialogue'/name;e=json.loads((q/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and(q/'trace_complete.txt').read_text()==str(e['frames']);expected=R/('build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes'if name.startswith('reset039')else 'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes');assert e['rom_sha256']==sha(expected)
  for n,h in e['files'].items():assert sha(q/n)==h;frozen+=1
  blob=expected.read_bytes();ps=sorted(q.glob('frame_*.png'));activebanks=set()
  for p in ps:
   tag=p.stem;ppu=(q/(tag+'_ppu.bin')).read_bytes()
   for m in csv.DictReader((q/(tag+'_mapping.csv')).open()):
    if m['kind']!='chr':continue
    a=int(m['cpu_or_ppu_address'],16);b=int(m['relative_offset'],16);assert ppu[a:a+1024]==blob[0x40010+b:0x40410+b],(name,tag,m);activebanks.add(b//1024);chunks+=1
  rows=list(csv.DictReader((q/'world_phase.csv').open()));assert len(rows)==e['frames']//30;phases=collections.Counter(r['phase']for r in rows if r['root']=='04');native_bonus=any(r['root']=='04'and 20<=int(r['phase'],16)<=24 for r in rows)
  if name.startswith('reset'):
   events=list(csv.DictReader((q/'reset_events.csv').open()));assert [r['kind']for r in events]==['request_console_reset','actual_reset_event','complete'];assert events[0]['frame']=='3600'and events[0]['root']=='04'and events[0]['phase']=='05'and events[0]['course']=='00';assert events[1]['frame']=='3601';assert any(r['root']=='05'and 3600<int(r['frame'])<4500 for r in rows);assert any(r['root']=='00'and 3600<int(r['frame'])<4500 for r in rows);assert any(r['root']=='04'and r['phase']=='05'and int(r['frame'])>5600 for r in rows)
  else:assert e['frames']==18000 and e['intervention']=='controller input only; no state loading or RAM/ROM writes'and not native_bonus
  images+=len(ps);runs.append({'QA':name,'frames':e['frames'],'screens':len(ps),'intervention':e['intervention'],'native_play_samples':phases.get('05',0),'root4_phase_counts':dict(phases),'sampled_CHR_banks':sorted(activebanks),'bonus20_24_observed':native_bonus,'last_sample':rows[-1]})
 a=R/'qa/dialogue/reset039_coaster_reference';b=R/'qa/dialogue/reset043_coaster';assert(a/'reset_events.csv').read_bytes()==(b/'reset_events.csv').read_bytes();assert(a/'world_phase.csv').read_bytes()==(b/'world_phase.csv').read_bytes()
 hud=json.loads((R/'qa/reports/reset057_HUD_pixels.json').read_text('utf-8'));assert hud['status']=='PASS'and hud['result']['screens']==435
 report={'work':57,'status':'PASS','status_scope':'Declared console-reset/reboot/re-entry, actual435 reset comparison andfour bounded18k controller paths; no wholegameclear','ROM_sha256':rh,'source_sha256':src['sha256'],'ROM_SSOT_changes':0,'runs':runs,'screens_including_both_reset_sides':images,'runtime_frozen_files':frozen,'mapped_CHR_1K_chunks_exact':chunks,'reset_events_worldphase_byteexact_reference039':True,'reset_HUD_comparison':hud['result'],'reset_anchor_scope_corrected':'190 supplied establishedcoaster geometry and actualsource/newRGB glyph/number checks, no57 fullIRQ collection; see separateerratum','save_loading_in_reset_runs':False,'controller_long_route_naturalclear_proof':False,'limits':['Coaster/train/water fail andreturnmenu underrecordedinputs; cart remainsplay at18k. None reachesnativebonus20..24','No handlives/currency/phase/PC/ROM intervention inlongroutes; onlyresetAPI intervention inresetpair','Originalnative wholeplay/audio/hardware/finalhumanlanguage andallreset situations notverified','No save-state compatibility claim. Frozen55 reviewpackage notes describe its own earlierQA state.','Registered/source graphicalclosure remains bounded, not wholecorpus absenceproof'],'next_action':'Inspect official save-state API and validate same43 state roundtrip innativeexec callback, separately from old-build state compatibility.'}
 out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in ('status','screens_including_both_reset_sides','runtime_frozen_files','mapped_CHR_1K_chunks_exact','reset_events_worldphase_byteexact_reference039')},indent=2))
if __name__=='__main__':main()
