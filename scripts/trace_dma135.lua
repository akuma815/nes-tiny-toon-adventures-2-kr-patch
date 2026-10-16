-- Natural first home call only: instruction gaps + native DMC cursor + freshCDL.
local out=assert(os.getenv('TTA2_QA_OUT'));local limit=tonumber(os.getenv('TTA2_FRAMES'));local frame=0;local active=false;local entered=false;local returned=false
local function save(n,b)local f=assert(io.open(out..'/'..n,'wb'));f:write(b);f:close()end
local function dump(n)local t={};for i=0,0x7ff do t[#t+1]=string.char(emu.read(i,emu.memType.nesDebug))end;save(n,table.concat(t))end
local instructions=assert(io.open(out..'/instructions.csv','wb'));instructions:write('frame,kind,pc,opcode,PRG_relative,cycle,a,x,y,ps,sp,scanline,dot\n')
local dmc=assert(io.open(out..'/DMC_reads.csv','wb'));dmc:write('frame,cycle,pc,address,value,PRG_relative,current_address,bytes_remaining,sample_address,sample_length,silence\n')
local function record(kind,p,v)
 local s=emu.getState();local m=emu.convertAddress(p,emu.memType.nesMemory)
 instructions:write(string.format('%d,%s,%04X,%02X,%05X,%s,%02X,%02X,%02X,%02X,%02X,%s,%s\n',frame,kind,p,v,m.address,tostring(s['cpu.cycleCount']),s['cpu.a'],s['cpu.x'],s['cpu.y'],s['cpu.ps'],s['cpu.sp'],tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
end
local function exec(p,v)
 if frame~=924 then return end
 local m=emu.convertAddress(p,emu.memType.nesMemory)
 if p==0x9417 and m.address==0x25417 and not entered then
  entered=true;active=true;dump('entry_RAM.bin');record('entry',p,v)
  local s=emu.getState();assert(s['cpu.sp']==0xf5 and emu.read(0x1f6,emu.memType.nesDebug)==0xb9 and emu.read(0x1f7,emu.memType.nesDebug)==0x9b)
 elseif active then record('exec',p,v)end
end
emu.addMemoryCallback(exec,emu.callbackType.exec,0x9417,0x96ff,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(exec,emu.callbackType.exec,0xfdd3,0xfdfc,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(p,v)
 if frame==924 and active then record('returned',p,v);returned=true;active=false;dump('returned_RAM.bin')end
end,emu.callbackType.exec,0x9bba,0x9bba,emu.cpuType.nes,emu.memType.nesMemory)
local function cdl(name,initial)
 local c=emu.getCdlData(emu.memType.nesPrgRom);local n=emu.getMemorySize(emu.memType.nesPrgRom);local base=c[0]~=nil and 0 or 1;local t={};local count=0
 for i=0,n-1 do local v=assert(c[i+base]);t[#t+1]=string.char(v);if(v&0x80)~=0 then count=count+1 end end
 if initial then assert(count==0)else assert(count>0)end;save(name,table.concat(t))
end
cdl('initial_PRG_cdl.bin',true)
local reads=0
emu.addMemoryCallback(function(p,v)
 if frame<920 or frame>926 then return end
 local s=emu.getState()
 if p==s['apu.dmc.currentAddr'] and s['apu.dmc.bytesRemaining']>0 then
  local m=emu.convertAddress(p,emu.memType.nesMemory);reads=reads+1
  dmc:write(string.format('%d,%s,%04X,%04X,%02X,%05X,%04X,%d,%04X,%d,%s\n',frame,tostring(s['cpu.cycleCount']),s['cpu.pc'],p,v,m.address,s['apu.dmc.currentAddr'],s['apu.dmc.bytesRemaining'],s['apu.dmc.sampleAddr'],s['apu.dmc.sampleLength'],tostring(s['apu.dmc.silenceFlag'])))
 end
end,emu.callbackType.read,0xc000,0xc880,emu.cpuType.nes,emu.memType.nesMemory)
local sequence={}
for item in string.gmatch(assert(os.getenv('TTA2_INPUTS')),'[^;]+')do local n,d,b=string.match(item,'^(%d+),(%d+),(%a+)$');sequence[#sequence+1]={frame=tonumber(n),duration=tonumber(d),button=b}end
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end;emu.setInput(input,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if frame==limit then
  assert(entered and returned and not active and reads>0);instructions:close();dmc:close();cdl('final_PRG_cdl.bin',false);save('trace_complete.txt',tostring(frame));emu.stop(0)
 end
end,emu.eventType.endFrame)
