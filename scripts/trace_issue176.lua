-- Private saved-state issue observation only. No controller/RAM/ROM patches.
local out=assert(os.getenv('TT_ISSUE_OUT'))
local statepath=assert(os.getenv('TT_ISSUE_STATE'))
local loaded=false
local frame=0
local function save(name,data)
 local f=assert(io.open(out..'/'..name,'wb'));f:write(data);f:close()
end
local function dump(name,kind,size)
 local b={};for i=0,size-1 do b[#b+1]=string.char(emu.read(i,kind))end
 save(name,table.concat(b))
end
local function snapshot(tag)
 dump(tag..'_ram.bin',emu.memType.nesDebug,0x800)
 dump(tag..'_ppu.bin',emu.memType.nesPpuDebug,0x4000)
 dump(tag..'_oam.bin',emu.memType.nesSpriteRam,256)
 local rows={};for k,v in pairs(emu.getState())do rows[#rows+1]=tostring(k)..'='..tostring(v)end
 table.sort(rows);save(tag..'_state.txt',table.concat(rows,'\n'))
 local maps={'kind,address,relative_offset,mem_type'}
 for a=0,0x1fff,0x400 do local m=emu.convertAddress(a,emu.memType.nesPpuMemory);maps[#maps+1]=string.format('chr,%04X,%05X,%s',a,m.address,tostring(m.memType))end
 for a=0x8000,0xffff,0x2000 do local m=emu.convertAddress(a,emu.memType.nesMemory);maps[#maps+1]=string.format('prg,%04X,%05X,%s',a,m.address,tostring(m.memType))end
 save(tag..'_mapping.csv',table.concat(maps,'\n'));save(tag..'.png',emu.takeScreenshot())
end
local ri=emu.getRomInfo();local info={}
for k,v in pairs(ri)do info[#info+1]=tostring(k)..'='..tostring(v)end;table.sort(info);save('rom_info.txt',table.concat(info,'\n'))
emu.addMemoryCallback(function()
 if not loaded then
  loaded=true
  local f=assert(io.open(statepath,'rb'));local b=f:read('*all');f:close()
  emu.loadSavestate(b);snapshot('restored');save('state_loaded.txt',statepath)
 end
end,emu.callbackType.exec,0xfd9e,0xfd9e,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 if loaded then
  frame=frame+1
  if frame<=3 or frame==12 then snapshot(string.format('frame_%03d',frame))end
  if frame==12 then save('trace_complete.txt','12');emu.stop(0)end
 end
end,emu.eventType.endFrame)
