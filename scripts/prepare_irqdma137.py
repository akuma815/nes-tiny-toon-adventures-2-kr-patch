"""Add typed-area/cursor discrimination to frozen136 idle/IRQ trace."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'scripts/trace_irqdma137.lua';assert not p.exists();s=(R/'scripts/trace_irq136.lua').read_text('utf-8').replace('local frame=0;','local frame=0;local finalize137=nil;')
before="save('trace_complete.txt',tostring(frame));emu.stop(0)";assert s.count(before)==1
s=s.replace(before,"assert(finalize137);finalize137();save('trace_complete.txt',tostring(frame));emu.stop(0)")
s+='''
-- Work137: fresh native PCM-CDL and narrowly recorded DMC cursor reads.
local function cdl(name,initial)
 local c=emu.getCdlData(emu.memType.nesPrgRom);local n=emu.getMemorySize(emu.memType.nesPrgRom);local base=c[0]~=nil and 0 or 1;local t={};local pcm=0
 for i=0,n-1 do local v=assert(c[i+base]);t[#t+1]=string.char(v);if(v&0x80)~=0 then pcm=pcm+1 end end
 if initial then assert(pcm==0)else assert(pcm>0)end;save(name,table.concat(t))
end
cdl('initial_PRG_cdl.bin',true)
local dmc=assert(io.open(out..'/DMC_reads.csv','wb'));dmc:write('frame,cycle,pc,address,value,PRG_relative,current_address,bytes_remaining,sample_address,sample_length,silence,irq\\n')
local dmccount=0
emu.addMemoryCallback(function(p,v)
 if not window()then return end;local st=emu.getState()
 if p==st['apu.dmc.currentAddr']and st['apu.dmc.bytesRemaining']>0 then
  local m=emu.convertAddress(p,emu.memType.nesMemory);dmccount=dmccount+1
  dmc:write(string.format('%d,%s,%04X,%04X,%02X,%05X,%04X,%d,%04X,%d,%s,%d\\n',frame,tostring(st['cpu.cycleCount']),st['cpu.pc'],p,v,m.address,st['apu.dmc.currentAddr'],st['apu.dmc.bytesRemaining'],st['apu.dmc.sampleAddr'],st['apu.dmc.sampleLength'],tostring(st['apu.dmc.silenceFlag']),active and count or 0))
 end
end,emu.callbackType.read,0xc000,0xc880,emu.cpuType.nes,emu.memType.nesMemory)
finalize137=function()assert(dmccount>0);dmc:close();cdl('final_PRG_cdl.bin',false)end
''';p.write_text(s,'utf-8')
p=R/'scripts/run_irqdma137.py';assert not p.exists();s=(R/'scripts/run_irq136.py').read_text('utf-8').replace("('trace_irq136.lua',)","('trace_irqdma137.lua',)")
s=s.replace("command=[str(exe),'--testrunner',str(script),str(rom)","qa_rom=output/('TTA2_IRQDMA137_'+output.name+'.nes');qa_rom.write_bytes(rom.read_bytes());assert sha(qa_rom)==rom_sha\n    command=[str(exe),'--testrunner',str(script),str(qa_rom)")
s=s.replace("'rom_sha256':rom_sha,'emulator'","'rom_sha256':rom_sha,'actual_QA_ROM':str(qa_rom),'actual_QA_ROM_sha256':sha(qa_rom),'emulator'")
s=s.replace('Narrow1999..2002 nativeIRQ entry/body/idle discrimination','Narrow1999..2002 nativeIRQ entry/body/idle plus DMC cursor/fresh native PCM-CDL discrimination')
compile(s,str(p),'exec');p.write_text(s,'utf-8')
p=R/'scripts/run_irqdma_pair137.py';assert not p.exists();s=(R/'scripts/run_irq_pair136.py').read_text('utf-8').replace("'work/irq136'","'work/irqdma137'").replace('scripts/run_irq136.py','scripts/run_irqdma137.py').replace('irq136_normal3_{build}','irqdma137_normal3_{build}').replace('scripts/trace_irq136.lua','scripts/trace_irqdma137.lua');compile(s,str(p),'exec');p.write_text(s,'utf-8')
