from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=R/'work/gate140/run_plan.json';assert not plan.exists();plan.parent.mkdir(parents=True,exist_ok=True)
 d=R/'qa/dialogue/gate094_normal50047';e=json.loads((d/'environment.json').read_text('utf-8'))
 script=R/'scripts/trace_branch_seed_v1.lua';assert sha(script)==sha(d/'capture_survey_used.lua')==e['lua_sha256']
 for n,k in [('inputs_used.json','input'),('seed_used.json','seed')]:
  expected=e['input']['file_sha256']if k=='input'else e['seed_file_sha256'];assert sha(d/n)==expected
 args=[sys.executable,str(R/'scripts/run_branch_seed_qa.py'),'--rom','build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes','--output','qa/dialogue/gate140_normal50049','--frames','9000','--inputs',str(d/'inputs_used.json'),'--seed',str(d/'seed_used.json'),'--script',str(script)]
 plan.write_text(json.dumps({'work':140,'baseline':'gate094_normal50047','baseline_environment_sha256':sha(d/'environment.json'),'command':args,'scope':'New049 normal50 castle branch; initial1000 normal ticket digits50, controller thereafter; no savestate/ROM edits.'},indent=2)+'\n','utf-8')
 p=subprocess.run(args,cwd=R,capture_output=True)
 (plan.parent/'runner_stdout.txt').write_bytes(p.stdout);(plan.parent/'runner_stderr.txt').write_bytes(p.stderr)
 assert p.returncode==0,p.stderr.decode('utf-8','replace');print('PASS gate140 9000 frames')
if __name__=='__main__':main()
