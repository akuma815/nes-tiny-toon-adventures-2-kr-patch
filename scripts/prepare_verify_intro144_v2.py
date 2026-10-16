from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/verify_intro144_v2.py';assert not p.exists()
 s=(R/'scripts/verify_intro144.py').read_text('utf-8')
 s=s.replace("('961C','9653','0034')]","('961C','9653','0034'),('9673','96AA','06CF'),('9677','96AE','00C6'),('967A','96B1','06F3')]")
 s=s.replace("n=3 if x['address']=='06F3'else 2","n=3 if x['address']in ['06F3','06CF']else 2")
 p.write_text(s,'utf-8');print('prepared exact intro STORE relocation guards v2')
if __name__=='__main__':main()
