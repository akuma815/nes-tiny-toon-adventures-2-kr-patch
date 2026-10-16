"""Seal technical writing, source provenance, publication ZIP and handoff."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,sys,re
from seal_nonplay171 import R,sha
import seal_nonplay171 as records
from build_technical_guide227 import OUT,TITLE
records.DATE='2026-10-09'
NAME='TinyToon12_NES_Korean_TechnicalGuide_20261009'
G1=R.parent/'Tiny Toon Adventures'
TARGET1='d57b816fce99d99eb700ebecc3d2397a1d039418ead3b1233d720c712fb2df3d'
TARGET2='7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce'

def main():
    source_refs=[
      (G1,'docs/POC_TITLE.md'),(G1,'docs/POC_DIALOGUE.md'),(G1,'docs/DIALOGUE_FULL.md'),
      (G1,'docs/DIALOGUE_PAGED.md'),(G1,'docs/FONT_SIZE_SURVEY.md'),
      (G1,'docs/HAMTON_FONT_FIX_2026-10-04.md'),(G1,'scripts/extract_dialogue.py'),
      (R,'docs/POC_TITLE.md'),(R,'docs/POC_DIALOGUE.md'),(R,'docs/POC_INTRO_COMPLETE.md'),
      (R,'docs/BOOTH_EXCHANGE_FONT_FIX_050_177.md'),(R,'docs/MOVING_STOP_GLYPH_FIX_051_182.md'),
      (R,'docs/HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md'),
      (R,'docs/OPENING11_PAIRED_ROW_POC053_BUILD_186.md'),
      (R,'docs/TEXT11_SCRIPT_SCOPE_AND_FEASIBILITY_197.md'),
      (R,'docs/TEXT11_REMAINING_NUMERALS_CARDS_CREDITS_DESIGN_201.md'),
      (R,'docs/CREDITS11_SHARED_FONT106_SPACING_OPTION_202.md'),
      (R,'docs/TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md'),
      (R,'docs/TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md'),
      (R,'docs/TEXT11_OPENING_CREDITS_IRQ_218.md'),(R,'docs/TEXT11_IRQ_STACK_GAP_CORRECTION_219.md'),
      (R,'docs/FINAL_RELEASE_USER_FIRST_QA_224.md'),(R,'docs/FINAL_DELIVERY_CLEANUP_226.md'),
      (R,'scripts/extract_text.py'),(R,'workspace/asm/dialogue_page_font_010.asm'),
      (R,'qa/reports/user_review224.json')]
    refs=[{'project':root.name,'path':rel,'sha256':sha(root/rel)} for root,rel in source_refs]
    assert sha(G1/'build/dialogue_footer_fix_003/TinyToon_dialogue_full.nes')==TARGET1
    assert sha(R/'build/release_v1_0_220/TinyToon2_KR_v1.0.nes')==TARGET2
    original1=G1/'original/rom/Tiny Toon Adventures (Japan).nes'
    assert not original1.exists(),'Update source-identity observation if original1 has changed'
    assert sha(R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes')=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    provenance=R/'qa/reports/technical227_sources.json'
    provenance.write_text(json.dumps({'work':227,'source_refs':refs,'original1_identity':'Historical source manifest; original path currently missing; no restore/build attempted',
      'original2_identity':'Live verify_source.ps1 PASS','final_ROM1_sha256':TARGET1,'final_ROM2_sha256':TARGET2,
      'new_game_build_or_execution':False,'game1_read_only':True,
      'external_primary_refs':['https://github.com/SourMesen/Mesen2/blob/master/Core/NES/Debugger/NesPpuTools.cpp',
      'https://raw.githubusercontent.com/SourMesen/Mesen2/master/UI/Debugger/Documentation/LuaDocumentation.json',
      'https://github.com/quiple/galmuri/blob/main/ofl.md'],
      'external_fetch_note':'NESdev direct pages returned403; generic PPU/API/license explanations linked to accessible primary source code and license',
      'figures':['Own explanatory diagram01','Own font-lifetime diagram02'],'new_actual_game_captures':0},ensure_ascii=False,indent=2)+'\n','utf-8')
    pageproof=R/'qa/reports/technical227_page.json';page=json.loads(pageproof.read_text('utf-8'))
    assert page['readback_verified'] and page['normalized_entire_body_equal'] and page['headings']==16
    render=R/'qa/publication/technical227_final/render_report.json';assert json.loads(render.read_text('utf-8'))['status']=='PASS'
    article=(OUT/'기술_지침.md').read_text('utf-8')
    assert article.startswith('# '+TITLE) and len(re.findall(r'^## ',article,re.M))==16
    for token in ('mapper 23','mapper 85','175개','54개','106개','212,764','44사이클','1차 검수를 마쳤습니다'):
        assert token in article,token
    files=sorted(p for p in OUT.rglob('*') if p.is_file())
    assert len(files)==7 and all(p.suffix in ('.md','.txt','.html','.py','.png') for p in files)
    assert all('\ufffd' not in p.read_text('utf-8-sig') for p in files if p.suffix!='.png')
    checksums=OUT/'SHA256.txt';checksums.write_text(''.join(f'{sha(p).upper()}  {p.relative_to(OUT).as_posix()}\n' for p in files),'utf-8')
    files.append(checksums);archive=R/'dist'/(NAME+'.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,NAME+'/'+p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==8
        for p in files:assert z.read(NAME+'/'+p.relative_to(OUT).as_posix())==p.read_bytes()
        example=z.read(NAME+'/examples_nes.py')
    run=subprocess.run([sys.executable,'-B','-'],input=example,capture_output=True)
    assert run.returncode==0 and b'PASS:' in run.stdout,(run.returncode,run.stderr)
    hashfile=Path(str(archive)+'.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
    evidence=R/'qa/reports/technical227_verified.json'
    evidence.write_text(json.dumps({'work':227,'status':'PASS_TECHNICAL_GUIDE_PAGE_AND_ROMFREE_POSTING_KIT',
      'archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'files':8,'ROM_free':True,
      'native_Page':page['url'],'native_Page_full_body_readback_equal':True,'native_Page_visual_preview':False,
      'local_HTML_desktop_mobile_contents':'PASS','direct_local_visual_review':True,'actual_ZIP_example_execution':'PASS',
      'example_stdout':run.stdout.decode('utf-8'),'factual_scope':'Game1 historical scoped QA, game2 user first screen/playthrough reported; post-release QA planned',
      'new_game_execution':False,'cafe_uploaded':False,'contents_sha256':{p.relative_to(OUT).as_posix():sha(p) for p in files}},ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자 요청에 따라1·2편 기술 경험을 후속 한글화 작업자가 참고할 지침으로 작성했다. [Page]({page['url']}), [게시자료 ZIP](../dist/{archive.name}), [오프라인 HTML](../{OUT.relative_to(R).as_posix()}/기술_지침.html), [편집 원천](../{OUT.relative_to(R).as_posix()}/기술_지침.md). ZIP SHA `{sha(archive)}`,8파일/ROM없음. 폰트·ROM·세이브·덤프·private보관본을 넣지 않았다.

15개 기술 항목과 원천 읽기 순서를 포함했다. 두 게임의 매퍼/압축/제어코드 차이, AI타이틀의 PNG/타일/팔레트/압축예산, 주소종류·헤더, 원천 토큰/포인터 그래프, 문단별 작업집합과 글꼴수명,1편당근/2편숫자갱신 충돌,11px 상하타일·위상·숫자54/크레딧106타일,후크ABI/NMI/IRQ,ExpectedWrites,같은조건 시각검사와 실제최종ZIP적용·인계를 설명했다. 설명도2개는 새로 그린 구조도이며 실제 캡처로 표시하지 않았다. ROM없는Python교육예제는 고정2bpp벡터·64왕복·위상·중첩/보호/기대바이트 거부를 포함한다.

정적:16본문제목·주소/수량 근거·UTF8/본문표식·8파일CRC/정확payload/ROMfree PASS. 최종ZIP에서 꺼낸 예제 바이트를 Python표준라이브러리로 실제 실행 PASS. Page는 개인 위치에 생성하고 전체본문을 읽어 공백 정규화 후 원천과 동일함을 확인했다(120blocks/16h2/2mermaid). 공개공유 설정은 바꾸지 않았다. 사용 가능한 브라우저 표면이 없어 네이티브Page 미리보기는 확인하지 못했다.

로컬HTML은 격리headless Edge1280×1000/390×844에서2설명도·16제목·문단폭·목차펼침/링크이동·JS오류0 확인.4스크린샷과2설명도를 직접 열어 검토했다. [렌더](../qa/publication/technical227_final/render_report.json), [최종검증](../qa/reports/technical227_verified.json), [Page영수증](../qa/reports/technical227_page.json), [기술근거](../qa/reports/technical227_sources.json).

1편은 현재원본경로가 없어 verify_source.ps1이 실패했다. 기존footer003 최종ROM 해시는 기록과 같음을 확인했고 원본을 복원하거나 새게임빌드를 실행하지 않았다. 공개주소표는 역사 원본식별값에 한정한다.2편원본 검증은 통과하고최종ROM은062와 같다.1편/2편ROM·번역CSV·패치ZIP·에뮬레이터/세이브는 수정하지 않았다.2편사용자1차화면·완주완료/배포후검증예정은 유지한다. 새플레이·네이버카페 실제게시없음.

변경: build_technical_guide227.py,prepare_technical_renderer227.py,render_technical227.py,seal_technical_guide227.py,작성MD/HTML/복사용본문/게시안내/2PNG/예제/SHA/ZIP와QA·인계. 재현은 build_technical_guide227.py의OUT를 새경로로 지정하고 입력MD/예제를 복사한 뒤 빌드/렌더/봉인한다. 고정결과는 덮어쓰지 않는다. 실패한 무효빈patch호출은 파일변경없음. 기존자료를 재작성하지 않았다.'''
    records.seal(227,'TINYTOON12_TECHNICAL_GUIDE_227.md','1·2편 NES 한글화 기술 지침과 게시자료',body,
      '1·2편 기술지침15항목+자료참조·설명도2·ROM없는예제/8파일ZIP.전체Page읽기동일·HTML PC/모바일·예제 PASS.',
      '사용자가 기술 지침 본문과 설명도2개를 게시 위치에 배치하고 배포 후 제보를 같은 검증 원칙으로 수집한다.',
      [Path(__file__),*[R/p for p in ('scripts/build_technical_guide227.py','scripts/prepare_technical_renderer227.py',
       'scripts/render_technical227.py','qa/reports/technical227_generation.json')],evidence,provenance,pageproof,render,archive,hashfile,*files,
       *[render.parent/n for n in ('desktop_top.png','desktop_font_section.png','mobile_top.png','mobile_font_section.png')]])
    # Keep final release status current; the shared historical recorder uses old banners.
    p=R/'docs/HANDOFF.md';txt=p.read_text('utf-8')
    txt=re.sub(r'^# .*?\n','# 최종 배포 유지 및 기술 지침 완료 — 2026-10-09, 작업227\n',txt,count=1)
    note=f'''\n[1·2편 한글화 기술 지침 Page]({page['url']})와 [게시자료 ZIP](../dist/{archive.name})을 추가했다. 기존 게임 배포파일과062 검수 상태는 그대로다. [기술지침 인계](TINYTOON12_TECHNICAL_GUIDE_227.md).\n'''
    txt=txt.replace('\n\n', '\n'+note+'\n',1);p.write_text(txt,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';txt=p.read_text('utf-8')
    txt=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 작업227: v1.0(062) 최종배포 유지·1/2편 기술지침 완료. 사용자1차실화면·완주 완료, 배포후검증 예정.**',txt,count=1);p.write_text(txt,'utf-8')
    p=R/'README.md';txt=p.read_text('utf-8');txt=txt.replace('\n\n','\n\n'+note.replace('(../dist/','(dist/').replace('(TINYTOON12_TECHNICAL_GUIDE_227.md)','(docs/TINYTOON12_TECHNICAL_GUIDE_227.md)')+'\n',1);p.write_text(txt,'utf-8')
    for root,rel in source_refs:assert sha(root/rel)==next(x['sha256'] for x in refs if x['project']==root.name and x['path']==rel)
    print(json.dumps({'status':'PASS','Page':page['url'],'ZIP':archive.name,'sha256':sha(archive)},ensure_ascii=False))

if __name__=='__main__':main()
