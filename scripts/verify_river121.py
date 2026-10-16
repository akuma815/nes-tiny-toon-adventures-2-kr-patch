"""Separate native constructor execution from absent sprite-render evidence."""
from pathlib import Path
import csv, hashlib, json

R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))

def main():
    out=R/'qa/reports/river121_validation.json';assert not out.exists()
    dirs=[R/'qa/dialogue/river121_source',R/'qa/dialogue/river121_current047']
    files={};results=[];normalized=[]
    for q in dirs:
        env=json.loads((q/'environment.json').read_text('utf-8'))
        assert env['exit_code']==0 and env['frames']==4000
        assert (q/'trace_complete.txt').read_text()=='4000'
        for n,h in env['files'].items():
            assert sha(q/n)==h
            files[(q/n).relative_to(R).as_posix()]=h
        files[(q/'environment.json').relative_to(R).as_posix()]=sha(q/'environment.json')
        inj=rows(q/'river121_injection.csv')
        assert len(inj)==2 and {x['frame']for x in inj}=={'3000'}
        assert [(x['address'],x['before'],x['after'])for x in inj]==[('0069','00','0B'),('006D','F5','F0')]
        native=rows(q/'river121_native.csv')
        before=[x for x in native if x['pc']=='A5FD']
        made=[x for x in native if x['pc']=='A642']
        assert len(before)==len(made)==1 and made[0]['actor2_art']=='ED' and made[0]['actor2_state']=='02'
        assert made[0]['bank38']=='3D'
        assembler=[x for x in native if x['pc']=='9643']
        stage=[x for x in assembler if x['cpu_a']in('ED','EE','EF')]
        assert not stage and not rows(q/'river121_render_fetch.csv')
        norm=[]
        for x in native:
            x=dict(x);x['PRG_relative']=f"{int(x['PRG_relative'],16)%(0x20000):05X}"
            norm.append(x)
        normalized.append(norm)
        chunks=0
        for p in sorted(q.glob('frame_*_mapping.csv')):
            ppu=(q/(p.stem.replace('_mapping','')+'_ppu.bin')).read_bytes()
            rom=(R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes').read_bytes() if q==dirs[0] else (R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
            chrbase=16+rom[4]*16384
            for row in rows(p):
                if row['kind']!='chr':continue
                a=int(row['cpu_or_ppu_address'],16);relative=int(row['relative_offset'],16)
                assert ppu[a:a+1024]==rom[chrbase+relative:chrbase+relative+1024]
                chunks+=1
        results.append({'directory':q.relative_to(R).as_posix(),'native_rows':len(native),
                        'native_constructor_A5FD_executions':len(before),'native_actor2_ED_created':True,
                        'observed_ED_EE_EF_assembler_calls':len(stage),'observed_physical_CHR61_render_reads':0,
                        'mapped_1KiB_CHR_chunks_exact':chunks,
                        'sprites_not_present_in_logged_assembler':'No ED/EE/EF calls in injectionFrame..+300; not a global absence statement.'})
    assert normalized[0]==normalized[1]
    baseline=R/'qa/dialogue/stop081_water046';old=json.loads((baseline/'environment.json').read_text('utf-8'))
    current=dirs[1]; raw=0; core=0; png_equal=0; png_exceptions=[]
    for p in sorted(current.glob('frame_*_ram.bin')):
        frame=int(p.name[6:11])
        if frame>3000:continue
        stem=p.name[:11]
        for suffix in ['_ram.bin','_ppu.bin','_oam.bin','_mapping.csv','_state.txt','.png']:
            n=stem+suffix;assert sha(baseline/n)==old['files'][n]
            files[(baseline/n).relative_to(R).as_posix()]=sha(baseline/n)
            equal=(baseline/n).read_bytes()==(current/n).read_bytes()
            if suffix=='.png':
                if equal:png_equal+=1
                else:png_exceptions.append({'frame':frame,'current_sha256':sha(current/n),'baseline_sha256':sha(baseline/n)})
            else:
                assert equal,n
                if suffix=='_state.txt':core+=1
                else:raw+=1
    assert core==100 and raw==400
    report={'work':121,'status':'PASS_NATIVE_DIAGNOSTIC_CONSTRUCTOR_DISPLAY_NOT_CONNECTED',
            'source_sha256':sha(R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'),
            'ROM047_sha256':sha(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'),
            'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),
            'runs':results,'normalized_native_rows_source_current_exact':len(normalized[0]),
            'before_injection_current047_vs_historical046':{'raw_files_exact':raw,'core_files_exact':core,
                                                           'PNG_equal':png_equal,'PNG_exceptions':png_exceptions,
                                                           'historical_environment_sha256':sha(baseline/'environment.json')},
            'frozen_files':files,'direct_assistant_scene_visual':False,
            'limitations':['Exactly two condition-field writes at nativeA5C6 after frame3000; no natural river late-game traversal or wholeplay.',
                           'Native ED creation executed; no ED/EE/EF assembler calls or bank61 pattern reads in the declared300frame observer window. Actual display remains unconnected.',
                           'Zero reads is not a globally unused POW proof; it does not identify the game object or translation need.',
                           'Baseline046 evidence is explicitly historical. Prefix game-state comparisons are bounded to100 captures before intervention; PNG exceptions, if any, kept separate.',
                           'No new ROM build/apply, original/CSV change or human approval.'],
            'release_eligible':False}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(report['status'],'native rows',len(normalized[0]),'prefixPNG equal',png_equal,'exceptions',len(png_exceptions))

if __name__=='__main__':main()
