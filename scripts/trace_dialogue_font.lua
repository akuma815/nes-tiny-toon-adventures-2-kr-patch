-- Read-only mapping/renderer diagnosis around first two intro paragraphs.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 1500
local f=assert(io.open(out..'/font_registers.csv','wb'))
f:write('frame,scanline,pc,register,value,script_id,ptr_low,ptr_high,shadow0404,shadow0405\n')
for _,a in ipairs({0xA000,0xA008}) do
 emu.addMemoryCallback(function(address,value)
  if frame>=850 and frame<1500 then
   local s=emu.getState()
   f:write(string.format('%d,%s,%04X,%04X,%02X,%02X,%02X,%02X,%02X,%02X\n',frame,tostring(s['ppu.scanline']),s['cpu.pc'],address,value,emu.read(0x6cf,emu.memType.nesDebug),emu.read(0x6cd,emu.memType.nesDebug),emu.read(0x6ce,emu.memType.nesDebug),emu.read(0x404,emu.memType.nesDebug),emu.read(0x405,emu.memType.nesDebug)))
  end
 end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
