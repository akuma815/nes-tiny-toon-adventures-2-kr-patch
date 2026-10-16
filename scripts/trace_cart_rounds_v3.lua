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

-- Work71 level1/2 axisrotation + clearsegment; nativelevel0 identicalto70V2; first4200 reproduces prior charge policy, then full-charge intercept and per-level interior routing.
local r=function(a)return emu.read(a,emu.memType.nesDebug)end
local function signed(lo,hi)local v=r(lo)+256*r(hi);if v>=32768 then return v-65536 end;return v end
local function xy(i)return r(0x470+i)+240*r(0x480+i),r(0x4a0+i)+256*r(0x4b0+i)end
local function car(i)local t=r(0x420+i);return(t>=0x2d and t<=0x2f)and(r(0x410+i)&1)~=0 and r(0x480+i)<=1 and r(0x4b0+i)<=1 end
local maps={};local pits={}
maps[0]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,17,17,17,17,17,17,17,17,17,17,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,6,7,0,0,0,0,0,0,9,6,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,17,21,7,0,0,0,0,0,0,0,0,9,19,17,24,0,0,0,0,0,0,0,10,0,0,0,0,0,0,16,6,7,0,0,0,0,0,0,0,0,0,0,9,6,26,0,0,0,0,0,27,27,27,0,0,0,0,22,17,21,7,0,0,0,0,0,0,0,0,0,0,0,0,9,19,17,24,0,0,0,0,0,0,0,0,0,0,16,6,7,0,0,0,0,11,13,0,0,0,0,0,0,0,0,9,6,26,0,0,0,0,0,0,0,0,0,0,16,7,0,0,0,0,0,12,14,0,0,0,0,0,0,0,0,0,9,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,15,15,0,0,0,0,0,0,11,13,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,15,15,0,0,0,0,0,0,12,14,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,8,0,0,0,0,0,11,13,0,0,0,0,0,0,0,0,0,10,26,0,0,0,0,0,0,0,0,0,0,16,6,8,0,0,0,0,12,14,0,0,0,0,0,0,0,0,10,6,26,0,0,0,0,0,0,0,0,0,0,23,27,20,8,0,0,0,0,0,0,0,0,0,0,0,0,10,18,27,25,0,0,0,0,0,0,0,0,0,0,0,0,16,6,8,0,0,0,0,0,0,0,0,0,0,10,6,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,27,20,8,0,0,0,0,0,0,0,0,10,18,27,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,6,8,0,0,0,0,0,0,10,6,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,27,27,27,27,27,27,27,27,27,27,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
pits[0]={{112,240,144,272}}
maps[1]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,6,0,0,0,0,0,0,0,0,0,0,22,17,17,17,17,17,17,24,0,0,0,0,0,0,0,0,0,17,21,7,0,0,0,0,0,0,0,0,0,0,16,11,13,0,0,9,6,26,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,22,17,21,12,14,0,0,0,9,19,17,24,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,16,6,7,0,0,0,0,0,0,9,6,26,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,22,17,21,7,0,0,0,0,0,0,0,0,9,19,17,24,0,0,0,0,0,1,1,0,0,0,0,0,0,0,16,6,7,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,1,1,0,0,0,0,0,0,0,16,7,0,0,0,0,0,0,0,0,0,0,0,0,0,19,17,24,0,0,0,1,1,0,0,0,0,0,0,0,16,0,0,0,0,0,10,18,27,27,20,8,0,0,0,9,6,26,0,0,0,1,1,0,0,0,0,0,0,0,16,0,0,0,0,10,6,26,0,0,16,6,8,0,0,0,9,26,0,0,0,1,1,10,0,0,0,0,0,0,16,0,0,0,0,18,27,21,0,0,16,6,7,0,0,0,0,26,0,0,0,1,1,18,0,0,0,0,0,0,16,0,0,0,0,26,0,0,0,0,16,7,0,0,0,0,0,26,0,0,0,1,1,26,0,0,0,0,0,0,16,0,0,0,0,26,0,0,0,0,16,0,0,0,0,0,10,26,0,0,0,27,27,25,0,0,0,0,0,0,16,0,0,0,0,26,0,0,0,0,16,0,0,0,0,10,6,26,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,26,0,0,0,0,16,8,0,0,0,9,6,26,0,0,0,3,0,0,0,0,0,0,0,0,16,0,0,0,0,26,0,0,0,0,16,6,8,0,0,0,9,26,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,26,0,0,0,0,16,6,7,0,0,0,0,26,0,0,0,201,0,0,0,0,0,0,0,0,16,0,0,0,0,19,17,17,17,17,21,7,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,10,26,0,0,0,76,0,0,0,0,0,0,0,0,16,0,0,0,0,1,1,1,1,1,1,0,0,0,0,10,6,26,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,1,1,0,0,1,1,0,0,0,0,18,27,25,0,0,0,208,0,0,0,0,0,0,0,0,16,0,0,0,0,1,1,0,0,1,1,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,8,0,0,0,1,1,0,0,1,1,0,0,0,10,26,0,0,0,0,0,165,0,0,0,0,0,0,0,0,16,6,8,0,0,1,1,0,0,1,1,0,0,10,6,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,27,20,8,0,1,1,0,0,1,1,0,10,18,27,25,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,16,6,8,1,1,0,0,1,1,10,6,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,27,20,1,1,15,15,1,1,18,27,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,1,1,15,15,1,1,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,27,27,27,27,27,27,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
pits[1]={{208,448,240,480}}
maps[2]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,17,17,17,17,17,17,24,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,0,18,0,0,0,0,0,0,0,0,22,17,21,0,0,0,0,0,0,19,17,24,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,16,6,7,0,0,0,0,0,0,9,6,26,0,0,0,0,0,0,0,27,27,25,0,0,0,0,0,0,22,17,21,7,0,0,0,0,0,0,0,0,9,19,17,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,6,7,0,0,0,0,11,13,0,0,0,0,9,6,26,0,0,0,0,0,0,0,0,0,0,0,0,22,17,21,7,0,0,0,0,0,12,14,0,0,0,0,0,9,19,17,24,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,11,13,0,0,15,15,0,0,11,13,0,0,0,0,26,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,12,14,0,0,15,15,0,0,12,14,0,0,0,0,26,0,0,0,0,1,1,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,1,141,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,0,0,0,0,1,1,0,0,0,0,23,27,20,8,0,0,0,0,0,11,13,0,0,0,0,0,10,18,27,25,0,0,0,0,1,1,0,0,0,0,0,0,16,6,8,0,0,0,0,12,14,0,0,0,0,10,6,26,0,0,0,0,0,0,1,1,0,0,0,0,0,0,23,27,20,8,0,0,0,0,0,0,0,0,10,18,27,25,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,16,6,8,0,0,0,0,0,0,10,6,26,0,0,0,0,0,0,0,0,1,221,0,0,0,0,0,0,0,0,23,27,20,0,0,0,0,0,0,18,27,25,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,26,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,23,27,27,27,27,27,27,25,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1}
pits[2]={{208,240,240,272}}
local headings={[1]=6,[2]=2,[4]=0,[8]=4,[5]=7,[6]=1,[9]=5,[10]=3}
local floors={};local target=nil;local lastdirection=1;local waypoint=1
local route0={{240,256},{400,96},{400,400},{80,400},{80,96}}
local function hazard(level,x,y,margin)
 for _,p in ipairs(pits[level]or{})do if x>p[1]-margin and x<p[3]+margin and y>p[2]-margin and y<p[4]+margin then return true end end;return false
