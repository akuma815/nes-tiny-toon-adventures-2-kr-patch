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

-- Work67 geometry-aware controller, offline verified level0 arena only.
local r=function(a)return emu.read(a,emu.memType.nesDebug)end
local function signed(lo,hi)local v=r(lo)+256*r(hi);if v>=32768 then return v-65536 end;return v end
local function xy(i)return r(0x470+i)+240*r(0x480+i),r(0x4a0+i)+256*r(0x4b0+i)end
local function car(i)return(r(0x420+i)==0x2e or r(0x420+i)==0x2f)and(r(0x410+i)&1)~=0 and r(0x480+i)<=1 and r(0x4b0+i)<=1 end
local floor={}
floor[335]=true
floor[365]=true
floor[395]=true
floor[425]=true
floor[455]=true
floor[485]=true
floor[515]=true
floor[545]=true
floor[575]=true
floor[605]=true
floor[336]=true
floor[366]=true
floor[396]=true
floor[426]=true
floor[456]=true
floor[486]=true
floor[516]=true
floor[546]=true
floor[576]=true
floor[606]=true
floor[277]=true
floor[307]=true
floor[337]=true
floor[367]=true
floor[397]=true
floor[427]=true
floor[517]=true
floor[547]=true
floor[577]=true
floor[607]=true
floor[637]=true
floor[667]=true
floor[278]=true
floor[308]=true
floor[338]=true
floor[368]=true
floor[398]=true
floor[428]=true
floor[518]=true
floor[548]=true
floor[578]=true
floor[608]=true
floor[638]=true
floor[668]=true
floor[219]=true
floor[249]=true
floor[279]=true
floor[309]=true
floor[339]=true
floor[369]=true
floor[399]=true
floor[429]=true
floor[459]=true
floor[489]=true
floor[519]=true
floor[549]=true
floor[579]=true
floor[609]=true
floor[639]=true
floor[669]=true
floor[699]=true
floor[729]=true
floor[220]=true
floor[250]=true
floor[280]=true
floor[310]=true
floor[340]=true
floor[370]=true
floor[400]=true
floor[430]=true
floor[460]=true
floor[490]=true
floor[520]=true
floor[550]=true
floor[580]=true
floor[610]=true
floor[640]=true
floor[670]=true
floor[700]=true
floor[730]=true
floor[221]=true
floor[251]=true
floor[281]=true
floor[311]=true
floor[341]=true
floor[371]=true
floor[401]=true
floor[431]=true
floor[461]=true
floor[491]=true
floor[521]=true
floor[551]=true
floor[581]=true
floor[611]=true
floor[641]=true
floor[671]=true
floor[701]=true
floor[731]=true
floor[222]=true
floor[252]=true
floor[282]=true
floor[312]=true
floor[342]=true
floor[372]=true
floor[402]=true
floor[432]=true
floor[462]=true
floor[492]=true
floor[522]=true
floor[552]=true
floor[582]=true
floor[612]=true
floor[642]=true
floor[672]=true
floor[702]=true
floor[732]=true
floor[223]=true
floor[253]=true
floor[283]=true
floor[313]=true
floor[343]=true
floor[373]=true
floor[403]=true
floor[433]=true
floor[463]=true
floor[493]=true
floor[523]=true
floor[553]=true
floor[583]=true
floor[613]=true
floor[643]=true
floor[673]=true
floor[703]=true
floor[733]=true
floor[224]=true
floor[254]=true
floor[284]=true
floor[314]=true
floor[344]=true
floor[374]=true
floor[404]=true
floor[434]=true
floor[464]=true
floor[494]=true
floor[524]=true
floor[554]=true
floor[584]=true
floor[614]=true
floor[644]=true
floor[674]=true
floor[704]=true
floor[734]=true
floor[225]=true
floor[255]=true
floor[285]=true
floor[315]=true
floor[345]=true
floor[375]=true
floor[405]=true
floor[435]=true
floor[465]=true
floor[495]=true
floor[525]=true
floor[555]=true
floor[585]=true
floor[615]=true
floor[645]=true
floor[675]=true
floor[705]=true
floor[735]=true
floor[226]=true
floor[256]=true
floor[286]=true
floor[316]=true
floor[346]=true
floor[376]=true
floor[406]=true
floor[436]=true
floor[466]=true
floor[496]=true
floor[526]=true
floor[556]=true
floor[586]=true
floor[616]=true
floor[646]=true
floor[676]=true
floor[706]=true
floor[736]=true
floor[227]=true
floor[257]=true
floor[287]=true
floor[317]=true
floor[347]=true
floor[377]=true
floor[407]=true
floor[437]=true
floor[467]=true
floor[497]=true
floor[527]=true
floor[557]=true
floor[587]=true
floor[617]=true
floor[647]=true
floor[677]=true
floor[707]=true
floor[737]=true
floor[228]=true
floor[258]=true
floor[288]=true
floor[318]=true
floor[348]=true
floor[378]=true
floor[408]=true
floor[438]=true
floor[468]=true
floor[498]=true
floor[528]=true
floor[558]=true
floor[588]=true
floor[618]=true
floor[648]=true
floor[678]=true
floor[708]=true
floor[738]=true
floor[289]=true
floor[319]=true
floor[349]=true
floor[379]=true
floor[409]=true
floor[439]=true
floor[469]=true
floor[499]=true
floor[529]=true
floor[559]=true
floor[589]=true
floor[619]=true
floor[649]=true
floor[679]=true
floor[290]=true
floor[320]=true
floor[350]=true
floor[380]=true
floor[410]=true
floor[440]=true
floor[470]=true
floor[500]=true
floor[530]=true
floor[560]=true
floor[590]=true
floor[620]=true
floor[650]=true
floor[680]=true
floor[351]=true
floor[381]=true
floor[411]=true
floor[441]=true
floor[471]=true
floor[501]=true
floor[531]=true
floor[561]=true
floor[591]=true
floor[621]=true
floor[352]=true
floor[382]=true
floor[412]=true
floor[442]=true
floor[472]=true
floor[502]=true
floor[532]=true
floor[562]=true
floor[592]=true
floor[622]=true
local headings={[1]=6,[2]=2,[4]=0,[8]=4,[5]=7,[6]=1,[9]=5,[10]=3}
local function safe(x,y)
 return floor[y*30+x] and not(x>=6 and x<=9 and y>=14 and y<=17)
