"""Exact real post-A008 NMI font data and physical mapping; endframe IRQ differs."""
import json,csv,hashlib
from pathlib import Path
from verify_gate_font_tag import env
R=Path(__file__).resolve().parents[1]
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8')))
def main():
 old=(R/'build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes').read_bytes();new=(R/'build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes').read_bytes();a,b=env('booth038_font_probe',old),env('booth039_font_probe',new);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));x=R/'qa/dialogue/booth038_font_probe';y=R/'qa/dialogue/booth039_font_probe';aa,bb=rows(x/'head_font_samples.csv'),rows(y/'head_font_samples.csv');assert len(aa)==len(bb)>0
 changed=0
 for a,b in zip(aa,bb):
  assert all(a[k]==b[k] for k in ('frame','pc','x','scanline','dot','cycles','file'));assert a['pc']=='FD92' and a['x']=='00';assert a['font']=='7C' and (a['chr0'],a['chr1'])==('1F000','1F400');assert (x/a['file']).read_bytes()==old[0x5f010:0x5f810]
  if b['font']=='CC':assert (b['chr0'],b['chr1'])==('33000','33400') and (y/b['file']).read_bytes()==new[0x73010:0x73810];changed+=1
  else:assert b['font']=='7C' and (b['chr0'],b['chr1'])==('1F000','1F400') and (y/b['file']).read_bytes()==new[0x5f010:0x5f810]
 assert changed>0
 out={'status':'PASS','work':42,'build':'dialogue_kr_poc_039','ROM_sha256':hashlib.sha256(new).hexdigest(),'actual_post_A008_NMI_font_samples':len(aa),'actual_booth_font204_samples':changed,'earlier_native_font124_control_samples':len(aa)-changed,'native_current_CHR_pairs':[[124,125],[204,205]],'full_PPU0000_07FF_font_bytes_equal_selected_ROM':True,'exact_sample_PC_X_frame_scanline_dot_cycles_equal':True,'samples':bb,'scope':'Read-only execution callbackFD92 X0 after mapper storeFD90 completed; actual source124/new204 font0000/0400 before later IRQ lower-font switch; earlier shared124 also checked unchanged','limits':['Not an endframe font sample; those snapshots correctly show lower IRQ font','Controller-only2000 frames, no RAM/ROM/state writes; fullplay not claimed']};(R/'qa/reports/booth039_top_font_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='samples'},indent=2))
if __name__=='__main__':main()
