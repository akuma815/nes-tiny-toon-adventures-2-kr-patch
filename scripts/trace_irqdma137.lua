-- Narrow native IRQ acceptance and body after declared initial ticket3 seed.
local out=assert(os.getenv('TTA2_QA_OUT'));local limit=tonumber(os.getenv('TTA2_FRAMES'));local frame=0;local finalize137=nil;local active=false;local count=0;local lastidle={}
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function save(n,b)local f=assert(io.open(out..'/'..n,'wb'));f:write(b);f:close()end
local function file(n,h)local f=assert(io.open(out..'/'..n,'wb'));f:write(h..'\n');return f end
local inst=file('IRQ_instructions.csv','frame,irq,kind,pc,opcode,PRG_relative,cycle,a,x,y,ps,sp,scanline,dot')
local ports=file('IRQ_ports.csv','frame,irq,pc,cycle,address,value,scanline,dot')
local reads=file('IRQ_reads.csv','frame,irq,pc,cycle,address,value')
local idle=file('idle_opcodes.csv','frame,pc,cycle,a,ps,RAM22,scanline,dot')
local entries=file('IRQ_entries.csv','frame,irq,cycle,sp,saved_pc,saved_ps,last_idle_pc,last_idle_cycle,scanline,dot')
local counters=file('frame_counters.csv','frame,cycle,RAM1B,RAM22,root,phase,ride,font')
local seedlog=file('seed_writes.csv','frame,pc,cycles,address,before,value,after')
local function window()return frame>=1999 and frame<=2002 end
local function instruction(kind,p,v)
 local s=emu.getState();local m=emu.convertAddress(p,emu.memType.nesMemory)
 inst:write(string.format('%d,%d,%s,%04X,%02X,%05X,%s,%02X,%02X,%02X,%02X,%02X,%s,%s\n',frame,count,kind,p,v,m.address,tostring(s['cpu.cycleCount']),s['cpu.a'],s['cpu.x'],s['cpu.y'],s['cpu.ps'],s['cpu.sp'],tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
end
emu.addMemoryCallback(function(p,v)
 if not window()then return end
 local s=emu.getState();lastidle={pc=p,cycle=s['cpu.cycleCount']}
 idle:write(string.format('%d,%04X,%s,%02X,%02X,%02X,%s,%s\n',frame,p,tostring(s['cpu.cycleCount']),s['cpu.a'],s['cpu.ps'],r(0x22),tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
end,emu.callbackType.exec,0xfe53,0xfe5e,emu.cpuType.nes,emu.memType.nesMemory)
emu.addMemoryCallback(function(p,v)
 if not window()then return end
 if p==0xfa5b then
  assert(not active and lastidle.pc);active=true;count=count+1;local s=emu.getState();local sp=s['cpu.sp'];local pc=r(0x100+((sp+2)%256))+256*r(0x100+((sp+3)%256))
  entries:write(string.format('%d,%d,%s,%02X,%04X,%02X,%04X,%s,%s,%s\n',frame,count,tostring(s['cpu.cycleCount']),sp,pc,r(0x100+((sp+1)%256)),lastidle.pc,tostring(lastidle.cycle),tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
  local t={};for i=0,0x7ff do t[#t+1]=string.char(r(i))end;save(string.format('IRQ_%02d_entry_RAM.bin',count),table.concat(t));instruction('entry',p,v)
 elseif active then instruction('exec',p,v)end
 if p==0xfd18 and active then active=false end
end,emu.callbackType.exec,0xfa5b,0xfd18,emu.cpuType.nes,emu.memType.nesMemory)
for _,a in ipairs({0xa000,0xa008,0xb000,0xb008,0xc000,0xc008,0xd000,0xd008,0xf000,0xf008,0x2000,0x2005,0x2006})do
 emu.addMemoryCallback(function(p,v)
  if not window()then return end;local s=emu.getState()
  ports:write(string.format('%d,%d,%04X,%s,%04X,%02X,%s,%s\n',frame,active and count or 0,s['cpu.pc'],tostring(s['cpu.cycleCount']),p,v,tostring(s['ppu.scanline']),tostring(s['ppu.cycle'])))
 end,emu.callbackType.write,a,a,emu.cpuType.nes,emu.memType.nesMemory)
end
emu.addMemoryCallback(function(p,v)
 if active then local s=emu.getState();reads:write(string.format('%d,%d,%04X,%s,%04X,%02X\n',frame,count,s['cpu.pc'],tostring(s['cpu.cycleCount']),p,v))end
end,emu.callbackType.read,0x2000,0x2007,emu.cpuType.nes,emu.memType.nesMemory)
local sequence={}
for item in string.gmatch(assert(os.getenv('TTA2_INPUTS')),'[^;]+')do local n,d,b=string.match(item,'^(%d+),(%d+),(%a+)$');sequence[#sequence+1]={frame=tonumber(n),duration=tonumber(d),button=b}end
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false};for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end;emu.setInput(input,0)
end,emu.eventType.inputPolled)
local seeds={};local seeded=false;local seedframe=tonumber(os.getenv('TTA2_SEED_FRAME'))
for item in string.gmatch(assert(os.getenv('TTA2_SEEDS')),'[^;]+')do local a,v=string.match(item,'^(%d+),(%d+)$');a=tonumber(a);v=tonumber(v);assert(a>=0x7d0 and a<=0x7d2 and v>=0 and v<=9);seeds[#seeds+1]={a=a,v=v}end
emu.addEventCallback(function()
 frame=frame+1
 if frame==seedframe then
  assert(not seeded);seeded=true;for _,e in ipairs(seeds)do local before=r(e.a);local s=emu.getState();emu.write(e.a,e.v,emu.memType.nesDebug);assert(r(e.a)==e.v);seedlog:write(string.format('%d,%04X,%s,%04X,%02X,%02X,%02X\n',frame,s['cpu.pc'],tostring(s['cpu.cycleCount']),e.a,before,e.v,r(e.a)))end
 end
 local s=emu.getState();counters:write(string.format('%d,%s,%02X,%02X,%02X,%02X,%02X,%02X\n',frame,tostring(s['cpu.cycleCount']),r(0x1b),r(0x22),r(0x18),r(0x54),r(0x25),r(0x6f3)))
 if frame==limit then
  assert(seeded and count>0 and not active);inst:close();ports:close();reads:close();idle:close();entries:close();counters:close();seedlog:close();assert(finalize137);finalize137();save('trace_complete.txt',tostring(frame));emu.stop(0)
 end
end,emu.eventType.endFrame)

-- Work137: fresh native PCM-CDL and narrowly recorded DMC cursor reads.
local function cdl(name,initial)
 local c=emu.getCdlData(emu.memType.nesPrgRom);local n=emu.getMemorySize(emu.memType.nesPrgRom);local base=c[0]~=nil and 0 or 1;local t={};local pcm=0
 for i=0,n-1 do local v=assert(c[i+base]);t[#t+1]=string.char(v);if(v&0x80)~=0 then pcm=pcm+1 end end
 if initial then assert(pcm==0)else assert(pcm>0)end;save(name,table.concat(t))
end
cdl('initial_PRG_cdl.bin',true)
local dmc=assert(io.open(out..'/DMC_reads.csv','wb'));dmc:write('frame,cycle,pc,address,value,PRG_relative,current_address,bytes_remaining,sample_address,sample_length,silence,irq\n')
local dmccount=0
emu.addMemoryCallback(function(p,v)
 if not window()then return end;local st=emu.getState()
 if p==st['apu.dmc.currentAddr']and st['apu.dmc.bytesRemaining']>0 then
  local m=emu.convertAddress(p,emu.memType.nesMemory);dmccount=dmccount+1
  dmc:write(string.format('%d,%s,%04X,%04X,%02X,%05X,%04X,%d,%04X,%d,%s,%d\n',frame,tostring(st['cpu.cycleCount']),st['cpu.pc'],p,v,m.address,st['apu.dmc.currentAddr'],st['apu.dmc.bytesRemaining'],st['apu.dmc.sampleAddr'],st['apu.dmc.sampleLength'],tostring(st['apu.dmc.silenceFlag']),active and count or 0))
 end
end,emu.callbackType.read,0xc000,0xc880,emu.cpuType.nes,emu.memType.nesMemory)
finalize137=function()assert(dmccount>0);dmc:close();cdl('final_PRG_cdl.bin',false)end
