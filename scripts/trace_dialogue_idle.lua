-- Read-only actual IRQ instruction/PPU/mapper timing. No state or memory writes.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 1050
local f=assert(io.open(out..'/irq_phase.csv','wb'))
f:write('frame,kind,pc,address,value,scanline,dot,cycles\n')
local function record(kind,address,value)
 if frame>=938 and frame<=1005 then
  local s=emu.getState()
  f:write(string.format('%d,%s,%04X,%04X,%02X,%s,%s,%s\n',frame,kind,s['cpu.pc'],address,value,tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),tostring(s['cpu.cycleCount'])))
 end
end
emu.addMemoryCallback(function(a,v) if frame~=939 then return end; local z=emu.getState(); if z['ppu.scanline']>=90 and z['ppu.scanline']<=91 then record('idle',a,v) end end,emu.callbackType.exec,0x8000,0xffff,emu.cpuType.nes,emu.memType.nesMemory)
for _,a in ipairs({0xa000,0xa008,0xb000,0xb008,0x2000,0x2005,0x2006}) do
 emu.addMemoryCallback(function(p,v) record('write',p,v) end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
