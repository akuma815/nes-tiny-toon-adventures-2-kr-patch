from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=R/'scripts/trace_booth_reader141.lua';assert not p.exists()
 s=(R/'scripts/trace_branch_seed_v1.lua').read_text('utf-8')
 insertion="""
-- Physical PRG data reads in registered main/macro body regions only.
-- Does not change CPU registers, input timing, ROM, or return read values.
local textlog=assert(io.open(out..'/prg_text_reads.csv','wb'))
textlog:write('frame,pc,cycles,cpu_address,PRG_relative_offset,value,native_id,pointer,active_font\\n')
emu.addMemoryCallback(function(a,v)
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.memType~=emu.memType.nesPrgRom then return end
 local f=m.address+0x10
 if not(f>=0x25609 and f<0x25A28 or f>=0x261C3 and f<0x261FF) then return end
 local t=emu.getState()
 local function r(x)return emu.read(x,emu.memType.nesDebug)end
 textlog:write(string.format('%d,%04X,%s,%04X,%05X,%02X,%02X,%04X,%02X\\n',frame,t['cpu.pc'],tostring(t['cpu.cycleCount']),a,m.address,v,r(0x6cf),r(0x6cd)+256*r(0x6ce),r(0x6f3)))
end,emu.callbackType.read,0x9000,0xBFFF,emu.cpuType.nes,emu.memType.nesMemory)
"""
 marker='emu.addEventCallback(function()\n frame=frame+1';assert marker in s
 s=s.replace(marker,insertion+'\n'+marker).replace("seedlog:close();log:close();save('trace_complete.txt'","textlog:close();seedlog:close();log:close();save('trace_complete.txt'")
 p.write_text(s,'utf-8')
 p=R/'scripts/run_branch_reader141.py';assert not p.exists()
 s=(R/'scripts/run_branch_seed_qa.py').read_text('utf-8').replace("('trace_branch_seed_v1.lua','trace_branch_seed_irq_v1.lua')","('trace_booth_reader141.lua',)")
 p.write_text(s,'utf-8')
 p=R/'work/booth141/preparation.json';assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps({'work':141,'scope':'New current049 successful booth exchange plus fresh047 paired reader observer. Source mapped physical body reads only; page init and read are distinct.','main_file_range':[0x25609,0x25a28],'macro_file_range':[0x261c3,0x261ff],'observer_sha256':sha(R/'scripts/trace_booth_reader141.lua'),'historical_route':'booth039_points3_irq (only inputs/seed reused; not current baseline)'},indent=2)+'\n','utf-8')
 print('prepared booth141 physical PRG reader observer')
if __name__=='__main__':main()
