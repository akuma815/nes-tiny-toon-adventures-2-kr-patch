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

-- Work52: exact minimal initialization diagnosis, optional; no PC/ROM/state loads.
local seedframe=tonumber(os.getenv('TTA2_ROOT9_FRAME'))
local seeded=false
local seedlog=assert(io.open(out..'/root9_seed.csv','wb'))
seedlog:write('frame,pc,cycles,address,before,value,after\n')
emu.addEventCallback(function()
 if seedframe and frame==seedframe then
  assert(not seeded);seeded=true
  local function r(a)return emu.read(a,emu.memType.nesDebug)end
  assert(r(0x18)==8 and r(0x19)==1 and r(0x6de)==2)
  for _,a in ipairs({0x68,0x69,0x6a,0x6b,0x6c,0x6d,0xfc,0xfd})do assert(r(a)==0)end
  assert(r(0xff)%4<2) -- F886 prerequisites already satisfied by native home.
  local before={};for a=0,0x7ff do before[a]=r(a)end
  for _,w in ipairs({{0x6de,0},{0x19,0},{0x18,9}})do
   local s=emu.getState();local b=r(w[1]);emu.write(w[1],w[2],emu.memType.nesDebug)
   assert(r(w[1])==w[2]);seedlog:write(string.format('%d,%04X,%s,%04X,%02X,%02X,%02X\n',frame,s['cpu.pc'],tostring(s['cpu.cycleCount']),w[1],b,w[2],r(w[1])))
  end
  for a=0,0x7ff do if a~=0x6de and a~=0x19 and a~=0x18 then assert(before[a]==r(a))end end
  seedlog:flush()
 end
 if frame==limit then if seedframe then assert(seeded)end;seedlog:close()end
end,emu.eventType.endFrame)
local fonts=assert(io.open(out..'/candidate_font_writes.csv','wb'))
fonts:write('frame,root,phase,subphase,pc,PRG_relative,address,value\n')
for _,addr in ipairs({0xa000,0xa008,0xb000,0xb008,0xc000,0xc008,0xd000,0xd008})do
 emu.addMemoryCallback(function(a,v)
  if v>=116 and v<=121 or emu.read(0x18,emu.memType.nesDebug)==9 then
   local s=emu.getState();local p=emu.convertAddress(s['cpu.pc'],emu.memType.nesMemory)
   fonts:write(string.format('%d,%02X,%02X,%02X,%04X,%05X,%04X,%02X\n',frame,emu.read(0x18,emu.memType.nesDebug),emu.read(0x54,emu.memType.nesDebug),emu.read(0x6de,emu.memType.nesDebug),s['cpu.pc'],p.address,a,v))
  end
 end,emu.callbackType.write,addr,addr,emu.cpuType.nes,emu.memType.nesMemory)
end
local roots=assert(io.open(out..'/root_transitions.csv','wb'));roots:write('frame,address,value,pc,PRG_relative\n')
for _,addr in ipairs({0x18,0x19,0x6de,0x7df})do
 emu.addMemoryCallback(function(a,v)local s=emu.getState();local p=emu.convertAddress(s['cpu.pc'],emu.memType.nesMemory);roots:write(string.format('%d,%04X,%02X,%04X,%05X\n',frame,a,v,s['cpu.pc'],p.address))end,emu.callbackType.write,addr,addr,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then fonts:close();roots:close()end end,emu.eventType.endFrame)
