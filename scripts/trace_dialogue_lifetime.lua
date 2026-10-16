-- Native consumers and font lifetime. Read only; controller input is the sole intervention.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 3100
local start=tonumber(os.getenv('TTA2_START')) or -1
local f=assert(io.open(out..'/lifetime.csv','wb'))
f:write('frame,scanline,cycle,kind,pc,address,value,script_id,stream_ptr,dest,shadow34,shadow35,queue_size,wait\n')
local function read(a) return emu.read(a,emu.memType.nesDebug) end
local function log(kind,address,value)
 local s=emu.getState()
 f:write(string.format('%d,%s,%s,%s,%04X,%04X,%02X,%02X,%04X,%04X,%02X,%02X,%02X,%02X\n',frame,tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),kind,s['cpu.pc'],address,value,read(0x6cf),read(0x6cd)+256*read(0x6ce),read(0x6c0)+256*read(0x6c1),read(0x34),read(0x35),read(0x1e),read(0x58)))
end
for _,a in ipairs({0x34,0x35,0x6cf,0x6cd,0x6ce,0xA000,0xA008}) do
 emu.addMemoryCallback(function(address,value)
  if frame>=700 then log('write',address,value) end
 end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
for _,pair in ipairs({{0x5417,'init_enter'},{0x5448,'init_return'},{0x53f0,'line_or_end'},{0x5409,'glyph_queue'},{0x5393,'reader_byte'}}) do
 emu.addMemoryCallback(function(address,value)
  if frame>=700 then
   local ptr=read(6)+256*read(7)+emu.getState()['cpu.y']
   log(pair[2],ptr,read(ptr))
  end
 end,emu.callbackType.exec,pair[1],pair[1],emu.cpuType.nes,emu.memType.nesPrgRom)
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then
  f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0)
 end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=start>=0 and frame>=start and frame<start+8,select=false,a=false,b=false,up=false,down=false,left=false,right=false},0)
end,emu.eventType.inputPolled)
