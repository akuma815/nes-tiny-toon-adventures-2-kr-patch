from pathlib import Path
import json
from seal_continuation159 import R,sha
def main():
 lua=R/'scripts/trace_water_rope165.lua';plan=R/'work/water165/run_plan.json';assert not lua.exists()and not plan.exists()
 src=R/'scripts/trace_water_hold163.lua';s=src.read_text('utf-8')
 key='r(0x422)==1 and ahead>32';assert s.count(key)==1;s=s.replace(key,'(r(0x422)==1 or r(0x422)==2) and ahead>32')
 key='if transferring and r(0x716)~=transfer_stage then';assert s.count(key)==1
 addition=r'''
  if transferring and r(0xc9)~=0 then
   transferlog:write(string.format('%d,native_rope_capture,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,r(0x716),w(0x4a0,0x4b0),w(0x4a1,0x4b1),w(0x4a2,0x4b2),w(0x4c1,0x4d1),r(0x99),r(0xc1),r(0x7c0)))
   transferring=false
  end
'''
 s=s.replace(key,addition+'\n  '+key)
 key='if input.a or r(0x99)~=0 and r(0xc1)==0 then';assert s.count(key)==1;s=s.replace(key,'if r(0xc9)==0 and (input.a or r(0x99)~=0 and r(0xc1)==0) then')
 s+=r'''
local rope=assert(io.open(out..'/rope_capture_writes.csv','wb'))
rope:write('event,frame,address,before,value,pc,PRG_relative,preceding3_hex,a,x,y,sp,ps,cycles\n')
local ropeid=0;local observed={}
for _,a in ipairs({0xc9,0x541})do
 emu.addMemoryCallback(function(p,v)
  if observed[p]or v~=1 or r(0x18)~=4 or r(0x25)~=3 or r(0x422)~=2 then return end
  local st=emu.getState();local pc=st['cpu.pc'];local pm=emu.convertAddress(pc,emu.memType.nesMemory)
  if pm.memType~=emu.memType.nesPrgRom or pm.address~=0x30000+pc-0x8000 then return end
  observed[p]=true;ropeid=ropeid+1
  local bytes={};for k=pc-3,pc-1 do bytes[#bytes+1]=string.format('%02X',r(k))end
  local f={ropeid,frame,string.format('%04X',p),r(p),v,string.format('%04X',pc),string.format('%05X',pm.address),table.concat(bytes,''),st['cpu.a'],st['cpu.x'],st['cpu.y'],st['cpu.sp'],st['cpu.ps'],st['cpu.cycleCount']}
  rope:write(table.concat(f,',')..'\n');dump(string.format('rope_%02d_before_ram.bin',ropeid),emu.memType.nesDebug,0x800)
 end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then rope:close()end end,emu.eventType.endFrame)
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
 assert 'emu.write('not in s and 'loadSavestate'not in s;lua.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':165,'base_sha256':sha(src),'observer_sha256':sha(lua),'rope_model_sha256':sha(R/'qa/reports/water164_rope_model.json'),'frames':11500,'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water165_rope_capture049 --frames 11500 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_rope165.lua','scope':'Type2 target jump on nativefall condition, stop air-follow whenC9 active; first actualC9/0541 stores read-only, no RAM/state/ROM writes. No clear assumed.'},indent=2)+'\n','utf-8');print('PASS165 preflight')
if __name__=='__main__':main()
