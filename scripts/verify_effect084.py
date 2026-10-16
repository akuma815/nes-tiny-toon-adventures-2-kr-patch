"""Work84 bounded native61 consumer evidence; zero observations is not unused proof."""
from pathlib import Path
import hashlib,json,csv
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 report=R/'qa/reports/effect084_survey.json';assert not report.exists()
 m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));src=R/m['path'];rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes';assert sha(src)==m['sha256']
 b=rom.read_bytes();assert b[0x4f410:0x4f810]==src.read_bytes()[0x2f410:0x2f810]
 baseline=R/'qa/dialogue/stop081_coaster046';results={}
 for name in ['effect084_coaster046','effect084_menu046']:
  q=R/'qa/dialogue'/name;env=json.loads((q/'environment.json').read_text('utf-8'));assert env['rom_sha256']==sha(rom)
  for n,h in env['files'].items():assert sha(q/n)==h,n
  reads=list(csv.DictReader((q/'effect_pattern_reads.csv').open()));top=list(csv.DictReader((q/'effect_top_banks.csv').open()));writers=list(csv.DictReader((q/'effect_bank_writes.csv').open()))
  assert not reads and not [x for x in top if int(x['pow_OAM_count'])] and not list(q.glob('effect_actual*.png'))
  entries=[]
  for p in q.glob('frame_*.png'):
   if (baseline/p.name).exists():
    tag=p.stem
    for suffix in ['.png','_ppu.bin','_ram.bin','_oam.bin','_mapping.csv']:
     z=q/(tag+suffix);assert z.read_bytes()==(baseline/z.name).read_bytes();entries.append(z.name)
  assert entries
  assert b[0x25e47:0x25e4b]==bytes.fromhex('a93d8538')
  native61=[x for x in writers if x['value']=='3D'];assert any(x['pc']=='9E3B'and x['PRG_relative']=='25E3B'for x in native61)
  results[name]={'frames':env['frames'],'observation_start':2400 if 'coaster'in name else 1400,'ROM_pattern61_read_rows':len(reads),'top_observations':len(top),'visible_pow_OAM_hits':0,'baseline_byte_exact_files':len(entries),'native_bank61_writes':native61,'environment_sha256':sha(q/'environment.json')}
 result={'work':84,'status':'PASS_BOUNDED_SURVEY_NO_EDIT','source_sha256':sha(src),'ROM046_sha256':sha(rom),'native61_preserved':True,'font61_current_file_range':[0x4f410,0x4f810],'static_text_candidate':'POW','consumer_connected':False,'runtime':results,'interpretation':'Bank61 selection proved, but glyph rendering not observed in these menu/coaster intervals. Not proof of global unused art. No translation/preservation approval inferred.','scope':'Read-only static candidate and controller-only bounded observation; no ROM/CSV edits or new apply. End-frame historical scan is weaker than top mapping plus real PPU callbacks.'}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()