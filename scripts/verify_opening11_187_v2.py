"""Actual nine-page11px pixels, three loops, native transfers/clear and skip regression."""
from pathlib import Path
import csv,json,collections,shutil
from PIL import Image,ImageDraw,ImageFont
from seal_nonplay171 import R,sha
from extract_title_png import decode
from verify_intro144_v3 import native_lines

def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def environment(p):
    e=json.loads((p/'environment.json').read_text('utf-8'));assert e['exit_code']==0
    for f,h in e['files'].items():assert sha(p/f)==h,(p.name,f)
    return e

def main():
    out=R/'qa/reports/opening11_187_validation.json';assert not out.exists()
    build=R/'build/opening11_poc_053';plan=json.loads((build/'opening11_plan.json').read_text('utf-8'));rom=(build/'TinyToon2_Opening11_PoC053.nes').read_bytes()
    for n in ['TinyToon2_Opening11_PoC053.nes','TinyToon2_Opening11_PoC053.ips']:assert (build/n).read_bytes()==(R/'build/opening11_186_rebuild053'/n).read_bytes()
    p=R/'qa/dialogue/opening11_186_053_v2';e=environment(p);assert e['frames']==9000 and not e['input']['sequence']
    v=rows(p/'ppu_native_writes.csv');index=collections.defaultdict(list)
    for r in v:index[(int(r['frame']),int(r['address'],16),int(r['value'],16))].append(r)
    history={};nt=bytearray(216);groups=collections.defaultdict(list)
    for row in v:groups[int(row['frame'])].append(row)
    for frame in range(9000):
        for row in groups[frame]:
            a=int(row['address'],16);delta=a-0x21e4
            if 0<=delta<9*32 and delta%32<24:nt[(delta//32)*24+delta%32]=int(row['value'],16)
        history[frame]=bytes(nt)
    q=rows(p/'paired_printer.csv');beg=[r for r in q if r['kind']=='begin'];end=[r for r in q if r['kind']=='end'];assert len(beg)==len(end)==1575
    pp={z['page']:z for z in plan['pages']};calls=collections.Counter();glyphwrites=0;scanlines=set();maxq=0;maxcycles=0
    for b,a in zip(beg,end):
        assert b['frame']==a['frame'] and b['PRG_relative_offset']==a['PRG_relative_offset']=='10000'
        page=int(b['page'],16);c=int(b['cursor'],16);body=bytes.fromhex(pp[page]['body_hex']);first=body[c];calls[page]+=1
        assert int(a['sp'],16)==int(b['sp'],16)+2
        delta=int(a['queue_size'],16)-int(b['queue_size'],16);maxq=max(maxq,int(a['queue_size'],16));maxcycles=max(maxcycles,int(a['cycles'])-int(b['cycles']))
        if first<128:
            assert delta==10 and int(a['cursor'],16)==c+2
            raw=bytes.fromhex(a['queue_hex']);o=int(b['queue_size'],16);top=int(b['high_nt'],16)*256+int(b['low_nt'],16)
            for half,j in enumerate((o,o+5)):
                assert raw[j]==1 and raw[j+4]==255
                address=raw[j+1]*256+raw[j+2];value=raw[j+3]
                assert address==top+32*half and value==body[c+half]
                actual=index[(int(a['frame'])+1,address,value)];assert len(actual)==1,(a['frame'],address,value)
                scan=int(actual[0]['scanline']);assert 241<=scan<=260;scanlines.add(scan);glyphwrites+=1
        else:
            assert delta==0 and first in (254,255)
            assert int(a['cursor'],16)==(0 if first==255 else c+1)
    assert glyphwrites==3024 and all(calls[z['page']]==3*z['typewriter_units'] for z in plan['pages'])
    init=rows(p/'opening_init_clear.csv');assert len(init)==30 and all(not any(bytes.fromhex(r['rows9_hex'])) for r in init)
    assert set(int(r['page'],16) for r in init)==set(range(1,10))
    face=ImageFont.truetype(str(R/'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'),12)
    expectations={};complete=collections.defaultdict(list);rendered=0;pixels=0;selected={}
    for z in plan['pages']:
        im=Image.new('L',(192,z['height']));d=ImageDraw.Draw(im)
        for y,line in enumerate(z['lines']):
            left=(192-len(line)*12)//2
            for x,c in enumerate(line):d.text((left+12*x,y*16-1),c,font=face,fill=2)
        assert set(im.get_flattened_data())<={0,2}
        decoded=Image.new('L',im.size);font=bytes.fromhex(z['font_hex'])
        for y,rr in enumerate(z['NT_rows']):
            for x,t in enumerate(rr):decoded.paste(Image.frombytes('L',(8,8),decode(font[16*t:16*t+16])),(8*x,8*y))
        assert decoded.tobytes()==im.tobytes();expectations[z['page']]=im
    # Match each eligible active-font snapshot, including partial typing/wait/clear.
    for f in sorted(p.glob('frame_*_ram.bin')):
        tag=f.name[:11];ram=f.read_bytes()
        if ram[0x18]!=7:continue
        ptr=int.from_bytes(ram[0x6cd:0x6cf],'little');candidates=[z for z in plan['pages'] if z['original_pointer']==ptr and z['font_bank']==ram[0xc6]]
        if not candidates:continue
        z=candidates[0];ppu=(p/(tag+'_ppu.bin')).read_bytes();font=bytes.fromhex(z['font_hex'])
        if ppu[:0x800]!=font:continue # pre-IRQ/new latch epoch not eligible
        n=int(tag[6:]);current=b''.join(ppu[0x21e4+y*32:0x21e4+y*32+24] for y in range(9))
        assert current==history[n-1],(tag,'VRAM log to current snapshot epoch')
        consumed=history[n-2] # measured Mesen screenshot lags currentNT by one render epoch
        predicted=Image.new('RGB',(192,72));allrows=[]
        for y in range(9):
            rr=consumed[y*24:y*24+24];allrows.append(rr)
            for x,t in enumerate(rr):
                assert t<128,(tag,y,t)
                bits=decode(font[16*t:16*t+16]);assert set(bits)<={0,2}
                tile=Image.new('RGB',(8,8));tile.putdata([(255,254,255) if b==2 else (0,0,0) for b in bits]);predicted.paste(tile,(8*x,8*y))
        actual=Image.open(p/(tag+'.png')).convert('RGB').crop((32,116,224,188))
        assert actual.tobytes()==predicted.tobytes(),(tag,z['page'],'native11px RGB or clear mismatch')
        rendered+=1;pixels+=192*72
        if all(allrows[y]==bytes(rr) for y,rr in enumerate(z['NT_rows'])):
            complete[z['page']].append(int(tag[6:]))
            if z['page'] not in selected:selected[z['page']]=tag
    assert set(complete)==set(range(1,10)) and rendered>1500
    # Adjacent Start skip: post-reset home screen/activePPU/OAM retained.
    skip=[]
    for at in (1000,1900):
        a,b=[R/f'qa/dialogue/opening11_187_skip{at}_{n}' for n in ('051','053')];ea,eb=[environment(x) for x in (a,b)]
        for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'):assert ea[k]==eb[k]
        count=0
        for f in sorted(a.glob('frame_*.png')):
            if not (b/f.name).exists():continue
            tag=f.stem;n=int(tag[6:]);ra=(a/(tag+'_ram.bin')).read_bytes();rb=(b/(tag+'_ram.bin')).read_bytes()
            if n<at+90 or ra[0x18]!=0 or rb[0x18]!=0:continue
            assert f.read_bytes()==(b/f.name).read_bytes(),(at,tag,'native title PNG')
            for suffix in ('_ppu.bin','_oam.bin','_mapping.csv'):assert (a/(tag+suffix)).read_bytes()==(b/(tag+suffix)).read_bytes(),(at,tag,suffix)
            assert ra[0xc6]==rb[0xc6] and ra[0x6cd:0x6cf]==rb[0x6cd:0x6cf]
            count+=1
        assert count>=5,(at,count);skip.append({'Start_frame':at,'title_entire_PNG_PPU_OAM_mapping_equal':count,'historical_reader_scratch_RAM_not_claimed_equal':True})
    a=R/'qa/dialogue/moving_stop182_051';b=R/'qa/dialogue/opening11_187_train053';ea,eb=[environment(x) for x in (a,b)]
    for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'):assert ea[k]==eb[k]
    train=0
    for f in sorted(a.glob('frame_*.png')):
        assert f.read_bytes()==(b/f.name).read_bytes(),f.name
        for suffix in ('_ram.bin','_ppu.bin','_oam.bin','_mapping.csv','_state.txt'):assert (a/(f.stem+suffix)).read_bytes()==(b/(f.stem+suffix)).read_bytes(),(f.name,suffix)
        train+=1
    assert train==734
    review=R/'workspace/review/opening11_187';review.mkdir(exist_ok=False)
    baseline=R/'qa/dialogue/opening11_186_051';old=(R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes').read_bytes();environment(baseline)
    oldselected={}
    for z in plan['pages']:
        lines=native_lines(old,z['page'])
        for f in sorted(baseline.glob('frame_*_ram.bin')):
            r=f.read_bytes();tag=f.name[:11]
            if r[0x18]!=7 or r[0xc6]!=z['font_bank'] or int.from_bytes(r[0x6cd:0x6cf],'little')!=z['original_pointer']:continue
            raw=(baseline/(tag+'_ppu.bin')).read_bytes()
            if all(raw[0x21e4+64*y:0x21e4+64*y+len(rr)]==rr for y,rr in enumerate(lines)):oldselected[z['page']]=tag;break
        assert z['page'] in oldselected
        shutil.copyfile(p/(selected[z['page']]+'.png'),review/f'page{z["page"]:02d}_11px.png')
        shutil.copyfile(baseline/(oldselected[z['page']]+'.png'),review/f'page{z["page"]:02d}_8px.png')
    cards=''.join(f'<article><h2>문단 {z["page"]}: {z["entry_id"]}</h2><div class="pair"><figure><figcaption>기존8px / {oldselected[z["page"]]}</figcaption><img src="page{z["page"]:02d}_8px.png"></figure><figure><figcaption>11px PoC / {selected[z["page"]]}</figcaption><img src="page{z["page"]:02d}_11px.png"></figure></div><pre>{chr(10).join(z["lines"])}</pre></article>' for z in plan['pages'])
    (review/'review.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>오프닝11px PoC053</title><style>body{font-family:sans-serif;background:#202027;color:#eee;margin:24px}article{border-top:1px solid #777;padding:20px 0}.pair{display:flex;flex-wrap:wrap;gap:20px}figure{margin:0;max-width:100%}img{width:512px;max-width:100%;image-rendering:pixelated}pre{white-space:pre-wrap;font-size:18px}</style><h1>오프닝11px PoC053 — 실제 Mesen 화면</h1><p>9문단의 각 빌드 완성시점 캡처입니다. 타이핑 길이가 달라 서로 같은 프레임 비교는 아닙니다. ROM 전체11px 적용/최종그림승인/전체플레이 검증은 아닙니다.</p>'+cards+'</html>','utf-8')
    result={'work':187,'status':'PASS_OPENING11_053_NINE_PAGES_THREE_LOOPS_AND_ADJACENT_REGRESSION','ROM_sha256':sha(build/'TinyToon2_Opening11_PoC053.nes'),'frames':9000,'loops_each_page':3,'paired_printer_calls':len(beg),'exact_final6502_glyph_transfers_in_following_vblank':glyphwrites,'glyph_transfer_scanlines':sorted(scanlines),'max_total_queue_bytes':maxq,'max_inner_printer_cycles':maxcycles,'pre_init9row_clear_zero_checks':len(init),'eligible_partial_wait_clear_RGB_snapshots_exact':rendered,'native_text_field_RGB_pixels_exact':pixels,'complete_frames_by_page':dict(complete),'selected_current_frames':selected,'selected_baseline_frames':oldselected,'Start_skips_return_to_native_title_then_intro_reenters':skip,'pixel_epoch_proof':'Actual VRAM write replay asof frameN-1 equals current NT dump; asof N-2 exactly matches complete screenshot. Fixed one-render-epoch latency; no broad pixel mask.','train734_wholePNG_RAM_PPU_OAM_mapping_CPUstate_equal051':train,'independent_ROM_IPS_rebuild_exact':True,'CSV_unchanged':True,'stable_baseline051_retained':True,'scope':'Opening9 paragraphs only11px. Native paired PPUNT consumption and font residency, typing/wait/clear/three loops, Start1000/1900 title+intro reentry, inherited controller train regression. No forced memory/PC/state or life seed.','limits':['Not global11px migration','Different scene pacing from old tile counts; exact old timing not promised','No full gameplay/audio/hardware/general save-state compatibility','Private PRG8/9 globally unreachable outside observed routes not proven','Final human font/layout approval pending']}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('complete_frames_by_page',)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
