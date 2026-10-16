local out=assert(os.getenv('TTA2_QA_OUT'))
local frame=0
local limit=tonumber(os.getenv('TTA2_FRAMES')) or 1800
local f=assert(io.open(out..'/hook_steps.csv','wb'))
f:write('frame,pc,opcode,a,x,y,sp,bank8000,bankA000,bank_return,C6,stack\n')
emu.addMemoryCallback(function(address,value)
 if frame>=918 and frame<=925 and ((address>=0x8e88 and address<=0x8ea3) or (address>=0x95f9 and address<=0x9661) or (address>=0xfdd3 and address<=0xfe09)) then
  local s=emu.getState();local m=emu.convertAddress(0x8000,emu.memType.nesMemory);local n=emu.convertAddress(0xa000,emu.memType.nesMemory);local stack={}
  for i=1,6 do stack[#stack+1]=string.format('%02X',emu.read(0x100+(s['cpu.sp']+i)%256,emu.memType.nesDebug)) end
  f:write(string.format('%d,%04X,%02X,%02X,%02X,%02X,%02X,%05X,%05X,%02X,%02X,%s\n',frame,address,emu.read(address,emu.memType.nesDebug),s['cpu.a'],s['cpu.x'],s['cpu.y'],s['cpu.sp'],m.address,n.address,emu.read(0x2b,emu.memType.nesDebug),emu.read(0xc6,emu.memType.nesDebug),table.concat(stack,' ')))
 end
end,emu.callbackType.exec,0x8000,0xffff,emu.cpuType.nes,emu.memType.nesMemory)
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then f:close();local h=assert(io.open(out..'/trace_complete.txt','wb'));h:write(tostring(frame));h:close();emu.stop(0) end
end,emu.eventType.endFrame)
