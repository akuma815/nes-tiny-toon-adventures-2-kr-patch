-- Explicit native river constructor diagnostic, not natural late-game progression.
local out=assert(os.getenv('TTA2_QA_OUT'))
local limit=assert(tonumber(os.getenv('TTA2_FRAMES')))
local frame=0
local injected=false
local injectFrame=-1
local sequence={}
for item in string.gmatch(assert(os.getenv('TTA2_INPUTS')),'[^;]+')do
 local n,d,b=string.match(item,'^(%d+),(%d+),(%a+)$');assert(n)
 sequence[#sequence+1]={frame=tonumber(n),duration=tonumber(d),button=b}
end
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function save(name,data)local f=assert(io.open(out..'/'..name,'wb'));f:write(data);f:close()end
local function dump(name,kind,size)
 local b={};for i=0,size-1 do b[#b+1]=string.char(emu.read(i,kind))end;save(name,table.concat(b))
end
local function snap()
 local tag=string.format('frame_%05d',frame);save(tag..'.png',emu.takeScreenshot())
 dump(tag..'_ram.bin',emu.memType.nesDebug,0x800)
 dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000)
 dump(tag..'_oam.bin',emu.memType.nesSpriteRam,256)
 local state={};for k,v in pairs(emu.getState())do state[#state+1]=tostring(k)..'='..tostring(v)end
 table.sort(state);save(tag..'_state.txt',table.concat(state,'\n'))
 local rows={'kind,cpu_or_ppu_address,relative_offset,mem_type'}
 for a=0,0x1fff,0x400 do local m=emu.convertAddress(a,emu.memType.nesPpuMemory)
  rows[#rows+1]=string.format('chr,%04X,%05X,%s',a,m.address,tostring(m.memType))end
 for a=0x8000,0xffff,0x2000 do local m=emu.convertAddress(a,emu.memType.nesMemory)
  rows[#rows+1]=string.format('prg,%04X,%05X,%s',a,m.address,tostring(m.memType))end
 save(tag..'_mapping.csv',table.concat(rows,'\n'))
end
local inj=assert(io.open(out..'/river121_injection.csv','wb'))
inj:write('frame,pc,PRG_relative,root,ride,phase,address,before,value,after\n')
local native=assert(io.open(out..'/river121_native.csv','wb'))
native:write('frame,pc,PRG_relative,root,ride,phase,cpu_a,bank38,actor2_state,actor2_art,actor3_art,actor4_art,field69,field6D\n')
local function record(a,m)
 local s=emu.getState()
 native:write(string.format('%d,%04X,%05X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X,%02X\n',frame,a,m.address,r(0x18),r(0x25),r(0x54),s['cpu.a'],r(0x38),r(0x422),r(0x402),r(0x403),r(0x404),r(0x69),r(0x6d)))
end
for _,a in ipairs({0xa5c6,0xa5fd,0xa642,0xb6cc,0xb6e5,0xb6fd,0x9643})do
 emu.addMemoryCallback(function(addr,value)
  local m=emu.convertAddress(addr,emu.memType.nesMemory)
  local base=addr==0x9643 and 0xd643 or 0x10000+addr-0x8000
  if m.address~=base and m.address~=base+0x20000 then return end
  if addr==0xa5c6 and not injected and frame>=3000 then
   assert(r(0x18)==4 and r(0x25)==3 and r(0x54)==5 and r(0x422)==0)
   injected=true;injectFrame=frame
   for _,w in ipairs({{0x69,11},{0x6d,240}})do
    local before=r(w[1]);emu.write(w[1],w[2],emu.memType.nesDebug);assert(r(w[1])==w[2])
    inj:write(string.format('%d,%04X,%05X,04,03,05,%04X,%02X,%02X,%02X\n',frame,addr,m.address,w[1],before,w[2],r(w[1])));inj:flush()
   end
  end
  if injected and frame<=injectFrame+300 then record(addr,m)end
 end,emu.callbackType.exec,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
local fetch={}
emu.addMemoryCallback(function(a,v)
 if not injected or frame>injectFrame+300 then return end
 local s=emu.getState();if s['ppu.scanline']<0 or s['ppu.scanline']>=240 then return end
 local m=emu.convertAddress(a,emu.memType.nesPpuMemory)
 if m.address<0xf400 or m.address>=0xf800 then return end
 local key=string.format('%d,%d,%04X,%05X',frame+1,s['ppu.scanline'],math.floor(a/16)*16,math.floor(m.address/16)*16)
 fetch[key]=(fetch[key]or 0)+1
end,emu.callbackType.read,0x1800,0x1bff,emu.cpuType.nes,emu.memType.nesPpuMemory)
emu.addEventCallback(function()
 frame=frame+1
 if frame%30==0 or injected and frame<=injectFrame+150 and frame%3==0 or frame==limit then snap()end
 if frame==limit then
  assert(injected);inj:close();native:close()
  local rows={'render_frame,scanline,ppu_tile_base,CHR_relative_tile_base,read_count'}
  local keys={};for key in pairs(fetch)do keys[#keys+1]=key end;table.sort(keys)
  for _,key in ipairs(keys)do rows[#rows+1]=key..','..fetch[key]end
  save('river121_render_fetch.csv',table.concat(rows,'\n')..'\n');save('trace_complete.txt',tostring(frame));emu.stop(0)
 end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)

-- Read-only diagnosis of the actor2 disappearance; no additional field writes.
local writes=assert(io.open(out..'/river122_actor2_writes.csv','wb'))
writes:write('event,frame,address,before,value,pc,PRG_relative,cpu_a,cpu_x,cpu_y,cpu_sp,cpu_ps,preceding3_hex,current3_hex,root,ride,phase,field69,field6D\n')
local counter=0
for _,watch in ipairs({0x422,0x402})do
 emu.addMemoryCallback(function(a,v)
  if not injected or frame>injectFrame+300 then return end
  counter=counter+1
  local s=emu.getState();local pc=s['cpu.pc'];local m=emu.convertAddress(pc,emu.memType.nesMemory)
  local function hexbytes(start,n)local b={};for i=0,n-1 do b[#b+1]=string.format('%02X',emu.read(start+i,emu.memType.nesDebug))end;return table.concat(b)end
  writes:write(string.format('%d,%d,%04X,%02X,%02X,%04X,%05X,%02X,%02X,%02X,%02X,%02X,%s,%s,%02X,%02X,%02X,%02X,%02X\n',counter,frame,a,r(a),v,pc,m.address,s['cpu.a'],s['cpu.x'],s['cpu.y'],s['cpu.sp'],s['cpu.ps'],hexbytes(pc-3,3),hexbytes(pc,3),r(0x18),r(0x25),r(0x54),r(0x69),r(0x6d)))
  writes:flush()
  dump(string.format('actor2write_%04d_before_ram.bin',counter),emu.memType.nesDebug,0x800)
 end,emu.callbackType.write,watch,watch,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addEventCallback(function()if frame==limit then writes:close()end end,emu.eventType.endFrame)

-- Once-only projection diagnostic after native ED initialization; actor coordinates unchanged.
local camera=assert(io.open(out..'/river123_camera_writes.csv','wb'))
camera:write('frame,pc,PRG_relative,actor2_art,actor2_state,address,before,value,after\n')
local projected=false
emu.addMemoryCallback(function(a,v)
 if not injected or projected then return end
 local m=emu.convertAddress(a,emu.memType.nesMemory)
 if m.address~=0xd582 and m.address~=0x2d582 then return end
 local s=emu.getState()
 if s['cpu.y']~=2 or r(0x402)~=0xed or r(0x422)~=2 then return end
 assert(frame==injectFrame and r(0x18)==4 and r(0x25)==3 and r(0x54)==5)
 projected=true
 for _,w in ipairs({{0x68,1},{0x6b,64},{0x69,12},{0x6d,128}})do
  local before=r(w[1]);emu.write(w[1],w[2],emu.memType.nesDebug);assert(r(w[1])==w[2])
  camera:write(string.format('%d,%04X,%05X,ED,02,%04X,%02X,%02X,%02X\n',frame,a,m.address,w[1],before,w[2],r(w[1])));camera:flush()
 end
end,emu.callbackType.exec,0x9582,0x9582,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then assert(projected);camera:close()end end,emu.eventType.endFrame)

-- Read-only lower-screen PPU consumer probe in one specific render frame.
local bottom=assert(io.open(out..'/bottom124_PPU_reads.csv','wb'))
bottom:write('render_frame,scanline,dot,address,value,physical_relative,mem_type,vram_address,xscroll,nt_address,nt_value,head_font,active_font,palette32_hex\n')
local mid=false
emu.addMemoryCallback(function(a,v)
 if frame~=3031 then return end
 local s=emu.getState();local line=s['ppu.scanline']
 if line<233 or line>239 then return end
 if not mid then
  mid=true;dump('bottom124_midframe_ppu.bin',emu.memType.nesPpuDebug,0x4000)
  dump('bottom124_midframe_ram.bin',emu.memType.nesDebug,0x800)
  local state={};for k,x in pairs(s)do state[#state+1]=tostring(k)..'='..tostring(x)end;table.sort(state);save('bottom124_midframe_state.txt',table.concat(state,'\n'))
 end
 local m=emu.convertAddress(a,emu.memType.nesPpuMemory)
 local nt=0x2000+(s['ppu.videoRamAddr']%0x1000)
 local pal={};for i=0,31 do pal[#pal+1]=string.format('%02X',emu.read(0x3f00+i,emu.memType.nesPpuDebug))end
 bottom:write(string.format('%d,%d,%d,%04X,%02X,%05X,%s,%04X,%d,%04X,%02X,%02X,%02X,%s\n',frame+1,line,s['ppu.cycle'],a,emu.read(a,emu.memType.nesPpuDebug),m.address,tostring(m.memType),s['ppu.videoRamAddr'],s['ppu.xScroll'],nt,emu.read(nt,emu.memType.nesPpuDebug),r(0x34),r(0x6f3),table.concat(pal)))
end,emu.callbackType.read,0,0x3eff,emu.cpuType.nes,emu.memType.nesPpuMemory)
emu.addEventCallback(function()if frame==limit then assert(mid);bottom:close()end end,emu.eventType.endFrame)
