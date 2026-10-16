"""Fresh047 intro +049 unaffected page paths; reuse pinned historical observer/input."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    plan=R/'work/pages130/run_plan.json';assert not plan.exists();plan.parent.mkdir(parents=True,exist_ok=True)
    jobs=[{'label':'intro047','runner':'run_dialogue_qa.py','rom':'047','frames':6000,'output':'pages130_intro047','extra':['--start','-1']}]
    for label,baseline in [('gate','gate091_castle047'),('tour','booth039_tour'),('booth','train043_booth_regression'),('credits','train043_credits_regression')]:
        d=R/'qa/dialogue'/baseline;e=json.loads((d/'environment.json').read_text('utf-8'))
        assert sha(d/'capture_survey_used.lua')==e['lua_sha256'] and sha(d/'inputs_used.json')==e['input']['file_sha256']
        extra=['--inputs',str(d/'inputs_used.json')]
        if label=='credits':
            runner='run_credits_seed_qa_v3.py';script=R/'scripts/trace_credits_seed_v3.lua'
            assert sha(script)==e['lua_sha256'];assert sha(d/'seed_used.json')==e['seed_file_sha256']
            extra+=['--seed',str(d/'seed_used.json'),'--script',str(script)]
        else:runner='run_menu_qa.py';extra+=['--script',str(d/'capture_survey_used.lua')]
        jobs.append({'label':label,'runner':runner,'rom':'049','frames':e['frames'],'output':f'pages130_{label}049','baseline':baseline,'baseline_ROM_sha256':e['rom_sha256'],'baseline_environment_sha256':sha(d/'environment.json'),'extra':extra})
    for job in jobs:assert not (R/'qa/dialogue'/job['output']).exists()
    plan.write_text(json.dumps({'work':130,'already_completed049_intro':'qa/dialogue/pages130_intro049','jobs':jobs,'scope':'Global helper regression. All scripts read-only except declared historical credits root/selector seed. Source and user emulator preserved.'},indent=2)+'\n','utf-8')
    for job in jobs:
        args=[sys.executable,str(R/'scripts'/job['runner']),'--rom',str(R/f'build/dialogue_kr_poc_{job["rom"]}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/'qa/dialogue'/job['output']),'--frames',str(job['frames']),*job['extra']]
        print('START '+job['label'],flush=True);p=subprocess.run(args,cwd=R,capture_output=True)
        (plan.parent/(job['label']+'_runner_stdout.txt')).write_bytes(p.stdout);(plan.parent/(job['label']+'_runner_stderr.txt')).write_bytes(p.stderr)
        print('COMPLETE '+job['label']+' exit='+str(p.returncode),flush=True);assert p.returncode==0,p.stderr.decode('utf-8','replace')
if __name__=='__main__':main()
