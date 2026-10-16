-- Read-only lifecycle, bank return, latch, and IRQ observations.
local out=assert(os.getenv('TTA2_QA_OUT'))
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 5400
local frame=0
local f=assert(io.open(out..'/page_events.csv','wb'))
f:write('frame,kind,pc,address,value,scanline,dot,cycles,sp,C6,id,pointer,bank8000,bankA000,return_bank\n')
local function r(a) return emu.read(a,emu.memType.nesDebug) end
local function log(kind,a,v)
 if frame<900 then return end
 local s=emu.getState();local m=emu.convertAddress(0x8000,emu.memType.nesMemory);local n=emu.convertAddress(0xa000,emu.memType.nesMemory)
 f:write(string.format('%d,%s,%04X,%04X,%02X,%s,%s,%s,%02X,%02X,%02X,%04X,%05X,%05X,%02X\n',frame,kind,s['cpu.pc'],a,v,tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),tostring(s['cpu.cycleCount']),s['cpu.sp'],r(0xc6),r(0x6cf),r(0x6cd)+256*r(0x6ce),m.address,n.address,r(0x2b)))
end
for _,a in ipairs({0x9417,0x9445,0x8e88,0x8ea1,0xfb97}) do
 emu.addMemoryCallback(function(p,v) log('exec',p,v) end,emu.callbackType.exec,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
for _,a in ipairs({0xc6,0x6cf,0xa000,0xa008}) do
 emu.addMemoryCallback(function(p,v) log('write',p,v) end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
