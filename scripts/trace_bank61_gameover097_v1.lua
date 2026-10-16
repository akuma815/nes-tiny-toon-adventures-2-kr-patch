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
 local near=false
 for _,e in ipairs(sequence) do if frame>=e.frame-10 and frame<=e.frame+80 then near=true end end
 if frame%30==0 or frame==limit or near and frame%3==0 or frame>=4900 and frame<=5400 and frame%3==0 then snapshot() end
 if frame==limit then assert(seeded);seedlog:close();log:close();save('trace_complete.txt',tostring(frame));emu.stop(0) end
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

local cons=assert(io.open(out..'/gameover_consumers.csv','wb'));cons:write('frame,kind,pc,address,value,root,phase,PRG_relative,scanline,dot,cycles\n')
local function gc(kind,a,v)
 if frame<4000 then return end
 local st=emu.getState();local m=emu.convertAddress(st['cpu.pc'],emu.memType.nesMemory);cons:write(string.format('%d,%s,%04X,%04X,%02X,%02X,%02X,%05X,%s,%s,%s\n',frame,kind,st['cpu.pc'],a,v,emu.read(0x18,emu.memType.nesDebug),emu.read(0x54,emu.memType.nesDebug),m.address,tostring(st['ppu.scanline']),tostring(st['ppu.cycle']),tostring(st['cpu.cycleCount'])));cons:flush()
end
for _,pc in ipairs({0xf6ed,0xf6fc,0x93ac,0x9412,0xf723,0xf78d}) do emu.addMemoryCallback(function(a,v)gc('exec',a,v)end,emu.callbackType.exec,pc,pc,emu.cpuType.nes,emu.memType.nesMemory)end
for _,a in ipairs({0x34,0x35}) do emu.addMemoryCallback(function(a,v)gc('write',a,v)end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)end
emu.addMemoryCallback(function(a,v)gc('read',a,v)end,emu.callbackType.read,0x94d8,0x94ed,emu.cpuType.nes,emu.memType.nesMemory)
local flog=assert(io.open(out..'/gameover_top_fonts.csv','wb'));flog:write('frame,pc,font0,font1,font2,font3,scanline,dot,cycles,tag\n')
emu.addMemoryCallback(function(a,v)
 local st=emu.getState();if frame<4800 or frame%30~=0 or st['cpu.x']~=0 or emu.read(0x18,emu.memType.nesDebug)~=4 or emu.read(0x54,emu.memType.nesDebug)~=12 then return end
 local tag=string.format('gameover_top_%05d',frame);local banks={};for a=0,0xc00,0x400 do banks[#banks+1]=emu.convertAddress(a,emu.memType.nesPpuMemory).address end
 dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000);flog:write(string.format('%d,%04X,%05X,%05X,%05X,%05X,%s,%s,%s,%s\n',frame,st['cpu.pc'],banks[1],banks[2],banks[3],banks[4],tostring(st['ppu.scanline']),tostring(st['ppu.cycle']),tostring(st['cpu.cycleCount']),tag));flog:flush()
end,emu.callbackType.exec,0xfd92,0xfd92,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then cons:close();flog:close()end end,emu.eventType.endFrame)

-- Work97 bank61 positive control: flag3E is distinct from POW candidates.
local pose_ids={[0x18]=true,[0x19]=true,[0x3c]=true,[0x3e]=true,[0x7c]=true,[0x9c]=true,[0x9d]=true}
local poses=assert(io.open(out..'/bank61_pose_consumers.csv','wb'));poses:write('frame,kind,observed_pc,PRG_relative,actor,address,art_id,RAM38,CHR1800,root,phase,largeSprites\n')
local function pose(kind,address,art,actor)
 if frame<4000 or not pose_ids[art]then return end
 local s=emu.getState();local m=emu.convertAddress(s['cpu.pc'],emu.memType.nesMemory);local p=emu.convertAddress(0x1800,emu.memType.nesPpuMemory)
 poses:write(string.format('%d,%s,%04X,%05X,%d,%04X,%02X,%02X,%05X,%02X,%02X,%s\n',frame,kind,s['cpu.pc'],m.address,actor,address,art,emu.read(0x38,emu.memType.nesDebug),p.address,emu.read(0x18,emu.memType.nesDebug),emu.read(0x54,emu.memType.nesDebug),tostring(s['ppu.control.largeSprites'])))
