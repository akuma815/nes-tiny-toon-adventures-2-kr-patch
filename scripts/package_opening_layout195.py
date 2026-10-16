"""ROM-free user-directed055 page6, realWindows8 andfinalZIP apply."""
from pathlib import Path
import json,shutil,subprocess,zipfile,re
import seal_nonplay171 as records
from seal_nonplay171 import R,sha
import release_apply_helpers132 as helpers

def j(p):return json.loads(p.read_text('utf-8'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')

def main():
    records.DATE='2026-10-09';name='TinyToonAdventures2_KR_Opening11_PoC055_Layout6_20261009';patchname=name+'.xdelta';out=R/'dist'/name;archive=out.with_suffix('.zip');assert not out.exists() and not archive.exists()
    target=R/'build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes';source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';prior=R/'build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes';validation=R/'qa/reports/opening11_194_validation.json';v=j(validation)
    assert v['status']=='PASS_OPENING11_055_NINE_PAGES_THREE_LOOPS_USER_PAGE6_LAYOUT' and sha(target)==v['ROM_sha256']=='8346499ca4240ffad350e3977f792735563779b8c749744a8d9b413ea0b44086'
    assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    for work in (193,194):
        for f,h in j(R/f'manifests/nonplay{work}_assets.json')['files'].items():assert sha(R/f)==h,f
    plan=j(target.parent/'opening11_plan.json');a=prior.read_bytes();b=target.read_bytes();diff=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    assert len(diff)==508 and all(any(lo<=i<hi for lo,hi in plan['allowed_ranges_vs053']) for i in diff)
    assert a[:16]==b[:16] and a[0x24010:0x40010]==b[0x24010:0x40010] and a[0x4ba90:0x4bb50]==b[0x4ba90:0x4bb50]
    old=R/'dist/TinyToonAdventures2_KR_Opening11_PoC053_20261009';proof188=j(R/'qa/reports/opening11_188_package.json');out.mkdir()
    copied=['apply.cmd','tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md','licenses/Galmuri11_v2.40.4_OFL.txt']
    for n in copied:
        assert sha(old/n)==proof188['contents_sha256'][n];p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old/n,p)
    patch=out/patchname;subprocess.run([str(out/'tools/xdelta3.exe'),'-e','-s',str(source),str(target),str(patch)],check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert sha(old/'apply.ps1')==proof188['contents_sha256']['apply.ps1'];text=(old/'apply.ps1').read_text('utf-8-sig');oldpatch=old.name+'.xdelta'
    for before,after in ((oldpatch,patchname),(proof188['contents_sha256'][oldpatch],sha(patch)),(proof188['ROM_sha256'],sha(target)),('오프닝11px PoC053','오프닝11px PoC055')):
        assert before in text; text=text.replace(before,after)
    helpers.windows_text(out/'apply.ps1',text)
    helpers.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처2 일본판 — 오프닝11px PoC055 / 문단6 배치조정 (2026-10-09)

원본 일본판ROM을apply.cmd에드래그하거나다음처럼실행하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_Opening11_PoC055.nes"
원본:262160바이트 / SHA-256 {sha(source)}
결과:499728바이트 / SHA-256 {sha(target)}
기존한글ROM에덧씌우지않습니다. 기존출력은덮어쓰지않습니다.
결과이름생략시원본이름_KR.nes로생성됩니다.

새055ROM을Mesen에서열어초기화한뒤타이틀에서기다리면오프닝이나옵니다.
6문단은다음처럼배치했습니다.
  친구들도 데려와!
  깜짝 놀랄 거다!

                         의문의 대부호로부터
앞두줄은가운데,빈줄뒤서명은한줄오른쪽정렬입니다. 갈무리11폰트와원래어휘는같습니다.
review/review.html의맨위에같은frame02199의053수정전/055수정후실제화면이있습니다.
아래9문단8px/11px비교는각완성시점캡처로같은프레임의시간비교가아닙니다.

11px는오프닝9문단에만적용했습니다. 다른화면은기존8px입니다.
053대비6문단타일/폰트508바이트만변경했습니다. 코드/본문길이/제어위치/다른8문단은같습니다.
기준051/기존053/미실행054홈후보는보존했으며054는이패키지에포함하지않았습니다.
기존050티켓교환대사수정과051움직이는‘정지’표지판은포함됩니다.

055새실행:오프닝9문단3회·2167부분/대기/소거RGB·3024상하vblank전송·30초기화소거PASS.
053같은프레임2318쌍:2086전체PNG동일,232는6문단글자영역만변경.
055의Start/기차회귀는새실행하지않았습니다. 053에서확인한자료는그버전의역사근거입니다.
전체플레이/전체텍스트11px/최종사람폰트승인/오디오·하드웨어/다른버전저장상태호환은미완료입니다.
HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는기존선택대로원문유지입니다.
이것은ROM없는개인검수용오프닝PoC이며최종배포본·카페완성작업기가아닙니다.
''')
    (out/'RELEASE_NOTES_KO.md').write_text('''# 오프닝11px PoC055 — 요청6문단 배치

사용자요청에따라6문단을‘친구들도데려와!’/‘깜짝놀랄거다!’/빈줄/‘의문의대부호로부터’로배치하고서명한줄을오른쪽에맞췄다. 원래어휘/갈무리11은유지했다. 053대비508바이트만바뀌고코드/대기제어위치/문단길이/다른8문단은같다. 054홈후보는포함하지않았다.

immutable원본ExpectedWrite/전체diff/실제IPS/독립ROM·IPS재빌드/최종CPU는193,새실제055오프닝9000프레임검사는194에귀속된다. 9문단3회·2167RGB·3024상하PPUNT소비·30소거PASS. 053동일프레임2318쌍의2086전체PNG동일,232는6문단영역만변경. 새055Start/기차/전체게임실행은없다. 해당053검증을055실행으로재명명하지않는다.

현재는오프닝전용PoC다. 전체텍스트11px/홈054실제소비/최종사람폰트·문구·명칭·그림승인/전체플레이/하드웨어·오디오/버전간강제저장호환/전역PRG8미사용증명은미완료다. 050교환대사/051정지표지판을포함하고원문유지6건·타이틀그림은그대로다. 외부게시하지않았다.
''','utf-8')
    review=out/'review';shutil.copytree(R/'workspace/review/opening11_194',review)
    for src,dst in ((validation,'validation.json'),(R/'qa/reports/opening_layout193_cpu.json','CPU_validation.json'),(R/'workspace/translation/opening_layout_override193.json','page6_layout_request.json')):shutil.copyfile(src,review/dst)
    z=plan['pages'][5];put(review/'layout_and_consumer.json',{'ROM_sha256':sha(target),'font_source':j(R/'workspace/fonts/galmuri11_candidate185/font_source.json'),'font_bank':140,'cell':[12,16],'page6':{k:z[k] for k in ('entry_id','original_text','lines','line_alignments','line_left_pixels','font_unique_tiles','stream_pointer','NT_top_origin','typewriter_units')},'allowed_ranges_vs053':plan['allowed_ranges_vs053'],'other8pages_preserved':True})
    policy=j(old/'scope_policy053.json');policy['current_ROM_sha256']=sha(target);policy['change_scope']='Page6layoutonly508bytes vs053, allcode/other8pages unchanged. Complete source-to055 patch includes prior053opening and051base.';policy['user_page6_layout_request']='review/page6_layout_request.json';put(out/'scope_policy055.json',policy)
    put(out/'release_report.json',{'name':name,'date':'2026-10-09','status':'DEVELOPMENT_OPENING_ONLY_POC_USER_PAGE6_LAYOUT','distribution_eligible':False,'ROM_free':True,'source':{'bytes':source.stat().st_size,'sha256':sha(source)},'target':{'build':'opening11_poc_055','bytes':target.stat().st_size,'sha256':sha(target)},'patch':{'file':patchname,'bytes':patch.stat().st_size,'sha256':sha(patch)},'validation':{'file':'review/validation.json','sha256':sha(validation),'scope':'Actual055opening194; no fresh55skip/train. Packaging has no new runtime.'},'home054_included':False,'stable_baseline051_retained':True,'global11px_or_fullplay_or_human_final_approval':False,'prior053_retained':True,'user_page6_layout_implemented':True,'tools_and_licenses_sha256':{n:sha(out/n) for n in copied if n!='apply.cmd'}})
    helpers.PATCH=patchname;helpers.TARGET_SHA=sha(target);helpers.SOURCE_SHA=sha(source);qa=R/'qa/release/opening11_195_apply055';proof=helpers.check_apply(out,qa,source,target);shutil.copyfile(qa/'apply_verification.json',out/'Windows_apply_verification.json')
    files=sorted(p for p in out.rglob('*') if p.is_file());(out/'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files),'utf-8');files=sorted(p for p in out.rglob('*') if p.is_file());assert all(p.suffix.lower() not in {'.nes','.mss','.bin','.ips'} for p in files)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            item=zipfile.ZipInfo(name+'/'+p.relative_to(out).as_posix(),(2026,10,9,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;z.writestr(item,p.read_bytes())
    extracted=qa/'최종 ZIP 추출';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={name+'/'+p.relative_to(out).as_posix() for p in files}
        for p in files:assert z.read(name+'/'+p.relative_to(out).as_posix())==p.read_bytes()
        z.extractall(extracted)
    result=extracted/'새055 결과.nes';final=helpers.apply(extracted/name,source,extracted,result);assert final['exit_code']==0 and result.read_bytes()==target.read_bytes(),final
    for p in files:assert (extracted/name/p.relative_to(out)).read_bytes()==p.read_bytes()
    hashfile=archive.with_suffix('.zip.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii');evidence=R/'qa/reports/opening11_195_package.json'
    put(evidence,{'work':195,'status':'PASS_ROMFREE_OPENING055_WINDOWS8_FINAL_ZIP_APPLY','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'ROM_sha256':sha(target),'source_sha256':sha(source),'files':len(files),'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files},'Windows_helper_checks':proof,'final_ZIP_apply':final,'final_output_sha256':sha(result),'source_unchanged':sha(source)==helpers.SOURCE_SHA,'final_ZIP_payload_unchanged':True,'ROM_free':True,'new_runtime_execution':False,'global11px_fullplay_or_human_final_approval':False})
    body=f'''[ユーザー調整055パッケージ](../dist/{archive.name})'''
    body=f'''사용자문단6요청을반영한 [055적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}`를만들었다. [사용법](../dist/{name}/README_적용방법.txt), [053/055 6문단실제비교](../dist/{name}/review/review.html), [실적용보고](../qa/reports/opening11_195_package.json). 원본일본판→055전체차분이며기존한글ROM에덧씌우지않는다. ROM SHA `{sha(target)}`,원본SHA `{sha(source)}`. 변경파일전체SHA는 [195매니페스트](../manifests/nonplay195_assets.json).

Windows8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로의최종ZIP추출본apply.cmd→byte-exact055 PASS. ZIP CRC/파일목록/전내용exact/적용후payload불변/ROM-free PASS. {len(files)}파일에실제9문단PNG와동일시점053수정전PNG·검증보고·CPU·레이아웃요청·폰트/xdelta라이선스를포함했다.

코드/입력별실제검증은193/194의정확한055에연결한다. 이작업은패키지실적용이며새에뮬레이터/플레이없다. 054홈후보는포함하지않는다. 기준051/053패키지/054후보/원본/1편/CSV/사용자Mesen/세이브보존. 전체11px/사람최종승인/전체플레이/055Start·기차신규검수/하드웨어·오디오·세이브호환미완료다. 원문유지6건그대로,카페완성작업기/외부게시없음.

재현: `python scripts/package_opening_layout195.py`는기존출력을덮어쓰지않는다. 새출력명/QA경로를정한별도복제에서재현한다. 사용자검수는원본을apply.cmd에넣고새055를초기화한뒤타이틀에서기다려6문단을확인한다.'''
    records.seal(195,'OPENING11_PAGE6_LAYOUT_POC055_PACKAGE_195.md','요청6문단 조정055 패키지·Windows 실적용',body,'ROM없는055사용자배치조정판·Windows8/최종ZIP실적용 exact PASS.053/055동일프레임비교·라이선스포함;054미포함.', '055패키지·193/194의고정근거·인계링크/원본보존을감사하고재개표지를갱신한다.',[Path(__file__),R/'scripts/release_apply_helpers132.py',evidence,archive,hashfile,*files,qa/'apply_verification.json'])
    f=R/'docs/LOCALIZATION_WORK_PLAN.md';s=f.read_text('utf-8').replace('현재 개발049 / 작업195','기준051 / 문단6조정055패키지 / 작업195',1);f.write_text(s,'utf-8');print(json.dumps({'status':'PASS','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'files':len(files)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
