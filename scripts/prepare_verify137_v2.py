from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'scripts/verify_irqdma137_v2.py';obs=R/'qa/reports/irqdma137_verifier_v1_observation.json';assert not p.exists() and not obs.exists()
s=(R/'scripts/verify_irqdma137.py').read_text('utf-8').replace("int(y['cycle'])-int(x['cycle'])==-2","int(y['cycle'])-int(x['cycle']) in [-2,2]")
s=s.replace('four_two_cycle_earlier_DMC_reads','four_two_cycle_shifted_DMC_reads').replace('4 sample reads are2cycles earlier','2 sample reads are2cycles earlier and2 are2cycles later').replace('two_cycle_earlier_reads','two_cycle_shifted_reads')
s=s.replace('assert len(timediffs)==4','assert len(timediffs)==4 and collections.Counter(int(x[\'049\'][\'cycle\'])-int(x[\'047\'][\'cycle\'])for x in timediffs)=={-2:2,2:2}')
compile(s,str(p),'exec');p.write_text(s,'utf-8');obs.write_text(json.dumps({'work':137,'status':'FAILED_NEGATIVE_ONLY_TIME_DELTA_GUARD','reason':'All4 differing read cycles were incorrectly required to be-2 from two inspected examples. Complete data are two-2 and two+2. v2 records both signs and verifies their exact histogram. Probe/ROM unchanged.'},indent=2)+'\n','utf-8')
