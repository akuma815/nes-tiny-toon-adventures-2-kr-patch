from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'scripts/verify_dma135_v2.py';obs=R/'qa/reports/dma135_verifier_v1_observation.json';assert not p.exists() and not obs.exists()
s=(R/'scripts/verify_dma135.py').read_text('utf-8').replace('.read_text();debug=',".read_text('utf-8');debug=").replace("NesDebugger.cpp').read_text()","NesDebugger.cpp').read_text('utf-8')")
p.write_text(s,'utf-8');obs.write_text(json.dumps({'work':135,'status':'SOURCE_READ_ENCODING_FAILED_BEFORE_REPORT','reason':'UTF8 pinned C++ source was read with Windows defaultcp949. v2 reads both source files explicitlyUTF8. No probe/ROM changes.'},indent=2)+'\n','utf-8')
