"""Same native moving-sign reproduction: glyph-only changes, motion/other scenes exact."""
from pathlib import Path
import csv,json
from PIL import Image,ImageChops
from extract_title_png import decode
from seal_nonplay171 import R,sha

def main():
    out=R/'qa/reports/moving_stop182_validation.json';assert not out.exists()
    a=R/'qa/dialogue/moving_stop181_050';b=R/'qa/dialogue/moving_stop182_051';dirs=[a,b];env=[json.loads((p/'environment.json').read_text('utf-8')) for p in dirs]
    assert all(e['exit_code']==0 and e['frames']==5000 for e in env)
    for k in ['exe_sha256','lua_sha256','config_sha256','frames','input','intervention']:assert env[0][k]==env[1][k]
    for p,e in zip(dirs,env):
        for f,h in e['files'].items():assert sha(p/f)==h,(p.name,f)
    old=(R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes').read_bytes();new=(R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes').read_bytes();base=0x4b810
    assert old[:0x40010]==new[:0x40010]
    for n in ['TinyToon2_dialogue_kr_poc.nes','TinyToon2_dialogue_kr_poc.ips']:assert (R/'build/dialogue_kr_poc_051'/n).read_bytes()==(R/'build/moving_stop182_rebuild051'/n).read_bytes()
    masks={}
    for code in range(40,52):
        x=decode(old[base+code*16:base+(code+1)*16]);y=decode(new[base+code*16:base+(code+1)*16]);masks[code]={(k%8,k//8):(u,v) for k,(u,v) in enumerate(zip(x,y)) if u!=v}
        assert all({u,v}=={1,2} for u,v in masks[code].values())
    frames=sorted(a.glob('frame_*.png'));changes=[];totalpixels=0
    for f in frames:
        tag=f.stem
        for suffix in ['_ram.bin','_oam.bin','_mapping.csv','_state.txt']:assert (a/(tag+suffix)).read_bytes()==(b/(tag+suffix)).read_bytes(),(tag,suffix)
        assert (a/(tag+'_ppu.bin')).read_bytes()==(b/(tag+'_ppu.bin')).read_bytes() # HUD-time dump has sprite font63; top epoch separately below
        im,jm=[Image.open(p/f.name).convert('RGB') for p in dirs];box=ImageChops.difference(im,jm).getbbox()
        if not box:continue
        assert box[3]<190,(tag,box)
        points=[(x,y,im.getpixel((x,y)),jm.getpixel((x,y))) for y in range(box[1],box[3]) for x in range(box[0],box[2]) if im.getpixel((x,y))!=jm.getpixel((x,y))]
        assert all({u,v}=={(0,0,0),(188,190,0)} for x,y,u,v in points)
        oam=(a/(tag+'_oam.bin')).read_bytes();pred={};color={1:(188,190,0),2:(0,0,0)}
        for i in range(0,256,4):
            yy,c,attr,xx=oam[i:i+4]
            if c not in (0x69,0x6b,0x6d,0x6f,0x71,0x73):continue
            assert attr&3==1
            local=(c&0xfe)-64
            for half in (0,1):
                for (x,y),(u,v) in masks[local+half].items():
                    dy=half*8+y;dx=x
                    if attr&0x40:dx=7-dx
                    if attr&0x80:dy=15-dy
                    pred[(xx+dx,yy+1+dy)]=(color[u],color[v])
        offsets=[(dx,dy) for dx in range(-2,3) for dy in range(-2,3) if all(pred.get((x-dx,y-dy))==(u,v) for x,y,u,v in points)]
        assert offsets,(tag,box,'pixel not moving STOP field')
        changes.append({'frame':int(tag[6:]),'changed_pixels':len(points),'OAM_to_completed_screenshot_offsets':offsets});totalpixels+=len(points)
    assert len(changes)==90 and any(c['frame']==4200 for c in changes)
    maps=list(csv.DictReader((a/'sprite_top_mapping.csv').open(encoding='utf-8')))
    assert (a/'sprite_top_mapping.csv').read_bytes()==(b/'sprite_top_mapping.csv').read_bytes()
    chunks=0
    for row in maps:
        n=int(row['frame']);addr=int(row['address'],16);off=int(row['relative_offset'],16)
        for p,r in [(a,old),(b,new)]:assert (p/f'sprite_top_{n:05d}_ppu.bin').read_bytes()[addr:addr+1024]==r[0x40010+off:0x40410+off]
        chunks+=1
    assert any(row['frame']=='4200' and row['address']=='1400' and row['relative_offset']=='0B800' for row in maps)
    result={'work':182,'status':'PASS_MOVING_STOP051_NATIVE_GLYPH_ONLY_FIX','ROM_sha256':sha(R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'screens':len(frames),'changed_screens':len(changes),'unchanged_screens':len(frames)-len(changes),'changed_pixels_exact_native_OAM_fields_and_RGB':totalpixels,'pixel_proofs':changes,'all_RAM_OAM_NT_palette_mapper_CPU_PPU_state_equal':True,'HUD_full_RGB_equal':True,'sprite_top_CHR_chunks_each_match_named_ROM':chunks,'PRG_header_IRQ_input_timing_unchanged':True,'independent_ROM_IPS_rebuild_exact':True,'fixed_STOP_graphics224225_unchanged':True,'intervention':'Controller-only5000frame coldboot; no life seed/state load/forced PC or ROM/RAM writes. User copied saved-state replay was a different cart scene and not used as bug reproduction.','limits':['not full train/game playthrough','new glyph appearance not final human art approval','does not claim old crossbuild saved-state compatibility'],'cause':'Old fixed STOP scope covered BGCHR68/69->224/225 only; moving board uses separate spriteCHR46 local40..51 and was untranslated. User clarification identified moving variant.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items() if k!='pixel_proofs'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
