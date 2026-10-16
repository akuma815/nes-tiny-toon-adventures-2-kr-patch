-- Observe native candidate padding and IRQ temporary C6, without game memory writes.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 5400
local start=tonumber(os.getenv('TTA2_START')) or -1
local f=assert(io.open(out..'/space_and_scratch.csv','wb'))
f:write('frame,kind,pc,address,value,script_id,stream_ptr\n')
local function record(kind,a,v)
 local s=emu.getState()
 f:write(string.format('%d,%s,%04X,%04X,%02X,%02X,%04X\n',frame,kind,s['cpu.pc'],a,v,emu.read(0x6cf,emu.memType.nesDebug),emu.read(0x6cd,emu.memType.nesDebug)+256*emu.read(0x6ce,emu.memType.nesDebug)))
end
for _,kind in ipairs({'read','exec'}) do
 emu.addMemoryCallback(function(a,v) record('padding_'..kind,a,v) end,emu.callbackType[kind],0x1e148,0x1e237,emu.cpuType.nes,emu.memType.nesPrgRom)
end
for _,kind in ipairs({'read','write'}) do
 emu.addMemoryCallback(function(a,v) record('C6_'..kind,a,v) end,emu.callbackType[kind],0xc6,0xc6,emu.cpuType.nes,emu.memType.nesMemory)
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
