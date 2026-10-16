"""Explain footer rows using live PPU reads and the previously declared HUD shift."""
from pathlib import Path
import csv,hashlib,json,re,collections
from PIL import Image

R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))

def main():
    out=R/'qa/reports/bottom124_validation.json';assert not out.exists()
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
    src,rom=source.read_bytes(),current.read_bytes()
    assert src[0x1fce5]==0x2f and rom[0x3fce5]==0x0f
    assert src[0x1fcf9]==124 and rom[0x3fcf9]==206
    plan=json.loads((R/'workspace/translation/game_hud_plan_001.json').read_text('utf-8'))
    assert plan['producers'][0]['old']==0x2f and plan['producers'][0]['new']==0x0f
    assert 0 not in plan['changed_codes'] and 0x20 not in plan['changed_codes']
    assert '소유영역은y190..239' in (R/'docs/GAME_HUD_KOREAN.md').read_text('utf-8')
    palette=R/'work/context107/NesDefaultVideoFilter_2.1.1.cpp'
    assert sha(palette)=='a3346609701b883c60a1c48a0c23e0c18c8f00543c551fc7c314b341c5e6f990'
    line=next(s for s in palette.read_text('utf-8').splitlines()if'/* 2C02 */'in s)
    packed=[int(v,16)for v in re.findall('0x([0-9A-F]{8})',line)];assert len(packed)==64
    colors=[((v>>16)&255,(v>>8)&255,v&255)for v in packed]
    assert colors[7]==(86,29,0) and colors[15]==(0,0,0)
    probes=[];results=[];files={}
    for label,oldlabel,data in [('bottom124_source','river123_projection_source',src),
                               ('bottom124_current047','river123_projection_current047',rom)]:
        q=R/'qa/dialogue'/label;old=R/'qa/dialogue'/oldlabel
        env=json.loads((q/'environment.json').read_text('utf-8'));oe=json.loads((old/'environment.json').read_text('utf-8'))
        assert env['exit_code']==0 and env['frames']==3300
        for n,h in env['files'].items():assert sha(q/n)==h;files[(q/n).relative_to(R).as_posix()]=h
        files[(q/'environment.json').relative_to(R).as_posix()]=sha(q/'environment.json')
        raw=0;core=0;png_equal=0;png_exceptions=[]
        for p in sorted(q.glob('frame_*_ram.bin')):
            stem=p.name[:11]
            for suffix in ['_ram.bin','_ppu.bin','_oam.bin','_mapping.csv','_state.txt','.png']:
                n=stem+suffix;assert sha(old/n)==oe['files'][n]
                files[(old/n).relative_to(R).as_posix()]=sha(old/n)
                equal=(old/n).read_bytes()==(q/n).read_bytes()
                if suffix=='.png':
                    if equal:png_equal+=1
                    else:png_exceptions.append(n)
                else:
                    assert equal,n
                    if suffix=='_state.txt':core+=1
                    else:raw+=1
        r=rows(q/'bottom124_PPU_reads.csv');assert len(r)==1190
        assert {x['render_frame']for x in r}=={'3032'}
        pattern=[x for x in r if int(x['address'],16)<0x800 and int(x['dot'])%8 in(5,7)
                 and (1<=int(x['dot'])<=256 or 321<=int(x['dot'])<=336)]
        chrbase=16+data[4]*16384
        for x in pattern:
            assert int(x['value'],16)==data[chrbase+int(x['physical_relative'],16)]
            assert (int(x['vram_address'],16)>>12)&7==int(x['address'],16)&7
        representative=[next(x for x in r if int(x['scanline'])==y and x['dot']=='5')for y in range(233,240)]
        mid=(q/'bottom124_midframe_ppu.bin').read_bytes()
        assert mid[0x200:0x210]==bytes.fromhex('ffffffffffffffff0000000000000000')
        assert mid[0x2ff8]==255 and mid[0x2fa0:0x2fc0]==b'\x20'*32
        assert mid[0x2400:0x2420]==bytes(32)
        image=Image.open(q/'frame_03033.png').convert('RGB')
        boundary=235 if label=='bottom124_source' else 237
        matched=0
        for y in range(233,240):
            for x in range(256):
                wanted=colors[15] if y<boundary and x>=8 else colors[7]
                assert image.getpixel((x,y))==wanted,(label,x,y,image.getpixel((x,y)),wanted)
                matched+=1
        assert matched==1792
        probes.append(r)
        results.append({'directory':q.relative_to(R).as_posix(),'PPU_read_rows':len(r),
                        'live_pattern_rows_ROM_exact':len(pattern),'footer_representative_rows':representative,
                        'opaque_row29_wrap_to_next_nametable_row0_scanline':boundary,
                        'independent_footer_RGB_exact_pixels':matched,
                        'same_ROM_baseline123_raw_files_exact':raw,'same_ROM_baseline123_core_files_exact':core,
                        'same_ROM_baseline123_PNG_equal':png_equal,'same_ROM_baseline123_PNG_exceptions':png_exceptions})
    # Same footer tile/palette/VRAM consumers shifted down2scanlines, matching old40plan.
    keys=['dot','address','value','vram_address','xscroll','nt_address','nt_value','palette32_hex']
    paired=0
    for y in range(233,238):
        a=[x for x in probes[0]if int(x['scanline'])==y and int(x['address'],16)<0x800]
        b=[x for x in probes[1]if int(x['scanline'])==y+2 and int(x['address'],16)<0x800]
        assert [{k:x[k]for k in keys}for x in a]==[{k:x[k]for k in keys}for x in b]
        paired+=len(a)
    result={'work':124,'status':'PASS_FOOTER_TWO_ROW_DIFFERENCE_EXPLAINED_BY_DECLARED_HUD_SHIFT',
            'source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),
            'runs':results,'live_footer_pattern_rows_source_current_shifted2px_exact':paired,
            'original_IRQ_high2006_hex':'2F','current_IRQ_high2006_hex':'0F',
            'source_to_current_fineY_change':'2->0, same low12VRAM, previously declared040HUDlayout',
            'native_font124_tile00_and20_current_font206_preserved':True,
            'conclusion':'HUD lasttileRow29 uses black space20; source wraps to transparent nextNTrow0 at235, current at237 after intended2pxbody shift. Original and localized tile bits/NT/palette unchanged for this footer. No new font corruption or lost game scene inferred.',
            'ownership_correction':'Work40already ownsHUD190..239. Work123rectangle190..217was too narrow for originalROM comparison. This conclusion uses prior declared ownership and live PPU/RGB proof, not an arbitrary broader mask.',
            'reference_hashes':{p:sha(R/p)for p in ['docs/GAME_HUD_KOREAN.md','workspace/translation/game_hud_plan_001.json','qa/reports/game040_validation.json','qa/reports/river123_validation.json']},
            'frozen_files':files,
            'limits':['One diagnostic river frame with sevenfooter rows, not everyscene/viewport/IRQ/hardware case.',
                      'Same six inherited123writes plus read-only observer. No newROM/CSV/build/apply or CPU case.',
                      'No intended naturalEDpalette, commonPOW display, natural fullplay, human approval or final release claim.'],
            'release_eligible':False}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(result['status'],'shiftedpatternrows',paired,'RGBpixels',sum(x['independent_footer_RGB_exact_pixels']for x in results))

if __name__=='__main__':main()
