"""Convert fixed AI PNG inputs to native tiles and two traced CHR layout streams."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageChops,__version__ as pillow_version
from extract_title_png import ROOT,decode,encode
from title_codec import unpack,pack
ASSET=ROOT/'extracted/title/title_20261004_001'
STREAM_START=0x24939
STREAM_BOUNDARY=0x249A7
STREAM_END=0x24A0B
BOUNDARY_POINTER=0x4249
PALETTE_MAIN=[(0,0,0),(100,176,255),(255,254,255),(66,64,255)]
PALETTE_RIBBON=[(0,0,0),(181,49,32),(255,254,255)]
def sha(b):return hashlib.sha256(b).hexdigest()
def quantize(im,palette):
    result=Image.new('L',im.size)
    result.putdata([min(range(len(palette)),key=lambda i:sum((c[k]-palette[i][k])**2 for k in range(3))) for c in im.convert('RGB').get_flattened_data()])
    return result
def rgb(indices,palette):
    out=Image.new('RGB',indices.size);out.putdata([palette[v] for v in indices.get_flattened_data()]);return out
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--main-png',type=Path,required=True);ap.add_argument('--ribbon-png',type=Path,required=True)
    ap.add_argument('--caption-png',type=Path,help='Optional separately corrected generated Korean caption')
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--roundtrip',action='store_true')
    a=ap.parse_args();m=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256'] and len(source)==m['size_bytes']
    info=json.loads((ASSET/'title_extraction.json').read_text(encoding='utf-8'))
    assert info['source_sha256']==m['sha256']
    assert source[BOUNDARY_POINTER:BOUNDARY_POINTER+2]==bytes.fromhex('97 11')
    assert source[0x4065:0x4069]==bytes.fromhex('B1 00 C9 FF')
    copies=ROOT/'qa/title/chr_stream_trace_001'
    assert (copies/'copy_1.bin').read_bytes()==source[STREAM_START:STREAM_BOUNDARY]
    assert (copies/'copy_2.bin').read_bytes()==source[STREAM_BOUNDARY:STREAM_END]
    plan=[];new_nt=[];targets=[];budgets=[];protected=[]
    for index,s in enumerate(info['sections']):
        name=s['name'];box=s['box'];x0,y0,x1,y1=box;w,h=x1-x0,y1-y0
        nt=(ASSET/f'{name}_nametable.bin').read_bytes();assert len(nt)==1024
        old_indices=Image.open(ASSET/s['indices_png']).convert('L')
        target=old_indices.copy();allowed=Image.new('L',(256,240))
        original_stream=source[(STREAM_START if index==0 else STREAM_BOUNDARY):(STREAM_BOUNDARY if index==0 else STREAM_END)]
        d,used=unpack(original_stream);assert len(d)==1024
        assert bytes(d[s['nametable_ppu_base']+i] for i in range(1024))==nt
        raw_png=a.main_png if index==0 else a.ribbon_png
        palette=PALETTE_MAIN if index==0 else PALETTE_RIBBON
        im=Image.open(raw_png).convert('RGB')
        if not a.roundtrip and index==1:
            # Built-in generation can add black margins; crop the nonblack asset as specified.
            ink=im.point(lambda v:255 if v>65 else 0).convert('L').point(lambda v:255 if v>0 else 0)
            bounds=ink.getbbox();assert bounds,'Empty generated ribbon';im=im.crop(bounds)
        pixels=quantize(im.resize((w,h),Image.Resampling.BOX),palette)
        if not a.roundtrip and index==1:
            # Convert generated lettering separately into the traced ribbon's solid inner panel.
            # Outer silhouette pixels come from the immutable original, not from the AI redesign.
            # Extract lettering before downsampling: a second resize destroys tiny Hangul strokes.
            white=Image.new('L',im.size)
            white.putdata([255 if min(c)>180 else 0 for c in im.get_flattened_data()])
            split=round(im.height*0.70)
            first=white.crop((0,0,im.width,split));second=white.crop((0,split,im.width,im.height))
            first_bounds=first.getbbox();second_bounds=second.getbbox()
            assert first_bounds and second_bounds,'Generated Korean text lines missing'
            primary=first.crop(first_bounds).resize((148,14),Image.Resampling.BOX).point(lambda v:255 if v>=128 else 0)
            secondary=second.crop(second_bounds)
            if a.caption_png:
                raw_caption=Image.open(a.caption_png).convert('RGB')
                secondary=Image.new('L',raw_caption.size)
                secondary.putdata([255 if min(c)>180 else 0 for c in raw_caption.get_flattened_data()])
                secondary=secondary.crop(secondary.getbbox())
            secondary=secondary.resize((100,8),Image.Resampling.BOX).point(lambda v:255 if v>=112 else 0)
            pixels=Image.new('L',(192,32))
            pixels.paste(primary.point(lambda v:2 if v else 0),(24,8))
            pixels.paste(secondary.point(lambda v:2 if v else 0),(48,24))
        if a.roundtrip:
            assert pixels.tobytes()==old_indices.crop(box).tobytes(),'PNG pixel roundtrip mismatch'
        else:
            for y in range(y0,y1):
                for x in range(x0,x1):
                    if index==0:
                        allowed.putpixel((x,y),255);target.putpixel((x,y),pixels.getpixel((x-x0,y-y0)))
                    else:
                        old=old_indices.getpixel((x,y));v=pixels.getpixel((x-x0,y-y0))
                        panel=48<=x<208 and 112<=y<136 and old in (1,2)
                        caption=72<=x<184 and 136<=y<144 and old!=1
                        if panel:
                            allowed.putpixel((x,y),255);target.putpixel((x,y),2 if v==2 else 1)
                        elif caption:
                            allowed.putpixel((x,y),255);target.putpixel((x,y),2 if v==2 else 0)
                        elif v==2 and old!=2:
                            raise ValueError(f'Generated ribbon text crosses protected silhouette at {x},{y}')
        updated=bytearray(nt);writes={};patterns={bytes(16):0};pool=list(s['exclusive_tiles'])
        if a.roundtrip:
            for tile in s['used_tiles']:
                raw=source[s['chr_file_base']+16*tile:s['chr_file_base']+16*(tile+1)]
                assert encode(decode(raw))==raw
        else:
            # Unique-per-cell allocation keeps increment RLE efficient. Fall back to dedup only if needed.
            cells=[]
            for row in range(y0//8,y1//8):
                for col in range(x0//8,x1//8):
                    raw=encode(bytes(target.crop((col*8,row*8,col*8+8,row*8+8)).get_flattened_data()))
                    cells.append((row,col,raw))
            nonblank=sum(raw!=bytes(16) for _,_,raw in cells)
            unique=len({raw for _,_,raw in cells if raw!=bytes(16)})
            assert unique<=len(pool),f'{name} tile budget: {unique}>{len(pool)}'
            per_cell=nonblank<=len(pool)
            cursor=0
            for row,col,raw in cells:
                if raw==bytes(16):tile=0
                elif not per_cell and raw in patterns:tile=patterns[raw]
                else:
                    tile=pool[cursor];cursor+=1;patterns[raw]=tile;writes[tile]=raw
                updated[row*32+col]=tile
            for tile,raw in writes.items():
                offset=s['chr_file_base']+tile*16
                plan.append({'owner':name+'_pixels','file_offset':offset,'length':16,
                    'expected_hex':source[offset:offset+16].hex(),'final_hex':raw.hex()})
            assert updated[960:]==nt[960:]
            assert all(updated[i]==nt[i] for i in range(960) if not (y0//8<=i//32<y1//8 and x0//8<=i%32<x1//8))
        new_nt.append(bytes(updated));targets.append((name,target,allowed,palette,box))
        budgets.append({'section':name,'available_tiles':len(pool),'used_tiles':len(writes),'allocation':'identity' if a.roundtrip else 'per-cell' if per_cell else 'deduplicated'})
        protected.append({'section':name,'pixel_mask':allowed})
    if not a.roundtrip:
        streams=[pack(nt,s['nametable_ppu_base']) for nt,s in zip(new_nt,info['sections'])]
        size1,size2=map(len,streams);capacity=STREAM_END-STREAM_START
        assert size1+size2<=capacity,f'Combined CHR stream budget: {size1}+{size2}>{capacity}'
        assert size1<=512 and size2<=512,'Temporary source RAM buffer budget'
        boundary=STREAM_BOUNDARY if size1<=STREAM_BOUNDARY-STREAM_START and size2<=STREAM_END-STREAM_BOUNDARY else STREAM_START+size1
        pointer=0x1129+boundary-STREAM_START
        merged=bytearray(source[STREAM_START:STREAM_END]);merged[:size1]=streams[0]
        rib_offset=boundary-STREAM_START;merged[rib_offset:rib_offset+size2]=streams[1]
        plan.append({'owner':'title_layouts','file_offset':STREAM_START,'length':capacity,
            'expected_hex':source[STREAM_START:STREAM_END].hex(),'final_hex':merged.hex()})
        if boundary!=STREAM_BOUNDARY:
            plan.append({'owner':'title_stream_boundary','file_offset':BOUNDARY_POINTER,'length':2,
                'expected_hex':source[BOUNDARY_POINTER:BOUNDARY_POINTER+2].hex(),'final_hex':pointer.to_bytes(2,'little').hex()})
        for b,sz in zip(budgets,(size1,size2)):b['compressed_bytes']=sz
    else:boundary=STREAM_BOUNDARY;pointer=0x1197
    modified=bytearray(source);owned=set()
    for write in plan:
        start=write['file_offset'];length=write['length'];region=set(range(start,start+length))
        assert not owned&region;owned|=region
        assert source[start:start+length]==bytes.fromhex(write['expected_hex'])
        final=bytes.fromhex(write['final_hex']);assert len(final)==length;modified[start:start+length]=final
    diffs={i for i,(x,y) in enumerate(zip(source,modified)) if x!=y};assert diffs<=owned and len(modified)==len(source)
    assert modified[:16]==source[:16]
    for i,s in enumerate(info['sections']):
        decoded,_=unpack(modified[(STREAM_START if i==0 else boundary):(boundary if i==0 else STREAM_END)])
        assert bytes(decoded[s['nametable_ppu_base']+k] for k in range(1024))==new_nt[i]
        name,target,mask,palette,box=targets[i]
        old=Image.open(ASSET/s['indices_png']).convert('L')
        for y in range(240):
            for x in range(256):
                tile=new_nt[i][y//8*32+x//8]
                value=decode(modified[s['chr_file_base']+tile*16:s['chr_file_base']+(tile+1)*16])[y%8*8+x%8]
                assert value==target.getpixel((x,y))
                if not mask.getpixel((x,y)):assert value==old.getpixel((x,y))
    output=a.output.resolve();assert ROOT/'original' not in output.parents and output!=ROOT/'original'
    output.mkdir(parents=True,exist_ok=False)
    (output/'expected_writes.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    rom_name='TinyToon2_title_roundtrip.nes' if a.roundtrip else 'TinyToon2_title_kr_poc.nes'
    (output/rom_name).write_bytes(modified)
    preview=Image.open(ROOT/'qa/screenshots/baseline_attract_002/frame_00720.png').convert('RGB')
    protect_mask=Image.new('L',(256,240))
    for name,target,mask,palette,box in targets:
        crop=rgb(target.crop(box),palette);crop.save(output/f'{name}_nes.png')
        crop.resize((crop.width*8,crop.height*8),Image.Resampling.NEAREST).save(output/f'{name}_nes_8x.png')
        target.save(output/f'{name}_indices.png');mask.save(output/f'{name}_edit_mask.png')
        source_rgb=Image.open(ASSET/f'{name}_original.png').convert('RGB')
        display_dy=-2 if name=='ribbon' else 0
        for y in range(box[1],box[3]):
            for x in range(box[0],box[2]):
                if mask.getpixel((x,y)):
                    # The numeral 2 is a protected sprite composited over the background.
                    screen_xy=(x,y+display_dy)
                    if preview.getpixel(screen_xy)==source_rgb.getpixel((x-box[0],y-box[1])):
                        protect_mask.putpixel(screen_xy,255)
                        preview.putpixel(screen_xy,crop.getpixel((x-box[0],y-box[1])))
    preview.save(output/'title_static_preview.png');preview.resize((1024,960),Image.Resampling.NEAREST).save(output/'title_static_preview_4x.png')
    protect_mask.save(output/'title_allowed_pixel_mask.png')
    report={'source_sha256':sha(source),'output_sha256':sha(modified),'output_rom':rom_name,
        'roundtrip_identity':bytes(modified)==source,'changed_bytes':len(diffs),'expected_writes':len(plan),
        'main_input_sha256':sha(a.main_png.read_bytes()),'ribbon_input_sha256':sha(a.ribbon_png.read_bytes()),
        'caption_input_sha256':sha(a.caption_png.read_bytes()) if a.caption_png else None,
        'display_offsets':{'main':0,'ribbon':-2},
        'budgets':budgets,'stream_capacity_bytes':210,'new_boundary_chr_file_offset':boundary,'new_boundary_ppu_pointer':pointer,
        'header_size_palette_attributes_oam_preserved':True,'protected_graphics_pixels_preserved':True,
        'python':sys.version,'pillow':pillow_version,'scope':'Static build/preview only; execute actual ROM before claiming runtime success'}
    (output/'build_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