end
local function inside(level,px,py)
 if floors[level]then return floors[level]end
 local raw=assert(maps[level]);local queue={math.floor(py/16)*30+math.floor(px/16)};local found={};local n=1
 while n<=#queue do
  local k=queue[n];n=n+1;local x,y=k%30,math.floor(k/30)
  if not found[k]and x>=0 and x<30 and y>=0 and y<32 and raw[k+1]<15 then
   found[k]=true;for _,d in ipairs({{1,0},{-1,0},{0,1},{0,-1}})do local xx,yy=x+d[1],y+d[2];if xx>=0 and xx<30 and yy>=0 and yy<32 then queue[#queue+1]=yy*30+xx end end
  end
 end
 floors[level]=found;return found
end
local function path(level,px,py,tx,ty)
 local floor=inside(level,px,py);local function safe(x,y)return floor[y*30+x]and not hazard(level,x*16+8,y*16+8,16)end
 local sx,sy=math.floor(px/16),math.floor(py/16);local gx,gy=math.floor(tx/16),math.floor(ty/16);local best=math.huge
 if not safe(gx,gy)then for k,_ in pairs(floor)do local x,y=k%30,math.floor(k/30);local d=(x*16+8-tx)^2+(y*16+8-ty)^2;if safe(x,y)and d<best then best=d;gx=x;gy=y end end end
 local sk=sy*30+sx;local goal=gy*30+gx;local queue={sk};local prev={[sk]=-1};local n=1
 while n<=#queue do
  local k=queue[n];n=n+1;if k==goal then break end;local x,y=k%30,math.floor(k/30)
  for _,d in ipairs({{1,0},{-1,0},{0,1},{0,-1}})do local xx,yy=x+d[1],y+d[2];local kk=yy*30+xx;if xx>=0 and xx<30 and yy>=0 and yy<32 and safe(xx,yy)and prev[kk]==nil then prev[kk]=k;queue[#queue+1]=kk end end
 end
 if prev[goal]==nil then return tx,ty,false end
 local reverse={goal};local k=goal;while k~=sk and prev[k]~=-1 do k=prev[k];reverse[#reverse+1]=k end
 local index=math.max(1,#reverse-4)
 if level>=1 then
  local function clearsegment(xx,yy)
   local len=math.sqrt((xx-px)^2+(yy-py)^2);local steps=math.max(1,math.ceil(len/2))
   for i=0,steps do local x=px+(xx-px)*i/steps;local y=py+(yy-py)*i/steps
    for _,d in ipairs({{0,0},{8,0},{-8,0},{0,8},{0,-8}})do
     local cx,cy=math.floor((x+d[1])/16),math.floor((y+d[2])/16)
     if cx<0 or cx>=30 or cy<0 or cy>=32 or not safe(cx,cy)then return false end
    end
   end;return true
  end
  index=math.max(1,#reverse-1)
  for i=math.max(1,#reverse-4),#reverse-1 do local kk=reverse[i];if clearsegment(kk%30*16+8,math.floor(kk/30)*16+8)then index=i;break end end
 end
 k=reverse[index];return k%30*16+8,math.floor(k/30)*16+8,true
end
local log=assert(io.open(out..'/cart_round_policy.csv','wb'));log:write('frame,root,phase,level,life,history,gold,px,py,vx,vy,target,target_type,tx,ty,aimx,aimy,mode,mask,charge,heading,path_found,remaining13,remaining14,remaining15\n')
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 local px,py=xy(0);local vx,vy=signed(0x4c0,0x4d0)/256,signed(0x4e0,0x4f0)/256;local level=r(0x79)
 local tx,ty=-1,-1;local ax,ay=px,py;local mode='base';local found=false;local targettype=-1
 if r(0x18)==4 and r(0x54)==5 and r(0x25)==1 and level<=2 and r(0x480)<=1 and r(0x4b0)<=1 and (frame>=4200 or r(0x400)~=0)then
  if target~=nil and not car(target)then target=nil end
  if target==nil or frame<4200 and frame%120==0 then
   target=nil;local closest=math.huge
   for i=1,15 do if car(i)then local x,y=xy(i);local d=(x-px)^2+(y-py)^2;if d<closest then closest=d;target=i end end end
  end
  if target~=nil then tx,ty=xy(target);targettype=r(0x420+target)end
  if frame<4200 then
   if target==nil then tx,ty=route0[waypoint][1],route0[waypoint][2];if math.abs(px-tx)+math.abs(py-ty)<24 then waypoint=waypoint%#route0+1;tx,ty=route0[waypoint][1],route0[waypoint][2]end end
   ax,ay=tx,ty;mode='reproduce40_24'
  elseif target~=nil then
   local p=assert(pits[level][1]);local hx,hy=(p[1]+p[3])/2,(p[2]+p[4])/2
   local dx,dy=tx-hx,ty-hy;local len=math.sqrt(dx*dx+dy*dy);if len<1 then len=1 end
   local ex,ey=signed(0x4c0+target,0x4d0+target)/256,signed(0x4e0+target,0x4f0+target)/256
   local sx,sy=tx+ex*12+dx/len*38,ty+ey*12+dy/len*38
   local dist=math.sqrt((px-tx)^2+(py-ty)^2);local behind=((px-tx)*dx+(py-ty)*dy)>0
   if dist<56 and behind then ax,ay=tx+ex*6,ty+ey*6;mode='push'
   else ax,ay,found=path(level,px,py,sx,sy);mode='intercept'end
   if hazard(level,px+vx*12,py+vy*12,16)then
    local dx,dy=px-hx,py-hy;local len=math.sqrt(dx*dx+dy*dy);if len<1 then dx=1;len=1 end
    ax,ay=px+dx/len*48,py+dy/len*48;mode='pit_avoid';input.b=true
   end
  else ax,ay=px,py;mode='wait_clear'end
  local dx,dy=ax-px,ay-py
  if frame>=4200 then dx=dx*0.08-vx*0.60;dy=dy*0.08-vy*0.60 end
  local deadzone=frame<4200 and 6 or 0.20;local direction=0;if dx>deadzone then direction=direction|1 elseif dx< -deadzone then direction=direction|2 end;if dy>deadzone then direction=direction|4 elseif dy< -deadzone then direction=direction|8 end
  if direction==0 then direction=lastdirection else lastdirection=direction end
  if level>=1 then
   local rotated=0;if direction&1~=0 then rotated=rotated|4 end;if direction&2~=0 then rotated=rotated|8 end;if direction&4~=0 then rotated=rotated|1 end;if direction&8~=0 then rotated=rotated|2 end;direction=rotated
  end
  input.right=(direction&1)~=0;input.left=(direction&2)~=0;input.down=(direction&4)~=0;input.up=(direction&8)~=0
  if frame<4200 then input.b=false;input.a=frame%64<40
  else input.a=frame%48<40;if mode~='push'and vx*vx+vy*vy>6.25 then input.b=true end;if mode=='pit_avoid'then input.a=false end end
 elseif r(0x18)==4 and r(0x25)==1 and frame>=4200 then input.a=frame%120<8;mode='native_transition'end
 local mask=0;for key,bit in pairs({a=128,b=64,select=32,start=16,up=8,down=4,left=2,right=1})do if input[key]then mask=mask|bit end end;emu.setInput(input,0)
 log:write(string.format('%d,%02X,%02X,%d,%02X,%02X,%02X,%d,%d,%.4f,%.4f,%d,%d,%d,%d,%.4f,%.4f,%s,%02X,%d,%d,%s,%02X,%02X,%02X\n',frame,r(0x18),r(0x54),level,r(0x7c0),r(0x7e1),r(0x7e0),px,py,vx,vy,target or -1,targettype,tx,ty,ax,ay,mode,mask,r(0xa9)+256*r(0xaa),r(0x510),tostring(found),r(0x42d),r(0x42e),r(0x42f)))
end,emu.eventType.inputPolled)
emu.addEventCallback(function()if frame%30==0 then log:flush()end;if frame==limit then log:close()end end,emu.eventType.endFrame)

-- Work66 native tile-query return observation and actor lifecycle, read-only.
local pits=assert(io.open(out..'/cart_tile_queries.csv','wb'));pits:write('frame,pc,PRG_relative,course,level,x_page,x_low,y_page,y_low,class,actor_state\n')
emu.addMemoryCallback(function(a,v)
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.address~=0x32274 or r(0x18)~=4 or r(0x25)~=1 then return end
 pits:write(string.format('%d,%04X,%05X,%02X,%02X,%d,%d,%d,%d,%d,%d\n',frame,a,m.address,r(0x25),r(0x79),r(0x6ae),r(0x6ad),r(0x6ac),r(0x6ab),r(0x10),r(0x430)))
end,emu.callbackType.exec,0xa274,0xa274,emu.cpuType.nes,emu.memType.nesMemory)
local actors=assert(io.open(out..'/cart_actors.csv','wb'));actors:write('frame,index,id,flags,type,state,x,y,vx,vy,level,v071B,v0724\n')
emu.addEventCallback(function()
 if frame%30==0 and r(0x18)==4 and r(0x25)==1 then
  for i=0,15 do
   local x,y=xy(i)
   actors:write(string.format('%d,%d,%02X,%02X,%02X,%02X,%d,%d,%d,%d,%d,%d,%d\n',frame,i,r(0x400+i),r(0x410+i),r(0x420+i),r(0x430+i),x,y,signed(0x4c0+i,0x4d0+i),signed(0x4e0+i,0x4f0+i),r(0x79),r(0x71b),r(0x724)))
  end
  pits:flush();actors:flush()
 end
 if frame==limit then pits:close();actors:close()end
end,emu.eventType.endFrame)
