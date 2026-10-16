"""Read-only actual ride/HUD survey. Screenshot and IRQ dumps have distinct epochs."""
import json,hashlib
from pathlib import Path
from PIL import Image
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));s=(R/m['path']).read_bytes();r=(R/'build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(s)==m['sha256'];q=R/'qa/dialogue/hud039_live_coaster';p=(q/'hud_live_04200_ppu.bin').read_bytes();im=Image.open(q/'frame_04200.png').convert('RGB');assert p[:0x800]==r[0x5f010:0x5f810]==s[0x3f010:0x3f810];assert p[0x2f00:0x3000]==p[0x2b00:0x2c00]
 colors={0:(0,0,0),1:(0,0,0),2:(247,216,165),3:(183,30,123)};bad=[];protected=0
 for y in range(190,213):
  sy=y+5
  for x in range(20,236):
   row,col=sy//8,x//8;t=p[0x2c00+row*32+col];a=p[0x2fc0+(row//4)*8+col//4];assert (a>>((row%4//2)*4+(col%4//2)*2))&3==3;v=decode(p[t*16:t*16+16])[(sy%8)*8+x%8]
   if im.getpixel((x,y))!=colors[v]:bad.append([x,y,t,v,list(im.getpixel((x,y)))])
   if not 224<=x<232:assert im.getpixel((x,y))==colors[v];protected+=1
 assert len(bad)==3 and all(x[2]==0x78 for x in bad)
 # Full last-counter tile matches previous value9: screenshot precedes the dump.
 bits=decode(p[0x79*16:0x7a*16]);assert all(im.getpixel((224+x,195+y))==colors[bits[y*8+x]] for y in range(8) for x in range(8))
 labels=[('LIFE','체력',[0x22,0x23,0x24],3),('SCORE','점수',list(range(0x27,0x2c)),3),('TIME','시간',[0x7c,0x7d,0x7e],3),('PTS.','점',[0x7a,0x7b],2),('TICKET','티켓',[0x30,0x31,0x32],2),('G.TICKET','금티켓',[0x3c,0x3d,0x3e,0x3f],3)]
 routes=[]
 for ride in ('coaster','cart','train','water'):
  folder=R/f'qa/dialogue/game039_{ride}_survey';e=json.loads((folder/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['rom_sha256']==sha(r);states=[]
  for f in sorted(folder.glob('frame_*_ram.bin')):
   b=f.read_bytes()
   if b[0x18]==4:states.append({'frame':int(f.stem.split('_')[1]),'root':b[0x18],'substate':b[0x19],'head_font':b[0x34],'IRQ_selector':b[0x40]})
  assert states;routes.append({'ride':ride,'frames':e['frames'],'gameplay_samples':len(states),'first_gameplay':states[0],'last_gameplay':states[-1],'IRQ_selectors':sorted({x['IRQ_selector'] for x in states}),'environment_sha256':sha((folder/'environment.json').read_bytes()),'natural_clear_or_full_playthrough':False})
 out=R/'extracted/graphics/hud_001';out.mkdir(exist_ok=False,parents=True);im.crop((16,188,240,216)).save(out/'source_actual_native.png');im.crop((16,188,240,216)).resize((1344,168),Image.Resampling.NEAREST).save(out/'source_actual_6x.png');(out/'source_font124_125.bin').write_bytes(p[:0x800]);(out/'source_NT_2F00.bin').write_bytes(p[0x2f00:0x3000])
 result={'work':43,'status':'PASS','source_sha256':sha(s),'adopted_ROM_sha256':sha(r),'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'routes':routes,'labels':[dict(zip(('source','draft_ko','codes','ink'),x)) for x in labels],'consumer':{'IRQ_CPU':0xfccf,'font_CPU':0xfce8,'font_immediate_file':0x3fcf9,'fine_y_CPU':0xfcd4,'fine_y_immediate_file':0x3fce5,'actual_post_IRQ_PC':0xfd08,'banks':[124,125],'source_CHR_file':[0x3f010,0x3f810],'expanded_CHR_file':[0x5f010,0x5f810],'NT':0x2f00,'NT_mirror':0x2b00,'native_raw_template_file':0xd182,'source_projection_dy':-5,'palette_group':3,'actual_colors':colors},'screenshot_epoch':{'native_projection_pixels':4968,'exact_excluding_last_counter_column':protected,'three_pixel_mismatch':bad,'previous_digit_79_full_cell_exact':True,'explanation':'endFrame screenshot precedes same-tag read-only IRQ/dump time update. This is not exact same-epoch all-HUD proof.'},'remaining_results':{'source_CHR_compressed_candidate':0x24a0b,'strings':['CONGRATULATIONS!','LIFE BONUS','CLEAR BONUS','TIME BONUS','NOW YOU GET','POINTS','YOUR POINTS'],'actual_consumer_unresolved':True},'changes':'No ROM/CSV edits. New surveys/scripts/extracted evidence/docs only.','limits':['Four controller-only ride samples, not completed playthroughs; train IRQ selector5 needs separate verification','Source captions have5 visible rows; Galmuri7 needs7. Proposed fineY0/header fonts changes panel geometry by2px, still unbuilt/unverified','Actual results consumer and all-game corpus remain unresolved','Theoretical work/hud_survey_001 candidate previews are analysis, not game evidence'],'next_action':'Build isolated font206/207 with7px Korean headers and fineY2→0; validate owned HUD geometry, all numeric/digit/hearts and exact outside pixels/IRQ cycles before adoption'}
 (out/'consumer.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'status':'PASS','work':43,'routes':routes,'projection_bad':bad,'ROM_unchanged':sha(r)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
