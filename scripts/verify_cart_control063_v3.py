"""Actual cart held/edge reads, native player stores, source-preserved movement/control."""
from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_control063_validation_v3.json';assert not out.exists();rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();src=json.loads((R/'manifests/source_rom.json').read_text());original=R/src['path'];assert sha(original)==src['sha256'];assert original.read_bytes()[0x10010:0x18010]==blob[0x30010:0x38010];frozen=chunks=screens=0;runs=[]
 for name in ('cart063_control_probe','cart063_control_probe_v2'):
  q=R/'qa/dialogue'/name;e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==4800 and(q/'trace_complete.txt').read_text()=='4800';assert e['rom_sha256']==sha(rom)
  for p,h in e['files'].items():assert sha(q/p)==h;frozen+=1
  ps=list(q.glob('frame_*.png'));screens+=len(ps)
  for p in ps:
   pp=(q/(p.stem+'_ppu.bin')).read_bytes()
   for x in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
    if x['kind']!='chr':continue
    a=int(x['cpu_or_ppu_address'],16);off=int(x['relative_offset'],16);assert pp[a:a+1024]==blob[0x40010+off:0x40410+off];chunks+=1
  r=list(csv.DictReader((q/'world_phase.csv').open()));assert any(x['phase']=='0D'and x['life']=='02'for x in r if x['root']=='04');assert r[-1]['phase']=='05'and r[-1]['life']=='02'and r[-1]['gold']=='00'and r[-1]['history']=='00';runs.append({'QA':name,'frames':4800,'screens':len(ps),'native_life3_to2_death_and_restart':True,'natural_clear':False})
 a=R/'qa/dialogue/cart063_control_probe';b=R/'qa/dialogue/cart063_control_probe_v2';assert(a/'world_phase.csv').read_bytes()==(b/'world_phase.csv').read_bytes()
 for p in b.glob('frame_*_ram.bin'):assert p.read_bytes()==(a/p.name).read_bytes()
 rows=list(csv.DictReader((b/'cart_joy_reads.csv').open()));game=[x for x in rows if int(x['PRG_relative'],16)<0x3e000];assert game and all(0x30000<=int(x['PRG_relative'],16)<0x32000 for x in game)
 for x in game:
  addr=int(x['address'],16);off=int(x['PRG_relative'],16);assert blob[16+off-2:16+off]==bytes((0xa5,addr))
 masks={}
 for f,button,value in ((3390,'right',1),(3540,'down',4),(3690,'left',2),(3840,'up',8),(3990,'a',128),(4140,'b',64)):
  raw=(b/f'frame_{f:05d}_ram.bin').read_bytes();assert raw[0x52]==value;masks[button]=value
 writes=list(csv.DictReader((b/'cart_position_writes.csv').open()));player=[x for x in writes if x['address']in ('0470','04A0')];assert player
 for x in player:
  off=int(x['PRG_relative'],16);addr=int(x['address'],16);op=blob[16+off-3];operand=int.from_bytes(blob[16+off-2:16+off],'little');assert op in (0x8d,0x9d,0xee,0xce)
  actual=operand+(int(x['x'],16)if op==0x9d else 0);assert actual==addr
 directions=json.loads((R/'work/cart_control_001/native_direction_table.json').read_text());assert len(directions)==8
 report={'work':63,'status':'PASS_CONSUMER_MAPPING','scope':'Two4.8k controller-only cartprobes, held/edge actualreads and directplayer stores tied to preserved nativecode; no naturalclear','ROM_SSOT_changes':0,'source_and_043_unchanged':True,'runtime_frozen_files':frozen,'screens':screens,'mapped_CHR_1K_chunks_exact':chunks,'runs':runs,'same_world_and_all_RAM_V1_V2':True,'held_input_RAM52_masks':masks,'game_joy_read_consumers':dict(collections.Counter(x['pc']for x in game)),'game_joy_read_count':len(game),'native_controller_banks38_39_and_movement3A_3B_32K_byteexact_sha256':hashlib.sha256(blob[0x30010:0x38010]).hexdigest(),'player_actor0_integer_store_count':len(player),'player_store_nextPCs':dict(collections.Counter(x['pc']for x in player)),'native_direction_lookup':directions,'rejected_initial_models':['Coordinate INC/DEC RMW writes accounted inV3; originalV1/V2 assertion histories preserved','Initialall-player-stores-indexedX0 assumption failed; nativefixedEE3F/EE5D are directSTA withtemporaryX. Opcode-based V2 preserves those cases','RAMF7/F8 were not heldinput; observedRAM52 masks and runtime readcallbacks corrected mapping','First3A/3B scan was commonmotionbank, not heldinputconsumer38','InitialADA0 candidate linearlisting contains unvalidated prefix; only actualSTA addresses andruntime-heldreadentry instructions accepted','047E/F/049E/F initialwatches concern otheractors/fraction field, not directplayer integer position'],'source_geometry':'Native movement stores Xint0470+index, Xpage0480, Yfraction0490, Yint04A0, Ypage04B0; common code uses mixed Xpage240/Ypage256. Use actualcoordinates in nextpolicy, not screenshot inference','direct_visual':'V1 cart3390/3840/4500 viewed; no globalhuman visualreview','limits':['Natural playerdeath/restart only, no nativebonus/Gold/fullclear','A/B semantic effects not completelycharacterized yet; source masks/branches recorded, no manualgameguide claim','No actorcharacter-name assertion, audio/listening/hardware/finalhumanapproval'],'next_action':'Run controller-only pursuit policy using native player/enemy objectcoordinates and verified direction table, logging everypolicy decision; no state/life/currency edits.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_frozen_files','screens','mapped_CHR_1K_chunks_exact','game_joy_read_count','player_actor0_integer_store_count')},indent=2))
if __name__=='__main__':main()
