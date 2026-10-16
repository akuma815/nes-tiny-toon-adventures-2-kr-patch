"""Work100 actual current047 bank116 decoration; bound HOWTO label consumption."""
from pathlib import Path
import json,csv,hashlib,collections
from PIL import Image,ImageChops
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def rows(p):return list(csv.DictReader((R/p).open(encoding='utf-8')))
def main():
 out=R/'qa/reports/candidate100_runtime.json';assert not out.exists();meta=j('manifests/source_rom.json');src=(R/meta['path']).read_bytes();assert sha(R/meta['path'])==meta['sha256'];rom=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256']
 baseline='qa/dialogue/candidate100_baseline047';probe='qa/dialogue/candidate100_probe047';ea=j(baseline+'/environment.json');eb=j(probe+'/environment.json');assert ea['exit_code']==eb['exit_code']==0 and ea['rom_sha256']==eb['rom_sha256']==sha(rom)and ea['input']==eb['input']and ea['frames']==eb['frames']==4200
 for name,e in ((baseline,ea),(probe,eb)):
  for p,h in e['files'].items():assert sha(R/name/p)==h
  assert e['exe_sha256']==sha(R/'tools/mesen-2.1.1/Mesen.exe')and e['config_sha256']==sha(R/'config/mesen_survey.json')
 comparable=[p for p in ea['files']if p!='capture_survey_used.lua'];assert len(comparable)==1658
 for p in comparable:assert ea['files'][p]==eb['files'][p],p
 pngs=sum(p.endswith('.png')for p in comparable);assert pngs==275
 bank=rows(probe+'/candidate100_bank35.csv');chosen=[x for x in bank if x['value']=='74'];assert len(chosen)==1 and chosen[0]['frame']=='1574'and chosen[0]['observed_pc']=='9E30'and chosen[0]['PRG_relative']=='25E30'
 top=rows(probe+'/candidate100_top.csv');assert len(top)==1060
 for x in top:assert x['RAM35']=='74'and x['CHR0800']=='1D000'and x['CHR0C00']=='1D400'and x['backgroundPatternAddr']=='0'and x['label_NT_top_cells']=='0'
 pattern=rows(probe+'/candidate100_pattern.csv');assert len(pattern)==16896 and {x['classification']for x in pattern}=={'border81_positive_control'};frames=collections.defaultdict(list)
 for x in pattern:
  a=int(x['ppu_address'],16);relative=int(x['CHR_relative'],16);assert 0x810<=a<0x820 and relative==0x1d010+a-0x810 and int(x['value'],16)==src[0x20010+relative]and x['count']=='1';assert32=32<=int(x['first_scanline'])<=39;assert assert32 and x['first_scanline']==x['last_scanline'];frames[int(x['frame'])].append(x)
 assert set(frames)==set(range(1578,2634))and all(len(x)==16 for x in frames.values())
 # The observed palette is the private Mesen preset; source pixel decode and
 # captured native PPU palette are used together, not a hardware color claim.
 colors={0x0f:(0,0,0),0x27:(234,158,34),0x20:(255,254,255),0x17:(153,78,0),0x07:(86,29,0),0x10:(173,173,173)};v=j('qa/reports/candidate099_bank_nt.json');high={x['NT']:x['tile']for x in v['panel_high_cells']};captures=[]
 for x in top:
  if not x['capture_tag']:continue
  tag=x['capture_tag'];ppu=(R/probe/(tag+'_ppu.bin')).read_bytes();assert ppu[0x800:0x1000]==src[0x3d010:0x3d810];assert{a:ppu[a]for a in range(0x2000,0x23c0)if ppu[a]>=128}==high
  row,col=4,2;addr=0x2000+row*32+col;assert ppu[addr]==0x81;attr=ppu[0x23c0+(row//4)*8+col//4];shift=((row%4)//2)*4+((col%4)//2)*2;grp=(attr>>shift)&3;assert grp==0 and ppu[0x3f00:0x3f04]in[bytes.fromhex(x)for x in('0f272017','0f0f0f0f','0f171007')]
  bits=decode(src[0x3d020:0x3d030]);expected=Image.new('RGB',(8,8));expected.putdata([colors[ppu[0x3f00+grp*4+b]]for b in bits]);pic=R/probe/f"frame_{int(x['frame']):05d}.png";crop=Image.open(pic).convert('RGB').crop((16,32,24,40));assert ImageChops.difference(crop,expected).getbbox()is None
  captures.append({'frame':int(x['frame']),'tag':tag,'NT':addr,'tile_hex':'81','source_ROM_offset':0x3d020,'RGB_box':[16,32,24,40],'native_palette_hex':ppu[0x3f00:0x3f04].hex()})
 assert len(captures)==35
 result={'work':100,'status':'PASS_CURRENT047_HOWTO_BANK_POSITIVE_CONTROL','source_sha256':meta['sha256'],'ROM047_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'controller_only':True,'frames_each':4200,'baseline_probe_native_files_byte_exact':len(comparable),'whole_screen_pairs_exact':pngs,'bank35_producer_observed':chosen,'top_mapping_frames':len(top),'top_label90_96_cell_observations':0,'real_border_pattern_read_rows':len(pattern),'real_border_consumption_frames':len(frames),'real_border_pattern_values_source_exact':True,'HOWTO_label_pattern_reads_observed':0,'top_captures':captures,'source_CHR0800_2KiB_NT_high267_and_border_RGB_exact':35,'direct_visual_review_frames':[1800],'ROM_CSV_edited':False,'limits':['One bounded controller-only coaster menu/start route; no global-unused/all engines/all label consumer proof','RAM write callback logs advancedPC and pre-write RAM;1574observedPC9E30 corresponds to nativeSTA35 at9E2E','Top samples atFD9E are not endframe mappings; 1060top and1056consumption frames have different event boundaries','No human preservation approval/full natural game/all corpus/hardware/PCM/final language/release claim'],'next_action':'Trace native PAUSE120121 supply across remaining softwareCHR shadow registers and distinguish code constants from data motifs, without equivalent zero runtime loops.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k!='top_captures'},indent=2))
if __name__=='__main__':main()