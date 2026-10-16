-- Baseline controller-only trace; window bounds keep raw evidence manageable.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local prg=assert(io.open(out..'/prg_reads.csv','wb'))
local ppu=assert(io.open(out..'/ppu_writes.csv','wb'))
prg:write('frame,pc,cpu_address,file_offset,value\n')
ppu:write('frame,pc,ppu_address,value\n')
emu.addMemoryCallback(function(address,value)
 if frame>=950 and frame<1450 then
  local s=emu.getState()
  if address>=s['cpu.pc'] and address<=s['cpu.pc']+2 then return end
  local m=emu.convertAddress(address,emu.memType.nesMemory)
  prg:write(string.format('%d,%04X,%04X,%05X,%02X\n',frame,s['cpu.pc'],address,m.address+16,value))
 end
end,emu.callbackType.read,0x1C000,0x1FFFF,emu.cpuType.nes,emu.memType.nesPrgRom)
emu.addMemoryCallback(function(address,value)
 if frame>=950 and frame<1450 and address>=0x2000 and address<0x2800 then
  ppu:write(string.format('%d,%04X,%04X,%02X\n',frame,emu.getState()['cpu.pc'],address,value))
 end
end,emu.callbackType.write,0x2000,0x27FF,emu.cpuType.nes,emu.memType.nesPpuMemory)
emu.addEventCallback(function()
 frame=frame+1
 if frame==1500 then
  prg:close();ppu:close()
  local f=assert(io.open(out..'/trace_complete.txt','wb'));f:write(tostring(frame));f:close()
  emu.stop(0)
 end
end,emu.eventType.endFrame)
