"""Fresh037 intro and coaster regression, whole pixels/RAM/PPU/OAM and exact IRQ."""
import json,csv,hashlib
from pathlib import Path
from PIL import Image,ImageChops
from verify_gate_font_tag import env
ROOT=Path(__file__).resolve().parents[1]
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 prior=(ROOT/'build/dialogue_kr_poc_036/TinyToon2_dialogue_kr_poc.nes').read_bytes();rom=(ROOT/'build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes').read_bytes();checks=[]
 for ref,new in [('stage_lower036_intro','credits037_intro'),('stage_lower036_coaster','credits037_coaster')]:
  a,b=env(ref,prior),env(new,rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));old=ROOT/'qa/dialogue'/ref;current=ROOT/'qa/dialogue'/new;images=sorted(current.glob('frame_*.png'));assert images and [p.name for p in images]==[p.name for p in sorted(old.glob('frame_*.png'))]
  for f in images:
   assert ImageChops.difference(Image.open(f).convert('RGB'),Image.open(old/f.name).convert('RGB')).getbbox() is None,f.name
   for suffix in ('_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):assert f.with_name(f.stem+suffix).read_bytes()==(old/(f.stem+suffix)).read_bytes(),(f.name,suffix)
  a,b=env(ref+'_irq',prior),env(new+'_irq',rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));a=rows(ROOT/f'qa/dialogue/{ref}_irq/irq_phase.csv');b=rows(ROOT/f'qa/dialogue/{new}_irq/irq_phase.csv');assert a==b
  checks.append({'reference':ref,'candidate':new,'whole_images_RAM_PPU_OAM_mapping_equal':len(images),'actual_IRQ_rows_including_values_equal':len(a)})
 out={'status':'PASS','work':37,'build':'dialogue_kr_poc_037','prior_build':'dialogue_kr_poc_036','ROM_sha256':hashlib.sha256(rom).hexdigest(),'checks':checks,'whole_screens_equal':sum(x['whole_images_RAM_PPU_OAM_mapping_equal'] for x in checks),'actual_IRQ_rows_equal':sum(x['actual_IRQ_rows_including_values_equal'] for x in checks),'scope':'Fresh complete title/nine intro paragraphs plus controller-only coaster regression; no fullplay/audio/reset/savestate/physical console claim'};p=ROOT/'qa/reports/credits037_regression.json';p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
