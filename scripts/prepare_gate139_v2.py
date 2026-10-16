from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/verify_gate139_v2.py';assert not p.exists()
 s=(R/'scripts/verify_gate139.py').read_text('utf-8')
 old=" assert [{k:r[k]for k in fields}for r in A]==[{k:r[k]for k in fields}for r in B]"
 new=""" assert len(A)==len(B)
 oldrom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 relocated=collections.Counter()
 for x,y in zip(A,B):
  assert {k:v for k,v in x.items()if k!='pc'}=={k:v for k,v in y.items()if k!='pc'}
  if x['pc']==y['pc']:continue
  assert x['kind']=='write' and (x['pc'],y['pc'],x['address']) in [('9613','964A','00C6'),('9616','964D','06F3'),('961C','9653','06F4')]
  po,pn=[0x4010+int(z['pc'],16)-0x8000 for z in [x,y]]
  assert oldrom[po-3:po]==rom[pn-3:pn] and oldrom[po-3]==0x8d
  relocated[x['pc']+'->'+y['pc']+'/'+x['address']]+=1"""
 assert old in s;s=s.replace(old,new).replace("'protected_menu_events_exact':len(B)","'protected_menu_events_except_verified_relocated_STA_PC_exact':len(B),'relocated_helper_write_PC_counts':dict(relocated)")
 p.write_text(s,'utf-8');print('prepared gate139 verifier v2')
if __name__=='__main__':main()
