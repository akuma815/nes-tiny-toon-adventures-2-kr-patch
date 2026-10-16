"""049 global page regression, explicitly named current/historical baselines."""
from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
    out=R/'qa/reports/pages130_validation.json';assert not out.exists()
    rompath=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';rom=rompath.read_bytes()
    assert sha(rompath)==json.loads((rompath.parent/'build_report.json').read_text('utf-8'))['output_sha256']
    routes=[('intro','pages130_intro047',6000),('tour','pages130_tour047',3600),('gate','gate091_castle047',5400),('booth','train043_booth_regression',4500),('credits','train043_credits_regression',9000)]
    results={};total=0
    for name,baseline,frames in routes:
        a,b=[R/'qa/dialogue'/d for d in [baseline,f'pages130_{name}049']]
        ae,be=[json.loads((d/'environment.json').read_text('utf-8')) for d in (a,b)]
        assert ae['exit_code']==be['exit_code']==0 and ae['frames']==be['frames']==frames
        for k in ['exe_sha256','lua_sha256','config_sha256','input','intervention']:assert ae[k]==be[k],(name,k)
        if name=='credits':
            for k in ['seed','seed_file_sha256']:assert ae[k]==be[k]
        assert be['rom_sha256']==sha(rompath)
        oldrom=Path(ae['command'][3]);assert sha(oldrom)==ae['rom_sha256']
        for d,e in zip((a,b),(ae,be)):
            assert sha(d/'capture_survey_used.lua')==e['lua_sha256'] and sha(d/'config_used.json')==e['config_sha256']
            for f,h in e['files'].items():assert sha(d/f)==h,f
        oldbytes=oldrom.read_bytes();assert oldbytes[0x3fe63:0x3fe6f]==rom[0x3fe63:0x3fe6f]==bytes.fromhex('e62218a522651b85224c53fe')
        images=sorted(f for f in be['files'] if f.endswith('.png'));assert images==sorted(f for f in ae['files'] if f.endswith('.png'))
        ramdiff=collections.Counter();statediff=collections.Counter();pcpairs=collections.Counter();returnPCpairs=collections.Counter();fonts=collections.Counter();fontframes={};chunks=0
        for f in images:
            stem=f[:-4];frame=int(stem[6:]);ra=(a/(stem+'_ram.bin')).read_bytes();rb=(b/(stem+'_ram.bin')).read_bytes()
            assert ImageChops.difference(Image.open(a/f).convert('RGB'),Image.open(b/f).convert('RGB')).getbbox() is None,(name,f)
            for suffix in ['_ppu.bin','_oam.bin','_mapping.csv']:assert (a/(stem+suffix)).read_bytes()==(b/(stem+suffix)).read_bytes(),(name,f,suffix)
            for i,(x,y) in enumerate(zip(ra,rb)):
                if x!=y:
                    assert i in {0x22,0x1fc,0x1fd,0x1fe},(name,frame,hex(i),x,y);ramdiff[f'{i:04X}']+=1
                    if i==0x1fe:
                        assert x in (0x53,0x55,0x56,0x58,0x5a,0x5c) and y in (0x53,0x55,0x56,0x58,0x5a,0x5c) and ra[0x1ff]==rb[0x1ff]==0xfe
                        returnPCpairs[f'{x:02X}->{y:02X}']+=1
            sa,sb=[dict(s.split('=',1) for s in (d/(stem+'_state.txt')).read_text('utf-8').splitlines()) for d in (a,b)]
            assert sa.keys()==sb.keys()
            for k in sa:
                if sa[k]!=sb[k]:
                    assert k in {'cpu.a','cpu.ps','cpu.pc','memoryManager.openBusHandler.externalOpenBus','memoryManager.openBusHandler.internalOpenBus'},(name,frame,k);statediff[k]+=1
            assert sa['cpu.cycleCount']==sb['cpu.cycleCount'] and sa['cpu.sp']==sb['cpu.sp'] and sa['cpu.x']==sb['cpu.x'] and sa['cpu.y']==sb['cpu.y']
            if sa['cpu.pc']!=sb['cpu.pc']:
                # Mesen reports instruction/operand microcycle PC; retain the exact pairs,
                # bounded to bytes in the identical native wait loop, not opcode starts only.
                assert 0xfe53<=int(sa['cpu.pc'])<0xfe5f and 0xfe53<=int(sb['cpu.pc'])<0xfe5f
                pcpairs[f'{int(sa["cpu.pc"]):04X}->{int(sb["cpu.pc"]):04X}']+=1
            ppu=(b/(stem+'_ppu.bin')).read_bytes()
            for row in rows(b/(stem+'_mapping.csv')):
                if row['kind']=='chr':
                    addr=int(row['cpu_or_ppu_address'],16);offset=int(row['relative_offset'],16)
                    assert ppu[addr:addr+0x400]==rom[0x40010+offset:0x40410+offset],(name,frame,addr);chunks+=1
            fonts[str(rb[0xc6])]+=1;fontframes.setdefault(str(rb[0xc6]),[]).append(frame)
        init_slots={};protected_execs=0
        if (b/'menu_events.csv').exists():
            old=[x for x in rows(a/'menu_events.csv') if x['kind']=='exec'];new=[x for x in rows(b/'menu_events.csv') if x['kind']=='exec'];assert len(old)==len(new)
            for x,y in zip(old,new):
                for key in x:
                    if key in ('cpu_a',):continue
                    assert x[key]==y[key],(name,key,x,y)
                protected_execs+=1
                if y['address']=='9445':init_slots[y['id']]=init_slots.get(y['id'],0)+1
        if name=='intro':assert set(map(str,[128,132,134,136,138,140,142,144,146]))<=fonts.keys()
        if name=='credits':assert {'2D','2E','2F'}<=init_slots.keys()
        results[name]={'frames':frames,'baseline':baseline,'baseline_ROM_sha256':ae['rom_sha256'],'baseline_build_class':'current047' if ae['rom_sha256']=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10' else 'historical043, not current047','whole_PNG_PPU_OAM_mapping_exact':len(images),'actual_CHR_chunks_match049_ROM':chunks,'verified_baseline_files':len(ae['files']),'verified_new_files':len(be['files']),'RAM_differences':dict(ramdiff),'state_difference_keys':dict(statediff),'native_wait_microcycle_PC_pairs':dict(pcpairs),'IRQ_saved_wait_return_PC_pairs':dict(returnPCpairs),'native_execs_protected_fields_equal':protected_execs,'native_init_slots':init_slots,'observed_font_frames':fontframes,'evidence_scope':'All compared pixels/PPU/OAM/mapper and protected page state, with explicit idle RNG/A/flags/stack/bus differences. No claim of identical total CPU state or exact every-IRQ write timing.'}
        total+=len(images)
    # Explicitly preserve the older039 comparison rather than labeling it047.
    historical=R/'qa/dialogue/booth039_tour';fresh=R/'qa/dialogue/pages130_tour047';e=json.loads((fresh/'environment.json').read_text('utf-8'))
    historical_ppu=sum((historical/f).read_bytes()!=(fresh/f).read_bytes() for f in e['files'] if f.endswith('_ppu.bin'))
    assert historical_ppu==19
    result={'work':130,'status':'PASS_BOUNDED_PAGE_REGRESSION_ADOPT_DEVELOPMENT049','adopted_build':'dialogue_kr_poc_049','ROM_sha256':sha(rompath),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'routes':results,'whole_PNG_PPU_OAM_mapping_exact':total,'source_and_prior_builds_preserved':True,'historical039_tour_rawPPU_note':{'differences_to_fresh047':historical_ppu,'decision':'Use fresh047 for rawPPU tour comparison; retain039 original and run-plan. Never enlarge a PPU exclusion to hide earlier-build differences.'},'direct_actual_image_review':'Recorded separately with selected real title/intro/gate/booth/credit frames; not human approval.','human_approved':False,'release_eligible':False,'limits':['Development adoption; human wording/names/graphics/full corpus closure and natural wholegame/hardware/PCM remain pending','RAM22 and native idle PC/flags/IRQ saved values differ with new dispatch; exact whole CPU state/IRQ timestamp is not claimed','Credits selector is an explicit four-field diagnostic, not naturally earned ending','Historical043 booth/credits baselines are correctly named; their matched captured images are not promoted to all-current047 QA','No new builds/apply in130;128 real apply/rebuild retained'],'next_action':'Refresh ROM-free translation/review assets for adopted049, keep047 kits historical and label actual049 images with their seeded/diagnostic scope.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':result['status'],'total_exact_images':total,'routes':{k:v['whole_PNG_PPU_OAM_mapping_exact'] for k,v in results.items()}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
