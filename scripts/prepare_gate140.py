from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 for src,dst in [('run_gate139.py','run_gate140.py'),('verify_gate139_v3.py','verify_gate140.py')]:
  p=R/'scripts'/dst;assert not p.exists();s=(R/'scripts'/src).read_text('utf-8')
  s=s.replace('139','140').replace('gold4','normal50').replace('GOLD4','NORMAL50')
  if dst.startswith('run_'):
   s=s.replace('initial1000 RAM7E0=4','initial1000 normal ticket digits50')
  else:
   s=s.replace("'writes':[{'address':2016,'value':4}]","'writes':[{'address':2000,'value':0},{'address':2001,'value':5},{'address':2002,'value':0}]")
   s=s.replace("last[0x7e0]==4 and list(last[0x7d0:0x7d3])==[0,1,0]","last[0x7e0]==0 and list(last[0x7d0:0x7d3])==[0,0,0]")
   s=s.replace("'final_gold':4,'final_normal':10","'final_gold':0,'final_normal':0")
   s=s.replace('Initial normal504 seed','Initial normal50 seed')
  p.write_text(s,'utf-8')
 print('prepared distinct normal50 branch140')
if __name__=='__main__':main()
