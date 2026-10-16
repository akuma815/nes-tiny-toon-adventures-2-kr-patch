from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'scripts/seal_irq136_v2.py';obs=R/'qa/reports/irq136_handoff_v1_observation.json';assert not p.exists() and not obs.exists()
s=(R/'scripts/seal_irq136.py').read_text('utf-8')
s=s.replace("人검토'.replace('人검토','사람검토')+'false/현재","사람검토false/현재").replace("외부게시없음.\\n\\n'","외부게시없음.\\n\\n'''")
s=s.replace('변경:scripts/trace_irq136.lua','인계v1 작성기의triplequote종료누락으로문서쓰기전SyntaxError가발생했고바로뒤감사는manifest부재로중단했다. v1과관측을보존하고v2에서종료인용을교정했다. 검증/runtime자료변경없음.\n\n변경:scripts/trace_irq136.lua')
s=s.replace("R/'qa/reports/irq136_validation.json',","R/'qa/reports/irq136_validation.json',R/'qa/reports/irq136_handoff_v1_observation.json',")
compile(s,str(p),'exec');p.write_text(s,'utf-8')
obs.write_text(json.dumps({'work':136,'status':'HANDOFF_SCRIPT_SYNTAX_FAILED_BEFORE_OUTPUT','reason':'Triplequoted detailed document terminator missing in seal v1. No docs/manifest were written. Following audit failed due missing manifest. v2 closes text correctly; original script preserved.'},indent=2)+'\n','utf-8')