end
local function route(px,py,tx,ty)
 local sx,sy=math.floor(px/16),math.floor(py/16);local gx,gy=math.floor(tx/16),math.floor(ty/16)
 if not safe(gx,gy)then
  local best=math.huge
  for k,_ in pairs(floor)do local x,y=k%30,math.floor(k/30);local d=(x*16+8-tx)^2+(y*16+8-ty)^2;if safe(x,y)and d<best then best=d;gx=x;gy=y end end
 end
 local sk=sy*30+sx;local goal=gy*30+gx;local queue={sk};local prev={[sk]=-1};local n=1
 while n<=#queue do
  local k=queue[n];n=n+1;if k==goal then break end
  local x,y=k%30,math.floor(k/30)
  for _,d in ipairs({{1,0},{-1,0},{0,1},{0,-1}})do local xx,yy=x+d[1],y+d[2];local kk=yy*30+xx;if xx>=0 and xx<30 and yy>=0 and yy<32 and safe(xx,yy)and prev[kk]==nil then prev[kk]=k;queue[#queue+1]=kk end end
 end
 if prev[goal]==nil then return tx,ty,false end
 if goal==sk then return tx,ty,true end
 local k=goal;while prev[k]~=sk and prev[k]~=-1 do k=prev[k]end
 return(k%30)*16+8,math.floor(k/30)*16+8,true
end
local log=assert(io.open(out..'/cart_geometry_policy.csv','wb'));log:write('frame,root,phase,level,life,history,gold,px,py,vx,vy,target,tx,ty,aimx,aimy,mode,mask,charge,heading,path_found\n')
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 local px,py=xy(0);local vx,vy=signed(0x4c0,0x4d0)/256,signed(0x4e0,0x4f0)/256
 local target=-1;local tx,ty=-1,-1;local ax,ay=px,py;local mode='menu';local found=false
 if r(0x18)==4 and r(0x54)==5 and r(0x25)==1 and r(0x79)==0 and r(0x400)~=0 and r(0x480)<=1 and r(0x4b0)<=1 then
  input.a=false;input.b=false;input.up=false;input.down=false;input.left=false;input.right=false
  local closest=math.huge
  for i=1,15 do if car(i)then local x,y=xy(i);local d=(x-px)^2+(y-py)^2;if d<closest then closest=d;target=i;tx=x;ty=y end end end
  local dist=math.sqrt(closest)
  if target>=0 then
   local dx,dy=tx-128,ty-256;local len=math.sqrt(dx*dx+dy*dy);if len<1 then len=1 end
   local sx,sy=tx+dx/len*42,ty+dy/len*42
   if math.sqrt((px-sx)^2+(py-sy)^2)<26 or dist<30 then ax,ay=tx,ty;mode='push'
   else ax,ay,found=route(px,py,sx,sy);mode='approach'end
  else ax,ay,found=route(px,py,256,256);mode='no_target'end
  local predictedx,predictedy=px+vx*12,py+vy*12
  if predictedx>94 and predictedx<162 and predictedy>222 and predictedy<290 then
   local dx,dy=px-128,py-256;local len=math.sqrt(dx*dx+dy*dy);if len<1 then dx=1;len=1 end
   ax,ay=px+dx/len*40,py+dy/len*40;mode='pit_avoid';input.b=true
  end
  local dx,dy=(ax-px)*0.10-vx*1.5,(ay-py)*0.10-vy*1.5
  local direction=0;if dx>0.20 then direction=direction|1 elseif dx< -0.20 then direction=direction|2 end;if dy>0.20 then direction=direction|4 elseif dy< -0.20 then direction=direction|8 end
  if direction==0 then input.b=true;direction=1 end
  input.right=(direction&1)~=0;input.left=(direction&2)~=0;input.down=(direction&4)~=0;input.up=(direction&8)~=0
  input.a=frame%32<(mode=='push'and24 or12)
  if mode~='push'and vx*vx+vy*vy>2.25 then input.b=true end
  if mode=='pit_avoid'then input.a=false end
 elseif r(0x18)==4 and r(0x25)==1 and r(0x54)>=0x20 and r(0x54)<=0x24 then input.a=frame%120<8;mode='native_bonus' end
 local mask=0;for key,bit in pairs({a=128,b=64,select=32,start=16,up=8,down=4,left=2,right=1})do if input[key]then mask=mask|bit end end
 emu.setInput(input,0)
 log:write(string.format('%d,%02X,%02X,%d,%02X,%02X,%02X,%d,%d,%.4f,%.4f,%d,%d,%d,%.4f,%.4f,%s,%02X,%d,%d,%s\n',frame,r(0x18),r(0x54),r(0x79),r(0x7c0),r(0x7e1),r(0x7e0),px,py,vx,vy,target,tx,ty,ax,ay,mode,mask,r(0xa9)+256*r(0xaa),r(0x510),tostring(found)))
end,emu.eventType.inputPolled)
emu.addEventCallback(function()if frame%30==0 then log:flush()end;if frame==limit then log:close()end end,emu.eventType.endFrame)
