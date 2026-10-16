from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'scripts/trace_water_damage154.lua';plan=R/'work/water154/run_plan.json';assert not out.exists()and not plan.exists()
 src=R/'scripts/trace_water_progress153_v2.lua';s=src.read_text('utf-8')
 s+=r'''
-- Read-only damage-write telemetry. Keep exact input and prior observation.
local damage=assert(io.open(out..'/damage_events.csv','wb'))
damage:write('event,frame,address,before,value,pc,PRG_relative,preceding3_hex,a,x,y,sp,ps,cycles,bank8000,bankA000,bankC000,bankE000,caller,state,life,boat_art,boat_state,player_xhi,player_xlo,player_yhi,player_ylo,boat_xhi,boat_xlo,boat_yhi,boat_ylo,supportC1,supportC9,jump,vertical_hi,vertical_lo
')
local serial=0
for _,address in ipairs({0x0430,0x07C0})do
 emu.addMemoryCallback(function(a,v)
  local function r(b)return emu.read(b,emu.memType.nesDebug)end
  if r(0x18)~=4 or r(0x25)~=3 or r(0x54)~=5 then return end
  if r(a)==v or (a==0x430 and v~=6)then return end
  serial=serial+1
  local st=emu.getState();local pc=st['cpu.pc'];local pm=emu.convertAddress(pc,emu.memType.nesMemory)
  local bytes={};for k=pc-3,pc-1 do bytes[#bytes+1]=string.format('%02X',r(k))end
  local banks={};for _,b in ipairs({0x8000,0xA000,0xC000,0xE000})do banks[#banks+1]=string.format('%05X',emu.convertAddress(b,emu.memType.nesMemory).address)end
  local caller=r(0x100+((st['cpu.sp']+1)%256))+256*r(0x100+((st['cpu.sp']+2)%256))
  local fields={serial,frame,string.format('%04X',a),r(a),v,string.format('%04X',pc),string.format('%05X',pm.address),table.concat(bytes,''),st['cpu.a'],st['cpu.x'],st['cpu.y'],st['cpu.sp'],st['cpu.ps'],st['cpu.cycleCount'],banks[1],banks[2],banks[3],banks[4],string.format('%04X',caller),r(0x430),r(0x7c0),r(0x401),r(0x421),r(0x4b0),r(0x4a0),r(0x480),r(0x470),r(0x4b1),r(0x4a1),r(0x481),r(0x471),r(0xc1),r(0xc9),r(0x99),r(0x69),r(0x6d)}
  damage:write(table.concat(fields,',')..'
')
  dump(string.format('damage_%04d_before_ram.bin',serial),emu.memType.nesDebug,0x800)
 end,emu.callbackType.write,address,address,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then damage:close()end end,emu.eventType.endFrame)
'''
 # Convert actual line breaks inside the appended short quoted literals only.
 # The raw template above intentionally exposes the two exact boundaries.
 for ending in ["vertical_hi,vertical_lo\n')","..'\n')"]:
  assert s.count(ending)==1;s=s.replace(ending,ending.replace('\n','\\n'))
 for quote in ["'",'"']:
  opened=False;escaped=False
  for ch in s:
   if opened:
    assert ch not in '\r\n'
    if escaped:escaped=False
    elif ch=='\\':escaped=True
    elif ch==quote:opened=False
   elif ch==quote:opened=True
  assert not opened
 assert 'emu.write('not in s and 'loadSavestate'not in s
 out.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':154,'observer_base_sha256':sha(src),'observer_sha256':sha(out),'input_sha256':sha(R/'config/water_jump_probe153.json'),'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water154_damage049 --frames 4200 --inputs config/water_jump_probe153.json --script scripts/trace_water_damage154.lua','scope':'Read-only writes at actual damage/health consumers; same controller input as153 and snapshot identity comparison before any new route input'},indent=2)+'\n','utf-8');print('PASS154 short-string guard; no RAM/ROM writes')
if __name__=='__main__':main()
