"""Run the unchanged native DE91 tile consumer offline and compare actual A274 return queries."""
from pathlib import Path
import json,csv,hashlib,collections
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def classify(blob,xp,xl,yp,yl,level):
 m=Memory(blob);m.banks=[0x38,0x39,0x3e,31]
 m.ram[0x25]=1;m.ram[0x79]=level
 for a,v in ((0x10,xp),(0x11,xl),(0x12,yp),(0x13,yl),(0x1fe,255),(0x1ff,192)):m.ram[a]=v
 c=MPU(memory=m);c.sp=0xfd;c.pc=0xde91
 for _ in range(3000):
  if c.pc==0xc100:return m.ram[0x10]
  c.step()
 raise AssertionError(hex(c.pc))
def main():
 out=R/'qa/reports/cart_geometry066_validation.json';assert not out.exists();q=R/'qa/dialogue/cart066_geometry'
 e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and(q/'trace_complete.txt').read_text()=='6000'
 for p,h in e['files'].items():assert sha(q/p)==h
 blob=(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes').read_bytes();cache={}
 rows=list(csv.DictReader((q/'cart_tile_queries.csv').open()));assert rows
 for r in rows:
  assert r['PRG_relative']=='32274' and r['course']=='01'
  k=tuple(int(r[x])for x in ('x_page','x_low','y_page','y_low','level'))
  if k not in cache:cache[k]=classify(blob,*k)
  assert cache[k]==int(r['class']),(k,r,cache[k])
 grid=[[classify(blob,x//240,x%240,y//256,y%256,0)for x in range(8,480,16)]for y in range(8,512,16)]
 mp=R/'work/cart_geometry_001/native_level0_classes_v2.json';assert not mp.exists();mp.parent.mkdir(exist_ok=True)
 mp.write_text(json.dumps({'ROM_SHA256':hashlib.sha256(blob).hexdigest(),'level':0,'tile_step':16,'sample_origin':[8,8],'width':30,'height':32,'classes':grid,'consumer':'DE91 -> DE26 -> DDC2, temporary canonical32; class conversion DE5E; actual return A274','limits':'Class0 outside the closed arena is also0; must restrict to inside-wall connected component. Only level0.'},indent=2)+'\n')
 pits=[(x*16,y*16)for y,row in enumerate(grid)for x,v in enumerate(row)if v==15]
 assert pits==[(112,240),(128,240),(112,256),(128,256)],pits
 actors=list(csv.DictReader((q/'cart_actors.csv').open()));a0=[r for r in actors if r['index']=='0'];states=collections.Counter(r['state']for r in a0)
 report={'work':66,'status':'NATIVE_TILE_CONSUMER_MATCH','ROM_SSOT_changes':0,'runtime_files':len(e['files']),'actual_queries':len(rows),'unique_queries_offline_exact':len(cache),'native_levels_observed':sorted(set(int(r['level'])for r in rows)),'class_counts':dict(collections.Counter(int(r['class'])for r in rows)),'level0_pit_tiles_top_left':pits,'level0_pit_bounds':[112,240,144,272],'player_states':dict(states),'actor_rows':len(actors),'native_fall_consumer':'9869..988D queries four offsets +/-8; all class0F ->0430=4; F17E/F187. A051 only checks nonzero velocity, not pit.','validation_scope':'Offline native CPU routine against actual read-only runtime tile queries; no actual RAM intervention. Disassembly table bytes must not be treated as instructions.','next_action':'Use the confirmed arena and pit geometry to route behind an enemy and apply momentum-controlled charge/release input.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
