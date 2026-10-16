"""Replay the observed clears and derive a bounded camera projection hypothesis."""
from pathlib import Path
import csv,hashlib,json
from verify_dialogue_home import MPU
from verify_gate_font_tag_hooks import Memory

R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def mem(data,bank):
    m=Memory(data);m.banks=[bank,bank+1,0x3e,m.count-1]
    c=MPU(memory=m);m.cpu=c
    return m,c

def project(data,ram,camera=None):
    m,c=mem(data,0x36);m.ram[:2048]=ram
    if camera:
        for a,v in camera.items():m.ram[a]=v
    m.ram[0x1fe:0x200]=bytes.fromhex('ff5f')
    c.pc=0x9582;c.sp=0xfd;c.y=2;c.p=0x30
    trace=[]
    while c.pc!=0x6000:
        trace.append(c.pc);c.step();assert len(trace)<200
    return (c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram)),trace

def main():
    out=R/'qa/reports/river122_validation.json';assert not out.exists()
    q=R/'qa/dialogue/river122_actor2_current047';old=R/'qa/dialogue/river121_current047'
    env=json.loads((q/'environment.json').read_text('utf-8'))
    oe=json.loads((old/'environment.json').read_text('utf-8'))
    assert env['exit_code']==0 and env['frames']==3300 and(q/'trace_complete.txt').read_text()=='3300'
    assert len(rows(q/'river121_injection.csv'))==2
    files={}
    for n,h in env['files'].items():assert sha(q/n)==h;files[(q/n).relative_to(R).as_posix()]=h
    files[(q/'environment.json').relative_to(R).as_posix()]=sha(q/'environment.json')
    raw=0;core=0;png_equal=0;png_exceptions=[]
    for p in sorted(q.glob('frame_*_ram.bin')):
        stem=p.name[:11]
        for suffix in ['_ram.bin','_ppu.bin','_oam.bin','_mapping.csv','_state.txt','.png']:
            n=stem+suffix;assert sha(old/n)==oe['files'][n]
            files[(old/n).relative_to(R).as_posix()]=sha(old/n)
            equal=(q/n).read_bytes()==(old/n).read_bytes()
            if suffix=='.png':
                if equal:png_equal+=1
                else:png_exceptions.append({'name':n,'old_sha256':sha(old/n),'new_sha256':sha(q/n)})
            else:
                assert equal,n
                if suffix=='_state.txt':core+=1
                else:raw+=1
    newnative=rows(q/'river121_native.csv');baseline=rows(old/'river121_native.csv')
    assert newnative==[x for x in baseline if int(x['frame'])<=3300]
    writes=rows(q/'river122_actor2_writes.csv');assert len(writes)==6
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
    src,rom=source.read_bytes(),current.read_bytes()
    assert src[0xd592:0xd627]==rom[0x2d592:0x2d627]
    assert src[0x1f214:0x1f25c]==rom[0x3f214:0x3f25c]
    replay=[]
    for x in writes:
        pc=int(x['pc'],16);store=pc-3;address=int(x['address'],16)
        bank=0x36 if int(x['PRG_relative'],16)<0x30000 else 0x38
        ram=(q/f"actor2write_{int(x['event']):04d}_before_ram.bin").read_bytes()
        assert ram[address]==int(x['before'],16)
        pair=[]
        for data in [src,rom]:
            m,c=mem(data,bank);m.ram[:2048]=ram
            c.pc=store;c.a=int(x['cpu_a'],16);c.x=int(x['cpu_x'],16);c.y=int(x['cpu_y'],16)
            c.sp=int(x['cpu_sp'],16);c.p=int(x['cpu_ps'],16)
            assert bytes(m[store+i]for i in range(3)).hex().upper()==x['preceding3_hex']
            c.step();expected=bytearray(ram);expected[address]=int(x['value'],16)
            assert bytes(m.ram[:2048])==bytes(expected) and c.pc==pc
            pair.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles))
        assert pair[0]==pair[1]
        replay.append({'event':int(x['event']),'native_store_CPU_hex':f'{store:04X}',
                       'address_hex':x['address'],'value_hex':x['value'],'cycles':pair[0][5]})
    ram=(q/'actor2write_0003_before_ram.bin').read_bytes()
    camera={0x68:1,0x6b:0x40,0x69:0x0c,0x6d:0x80}
    projections=[]
    for name,override in [('observed_camera',None),('synthetic_projection_camera',camera)]:
        a,trace=project(src,ram,override);b,t2=project(rom,ram,override)
        assert a==b and trace==t2
        if override:
            assert a[6][0x402]==0xed and a[6][0x422]==2 and a[6][1]==64 and a[6][2]==144
            assert 0xf204 not in trace
        else:
            assert a[6][0x402]==a[6][0x422]==0 and 0x95bf in trace and 0xf204 in trace
        projections.append({'case':name,'cycles':a[5],'sprite_x':a[6][1],'sprite_y':a[6][2],
                            'actor2_art_hex':f'{a[6][0x402]:02X}','actor2_state_hex':f'{a[6][0x422]:02X}',
                            'F204_cleanup_reached':0xf204 in trace,
                            'explicit_model_camera':{f'{k:04X}':f'{v:02X}'for k,v in (override or {}).items()}})
    result={'work':122,'status':'PASS_OBSERVED_NATIVE_CULL_AND_PROJECTION_HYPOTHESIS',
            'source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),
            'Mesen_exit_code':0,'frames':3300,'wrapper_v1_postflight_failed':True,
            'postflight_error_record':'qa/reports/river122_v1_postflight_error.json',
            'baseline121_raw_files_exact':raw,'baseline121_core_files_exact':core,
            'baseline121_PNG_equal':png_equal,'baseline121_PNG_exceptions':png_exceptions,
            'native_rows_exact':len(newnative),'RAM_write_CPU_case_pairs':6,'write_replay':replay,
            'cause_bound':'At actor2 projection, vertical delta0126 clears ED at nativebank36/95BF. Horizontal delta0175 with0572=0 reachesF204 via960F/9614, then F20C clears0422. Native culling in this diagnostic, not a corrupt font or proven natural scene fault.',
            'projection_CPU_case_pairs':2,'projection_cases':projections,
            'frozen_files':files,
            'limits':['Exact observed diagnostic and two supplied CPU projection cases only; no full geometry-domain/global scene proof.',
                      'Synthetic camera values preserve source/current actor2 and yield screen64/144 in CPU model; not yet an actual displayed frame.',
                      'Same two field injections as121 plus read-only callbacks; no additional runtime coordinate/health/time/ROM/state writes.',
                      'v1 wrapper failed after emulator exit0 because it expected a renamed CSV. Runtime and environment retained; v2 fixes postflight/3300input guards without rerunning.',
                      'No build/apply, full natural game, human approval or final release.'],
            'release_eligible':False}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(result['status'],'raw',raw,'core',core,'PNG equal',png_equal,'exceptions',len(png_exceptions))

if __name__=='__main__':main()
