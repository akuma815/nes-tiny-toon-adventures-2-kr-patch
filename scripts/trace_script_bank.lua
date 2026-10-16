-- Source-only data-bank trace, including temporary bank selection.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local f=assert(io.open(out..'/script_bank_reads.csv','wb'))
f:write('frame,pc,cpu_address,file_offset,value,a,x,y\n')
emu.addMemoryCallback(function(address,value)
 if frame>=950 and frame<1450 then
  local s=emu.getState()
  if address>=s['cpu.pc'] and address<=s['cpu.pc']+2 then return end
  local m=emu.convertAddress(address,emu.memType.nesMemory)
  f:write(string.format('%d,%04X,%04X,%05X,%02X,%02X,%02X,%02X\n',frame,s['cpu.pc'],address,m.address+16,value,s['cpu.a'],s['cpu.x'],s['cpu.y']))
 end
end,emu.callbackType.read,0x4000,0x5FFF,emu.cpuType.nes,emu.memType.nesPrgRom)
emu.addEventCallback(function()
 frame=frame+1
 if frame==1500 then
  f:close()
  local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close()
  emu.stop(0)
 end
end,emu.eventType.endFrame)
