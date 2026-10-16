from verify_reader_pair142 import R,sha,rows,native_lines
from PIL import Image,ImageChops
import collections,json,hashlib
def main():
 out=R/'qa/reports/shortagereader150_validation.json';assert not out.exists()
 ds=[R/'qa/dialogue'/f'shortagereader150_{z}'for z in ['047','049']]
 env=[json.loads((d/'environment.json').read_text('utf-8'))for d in ds]
 for k in ['source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256']:assert env[0][k]==env[1][k],k
 assert env[1]['frames']==4200 and env[1]['seed']['frame']==1000
 roms=[(R/f'build/dialogue_kr_poc_{z}/TinyToon2_dialogue_kr_poc.nes').read_bytes()for z in ['047','049']]
 historic=[R/'qa/dialogue'/n for n in ['context106_normal3047','clear129_normal3049']]
 hp=R/'qa/reports/clear129_validation.json';prior=json.loads(hp.read_text('utf-8'))
 assert prior['candidate049_sha256']==env[1]['rom_sha256']
 # Frozen129 declared SHA is pinned by its successfully audited asset manifest.
 manifest=json.loads((R/'manifests/clear129_assets.json').read_text('utf-8'))
 assert manifest['files']['qa/reports/clear129_validation.json']==sha(hp)
 reused=[]
 for d,e,rom,h in zip(ds,env,roms,historic):
  assert e['exit_code']==0 and (d/'trace_complete.txt').read_text()=='4200'and hashlib.sha256(rom).hexdigest()==e['rom_sha256']
  he=json.loads((h/'environment.json').read_text('utf-8'))
  for f,digest in e['files'].items():assert sha(d/f)==digest
  count=0
  for f,digest in he['files'].items():
   assert sha(h/f)==digest
   if not f.startswith('frame_'):continue
   if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
   else:assert (d/f).read_bytes()==(h/f).read_bytes()
   count+=1
  reused.append({'directory':h.relative_to(R).as_posix(),'all_snapshot_artifacts_exact':count})
 A,B=[rows(d/'prg_text_reads.csv')for d in ds];assert len(A)==len(B)==190
 cat=json.loads((R/'extracted/text/table_20261004_001/text_tokens.json').read_text('utf-8'))
 groups=collections.defaultdict(list);cycles=collections.Counter();changed=[];fontdiff=[]
 for x,y in zip(A,B):
  assert {k:v for k,v in x.items()if k not in ['cycles','value','active_font']}=={k:v for k,v in y.items()if k not in ['cycles','value','active_font']}
  f=int(y['PRG_relative_offset'],16)+16
  assert roms[0][f]==int(x['value'],16)and roms[1][f]==int(y['value'],16)
  us=[u for u in cat['units']if u['file_offset']+0x20000<=f<u['end_exclusive']+0x20000];assert len(us)==1;u=us[0]
  p=0x24010+int(y['pc'],16)-0x8000
  assert y['pc']in ['9395','9362','92CF']and roms[0][p-2:p]==roms[1][p-2:p]==bytes.fromhex('b1 06')
  if x['value']!=y['value']:
   assert u['entry_id']=='MAIN_0590C';changed.append({'source_relative_offset':f-u['file_offset']-0x20000,'old_hex':x['value'],'new_hex':y['value'],'frame':int(y['frame'])})
  if x['active_font']!=y['active_font']:
   assert x['active_font']=='C4'and y['active_font']=='E2'and 2009<=int(y['frame'])<=2601 and y['native_id']in ['29','2B'];fontdiff.append({'frame':int(y['frame']),'unit':u['entry_id'],'native_id':y['native_id']})
  groups[u['entry_id']].append({'frame':int(y['frame']),'source_relative_offset':f-u['file_offset']-0x20000,'value_hex':y['value'],'native_id_hex':y['native_id'],'reader_PC':y['pc'],'active_font':int(y['active_font'],16)})
  cycles[int(y['cycles'])-int(x['cycles'])]+=1
 required=['MAIN_0590C','MAIN_05929','MACRO_061FA']
 for unit in required:
  u=next(z for z in cat['units']if z['entry_id']==unit)
  assert set(z['source_relative_offset']for z in groups[unit])==set(range(u['end_exclusive']-u['file_offset'])),unit
 mapping=json.loads((R/'build/dialogue_kr_poc_049/shortage_editorial_mapping.json').read_text('utf-8'))
 assert roms[1][0x2590c:0x25920].hex()==mapping['body_hex']
 lines=native_lines(roms[1],0x29);assert [z.hex()for z in lines]==[x['expanded_hex']for x in mapping['layout']]
 complete=[];chunks=0;changedpng=[];equalpng=0
 for f in sorted(n for n in env[1]['files']if n.endswith('.png')):
  stem=f[:-4];frame=int(stem[6:]);pp=(ds[1]/(stem+'_ppu.bin')).read_bytes();ram=(ds[1]/(stem+'_ram.bin')).read_bytes()
  if ram[0x6f3]==226 and all(pp[0x22a8+i*64:0x22a8+i*64+len(z)]==z for i,z in enumerate(lines)):complete.append(frame)
  for z in rows(ds[1]/(stem+'_mapping.csv')):
   if z['kind']!='chr':continue
   addr=int(z['cpu_or_ppu_address'],16);off=int(z['relative_offset'],16)
   assert pp[addr:addr+1024]==roms[1][0x40010+off:0x40410+off];chunks+=1
  diff=ImageChops.difference(Image.open(ds[0]/f).convert('RGB'),Image.open(ds[1]/f).convert('RGB'))
  if diff.getbbox():
   assert 2019<=frame<=2604;diff.paste(0,(80,179,152,187));assert diff.getbbox()is None;changedpng.append(frame)
  else:equalpng+=1
 assert complete and len(changed)==10 and len(fontdiff)==41 and equalpng==261 and len(changedpng)==41
 lifetime=[]
 for frame,font in [(2004,196),(2100,226),(2604,226),(2700,196)]:
  ram=(ds[1]/f'frame_{frame:05d}_ram.bin').read_bytes();assert ram[0xc6]==ram[0x6f3]==font and ram[0x7d0:0x7d3]==bytes([3,0,0]);lifetime.append({'snapshot':frame,'font':font})
 result={'work':150,'status':'PASS_BOUNDED049_CHANGED_SHORTAGE_ACTUAL_READER','ROM_sha256':env[1]['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'historical_snapshot_identity':reused,'frozen129_report_sha256':sha(hp),'frames_each':4200,'actual_PRG_data_reads_each':190,'actual_read_units':dict(groups),'full_unit_byte_coverage':required,'intended_source_byte_changes':changed,'intended_reader_font_changes':fontdiff,'source_read_cycle_deltas':dict(cycles),'complete_shortage_NT_frames':complete,'expected_lines':[z.hex(' ')for z in lines],'actual_CHR_chunks_match_ROM':chunks,'PNG_exact':equalpng,'only_changed_second_row_PNGs':changedpng,'font_lifetime_snapshots':lifetime,'human_approved':False,'release_eligible':False,'limits':['Initial normal3 seed, not natural currency earning/full gameplay','Historical129 protects full snapshot state with explicit RNG/CPU differences; observer adds actual source discrimination','No new build/apply/reset/state/audio/hardware or human final review','Whole global corpus and natural route closure remain pending']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:v for k,v in result.items()if k not in ['actual_read_units','intended_reader_font_changes','complete_shortage_NT_frames','only_changed_second_row_PNGs']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
