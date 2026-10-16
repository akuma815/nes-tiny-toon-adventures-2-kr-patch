"""Matched native exchange and adjacent branch verification; no fullplay claim."""
from pathlib import Path
import csv,json,collections
from PIL import Image,ImageChops
from seal_nonplay171 import R,sha

def rows(p):return list(csv.DictReader(p.open(encoding='utf-8')))
def main():
    out=R/'qa/reports/issue177_validation.json';assert not out.exists()
    rom=R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes';data=rom.read_bytes()
    for n in ['TinyToon2_dialogue_kr_poc.nes','TinyToon2_dialogue_kr_poc.ips']:
        assert (rom.parent/n).read_bytes()==(R/'build/issue177_rebuild050'/n).read_bytes()
    result={}
    for kind in ['exchange','booth0','ride3','ride4']:
        old=R/f'qa/dialogue/issue177_{kind}_049';new=R/f'qa/dialogue/issue177_{kind}_050'
        a,b=[json.loads((d/'environment.json').read_text('utf-8')) for d in (old,new)]
        assert a['exit_code']==b['exit_code']==0
        for k in ['exe_sha256','lua_sha256','config_sha256','frames','input','seed','seed_file_sha256']:assert a[k]==b[k],k
        for d,e in [(old,a),(new,b)]:
            for f,h in e['files'].items():assert sha(d/f)==h,(kind,f)
        ae,be=[rows(d/'menu_events.csv') for d in (old,new)]
        ax,bx=[[x for x in e if x['kind']=='exec'] for e in (ae,be)]
        assert len(ax)==len(bx)
        for x,y in zip(ax,bx):
            for k in x:
                if k not in ['font','active_font']:assert x[k]==y[k],(kind,k,x,y)
        changed=collections.Counter();statechanges=collections.Counter();pngchanged=0;frames=0
        for f in sorted(old.glob('*_ram.bin')):
            frames+=1;tag=f.name[:-8];x=f.read_bytes();y=(new/f.name).read_bytes()
            for i,(u,v) in enumerate(zip(x,y)):
                if u!=v:
                    assert i in {0xc6,0x6f3} or 0x100<=i<0x200,(kind,hex(i),u,v)
                    changed[f'{i:04X}']+=1
            assert x[0x22]==y[0x22] # identical RNG state, unlike earlier048->049 timing change
            ps=[(d/(tag+'_ppu.bin')).read_bytes() for d in (old,new)]
            assert ps[0][0x400:]==ps[1][0x400:],(kind,tag,'outside first lower-font CHR page')
            assert (old/(tag+'_oam.bin')).read_bytes()==(new/(tag+'_oam.bin')).read_bytes()
            st=[dict(z.split('=',1) for z in (d/(tag+'_state.txt')).read_text('utf-8').splitlines()) for d in (old,new)]
            for k in st[0]:
                if st[0][k]!=st[1][k]:
                    assert k.startswith('mapper.chrMemoryOffset'),(kind,tag,k)
                    statechanges[k]+=1
            im=[Image.open(d/(tag+'.png')).convert('RGB') for d in (old,new)]
            assert ImageChops.difference(im[0].crop((0,0,256,130)),im[1].crop((0,0,256,130))).getbbox() is None
            assert ImageChops.difference(im[0].crop((0,130,48,240)),im[1].crop((0,130,48,240))).getbbox() is None
            pngchanged+=int(ImageChops.difference(*im).getbbox() is not None)
            if kind.startswith('ride'):assert ps[0]==ps[1] and pngchanged==0
        commits=[x for x in bx if x['address']=='9445']
        numeric=[x for x in commits if x['id']=='23']
        if kind=='exchange':
            assert len(numeric)==12 and all(x['caller']=='9CD2' and x['ride']=='06' for x in numeric)
            assert numeric[0]['active_font']=='9E' and all(x['active_font']=='A2' for x in numeric[1:])
            p=(new/'frame_01710_ppu.bin').read_bytes();r=(new/'frame_01710_ram.bin').read_bytes()
            assert r[0x6f3]==162 and r[0x7d0:0x7d3]==bytes([6,1,0]) and r[0x7f2:0x7f7]==bytes(5)
            assert p[:0x400]==data[0x40010+162*1024:0x40010+163*1024]
            assert p[0x22a8:0x22b3]==bytes.fromhex('2b2c2d2e7a2f2728292a7a') and p[0x22e8:0x22f0]==bytes.fromhex('30317a323334357a')
            assert next(x for x in commits if x['id']=='15')['active_font']=='BC'
        if kind=='booth0':assert next(x for x in commits if x['id']=='14')['active_font']=='A4'
        if kind=='ride3':
            assert next(x for x in commits if x['id']=='29' and x['phase']=='03')['active_font']=='E2'
            assert any(x['id']=='2B' and x['active_font']=='C4' for x in commits)
        if kind=='ride4':assert len(numeric)==1 and numeric[0]['ride']=='01' and numeric[0]['active_font']=='C4' and any(x['id']=='2A' for x in commits)
        result[kind]={'status':'PASS','paired_snapshots':frames,'native_init_commits':len(commits),'numeric_commits':numeric,'changed_RAM_counts':dict(changed),'changed_state_counts':dict(statechanges),'changed_PNGs':pngchanged,'all_NT_OAM_protected_upper_RGB_equal':True,'RNG_and_CPU_PPU_state_equal_except_selected_CHR':True}
    report={'work':177,'status':'PASS_FOCUSED_BOOTH_FONT_FIX_AND_ADJACENT_REGRESSION','ROM_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'build_report_sha256':sha(rom.parent/'build_report.json'),'independent_ROM_IPS_rebuild_exact':True,'branches':result,'visual_review':'Human assistant inspected exchange049/050 PNG1710; additional representative snapshots recorded in handoff.','interventions':'Cold boot with recorded initial currency seeds and timed controller input. Native callers thereafter; no state loads or forced PC/ROM writes.','limits':['not full playthrough','not final user language/art approval','old corrupted saved-state is not automatically repaired','live user Mesen not modified'],'fixed_text':['포인트를 티켓으로','바꿔 드릴게요']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':report['status'],'ROM_sha256':report['ROM_sha256'],'branches':{k:{'snapshots':v['paired_snapshots'],'changed_PNGs':v['changed_PNGs']} for k,v in result.items()}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
