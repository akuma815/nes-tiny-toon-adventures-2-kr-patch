from pathlib import Path
import ast,hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 lua=R/'scripts/trace_water_controller157.lua';plan=R/'work/water157/run_plan.json';assert not lua.exists()and not plan.exists()
 report=R/'qa/reports/water157_bbox_model.json';v=json.loads(report.read_text('utf-8'));assert v['status']=='PASS_BOUNDED_NATIVE_COLLISION_BOX_COMPILER'and len(v['CPU_case_pairs'])==36
 old=R/'scripts/prepare_water_controller157.py';a=ast.parse(old.read_text('utf-8'))
 templates=[n.value.value for n in ast.walk(a)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='addition'for t in n.targets)and isinstance(n.value,ast.Constant)]
 assert len(templates)==1;addition=templates[0]
 # Retain the raw template's literal Lua backslash-n; never turn it into a newline.
 addition=addition.replace(chr(92)*2+'n',chr(92)+'n')
 tables='local profiles='+json.dumps(v['player_profiles'],separators=(',',':')).replace('[','{').replace(']','}')+'\nlocal shapes='+json.dumps(v['actor_shapes'],separators=(',',':')).replace('[','{').replace(']','}')+'\n'
 s=(R/'scripts/trace_water_damage154.lua').read_text('utf-8')+'\n'+tables+addition
 for quote in ["'",'"']:
  opened=False;esc=False
  for ch in s:
   if opened:
    assert ch not in '\r\n'
    if esc:esc=False
    elif ch=='\\':esc=True
    elif ch==quote:opened=False
   elif ch==quote:opened=True
  assert not opened
 assert 'emu.write('not in s and 'loadSavestate'not in s
 lua.write_text(s,'utf-8')
 error=R/'qa/reports/water157_v1_preflight_error.json';assert not error.exists()
 error.write_text(json.dumps({'work':157,'status':'PRE_EXECUTION_RAW_TEMPLATE_ESCAPE_GUARD_REJECTED','v1_script_sha256':sha(old),'completed_model_sha256':sha(report),'model_CPU_case_pairs':36,'emulator_started':False,'cause':'v1 postprocessing converted valid literal Lua backslash-n in raw template into actual newline. Short-string guard rejected before writing Lua or launching emulator.','fix':'v2 reads raw template literal and retains backslash-n. Completed36CPU cases retained, no overwrite or rerun.'},indent=2)+'\n','utf-8')
 plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':157,'revision':'v2','observer_sha256':sha(lua),'geometry_report_sha256':sha(report),'fixed_prefix_input':'config/water_first_hazard_steer156.json','adaptive_start_frame':3300,'frames':9000,'scope':'Read-only native geometry, future constant-velocity controller hypothesis and complete input-poll log; natural completion not presumed','command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water157_controller049 --frames 9000 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_controller157.lua','input_evidence':'adaptive_inputs.csv records every final input poll; environment.input is fixed prefix only; later Lua callback overrides inherited fixed input.'},indent=2)+'\n','utf-8');print('PASS157 v2 short-string guard and36 frozen CPU pairs')
if __name__=='__main__':main()
