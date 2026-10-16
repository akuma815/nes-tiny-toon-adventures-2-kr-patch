-- Narrow execution trace at verified bank-2 readers; no game writes.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 3100
local f=assert(io.open(out..'/consumer_reads.csv','wb'))
f:write('frame,instruction_cpu,kind,cpu_address,file_offset,value,x,y,script_id\n')
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local a=nil;local kind=nil
 if address==0x9351 then a=0xA1A1+s['cpu.x'];kind='macro_pointer_low'
 elseif address==0x9356 then a=0xA1A2+s['cpu.x'];kind='macro_pointer_high'
 elseif address==0x9360 then a=emu.read(6,emu.memType.nesDebug)+256*emu.read(7,emu.memType.nesDebug)+s['cpu.y'];kind='macro_byte'
 elseif address==0x9393 then a=emu.read(6,emu.memType.nesDebug)+256*emu.read(7,emu.memType.nesDebug)+s['cpu.y'];kind='script_byte'
 end
 if a then
  local m=emu.convertAddress(a,emu.memType.nesMemory)
  local v=emu.read(a,emu.memType.nesDebug)
  f:write(string.format('%d,%04X,%s,%04X,%05X,%02X,%02X,%02X,%02X\n',frame,address,kind,a,m.address+16,v,s['cpu.x'],s['cpu.y'],emu.read(0x6CF,emu.memType.nesDebug)))
 end
end,emu.callbackType.exec,0x5351,0x5393,emu.cpuType.nes,emu.memType.nesPrgRom)
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then
  f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0)
 end
end,emu.eventType.endFrame)
