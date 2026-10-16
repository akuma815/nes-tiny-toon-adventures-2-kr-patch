"""Work86 exact native2F velocity producers and historical/current controller slowdown."""
from pathlib import Path
import hashlib,json,csv,collections,math
from verify_gate_font_tag_hooks import Memory,MPU
from py65.disassembler import Disassembler
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def friction(v):return max(0,v-64)if v>=0 else min(0,v+64)
def signed(v):return v-65536 if v>=32768 else v
def main():
 out=R/'qa/reports/cart_speed086_validation.json';assert not out.exists();rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();sm=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=R/sm['path'];assert sha(source)==sm['sha256'];assert source.read_bytes()[0x14010:0x18010]==blob[0x34010:0x38010]
 mem=Memory(blob);mem.banks=[0x3a,0x3b,0x3e,31];yt=[mem[0x9791+i]for i in range(8)];xt=[mem[0x9799+i]for i in range(8)]
 cases=0;vs=[-1024,-768,-513,-512,-511,-256,-64,-1,0,1,64,255,256,511,512,513,768,1024]
 for heading in range(8):
  for vx in vs:
   for vy in vs:
    m=Memory(blob);m.banks=[0x3a,0x3b,0x3e,31];c=MPU(memory=m);m.cpu=c;c.pc=0x9767;c.x=15;c.p=0x34;c.sp=0xfd
    for base,v in [(0x4c0,vx),(0x4e0,vy)]:m.ram[base+15]=v&255;m.ram[base+31]=(v>>8)&255
    m.ram[0x50f]=heading;m.ram[0x43f]=1;m.ram[0x55f]=8;n=0
    while c.pc!=0x98c2:c.step();n+=1;assert n<100
    ex=(xt[heading]<<8)|(friction(vx)&255);ey=(yt[heading]<<8)|(friction(vy)&255)
    assert m.ram[0x4cf]+256*m.ram[0x4df]==ex and m.ram[0x4ef]+256*m.ram[0x4ff]==ey
    assert m.ram[0x43f]==2 and m.ram[0x55f]==0 and m.ram[0x45f]==80;cases+=1
 q=R/'qa/dialogue/cart086_speed046';env=json.loads((q/'environment.json').read_text('utf-8'));assert env['rom_sha256']==sha(rom)and env['frames']==10000
 for n,h in env['files'].items():assert sha(q/n)==h,n
 rows=list(csv.DictReader((q/'enemy2F_speed.csv').open()));groups=collections.defaultdict(list)
 for r in rows:groups[(r['frame'],r['X'])].append(r)
 charges=0;directions=collections.Counter();examples=[]
 for key,group in groups.items():
  charge=[r for r in group if r['pc']=='9767'and r['kind']=='exec']
  if not charge:continue
  assert len(charge)==1;start=group.index(charge[0]);seq=group[start:];assert [r['pc']for r in seq[:6]]==['9767','ACD2','AD0A',f'{0x9791+int(charge[0]["heading"],16):04X}',f'{0x9799+int(charge[0]["heading"],16):04X}','9781']
  a,y,x,readY,readX,z=seq[:6];h=int(a['heading'],16);assert y['A']==x['A']=='40';assert int(x['vy'])==friction(int(a['vy'])) and x['vx']==a['vx']
  ex=signed((xt[h]<<8)|(friction(int(a['vx']))&255));ey=signed((yt[h]<<8)|(friction(int(a['vy']))&255));assert int(z['vx'])==ex and int(z['vy'])==ey
  assert z['PRG_relative']=='35781' and int(z['A'],16)==xt[h];charges+=1;directions[h]+=1
  if len(examples)<8:examples.append({'frame':a['frame'],'heading':h,'before':[a['vx'],a['vy']],'after':[z['vx'],z['vy']]})
 assert charges==48 and len(directions)==8
 exact=0;images=list(q.glob('frame_*.png'));baseline=R/'qa/dialogue/start077_cart045'
 for p in images:
  if not (baseline/p.name).exists():continue
  for suffix in ('.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):
   x=q/(p.stem+suffix);assert x.read_bytes()==(baseline/x.name).read_bytes();exact+=1
 historical_env=json.loads((baseline/'environment.json').read_text('utf-8'));assert sha(baseline/'cart_round_policy.csv')==historical_env['files']['cart_round_policy.csv']
 ps=[r for r in csv.DictReader((baseline/'cart_round_policy.csv').open())if r['level']=='1'and r['target_type']=='47'and r['phase']=='05'];br=[r for r in ps if int(r['mask'],16)&64];assert br and all(r['mode']=='intercept'for r in br)
 actors=[r for r in csv.DictReader((q/'cart_actors.csv').open())if r['level']=='1'and r['index']=='15'and r['type']=='2F'];speeds=[math.hypot(int(r['vx']),int(r['vy']))/256 for r in actors]
 d=Disassembler(MPU(memory=mem));valid={}
 for pc in [0x95e3,0x9767,0x9781,0xacd2,0xad0a]:n,t=d.instruction_at(pc);assert '???'not in t;valid[f'{pc:04X}']={'instruction':t,'PRG_relative':hex((0x34000 if pc<0xa000 else 0x36000)+(pc%8192))}
 result={'work':86,'status':'PASS_NATIVE2F_SPEED_PRODUCER','ROM_sha256':sha(rom),'ROM_CSV_changes':0,'source_native_movement_16KiB_preserved':True,'native2F_state_inline_table95F9':[f'{mem[0x95f9+i*2]+256*mem[0x95fa+i*2]:04X}'for i in range(4)],'native2F_subphase_inline_table9658':[f'{mem[0x9658+i*2]+256*mem[0x9659+i*2]:04X}'for i in range(9)],'speed_highbyte_tables':{'Y9791':yt,'X9799':xt},'CPU_local_Dclear_cases':cases,'observed_charge_producers_exact':charges,'all8_observed_headings':dict(directions),'charge_examples':examples,'observed_exec_instructions':valid,'actual_speed_rows':len(rows),'baseline045_byte_exact_files':exact,'policy_evidence':'Preserved04520k full run; current04610k connects nativeproducer before targetselection2F at14276', 'policy2F_level1_rows':len(ps),'intercept_B_rows':len(br),'2F_actor_samples':len(speeds),'2F_samples_above_policy2_5_threshold':sum(v>2.5 for v in speeds),'2F_sample_speed_max':max(speeds),'meaning':'Nativecharge subtracts64 friction before replacing velocity highbytes from heading tables, retaining fractional lowbytes. Variable speed, not a fixed2.8 constant. Existing B policy uses6.25 squared threshold in intercept mode while observed2F samples can exceed2.5; this supports a selective slowdown-policy experiment, not sole-cause or wholeclear proof.','scope':'Same controller10k observation, first nativecart clear then2F level1 analysis. No gameplay logic/ROM edits or new natural fullclear claim.'}
 out.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','CPU_local_Dclear_cases','observed_charge_producers_exact','baseline045_byte_exact_files','intercept_B_rows','2F_samples_above_policy2_5_threshold']}))
if __name__=='__main__':main()