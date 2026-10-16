"""Current049 ROM-free private review; single SSOT change, explicit scene provenance."""
from pathlib import Path
import base64,csv,hashlib,html,json,re,zipfile
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=R/'workspace/review/translation047_20261005';out=R/'workspace/review/translation049_20261006'
    archive=R/'workspace/review/TinyToon2_Translation_Review_049_20261006.zip'
    report=R/'qa/reports/review049_records131.json';assert not out.exists() and not archive.exists() and not report.exists()
    previous=json.loads((old/'artifact_manifest.json').read_text('utf-8'))
    for f,h in previous['files'].items():assert sha(old/f)==h
    x=json.loads((old/'review_records.json').read_text('utf-8'));source=(old/'review.html').read_text('utf-8')
    assert (len(x['units']),len(x['graphics']),len(x['actual_images']))==(54,33,14)
    ssot=R/'workspace/translation/text_ja.csv';by={r['entry_id']:r for r in csv.DictReader(ssot.open(encoding='utf-8-sig',newline=''))}
    changed=[];overrides={v['entry_id']:v['exact_context'] for v in json.loads((R/'workspace/translation/scene_context_105.json').read_text('utf-8'))['context_overrides']}
    for unit in x['units']:
        current=by[unit['entry_id']]
        for key in ['status','source_tokens','raw_sha256','source_sha256','reference_ids','original_view']:assert unit[key]==current[key],(unit['entry_id'],key)
        unit_id=unit['entry_id'];match=re.search(r'<details class="unit" id="'+unit_id+r'">.*?<details>',source,re.S);assert match
        block=match.group(0)
        if unit['translation_ko']!=current['translation_ko']:
            assert unit_id=='MAIN_0590C';changed.append(unit_id)
            before=html.escape(unit['translation_ko']);after=html.escape(current['translation_ko']);assert block.count(before)==1;block=block.replace(before,after)
            note='現在049: 원문의 티켓 부족 안내를 직접 전달하는 한 문장 초안. 전용226/227, 공유196/197·macro정의 보존.009 helper는29/2B의nativeclear전활성폰트를유지하고clear후선택한다.128 build/apply·129 부분/완성/넘김·130 다른page회귀검증. idleRNG/CPU차이는별도한계이며최종사람승인이아니다.'.replace('現在049','현재049')
            oldnote=html.escape(unit['notes']);assert block.count(oldnote)==1
            block=block.replace('삽입 당시 기술 메모: '+oldnote,'현재 삽입 근거: '+html.escape(note))
            unit['historical_notes047']=unit['notes'];unit['current_insertion_context049']=note
            expanded='ざんねんだけど\nチケットがたりないよ';assert html.escape(unit['original_view']) in block
            block=block.replace(html.escape(unit['original_view']),html.escape(expanded));unit['expanded_source_view']=expanded
        if unit_id in overrides:
            frozen=html.escape(unit['scene']+' / '+unit['speaker']);assert block.count(frozen)==1
            block=block.replace(frozen,html.escape(overrides[unit_id]+' / '+unit['speaker']))
            unit['exact_scene_from_context105']=overrides[unit_id]
        source=source[:match.start()]+block+source[match.end():]
        unit['translation_ko']=current['translation_ko'];unit['notes']=current['notes'];unit['notes_scope']='Historical insertion memo in SSOT, not a claim that the original008 remains current. Current049 helper009 scope/idle differences in128..130; selected sentence has explicit current context.'
    assert changed==['MAIN_0590C']
    x.update(ROM_build='dialogue_kr_poc_049',ROM_sha256=sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'),SSOT_sha256=sha(ssot),human_review_complete=False)
    for g in x['graphics']:
        if 'plan' in g:assert sha(R/g['plan'])==g['plan_sha256']
    for img in x['actual_images']:
        assert sha(R/img['path'])==img['sha256']
        img['evidence_scope']='Historical actual '+img['ROM_build']+' image. Preserved as evidence for that build; current049 images are separate. Not a newly executed049 scene or wholeplay proof.'
    additions=[
        ('현재049 타이틀','pages130_intro049',720,'Controller-only cold boot/title; generative title artwork inserted before this work, rechecked in130. Not final artwork approval.'),
        ('현재049 성 입구 조건','pages130_gate049',1920,'Controller-only native zero-gold gate route; no naturally earned successful castle admission.'),
        ('현재049 부족 안내 부분출력','clear129_normal3049',2025,'Initial normal-ticket3 seed; native shortage29 partial printing, not natural currency acquisition.'),
        ('현재049 부족 안내 완성','clear129_normal3049',2100,'Initial normal-ticket3 seed; native shortage29 complete. Private226/227 selected after native clear.'),
        ('현재049 거절 대사 지우기','clear129_normal3049',2604,'Same normal3 seed; retains226 during native clear before possession paragraph, not a mixed-font failure.'),
        ('현재049 다음 보유량 대사','clear129_normal3049',2700,'Same normal3 seed; shared196 restored after clear, displays possession3.'),
        ('현재049 정상 입장 출발','clear129_normal4049',2100,'Initial normal-ticket4 seed; native4→0 charge and start2A. Not naturally earned currency or fullplay.')]
    for label,directory,frame,scope in additions:
        p=R/'qa/dialogue'/directory/f'frame_{frame:05d}.png';env=json.loads((p.parent/'environment.json').read_text('utf-8'))
        assert env['rom_sha256']==x['ROM_sha256'] and sha(p)==env['files'][p.name]
        x['actual_images'].append({'label':label,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'type':'Actual native emulator PNG','ROM_build':x['ROM_build'],'ROM_sha256':x['ROM_sha256'],'intervention':env['intervention'],'evidence_scope':scope})
    assert len(x['actual_images'])==21
    x['limits']=['Human wording/names/graphics approval remains pending; no automatic approval','Registered54units/33graphics are bounded inventories, not global corpus or whole-game percentage','21 actual images:14 historical043/045/046/047 and7 current049 with exact seed/controller scopes','048 completed text passed but transition font mixing was rejected;049 native post-clear selection fixed the observed defect','049 extra38page cycles change idleRAM22/CPU flags/microPC; bounded captured pixels/protected state match, not whole CPU or global gameplay identity','Natural wholeplay/hardware/PCM/all branches not complete; historical state/reset/audio checks remain scoped to their own builds','HOWTO/PAUSE/commonPOW and dormant diagnostic candidates remain unresolved; no global unused decision','No final release or Cafe article; archive contains no ROM/patch/font/emulator']
    for name in ['shortage126_validation.json','shortage127_observation.json','clear128_validation.json','clear129_validation.json','pages130_validation.json','pages130_direct_scene.json']:
        x['technical_reports'][name]=sha(R/'qa/reports'/name)
    x['context_ledger105_sha256']=sha(R/'workspace/translation/scene_context_105.json')
    x['artifact_policy']='ROM-free private review for adopted development049. Human approval false. Historical screenshots/insertion memos retain named-build provenance.'
    source=source.replace('047 사람 검토자료','049 사람 검토자료').replace('검토자료047','검토자료049')
    paragraph=re.search(r'<p>현재047에는.*?</p>',source,re.S);assert paragraph
    replacement='<p>현재049의 본문45초안·9기술공유와 그림33문구를 검토합니다. 일반 티켓 부족 안내 한 문장을 원문에 맞춰 다듬었습니다. 사진21개 중14개는043/045/046/047의 역사적 실제 화면이고, 나머지7개는049에서 새로 실행한 타이틀·성 입구·거절 대사의 부분출력/완성/지우기/다음 보유량·출발 화면입니다. 초기 티켓 seed와 controller 실행을 구분했으며, 전체 자연 플레이와 최종 사람 승인을 의미하지 않습니다.</p>'
    source=source[:paragraph.start()]+replacement+source[paragraph.end():]
    gallery='<div class="gallery">'
    for img in x['actual_images']:
        encoded=base64.b64encode((R/img['path']).read_bytes()).decode()
        gallery+=f'<figure><img alt="{html.escape(img["label"])}" src="data:image/png;base64,{encoded}"><figcaption>{html.escape(img["label"])} · 실제 {html.escape(img["ROM_build"])}<br>{html.escape(img["evidence_scope"])}<br>{html.escape(img["path"])}</figcaption></figure>'
    gallery+='</div>';source,n=re.subn(r'<div class="gallery">.*?</div>',lambda _:gallery,source,count=1,flags=re.S);assert n==1
    source=source.replace('전체 자연플레이/실기/PCM 청음은 미완료이며','현재049의 page 초기화에는38cycles 추가가 있으며 idle 난수용 값/CPU 대기상태 차이가 남습니다. 전체 자연플레이/실기/PCM 청음은 미완료이며')
    assert '티켓을 더 모아줘!' not in source and '티켓이 부족해!' in source and source.count('<details class="unit"')==54
    out.mkdir();(out/'review.html').write_text(source,'utf-8');(out/'review_records.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')
    pending=(old/'DECISIONS_PENDING.md').read_text('utf-8');pending='현재 개발049 검토, 사람 최종승인 미완료. 아래 이전046/047 문구는 당시 기록입니다.\n\n'+pending+'\n\n작업131: MAIN0590C는 ‘아쉽지만 / 티켓이 부족해!’ 초안으로 수정. 크레딧 PACKAGE D. 직함의 정확한 표현, 고유명사/말투, HOWTO/PAUSE/POW 그림범위, 자연전체플레이/실기/PCM/정식배포 결정은 보류합니다. 사람 결정은 문구ID·수정 전후·이유·장면과 함께 기록합니다. 이 파일은 승인 응답이 아닙니다.\n';(out/'DECISIONS_PENDING.md').write_text(pending,'utf-8')
    (out/'README.txt').write_text('타이니툰2 현재개발049 사람검토자료\nreview.html: 오프라인PNG21(역사14/현재0497)·본문54원천·그림33문구. 모든 초안/그림 최종사람승인 미완료. 한 문장 수정과clear이후폰트선택을 반영. 현재/역사화면·seed/diagnostic 조건과idleRNG/CPU차이를records에보존. ROM/패치/폰트/에뮬레이터 없는 검토ZIP. 전체완주/정식배포/카페작업기 아님.\n','utf-8')
    manifest={'work':131,'ROM_build':x['ROM_build'],'ROM_sha256':x['ROM_sha256'],'SSOT_sha256':x['SSOT_sha256'],'ROM_free':True,'human_review_complete':False,'registered_units':54,'graphics':33,'actual_images':21,'changed_unit':['MAIN_0590C'],'files':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}}
    (out/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(out.iterdir()):z.write(p,(Path(out.name)/p.name).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==5
        assert all(Path(f).suffix in ('.html','.json','.md','.txt') for f in z.namelist())
        for p in out.iterdir():assert z.read((Path(out.name)/p.name).as_posix())==p.read_bytes()
    result={'work':131,'status':'PASS_RECORDS_AND_ROMFREE_ZIP_RENDER_PENDING','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'units':54,'graphics':33,'actual_images':21,'historical_images':14,'current049_images':7,'changed_units':changed,'ROM_sha256':x['ROM_sha256'],'SSOT_sha256':x['SSOT_sha256'],'source_tokens_status_and_raw_hashes_equal_SSOT':True,'scene_context105_overrides':['MAIN_057AC','MAIN_05920'],'human_review_complete':False,'ROM_free':True,'render':'pending separate headless browser UI check','scope':'Private review reader; no Cafe article/post or formal release.'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
