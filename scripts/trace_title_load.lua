local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local p=assert(io.open(out..'/ppu_load.csv','wb'))
local counts={}
p:write('frame,pc,ppu_address,value\n')
emu.addMemoryCallback(function(address,value)
 if frame>=550 and frame<650 then
  p:write(string.format('%d,%04X,%04X,%02X\n',frame,emu.getState()['cpu.pc'],address,value))
 end
end,emu.callbackType.write,0x2000,0x2FFF,emu.cpuType.nes,emu.memType.nesPpuMemory)
emu.addMemoryCallback(function(address,value)
 if frame>=550 and frame<650 then
  local s=emu.getState();local pc=s['cpu.pc'];local m=emu.convertAddress(pc,emu.memType.nesMemory)
  local key=string.format('%04X,%05X',pc,m.address+16)
  counts[key]=(counts[key] or 0)+1
 end
end,emu.callbackType.write,0x0100,0x01FF,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 frame=frame+1
 if frame==720 then
  p:close();local h=assert(io.open(out..'/queue_writers.csv','wb'));h:write('pc,file_offset,count\n')
  for k,v in pairs(counts) do h:write(k..','..v..'\n') end;h:close()
  h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0)
 end
end,emu.eventType.endFrame)
