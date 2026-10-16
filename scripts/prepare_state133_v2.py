"""Correct unconsumed gate-only exec callback and enforce experiment completion."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
old=R/'scripts/trace_state049_shortage133.lua';new=R/'scripts/trace_state049_shortage133_v2.lua';assert not new.exists()
s=old.read_text('utf-8').replace('local frame=0','local frame=0\nlocal finalize_work133=nil')
s=s.replace("emu.stop(0)","assert(finalize_work133);finalize_work133();emu.stop(0)")
s=s.replace('native NMI exec.','native fixed-bank idle exec, with private226 already mapped.')
s=s.replace('0xfd9e,0xfd9e','0xfe53,0xfe53')
s=s.replace("emu.addEventCallback(function()if frame==limit then assert(saved~=nil and loaded);event('complete');events:close()end end,emu.eventType.endFrame)","finalize_work133=function()assert(saved~=nil and loaded);event('complete');events:close();save('experiment_complete.txt','same049_private226_state_roundtrip')end")
new.write_text(s,'utf-8')
runner=R/'scripts/run_state133_v2.py';assert not runner.exists();s=(R/'scripts/run_state133.py').read_text('utf-8')
s=s.replace("('trace_state049_shortage133.lua','trace_reset049_shortage133.lua')","('trace_state049_shortage133_v2.lua',)")
s=s.replace('native NMI2100 create','native fixed-bank idleFE53 at2100 create')
s=s.replace("assert sha(rom)==rom_sha","assert (output/'experiment_complete.txt').read_text()=='same049_private226_state_roundtrip'\n    assert (output/'same049_native_shortage_lower.state').stat().st_size>0\n    assert sha(rom)==rom_sha")
runner.write_text(s,'utf-8')
q=R/'qa/dialogue/state133_shortage049';obs=R/'qa/reports/state133_v1_observation.json';assert not obs.exists()
assert not (q/'saved_machine_state.txt').exists() and (q/'savestate_events.csv').read_text().count('\n')==1
obs.write_text(json.dumps({'work':133,'status':'FAIL_EXPERIMENT_NOT_EXECUTED_DESPITE_RUNNER_EXIT_ZERO','reason':'FD9E gate/top exec callback was unconsumed in ordinary lower-font dialogue. The old trace_complete marker only proved frames, and stop preceded the appended completeness assertion. No save/load took place; v1 must not be claimed as successful state QA.','v2_changes':'Native idle FE53 actually consumed with226 mapped; explicit finalize before stop and experiment marker/state-file guards','old_lua_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'old_environment_sha256':hashlib.sha256((q/'environment.json').read_bytes()).hexdigest(),'reset_stream':'Separate reset133_shortage049 did request/observe reset; native game initialization grants10 normal tickets and reentry charges10 to6, without reseeding. Use observed success, not assumed zero-ticket shortage.'},indent=2)+'\n','utf-8')
