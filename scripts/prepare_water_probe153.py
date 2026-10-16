from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 lua=R/'scripts/trace_water_progress153.lua';inp=R/'config/water_jump_probe153.json';plan=R/'work/water153/run_plan.json'
 assert not lua.exists()and not inp.exists()and not plan.exists()
 base=R/'scripts/trace_train_reader142.lua';s=base.read_text('utf-8')
 s+='''
-- Water read-only native gameplay discrimination; controller sequence only.
local player=assert(io.open(out..'/water_player.csv','wb'))
player:write('frame,root,phase,course,state,subphase,pressed,held,jump,supportC1,supportC9,vertical_hi,vertical_lo,x_hi,x_lo,y_hi,y_lo,life,clear_count\n')
emu.addEventCallback(function()
 local function r(a)return emu.read(a,emu.memType.nesDebug)end
 if r(0x25)==3 and r(0x18)==4 then
  local fields={frame,r(0x18),r(0x54),r(0x25),r(0x430),r(0x550),r(0x50),r(0x52),r(0x99),r(0xc1),r(0xc9),r(0x69),r(0x6d),r(0x4b0),r(0x4a0),r(0x480),r(0x470),r(0x7c0),r(0x725)}
  player:write(table.concat(fields,',')..'\\n')
 end
 if frame==limit then player:close()end
end,emu.eventType.endFrame)
local native=assert(io.open(out..'/water_native.csv','wb'))
native:write('frame,pc,PRG_relative,state,pressed,held,jump,supportC1,supportC9,vertical_hi,vertical_lo\n')
for _,pc in ipairs({0xA80E,0xA68E,0xACDF,0xB873,0xA8E2,0xA7CF})do
 emu.addMemoryCallback(function(a,v)
  local m=emu.convertAddress(a,emu.memType.nesMemory)
  if m.memType~=emu.memType.nesPrgRom or m.address~=0x30000+a-0x8000 then return end
  local function r(b)return emu.read(b,emu.memType.nesDebug)end
  if r(0x25)~=3 then return end
  native:write(string.format('%d,%04X,%05X,%d,%d,%d,%d,%d,%d,%d,%d\\n',frame,a,m.address,r(0x430),r(0x50),r(0x52),r(0x99),r(0xc1),r(0xc9),r(0x69),r(0x6d)))
 end,emu.callbackType.exec,pc,pc,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then native:close()end end,emu.eventType.endFrame)
'''
 assert 'emu.write('not in s and 'loadSavestate'not in s
 lua.write_text(s,'utf-8')
 seq=json.loads((R/'config/menu_water_001.json').read_text('utf-8'));seq=[z for z in seq if z['frame']<=2600];seq.append({'frame':2800,'duration':8,'button':'a'})
 inp.write_text(json.dumps(seq,indent=2)+'\n','utf-8')
 plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':153,'observer_base_SHA':sha(base),'observer_SHA':sha(lua),'input_SHA':sha(inp),'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water153_jump049 --frames 6000 --inputs config/water_jump_probe153.json --script scripts/trace_water_progress153.lua','scope':'One new native jump discriminator at2800; no RAM/ROM/state writes or equivalent cartbot retries'},indent=2)+'\n','utf-8')
 print('Prepared153 controller-only jump probe')
if __name__=='__main__':main()
