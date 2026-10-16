"""Native pause dispatcher CPU cases and four recorded controller routes; noROM mutation."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/pause049_survey.json';assert not out.exists()
 rom=(R/'build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes').read_bytes();source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));old=(R/source['path']).read_bytes();assert hashlib.sha256(old).hexdigest()==source['sha256']
 assert old[0x6524:0x6547]==rom[0x26524:0x26547]
 ptrs=[int.from_bytes(rom[0x2652a+2*i:0x2652c+2*i],'little')for i in range(8)]
 assert ptrs==[0xa536]*7+[0xa52a]
 cases=0;timings={}
 for slot in range(8):
  for flags in range(256):
   if flags&8:continue
   m=Memory(rom);m.ram[:0x800]=bytes((i*37+91)&255 for i in range(0x800));m.ram[0x6de]=slot;m.ram[0x55]=1
   c=MPU(memory=m);m.cpu=c;c.pc=0xa514;c.sp=0xfd;c.a=0x44;c.x=0x17;c.y=0x29;c.p=flags;m.ram[0x1fe]=0xff;m.ram[0x1ff]=0xc0;before=bytes(m.ram);n=0
   while c.pc!=0xc100:c.step();n+=1;assert n<1000
   assert not m.writes and before[0x34:0x40]==m.ram[0x34:0x40]
   allowed={0xb2,0xb3,0xb4,0xb5,0x1fc,0x1fd}|({0x55,0x6de,0x425}if slot==7 else set())
   assert all(before[i]==m.ram[i]for i in range(0x800)if i not in allowed)
   assert c.sp==0xff and c.x==0x17 and c.processorCycles==(80 if slot==7 else 65)
   cases+=1;timings[str(slot)]=c.processorCycles
 runs=[];frozen=0
 for ride in ('coaster','cart','train','water'):
  d=R/f'qa/dialogue/pause042_{ride}';env=json.loads((d/'environment.json').read_text('utf-8'));assert env['exit_code']==0 and (d/'trace_complete.txt').read_text()=='4500'
  for name,h in env['files'].items():assert sha(d/name)==h;frozen+=1
  logs=list(csv.DictReader((d/'pause_consumers.csv').open()));assert not [x for x in logs if x['kind']=='font120']
  dispatch=[x for x in logs if x['kind']=='exec'and x['pc']=='A514'and x['pause']=='01']
  enter=[x for x in logs if x['kind']=='write'and x['address']=='0055'and x['value']=='01'];leave=[x for x in logs if x['kind']=='write'and x['address']=='0055'and x['value']=='00'];assert len(enter)==len(leave)==1
  first,last=int(enter[0]['frame']),int(leave[0]['frame']);assert first in (3000,3001) and last==3300
  assert [int(x['frame'])for x in dispatch]==list(range(first,last+1)) and all(x['root']=='04'and x['phase']=='05'for x in dispatch)
  assert all(x['subphase']=='00'for x in dispatch[:-1]) and dispatch[-1]['subphase']=='07'
  state={f:(d/f'frame_{f:05d}_ram.bin').read_bytes()for f in (2970,3030,3150,3270,3330)}
  assert state[2970][0x55]==state[3330][0x55]==0 and all(state[f][0x55]==1 for f in (3030,3150,3270))
  pixels={f:Image.open(d/f'frame_{f:05d}.png').convert('RGB').tobytes()for f in (3030,3150,3270,3330)}
  assert pixels[3030]==pixels[3150]==pixels[3270]
  runs.append({'ride':ride,'paused_native_dispatch_calls':len(dispatch),'subphase':0,'actual_pics_frozen':[3030,3150,3270],'font120_121_port_writes_observed':0,'resumed_after3300':True,'screens':len(list(d.glob('frame_*.png'))),'environment_sha256':sha(d/'environment.json')})
 report={'work':49,'status':'PASS','ROM_sha256':hashlib.sha256(rom).hexdigest(),'source_sha256':source['sha256'],'CPU_D_clear_cases':cases,'native_pause_dispatch_cycles':timings,'dispatch_table':ptrs,'no_font_or_PPU_producer_in_native_pause_dispatch':True,'routes':runs,'runtime_frozen_files':frozen,'scope':'Four ordinary ride pause/resume paths, controlleronly; nativepause dispatcher slots0..7 CPUmodel; notallgameunusedproof','limits':['NESdecimaldisabled; NMOSMPU casesexcludeDset','PAUSEbitmap120/121 actualconsumeroutsideobservedpausepath remainsunconnected','Wholeplay/otherengines/physicalconsole/humanreview pending'],'next_action':'Trace actualtrainenginebitmap labels with guardednativehealthdiagnostic; preservePUSHSTARTtitledecision'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k]for k in ('status','CPU_D_clear_cases','routes','runtime_frozen_files')},indent=2))
if __name__=='__main__':main()
