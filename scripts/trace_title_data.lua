local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local f=assert(io.open(out..'/title_data_reads.csv','wb'))
f:write('frame,pc,cpu_address,file_offset,value\n')
emu.addMemoryCallback(function(address,value)
 if frame>=550 and frame<700 then
  local s=emu.getState();local m=emu.convertAddress(address,emu.memType.nesMemory)
  f:write(string.format('%d,%04X,%04X,%05X,%02X\n',frame,s['cpu.pc'],address,m.address+16,value))
 end
end,emu.callbackType.read,0x12900,0x12DFF,emu.cpuType.nes,emu.memType.nesPrgRom)
emu.addEventCallback(function()
 frame=frame+1
 if frame==720 then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
