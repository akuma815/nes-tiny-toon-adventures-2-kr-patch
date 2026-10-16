-- Controlled seed full-route timing, all RAM seed writes recorded; no ROM/state intervention; not normal gameplay.
local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local seedlog=assert(io.open(out..'/seed_writes.csv','wb'))
seedlog:write('frame,pc,cycles,address,before,value,after\n')
local seedframe=assert(tonumber(os.getenv('TTA2_SEED_FRAME')))
local seeds={}
for item in string.gmatch(assert(os.getenv('TTA2_SEEDS')),'[^;]+') do
 local a,v=string.match(item,'^(%d+),(%d+)$');assert(a);a=tonumber(a);v=tonumber(v)
 assert((a>=0x7d0 and a<=0x7d2 or a==0x7e0 or a>=0x7f2 and a<=0x7f6) and v>=0 and v<=9)
 seeds[#seeds+1]={a=a,v=v}
end
local seeded=false

local limit=tonumber(os.getenv('TTA2_FRAMES')) or 1050
local f=assert(io.open(out..'/irq_phase.csv','wb'))
f:write('frame,kind,pc,address,value,scanline,dot,cycles\n')
local function record(kind,address,value)
 if frame>=900 and frame<=limit then
  local s=emu.getState()
  f:write(string.format('%d,%s,%04X,%04X,%02X,%s,%s,%s\n',frame,kind,s['cpu.pc'],address,value,tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),tostring(s['cpu.cycleCount'])))
 end
end
emu.addMemoryCallback(function(a,v) record('exec',a,v) end,emu.callbackType.exec,0xfb97,0xfb97,emu.cpuType.nes,emu.memType.nesMemory)
for _,a in ipairs({0xa000,0xa008,0xb000,0xb008,0x2000,0x2005,0x2006}) do
 emu.addMemoryCallback(function(p,v) record('write',p,v) end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
local sequence={}
for item in string.gmatch(assert(os.getenv('TTA2_INPUTS')),'[^;]+') do
 local n,d,b=string.match(item,'^(%d+),(%d+),(%a+)$');sequence[#sequence+1]={frame=tonumber(n),duration=tonumber(d),button=b}
end
emu.addMemoryCallback(function(a,v)record('exec',a,v)end,emu.callbackType.exec,0xfb0d,0xfb0d,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if frame==seedframe then
  assert(not seeded);seeded=true
  for _,e in ipairs(seeds) do
   local before=emu.read(e.a,emu.memType.nesDebug);local state=emu.getState()
   emu.write(e.a,e.v,emu.memType.nesDebug)
   local after=emu.read(e.a,emu.memType.nesDebug);assert(after==e.v)
   seedlog:write(string.format('%d,%04X,%s,%04X,%02X,%02X,%02X\n',frame,state['cpu.pc'],tostring(state['cpu.cycleCount']),e.a,before,e.v,after))
  end
 end

 if frame==limit then assert(seeded);seedlog:close();f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
