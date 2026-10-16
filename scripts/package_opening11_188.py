"""ROM-free opening053 PoC package, real Windows8 cases and extractedZIP apply."""
from pathlib import Path
import json,shutil,subprocess,zipfile,re
import seal_nonplay171 as records
from seal_nonplay171 import R,sha
import release_apply_helpers132 as helpers

def j(p):return json.loads(p.read_text('utf-8'))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')

def main():
    records.DATE='2026-10-09'
    name='TinyToonAdventures2_KR_Opening11_PoC053_20261009';patchname=name+'.xdelta'
    out=R/'dist'/name;archive=out.with_suffix('.zip');assert not out.exists() and not archive.exists()
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    target=R/'build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes'
    baseline=R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes'
    validation=R/'qa/reports/opening11_187_validation.json';v=j(validation)
    assert v['status']=='PASS_OPENING11_053_NINE_PAGES_THREE_LOOPS_AND_ADJACENT_REGRESSION'
    assert sha(target)==v['ROM_sha256']=='d27a78ddfd0f8b3d6d46bf1b9db85dbd1d1051bde99ea7eb65a46c5656b53e3c'
    assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(baseline)=='b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24'
    assert sha(R/'workspace/translation/text_ja.csv')=='43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    for n in (186,187):
        for f,h in j(R/f'manifests/nonplay{n}_assets.json')['files'].items():assert sha(R/f)==h,f
    plan=j(target.parent/'opening11_plan.json');a=baseline.read_bytes();b=target.read_bytes()
    changes=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    assert len(a)==len(b)==499728 and len(changes)==24223
    assert all(any(lo<=i<hi for lo,hi in plan['allowed_ranges_vs051']) for i in changes)
    assert a[:16]==b[:16] and a[0x3e010:0x40010]==b[0x3e010:0x40010]
    # Both earlier game fixes are included, without altering their ranges.
    assert a[0x4ba90:0x4bb50]==b[0x4ba90:0x4bb50] # movingSTOP glyphs
    for lo,hi in ((0x10010,0x14010),):assert any(lo<=i<hi for i in changes)
    old=R/'dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008';oldproof=j(R/'qa/reports/nonplay173_package.json')
    out.mkdir()
    for n in ('apply.cmd','tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md'):
        assert sha(old/n)==oldproof['contents_sha256'][n];p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old/n,p)
    shutil.copyfile(R/'workspace/fonts/galmuri11_candidate185/LICENSE.txt',out/'licenses/Galmuri11_v2.40.4_OFL.txt')
    patch=out/patchname
    subprocess.run([str(out/'tools/xdelta3.exe'),'-e','-s',str(source),str(target),str(patch)],check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert sha(old/'apply.ps1')==oldproof['contents_sha256']['apply.ps1']
    oldpatch='TinyToonAdventures2_KR_Review_049_20261006.xdelta';text=(old/'apply.ps1').read_text('utf-8-sig')
    for s,t in ((oldpatch,patchname),(oldproof['contents_sha256'][oldpatch],sha(patch)),(oldproof['ROM_sha256'],sha(target)),('검토용049','오프닝11px PoC053')):
        assert s in text,s;text=text.replace(s,t)
    assert oldpatch not in text and oldproof['ROM_sha256'] not in text
    helpers.windows_text(out/'apply.ps1',text)
    helpers.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처2 일본판 — 오프닝11px PoC053 (2026-10-09)

오프닝9문단에만11px 한글 폰트를 적용한 시험판입니다. 다른 화면은 기존8px입니다.
원본 일본판 NES ROM을 apply.cmd에 드래그하거나 다음처럼 실행하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_Opening11_PoC053.nes"
원본:262160바이트 / SHA-256 {sha(source)}
결과:499728바이트 / SHA-256 {sha(target)}
이름은 달라도 원본의 크기와 전체해시가 같아야 합니다. 기존 한글ROM에 덧씌우지 않습니다.
이미 있는 출력은 덮어쓰지 않습니다. 출력이름을 생략하면 원본이름_KR.nes로 생성됩니다.

Mesen에서 새 결과ROM을 열고 초기화한 뒤 타이틀에서 기다리면 오프닝이 나옵니다.
오프닝9문단의 크기와 줄바꿈을 확인하세요. 문구는 유지하고 긴 문장만 줄바꿈했습니다.
review/review.html에서 각문단의 기존8px/11px 실제Mesen 화면을 비교할 수 있습니다.
두 빌드의 문단 완성시점이 달라 같은프레임의 시간비교는 아닙니다.
한글 획 높이11px, 문자셀12×16입니다. 오프닝 타입표시시간은 기존과 달라집니다.
Start로 건너뛰면 기존처럼 타이틀로 돌아가고 오프닝에 다시 진입합니다.

기존051의 움직이는 ‘정지’ 표지판과050의 티켓교환대사 글꼴수정도 포함합니다.
원본/기준051/기존패키지는 보존했습니다. 다른버전 강제저장상태의 호환은 검증하지 않았습니다.
HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT는 기존 선택대로 원문 유지입니다.

실제검증: 오프닝9문단3회, 출력중/대기/소거2167화면RGB, 상하타일3024기록,
30초기화소거, Start1000/1900 타이틀동일, 기차734전체화면/상태 동일051.
전체놀이기구/완주/음성/하드웨어/전역PRG8도달성/사람의최종폰트승인은 미검증입니다.
전체텍스트11px 전환과 카페완성작업기는 아직 완료하지 않았습니다.
이묶음에는 ROM/세이브가 없습니다. 개인검수용 PoC이며 최종배포본이 아닙니다.
''')
    (out/'RELEASE_NOTES_KO.md').write_text('''# 오프닝11px PoC053

오프닝9문단을 기존 한글 어휘 그대로 Galmuri11 v2.40.4로 키웠다. 한글 실획높이11px·문자셀12×16이며 긴문장은 최대4행으로 줄바꿈한다. 각8px열의 상하타일을 함께 출력하고 원래9행지우기·페이드·대기·문단전환을 유지한다. 출력열 수가 달라 오프닝의 장면시간은 기존과 다르다.

원본 ExpectedWrite/전체diff/IPS적용/독립ROM·IPS재빌드/최종6502검사는 구현186, 실제표시9문단3회/2167부분·대기·소거RGB/3024상하PPUNT소비/30초기화소거와Start분기·기차회귀는 검증187에 묶였다. 이 패키지는 같은053바이트를 적용하는경로만 검증하며 새자동플레이를 실행하지 않았다. 자세한수치와한계는review/validation.json 참조.

053은 오프닝 전용 시험판이며 기준051을 대체하는 전체11px 배포본이 아니다. 다른화면은8px다. 050교환대사수정과051움직이는정지표지판은 포함된다. 실제플레이와최종폰트·문체·명칭·그림검수는 사용자담당이다. PRG8/9의전역도달성/전체게임/오디오·하드웨어/이전버전강제저장호환은 미검증이다. 원문유지6건은그대로이며 카페완성작업기나외부게시를하지않았다.
''','utf-8')
    review=out/'review';shutil.copytree(R/'workspace/review/opening11_187',review)
    for src,dst in ((validation,'validation.json'),(R/'qa/reports/opening11_cpu186.json','CPU_validation.json')):shutil.copyfile(src,review/dst)
    put(review/'layout_and_consumer.json',{'ROM_sha256':sha(target),'font_source':j(R/'workspace/fonts/galmuri11_candidate185/font_source.json'),'cell':[12,16],'Hangul_ink_height':11,'scope':'Opening root7 IDs1..9 only','printer_PC':plan['private_printer_PC'],'reader_PC':plan['private_reader_PC'],'call_sites':plan['call_sites'],'allowed_ranges_vs051':plan['allowed_ranges_vs051'],'pages':[{k:z[k] for k in ('page','entry_id','original_pointer','stream_pointer','NT_top_origin','lines','original_text','font_bank','font_unique_tiles','typewriter_units','height')} for z in plan['pages']]})
    decisions=j(old/'review/scope_decisions.json');assert sha(old/'review/scope_decisions.json')==oldproof['contents_sha256']['review/scope_decisions.json']
    put(out/'scope_policy053.json',{'policy':'Six user-approved original retentions unchanged; opening-only11px development PoC, not final approval.','prior_policy_sha256':sha(old/'review/scope_decisions.json'),'decisions':decisions['decisions'],'source_scope_decisions':decisions['sources'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'current_ROM_sha256':sha(target),'baseline051_sha256':sha(baseline),'change_scope':'Opening9 only. Private PRG8/9 overlay, seven opening callsites and wrapper, nine opening CHR pairs;24223bytes vs051. Header/fixedIRQ/bytes outside declared ranges unchanged.','global_11px':False,'human_final_review':False})
    put(out/'release_report.json',{'name':name,'date':'2026-10-09','status':'DEVELOPMENT_OPENING_ONLY_POC','distribution_eligible':False,'ROM_free':True,'source':{'bytes':source.stat().st_size,'sha256':sha(source)},'target':{'build':'opening11_poc_053','bytes':target.stat().st_size,'sha256':sha(target)},'stable_baseline051_retained':True,'patch':{'file':patchname,'bytes':patch.stat().st_size,'sha256':sha(patch)},'validation':{'file':'review/validation.json','sha256':sha(validation),'scope':'Reused exact053 opening/skip/train187 evidence; no new runtime execution'},'CSV_unchanged':True,'movingSTOP051_glyphs_unchanged':True,'booth_fix050_retained_in_original051':True,'global11px':False,'fullplay_or_human_final_approval':False,'tools_and_licenses_sha256':{p.relative_to(out).as_posix():sha(p) for root in ('tools','licenses') for p in (out/root).rglob('*') if p.is_file()}})
    helpers.PATCH=patchname;helpers.TARGET_SHA=sha(target);helpers.SOURCE_SHA=sha(source)
    qa=R/'qa/release/opening11_188_apply053';proof=helpers.check_apply(out,qa,source,target)
    shutil.copyfile(qa/'apply_verification.json',out/'Windows_apply_verification.json')
    files=sorted(p for p in out.rglob('*') if p.is_file());(out/'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files),'utf-8');files=sorted(p for p in out.rglob('*') if p.is_file())
    assert all(p.suffix.lower() not in {'.nes','.mss','.bin','.ips'} for p in files)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            item=zipfile.ZipInfo(name+'/'+p.relative_to(out).as_posix(),(2026,10,9,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;z.writestr(item,p.read_bytes())
    extracted=qa/'최종 ZIP 추출';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={name+'/'+p.relative_to(out).as_posix() for p in files}
        for p in files:assert z.read(name+'/'+p.relative_to(out).as_posix())==p.read_bytes()
        z.extractall(extracted)
    applied=extracted/'새053 결과.nes';final=helpers.apply(extracted/name,source,extracted,applied)
    assert final['exit_code']==0 and applied.read_bytes()==target.read_bytes(),final
    for p in files:assert (extracted/name/p.relative_to(out)).read_bytes()==p.read_bytes()
    hashfile=archive.with_suffix('.zip.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
    evidence=R/'qa/reports/opening11_188_package.json';put(evidence,{'work':188,'status':'PASS_ROMFREE_OPENING053_WINDOWS8_AND_FINAL_ZIP_APPLY','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'ROM_sha256':sha(target),'source_sha256':sha(source),'files':len(files),'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files},'Windows_helper_checks':proof,'final_ZIP_apply':final,'final_output_sha256':sha(applied),'source_unchanged':sha(source)==helpers.SOURCE_SHA,'baseline051_unchanged':sha(baseline)=='b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24','final_ZIP_payload_unchanged':True,'ROM_free':True,'new_runtime_execution':False,'global11px_or_fullplay_or_human_final_approval':False})
    body=f'''사용자 ‘다시 진행’에따라187인계의패키지작업을재개했다. [053 적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}`, [사용법](../dist/{name}/README_적용방법.txt), [패키지내실제8px/11px 비교](../dist/{name}/review/review.html), [Windows/ZIP검증](../qa/reports/opening11_188_package.json). 원본일본판→오프닝11px PoC053 전체차분이며기존한글ROM에덧씌우지않는다. [대상ROM](../build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes) SHA `{sha(target)}`; 원본SHA `{sha(source)}`. 변경파일/해시는 [188매니페스트](../manifests/nonplay188_assets.json) 및패키지SHA256.txt.

빌드/적용: 실Windows apply.cmd8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로의최종ZIP추출본실적용→byte-exact053 PASS. ZIP CRC/정확한파일목록·모든내용/적용후payload불변/ROM-free PASS. {len(files)}파일에 실제18PNG·HTML·CPU/최종runtime보고·9문단배치·폰트출처·xdelta도구/라이선스·기존Galmuri및새Galmuri11 OFL을포함했다.

정적/빌드/CPU/실제장면검증은 [186](OPENING11_PAIRED_ROW_POC053_BUILD_186.md)·[187](OPENING11_POC053_RUNTIME_HANDOFF_187.md)의동일053SHA에귀속된다. 이작업188은실적용검증이며새Mesen/자동플레이/전체놀이기구실험없음. HTML브라우저렌더검증은미실시. 9문단3회·2167RGB·3024상하소비·30소거·Start분기·734기차동일근거를재사용한다.

기준051/CSV/원본/1편/이전dist와실패자료/사용자Mesen설정·세이브는유지한다. 053은오프닝한글실획11px·12×16셀의PoC이고다른화면8px,전체11px전환미완료다. 타이핑시간차이·전역PRG8도달성·오디오/하드웨어/다른버전강제저장호환·전체플레이/사람의최종폰트승인은남아있다. 원문유지6건그대로,카페완성작업기/외부게시없음.

재현: `python scripts/package_opening11_188.py`. 기존확정출력덮어쓰기방지로현재경로재실행은거부한다. 별도환경에서출력명/QA경로를새롭게설정해동일입력으로재현한다. 원본ROM을apply.cmd에드래그하거나명시적결과이름을지정한후새053을열어초기화하고타이틀에서기다린다.'''
    next_action='188패키지와186/187인계의해시·프로젝트링크·원본/1편보존을확인하고 전체11px의다음적용범위를정리한다.'
    records.seal(188,'OPENING11_POC053_APPLY_PACKAGE_188.md','오프닝11px PoC053 적용패키지·Windows 검증',body,'ROM없는053패키지·Windows8사례·최종ZIP실적용 byte-exact PASS. 오프닝전용범위·9문단비교·폰트라이선스포함;기준051유지.',next_action,[Path(__file__),R/'scripts/release_apply_helpers132.py',evidence,archive,hashfile,*files,qa/'apply_verification.json'])
    p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');s=s.replace('사용자 ‘오늘은 여기까지’ 지시로 중단했다.','사용자 ‘다시 진행’에따라2026-10-09재개해188패키지작업을완료했다.',1).replace('053ROM없는적용ZIP/Windows적용검증은아직없다.',f'[053ROM없는적용ZIP188](../dist/{archive.name})·Windows8사례·최종ZIP실적용 byte-exact PASS. [패키지인계](OPENING11_POC053_APPLY_PACKAGE_188.md).',1);p.write_text(s,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8');s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 재개 / 기준051 유지 / 오프닝11px PoC053·적용패키지188 검증완료. 전체11px 전환과사람검수미완료.**',s,count=1,flags=re.M);p.write_text(s,'utf-8')
    p=R/'README.md';s=p.read_text('utf-8');s=re.sub(r'^> \*\*.*?\*\*[^\n]*','> **2026-10-09 재개 / 작업188 완료 / 기준051 유지 / 오프닝11px PoC053 패키지** [최신 인계](docs/HANDOFF.md)',s,count=1,flags=re.M);p.write_text(s,'utf-8')
    print(json.dumps({'status':'PASS','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'files':len(files),'ROM_sha256':sha(target)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
