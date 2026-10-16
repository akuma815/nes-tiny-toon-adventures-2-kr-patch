from pathlib import Path
import json
from seal_continuation159 import R,sha
def main():
 lua=R/'scripts/trace_water_fish161.lua';plan=R/'work/water161/run_plan.json';assert not lua.exists()and not plan.exists()
 src=R/'scripts/trace_water_transfer160.lua';s=src.read_text('utf-8')+r'''
local fish=assert(io.open(out..'/fish_actors.csv','wb'))
fish:write('frame,slot,type,state,shape,x,y_packed240,vx_word,vy_word,player_x,player_y_packed240,player_jump,player_support,player_life\n')
emu.addEventCallback(function()
 if frame>=4200 and frame<=5000 and r(0x18)==4 and r(0x54)==5 and r(0x25)==3 then
  for i=2,15 do
   if r(0x420+i)==0x34 then
    local f={frame,i,r(0x420+i),r(0x430+i),r(0x530+i),w(0x4a0+i,0x4b0+i),r(0x470+i)+240*r(0x480+i),w(0x4e0+i,0x4f0+i),w(0x4c0+i,0x4d0+i),w(0x4a0,0x4b0),r(0x470)+240*r(0x480),r(0x99),r(0xc1),r(0x7c0)}
    fish:write(table.concat(f,',')..'\n')
   end
  end
 end
 if frame==limit then fish:close()end
end,emu.eventType.endFrame)
local physics=assert(io.open(out..'/fish_physics_writes.csv','wb'))
physics:write('event,frame,slot,address,before,value,pc,PRG_relative,preceding3_hex,a,x,y,sp,ps,cycles,bank8000,bankA000,bankC000,bankE000\n')
local phyid=0
local function tracewrite(a,v,i)
 if r(0x18)~=4 or r(0x25)~=3 then return end
 local st=emu.getState();local pc=st['cpu.pc'];local pm=emu.convertAddress(pc,emu.memType.nesMemory);phyid=phyid+1
 local bytes={};for k=pc-3,pc-1 do bytes[#bytes+1]=string.format('%02X',r(k))end
 local banks={};for _,b in ipairs({0x8000,0xA000,0xC000,0xE000})do banks[#banks+1]=string.format('%05X',emu.convertAddress(b,emu.memType.nesMemory).address)end
 local f={phyid,frame,i,string.format('%04X',a),r(a),v,string.format('%04X',pc),string.format('%05X',pm.address),table.concat(bytes,''),st['cpu.a'],st['cpu.x'],st['cpu.y'],st['cpu.sp'],st['cpu.ps'],st['cpu.cycleCount'],banks[1],banks[2],banks[3],banks[4]}
 physics:write(table.concat(f,',')..'\n');dump(string.format('physics_%04d_before_ram.bin',phyid),emu.memType.nesDebug,0x800)
end
for i=2,15 do
 for _,a in ipairs({0x430+i,0x4c0+i,0x4d0+i})do
  emu.addMemoryCallback(function(p,v)
   if frame>=4400 and frame<=4700 and r(0x420+i)==0x34 then tracewrite(p,v,i)end
  end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
 end
end
emu.addMemoryCallback(function(a,v)if r(a)~=v then tracewrite(a,v,-1)end end,emu.callbackType.write,0x716,0x716,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then physics:close()end end,emu.eventType.endFrame)
'''
 for quote in ["'",'"']:
  opened=False;esc=False
  for ch in s:
   if opened:
    assert ch not in '\r\n'
    if esc:esc=False
    elif ch=='\\':esc=True
    elif ch==quote:opened=False
   elif ch==quote:opened=True
  assert not opened
 assert 'emu.write('not in s and 'loadSavestate'not in s
 lua.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':161,'base_sha256':sha(src),'observer_sha256':sha(lua),'frames':5100,'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water161_fish_consumer049 --frames 5100 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_fish161.lua','scope':'Same160 inputs; read-only type34 velocity/state stores with beforeRAM/register/physicalPC and0716 store, require snapshot/input identity first.'},indent=2)+'\n','utf-8');print('PASS161 preflight')
if __name__=='__main__':main()
