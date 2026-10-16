"""Completed048 runtime evidence; reject transient font mixing, no new execution."""
from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    out=R/'qa/reports/shortage127_observation.json';assert not out.exists()
    old,new=[R/p for p in ['qa/dialogue/context106_normal3047','qa/dialogue/shortage127_normal3048']]
    envs=[json.loads((d/'environment.json').read_text('utf-8')) for d in (old,new)]
    for d,e in zip((old,new),envs):
        assert e['exit_code']==0 and e['frames']==4200
        for f,h in e['files'].items():assert sha(d/f)==h
    for k in ['exe_sha256','lua_sha256','config_sha256','input','seed','seed_file_sha256','frames']:assert envs[0][k]==envs[1][k]
    ramdiff=collections.Counter();bounds=collections.Counter();pngs=[];samepng=0;oam=0
    for name in envs[0]['files']:
        if name.endswith('_ram.bin'):
            for i,(x,y) in enumerate(zip((old/name).read_bytes(),(new/name).read_bytes())):
                if x!=y:ramdiff[i]+=1
        elif name.endswith('_oam.bin'):assert (old/name).read_bytes()==(new/name).read_bytes();oam+=1
        elif name.endswith('.png'):
            box=ImageChops.difference(Image.open(old/name).convert('RGB'),Image.open(new/name).convert('RGB')).getbbox()
            if box:bounds[str(box)]+=1;pngs.append(name)
            else:samepng+=1
    assert len(pngs)==43 and samepng==259 and oam==302
    events=list(csv.DictReader((new/'menu_events.csv').open(encoding='utf-8',newline='')))
    events=[r for r in events if r['kind']=='exec' and 1900<int(r['frame'])<2800]
    decoded=[];m=json.loads((R/'build/dialogue_kr_poc_048/shortage_editorial_mapping.json').read_text('utf-8'))
    g={x['code']:x['char'] for x in m['glyphs']};g[0]=' '
    ppu=(new/'frame_02100_ppu.bin').read_bytes()
    for addr,line in zip((0x22a8,0x22e8),m['layout']):
        actual=''.join(g[v] for v in ppu[addr:addr+line['expanded_tiles']]);assert actual==line['desired'];decoded.append(actual)
    for frame,font in [(1800,196),(2100,226),(2700,196)]:
        r=(new/f'frame_{frame:05d}_ram.bin').read_bytes();p=(new/f'frame_{frame:05d}_ppu.bin').read_bytes()
        assert r[0xc6]==r[0x6f3]==font and r[0x7d0:0x7d3]==bytes([3,0,0])
        rom=(R/'build/dialogue_kr_poc_048/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert p[:0x800]==rom[0x40010+font*1024:0x40010+(font+2)*1024]
    result={'work':127,'status':'REJECT048_TRANSIENT_FONT_LIFETIME','candidate048_sha256':envs[1]['rom_sha256'],'baseline047_historical_work106_sha256':envs[0]['rom_sha256'],'new_run_frames':4200,'baseline_reused_not_rerun':True,'declared_runtime_files_each':len(envs[1]['files']),'same_PNG':samepng,'different_PNG':len(pngs),'RGB_difference_bounds':dict(bounds),'all_OAM_exact':oam,'RAM_difference_offsets':{f'{k:04X}':v for k,v in sorted(ramdiff.items())},'completed_shortage_lines':decoded,'native_exec_lifetime_rows':events,'direct_actual_images_reviewed':['frame_02010.png','frame_02100.png','frame_02700.png','frame_02004.png','frame_02007.png','frame_02604.png'],'direct_observation':'Complete2100 and possession2700 are readable, but2004 remaps still-visible prior fee glyphs before native clear;2604 remaps still-visible shortage glyphs back to shared196 before clear. These actual transient images are defects, not accepted row-local edits. Filename/frame timing is only local evidence; screenshot async limitation retained.','cause':'Native9F09→9417 at pre-clear06DF00 commits226/196 immediately. Post-clear9A7F→9417 at06DF03 is already called2008/2607. New fonts must remain inactive until this post-clear init.','adopted_build':'dialogue_kr_poc_047','candidate048_rejected':True,'human_approved':False,'ROM_CSV_changes_this_work':False,'limits':['No natural fullplay/hardware/PCM or human approval','Completed text and eventual font restore do not prove transition correctness','No new build/apply or claimed successful048 adoption'],'next_action':'Build049 with targeted slot29/2B pre-clear font selection deferral in bank2 helper, preserve pointer/native reader and post-clear initialization, then verify balanced CPU timing and actual transitions.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('native_exec_lifetime_rows','RGB_difference_bounds')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
