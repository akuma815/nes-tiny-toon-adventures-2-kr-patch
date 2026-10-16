from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/verify_intro144_v3.py';assert not p.exists()
 s=(R/'scripts/verify_intro144_v2.py').read_text('utf-8');assert "['MACRO_061C3'],0,0)"in s
 s=s.replace("['MACRO_061C3'],0,0)","['MACRO_061C3'],0,10)");p.write_text(s,'utf-8')
 p=R/'qa/reports/intro144_verifier_v2_observation.json';assert not p.exists()
 p.write_text(json.dumps({'work':144,'status':'VERIFIER_FAILED_BEFORE_REPORT','reason':'Assumed no-input intro final normal-ticket digits0; native cold boot initialized10. Both fresh047 and current049 frozen6000 RAM are10; read/NT/image/CHR checks had passed.','v3_fix':'Expected native default10; no changing runtime evidence or ROM, no input/seed introduced'},indent=2)+'\n','utf-8');print('prepared native-default10 final-state guard v3')
if __name__=='__main__':main()
