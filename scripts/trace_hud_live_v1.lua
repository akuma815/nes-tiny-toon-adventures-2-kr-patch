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
 if frame%30==0 or frame==limit or near and frame%3==0 then snapshot() end
 if frame==limit then log:close();save('trace_complete.txt',tostring(frame));emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence) do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)

-- Read-only post-HUD IRQ consumer; source code checks precede any edit.
local hud=assert(io.open(out..'/hud_live.csv','wb'));hud:write('frame,pc,font0,font1,NTphysical,NTtype,scanline,dot,cycles,tag\n')
emu.addMemoryCallback(function(a,v)
 if frame<2800 or frame%60~=0 then return end
 local s=emu.getState();local tag=string.format('hud_live_%05d',frame);dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000);dump(tag..'_ram.bin',emu.memType.nesDebug,0x800);dump(tag..'_oam.bin',emu.memType.nesSpriteRam,256)
 local state={};for k,x in pairs(s) do state[#state+1]=tostring(k)..'='..tostring(x) end;table.sort(state);save(tag..'_state.txt',table.concat(state,'\n'));local m=emu.convertAddress(0,emu.memType.nesPpuMemory);local n=emu.convertAddress(0x400,emu.memType.nesPpuMemory);local nt=emu.convertAddress(0x2f00,emu.memType.nesPpuMemory)
 hud:write(string.format('%d,%04X,%05X,%05X,%05X,%s,%s,%s,%s,%s\n',frame,s['cpu.pc'],m.address,n.address,nt.address,tostring(nt.memType),tostring(s['ppu.scanline']),tostring(s['ppu.cycle']),tostring(s['cpu.cycleCount']),tag));hud:flush()
end,emu.callbackType.exec,0xfd08,0xfd08,emu.cpuType.nes,emu.memType.nesMemory)
local copies=assert(io.open(out..'/CHR_asset_copies.csv','wb'));copies:write('frame,selector,ppu_start,ppu_end,CHR_relative_start,file\n')
emu.addMemoryCallback(function(a,v)
 if frame<550 then return end
 local s=emu.getState();local selector=s['cpu.x'];local base=0x8233+selector;local lo=emu.read(base,emu.memType.nesDebug)+256*emu.read(base+1,emu.memType.nesDebug);local hi=emu.read(base+2,emu.memType.nesDebug)+256*emu.read(base+3,emu.memType.nesDebug);local m=emu.convertAddress(lo,emu.memType.nesPpuMemory);local tag=string.format('asset_%05d_%02x.bin',frame,selector);local data={};for i=0,hi-lo-1 do data[#data+1]=string.char(emu.read(0x400+i,emu.memType.nesDebug))end;save(tag,table.concat(data));copies:write(string.format('%d,%02X,%04X,%04X,%05X,%s\n',frame,selector,lo,hi,m.address,tag));copies:flush()
end,emu.callbackType.exec,0x8216,0x8216,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()if frame==limit then hud:close();copies:close() end end,emu.eventType.endFrame)
