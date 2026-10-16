"""052 opening9 paragraphs11px; dedicated paired-row printer and private PRG8/9."""
from pathlib import Path
import argparse,csv,json
from PIL import Image,ImageDraw,ImageFont
from asm6502 import assemble
from extract_title_png import encode,decode
from dialogue_ips import make,apply
from seal_nonplay171 import R,sha

WRAPPER='''
    PHA
    LDA $18
    CMP #$07
    BNE @fallback
    LDA $06CF
    BEQ @fallback
    CMP #$0A
    BCS @fallback
    PLA
    LDA #$08
    JSR $FDD3
    JSR $9800
    PHP
    PHA
    JSR $FDDB
    PLA
    PLP
    RTS
fallback:
    PLA
    JMP $93E1
'''
PRINTER='''
    JSR $9880
    TAY
    CMP #$FF
    BEQ @terminator
    CMP #$FE
    BEQ @terminator
    JSR $9227
    CLC
    LDA $06C0
    ADC #$1F
    STA $06C0
    LDA $06C1
    ADC #$00
    STA $06C1
    JSR $9880
    JSR $9227
    SEC
    LDA $06C0
    SBC #$20
    STA $06C0
    LDA $06C1
    SBC #$00
    STA $06C1
    SEC
    RTS
terminator:
    JMP $93F0
'''
READER='''
    LDA $06CF
    ASL A
    TAY
    LDA $9900,Y
    STA $06
    LDA $9901,Y
    STA $07
    LDY $06C3
    LDA ($06),Y
    INC $06C3
    RTS
'''
CALLS=[0x8edf,0x8f13,0x8f61,0x8ff2,0x9012,0x90b9,0x915e]

