"""Correct report-only wording, preserving the original calculated cases and file."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'qa/reports/cart114_analysis.json';q=R/'qa/reports/cart114_analysis_v2.json';assert not q.exists()
 r=json.loads(p.read_text('utf-8'));n=len(r['erratum088']['classification_changed_events']);assert n==77
 r['erratum088']['sign_changed_events']=n
 r['erratum088']['net_toward_count_change']=-1
 r['erratum088']['net_away_count_change']=1
 r['limits'][1]='Burst-start direction is not actual collision direction. Near-contact samples use input-polled positions and are not observed native9C9C/9D53 execution.'
 r['limits'][2]='Correct pit coordinate changes77event signs; net totals shift by one toward->away. Not an identified sole timeout cause.'
 r['metadata_erratum']={'original_report':p.relative_to(R).as_posix(),'original_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reason':'Original calculations/list of77changedevents were correct; limit sentence incorrectly described net1countshift as one event. New report clarifies77sign flips and actual callback address. Original preserved.'}
 q.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n','utf-8');print('Corrected metadata,77sign flips/net count shift1; no CPU/emulator rerun')
if __name__=='__main__':main()
