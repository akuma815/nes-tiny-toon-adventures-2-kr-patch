-- Read-only v4 ride/gate capture; corrected variable addresses/names. Full raw RAM remains authoritative; v3 evidence retained.
local out=assert(os.getenv('TTA2_QA_OUT'))
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 5400
local start=tonumber(os.getenv('TTA2_START')) or -1
local frame=0
local function save(name,data)
 local f=assert(io.open(out..'/'..name,'wb'));f:write(data);f:close()
end
local function dump(name,kind,size)
 local b={};for i=0,size-1 do b[#b+1]=string.char(emu.read(i,kind)) end
 save(name,table.concat(b))
end
local function snapshot()
 local tag=string.format('frame_%05d',frame)
 save(tag..'.png',emu.takeScreenshot())
 dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000)
 dump(tag..'_ram.bin',emu.memType.nesDebug,0x800)
 dump(tag..'_oam.bin',emu.memType.nesSpriteRam,256)
 local rows={};for k,v in pairs(emu.getState()) do rows[#rows+1]=tostring(k)..'='..tostring(v) end
 table.sort(rows);save(tag..'_state.txt',table.concat(rows,'\n'))
 local maps={'kind,cpu_or_ppu_address,relative_offset,mem_type'}
 for a=0,0x1fff,0x400 do
  local m=emu.convertAddress(a,emu.memType.nesPpuMemory)
  maps[#maps+1]=string.format('chr,%04X,%05X,%s',a,m.address,tostring(m.memType))
 end
 for a=0x8000,0xffff,0x2000 do
  local m=emu.convertAddress(a,emu.memType.nesMemory)
  maps[#maps+1]=string.format('prg,%04X,%05X,%s',a,m.address,tostring(m.memType))
 end
 save(tag..'_mapping.csv',table.concat(maps,'\n'))
end

local sequence={}
for item in string.gmatch(assert(os.getenv('TTA2_INPUTS')),'[^;]+') do
 local n,d,button=string.match(item,'^(%d+),(%d+),(%a+)$');assert(n)
 sequence[#sequence+1]={frame=tonumber(n),duration=tonumber(d),button=button}
end
local log=assert(io.open(out..'/menu_events.csv','wb'))
log:write('frame,kind,address,value,id,pointer,profile,font,return_bank,sp,pc,phase,ride,head_font,active_font,gold_tickets,points_low,normal_ticket0,normal_ticket1,normal_ticket2,cpu_a,caller\n')
local last={}
local function record(kind,a,v)
 if kind=='write' and last[a]==v and a~=0x6f3 then return end
 last[a]=v
 local function r(x)return emu.read(x,emu.memType.nesDebug)end
 local s=emu.getState()
 log:write(string.format('%d,%s,%04X,%02X,%02X,%04X,%02X,%02X,%02X,%02X,%04X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%04X\n',frame,kind,a,v,r(0x6cf),r(0x6cd)+r(0x6ce)*256,r(0x6ea),r(0xc6),r(0x2b),s['cpu.sp'],s['cpu.pc'],r(0x6df),r(0x25),r(0x34),r(0x6f3),r(0x7e0),r(0x7f2),r(0x7d0),r(0x7d1),r(0x7d2),s['cpu.a'],r(0x100+((s['cpu.sp']+1)%256))+256*r(0x100+((s['cpu.sp']+2)%256))))
end
for _,a in ipairs({0x9417,0x9445}) do emu.addMemoryCallback(function(p,v)record('exec',p,v)end,emu.callbackType.exec,a,a,emu.cpuType.nes,emu.memType.nesMemory) end
for _,a in ipairs({0x6cf,0x6ea,0xc6,0x6f3,0x34,0x25,0x6df}) do emu.addMemoryCallback(function(p,v)record('write',p,v)end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory) end
emu.addMemoryCallback(function(a,v)record('read',a,v)end,emu.callbackType.read,0x6f3,0x6f3,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 frame=frame+1
 local near=false
 for _,e in ipairs(sequence) do if frame>=e.frame-10 and frame<=e.frame+80 then near=true end end
 if frame%30==0 or frame==limit or near and frame<2800 and frame%3==0 then snapshot() end
 if frame==limit then log:close();save('trace_complete.txt',tostring(frame));emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence) do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)

-- Read-only world dispatcher/state telemetry. No RAM/ROM/state interventions.
local world=assert(io.open(out..'/world_phase.csv','wb'));world:write('frame,root,phase,ride,pause,life,history,gold,normal0,normal1,normal2,headfont,lowerfont,subphase,pc\n')
emu.addEventCallback(function()
 if frame%30==0 then
  local function r(a)return emu.read(a,emu.memType.nesDebug)end
  local st=emu.getState();world:write(string.format('%d,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%04X\n',frame,r(0x18),r(0x54),r(0x25),r(0x55),r(0x7c0),r(0x7e1),r(0x7e0),r(0x7d0),r(0x7d1),r(0x7d2),r(0x34),r(0x6f3),r(0x6de),st['cpu.pc']));world:flush()
 end
 if frame==limit then world:close()end
end,emu.eventType.endFrame)


local ntlog=assert(io.open(out..'/native_NT_calls.csv','wb'));ntlog:write('frame,root,ride,selector,head_font,pc,PRG_relative,CHR0_relative\n')
emu.addMemoryCallback(function(a,v)
 local st=emu.getState();local m=emu.convertAddress(a,emu.memType.nesMemory);if m.address~=0x4025 and m.address~=0x24025 then return end
 local q=emu.convertAddress(0,emu.memType.nesPpuMemory);ntlog:write(string.format('%d,%02X,%02X,%02X,%02X,%04X,%05X,%05X\n',frame,emu.read(0x18,emu.memType.nesDebug),emu.read(0x25,emu.memType.nesDebug),st['cpu.x'],emu.read(0x34,emu.memType.nesDebug),st['cpu.pc'],m.address,q.address));ntlog:flush()
end,emu.callbackType.exec,0x8025,0x8025,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then ntlog:close()end end,emu.eventType.endFrame)

-- Capture actual mid-frame train-enginefont selection andscroll consumer.
local engine=assert(io.open(out..'/train_engine_irq.csv','wb'))
engine:write('frame,PC,scanline,dot,cycle,root,phase,ride,scroll_control,scroll_y,prg_relative,chr0_relative,chr800_relative\n')
emu.addMemoryCallback(function(a,v)
 local function r(x)return emu.read(x,emu.memType.nesDebug)end
 local st=emu.getState();local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.address~=0x3fc1c and m.address~=0x1fc1c then return end
 local q=emu.convertAddress(0,emu.memType.nesPpuMemory);local h=emu.convertAddress(0x800,emu.memType.nesPpuMemory)
 engine:write(string.format('%d,%04X,%d,%d,%d,%02X,%02X,%02X,%02X,%02X,%05X,%05X,%05X\n',frame,st['cpu.pc'],st['ppu.scanline'],st['ppu.cycle'],st['cpu.cycleCount'],r(0x18),r(0x54),r(0x25),r(0x60c),r(0x60f),m.address,q.address,h.address));engine:flush()
 if frame%30==0 then
  local tag=string.format('engine_%05d',frame)
  dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000)
  dump(tag..'_ram.bin',emu.memType.nesDebug,0x800)
  local rows={};for k,v in pairs(st)do rows[#rows+1]=tostring(k)..'='..tostring(v)end
  table.sort(rows);save(tag..'_state.txt',table.concat(rows,'\n'))
 end
end,emu.callbackType.exec,0xfc1c,0xfc1c,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then engine:close()end end,emu.eventType.endFrame)

-- Explicit repeatedhealthdiagnostic, onlynative root4/phase5/course2/max3.
local life=assert(io.open(out..'/life_seed_writes.csv','wb'))
life:write('frame,pc,cycles,address,before,value,after,written,root,phase,ride,pause\n')
local first=assert(tonumber(os.getenv('TTA2_LIFE_START')));local final=assert(tonumber(os.getenv('TTA2_LIFE_END')));local period=assert(tonumber(os.getenv('TTA2_LIFE_PERIOD')))
local lastlife=-1
emu.addEventCallback(function()
 if frame<first or frame>final or (frame-first)%period~=0 or lastlife==frame then return end
 lastlife=frame;local function r(a)return emu.read(a,emu.memType.nesDebug)end
 local st=emu.getState();local root,phase,ride,pause=r(0x18),r(0x54),r(0x25),r(0x55)
 local before=r(0x7c0);local written=0
 if root==4 and phase==5 and ride==2 and pause==0 then
  assert(before<=3);local ram={};for a=0,0x7ff do ram[a]=r(a)end
  emu.write(0x7c0,3,emu.memType.nesDebug);assert(r(0x7c0)==3)
  for a=0,0x7ff do if a~=0x7c0 then assert(r(a)==ram[a])end end
  written=1
 end
 life:write(string.format('%d,%04X,%s,07C0,%02X,03,%02X,%d,%02X,%02X,%02X,%02X\n',frame,st['cpu.pc'],tostring(st['cpu.cycleCount']),before,r(0x7c0),written,root,phase,ride,pause));life:flush()
end,emu.eventType.inputPolled)
emu.addEventCallback(function()if frame==limit then life:close()end end,emu.eventType.endFrame)
