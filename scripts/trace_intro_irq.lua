-- Read-only actual IRQ instruction/PPU/mapper timing. No state or memory writes.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 1050
local f=assert(io.open(out..'/irq_phase.csv','wb'))
f:write('frame,kind,pc,address,value,scanline,dot,cycles\n')
local function record(kind,address,value)
 if frame>=1800 and frame<=2820 then
  local s=emu.getState()
  f:write(string.format('%d,%s,%04X,%04X,%02X,%s,%s,%s\n',frame,kind,s['cpu.pc'],address,value,tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),tostring(s['cpu.cycleCount'])))
 end
end
emu.addMemoryCallback(function(a,v) record('exec',a,v) end,emu.callbackType.exec,0xfb97,0xfb97,emu.cpuType.nes,emu.memType.nesMemory)
for _,a in ipairs({0xa000,0xa008,0xb000,0xb008,0x2000,0x2005,0x2006}) do
 emu.addMemoryCallback(function(p,v) record('write',p,v) end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
