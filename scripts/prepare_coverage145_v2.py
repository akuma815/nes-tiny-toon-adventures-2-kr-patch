from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/make_coverage145_v2.py';assert not p.exists()
 s=(R/'scripts/make_coverage145.py').read_text('utf-8')
 assert 'len(read)==30 and len(missing)==24'in s
 s=s.replace('len(read)==30 and len(missing)==24','len(read)==31 and len(missing)==23');p.write_text(s,'utf-8')
 p=R/'qa/reports/coverage145_v1_observation.json';assert not p.exists()
 p.write_text(json.dumps({'work':145,'status':'LEDGER_VERIFIER_FAILED_BEFORE_OUTPUT','reason':'Manual estimated union count24main+6macro missed an observed main unit; actual union25main+6macro=31. All46 main units have bounded current presence.','fix':'Use measured union31/missing23 with catalog set54 checked; do not change evidence inputs or ROM/CSV'},indent=2)+'\n','utf-8');print('prepared measured evidence cardinality145v2')
if __name__=='__main__':main()
