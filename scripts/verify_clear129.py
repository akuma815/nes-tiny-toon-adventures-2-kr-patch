"""Actual049 shortage lifecycle, protected pixels/state, successful entry; RNG scoped."""
from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def csvrows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
    out=R/'qa/reports/clear129_validation.json';assert not out.exists()
    rom=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes()
    assert hashlib.sha256(rom).hexdigest()==j('build/dialogue_kr_poc_049/build_report.json')['output_sha256']
    oldrom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
    # Native fixed-bank wait loop: each19 cycles adds 1+RAM1B (mod256) to RAM22.
    loop=bytes.fromhex('e6 22 18 a5 22 65 1b 85 22 4c 53 fe')
    assert rom[0x3fe63:0x3fe6f]==oldrom[0x3fe63:0x3fe6f]==loop
    mapping=j('build/dialogue_kr_poc_049/shortage_editorial_mapping.json')
    glyphs={x['code']:x['char'] for x in mapping['glyphs']};glyphs[0]=' '
    results={}
    for tag,baseline in [('normal3','context106_normal3047'),('normal4','context107_normal4047')]:
        old=R/'qa/dialogue'/baseline;new=R/'qa/dialogue'/f'clear129_{tag}049'
        oe,ne=[json.loads((d/'environment.json').read_text('utf-8')) for d in (old,new)]
        assert oe['exit_code']==ne['exit_code']==0 and oe['frames']==ne['frames']==4200
        for k in ['exe_sha256','lua_sha256','config_sha256','input','seed','seed_file_sha256']:assert oe[k]==ne[k]
        for d,e in zip((old,new),(oe,ne)):
            for f,h in e['files'].items():assert sha(d/f)==h,f
        frames=sorted(int(f.split('_')[1]) for f in ne['files'] if f.endswith('_ram.bin'))
        oldevents=csvrows(old/'menu_events.csv');events=csvrows(new/'menu_events.csv')
        oldexec=[x for x in oldevents if x['kind']=='exec'];execs=[x for x in events if x['kind']=='exec']
        assert len(oldexec)==len(execs)
        for x,y in zip(oldexec,execs):
            for k in ['frame','address','id','pointer','profile','return_bank','sp','pc','phase','ride','head_font','gold_tickets','points_low','normal_ticket0','normal_ticket1','normal_ticket2','cpu_a','caller']:assert x[k]==y[k],(tag,k,x,y)
        inits=[x for x in execs if x['address']=='9445'];weights=[]
        for x in inits:
            frame=int(x['frame']);n=next(f for f in frames if f>frame);r=(new/f'frame_{n:05d}_ram.bin').read_bytes()
            # Lua EndFrame label f precedes CPU execution in rendered f+1.
            # Infer this call's frame counter from the next snapshot, explicitly not live call telemetry.
            counter=(r[0x1b]-(n-frame-1))%256
            weights.append({'frame_label':frame,'inferred_RAM1B':counter,'next_snapshot_frame':n,'extra_idle_skips':2,'counter_delta_mod256':(-2*(counter+1))%256})
        rama=collections.Counter();values={};states=collections.Counter();pngchange=[];equalPNG=0;chrchunks=0;ntchange=0;rngcases=0
        for frame in frames:
            stem=f'frame_{frame:05d}';a=(old/(stem+'_ram.bin')).read_bytes();b=(new/(stem+'_ram.bin')).read_bytes()
            assert a[0x1b]==b[0x1b]
            expected_delta=sum(w['counter_delta_mod256'] for w in weights if w['frame_label']<frame)%256
            assert (b[0x22]-a[0x22])%256==expected_delta,(tag,frame,b[0x22],a[0x22],expected_delta)
            rngcases+=1
            for i,(x,y) in enumerate(zip(a,b)):
                if x!=y:
                    rama[i]+=1;values.setdefault(i,set()).add((x,y))
                    allowed={0x22,0x1fc,0x1fd} if tag=='normal4' else {0x22,0x1fc,0x1fd,0x1f1,0x103,0xc6,0x6f3,*range(0x740,0x74a)}
                    assert i in allowed,(tag,frame,hex(i),x,y)
            sa=dict(s.split('=',1) for s in (old/(stem+'_state.txt')).read_text('utf-8').splitlines());sb=dict(s.split('=',1) for s in (new/(stem+'_state.txt')).read_text('utf-8').splitlines())
            assert sa.keys()==sb.keys()
            for k in sa:
                if sa[k]!=sb[k]:
                    states[k]+=1
                    assert k in {'cpu.a','cpu.ps','memoryManager.openBusHandler.externalOpenBus','memoryManager.openBusHandler.internalOpenBus',*(f'mapper.chrMemoryOffset{i}' for i in range(8))},(tag,frame,k)
            assert sa['cpu.pc']==sb['cpu.pc'] and sa['cpu.cycleCount']==sb['cpu.cycleCount'] and sa['cpu.sp']==sb['cpu.sp']=='255'
            assert (old/(stem+'_oam.bin')).read_bytes()==(new/(stem+'_oam.bin')).read_bytes()
            ap=(old/(stem+'_ppu.bin')).read_bytes();bp=(new/(stem+'_ppu.bin')).read_bytes()
            if tag=='normal4':assert ap==bp
            else:
                protected=bytearray(bp);protected[:0x800]=ap[:0x800]
                for alias in (0,0x800,0x1000,0x1800):
                    for addr,width in [(0x22a8,10),(0x22e8,11)]:protected[addr+alias:addr+alias+width]=ap[addr+alias:addr+alias+width]
                assert protected==ap,(frame,'outside admitted font/NT aliases')
                ntchange+=int(ap[0x2000:0x3000]!=bp[0x2000:0x3000])
            for row in csvrows(new/(stem+'_mapping.csv')):
                if row['kind']=='chr':
                    addr=int(row['cpu_or_ppu_address'],16);offset=int(row['relative_offset'],16)
                    assert bp[addr:addr+0x400]==rom[0x40010+offset:0x40410+offset];chrchunks+=1
            ai,bi=[Image.open(d/(stem+'.png')).convert('RGB') for d in (old,new)];diff=ImageChops.difference(ai,bi);box=diff.getbbox()
            if box:
                assert tag=='normal3' and 2019<=frame<=2604,(tag,frame,box)
                # Same first line and ticket prefix are protected: only revised second-line pixels.
                diff.paste(0,(80,179,152,187));assert diff.getbbox() is None,(frame,'outside changed second line')
                pngchange.append({'frame':frame,'bbox':box})
            else:equalPNG+=1
        if tag=='normal3':
            assert equalPNG==261 and len(pngchange)==41
            wanted={(2000,'9445'):196,(2001,'9445'):196,(2008,'9445'):226,(2600,'9445'):226,(2607,'9445'):196}
            for (frame,addr),font in wanted.items():
                e=next(x for x in execs if int(x['frame'])==frame and x['address']==addr)
                assert int(e['font'],16)==int(e['active_font'],16)==font
            ppu=(new/'frame_02100_ppu.bin').read_bytes();actual=[]
            for addr,line in zip((0x22a8,0x22e8),mapping['layout']):
                lineactual=''.join(glyphs[x] for x in ppu[addr:addr+line['expanded_tiles']]);assert lineactual==line['desired'];actual.append(lineactual)
            assert (new/'frame_02004.png').read_bytes()==(old/'frame_02004.png').read_bytes()
            assert (new/'frame_02700.png').read_bytes()==(old/'frame_02700.png').read_bytes()
            for frame,font in [(2004,196),(2100,226),(2604,226),(2700,196)]:
                b=(new/f'frame_{frame:05d}_ram.bin').read_bytes();assert b[0xc6]==b[0x6f3]==font and b[0x7d0:0x7d3]==bytes([3,0,0])
        else:
            assert equalPNG==302 and not pngchange
            assert (new/'frame_01998_ram.bin').read_bytes()[0x7d0:0x7d3]==bytes([4,0,0])
            assert (new/'frame_02001_ram.bin').read_bytes()[0x7d0:0x7d3]==bytes(3)
            assert (new/'frame_02100_ppu.bin').read_bytes()[0x22a8:0x22b0]==bytes.fromhex('00 37 38 6c 7a 7a 7a 7a')
            for frame in frames:
                if frame>=3000:
                    b=(new/f'frame_{frame:05d}_ram.bin').read_bytes();assert b[0x18]==4 and b[0x54]==5
        results[tag]={'baseline_historical':baseline,'frames':4200,'verified_declared_files_each':len(ne['files']),'PNG_exact':equalPNG,'second_row_changed_PNGs':pngchange,'OAM_all_exact':len(frames),'mapped_CHR_chunks_ROM_exact':chrchunks,'native_exec_count':len(execs),'native_exec_protected_fields_equal':True,'RAM_difference_offsets':{f'{i:04X}':n for i,n in sorted(rama.items())},'RAM1F1_unused_stack_pairs':sorted(values.get(0x1f1,[])),'state_difference_keys':dict(states),'weighted_idle_RAM22_model_matches_snapshots':rngcases,'inferred_counter_records':weights,'counter_model_scope':'Counter values inferred from next completed snapshots and local EndFrame→next CPU-frame convention; not new direct helper/IRQ cycle telemetry. Same source idle loop and38/19=2 skip model predicts all302 RAM22 differences. Does not prove global gameplay equivalent.'}
    result={'work':129,'status':'PASS_BOUNDED049_SHORTAGE_LIFETIME_AND_SUCCESS_BRANCH_WITH_RNG_DIFFERENCE','candidate049_sha256':hashlib.sha256(rom).hexdigest(),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'routes':results,'direct_actual_images':{'normal3':[2004,2025,2100,2604,2700],'normal4':[2100,3000]},'direct_observation':'Prior fee remains readable during clearing; partial/complete shortage is readable; next possession restores shared196 after clear. Successful ticket4 charge/start/play screens match historical047 completely.','adopted_build':'dialogue_kr_poc_047','candidate049_pending_broader_pages':True,'human_approved':False,'limits':['Source/current all-game state is not identical; RAM22 plus idle CPU/saved flags/bus differ with added38 cycles','Global helper change requires title/intro/other page regression before development adoption','No new build/apply;128 evidence retained','Seeded initial currency, not natural wholeplay/hardware/PCM/final human approval','Screenshot timing claim remains bounded to captured comparisons'],'next_action':'Run049 title/nine intro and home/booth/gate/credits page paths; compare existing frozen baselines with exact protected pixels and scoped native state, then decide development adoption.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':result['status'],'routes':{k:{n:v[n] for n in ['frames','PNG_exact','OAM_all_exact','weighted_idle_RAM22_model_matches_snapshots']} for k,v in results.items()}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
