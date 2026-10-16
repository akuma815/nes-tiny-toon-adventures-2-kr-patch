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
-- Physical PRG data reads in registered main/macro body regions only.
-- Does not change CPU registers, input timing, ROM, or return read values.
local textlog=assert(io.open(out..'/prg_text_reads.csv','wb'))
textlog:write('frame,pc,cycles,cpu_address,PRG_relative_offset,value,native_id,pointer,active_font\n')
emu.addMemoryCallback(function(a,v)
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.memType~=emu.memType.nesPrgRom then return end
 local f=m.address+0x10
 if not(f>=0x25609 and f<0x25A28 or f>=0x261C3 and f<0x261FF) then return end
 local t=emu.getState()
 local function r(x)return emu.read(x,emu.memType.nesDebug)end
 textlog:write(string.format('%d,%04X,%s,%04X,%05X,%02X,%02X,%04X,%02X\n',frame,t['cpu.pc'],tostring(t['cpu.cycleCount']),a,m.address,v,r(0x6cf),r(0x6cd)+256*r(0x6ce),r(0x6f3)))
end,emu.callbackType.read,0x9000,0xBFFF,emu.cpuType.nes,emu.memType.nesMemory)


emu.addEventCallback(function()
 frame=frame+1
 local near=false
 for _,e in ipairs(sequence) do if frame>=e.frame-10 and frame<=e.frame+80 then near=true end end
 if frame%30==0 or frame==limit or near and frame%3==0 then snapshot() end
 if frame==limit then textlog:close();log:close();save('trace_complete.txt',tostring(frame));emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence) do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)

