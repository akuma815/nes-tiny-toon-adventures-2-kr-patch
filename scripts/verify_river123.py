"""Bind diagnostic ED OAM, physical pattern reads and actual PNG opaque pixels."""
from pathlib import Path
import csv,hashlib,json,collections
from PIL import Image,ImageChops
from analyze_pow_metasprites096 import run
from verify_dialogue_home import MPU
from extract_title_png import decode

R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))

def main():
    out=R/'qa/reports/river123_validation.json';assert not out.exists()
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
    src,rom=source.read_bytes(),current.read_bytes()
    assert src[0x2f410:0x2f810]==rom[0x4f410:0x4f810]
    datasets=[];files={};oams=[];results=[]
    for data,name in [(src,'river123_projection_source'),(rom,'river123_projection_current047')]:
        q=R/'qa/dialogue'/name;env=json.loads((q/'environment.json').read_text('utf-8'))
        assert env['exit_code']==0 and env['frames']==3300 and(q/'trace_complete.txt').read_text()=='3300'
        for n,h in env['files'].items():assert sha(q/n)==h;files[(q/n).relative_to(R).as_posix()]=h
        files[(q/'environment.json').relative_to(R).as_posix()]=sha(q/'environment.json')
        inj=rows(q/'river121_injection.csv');camera=rows(q/'river123_camera_writes.csv')
        assert [(x['address'],x['after'])for x in inj]==[('0069','0B'),('006D','F0')]
        assert [(x['address'],x['after'])for x in camera]==[('0068','01'),('006B','40'),('0069','0C'),('006D','80')]
        assert {x['frame']for x in inj+camera}=={'3000'}
        native=rows(q/'river121_native.csv');calls=collections.Counter(x['cpu_a']for x in native if x['pc']=='9643')
        assert calls['ED']==1 and calls['EE']==calls['EF']==0
        normalized=[]
        for x in native:
            x=dict(x);x['PRG_relative']=f"{int(x['PRG_relative'],16)%0x20000:05X}";normalized.append(x)
        fetch=rows(q/'river121_render_fetch.csv');assert len(fetch)==128
        assert {x['render_frame']for x in fetch}=={'3002'}
        m,c,discard,n=run(data,0xed,3)
        m[1]=64;m[2]=144;m[0x1fe:0x200]=bytes.fromhex('ffc0')
        c=MPU(memory=m);c.pc=0x9643;c.a=0xed;c.x=0;c.sp=0xfd;c.p=0x30
        steps=0
        while c.pc!=0xc100:c.step();steps+=1;assert steps<5000
        oam=bytes(m[0x200:0x200+c.x]);assert len(oam)==36
        ram=(q/'actor2write_0003_before_ram.bin').read_bytes()
        assert ram[0x200:0x224]==oam
        expected=collections.Counter();opaque=set()
        for i in range(0,len(oam),4):
            y,t,attr,x=oam[i:i+4];assert attr==2
            local=(t&0xfe)-0x80
            base=0xf400+local*16
            expected[f'{base:05X}']+=16;expected[f'{base+16:05X}']+=16
            raw=src[0x20010+base:0x20010+base+32]
            pixels=list(decode(raw[:16]))+list(decode(raw[16:]))
            for k,v in enumerate(pixels):
                if v:opaque.add((x+k%8,y+k//8+1))
        actual=collections.Counter()
        for x in fetch:actual[x['CHR_relative_tile_base']]+=int(x['read_count'])
        assert expected==actual and sum(actual.values())==288
        assert len(opaque)==518
        png=Image.open(q/'frame_03003.png').convert('RGB')
        assert all(png.getpixel(p)==(0,0,0)for p in opaque)
        ppu=(q/'frame_03003_ppu.bin').read_bytes()
        assert ppu[0x3f18:0x3f1c]==bytes.fromhex('070f0f0f')
        chunks=0
        for p in sorted(q.glob('frame_*_mapping.csv')):
            pp=(q/(p.stem.replace('_mapping','')+'_ppu.bin')).read_bytes();chrbase=16+data[4]*16384
            for x in rows(p):
                if x['kind']!='chr':continue
                a=int(x['cpu_or_ppu_address'],16);offset=int(x['relative_offset'],16)
                assert pp[a:a+1024]==data[chrbase+offset:chrbase+offset+1024];chunks+=1
        datasets.append((normalized,fetch));oams.append(oam)
        results.append({'directory':q.relative_to(R).as_posix(),'runtime_files':len(env['files']),
                        'native_ED_assembler_calls':1,'native_EE_EF_assembler_calls':0,
                        'shadow_OAM_36bytes_matches_native_CPU':True,'PPU_render_frame_label':3002,
                        'actual_pattern_read_rows':len(fetch),'actual_pattern_reads':288,
                        'native_ED_pattern_histogram_exact':dict(actual),
                        'PNG_frame_label':3003,'opaque_mask_pixels_RGB_black_exact':518,
                        'endframe_sprite_palette2_hex':'070F0F0F','mapped_1KiB_CHR_chunks_exact':chunks})
    assert datasets[0]==datasets[1] and oams[0]==oams[1]
    outside=[];exceptions=[]
    for frame in range(3003,3151,3):
        a=Image.open(R/f'qa/dialogue/river123_projection_source/frame_{frame:05d}.png').convert('RGB')
        b=Image.open(R/f'qa/dialogue/river123_projection_current047/frame_{frame:05d}.png').convert('RGB')
        equal=all(ImageChops.difference(a.crop(box),b.crop(box)).getbbox()is None
                  for box in [(0,0,256,190),(0,218,256,240)])
        (outside if equal else exceptions).append(frame)
    report={'work':123,'status':'PASS_CONTROLLED_ED_OAM_CHR_AND_ACTUAL_PNG_CONSUMER',
            'source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),
            'runs':results,'source_current_native_and_render_rows_exact':len(datasets[0][0]),
            'source_current_OAM_exact':oams[0].hex(),'outside_existing_HUD_RGB_equal_frames':outside,
            'outside_existing_HUD_RGB_exception_frames':exceptions,
            'coordinate_erratum122':'RAM01=64 is screen Y; RAM02=144 is screen X, as9643writes0200/0203. Previous122sprite_x/y labels and screen64/144 prose were swapped. Model bytes/cycles and explicit camera values unchanged; actual screen anchor is X144/Y64.',
            'frozen_files':files,'direct_assistant_scene_visual':False,
            'limits':['Six explicit condition/viewport writes once, source/current diagnostic. Native actor coordinates untouched; not natural late river scene or fullplay.',
                      'Positive consumer is course3 stageED, not common18/19 POW. EE/EF actual assembly not observed here.',
                      'PNG3003 opaque518pixels match OAM/CHR and loggedrender3002 in this local case; no universal screenshot timestamp guarantee.',
                      'Endframe palette2 is allblack for opaque colors; intended natural palette/lifecycle not established. No inference of ROM/color fault or final object name.',
                      'No new ROM build/apply or CSV change, no human translation/preservation approval.'],
            'release_eligible':False}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(report['status'],'outsideHUD RGB equal',len(outside),'exceptions',len(exceptions))

if __name__=='__main__':main()
