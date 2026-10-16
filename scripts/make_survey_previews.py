"""Create evidence contact sheets from the accepted original-ROM captures."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def sheet(name,items):
    out=Image.new('RGB',(3*512,2*512),'#202020');draw=ImageDraw.Draw(out)
    for i,(folder,frame,label) in enumerate(items):
        path=ROOT/'qa/screenshots'/folder/f'frame_{frame:05d}.png'
        im=Image.open(path);im.load();assert im.size==(256,240)
        x=i%3*512;y=i//3*512
        draw.text((x+8,y+8),label+f' / FRAME {frame}',fill='white')
        out.paste(im.resize((512,480),Image.Resampling.NEAREST),(x,y+32))
    out.save(ROOT/'qa/screenshots'/name)
sheet('baseline_intro_contact_sheet.png',[
 ('baseline_attract_002',720,'TITLE'),('baseline_attract_002',1080,'INTRO 1'),
 ('baseline_attract_002',1200,'INTRO 2'),('baseline_attract_002',1920,'LETTER'),
 ('baseline_attract_002',2520,'BUSTER'),('baseline_attract_002',2760,'MONTANA')])
sheet('baseline_home_contact_sheet.png',[
 ('baseline_game_001',840,'HOME ENTRY'),('baseline_game_001',960,'HOME TEXT START'),
 ('baseline_game_001',1080,'HOME PROMPT'),('baseline_game_001',1200,'HOME WAIT'),
 ('baseline_game_001',1440,'HOME WAIT'),('baseline_game_001',3000,'HOME WAIT')])
print('Two contact sheets created from accepted baseline captures.')
