"""Recompute the native A-charge world-velocity mapping; older rawvector labels are preserved as errata."""
from pathlib import Path
import json,hashlib
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def main():
 out=R/'qa/reports/cart_axis071_cpu.json';assert not out.exists();rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();proof=json.loads((R/'work/cart_geometry_001/axis071_native_velocity_proof.json').read_text());assert hashlib.sha256(blob).hexdigest()==proof['ROM_sha256']
 for row in proof['cases']:
  heading=row['heading'];charge=row['charge'];m=Memory(blob);m.banks=[56,57,62,31];m.ram[0xa9]=charge&255;m.ram[0xaa]=charge>>8
  for i,a in enumerate((0x11,0x10,0x13,0x12)):m.ram[a]=m[0x99b0+heading*4+i]
  mask=proof['native_button_masks_by_heading'][str(heading)];assert m[0x99d0+mask]==heading*4
  c=MPU(memory=m);m.ram[0x1fe]=255;m.ram[0x1ff]=192
  for pc in(0xa088,0xa0d1):
   c.sp=0xfd;c.pc=pc
   for _ in range(3000):
    if c.pc==0xc100:break
    c.step()
   else:raise AssertionError(hex(c.pc))
  def sign(lo,hi):
   v=m.ram[lo]+256*m.ram[hi];return v-65536 if v>=32768 else v
  vx,vy=sign(0x4c0,0x4d0),sign(0x4e0,0x4f0);assert(vx,vy)==(row['world_vx_4C'],row['world_vy_4E'])
  assert m.ram[0xa9]==m.ram[0xaa]==0
 q=R/'qa/dialogue/cart063_control_probe_v2';a=(q/'frame_03330_ram.bin').read_bytes();b=(q/'frame_03360_ram.bin').read_bytes()
 def xy(a):return(a[0x470]+240*a[0x480],a[0x4a0]+256*a[0x4b0])
 assert a[0x52]==b[0x52]==1 and a[0x9b:0x9f]==b[0x9b:0x9f]==bytes([128,0,0,0])and xy(a)==(319,271)and xy(b)==(319,286)
 report={'work':71,'status':'NATIVE_WORLD_AXIS_MAPPING_PASS','ROM_SSOT_changes':0,'CPU_cases':len(proof['cases']),'actual_right_held_evidence':{'QA':'cart063_control_probe_v2','frames':[3330,3360],'held52':1,'position_before':xy(a),'position_after':xy(b),'first_vector_pair_Y_fraction':128,'second_vector_pair_X':0},'corrected_world_key_masks':{'right':4,'left':8,'down':1,'up':2,'down_right':5,'down_left':9,'up_right':6,'up_left':10},'scope':'40 offline nativecharge cases + bounded actualright-held displacement. First native99B0pair isY, secondX; logger4C X and4E Y correct. Older frozen63 rawvector axislabels and controller pursuit worldassumptions corrected only in new71 policy. No ROM input mapping edits.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