end
emu.addMemoryCallback(function(a,v)
 local s=emu.getState();local m=emu.convertAddress(a,emu.memType.nesMemory);if m.address~=0x2d643 then return end
 pose('native9643_exec',a,s['cpu.a'],emu.read(0x05,emu.memType.nesDebug))
end,emu.callbackType.exec,0x9643,0x9643,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)pose('art_RAM_write',a,v,a-0x400)end,emu.callbackType.write,0x400,0x40f,emu.cpuType.nes,emu.memType.nesMemory)
local counts={};local pattern=assert(io.open(out..'/bank61_pattern_reads.csv','wb'));pattern:write('frame,ppu_address,CHR_relative,value,classification,count,first_scanline,last_scanline\n')
emu.addMemoryCallback(function(a,v)
 if frame<4000 then return end
 local m=emu.convertAddress(a,emu.memType.nesPpuMemory);if m.address<0xf400 or m.address>=0xf800 then return end
 local s=emu.getState();local class='other61'
 if m.address>=0xf420 and m.address<0xf440 then class='flag_control'elseif m.address>=0xf4c0 and m.address<0xf500 or m.address>=0xf520 and m.address<0xf600 then class='selected_POW_candidate'end
 local key=string.format('%05d:%04X:%05X',frame,a,m.address);local z=counts[key]
 if z then z.count=z.count+1;z.last=s['ppu.scanline']else counts[key]={frame=frame,a=a,relative=m.address,value=v,class=class,count=1,first=s['ppu.scanline'],last=s['ppu.scanline']}end
end,emu.callbackType.read,0,0x1fff,emu.cpuType.nes,emu.memType.nesPpuMemory)
local top=assert(io.open(out..'/bank61_top_OAM.csv','wb'));top:write('frame,pc,scanline,dot,CHR1800,largeSprites,OAM_index,y,tile,attributes,x,CHR_relative,capture_tag\n');local captured={}
emu.addMemoryCallback(function(a,v)
 if frame<4000 then return end
 local s=emu.getState();if not s['ppu.control.largeSprites']then return end
 for i=0,63 do
  local y=emu.read(i*4,emu.memType.nesSpriteRam);local tile=emu.read(i*4+1,emu.memType.nesSpriteRam)
  if y<239 and tile==0x83 then
   local aa=(tile%2)*0x1000+(tile-tile%2)*16;local m=emu.convertAddress(aa,emu.memType.nesPpuMemory)
   if m.address==0xf420 then
    local tag=''
    if frame%30==0 and not captured[frame]then
     captured[frame]=true;tag=string.format('flag_top_%05d',frame);dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000);dump(tag..'_oam.bin',emu.memType.nesSpriteRam,256)
    end
    top:write(string.format('%d,%04X,%s,%s,%05X,%s,%d,%d,%02X,%02X,%d,%05X,%s\n',frame,s['cpu.pc'],tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),emu.convertAddress(0x1800,emu.memType.nesPpuMemory).address,tostring(s['ppu.control.largeSprites']),i,y,tile,emu.read(i*4+2,emu.memType.nesSpriteRam),emu.read(i*4+3,emu.memType.nesSpriteRam),m.address,tag))
   end
  end
 end
end,emu.callbackType.exec,0xfd9e,0xfd9e,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 if frame==limit then
  local keys={};for key,_ in pairs(counts)do keys[#keys+1]=key end;table.sort(keys)
  for _,key in ipairs(keys)do local z=counts[key];pattern:write(string.format('%d,%04X,%05X,%02X,%s,%d,%s,%s\n',z.frame,z.a,z.relative,z.value,z.class,z.count,tostring(z.first),tostring(z.last)))end
  poses:close();pattern:close();top:close()
 end
end,emu.eventType.endFrame)