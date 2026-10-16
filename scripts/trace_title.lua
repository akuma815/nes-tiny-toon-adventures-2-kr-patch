-- Read-only title mapper/PPU-control trace. No RAM/ROM writes.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local f=assert(io.open(out..'/title_registers.csv','wb'))
f:write('frame,scanline,cycle,pc,register,value,bg0_chr_relative,bg1_chr_relative\n')
local function log(address,value)
 if frame>=550 and frame<900 then
  local s=emu.getState()
  local b0=emu.convertAddress(0,emu.memType.nesPpuMemory)
  local b1=emu.convertAddress(0x400,emu.memType.nesPpuMemory)
  f:write(string.format('%d,%s,%s,%04X,%04X,%02X,%05X,%05X\n',frame,tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),s['cpu.pc'],address,value,b0.address,b1.address))
 end
end
for _,a in ipairs({0xA000,0xA008,0xB000,0xB008,0xC000,0xC008,0xD000,0xD008,0x2000,0x2005,0x2006}) do
 emu.addMemoryCallback(log,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==960 then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
