-- Bounded live page timings, counters and exact mapper/PPU port writes. No ROM edits.
local out=assert(os.getenv('TTA2_QA_OUT'));local limit=tonumber(os.getenv('TTA2_FRAMES'));local frame=0
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function file(n,h)local f=assert(io.open(out..'/'..n,'wb'));f:write(h..'\n');return f end
local page=file('page_cycles.csv','frame,kind,pc,PRG_relative,cycle,id,phase,RAM1B,RAM22,headfont,lowerfont,sp,a,x,y,ps,scanline,dot')
local irq=file('port_writes.csv','frame,pc,cycle,address,value,scanline,dot')
local snap=file('frame_counters.csv','frame,cycle,RAM1B,RAM22,root,phase,ride,font')
local seedlog=file('seed_writes.csv','frame,pc,cycles,address,before,value,after')
local count=0;local pending=false
local function record(kind,a)
 local s=emu.getState();local m=emu.convertAddress(a,emu.memType.nesMemory)
 page:write(string.format('%d,%s,%04X,%05X,%s,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%s,%s\n',frame,kind,a,m.address,tostring(s['cpu.cycleCount']),r(0x6cf),r(0x6df),r(0x1b),r(0x22),r(0x34),r(0x6f3),s['cpu.sp'],s['cpu.a'],s['cpu.x'],s['cpu.y'],s['cpu.ps'],tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
end
emu.addMemoryCallback(function(a,v)
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.address~=0x25417 then return end
 assert(not pending);pending=true;count=count+1;record('entry',a)
end,emu.callbackType.exec,0x9417,0x9417,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.address==0x55f9 and pending then record('helper',a)end
end,emu.callbackType.exec,0x95f9,0x95f9,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.address~=0x25445 then return end
 assert(pending);record('before_rts',a);pending=false
end,emu.callbackType.exec,0x9445,0x9445,emu.cpuType.nes,emu.memType.nesMemory)
for _,a in ipairs({0xa000,0xa008,0xb000,0xb008,0xc000,0xc008,0xd000,0xd008,0x2000,0x2005,0x2006})do
 emu.addMemoryCallback(function(p,v)
  local s=emu.getState();irq:write(string.format('%d,%04X,%s,%04X,%02X,%s,%s\n',frame,s['cpu.pc'],tostring(s['cpu.cycleCount']),p,v,tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
 end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
local sequence={}
for item in string.gmatch(assert(os.getenv('TTA2_INPUTS')),'[^;]+')do local n,d,b=string.match(item,'^(%d+),(%d+),(%a+)$');sequence[#sequence+1]={frame=tonumber(n),duration=tonumber(d),button=b}end
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
local seedframe=tonumber(os.getenv('TTA2_SEED_FRAME'));local seeds={};local seeded=false
for item in string.gmatch(assert(os.getenv('TTA2_SEEDS')),'[^;]+')do
 local a,v=string.match(item,'^(%d+),(%d+)$');a=tonumber(a);v=tonumber(v);assert(a>=0x7d0 and a<=0x7d2 and v>=0 and v<=9);seeds[#seeds+1]={a=a,v=v}
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==seedframe then
  assert(not seeded);seeded=true
  for _,e in ipairs(seeds)do
   local before=r(e.a);local s=emu.getState();emu.write(e.a,e.v,emu.memType.nesDebug);assert(r(e.a)==e.v)
   seedlog:write(string.format('%d,%04X,%s,%04X,%02X,%02X,%02X\n',frame,s['cpu.pc'],tostring(s['cpu.cycleCount']),e.a,before,e.v,r(e.a)))
  end
 end
 local s=emu.getState();snap:write(string.format('%d,%s,%02X,%02X,%02X,%02X,%02X,%02X\n',frame,tostring(s['cpu.cycleCount']),r(0x1b),r(0x22),r(0x18),r(0x54),r(0x25),r(0x6f3)))
 if frame==limit then
  assert(seeded and not pending and count>0);page:close();irq:close();snap:close();seedlog:close()
  local f=assert(io.open(out..'/trace_complete.txt','wb'));f:write(tostring(frame));f:close();emu.stop(0)
 end
end,emu.eventType.endFrame)
