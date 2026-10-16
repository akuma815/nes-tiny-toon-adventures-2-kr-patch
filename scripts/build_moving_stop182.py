"""051 moving STOP sprite: preserve outline, pole, palette and all code/timing."""
from pathlib import Path
import argparse,json,sys
from PIL import Image,ImageDraw,ImageFont
from seal_nonplay171 import R,sha
from extract_title_png import decode,encode
from dialogue_ips import make,apply

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve();out.relative_to(R/'build');assert not out.exists()
    prior=R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes';old=prior.read_bytes();source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';src=source.read_bytes()
    assert sha(prior)=='49b8e869a232657f88c1810c3319d0f79b0ee23dd1ed993cf2bfc1f48726dc25' and sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    base=0x4b810;start=Image.new('L',(24,32));codes=list(range(40,52))
    for i,code in enumerate(range(40,52,2)):
        for dy in range(16):
            bits=decode(old[base+(code+dy//8)*16:base+(code+dy//8+1)*16])
            for x in range(8):start.putpixel((i%3*8+x,i//3*16+dy),bits[dy%8*8+x])
    assert old[base:base+1024]==src[base-0x20000:base-0x20000+1024]
    c=json.loads((R/'extracted/graphics/stop_001/consumer.json').read_text('utf-8'));fields={q['y']:(q['left'],q['right']) for q in c['inner_label_fields']};target=start.copy();mask=set()
    for y,(l,h) in fields.items():
        for x in range(l,h):assert start.getpixel((x,y)) in (1,2);mask.add((x,y));target.putpixel((x,y),2)
    font=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8)
    for ch,top in zip('정지',(8,16)):
        g=Image.new('L',(8,8));ImageDraw.Draw(g).text((0,-1),ch,font=font,fill=255);assert g.getbbox()==(0,0,6,7)
        for y in range(7):
            l,h=fields[top+y];assert h-l>=6
            for x in range(6):
                if g.getpixel((x,y))>127:assert (l+x,top+y) in mask;target.putpixel((l+x,top+y),1)
    for y in range(32):
        for x in range(24):assert (x,y) in mask or target.getpixel((x,y))==start.getpixel((x,y))
    new=bytearray(old);changed_codes=[]
    for i,code in enumerate(range(40,52,2)):
        for half in range(2):
            sub=target.crop((i%3*8,i//3*16+half*8,i%3*8+8,i//3*16+half*8+8));encoded=encode(bytes(sub.get_flattened_data()));p=base+(code+half)*16
            assert decode(encoded)==bytes(sub.get_flattened_data())
            if encoded!=old[p:p+16]:changed_codes.append(code+half)
            new[p:p+16]=encoded
    assert set(changed_codes)<={42,43,44,45,48,49,50,51}
    diff=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert diff and all(any(base+code*16<=i<base+(code+1)*16 for code in changed_codes) for i in diff)
    assert old[:0x40010]==new[:0x40010] and old[0x78010:0x78810]==new[0x78010:0x78810]
    writes=json.loads((prior.parent/'expected_writes.json').read_text('utf-8'));model=bytearray(src);owned=set()
    for w in writes:
        p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert src[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(new[p:p+n]).hex();model[p:p+n]=bytes.fromhex(w['final_hex'])
    assert model==new;patch=make(src,bytes(new));assert apply(src,patch)==new
    out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(new);(out/'TinyToon2_dialogue_kr_poc.ips').write_bytes(patch);start.save(out/'moving_stop_original_indices.png');target.save(out/'moving_stop_kr_indices.png')
    report={'work':182,'source_sha256':sha(source),'prior050_sha256':sha(prior),'output_sha256':sha(out/'TinyToon2_dialogue_kr_poc.nes'),'output_size':len(new),'IPS_sha256':sha(out/'TinyToon2_dialogue_kr_poc.ips'),'changed_bytes_vs050':len(diff),'CHR_bank':46,'source_range':[base-0x20000,base-0x20000+1024],'output_range':[base,base+1024],'changed_tile_codes':changed_codes,'OAM_8x16_tile_codes_hex':['69','6B','6D','6F','71','73'],'mapper_consumer':'Sprite PPU1400..17FF mapsCHR46; OAM69..73 use1680..173F, local tiles40..51. Native4200 recorded.','font':'Galmuri7 native6x7 vertical/sheared, same terminology/layout as fixed STOP','protected_pixels_outside_inner_field_equal':True,'all_PRG_header_other_CHR_fixed_STOP224225_equal050':True,'CPU_IRQ_input_timing_change':False,'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'runtime':'Pending same moving STOP reproduction and adjacent regression;050 adopted until PASS','human_final_approved':False}
    for name,obj in [('build_report.json',report),('expected_writes.json',writes),('moving_stop_plan.json',{'report':report,'fields':fields,'old_indices_hex':bytes(start.get_flattened_data()).hex(),'new_indices_hex':bytes(target.get_flattened_data()).hex(),'mask':sorted(mask)})]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n','utf-8')
    for n,p in [('builder_used.py',Path(__file__)),('translation_used.csv',R/'workspace/translation/text_ja.csv')]:(out/n).write_bytes(p.read_bytes())
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
