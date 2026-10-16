"""055 only page6 user-directed layout, preserving all053 code/control positions."""
from pathlib import Path
import argparse,csv,json,copy
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import encode,decode
from dialogue_ips import make,apply
from seal_nonplay171 import R,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve();out.relative_to(R/'build');assert not out.exists()
    prior=R/'build/opening11_poc_053';source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    assert sha(prior/'TinyToon2_Opening11_PoC053.nes')=='d27a78ddfd0f8b3d6d46bf1b9db85dbd1d1051bde99ea7eb65a46c5656b53e3c'
    assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    src=source.read_bytes();old=(prior/'TinyToon2_Opening11_PoC053.nes').read_bytes();new=bytearray(old);plan=json.loads((prior/'opening11_plan.json').read_text('utf-8'));previous=copy.deepcopy(plan)
    override=R/'workspace/translation/opening_layout_override193.json';layout=json.loads(override.read_text('utf-8'));rows={x['entry_id']:x for x in csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig'))};text=rows[layout['entry_id']]['translation_ko']
    assert ' '.join(text.split())==' '.join(' '.join(layout['lines']).split())
    assert len(layout['lines'])==len(layout['alignments'])==4 and all(len(x)<=16 for x in layout['lines'])
    z=plan['pages'][5];assert z['page']==layout['page']==6 and z['entry_id']==layout['entry_id']
    fontpath=R/'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf';assert sha(fontpath)=='e24256f42e43713d2ea086a1e1669d78b968f5b3cc547e5c157f0606ffa5def1'
    face=ImageFont.truetype(str(fontpath),12);im=Image.new('L',(192,64));d=ImageDraw.Draw(im);positions=[]
    for y,(line,align) in enumerate(zip(layout['lines'],layout['alignments'])):
        assert align in ('center','right');left=(192-len(line)*12)//2 if align=='center' else 192-len(line)*12-layout['right_inset_pixels'];positions.append(left)
        for x,c in enumerate(line):
            glyph=Image.new('L',(16,16));ImageDraw.Draw(glyph).text((0,-1),c,font=face,fill=2);assert c.isspace() or glyph.getbbox();d.text((left+12*x,16*y-1),c,font=face,fill=2)
    assert set(im.get_flattened_data())<={0,2}
    slots={bytes(64):0};font=bytearray(2048);body=bytearray();nt=[]
    for line in range(4):
        rr=[[],[]]
        for x in range(24):
            for half in range(2):
                bits=bytes(im.crop((x*8,line*16+half*8,x*8+8,line*16+half*8+8)).get_flattened_data())
                if bits not in slots:
                    code=len(slots);assert code<128;slots[bits]=code;raw=encode(bits);assert decode(raw)==bits;font[code*16:(code+1)*16]=raw
                code=slots[bits];body.append(code);rr[half].append(code)
        body.append(255 if line==3 else 254);nt.extend(rr)
    oldbody=bytes.fromhex(z['body_hex']);assert len(body)==len(oldbody)==196 and all(body[i]==oldbody[i] for i in (48,97,146,195))
    data=0x10010+z['stream_pointer']-0x8000;new[data:data+196]=body;off=z['font_file_offset'];new[off:off+2048]=font
    allowed=[[data,data+196],[off,off+2048]];changes=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert all(any(lo<=i<hi for lo,hi in allowed) for i in changes)
    assert new[:16]==old[:16] and new[0x24010:0x40010]==old[0x24010:0x40010]
    for q in previous['pages']:
        if q['page']==6:continue
        p=q['font_file_offset'];assert new[p:p+2048]==old[p:p+2048]
        p=0x10010+q['stream_pointer']-0x8000;n=len(bytes.fromhex(q['body_hex']));assert new[p:p+n]==old[p:p+n]
    z.update(lines=layout['lines'],line_alignments=layout['alignments'],line_left_pixels=positions,font_hex=font.hex(),font_unique_tiles=len(slots),body_hex=body.hex(),NT_rows=nt)
    plan['layout_override_input']=override.relative_to(R).as_posix();plan['layout_override_sha256']=sha(override);plan['allowed_ranges_vs053']=allowed
    writes=json.loads((prior/'expected_writes.json').read_text('utf-8'));model=bytearray(src);owned=set()
    for w in writes:
        p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert src[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(new[p:p+n]).hex();model[p:p+n]=bytes.fromhex(w['final_hex'])
    assert model==new;ips=make(src,bytes(new));assert apply(src,ips)==new
    out.mkdir();name='TinyToon2_Opening11_PoC055';(out/(name+'.nes')).write_bytes(new);(out/(name+'.ips')).write_bytes(ips)
    report={'work':193,'source_sha256':sha(source),'prior053_sha256':sha(prior/'TinyToon2_Opening11_PoC053.nes'),'output_sha256':sha(out/(name+'.nes')),'output_size':len(new),'output_rom':name+'.nes','IPS_sha256':sha(out/(name+'.ips')),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'font_sha256':sha(fontpath),'layout_override_sha256':sha(override),'changed_bytes_vs053':len(changes),'change_scope':'Only openingpage6 private stream tile codes andfont140/141; fontfamily/code/allcontrolpositions/length/pacingunits/other8pages unchanged','lines':layout['lines'],'alignments':layout['alignments'],'line_left_pixels':positions,'font_unique_tiles':len(slots),'home054_not_included':True,'runtime':'PENDING dedicated opening55 observation','human_request':'Page6 split surprise phrase andright aligned one-line signature','global_font_layout_approval':False}
    for n,v in [('build_report.json',report),('opening11_plan.json',plan),('expected_writes.json',writes)]: (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')
    (out/'builder_used.py').write_bytes(Path(__file__).read_bytes());(out/'translation_used.csv').write_bytes((R/'workspace/translation/text_ja.csv').read_bytes());(out/'layout_override_used.json').write_bytes(override.read_bytes())
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
