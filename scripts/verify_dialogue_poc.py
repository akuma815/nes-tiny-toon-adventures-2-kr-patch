"""Independent serialized-data and native sampled-screen audit for dialogue002."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def expand(raw):
    lines=[[]];pos=0
    while pos<len(raw):
        b=raw[pos];pos+=1
        if b==0xff:break
        if b==0xfe:lines.append([])
        elif b==0xfd:
            n=raw[pos];pos+=1;assert n>0;lines[-1].extend([0]*n)
        else:assert 0<b<0x7f;lines[-1].append(b)
    return lines,pos
def main():
    r=ROOT;folder=r/'build/dialogue_kr_poc_002';rom_path=folder/'TinyToon2_dialogue_kr_poc.nes'
    manifest=json.loads((r/'manifests/source_rom.json').read_text(encoding='utf-8'));source_path=r/manifest['path']
    assert sha(source_path)==manifest['sha256'];source=source_path.read_bytes();rom=rom_path.read_bytes()
    report=json.loads((folder/'build_report.json').read_text(encoding='utf-8'));assert sha(rom_path)==report['output_sha256']
    assert len(rom)==270352 and rom[4:6]==bytes((8,17))
    assert sha(r/'build/dialogue_kr_poc_002_rebuild/TinyToon2_dialogue_kr_poc.nes')==sha(rom_path)
    assert sha(r/'qa/dialogue/한글 패치 적용 002/TinyToon2_dialogue_applied.nes')==sha(rom_path)
    writes=json.loads((folder/'expected_writes.json').read_text(encoding='utf-8'));owned=set()
    for w in writes:
        p=w['file_offset'];n=w['length'];region=set(range(p,p+n));assert not owned&region;owned|=region
        if w.get('kind')=='append':assert p==len(source)
        else:assert source[p:p+n]==bytes.fromhex(w['expected_hex'])
        assert rom[p:p+n]==bytes.fromhex(w['final_hex'])
    changed={i for i,(x,y) in enumerate(zip(source,rom)) if x!=y}|set(range(len(source),len(rom)))
    assert changed<=owned
    assert rom[0x36810:0x37010]==source[0x36810:0x37010]
    title=(r/'build/title_kr_ai_003/TinyToon2_title_kr_poc.nes').read_bytes()
    assert rom[0x20010:0x40010]==title[0x20010:0x40010]
    assert rom[0x55a9:0x5609]==source[0x55a9:0x5609] and rom[0x5625:0x5a28]==source[0x5625:0x5a28]
    assert rom[0x61b1:0x61ff]==source[0x61b1:0x61ff]
    original,old_end=expand(source[0x5609:0x5625]);new,new_end=expand(rom[0x5609:0x5625])
    assert old_end==new_end==28 and [len(x) for x in original]==[len(x) for x in new]==[18,17]
    # Identical command positions and argument values; literal bytes are all nonzero/<7F.
    for i in range(28):
        if source[0x5609+i] in (0xfd,0xfe,0xff):assert rom[0x5609+i]==source[0x5609+i]
    assert rom[0x560a]==6 and rom[0x5619]==7
    glyphs=json.loads((folder/'glyph_mapping.json').read_text(encoding='utf-8'));mapping=glyphs['mapping'];reverse={v:k for k,v in mapping.items()}
    decoded='\n'.join(''.join(' ' if b==0 else reverse[b] for b in line).strip() for line in new)
    assert decoded==report['text']
    for g in glyphs['glyphs']:
        raw=rom[0x40010+g['code']*16:0x40010+(g['code']+1)*16];assert raw.hex()==g['chr_hex']
        independently_decoded=[((raw[y]>>(7-x))&1)+2*((raw[8+y]>>(7-x))&1) for y in range(8) for x in range(8)]
        assert set(independently_decoded)<={0,2} and any(independently_decoded)
    assert rom[0x40010+0x7a*16:0x40010+0x7b*16]==bytes(16)
    old_rows=list(csv.DictReader((r/'backups/translation/text_ja_before_dialogue_001.csv').open(encoding='utf-8-sig',newline='')))
    rows=list(csv.DictReader((r/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')))
    protected=('entry_id','reference_ids','file_offset','end_exclusive','source_tokens','raw_hex','raw_sha256','source_sha256')
    assert [[v[k] for k in protected] for v in rows]==[[v[k] for k in protected] for v in old_rows]
    assert sum(v['status']=='draft' for v in rows)==1 and sum(bool(v['translation_ko']) for v in rows)==1
    mask=Image.new('L',(256,240))
    for y0 in (116,132):
        for y in range(y0,y0+8):
            for x in range(32,224):mask.putpixel((x,y),255)
    runs=[];total=0;changed_samples=0
    for old_id,new_id in (('qa/dialogue/title_reference_attract','qa/dialogue/poc002_attract'),('qa/title/title_kr_ai_003_start','qa/dialogue/poc002_start')):
        a=r/old_id;b=r/new_id;old_env=json.loads((a/'environment.json').read_text(encoding='utf-8'));env=json.loads((b/'environment.json').read_text(encoding='utf-8'))
        assert env['exit_code']==old_env['exit_code']==0
        assert env['rom_sha256']==sha(rom_path) and env['config_sha256']==old_env['config_sha256'] and env['exe_sha256']==old_env['exe_sha256']
        assert env['lua_sha256']==old_env['lua_sha256'] and env['input']==old_env['input']
        comparisons=[]
        for p in sorted(b.glob('frame_*.png')):
            q=a/p.name;assert q.exists()
            old=Image.open(q).convert('RGB');current=Image.open(p).convert('RGB')
            pts=[(i%256,i//256) for i,v in enumerate(ImageChops.difference(old,current).get_flattened_data()) if v!=(0,0,0)]
            outside=sum(not mask.getpixel(xy) for xy in pts);assert outside==0,(p,outside)
            old_ram=(a/(p.stem+'_ram.bin')).read_bytes();ram=(b/(p.stem+'_ram.bin')).read_bytes()
            assert old_ram[0x6cf]==ram[0x6cf],(p,'paragraph timing changed')
            if pts:assert int.from_bytes(ram[0x6cd:0x6cf],'little')==0x95f9;changed_samples+=1
            else:assert old==current or ImageChops.difference(old,current).getbbox() is None
            old_ppu=(a/(p.stem+'_ppu.bin')).read_bytes();ppu=(b/(p.stem+'_ppu.bin')).read_bytes()
            assert old_ppu[0x3f00:0x3f20]==ppu[0x3f00:0x3f20]
            assert (a/(p.stem+'_oam.bin')).read_bytes()==(b/(p.stem+'_oam.bin')).read_bytes()
            comparisons.append({'frame':int(p.stem[6:]),'changed_pixels':len(pts),'outside_paragraph_pixels':outside,'script_id_equal':True,'oam_palette_equal':True})
        runs.append({'path':new_id,'samples':len(comparisons),'comparisons':comparisons});total+=len(comparisons)
    assert total==165
    actual_dir=r/'qa/dialogue/poc002_attract';ppu=(actual_dir/'frame_01080_ppu.bin').read_bytes();assert ppu[:2048]==rom[0x40010:0x40810]
    for row,expected in zip((15,17),new):assert ppu[0x2000+row*32+4:0x2000+row*32+4+len(expected)]==bytes(expected)
    actual=Image.open(actual_dir/'frame_01080.png').convert('RGB');actual.resize((1024,960),Image.Resampling.NEAREST).save(r/'qa/dialogue/poc002_actual_4x.png')
    contact=Image.new('RGB',(1032,1040),'#252525');draw=ImageDraw.Draw(contact)
    for i,(frame,label) in enumerate(((976,'Partial first line'),(1080,'Complete paragraph / waiting'),(1320,'Next Japanese paragraph'),(3840,'Second attract cycle'))):
        draw.text((4,i*260+3),f'{label} / {frame} : TITLE ONLY | TITLE + KOREAN PARAGRAPH',fill='white')
        for x,path in ((0,r/'qa/dialogue/title_reference_attract'),(520,actual_dir)):
            contact.paste(Image.open(path/f'frame_{frame:05d}.png').convert('RGB'),(x+128,i*260+20))
    contact.save(r/'qa/dialogue/poc002_comparison.png')
    result={'status':'PASS for one-paragraph development PoC only','source_sha256':sha(source_path),'output_sha256':sha(rom_path),'ips_sha256':sha(folder/'TinyToon2_dialogue_kr_poc.ips'),'static':{'expected_writes':len(writes),'changed_bytes_including_append':len(changed),'raw_translation_source_preserved':True,'registered_other_text_and_pointers_unchanged':True,'original_font_unchanged':True,'title003_chr_identical':True,'serialized_text_roundtrip':True,'native_command_positions_line_counts_and_nonzero_parser_path_preserved':True,'glyph_count':14,'blank_code':122},'build_apply':{'rebuild_sha256_equal':True,'actual_korean_space_path_ips_apply_equal':True},'runtime':{'samples':total,'changed_paragraph_samples':changed_samples,'fully_identical_samples':total-changed_samples,'outside_paragraph_pixels':0,'runs':runs,'actual_appended_font_and_nametable_match':True,'all_sampled_paragraph_ids_equal':True},'direct_visual':'Record direct inspection separately in docs/POC_DIALOGUE.md.','limits':['one draft translation, no final human approval','temporary code pool, not a full-corpus font design','only intro raster-font selector changed; other consumers require investigation','not full playthrough, physical console, audio review or distribution release']}
    (r/'qa/reports/dialogue_poc002_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='runtime'},ensure_ascii=True,indent=2));print('Compared',total,'changed paragraph',changed_samples)
if __name__=='__main__':main()
