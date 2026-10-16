"""Offline provenance of frozen162/163 PNG4410; no emulator or modified images."""
from pathlib import Path
import csv,hashlib,json,struct,zlib
import numpy as np
from PIL import Image
from seal_nonplay171 import R,sha,seal

def png_chunks(p):
    b=p.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n'
    pos=8;chunks=[]
    while pos<len(b):
        size=struct.unpack('>I',b[pos:pos+4])[0];kind=b[pos+4:pos+8];payload=b[pos+8:pos+8+size]
        assert zlib.crc32(kind+payload)&0xffffffff==struct.unpack('>I',b[pos+8+size:pos+12+size])[0]
        chunks.append({'type':kind.decode('ascii'),'bytes':size});pos+=size+12
        if kind==b'IEND':break
    assert pos==len(b) and chunks[-1]['type']=='IEND'
    return chunks

def main():
    report=R/'qa/reports/nonplay174_capture_provenance.json';assert not report.exists()
    roots=[R/'qa/dialogue/water162_fish_prediction049',R/'qa/dialogue/water163_held_jump049']
    envs=[json.loads((d/'environment.json').read_text('utf-8')) for d in roots]
    prior=R/'qa/reports/water163_hold_validation.json';old=json.loads(prior.read_text('utf-8'))
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';ssot=R/'workspace/translation/text_ja.csv'
    exe=R/'tools/mesen-2.1.1/Mesen.exe'
    used=[Path(__file__),prior,rom,ssot,exe,R/'scripts/audit_project_links171_v2.py']
    def checked(d,e,name):
        p=d/name;assert sha(p)==e['files'][name];used.append(p);return p
    for d,e in zip(roots,envs):
        assert e['exit_code']==0 and e['rom_sha256']==sha(rom)==old['ROM_sha256']
        assert e['exe_sha256']==sha(exe)
        used.append(d/'environment.json')
        assert checked(d,e,'trace_complete.txt').read_text()==str(e['frames'])
        assert sha(checked(d,e,'capture_survey_used.lua'))==e['lua_sha256']
        assert sha(checked(d,e,'config_used.json'))==e['config_sha256']
    assert envs[0]['input']==envs[1]['input'] and envs[0]['config_sha256']==envs[1]['config_sha256']
    inputs=[list(csv.DictReader(checked(d,e,'adaptive_inputs.csv').open(encoding='utf-8',newline=''))) for d,e in zip(roots,envs)]
    div=next(i for i in range(min(map(len,inputs))) if inputs[0][i]!=inputs[1][i])
    assert div==4644 and inputs[0][div]['frame']==inputs[1][div]['frame']=='4645'
    prefix=[];arrays={};PNGcounts=[]
    for d,e in zip(roots,envs):
        names=sorted(f for f in e['files'] if f.startswith('frame_') and f.endswith('.png') and int(f[6:11])<4645)
        PNGcounts.append(len(names))
        for name in names:
            p=checked(d,e,name);a=np.asarray(Image.open(p).convert('RGB'));assert a.shape==(240,256,3)
            arrays[(d.name,name)]=a
    assert PNGcounts==[343,343]
    a=arrays[(roots[0].name,'frame_04410.png')];b=arrays[(roots[1].name,'frame_04410.png')]
    mask=np.any(a!=b,axis=2);ys,xs=np.where(mask)
    count=int(mask.sum());bbox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
    assert count==7326 and bbox==[8,0,256,189]
    difference=old['prefix_RGB_differences'][0]
    assert sha(roots[0]/'frame_04410.png')==difference['prior_sha256']
    assert sha(roots[1]/'frame_04410.png')==difference['current_sha256']
    raw=[]
    for suffix in ['_ram.bin','_ppu.bin','_oam.bin','_mapping.csv','_state.txt']:
        paths=[checked(d,e,'frame_04410'+suffix) for d,e in zip(roots,envs)]
        assert paths[0].read_bytes()==paths[1].read_bytes()
        raw.append({'suffix':suffix,'bytes':paths[0].stat().st_size,'sha256':sha(paths[0]),'equal':True})
    state=dict(line.split('=',1) for line in (roots[0]/'frame_04410_state.txt').read_text('utf-8').splitlines())
    assert state['frameCount']==state['ppu.frameCount']=='4410'
    assert not any('decoder' in k.lower() or 'filter' in k.lower() or 'renderedframe' in k.lower() for k in state)
    # Same-labelled PNG exceptions remain failures, regardless of nearest-neighbour ranking.
    nearest=[]
    for d,target in zip(roots,[a,b]):
        matches=[]
        for (run,name),candidate in arrays.items():
            if run==d.name and name=='frame_04410.png':continue
            matches.append({'run':run,'file':name,'different_RGB_pixels':int(np.any(target!=candidate,axis=2).sum())})
        matches.sort(key=lambda x:(x['different_RGB_pixels'],x['run'],x['file']))
        exact=[m for m in matches if m['different_RGB_pixels']==0]
        assert not exact
        nearest.append({'target_run':d.name,'search_population':len(matches),'exact_other_saved_PNGs':exact,'nearest':matches[:5]})
    equal=sum(np.array_equal(arrays[(roots[0].name,f)],arrays[(roots[1].name,f)]) for run,f in arrays if run==roots[0].name)
    assert equal==342
    metadata=[]
    for d in roots:
        with Image.open(d/'frame_04410.png') as im:
            assert im.info=={};metadata.append({'run':d.name,'size':list(im.size),'mode':im.mode,'metadata':im.info,'chunks':png_chunks(d/'frame_04410.png')})
    lua=[(d/'capture_survey_used.lua').read_text('utf-8') for d in roots]
    observer=lua[0][lua[0].index('local function snapshot()'):lua[0].index('local sequence={}')]
    assert observer==lua[1][lua[1].index('local function snapshot()'):lua[1].index('local sequence={}')]
    assert "save(tag..'.png',emu.takeScreenshot())" in observer and observer.index('emu.takeScreenshot()')<observer.index("dump(tag..'_ppu.bin'")
    for s in lua:
        assert 'frame=frame+1' in s and 'end,emu.eventType.endFrame)' in s
    src_report=R/'qa/reports/capture118_bounds.json';sources=json.loads(src_report.read_text('utf-8'))['sources']
    treepath=R/'work/capture118/official_tree_2.1.1.json';tree={e['path']:e for e in json.loads(treepath.read_text('utf-8'))['tree']}
    for s in sources:
        p=R/s['local_path'];data=p.read_bytes()
        assert sha(p)==s['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==tree[s['official_path']]['sha']==s['git_blob_sha1']
        used.append(p)
    used.extend([src_report,treepath])
    ppu=(R/'work/context107/NesPpu_2.1.1.cpp').read_text('utf-8')
    section=ppu[ppu.index('template<class T> void NesPpu<T>::SendFrame()'):]
    assert section.index('ProcessEvent(EventType::EndFrame)')<section.index('UpdateFrame(frame, forRewind, forRewind)')
    decoder=(R/'work/capture118/VideoDecoder.cpp').read_text('utf-8')
    wrapper=decoder[decoder.index('void VideoDecoder::TakeScreenshot(std::stringstream &stream)'):]
    assert 'WaitForAsyncFrameDecode' not in wrapper
    result={'work':174,'status':'PASS_OFFLINE_CAPTURE_PROVENANCE_WHOLE_RGB_FAIL_CAUSE_UNRESOLVED',
        'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),'prior163_report_sha256':sha(prior),
        'closed_environments':[{'path':(d/'environment.json').relative_to(R).as_posix(),'sha256':sha(d/'environment.json'),'exit_code':e['exit_code'],'completed_frames':e['frames']} for d,e in zip(roots,envs)],
        'shared_prefix_input_rows':div,'first_input_difference_frame':4645,'target_label':4410,
        'prefix_saved_PNGs_each':343,'RGB_equal_same_label':equal,'RGB_different_same_label':1,
        'target_different_pixels':count,'target_difference_bbox':bbox,'target_raw_pairs':raw,
        'target_equal_RGB_bands':[[189,240]],'target_PNGs':metadata,'nearest_saved_prefix_PNGs':nearest,
        'Lua_snapshot_function_identical':True,'screenshot_before_debug_memory_dumps':True,
        'observed_native_frame_count':4410,'published_filter_frame_identity_recorded':False,
        'pinned_official_sources_git_blob_verified':len(sources),'source_facts':{
            'NES_endframe_precedes_current_frame_submission':True,'screenshot_wrapper_waits_for_async_decode':False},
        'inference':'Async filter scheduling is a possible explanation only; no decoder publication timeline or exact delay exists in these records.',
        'whole_prefix_RGB_equality_passed':False,'exception_cause_closed':False,'translation_defect_proven':False,
        'new_game_or_emulator_execution':False,'human_final_review':False,'release_eligible':False,
        'limits':['No exact saved neighbouring-frame duplicate in686 saved prefix PNGs; uncaptured intervening frames are untested.',
            'CRC-valid PNG and identical native snapshots do not identify which filtered output was copied.',
            'Mutex/source ordering is scoped to pinned2.1.1 source, not a rebuild/installed-binary equivalence proof.',
            'No new run, sleep compensation, screenshot replacement, ROM/CSV or historical evidence changes.']}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');used.append(report)
    body=f'''새 실행 없이 종료된162/163 자료의 frame04410 PNG를 대조했다. 양쪽 environment exit0·trace_complete(10500/18000)·현재049 ROM/개인Mesen SHA·사용Lua/설정/입력 파일을 확인했다. 같은 초기 입력과 적응입력4644행이 같고 첫 입력 차이는4645다.4410의 RAM/PPU/OAM/매핑/core상태5쌍은 바이트 동일하며 native frameCount/ppu.frameCount는4410이다.

종료 environment에 고정된 각343장, 총686개의4645이전 PNG SHA를 확인한 뒤 RGB를 비교했다.342쌍 동일,4410한쌍만7326픽셀/bbox[8,0,256,189] 차이로163결과와 같다. y189..239는 양쪽RGB동일이다. 두 대상마다 자기자신을 제외한685개 저장PNG에서 동일한 복사본은 없었다. 따라서 다른 **저장된** 인접 PNG를 그대로 잘못 저장한 경우는 이 검색 범위에서 연결되지 않는다. 저장하지 않은 사이 프레임의 동일성이나 정확한 지연량을 뜻하지 않는다. 두 PNG는 CRC정상·256×240 RGB이며 메타데이터/출력프레임 식별자를 갖지 않는다. 원본PNG를 보존했다.

양쪽Lua의 snapshot 함수는 동일하고 EndFrame에서 frame을 증가시킨 뒤 PNG를 먼저 캡처하고 debug메모리를 읽는다. 작업118의2.1.1 공식소스6개는 고정트리 Git blob/SHA와 재대조했다. EndFrame 이벤트는 현재프레임 제출보다 먼저이고 screenshot 래퍼는 비동기 디코더 완료를 기다리지 않는다. 필터 복사와ApplyFilter 잠금은118의 제한대로 유지한다. 이 소스 경로는 정확한 출력 프레임 식별/스케줄 기록을 대신하지 않으며 설치바이너리 재빌드 일치 증명도 아니다. 비동기 처리 시점은 가능한 설명일 뿐 이 PNG 차이의 확정 원인이 아니다.

[보고](../qa/reports/nonplay174_capture_provenance.json), [분석기](../scripts/analyze_capture174.py). 결론: 전체prefix RGB동일 판정은 계속FAIL, 원인은미확정이다. 같은native상태만으로 시각 회귀PASS로 바꾸지 않는다.049 번역/패치 결함이 입증된 것도 아니다. 정확한 원인은 기존자료만으로 닫을 수 없으므로 유사 캡처 반복/임의sleep/PNG교체는 진행하지 않는다. 실제 플레이와 최종 품질은 사용자 담당이다.

변경은174분석스크립트·보고·인계/계획/조사/journal/canonical·manifest/audit뿐이다. ROM `{sha(rom)}`, CSV `{sha(ssot)}`,173ZIP 및 모든 기존증거 불변. 정적소스/종료자료/PNG프로브 검증만 수행했고 신규ROM빌드/적용/CPU/에뮬레이터/플레이/청음/최종사람검수 없음. 재현 `python scripts/analyze_capture174.py`; 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay174_assets.json --output qa/reports/nonplay174_session.json`. 기존출력은 보호되므로 새경로를 쓰는복제로 재현한다. 사용파일SHA는manifest와실행environment에고정했다. 카페완성작업기/게시없음.'''
    seal(174,'CURRENT049_OFFLINE_CAPTURE_PROVENANCE_174.md','기존PNG 차이 오프라인 출처 대조',body,
        '종료162/163의343쌍PNG/4410raw5쌍/입력4644행·공식소스6개 재대조. 저장인접PNG동일복사본없음.7326픽셀/전체RGB FAIL·원인미확정 유지; 새게임실행없음.',
        '사용자 검수 결과를 연결할 현재049 점검표와 배포 전 남은 조건을 한 문서로 정리하고, 추가 기술 작업과 사용자 판단 항목을 구분한다.',used)
    print(json.dumps({k:v for k,v in result.items() if k not in ['nearest_saved_prefix_PNGs','target_raw_pairs','target_PNGs']},indent=2))

if __name__=='__main__':main()
