from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 lua=R/'scripts/trace_water_exit_input158.lua';plan=R/'work/water158/run_plan.json';assert not lua.exists()and not plan.exists()
 base=R/'scripts/trace_water_controller157.lua';s=base.read_text('utf-8').replace('vertical_hi,vertical_lo','cameraX_hi,cameraX_lo')
 s+=r'''
-- Read-only controller bus and RAM52 writes. Never read IO4016 in a callback.
local bus=assert(io.open(out..'/controller_bus.csv','wb'))
bus:write('event,frame,kind,address,value,pc,PRG_relative,cycles,poll_epoch,held_before,phase,root\n')
local busid=0
local function busrecord(kind,a,v)
 if frame<3300 or frame>4050 then return end
 local st=emu.getState();local pc=st['cpu.pc'];local pm=emu.convertAddress(pc,emu.memType.nesMemory)
 busid=busid+1
 bus:write(string.format('%d,%d,%s,%04X,%d,%04X,%05X,%s,%d,%d,%d,%d\n',busid,frame,kind,a,v,pc,pm.address,tostring(st['cpu.cycleCount']),polls,r(0x52),r(0x54),r(0x18)))
end
emu.addMemoryCallback(function(a,v)busrecord('strobe_write',a,v)end,emu.callbackType.write,0x4016,0x4016,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)busrecord('serial_read',a,v)end,emu.callbackType.read,0x4016,0x4016,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)busrecord('held_write',a,v)end,emu.callbackType.write,0x52,0x52,emu.cpuType.nes,emu.memType.nesMemory)
local exits=assert(io.open(out..'/water_exit.csv','wb'))
exits:write('event,frame,pc,PRG_relative,cycles,a,x,y,sp,ps,root,phase,state,player_yhi,player_ylo,cameraX_hi,cameraX_lo,cameraY_hi,cameraY_lo,life\n')
local exitid=0
for _,pc in ipairs({0xA658,0xA65A,0xA65C})do
 emu.addMemoryCallback(function(a,v)
  local pm=emu.convertAddress(a,emu.memType.nesMemory)
  if pm.memType~=emu.memType.nesPrgRom or pm.address~=0x30000+a-0x8000 or r(0x18)~=4 or r(0x25)~=3 then return end
  exitid=exitid+1;local st=emu.getState()
  local fields={exitid,frame,string.format('%04X',a),string.format('%05X',pm.address),st['cpu.cycleCount'],st['cpu.a'],st['cpu.x'],st['cpu.y'],st['cpu.sp'],st['cpu.ps'],r(0x18),r(0x54),r(0x430),r(0x480),r(0x470),r(0x69),r(0x6d),r(0x68),r(0x6b),r(0x7c0)}
  exits:write(table.concat(fields,',')..'\n')
  dump(string.format('exit_%03d_before_ram.bin',exitid),emu.memType.nesDebug,0x800)
 end,emu.callbackType.exec,pc,pc,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then bus:close();exits:close()end end,emu.eventType.endFrame)
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
 assert 'emu.write('not in s and 'loadSavestate'not in s and 'emu.read(0x4016'not in s
 lua.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':158,'base_observer_sha256':sha(base),'observer_sha256':sha(lua),'frames':4500,'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water158_exit_input049 --frames 4500 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_exit_input158.lua','scope':'Same157 controller policy; added read-only actual4016 bus/RAM52 writes and native bottom-exit callbacks. Correct camera axis header only. Require input and snapshot exact before interpretation.'},indent=2)+'\n','utf-8');print('PASS158 preflight')
if __name__=='__main__':main()
