local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local n=0
local f=assert(io.open(out..'/chr_stream_copies.csv','wb'))
f:write('frame,copy_id,selector,ppu_start,ppu_end_exclusive,chr_relative_start\n')
emu.addMemoryCallback(function(address,value)
 if address==0x8216 and frame>=550 and frame<650 then
  local s=emu.getState();local selector=s['cpu.x'];local base=0x8233+selector
  local lo=emu.read(base,emu.memType.nesDebug)+256*emu.read(base+1,emu.memType.nesDebug)
  local hi=emu.read(base+2,emu.memType.nesDebug)+256*emu.read(base+3,emu.memType.nesDebug)
  local mapped=emu.convertAddress(lo,emu.memType.nesPpuMemory)
  n=n+1
  local bytes={};for i=0,hi-lo-1 do bytes[#bytes+1]=string.char(emu.read(0x400+i,emu.memType.nesDebug)) end
  local h=assert(io.open(out..'/copy_'..n..'.bin','wb'));h:write(table.concat(bytes));h:close()
  f:write(string.format('%d,%d,%02X,%04X,%04X,%05X\n',frame,n,selector,lo,hi,mapped.address))
 end
end,emu.callbackType.exec,0x4216,0x4216,emu.cpuType.nes,emu.memType.nesPrgRom)
emu.addEventCallback(function()
 frame=frame+1
 if frame==720 then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
