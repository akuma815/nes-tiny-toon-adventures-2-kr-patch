"""Audit the fixed title prototype, rebuild/apply, and sampled native runtime screens."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from title_codec import unpack
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    source_path=ROOT/manifest['path'];assert sha(source_path)==manifest['sha256']
    base=ROOT/'build/title_kr_ai_003';rom=base/'TinyToon2_title_kr_poc.nes'
    report=json.loads((base/'build_report.json').read_text(encoding='utf-8'))
    assert sha(rom)==report['output_sha256'];original=source_path.read_bytes();new=rom.read_bytes()
    writes=json.loads((base/'expected_writes.json').read_text(encoding='utf-8'));covered=set()
    for w in writes:
        pos=w['file_offset'];n=w['length'];owned=set(range(pos,pos+n))
        assert not covered&owned;covered|=owned
        assert original[pos:pos+n]==bytes.fromhex(w['expected_hex'])
        assert new[pos:pos+n]==bytes.fromhex(w['final_hex'])
    changed={i for i,(x,y) in enumerate(zip(original,new)) if x!=y}
    assert len(new)==len(original)==262160 and changed<=covered and len(changed)==3209
    assert new[:0x20010]==original[:0x20010],'PRG/header must remain identical'
    assert new[0x4249:0x424b]==original[0x4249:0x424b]
    assert sha(ROOT/'build/title_kr_ai_003_rebuild/TinyToon2_title_kr_poc.nes')==sha(rom)
    assert sha(ROOT/'qa/title/패치 적용 검증 003/TinyToon2_title_kr_applied.nes')==sha(rom)
    assert sha(ROOT/'build/title_roundtrip_001/TinyToon2_title_roundtrip.nes')==manifest['sha256']
    assert sha(ROOT/'workspace/translation/text_ja.csv')=='934e13de97c024d4ee86420e0a2238447585b155ad1b21f2ffeef0d7b644d21f'
    first=json.loads((ROOT/'qa/reports/initial_session_20261004.json').read_text(encoding='utf-8'))['first_game_references']
    for p,h in first.items():assert sha(ROOT.parent/p)==h,p
    asset=ROOT/'extracted/title/title_20261004_001'
    old_nt=[(asset/f'{n}_nametable.bin').read_bytes() for n in ('main','ribbon')]
    specs=((0x24939,0x249a7,0x2000),(0x249a7,0x24a0b,0x2800));new_nt=[]
    for start,end,address in specs:
        d,_=unpack(new[start:end]);new_nt.append(bytes(d[address+i] for i in range(1024)))
    mask=Image.open(base/'title_allowed_pixel_mask.png').convert('L')
    runs=[];total_title=0;total_other=0
    for original_id,new_id,frames,input_frame in (('baseline_attract_002','title_kr_ai_003_attract',5400,-1),('baseline_game_001','title_kr_ai_003_start',3000,720)):
        a=ROOT/'qa/screenshots'/original_id;b=ROOT/'qa/title'/new_id
        env=json.loads((b/'environment.json').read_text(encoding='utf-8'))
        old_env=json.loads((a/'environment.json').read_text(encoding='utf-8'))
        assert env['exit_code']==0 and env['rom_sha256']==sha(rom) and env['frames']==frames
        assert env['exe_sha256']==old_env['exe_sha256'] and env['config_sha256']==old_env['config_sha256']
        assert env['input']['start_frame']==old_env['input']['start_frame']==input_frame
        # The only Lua change from the historic baseline is dropping its unusable frame1 snapshot.
        new_lua=(b/'capture_survey_used.lua').read_text(encoding='utf-8')
        old_lua=(a/'capture_survey_used.lua').read_text(encoding='utf-8')
        assert new_lua==old_lua.replace('frame==1 or ','') or new_lua==old_lua
        rows=[]
        for p in sorted(b.glob('frame_*.png')):
            q=a/p.name;assert q.exists() and q.stat().st_size>0
            old_ppu=(a/(p.stem+'_ppu.bin')).read_bytes();new_ppu=(b/(p.stem+'_ppu.bin')).read_bytes()
            title=all(old_ppu[address:address+1024]==nt for nt,(_,_,address) in zip(old_nt,specs))
            old=Image.open(q).convert('RGB');current=Image.open(p).convert('RGB')
            assert old.size==current.size==(256,240)
            pts=[(i%256,i//256) for i,v in enumerate(ImageChops.difference(old,current).get_flattened_data()) if v!=(0,0,0)]
            outside=sum(not mask.getpixel(xy) for xy in pts)
            assert outside==0,(p,outside)
            if pts:
                assert title,'Unexpected change outside a verified title layout'
                assert all(new_ppu[address:address+1024]==nt for nt,(_,_,address) in zip(new_nt,specs))
                total_title+=1
            else:total_other+=1
            assert old_ppu[0x3f00:0x3f20]==new_ppu[0x3f00:0x3f20]
            assert (a/(p.stem+'_oam.bin')).read_bytes()==(b/(p.stem+'_oam.bin')).read_bytes()
            rows.append({'frame':int(p.stem[6:]),'changed_pixels':len(pts),'outside_title_mask':outside,'oam_equal':True,'palette_equal':True})
        assert len(rows)==(46 if frames==5400 else 26)
        assert rows[-1]['changed_pixels']==0
        runs.append({'path':str(b.relative_to(ROOT)),'sample_count':len(rows),'frames':frames,'input_frame':input_frame,'comparisons':rows})
    actual=Image.open(ROOT/'qa/title/title_kr_ai_003_attract/frame_00720.png').convert('RGB')
    assert ImageChops.difference(actual,Image.open(base/'title_static_preview.png').convert('RGB')).getbbox() is None
    contact=Image.new('RGB',(1032,4*260),'#242424');draw=ImageDraw.Draw(contact)
    for i,(a,b,frame,label) in enumerate((('baseline_attract_002','title_kr_ai_003_attract',720,'Cold boot title / frame720'),('baseline_attract_002','title_kr_ai_003_attract',3360,'Natural title reentry / frame3360'),('baseline_game_001','title_kr_ai_003_start',1080,'Start input -> home / frame1080'),('baseline_attract_002','title_kr_ai_003_attract',1920,'Attract dialogue / frame1920'))):
        draw.text((4,i*260+3),label+' : ORIGINAL | KOREAN TITLE',fill='white')
        for x,path in ((0,ROOT/'qa/screenshots'/a),(520,ROOT/'qa/title'/b)):
            im=Image.open(path/f'frame_{frame:05d}.png').convert('RGB').resize((512,480),Image.Resampling.NEAREST)
            # Preserve the native aspect ratio in each compact comparison cell.
            contact.paste(im.resize((256,240),Image.Resampling.NEAREST),(x+128,i*260+20))
    contact.save(ROOT/'qa/title/title_kr_ai_003_comparison.png')
    actual.resize((1024,960),Image.Resampling.NEAREST).save(ROOT/'qa/title/title_kr_ai_003_actual_4x.png')
    final={'status':'PASS for title prototype checks only','source_sha256':manifest['sha256'],'rom_sha256':sha(rom),'ips_sha256':sha(base/'TinyToon2_title_kr_poc.ips'),
        'static':{'expected_write_count':len(writes),'changed_bytes':len(changed),'prg_header_unchanged':True,'original_png_roundtrip_identity':True,'translation_csv_unchanged':True,'first_game_reference_hashes_unchanged':True},
        'build_apply':{'rebuild_same_sha256':True,'actual_ips_apply_same_sha256':True,'apply_path_contains_korean_and_spaces':True},
        'emulator':{'runs':runs,'total_sample_count':total_title+total_other,'title_changed_samples':total_title,'fully_identical_samples':total_other,'outside_title_pixel_differences':0,'static_preview_matches_native_frame720':True},
        'direct_visual':'Record manual review separately in docs/POC_TITLE.md after inspecting the actual frame and comparison sheet.',
        'not_performed':['full playthrough','all-scene shared-tile QA','physical console','audio listening','user final design approval','public release','Naver cafe upload']}
    (ROOT/'qa/reports/title_kr_ai_003_validation.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in final.items() if k!='emulator'},ensure_ascii=True,indent=2));print('Compared samples:',total_title+total_other,'title:',total_title,'fully identical:',total_other)
if __name__=='__main__':main()
