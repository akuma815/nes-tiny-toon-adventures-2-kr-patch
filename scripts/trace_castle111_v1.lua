-- Controlled RAM seed branch QA; ROM never written. Every seed/before/after recorded; not normal gameplay.
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
local injected=false
local injectionFrame=-1
local inj=assert(io.open(out..'/castle111_injection.csv','wb'))
inj:write('frame,root,ride,phase,address,before,value,after\n')
local native=assert(io.open(out..'/castle111_native.csv','wb'))
native:write('frame,kind,pc,PRG_relative,root,ride,phase,room,waypoint,head_font,body_font,cpu_x\n')
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function nativeRecord(kind,a,m)
 local st=emu.getState()
 native:write(string.format('%d,%s,%04X,%05X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X\n',frame,kind,a,m.address,r(0x18),r(0x25),r(0x54),r(0x79),r(0xa5),r(0x34),r(0x35),st['cpu.x']));native:flush()
end
for _,a in ipairs({0xf5f8,0x969c,0x96ed,0xd347,0xd36e,0xd373,0x8025})do
 emu.addMemoryCallback(function(addr,value)
  local m=emu.convertAddress(addr,emu.memType.nesMemory)
  local base=addr>=0xc000 and (addr-0xc000+0x1c000)or(addr==0x8025 and 0x4025 or addr-0x8000)
  if m.address~=base and m.address~=base+0x20000 then return end
  nativeRecord(addr==0x8025 and 'NT_entry'or'native_entry',addr,m)
 end,emu.callbackType.exec,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
local fetch={}
emu.addMemoryCallback(function(a,v)
 if not injected or(frame~=injectionFrame+90 and frame~=injectionFrame+120)then return end
 local st=emu.getState();local m=emu.convertAddress(a,emu.memType.nesPpuMemory)
 local key=string.format('%d,%s,%04X,%05X',frame+1,tostring(st['ppu.scanline']),math.floor(a/16)*16,math.floor(m.address/16)*16)
 fetch[key]=(fetch[key]or 0)+1
end,emu.callbackType.read,0,0x1fff,emu.cpuType.nes,emu.memType.nesPpuMemory)
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
 if frame==seedframe then
  assert(not seeded);seeded=true
  for _,e in ipairs(seeds) do
   local before=emu.read(e.a,emu.memType.nesDebug);local state=emu.getState()
   emu.write(e.a,e.v,emu.memType.nesDebug)
   local after=emu.read(e.a,emu.memType.nesDebug);assert(after==e.v)
   seedlog:write(string.format('%d,%04X,%s,%04X,%02X,%02X,%02X\n',frame,state['cpu.pc'],tostring(state['cpu.cycleCount']),e.a,before,e.v,after))
  end
 end
 if not injected and frame>=4000 and r(0x18)==4 and r(0x25)==4 and r(0x54)==5 then
  assert(r(0x79)==0);injected=true;injectionFrame=frame
  for _,w in ipairs({{0xa5,35},{0x54,7}})do
   local before=r(w[1]);emu.write(w[1],w[2],emu.memType.nesDebug);assert(r(w[1])==w[2])
   inj:write(string.format('%d,04,04,05,%04X,%02X,%02X,%02X\n',frame,w[1],before,w[2],r(w[1])));inj:flush()
  end
 end
 local near=false
 for _,e in ipairs(sequence) do if frame>=e.frame-10 and frame<=e.frame+80 then near=true end end
 if injected and frame<=injectionFrame+150 and frame%3==0 or frame%30==0 or frame==limit or near and frame%3==0 then snapshot() end
 if frame==limit then assert(seeded and injected);seedlog:close();log:close();inj:close();native:close()
  local lines={};for key,count in pairs(fetch)do lines[#lines+1]=key..','..count end;table.sort(lines);table.insert(lines,1,'snapshot_frame,scanline,ppu_tile_base,CHR_relative_tile_base,read_count')
  save('castle111_render_fetch.csv',table.concat(lines,'\n')..'\n');save('trace_complete.txt',tostring(frame));emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence) do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
