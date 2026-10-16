"""Verify declared native castle room6 diagnostic, not natural completion."""
from pathlib import Path
import csv,json,hashlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/castle111_validation.json';assert not out.exists()
 source=next((R/'original/rom').glob('*.nes'));current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
 assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
 assert sha(current)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 catalog=json.loads((R/'work/nt_consumers109/source_nt_cells.json').read_text('utf-8'))
 pair=[x for x in catalog if x['selector_hex']in['14','16']]
 source_data=source.read_bytes();current_data=current.read_bytes()
 assert source_data[0x3d810:0x3e010]==current_data[0x5d810:0x5e010]
 environments=[];files={};dirlist=[];native_fetch=[]
 for name,rom in [('source',source),('current047',current)]:
  p=R/'qa/dialogue'/f'castle111_{name}';dirlist.append(p);ep=p/'environment.json';env=json.loads(ep.read_text('utf-8'))
  assert env['exit_code']==0 and env['frames']==4800 and env['rom_sha256']==sha(rom)
  assert sha(p/'capture_survey_used.lua')==env['lua_sha256']
  assert(p/'trace_complete.txt').read_text()=='4800'
  for n,h in env['files'].items():assert sha(p/n)==h;files[(p/n).relative_to(R).as_posix()]=h
  files[ep.relative_to(R).as_posix()]=sha(ep)
  seed=rows(p/'seed_writes.csv');assert len(seed)==1 and seed[0]['address']=='07E0'and seed[0]['frame']=='1000'and seed[0]['after']=='04'
  inj=rows(p/'castle111_injection.csv');assert len(inj)==2
  assert[(x['frame'],x['address'],x['before'],x['after'])for x in inj]==[('4000','00A5','00','23'),('4000','0054','05','07')]
  events=[x for x in rows(p/'castle111_native.csv')if int(x['frame'])>=4000]
  assert[(x['frame'],x['pc'])for x in events[:3]]==[('4000','F5F8'),('4000','969C'),('4000','96ED')]
  assert events[2]['room']=='06'
  nt=[x for x in events if x['kind']=='NT_entry'and x['cpu_x']in['14','16']]
  assert[(x['frame'],x['cpu_x'],x['room'],x['body_font'])for x in nt]==[('4002','14','06','76'),('4002','16','06','76')]
  raw=(p/'frame_04005_ppu.bin').read_bytes()
  assert all(raw[int(a,16)]==v for z in pair for a,v in z['cells'].items())
  fetch=rows(p/'castle111_render_fetch.csv')
  relevant={tuple(x[k]for k in ['snapshot_frame','scanline','ppu_tile_base','CHR_relative_tile_base']):int(x['read_count'])for x in fetch if int(x['CHR_relative_tile_base'],16)//0x400 in [118,119]}
  assert relevant and {int(k[0])for k in relevant}=={4091,4121}
  native_fetch.append(relevant)
  mapped=0
  for mp in sorted(p.glob('frame_*_mapping.csv')):
   if int(mp.name[6:11])<4005:continue
   raw=(p/mp.name.replace('_mapping.csv','_ppu.bin')).read_bytes();data=rom.read_bytes();start=16+data[4]*0x4000
   for x in rows(mp):
    if x['kind']!='chr':continue
    a=int(x['cpu_or_ppu_address'],16);rel=int(x['relative_offset'],16)
    assert raw[a:a+0x400]==data[start+rel:start+rel+0x400];mapped+=1
  environments.append({'revision':name,'environment_sha256':sha(ep),'frame4005_original_NT14_16_cells_exact':2048,'native118_119_render_read_rows':len(relevant),'native118_119_render_reads':sum(relevant.values()),'native118_119_read_snapshot_frames':[4091,4121],'mapped_1KiB_CHR_exact_after4005':mapped,'intervention':env['intervention']})
 assert native_fetch[0]==native_fetch[1]
 original,currentdir=dirlist;rgb=[];ntuples=[];union=None
 for sp in sorted(original.glob('frame_*.png')):
  frame=int(sp.name[6:11]);cp=currentdir/sp.name
  if frame<4005:continue
  a=Image.open(sp).convert('RGB');b=Image.open(cp).convert('RGB');box=ImageChops.difference(a,b).getbbox()
  assert ImageChops.difference(a.crop((0,0,256,190)),b.crop((0,0,256,190))).getbbox()is None
  assert ImageChops.difference(a.crop((0,218,256,240)),b.crop((0,218,256,240))).getbbox()is None
  if box:union=box if union is None else(min(union[0],box[0]),min(union[1],box[1]),max(union[2],box[2]),max(union[3],box[3]))
  rgb.append({'frame':frame,'whole_difference_bbox':box,'outside_HUD_exact':True})
  sn=sp.with_name(sp.name.replace('.png','_ppu.bin')).read_bytes();cn=cp.with_name(cp.name.replace('.png','_ppu.bin')).read_bytes()
  assert sn[0x2000:0x3000]==cn[0x2000:0x3000];ntuples.append(frame)
 assert len(rgb)==107 and union==(20,190,236,217)
 historical=R/'qa/dialogue/gate094_gold4047';henv=json.loads((historical/'environment.json').read_text('utf-8'));pre=[]
 for p in sorted(currentdir.glob('frame_*')):
  if int(p.name[6:11])>=4000:continue
  old=historical/p.name
  if not old.exists():continue
  assert sha(old)==henv['files'][old.name] and p.read_bytes()==old.read_bytes();pre.append(p.name)
 report={'work':111,'status':'PASS_CONTROLLED_NATIVE_CASTLE_ROOM6_NT14_16_CONSUMER','source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'environments':environments,'source_current_native118_119_ROM_2KiB_exact':True,'source_current_native118_119_read_histogram_exact':True,'source_current_NT_pages_exact_after4005':len(ntuples),'source_current_RGB_outside_existing_HUD_exact':len(rgb),'source_current_whole_RGB_difference_union_bbox':union,'RGB_cases':rgb,'current047_pre_intervention_vs_frozen094_exact_files':len(pre),'pre_intervention_files':pre,'frozen_selected_files':files,'ROM_CSV_changes':False,'new_build_or_apply':False,'direct_assistant_scene_visual':{'performed':True,'images':['qa/dialogue/castle111_current047/frame_04092.png','qa/dialogue/castle111_current047/frame_04200.png'],'observation':'Castle boss craft/background seen; labels requiring translation not newly observed in these NT14/16 scene images. Human final approval remains pending.'},'limits':['Gold4 at1000 and A5=35/phase54=7 at4000 are controlled RAM injections; natural room traversal, boss clear and wholeplay not verified.','4005 NT14/16 full2048cells exact; later NT16 includes native HUD overwrite and is not expected to remain source compressed-template exact.','End-frame PNG uses previous filtered frame in this pinned environment; read log4091/4121 and captures4092/4122 align as established work107; no false same-frame RGB/font assertion.','CHR118/119 positive render reads recorded only for two selected frames; not all IRQ/transitions or all sprite effects.','47 HUD changes are established UI scope; outside HUD pixels exact does not imply entire original/current PNG equality.','Other NT1C supplier, dormant stage-select consumer and HOWTO/PAUSE/POW/global corpus remain pending.','No finalhuman/hardware/PCM/release/Cafe completion claim'],'next_action':'Bound native8025 source call sites and computed selector suppliers to investigate remaining source NT1C, without labelling it unused from immediate-motif absence.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:report[k]for k in ['status','environments','source_current_NT_pages_exact_after4005','source_current_RGB_outside_existing_HUD_exact','current047_pre_intervention_vs_frozen094_exact_files']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
