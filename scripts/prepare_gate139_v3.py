from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/verify_gate139_v3.py';assert not p.exists()
 s=(R/'scripts/verify_gate139_v2.py').read_text('utf-8').replace("('961C','9653','06F4')","('961C','9653','0034')")
 old="  assert oldrom[po-3:po]==rom[pn-3:pn] and oldrom[po-3]==0x8d"
 new="  n=3 if x['address']=='06F3' else 2\n  assert oldrom[po-n:po]==rom[pn-n:pn] and oldrom[po-n]==(0x8d if n==3 else 0x85)"
 assert old in s;s=s.replace(old,new);p.write_text(s,'utf-8')
 obs=R/'qa/reports/gate139_verifier_v2_observation.json';assert not obs.exists()
 obs.write_text(json.dumps({'work':139,'status':'VERIFIER_FAILED_BEFORE_REPORT','correction_to_v1_observation_reason':'Only helper write PC relocations changed. No live IRQ/idle value mismatch observed. V1 dictionary Counter counted tuples incorrectly; retain raw examples but do not use counts.','v2_reason':'Assumed all helper writes were absolute STA; C6/34 actually zero-page STA. Third changed address is0034, not06F4.','verified_observed_PC_counts':{'9613->964A/00C6':9,'9616->964D/06F3':12,'961C->9653/0034':4},'v3_fix':'Exact instruction bytes with correct2/3byte lengths plus address allowlist; no runtime or file mutation'},indent=2)+'\n','utf-8')
 print('prepared v3 opcode-length guard')
if __name__=='__main__':main()
