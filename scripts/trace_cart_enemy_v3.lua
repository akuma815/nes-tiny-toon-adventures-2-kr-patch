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

-- Work65 controller-only charge40/release24, Bdisabled, retarget120; adaptive pursuit; no emu.write/load/reset/PC edit.
local policy=assert(io.open(out..'/cart_policy.csv','wb'));policy:write('frame,root,phase,course,life,history,gold,player_id,player_x,player_y,heading,target_index,target_type,target_x,target_y,distance,desired_heading,mask,charge,velocity_x,velocity_y\n')
local target=nil;local lastdirection=1;local waypoint=1
local route={{240,256},{400,96},{400,400},{80,400},{80,96}}
local headings={[1]=6,[2]=2,[4]=0,[8]=4,[5]=7,[6]=1,[9]=5,[10]=3}
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function signed(lo,hi)local v=r(lo)+256*r(hi);if v>=0x8000 then v=v-0x10000 end;return v end
local function xy(i)return r(0x470+i)+240*r(0x480+i),r(0x4a0+i)+256*r(0x4b0+i)end
local function car(i)return(r(0x420+i)==0x2e or r(0x420+i)==0x2f)and(r(0x410+i)&1)~=0 and r(0x480+i)<=1 and r(0x4b0+i)<=1 end
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 local px,py=xy(0);local tx,ty=-1,-1;local dist=-1;local desired=-1;local mask=0;local targettype=-1
 if r(0x18)==4 and r(0x54)==5 and r(0x25)==1 and r(0x55)==0 and r(0x400)~=0 and r(0x480)<=1 and r(0x4b0)<=1 then
  if target~=nil and not car(target)then target=nil end
  if target==nil or frame%120==0 then
   target=nil;local closest=math.huge
   for i=1,15 do if car(i)then local x,y=xy(i);local d=(x-px)^2+(y-py)^2;if d<closest then closest=d;target=i end end end
  end
  if target~=nil then tx,ty=xy(target);targettype=r(0x420+target)
  else tx,ty=route[waypoint][1],route[waypoint][2];if math.abs(px-tx)+math.abs(py-ty)<24 then waypoint=waypoint%#route+1;tx,ty=route[waypoint][1],route[waypoint][2]end end
  local dx,dy=tx-px,ty-py;dist=math.sqrt(dx*dx+dy*dy)
  local direction=0;if dx>6 then direction=direction|1 elseif dx< -6 then direction=direction|2 end;if dy>6 then direction=direction|4 elseif dy< -6 then direction=direction|8 end
  if direction==0 then direction=lastdirection else lastdirection=direction end
  desired=assert(headings[direction]);local error=(desired-r(0x510))&7;error=math.min(error,8-error)
  input.right=(direction&1)~=0;input.left=(direction&2)~=0;input.down=(direction&4)~=0;input.up=(direction&8)~=0
  input.b=false;input.a=frame%64<40
 elseif r(0x18)==4 and r(0x25)==1 and r(0x54)>=0x20 and r(0x54)<=0x24 then
  input.a=frame%120<8
 end
 for key,bit in pairs({a=128,b=64,select=32,start=16,up=8,down=4,left=2,right=1})do if input[key]then mask=mask|bit end end
 emu.setInput(input,0)
 policy:write(string.format('%d,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%d,%d,%d,%d,%d,%d,%d,%.3f,%d,%02X,%d,%d,%d\n',frame,r(0x18),r(0x54),r(0x25),r(0x7c0),r(0x7e1),r(0x7e0),r(0x400),px,py,r(0x510),target or -1,targettype,tx,ty,dist,desired,mask,r(0xa9)+256*r(0xaa),signed(0x4c0,0x4d0),signed(0x4e0,0x4f0)))
end,emu.eventType.inputPolled)
emu.addEventCallback(function()if frame%30==0 then policy:flush()end;if frame==limit then policy:close()end end,emu.eventType.endFrame)

-- Work68 read-only enemy lifecycle write consumers; original charge policy remains identical.
local enemy=assert(io.open(out..'/enemy_writes.csv','wb'));enemy:write('frame,address,old,value,type,state,id,cpu_pc,next_PRG,cpu_x,cpu_y,root,phase,level\n')
local enemy_last={}
for _,a in ipairs({0x40e,0x40f,0x42e,0x42f,0x43e,0x43f})do
 emu.addMemoryCallback(function(addr,v)
  if r(0x18)~=4 or r(0x25)~=1 then return end
  if enemy_last[addr]==v then return end;enemy_last[addr]=v
  local i=addr&15;local st=emu.getState();local m=emu.convertAddress(st['cpu.pc'],emu.memType.nesMemory)
  enemy:write(string.format('%d,%04X,%02X,%02X,%02X,%02X,%02X,%04X,%05X,%02X,%02X,%02X,%02X,%02X\n',frame,addr,r(addr),v,r(0x420+i),r(0x430+i),r(0x400+i),st['cpu.pc'],m.address,st['cpu.x'],st['cpu.y'],r(0x18),r(0x54),r(0x79)))
  if addr>=0x420 then dump(string.format('enemy_%05d_%04X_%02X_ram.bin',frame,addr,v),emu.memType.nesDebug,0x800)end
 end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame%30==0 then enemy:flush()end;if frame==limit then enemy:close()end end,emu.eventType.endFrame)

-- Work68 actual type-read consumers, aggregated by physical nextPC/address/value.
local reads={};local readlog=assert(io.open(out..'/enemy_type_consumers.csv','wb'));readlog:write('first_frame,address,value,next_pc,next_PRG,x,y,count\n')
emu.addMemoryCallback(function(a,v)
 if r(0x18)~=4 or r(0x25)~=1 or r(0x54)~=5 then return end
 local st=emu.getState();local m=emu.convertAddress(st['cpu.pc'],emu.memType.nesMemory)
 local key=string.format('%04X:%05X:%02X',a,m.address,v)
 if reads[key]then reads[key].count=reads[key].count+1
 else reads[key]={frame=frame,address=a,value=v,pc=st['cpu.pc'],prg=m.address,x=st['cpu.x'],y=st['cpu.y'],count=1}end
end,emu.callbackType.read,0x420,0x42f,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 if frame==limit then
  local keys={};for k,_ in pairs(reads)do keys[#keys+1]=k end;table.sort(keys)
  for _,k in ipairs(keys)do local t=reads[k];readlog:write(string.format('%d,%04X,%02X,%04X,%05X,%02X,%02X,%d\n',t.frame,t.address,t.value,t.pc,t.prg,t.x,t.y,t.count))end
  readlog:close()
 end
end,emu.eventType.endFrame)
