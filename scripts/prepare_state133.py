"""Freeze same049 lower-font state/reset experiments; original seed driver retained."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/trace_branch_seed_v1.lua').read_text('utf-8')
state='''
-- Work133: same049 state at completed private226 shortage; native NMI exec.
local saved=nil;local loaded=false
local events=assert(io.open(out..'/savestate_events.csv','wb'));events:write('frame,kind,pc,cycle,root,phase,course,headfont,lowerfont,CHR0_relative,CHR400_relative\\n')
local function event(kind)
 local s=emu.getState();local function r(a)return emu.read(a,emu.memType.nesDebug)end
 local a=emu.convertAddress(0,emu.memType.nesPpuMemory);local b=emu.convertAddress(0x400,emu.memType.nesPpuMemory)
 events:write(string.format('%d,%s,%04X,%s,%02X,%02X,%02X,%02X,%02X,%05X,%05X\\n',frame,kind,s['cpu.pc'],tostring(s['cpu.cycleCount']),r(0x18),r(0x54),r(0x25),r(0x34),r(0x6f3),a.address,b.address));events:flush()
end
local function machine(tag)
 dump(tag..'_ram.bin',emu.memType.nesDebug,0x800);dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000);dump(tag..'_oam.bin',emu.memType.nesSpriteRam,256)
 local rows={};for k,v in pairs(emu.getState())do rows[#rows+1]=tostring(k)..'='..tostring(v)end;table.sort(rows);save(tag..'_state.txt',table.concat(rows,'\\n'))
end
emu.addEventCallback(function()event('stateLoaded_event')end,emu.eventType.stateLoaded)
emu.addMemoryCallback(function(a,v)
 if frame==2100 and saved==nil then
  assert(emu.read(0x18,emu.memType.nesDebug)==8 and emu.read(0x54,emu.memType.nesDebug)==0 and emu.read(0x25,emu.memType.nesDebug)==1)
  assert(emu.read(0x6f3,emu.memType.nesDebug)==226 and emu.convertAddress(0,emu.memType.nesPpuMemory).address==0x38800)
  machine('precreate_machine');saved=emu.createSavestate();machine('saved_machine');assert(type(saved)=='string'and#saved>0);save('same049_native_shortage_lower.state',saved);event('created_in_exec')
 elseif frame==2400 and not loaded then
  assert(saved~=nil);loaded=true;machine('before_load_machine');event('request_load_in_exec');emu.loadSavestate(saved);machine('restored_machine');event('returned_from_load_in_exec')
 end
end,emu.callbackType.exec,0xfd9e,0xfd9e,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then assert(saved~=nil and loaded);event('complete');events:close()end end,emu.eventType.endFrame)
'''
reset='''
-- Work133: console reset while private226 active; only original1000 ticket seed.
local requested=false;local reset_count=0;local loads=0
local events=assert(io.open(out..'/reset_events.csv','wb'));events:write('frame,kind,pc,cycle,root,phase,course,headfont,lowerfont\\n')
local function event(kind)
 local s=emu.getState();local function r(a)return emu.read(a,emu.memType.nesDebug)end
 events:write(string.format('%d,%s,%04X,%s,%02X,%02X,%02X,%02X,%02X\\n',frame,kind,s['cpu.pc'],tostring(s['cpu.cycleCount']),r(0x18),r(0x54),r(0x25),r(0x34),r(0x6f3)));events:flush()
end
emu.addEventCallback(function()reset_count=reset_count+1;event('actual_reset_event')end,emu.eventType.reset)
emu.addEventCallback(function()loads=loads+1;event('unexpected_state_load');error('Reset-only experiment must not load state')end,emu.eventType.stateLoaded)
emu.addEventCallback(function()
 if frame==2160 then
  assert(not requested and loads==0 and emu.read(0x6f3,emu.memType.nesDebug)==226)
  requested=true;event('request_console_reset');emu.reset()
 end
 if frame==limit then assert(requested and reset_count==1 and loads==0);event('complete');events:close()end
end,emu.eventType.endFrame)
'''
for n,s in [('trace_state049_shortage133.lua',base+state),('trace_reset049_shortage133.lua',base+reset)]:
 p=R/'scripts'/n;assert not p.exists();p.write_text(s,'utf-8')
p=R/'scripts/run_state133.py';assert not p.exists();s=(R/'scripts/run_branch_seed_qa.py').read_text('utf-8')
s=s.replace("('trace_branch_seed_v1.lua','trace_branch_seed_irq_v1.lua')","('trace_state049_shortage133.lua','trace_reset049_shortage133.lua')")
s=s.replace("'intervention':'Explicit initial RAM seed at recorded frame; controller inputs thereafter; no state load or ROM writes; not normal gameplay'","'intervention':('Initial1000 ticket3 seed only; native NMI2100 create same049 lower226 state, load2400; controller thereafter, no manual PC/ROM edits' if 'trace_state' in a.script.name else 'Initial1000 ticket3 seed only; console reset2160, repeated controller route, no state load/manual PC/ROM edits or reseed after reset')")
s=s.replace("'scope':'Controlled ticket/point branch QA. Numerical state intentionally seeded; direct visual review separate; no full playthrough.'","'scope':'Same049 shortage state/reset experiment. Initial tickets seeded; no crossbuild state compatibility, all save/reset contexts, full playthrough or PCM claim.'")
p.write_text(s,'utf-8')
events=json.loads((R/'config/menu_coaster_001.json').read_text('utf-8'));out=R/'config/reset133_coaster.json';assert not out.exists()
first=[e for e in events if e['frame']<2160];second=[dict(e,frame=e['frame']+2160) for e in events]
out.write_text(json.dumps(first+second,indent=2)+'\n','utf-8')
print('Prepared133 immutable drivers/state/reset Lua/input')
