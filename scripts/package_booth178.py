"""ROM-free050 issue fix package; real Windows helper8 checks and final ZIP apply."""
from pathlib import Path
import json,shutil,subprocess,zipfile
from seal_nonplay171 import R,sha,seal
import release_apply_helpers132 as helpers

def j(p):return json.loads(p.read_text('utf-8'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')
def main():
    name='TinyToonAdventures2_KR_Review_050_BoothFix_20261008';patchname='TinyToonAdventures2_KR_Review_050_20261008.xdelta'
    out=R/'dist'/name;archive=out.with_suffix('.zip');assert not out.exists() and not archive.exists()
    target=R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes';source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    validation=R/'qa/reports/issue177_validation.json';assert j(validation)['status']=='PASS_FOCUSED_BOOTH_FONT_FIX_AND_ADJACENT_REGRESSION' and sha(target)==j(validation)['ROM_sha256']
    old=R/'dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008'
    oldproof=j(R/'qa/reports/nonplay173_package.json')
    out.mkdir()
    # Copy only immutable explicitly recorded files, never a user-applied ROM in old folder.
    for n in ['apply.cmd','tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md']:
        assert sha(old/n)==oldproof['contents_sha256'][n];p=out/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((old/n).read_bytes())
    for n,h in oldproof['contents_sha256'].items():
        if n.startswith('review/'):
            assert sha(old/n)==h;p=out/'review049_historical'/n[7:];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((old/n).read_bytes())
    patch=out/patchname
    subprocess.run([str(out/'tools/xdelta3.exe'),'-e','-s',str(source),str(target),str(patch)],check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    text=(old/'apply.ps1').read_text('utf-8-sig');assert sha(old/'apply.ps1')==oldproof['contents_sha256']['apply.ps1']
    text=text.replace('TinyToonAdventures2_KR_Review_049_20261006.xdelta',patchname).replace(oldproof['contents_sha256']['TinyToonAdventures2_KR_Review_049_20261006.xdelta'],sha(patch)).replace(oldproof['ROM_sha256'],sha(target)).replace('검토용049','검토용050')
    helpers.windows_text(out/'apply.ps1',text)
    readme=f'''타이니툰 어드벤처2 일본판 한글 개발050 — 티켓교환 대사깨짐 수정 (2026-10-08)

원본 일본판 NES ROM만 apply.cmd에 드래그하거나 아래 명령을 사용하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_KR_050_티켓교환수정.nes"
원본은262160바이트이며 SHA-256={sha(source)}
결과는499728바이트이며 SHA-256={sha(target)}
기존049 ROM에 덧씌우지 말고 원본에 적용하세요. 기존 출력은 덮어쓰지 않습니다.

Mesen에서 새050 ROM을 열고 초기화 후 매표소에 다시 들어가 검수하세요.
이미깨진049 강제저장상태는 기존CHR/NT 상태를 저장하므로050로불러와도자동복구되지않습니다.
현재열린사용자Mesen/원본/세이브/기존049는수정하지않았습니다.

수정: 상단소지숫자 갱신이 하단대사의글꼴을덮는 충돌을 고쳤습니다.
같은cold입력 교환·포인트부족·놀이기구티켓부족·성공출발 네분기 검증PASS.
initialcurrency seed만기록한집중검증이며 전체자연플레이/최종문구·명칭·그림승인은미완료입니다.
원문유지6건의사용자범위선택과번역CSV/CHR는동일합니다.

issue177/의PNG는실제동일조건049/050 교환결과입니다. report는집중검증자료입니다.
review049_historical/의HTML·문구/그림·결정양식·실행이미지는049기준역사자료입니다.
그자료를새050 전장면검증이나최종승인으로간주하지마세요. 기존사람범위결정169/173은그대로보존했습니다.
scope_policy050.json은그결정의050 적용근거를구분합니다.
정식배포/카페완성작업기/외부게시용이아닌사용자검수용입니다.
'''
    helpers.windows_text(out/'README_적용방법.txt',readme)
    (out/'RELEASE_NOTES_KO.md').write_text('''# 검토용050 — 티켓교환 글꼴 수정

숫자갱신의공유초기화가‘포인트를 티켓으로 / 바꿔 드릴게요’의폰트162를196으로바꾸던결함을수정했다. 매표소course6/slot23만거주하단폰트를보존하며놀이기구숫자는196을계속사용한다. 번역본문·그림데이터는동일하다.

53,760 CPU사례의ABI/시간계약, 독립ROM/IPS재빌드, 실제MesenCE 동일입력네분기1116 paired시점검증PASS. 숫자/점수/테두리/캐릭터보존, 놀이기구두분기NT/PPU/OAM/PNG동일. Windows적용검증은별도적용보고로기록한다. 전체플레이와최종사람검수는미완료다.

새ROM을열고초기화하여재진입한다. 이미깨진049 강제저장상태의자동복구/버전간상태호환은검증범위가아니다. review049_historical은그버전자료이며새050대사/그림전부검증의증거가아니다.
''','utf-8')
    issue=out/'issue177';issue.mkdir()
    for src,dst in [(validation,'validation.json'),(R/'qa/reports/issue176_diagnosis.json','diagnosis_before_fix.json'),(R/'qa/dialogue/issue177_exchange_049/frame_01710.png','exchange049_before.png'),(R/'qa/dialogue/issue177_exchange_050/frame_01710.png','exchange050_after.png')]:shutil.copyfile(src,issue/dst)
    before=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes();after=target.read_bytes();assert before[0x40010:]==after[0x40010:] and before[0x25609:0x25a28]==after[0x25609:0x25a28] and before[0x261b1:0x261ff]==after[0x261b1:0x261ff]
    put(out/'scope_policy050.json',{'policy':'Six explicit original-retention choices169/173 carry forward; not final text/art/fullplay approval.','prior_policy_sha256':sha(old/'review/scope_decisions.json'),'prior_policy_ROM_sha256':sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'),'current_ROM_sha256':sha(target),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'all_CHR_registered_bodies_macro_alternate_printer_tables_equal049':True,'decisions':j(old/'review/scope_decisions.json')['decisions'],'historical_review':'review049_historical/review.html;49/54 old coverage is not new050 coverage'})
    report={'name':name,'date':'2026-10-08','status':'DEVELOPMENT_REVIEW','version':'0.1.0-review050-boothfix','distribution_eligible':False,'ROM_free':True,'source':{'bytes':source.stat().st_size,'sha256':sha(source)},'target':{'build':'dialogue_kr_poc_050','bytes':target.stat().st_size,'sha256':sha(target)},'patch':{'file':patchname,'bytes':patch.stat().st_size,'sha256':sha(patch)},'validation':{'file':'issue177/validation.json','sha256':sha(validation),'scope':'Focused controlled native reproduction+adjacent4 branches; not full gameplay'},'historical_review':'049 images/records and original user scope decisions unchanged; not requalified050 global review','human_final_review':False,'global_corpus_complete':False,'tools_files_sha256':{n:sha(out/n) for n in ['tools/xdelta3.exe','tools/LICENSE_xdelta3.txt','tools/README_xdelta3.md','licenses/Galmuri_OFL.md']}}
    put(out/'release_report.json',report)
    helpers.PATCH=patchname;helpers.TARGET_SHA=sha(target);helpers.SOURCE_SHA=sha(source)
    qa=R/'qa/release/issue178_apply050';proof=helpers.check_apply(out,qa,source,target)
    # Store helper proof without path-dependent copied ROM; report contains hashes only.
    shutil.copyfile(qa/'apply_verification.json',out/'Windows_apply_verification.json')
    files=sorted(p for p in out.rglob('*') if p.is_file());(out/'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files),'utf-8');files=sorted(p for p in out.rglob('*') if p.is_file())
    assert all(p.suffix.lower() not in {'.nes','.mss','.bin','.ips'} for p in files)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            item=zipfile.ZipInfo(name+'/'+p.relative_to(out).as_posix(),(2026,10,8,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;z.writestr(item,p.read_bytes())
    extracted=qa/'최종 ZIP 추출';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p in files:assert z.read(name+'/'+p.relative_to(out).as_posix())==p.read_bytes()
        z.extractall(extracted)
    applied=extracted/'새050 결과.nes';final=helpers.apply(extracted/name,source,extracted,applied);assert final['exit_code']==0 and applied.read_bytes()==target.read_bytes()
    for p in files:assert (extracted/name/p.relative_to(out)).read_bytes()==p.read_bytes()
    hashfile=archive.with_suffix('.zip.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
    evidence=R/'qa/reports/issue178_package.json';put(evidence,{'work':178,'status':'PASS_ROMFREE050_PACKAGE_WINDOWS8_AND_FINAL_ZIP_APPLY','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'ROM_sha256':sha(target),'source_sha256':sha(source),'files':len(files),'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files},'Windows_helper_checks':proof,'final_ZIP_apply':final,'final_output_sha256':sha(applied),'source_unchanged':sha(source)==helpers.SOURCE_SHA,'final_ZIP_payload_unchanged':True,'ROM_free':True,'historical_review049_explicit':True,'fullplay_or_human_final_approval':False})
    body=f'''[050 적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}` / [ROM](../build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes) SHA `{sha(target)}`. 원본일본판→050 xdelta이며이전049를덮지않는다. [{len(files)}개포함파일/검증보고](../qa/reports/issue178_package.json), [사용법](../dist/{name}/README_적용방법.txt). tools/licenses/apply.cmd는이전검증본을그대로복사했다. PS1의패치명·패치SHA·결과SHA·050표시만바꾸고기존출력덮어쓰기금지/원본검증/도구해시/임시파일정리는보존했다.

검증: 실Windows apply.cmd8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로 최종ZIP 추출본 apply.cmd 실행 byte-exact050 PASS. ZIP CRC/전체포함파일exact/적용후payload불변/ROM없는ZIP PASS. 원본·1편·이전049적용본·사용자세이브·Mesen untouched. 기존173folder에사용자가만든ROM은복사하지않았다.

049검토HTML/이미지/결정169/173은review049_historical로exact보존하고역사자료임을root사용법/notes/report에명시했다. 새050대상54/33전장면재검증이나결정양식최종승인으로전환하지않았다. issue177에실제같은입력 교환before/afterPNG와집중4분기검증report를넣었다. scope_policy050은원문유지6건의사용자정책을그대로참조하며본문/CHR/별도printer표가049와같음을확인했다. [작업177](BOOTH_EXCHANGE_FONT_FIX_050_177.md)의집중runtime와package적용은구분한다. 전체플레이/최종사람승인/전역원천완결은미완료이고카페완성작업기/게시없음.

재생: 새050 ROM을열고초기화후매표소에다시들어가교환한다. 이미깨진049 강제저장상태의자동복구는보장하지않는다. builder: `python scripts/build_booth177.py --output build/NEW_050`; package: `python scripts/package_booth178.py`는기존최종산출물재작성방지로재실행하지않는다. hashes는위보고와패키지SHA256.txt를따른다.'''
    seal(178,'BOOTH_FIX050_APPLY_PACKAGE_178.md','수정050 ROM없는 적용묶음·실Windows 검증',body,'050수정ZIP 준비. 실Windows helper8+최종ZIP적용 byte-exact/ROM-free PASS.049검토는역사자료로보존, 현재사용자Mesen/세이브는수정하지않음.','사용자가 새050 ROM을 열고 초기화/매표소 재진입 후 티켓 교환 대사를 검수한다.',[Path(__file__),R/'scripts/release_apply_helpers132.py',evidence,archive,hashfile,*files,qa/'apply_verification.json'])
    # Current headers override seal_nonplay171's historical049 default; numbered entries remain immutable history.
    p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');pos=s.index('[작업107 실제');s=s[:pos]+f'''최신 [050 적용ZIP178](../dist/{archive.name}), [사용법](../dist/{name}/README_적용방법.txt), [적용검증178](BOOTH_FIX050_APPLY_PACKAGE_178.md). 실Windows8+최종ZIP적용 byte-exact PASS.050을새로열고reset/매표소재진입으로검수한다.049연결표175/HTML173은역사자료다.

'''+s[pos:];p.write_text(s,'utf-8')
    p=R/'README.md';s=p.read_text('utf-8').replace('작업177 완료 / 티켓교환','작업178 완료 / 티켓교환',1).replace('현재 개발본 — 작업177 / 050','현재 개발본 — 작업178 / 050',1);s=s.replace('050 적용묶음은 다음작업에서 만든다.',f'최신 [050 적용ZIP178](dist/{archive.name})과 [검증178](docs/BOOTH_FIX050_APPLY_PACKAGE_178.md)을 사용한다.');p.write_text(s,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업178','현재 개발050 / 작업178',1);p.write_text(s,'utf-8')
    print(json.dumps({'status':'PASS','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'files':len(files),'ROM_sha256':sha(target)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
