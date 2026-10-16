"""ROM-free051 moving STOP patch, actual Windows eight-case and ZIP-apply checks."""
from pathlib import Path
import json,shutil,subprocess,zipfile,re
from seal_nonplay171 import R,sha,seal
import release_apply_helpers132 as helpers

def j(p):return json.loads(p.read_text('utf-8'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')

def main():
    name='TinyToonAdventures2_KR_Review_051_MovingStop_20261008';patchname='TinyToonAdventures2_KR_Review_051_20261008.xdelta'
    out=R/'dist'/name;archive=out.with_suffix('.zip');assert not out.exists() and not archive.exists()
    target=R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes';source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    validation=R/'qa/reports/moving_stop182_validation.json';assert j(validation)['status']=='PASS_MOVING_STOP051_NATIVE_GLYPH_ONLY_FIX' and sha(target)==j(validation)['ROM_sha256']
    old=R/'dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008';proof173=j(R/'qa/reports/nonplay173_package.json')
    out.mkdir()
    for n in ['apply.cmd','tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md']:
        assert sha(old/n)==proof173['contents_sha256'][n];p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old/n,p)
    patch=out/patchname
    subprocess.run([str(out/'tools/xdelta3.exe'),'-e','-s',str(source),str(target),str(patch)],check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    text=(old/'apply.ps1').read_text('utf-8-sig');assert sha(old/'apply.ps1')==proof173['contents_sha256']['apply.ps1']
    oldpatch='TinyToonAdventures2_KR_Review_049_20261006.xdelta'
    text=text.replace(oldpatch,patchname).replace(proof173['contents_sha256'][oldpatch],sha(patch)).replace(proof173['ROM_sha256'],sha(target)).replace('검토용049','검토용051')
    helpers.windows_text(out/'apply.ps1',text)
    helpers.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처2 일본판 한글 검토용051 — 움직이는 STOP 한글화 (2026-10-08)

원본 일본판 ROM을 apply.cmd에 드래그하거나 다음 명령을 사용하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_KR_051_움직이는표지판수정.nes"
원본:262160바이트 / SHA-256 {sha(source)}
결과:499728바이트 / SHA-256 {sha(target)}
기존 한글 ROM에 덧씌우지 말고 원본에 적용하세요. 기존 출력은 덮어쓰지 않습니다.

새051 ROM을 Mesen에서 열고 초기화 후 기차 놀이기구에서 확인하세요.
처음의 고정 ‘정지’ 표지판 이후 위아래로 움직이는 표지판도 ‘정지’로 수정했습니다.
기존050의 티켓 교환 대사깨짐 수정도 포함합니다.
다른버전 강제저장상태의 자동복구/호환은 검증하지 않았습니다.

050대비 스프라이트CHR46 글자6타일의58바이트만 변경했습니다.
기둥·외곽·투명도·움직임·고정표지판·HUD와 CPU/IRQ 코드는 그대로입니다.
동일5000frame 입력의734화면 비교:644전체PNG동일,90화면은 움직이는표지판 글자만변경.
전체플레이/최종문구·명칭·그림 승인은 사용자검수 중입니다.

HUD의 왼쪽띠와 아래여백은 작업180의 원본 비교에서 원본 구성으로 확인됐습니다.
한글 HUD의2픽셀 세로이동은 별도이며 이번051에서 HUD는 바꾸지 않았습니다.
‘전체놀이기구에서같다’는 사용자관측이고,새전놀이기구검증을 주장하지 않습니다.

moving_stop/에는 실제같은입력050/051 화면4200/4272와검증보고가 있습니다.
scope_policy051.json은 원문유지6건의 기존 사용자결정을 보존합니다.
HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT는 이번범위 원문유지입니다.
이것은 사용자검수용 ROM없는 적용묶음입니다. 카페완성작업기/외부게시물은 아닙니다.
''')
    (out/'RELEASE_NOTES_KO.md').write_text('''# 검토용051 — 움직이는 STOP 한글화

처음의 고정 표지판 이후 위아래로 움직이는 표지판은 별도스프라이트CHR46을 사용해 STOP이 남아 있었다. 해당 글자영역을 ‘정지’로 바꿨다.050대비58바이트만 변경했으며 외곽/기둥/투명도와PRG/헤더/IRQ/CSV/다른CHR를 보존했다.050 티켓교환 대사글꼴 수정은 포함된다.

원본Expected Write/PNG-CHR 왕복/IPS적용/독립재빌드 PASS.같은입력5000frame 실제Mesen 비교의734 paired화면에서RAM/OAM/매퍼/CPU·PPU상태가같다.644전체PNG 동일,90화면7451픽셀은 움직이는표지판의 정확한글자쌍에서만변경.각객체의완료이미지와다음OAM 시차를별도로검증했다. HUD전체RGB와고정정지표지판은유지했다. Windows적용8사례와최종ZIP 실제적용은별도보고다.

전체기차/게임완주 및최종사람검수는 미완료다. 새051을열고초기화후재진입한다. 버전간강제저장상태호환을보장하지않는다. 기존049/050 전체검토자료는이ZIP에복사하지않았으며그자료는해당버전의역사자료다. 원문유지6건의결정은그대로다. 카페완성작업기/게시없음.
''','utf-8')
    issue=out/'moving_stop';issue.mkdir()
    for src,dst in [(validation,'validation.json'),(R/'extracted/graphics/moving_stop182/consumer.json','consumer.json')]:shutil.copyfile(src,issue/dst)
    for n in (4200,4272):
        for build,folder in [(50,'moving_stop181_050'),(51,'moving_stop182_051')]:shutil.copyfile(R/f'qa/dialogue/{folder}/frame_{n:05d}.png',issue/f'frame{n:05d}_{build:03d}.png')
    after=target.read_bytes();before=(R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes').read_bytes()
    diff=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b];assert len(diff)==58 and all(0x4ba90<=i<0x4bb50 for i in diff)
    decisions=j(old/'review/scope_decisions.json');assert sha(old/'review/scope_decisions.json')==proof173['contents_sha256']['review/scope_decisions.json']
    put(out/'scope_policy051.json',{'policy':'Six explicit original-retention decisions169/173 carry forward; not final text/art/fullplay approval.','prior_policy_sha256':sha(old/'review/scope_decisions.json'),'current_ROM_sha256':sha(target),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'decisions':decisions['decisions'],'change_scope':'Only moving STOP CHR46 local42,43,45,48,49,50;58bytes vs050. PRG/header/CSV/all bytes outside listed glyph tiles equal050. Not global CHR equality to049.','source_scope_decisions':decisions['sources'],'new_graphics_consumer':'MOVING_STOP_SPRITE46; separate from historical33-asset inventory','consumer_uncertainty_for_retained_six':6,'human_final_review':False})
    put(out/'release_report.json',{'name':name,'date':'2026-10-08','status':'DEVELOPMENT_REVIEW','version':'0.1.0-review051-movingstop','distribution_eligible':False,'ROM_free':True,'source':{'bytes':source.stat().st_size,'sha256':sha(source)},'target':{'build':'dialogue_kr_poc_051','bytes':target.stat().st_size,'sha256':sha(target)},'patch':{'file':patchname,'bytes':patch.stat().st_size,'sha256':sha(patch)},'validation':{'file':'moving_stop/validation.json','sha256':sha(validation),'scope':'Controller-only5000frame same-condition moving STOP reproduction; not full gameplay'},'booth_fix050_retained_PRG_equal':True,'HUD050_full_RGB_equal_in734_paired_screens':True,'human_final_review':False,'global_corpus_complete':False,'tools_files_sha256':{n:sha(out/n) for n in ['tools/xdelta3.exe','tools/LICENSE_xdelta3.txt','tools/README_xdelta3.md','licenses/Galmuri_OFL.md']}})
    helpers.PATCH=patchname;helpers.TARGET_SHA=sha(target);helpers.SOURCE_SHA=sha(source)
    qa=R/'qa/release/moving_stop183_apply051';proof=helpers.check_apply(out,qa,source,target)
    shutil.copyfile(qa/'apply_verification.json',out/'Windows_apply_verification.json')
    files=sorted(p for p in out.rglob('*') if p.is_file());(out/'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files),'utf-8');files=sorted(p for p in out.rglob('*') if p.is_file())
    assert all(p.suffix.lower() not in {'.nes','.mss','.bin','.ips'} for p in files)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            item=zipfile.ZipInfo(name+'/'+p.relative_to(out).as_posix(),(2026,10,8,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;z.writestr(item,p.read_bytes())
    extracted=qa/'최종 ZIP 추출';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={name+'/'+p.relative_to(out).as_posix() for p in files}
        for p in files:assert z.read(name+'/'+p.relative_to(out).as_posix())==p.read_bytes()
        z.extractall(extracted)
    applied=extracted/'새051 결과.nes';final=helpers.apply(extracted/name,source,extracted,applied);assert final['exit_code']==0 and applied.read_bytes()==target.read_bytes()
    for p in files:assert (extracted/name/p.relative_to(out)).read_bytes()==p.read_bytes()
    hashfile=archive.with_suffix('.zip.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
    evidence=R/'qa/reports/moving_stop183_package.json';put(evidence,{'work':183,'status':'PASS_ROMFREE051_PACKAGE_WINDOWS8_AND_FINAL_ZIP_APPLY','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'ROM_sha256':sha(target),'source_sha256':sha(source),'files':len(files),'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files},'Windows_helper_checks':proof,'final_ZIP_apply':final,'final_output_sha256':sha(applied),'source_unchanged':sha(source)==helpers.SOURCE_SHA,'final_ZIP_payload_unchanged':True,'ROM_free':True,'fullplay_or_human_final_approval':False})
    body=f'''[051 적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}` / [ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes) SHA `{sha(target)}`. 원본일본판→051 xdelta이며기존패치본에덧씌우지않는다. [사용법](../dist/{name}/README_적용방법.txt), [{len(files)}파일/적용검증](../qa/reports/moving_stop183_package.json). 변경파일의전체해시는manifests/nonplay183_assets.json 및묶음SHA256.txt 참조.

실Windows apply.cmd8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로 최종ZIP 추출본의apply.cmd→byte-exact051 PASS. ZIP CRC/파일목록/모든내용exact/적용후payload불변/ROM-free PASS. 원본SHA `{sha(source)}` 보존. 사용자적용050 ROM을포함한이전dist/원본/1편/사용자Mesen/설정/세이브는수정하지않았다.

moving_stop/의050/051 frame4200/4272 실제같은입력PNG,소비기록,최종집중검증보고를포함했다. tools/licenses/apply.cmd는173 고정기록의SHA와일치복사. PS1은패치명·패치SHA·결과SHA·버전표시만갱신했다. 기존049검토HTML은현재051로재명명하지않으며이ZIP에넣지않았다. scope_policy051은169/173의6원문유지선택을그대로보존하되전체CHR동일주장은이번수정에맞게제거했다. 글자58바이트외에는050 동일하며티켓교환수정177의PRG를그대로포함한다.

현재채택051. [작업182](MOVING_STOP_GLYPH_FIX_051_182.md)의정적/빌드/실제Mesen/직접장면검증과이작업의적용검증을구분한다. 사용자전체플레이/최종문구·명칭·그림검수는남는다. HUD 전놀이기구동일은사용자관측이고새전놀이기구실행검증을의미하지않는다. 카페완성작업기/외부게시없음.

실행: ZIP을풀고원본.nes를apply.cmd에드래그.051을새로열고초기화한뒤기차의고정정지뒤움직이는표지판을검수한다. 다른버전강제저장상태의호환/자동복구는검증범위아니다. 재현package: `python scripts/package_moving_stop183.py`는기존최종산출물재작성방지가있어현재경로에서재실행하지않는다.'''
    next_action='사용자가 새051 ROM을 열고 초기화/기차 재진입 후 위아래로 움직이는 정지 표지판을 검수한다.'
    seal(183,'MOVING_STOP051_APPLY_PACKAGE_183.md','수정051 ROM없는 적용묶음·실Windows 검증',body,'051 움직이는STOP 수정ZIP 준비.실Windows8사례와최종ZIP적용 byte-exact/ROM-free PASS.원문유지6건및050티켓교환수정보존.',next_action,[Path(__file__),R/'scripts/release_apply_helpers132.py',evidence,archive,hashfile,*files,qa/'apply_verification.json'])
    p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');pos=s.index('[작업107 실제')
    intro=f'''# 진행 중 — 2026-10-08, 작업183 완료

현재 **dialogue_kr_poc_051**, ROM SHA `{sha(target)}`, CSV SHA `{sha(R/'workspace/translation/text_ja.csv')}`. 사용자신고의 **움직이는 STOP**은고정표지판과다른CHR46 스프라이트였다. [진단181](MOVING_STOP_CONSUMER_DIAGNOSIS_181.md), [글자수정·동일입력검증182](MOVING_STOP_GLYPH_FIX_051_182.md)에서6타일58바이트만‘정지’로변경했다.734 paired화면의644전체PNG 동일/90화면 글자만변경;상태·HUD·고정정지·움직임보존. 독립ROM/IPS재빌드 PASS. [050 교환수정177](BOOTH_EXCHANGE_FONT_FIX_050_177.md)은PRG그대로포함한다.

최신 [051 적용ZIP183](../dist/{archive.name}), [사용법](../dist/{name}/README_적용방법.txt), [적용검증183](MOVING_STOP051_APPLY_PACKAGE_183.md). 실Windows8+최종ZIP적용 byte-exact PASS. 원본일본판에적용하고051을새로열어초기화/기차재진입한다. 이전049/050 문서·ZIP·사용자적용ROM·세이브는보존된역사자료다.

HUD [원본비교180](HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md):왼쪽띠/아래여백은원본구성,한글HUD2픽셀이동은별도. ‘모든놀이기구에서같다’는사용자검수결과로181에기록했고새전놀이기구검증으로확대하지않았다.051 HUD변경없음. 원문유지6건사용자결정/CSV동일;소비미확정6건·전역원천완결·최종문구/명칭/그림/전체플레이승인은미완료다. 카페완성작업기는전체완료후작성하고게시하지않는다.

**다음 작업 하나: {next_action}** [오늘 인계](HANDOFF_2026-10-08.md), [오늘 journal](journal/2026-10-08.md), [조사](SURVEY.md), [계획](LOCALIZATION_WORK_PLAN.md).

'''
    p.write_text(intro+s[pos:],'utf-8')
    p=R/'README.md';s=p.read_text('utf-8');pos=s.index('작업51 당시 채택043:')
    p.write_text(f'''> **2026-10-08 현재개발051 / 작업183 완료 / 움직이는 STOP 한글화.** [최신 인계](docs/HANDOFF.md)

# 현재 개발본 — 작업183 / 051

[움직이는 표지판 수정·검증182](docs/MOVING_STOP_GLYPH_FIX_051_182.md), [ROM](build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes), [IPS](build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.ips), [051 적용ZIP183](dist/{archive.name}). 처음고정표지판뒤위아래로움직이는 STOP을정지로수정했다.050대비CHR46 58바이트만변경.티켓교환글꼴수정050 포함.734 paired화면 비교/독립ROM·IPS재빌드/실Windows8·최종ZIP적용 PASS. 전체플레이/최종문구·명칭·그림검수는사용자담당이다.

[HUD원본비교180](docs/HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md)의왼쪽띠/아래여백은원본구성이며051 HUD수정없음.원문유지6건및CSV그대로다.등록33그림과이번추가움직이는소비를별도로기록했다.이전049/050자료는각버전의역사기록이며새051 전장면검증으로해석하지않는다.

'''+s[pos:],'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업183','현재 개발051 / 작업183',1);p.write_text(s,'utf-8')
    print(json.dumps({'status':'PASS','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'files':len(files),'ROM_sha256':sha(target)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