-- Water read-only native gameplay discrimination; controller sequence only.
local player=assert(io.open(out..'/water_player.csv','wb'))
player:write('frame,root,phase,course,state,subphase,pressed,held,jump,supportC1,supportC9,cameraX_hi,cameraX_lo,x_hi,x_lo,y_hi,y_lo,life,clear_count\n')
emu.addEventCallback(function()
 local function r(a)return emu.read(a,emu.memType.nesDebug)end
 if r(0x25)==3 and r(0x18)==4 then
  local fields={frame,r(0x18),r(0x54),r(0x25),r(0x430),r(0x550),r(0x50),r(0x52),r(0x99),r(0xc1),r(0xc9),r(0x69),r(0x6d),r(0x4b0),r(0x4a0),r(0x480),r(0x470),r(0x7c0),r(0x725)}
  player:write(table.concat(fields,',')..'\n')
 end
 if frame==limit then player:close()end
end,emu.eventType.endFrame)
local native=assert(io.open(out..'/water_native.csv','wb'))
native:write('frame,pc,PRG_relative,state,pressed,held,jump,supportC1,supportC9,cameraX_hi,cameraX_lo\n')
for _,pc in ipairs({0xA80E,0xA68E,0xACDF,0xB873,0xA8E2,0xA7CF})do
 emu.addMemoryCallback(function(a,v)
  local m=emu.convertAddress(a,emu.memType.nesMemory)
  if m.memType~=emu.memType.nesPrgRom or m.address~=0x30000+a-0x8000 then return end
  local function r(b)return emu.read(b,emu.memType.nesDebug)end
  if r(0x25)~=3 then return end
  native:write(string.format('%d,%04X,%05X,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,a,m.address,r(0x430),r(0x50),r(0x52),r(0x99),r(0xc1),r(0xc9),r(0x69),r(0x6d)))
 end,emu.callbackType.exec,pc,pc,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then native:close()end end,emu.eventType.endFrame)

-- Read-only damage-write telemetry. Keep exact input and prior observation.
local damage=assert(io.open(out..'/damage_events.csv','wb'))
damage:write('event,frame,address,before,value,pc,PRG_relative,preceding3_hex,a,x,y,sp,ps,cycles,bank8000,bankA000,bankC000,bankE000,caller,state,life,boat_art,boat_state,player_xhi,player_xlo,player_yhi,player_ylo,boat_xhi,boat_xlo,boat_yhi,boat_ylo,supportC1,supportC9,jump,cameraX_hi,cameraX_lo\n')
local serial=0
for _,address in ipairs({0x0430,0x07C0})do
 emu.addMemoryCallback(function(a,v)
  local function r(b)return emu.read(b,emu.memType.nesDebug)end
  if r(0x18)~=4 or r(0x25)~=3 or r(0x54)~=5 then return end
  if r(a)==v or (a==0x430 and v~=6)then return end
  serial=serial+1
  local st=emu.getState();local pc=st['cpu.pc'];local pm=emu.convertAddress(pc,emu.memType.nesMemory)
  local bytes={};for k=pc-3,pc-1 do bytes[#bytes+1]=string.format('%02X',r(k))end
  local banks={};for _,b in ipairs({0x8000,0xA000,0xC000,0xE000})do banks[#banks+1]=string.format('%05X',emu.convertAddress(b,emu.memType.nesMemory).address)end
  local caller=r(0x100+((st['cpu.sp']+1)%256))+256*r(0x100+((st['cpu.sp']+2)%256))
  local fields={serial,frame,string.format('%04X',a),r(a),v,string.format('%04X',pc),string.format('%05X',pm.address),table.concat(bytes,''),st['cpu.a'],st['cpu.x'],st['cpu.y'],st['cpu.sp'],st['cpu.ps'],st['cpu.cycleCount'],banks[1],banks[2],banks[3],banks[4],string.format('%04X',caller),r(0x430),r(0x7c0),r(0x401),r(0x421),r(0x4b0),r(0x4a0),r(0x480),r(0x470),r(0x4b1),r(0x4a1),r(0x481),r(0x471),r(0xc1),r(0xc9),r(0x99),r(0x69),r(0x6d)}
  damage:write(table.concat(fields,',')..'\n')
  dump(string.format('damage_%04d_before_ram.bin',serial),emu.memType.nesDebug,0x800)
 end,emu.callbackType.write,address,address,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then damage:close()end end,emu.eventType.endFrame)

local profiles={{250,6,228,0},{250,6,244,0},{250,6,0,28},{250,6,0,12},{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0}}
local shapes={{248,8,228,0},{248,8,234,246},{251,6,234,4},{252,4,238,1},{247,9,228,0},{250,6,222,4},{249,8,224,254},{244,12,228,0},{250,6,244,2},{248,8,240,0},{254,2,250,0},{249,7,240,248},{249,7,248,255},{243,13,242,254},{240,15,240,248},{249,7,1,8},{249,8,2,20},{249,7,240,255},{249,7,232,255},{249,7,1,16},{249,7,1,24},{248,7,248,7},{255,15,226,232},{242,14,224,248},{251,6,251,6},{242,14,228,0},{240,50,239,248},{206,16,239,248},{242,14,224,0},{242,14,228,0},{247,9,244,254},{255,1,32,33},{245,10,246,252},{246,10,238,2},{242,2,242,254},{2,14,2,14},{250,6,232,240},{250,6,16,24},{169,5,164,121},{192,6,176,2},{165,37,10,168},{185,159,233,133},{0,185,160,233},{133,1,160,0},{177,0,141,25},{6,177,0,153},{128,6,200,192},{32,144,246,206},{24,6,96,171},{233,11,234,203},{233,235,233,43},{234,75,234,49},{15,32,16,49},{15,42,40,49},{15,37,21,49},{15,55,21,49},{15,32,52,49},{56,36,15,49},{15,15,15,49},{15,15,15,49},{56,15,20,49},{41,55,26,49},{39,15,23,49},{15,55,21,49}}

-- Controller-only geometry prediction. All input polls recorded; no RAM writes.
local padlog=assert(io.open(out..'/adaptive_inputs.csv','wb'))
padlog:write('poll,frame,a,b,left,right,up,down,start,select,reason,target,player_x,boat_x,jump,life\n')
local decisions=assert(io.open(out..'/jump_decisions.csv','wb'))
decisions:write('frame,actor,predicted_horizon,actor_state,player_x,actor_x,player_y,actor_y,boat_x,life\n')
local polls=0;local untilA=-1;local lastjump=-100;local reason='fixed';local target=-1
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function w(lo,hi)return r(lo)+256*r(hi)end
local function sg(v)return v<128 and v or v-256 end
local function bit_or(a,b)local z=0;local p=1;for i=1,8 do if a%2==1 or b%2==1 then z=z+p end;a=math.floor(a/2);b=math.floor(b/2);p=p*2 end;return z end
local function yadd(y,o)
 local z=(y+sg(o))%65536;local hi=math.floor(z/256);local lo=z%256
 if hi==math.floor(y/256)then if lo>=240 then hi=(hi+1)%256;lo=(lo+16)%256 end
 else lo=(lo+(o<128 and 16 or -16))%256 end
 return lo+256*hi
end
local function bbox(i,s)
 local x=w(0x4a0+i,0x4b0+i);local y=w(0x470+i,0x480+i)
 return {(x+sg(s[1]))%65536,(x+sg(s[2]))%65536,yadd(y,s[3]),yadd(y,s[4])}
end
local function yp(y)return math.floor(y/256)*240+y%256 end
local function player_shape()
 if r(0x721)~=0 then return nil end
 local index=bit_or(r(0xa2),r(0x722))*2+(r(0xa8)~=0 and 1 or 0)+1
 return profiles[index]
end
local function predict()
 local ps=player_shape();if not ps then return nil end
 local pb=bbox(0,ps);local bvx=(w(0x4e1,0x4f1));if bvx>=32768 then bvx=bvx-65536 end;bvx=bvx/256
 local bvy=w(0x4c1,0x4d1);if bvy>=32768 then bvy=bvy-65536 end;bvy=bvy/256
 for i=2,15 do
  if r(0x420+i)==0x44 then
   local ab=bbox(i,shapes[r(0x530+i)%64+1])
   local avx=w(0x4e0+i,0x4f0+i);if avx>=32768 then avx=avx-65536 end;avx=avx/256
   local avy=w(0x4c0+i,0x4d0+i);if avy>=32768 then avy=avy-65536 end;avy=avy/256
   for n=8,20 do
    local ax0,ax1=ab[1]+avx*n,ab[2]+avx*n;local px0,px1=pb[1]+bvx*n,pb[2]+bvx*n
    local ay0,ay1=yp(ab[3])+avy*n,yp(ab[4])+avy*n;local py0,py1=yp(pb[3])+bvy*n,yp(pb[4])+bvy*n
    if ax1>=px0 and px1>=ax0 and ay1>=py0 and py1>=ay0 then return i,n end
   end
  end
 end
 return nil
end
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 reason='fixed';target=-1
 if frame>=3300 and r(0x18)==4 and r(0x54)==5 and r(0x25)==3 then
  if r(0x99)==0 and r(0xc1)~=0 and r(0x430)>=2 and r(0x430)<=3 and frame-lastjump>=40 then
   local i,n=predict()
   if i then
    untilA=frame+8;lastjump=frame;target=i;reason='predicted_actor'
    decisions:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,i,n,r(0x430+i),w(0x4a0,0x4b0),w(0x4a0+i,0x4b0+i),w(0x470,0x480),w(0x470+i,0x480+i),w(0x4a1,0x4b1),r(0x7c0)))
   end
  end
  if frame<untilA then input.a=true end
  if input.a or r(0x99)~=0 and r(0xc1)==0 then
   local dx=w(0x4a0,0x4b0)-w(0x4a1,0x4b1)
   input.right=dx<=0;input.left=dx>0
   if reason=='fixed'then reason='air_follow_boat'end
  end
 end
 emu.setInput(input,0);polls=polls+1
 local b=function(v)return v and 1 or 0 end
 padlog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d,%d,%d\n',polls,frame,b(input.a),b(input.b),b(input.left),b(input.right),b(input.up),b(input.down),b(input.start),b(input.select),reason,target,w(0x4a0,0x4b0),w(0x4a1,0x4b1),r(0x99),r(0x7c0)))
end,emu.eventType.inputPolled)
emu.addEventCallback(function()if frame==limit then padlog:close();decisions:close()end end,emu.eventType.endFrame)

-- Read-only controller bus and RAM52 writes. Never read IO4016 in a callback.
local bus=assert(io.open(out..'/controller_bus.csv','wb'))
bus:write('event,frame,kind,address,value,pc,PRG_relative,cycles,poll_epoch,held_before,phase,root\n')
local busid=0
local function busrecord(kind,a,v)
 if frame<3300 or frame>4050 then return end
 local st=emu.getState();local pc=st['cpu.pc'];local pm=emu.convertAddress(pc,emu.memType.nesMemory)
 busid=busid+1
 bus:write(string.format('%d,%d,%s,%04X,%d,%04X,%05X,%s,%d,%d,%d,%d\n',busid,frame,kind,a,v,pc,pm.address,tostring(st['cpu.cycleCount']),polls,r(0x52),r(0x54),r(0x18)))
end
emu.addMemoryCallback(function(a,v)busrecord('strobe_write',a,v)end,emu.callbackType.write,0x4016,0x4016,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)busrecord('serial_read',a,v)end,emu.callbackType.read,0x4016,0x4016,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(a,v)busrecord('held_write',a,v)end,emu.callbackType.write,0x52,0x52,emu.cpuType.nes,emu.memType.nesMemory)
local exits=assert(io.open(out..'/water_exit.csv','wb'))
exits:write('event,frame,pc,PRG_relative,cycles,a,x,y,sp,ps,root,phase,state,player_yhi,player_ylo,cameraX_hi,cameraX_lo,cameraY_hi,cameraY_lo,life\n')
local exitid=0
for _,pc in ipairs({0xA658,0xA65A,0xA65C})do
 emu.addMemoryCallback(function(a,v)
  local pm=emu.convertAddress(a,emu.memType.nesMemory)
  if pm.memType~=emu.memType.nesPrgRom or pm.address~=0x30000+a-0x8000 or r(0x18)~=4 or r(0x25)~=3 then return end
  exitid=exitid+1;local st=emu.getState()
  local fields={exitid,frame,string.format('%04X',a),string.format('%05X',pm.address),st['cpu.cycleCount'],st['cpu.a'],st['cpu.x'],st['cpu.y'],st['cpu.sp'],st['cpu.ps'],r(0x18),r(0x54),r(0x430),r(0x480),r(0x470),r(0x69),r(0x6d),r(0x68),r(0x6b),r(0x7c0)}
  exits:write(table.concat(fields,',')..'\n')
  dump(string.format('exit_%03d_before_ram.bin',exitid),emu.memType.nesDebug,0x800)
 end,emu.callbackType.exec,pc,pc,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then bus:close();exits:close()end end,emu.eventType.endFrame)
