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



local native=assert(io.open(out..'/ppu_native_writes.csv','wb'))
native:write('frame,address,value,scanline,dot,cycles,root,page,font,background_enabled,sprites_enabled\n')
emu.addMemoryCallback(function(a,v)
 if emu.read(0x18,emu.memType.nesDebug)~=7 then return end
 local t=emu.getState()
 native:write(string.format('%d,%04X,%02X,%s,%s,%s,%02X,%02X,%02X,%s,%s\n',frame,a,v,tostring(t['ppu.scanline']),tostring(t['ppu.cycle']),tostring(t['cpu.cycleCount']),emu.read(0x18,emu.memType.nesDebug),emu.read(0x6cf,emu.memType.nesDebug),emu.read(0xc6,emu.memType.nesDebug),tostring(t['ppu.mask.backgroundEnabled']),tostring(t['ppu.mask.spritesEnabled'])))
end,emu.callbackType.write,0x2000,0x2fff,emu.cpuType.nes,emu.memType.nesPpuMemory)
local packets=assert(io.open(out..'/paired_printer.csv','wb'))
packets:write('frame,kind,page,cursor,queue_size,low_nt,high_nt,PRG_relative_offset,sp,cycles,queue_hex\n')
local function packet(kind)
 local m=emu.convertAddress(0x8000,emu.memType.nesMemory)
 if m.address~=0x10000 then return end
 local t=emu.getState();local function r(a)return emu.read(a,emu.memType.nesDebug)end
 local q={};for i=0,r(0x1e) do q[#q+1]=string.format('%02X',r(0x100+i))end
 packets:write(string.format('%d,%s,%02X,%02X,%02X,%02X,%02X,%05X,%02X,%s,%s\n',frame,kind,r(0x6cf),r(0x6c3),r(0x1e),r(0x6c0),r(0x6c1),m.address,t['cpu.sp'],tostring(t['cpu.cycleCount']),table.concat(q)))
end
emu.addMemoryCallback(function()packet('begin')end,emu.callbackType.exec,0x9800,0x9800,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function()packet('end')end,emu.callbackType.exec,0x9612,0x9612,emu.cpuType.nes,emu.memType.nesMemory)


local init=assert(io.open(out..'/opening_init_clear.csv','wb'))
init:write('frame,page,root,old_pointer,font,rows9_hex,PRG_relative_offset,sp\n')
emu.addMemoryCallback(function()
 local function r(a)return emu.read(a,emu.memType.nesDebug)end
 if r(0x18)~=7 or r(0x6cf)<1 or r(0x6cf)>9 then return end
 local b={};for y=0,8 do for x=0,23 do b[#b+1]=string.format('%02X',emu.read(0x21e4+y*32+x,emu.memType.nesPpuDebug))end end
 local t=emu.getState();local m=emu.convertAddress(0x8000,emu.memType.nesMemory)
 init:write(string.format('%d,%02X,%02X,%04X,%02X,%s,%05X,%02X\n',frame,r(0x6cf),r(0x18),r(0x6cd)+256*r(0x6ce),r(0xc6),table.concat(b),m.address,t['cpu.sp']))
end,emu.callbackType.exec,0x9417,0x9417,emu.cpuType.nes,emu.memType.nesMemory)

local epochs=assert(io.open(out..'/video_epochs.csv','wb'))
epochs:write('frame,root,palette_hex,chr0000,chr0400\n')
emu.addEventCallback(function()
 frame=frame+1
 local pal={};for a=0x3f00,0x3f1f do pal[#pal+1]=string.format('%02X',emu.read(a,emu.memType.nesPpuDebug))end
 epochs:write(string.format('%d,%02X,%s,%05X,%05X\n',frame,emu.read(0x18,emu.memType.nesDebug),table.concat(pal),emu.convertAddress(0,emu.memType.nesPpuMemory).address,emu.convertAddress(0x400,emu.memType.nesPpuMemory).address))
 local near=false
 for _,e in ipairs(sequence) do if frame>=e.frame-10 and frame<=e.frame+80 then near=true end end
 if frame%30==0 or frame==limit or emu.read(0x18,emu.memType.nesDebug)==7 and frame%3==0 or near and frame%3==0 then snapshot() end
 if frame==limit then textlog:close();log:close();native:close();packets:close();init:close();epochs:close();save('trace_complete.txt',tostring(frame));emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence) do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