def wrap(text):
    lines=[]
    for raw in text.split('\n'):
        while len(raw)>16:
            cut=raw.rfind(' ',0,17);cut=cut if cut>0 else 16
            lines.append(raw[:cut]);raw=raw[cut:].lstrip(' ')
        lines.append(raw)
    assert ' '.join(text.split())==' '.join(' '.join(lines).split())
    assert 0<len(lines)<=4 and all(len(x)<=16 for x in lines)
    return lines

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to(R/'build');assert not out.exists()
    prior=R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes';source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    assert sha(prior)=='b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24' and sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    old=prior.read_bytes();src=source.read_bytes();new=bytearray(old)
    rows={r['entry_id']:r for r in csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline=''))}
    selected=['MAIN_05609','MAIN_05625','MAIN_0564D','MAIN_05665','MAIN_0568B','MAIN_056C1','MAIN_056EE','MAIN_0570D','MAIN_05718']
    fontpath=R/'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf';face=ImageFont.truetype(str(fontpath),12)
    # Private physical8/9 overlay. Native encoded38/39 still selects original24/25.
    private=bytearray(old[0x24010:0x28010]);private[0]=8;private[0x2000]=9
    wrapper,wl,ws=assemble(WRAPPER,0x95f9);printer,pl,ps=assemble(PRINTER,0x9800);reader,rl,rs=assemble(READER,0x9880)
    assert len(wrapper)<0x9615-0x95f9+40 and len(printer)<0x9880-0x9800 and len(reader)<0x9900-0x9880
    def cpuwrite(address,payload):private[address-0x8000:address-0x8000+len(payload)]=payload
    cpuwrite(0x95f9,wrapper);cpuwrite(0x9800,printer);cpuwrite(0x9880,reader)
    # Wrapper continuation must exist byte-exact in both banks before/after switching.
    new[0x255f9:0x255f9+len(wrapper)]=wrapper
    for pc in CALLS:
        p=0x24010+pc-0x8000;assert old[p:p+3]==bytes.fromhex('20 e1 93')
        new[p:p+3]=bytes.fromhex('20 f9 95');cpuwrite(pc,bytes.fromhex('20 f9 95'))
    # Dedicated printer calls original enqueue/terminator logic in private clone.
    assert private[0x9227-0x8000:0x925e-0x8000]==old[0x25237:0x2526e]
    assert private[0x93b5-0x8000:0x940e-0x8000]==old[0x253c5:0x2541e]
    pages=[];ptrs=bytearray(20);streampos=0x9a00;modified_fonts=[]
    for page,entry in enumerate(selected,1):
        row=rows[entry];assert row['status']=='draft';lines=wrap(row['translation_ko']);im=Image.new('L',(192,len(lines)*16));d=ImageDraw.Draw(im)
        for y,line in enumerate(lines):
            left=(192-len(line)*12)//2
            for i,c in enumerate(line):
                g=Image.new('L',(16,16));ImageDraw.Draw(g).text((0,-1),c,font=face,fill=2)
                assert c.isspace() or g.getbbox(),(entry,c)
                if '\uac00'<=c<='\ud7a3':assert g.getbbox()[3]<=11 and g.getbbox()[2]<=12,(c,g.getbbox())
                d.text((left+12*i,y*16-1),c,font=face,fill=2)
        slots={bytes(64):0};font=bytearray(2048);body=bytearray();nt_rows=[]
        for y in range(len(lines)):
            codes=[[],[]]
            for x in range(24):
                for half in range(2):
                    bits=bytes(im.crop((8*x,y*16+half*8,8*x+8,y*16+half*8+8)).get_flattened_data())
                    if bits not in slots:
                        code=len(slots);assert code<128,(entry,'font tile budget',code)
                        slots[bits]=code;encoded=encode(bits);assert decode(encoded)==bits;font[code*16:(code+1)*16]=encoded
                    code=slots[bits];body.append(code);codes[half].append(code)
            body.append(0xff if y==len(lines)-1 else 0xfe);nt_rows.extend(codes)
        assert len(body)<=255 and streampos+len(body)<0xa000
        ptrs[page*2:page*2+2]=streampos.to_bytes(2,'little');cpuwrite(streampos,body)
        bank=old[0x5710+2*page];assert bank==[0,128,132,134,136,138,140,142,144,146][page]
        p=0x40010+bank*1024;new[p:p+2048]=font;modified_fonts.append((p,p+2048))
        pages.append({'page':page,'entry_id':entry,'original_pointer':int.from_bytes(old[0x255a9+2*page:0x255ab+2*page],'little'),'stream_pointer':streampos,'body_hex':body.hex(),'NT_top_origin':0x21e4,'lines':lines,'original_text':row['translation_ko'],'font_bank':bank,'font_file_offset':p,'font_unique_tiles':len(slots),'font_hex':font.hex(),'NT_rows':nt_rows,'typewriter_units':24*len(lines)+len(lines),'height':16*len(lines),'font_actual_Hangul_ink_height_max':11})
        streampos+=len(body)
    cpuwrite(0x9900,ptrs);new[0x10010:0x14010]=private
    permitted=[(0x10010,0x14010),(0x255f9,0x255f9+len(wrapper)),*[(0x24010+pc-0x8000,0x24013+pc-0x8000) for pc in CALLS],*modified_fonts]
    changes=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y];assert all(any(lo<=i<hi for lo,hi in permitted) for i in changes)
    assert new[:16]==old[:16] and len(new)==len(old) and new[0x3e010:0x40010]==old[0x3e010:0x40010]
    # Compose once from immutable source with existing disjoint source Expected Writes.
    writes=json.loads((prior.parent/'expected_writes.json').read_text('utf-8'))
    claimed=set();model=bytearray(src)
    for w in writes:
        p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&claimed;claimed|=area
        assert src[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(new[p:p+n]).hex();model[p:p+n]=bytes.fromhex(w['final_hex'])
    for lo,hi in [(0x10010,0x14010)]:
        area=set(range(lo,hi));assert not area&claimed;claimed|=area
        writes.append({'owner':'opening11_private_PRG8_9_overlay','file_offset':lo,'length':hi-lo,'expected_hex':src[lo:hi].hex(),'final_hex':bytes(new[lo:hi]).hex()});model[lo:hi]=new[lo:hi]
    assert model==new;patch=make(src,bytes(new));assert apply(src,patch)==new
    out.mkdir();name='TinyToon2_Opening11_PoC052';(out/(name+'.nes')).write_bytes(new);(out/(name+'.ips')).write_bytes(patch)
    (out/'builder_used.py').write_bytes(Path(__file__).read_bytes());(out/'translation_used.csv').write_bytes((R/'workspace/translation/text_ja.csv').read_bytes())
    for n,v in [('opening11_plan.json',{'pages':pages,'call_sites':CALLS,'private_PRG8_9_range':[0x10010,0x14010],'private_printer_PC':0x9800,'private_reader_PC':0x9880,'wrapper':{'origin':0x95f9,'asm':WRAPPER,'listing':wl,'symbols':ws},'printer':{'asm':PRINTER,'listing':pl,'symbols':ps},'reader':{'asm':READER,'listing':rl,'symbols':rs},'allowed_ranges_vs051':permitted}),('expected_writes.json',writes)]:
        (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')
    report={'work':186,'source_sha256':sha(source),'prior051_sha256':sha(prior),'output_sha256':sha(out/(name+'.nes')),'output_size':len(new),'output_rom':name+'.nes','IPS_sha256':sha(out/(name+'.ips')),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'font_sha256':sha(fontpath),'opening_pages':9,'font_em_px':12,'Hangul_actual_ink_height':11,'cell':[12,16],'modified_bytes_vs051':len(changes),'original_words_preserved':True,'layout_change':'12px cells centered in192px;wordwrap16cells;9paragraphs <=4lines. Full11px columns upper/lower queued together;8px horizontal typewriter chunks.','IRQ_fixed_PRG_unchanged':True,'clear_range':'Original21E4 nine32-byte-spaced rows covers all8possibletextrows; no clear patch','input_policy':'Development opening PoC only, not release or global11px adoption.051 staysstablebaseline.','runtime':'PENDING actual coldboot9pages,transfer budget,wait/clear/skip/reentry','limits':['Not global11px','Native typing/scene duration changes by tile-column count; not exact old pacing','Non-opening PRG8/9 use reachability and interrupts require actual trace/regression','Final visual approval pending']}
    (out/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
