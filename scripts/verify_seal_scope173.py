"""Validate review173 evidence, apply its final ZIP, then seal scope-only closure."""
from pathlib import Path
from html.parser import HTMLParser
import base64,csv,hashlib,json,shutil,zipfile
from release_apply_helpers132 import apply as windows_apply
from seal_nonplay171 import R,sha,seal

class Images(HTMLParser):
    def __init__(self):super().__init__();self.sources=[]
    def handle_starttag(self,tag,attrs):
        if tag=='img':self.sources.append(dict(attrs)['src'])

def main():
    report=R/'qa/reports/nonplay173_final.json'
    root=R/'qa/apply/2편 개발049 보존6 확정 한글 공백 적용 검증 20261008_173'
    assert not report.exists() and not root.exists()
    review=R/'workspace/review/nonplay049_20261008_173'
    records=json.loads((review/'review_records.json').read_text('utf-8'))
    parser=Images();parser.feed((review/'review.html').read_text('utf-8'))
    evidence=records['actual_images']+records['static_source_images']
    assert len(parser.sources)==len(evidence)==25
    for src,e in zip(parser.sources,evidence):
        assert src.startswith('data:image/png;base64,')
        assert hashlib.sha256(base64.b64decode(src.split(',',1)[1],validate=True)).hexdigest()==e['sha256']==sha(R/e['path'])
    rows={r['entry_id']:r for r in csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline=''))}
    for u in records['units']:
        for k in ['translation_ko','status','source_tokens','raw_sha256']:assert u[k]==rows[u['entry_id']][k]
    oldrecords=json.loads((R/'workspace/review/nonplay049_20261007_170/review_records.json').read_text('utf-8'))
    assert len(records['units'])==54 and records['graphics']==oldrecords['graphics'] and len(records['graphics'])==33
    combined=json.loads((review/'scope_decisions.json').read_text('utf-8'))
    all_decisions=[]
    for s in combined['sources']:
        assert sha(review/s['file'])==s['sha256']
        all_decisions+=json.loads((review/s['file']).read_text('utf-8'))['decisions']
    assert combined['decisions']==all_decisions and len(all_decisions)==6
    assert all(d['human_approved'] and d['decision']=='preserve_original_for_this_scope' for d in all_decisions)
    assert (review/'scope_decisions169.json').read_bytes()==(R/'workspace/translation/scope_decisions_20261007_169.json').read_bytes()
    assert (review/'scope_decisions173.json').read_bytes()==(R/'workspace/translation/scope_decisions_20261008_173.json').read_bytes()
    ui=R/'qa/review/nonplay049_173_render/render_report.json'
    assert json.loads(ui.read_text('utf-8'))['status']=='PASS'
    pkg=json.loads((R/'qa/reports/nonplay173_package.json').read_text('utf-8'))
    archive=R/pkg['archive'];assert sha(archive)==pkg['archive_sha256']
    root.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==23
        for n in z.namelist():assert (root/n).resolve().is_relative_to(root.resolve())
        z.extractall(root)
    extracted=root/archive.stem
    for f,h in pkg['contents_sha256'].items():assert sha(extracted/f)==h
    sums=(extracted/'SHA256.txt').read_text('utf-8').splitlines();assert len(sums)==22
    for line in sums:
        h,f=line.split('  ',1);assert sha(extracted/f)==h
    for p in review.iterdir():
        if p.is_file():assert (extracted/'review'/p.name).read_bytes()==p.read_bytes()
    release=json.loads((extracted/'release_report.json').read_text('utf-8'))
    assert release['scope_decision']['sha256']==sha(review/'scope_decisions.json')
    assert release['outside_population_summary']==records['outside_population_summary']
    assert release['outside_population_summary']['explicit_user_retention']==6
    assert release['outside_population_summary']['still_unresolved_count']==0
    assert not release['distribution_eligible'] and not release['translation_review']['human_final_review']
    meta=json.loads((R/'manifests/source_rom.json').read_text('utf-8'))
    original=R/meta['path'];source=root/'검증 원본 일본판.nes';target=root/'새 결과 검토049.nes'
    assert sha(original)==meta['sha256'];shutil.copy2(original,source)
    obs=windows_apply(extracted,source,root,target)
    (root/'apply_observation.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n','utf-8')
    assert obs['exit_code']==0,obs
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';ssot=R/'workspace/translation/text_ja.csv'
    assert target.read_bytes()==rom.read_bytes() and sha(target)==pkg['ROM_sha256']
    assert sha(source)==sha(original)==meta['sha256'] and sha(ssot)==pkg['SSOT_sha256']
    for f,h in pkg['contents_sha256'].items():assert sha(extracted/f)==h
    assert sha(archive)==pkg['archive_sha256']
    result={'work':173,'status':'PASS_SIX_EXPLICIT_RETENTIONS_REVIEW_FINAL_ZIP_ACTUAL_WINDOWS_APPLY',
        'archive':pkg['archive'],'archive_sha256':sha(archive),'ZIP_files':23,'SHA256_manifest_files':22,
        'ROM_free':True,'actual_final_ZIP_Windows_apply':obs,'unicode_space_paths':True,'target_byte_exact':True,
        'output_bytes':target.stat().st_size,'exact_review173':True,'scope_original_records_byte_exact':True,
        'scope_projection_decisions_exact':True,'approved_retention':[d['id'] for d in all_decisions],
        'title_prompt_connected':True,'unresolved_scope_decisions':0,'consumer_uncertainty':6,'global_corpus_closed':False,
        'SSOT54_units_exact':True,'graphics33_unchanged':True,'embedded_PNGs_hash_exact':25,
        'browser_report':ui.relative_to(R).as_posix(),'browser_report_sha256':sha(ui),
        'document_visual_inspected':['mobile_candidate_nt1c.png'],
        'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),'actual_play_owner':'user','new_emulator_or_gameplay':False,
        'human_final_review':False,'distribution_eligible':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자가 남은 RYO51·NT1C·진단 STAGE SELECT도 **‘이번 범위에서는 원문 유지’**로 답했다. [173 원본 결정](../workspace/translation/scope_decisions_20261008_173.json)에 질문·답변·현재ROM/CSV·172근거SHA와 세 원천ID를 기록했다.169의 HOWTO·PAUSE·POW 결정은 그대로 보존했다. [새 원장](../workspace/translation/nonplay_inventory049_173.json)은 명시적 사용자 보존6건과 기존 타이틀 PUSH START 소비연결1건을 구분한다. 발견7건의 추가 번역 범위 미결정은0이다. 소비 미연결6건의 기술 상태와 전역 원천 목록 완결성·최종 문구/명칭/그림/플레이/배포 승인 미완료는 유지한다. 미사용 증명이나 전역 영어 보존 정책으로 확대하지 않는다.

[검토HTML](../workspace/review/nonplay049_20261008_173/review.html)과10파일 검토ZIP은 원본 결정169/173 두 파일과 읽기용 합본을 포함한다.54원천의 번역/상태/토큰/원천SHA,33그림 및25내장PNG(기존실제21/정적4)의 바이트SHA가 기존 원천과 일치했다. PC1280/모바일390의 검색·상세열기·크레딧3건·이미지 로드·너비 검사 PASS. 모바일NT1C 결정 카드를 직접 보았다. 실제게임 PNG는 이전 증거 재사용이며 신규 게임 장면이 아니다.

[새 적용ZIP](../{pkg['archive']})은23파일 ROM 없는 개발 검토 패키지다. 기존171을 보존했고 패치·apply.cmd/ps1·xdelta3·도구/글꼴 라이선스는171과 바이트 동일하다. 검수안내/알려진한계/적용안내/릴리스보고를6건 결정으로 동기화했다. [최종검증](../qa/reports/nonplay173_final.json): CRC/내용/SHA22항목 검증 후 최종ZIP을 새 한글·공백 경로에 풀어 실제 Windows apply.cmd를 실행했다. exit0이며 결과499728바이트 전체가 현재049와 일치했다. 원본/ROM/CSV/패치/도구/ZIP 불변이다. 같은 도구의132 오류8사례는 기존 근거를 재사용했다.

이번 검증은 정적 기록·문서 브라우저·압축/해시 및 실제 Windows 적용이다. 신규ROM빌드/CPU실험/에뮬레이터/플레이/PCM청음/사람 최종검수 없음. 실제 플레이는 사용자 담당이다.38cycles/page의 idle RNG/CPU/IRQ 차이,163 frame04410 PNG7326픽셀 차이와 원인 미확정, 모든 분기/상태/실기/PCM 및 최종 문구/그림 승인은 남는다. 카페 완성 작업기는 전체 작업 완료 후이며 외부 게시 없음.

ZIP SHA `{sha(archive)}`, 현재ROM `{sha(rom)}`, CSV `{sha(ssot)}`. 변경:173 결정·원장·검토10파일/ZIP·적용23파일/ZIP/해시·생성/렌더/검증스크립트·렌더PNG/보고·실제적용QA·인계/계획/조사/journal/canonical·manifest/audit. 재현: `python scripts/make_closed_scope173.py`; `python scripts/render_scope173.py --input workspace/review/nonplay049_20261008_173/review.html --output qa/review/nonplay049_173_render`; `python scripts/package_scope173.py`; `python scripts/verify_seal_scope173.py`; `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay173_assets.json --output qa/reports/nonplay173_session.json`. 출력보호가 있으므로 재실행은 별도 경로에서 한다. 파일별SHA는manifest다. 감사는 프로젝트 내부 링크/원본/기존 고정증거를 엄격히 검사하고 역사3.3외부캐시 링크1개 소실은 별도 표시한다.'''
    files=[Path(__file__),R/'scripts/make_closed_scope173.py',R/'scripts/render_scope173.py',R/'scripts/package_scope173.py',
        R/'scripts/release_apply_helpers132.py',R/'scripts/audit_project_links171_v2.py',
        R/'workspace/translation/scope_decisions_20261007_169.json',R/'workspace/translation/scope_decisions_20261008_173.json',
        R/'workspace/translation/nonplay_inventory049_173.json',R/'qa/reports/nonplay172_remaining_facts.json',
        R/'qa/reports/nonplay173_review_package.json',R/'qa/reports/nonplay173_package.json',report,ui,
        R/'qa/reports/nonplay171_final.json',archive,archive.with_name(archive.name+'.sha256'),
        R/'workspace/review/TinyToon2_Nonplay_Review_049_Scope173_20261008.zip',rom,ssot]
    for folder in [review,R/'dist'/archive.stem,root]:files.extend(p for p in folder.rglob('*') if p.is_file())
    files.extend(p for p in ui.parent.iterdir() if p.is_file())
    files.extend(R/e['path'] for e in evidence)
    seal(173,'CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md','보존6건 확정·검토/실제적용 반영',body,
        '사용자 결정으로 발견7건의 범위 미결정0(명시보존6+기존타이틀연결1). 검토173 PC/모바일·25PNG·54/33·최종23파일ZIP 실제Windows적용 PASS. ROM/CSV불변; 플레이 사용자 담당.',
        '보존된162/163 종료 자료만 사용해 frame04410 PNG 차이의 캡처 출처를 오프라인 대조하고, 확인 가능한 원인과 확인 불가한 한계를 구분한다.',files)
    p=R/'docs/HANDOFF.md';text=p.read_text('utf-8')
    start=text.index('최신171 [ROM없는적용ZIP]');end=text.index('\n\n\n[작업108',start)
    replacement='''최신 [적용ZIP173](../dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008.zip), [검토HTML173](../workspace/review/nonplay049_20261008_173/review.html), [인계173](CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md)를 따른다.54원천/33그림/기존실제21·정적4PNG를 보존했다. HOWTO·PAUSE·POW(169)와 RYO51·NT1C·진단 STAGE SELECT(173)는 이번 범위 원문 유지로 사용자 결정됐다. 타이틀 PUSH START는 기존 보존 안내에 소비 연결됐다. 발견7건의 번역 범위 미결정은0이나 소비 미확정6건은 남으며 전역 미사용이나 전체게임 승인이 아니다. 아래 각 작업 기록은 당시 역사 자료다.

실제 플레이는 사용자 담당이다. 현재049 ROM/CSV는 동일하고173의 최종ZIP 실제 Windows 적용은 byte-exact PASS다. 비플레이의 명시적 번역 범위 잔여6건과 패키지 반영은 닫았다.163 캡처 PNG 차이는 원인 미확정이며 전역 원천 목록 완결성과 최종 문체·명칭·그림/플레이 검수는 미완료다. 전체 작업 완료 후 카페 완성 작업기를 작성하며 외부 게시하지 않는다.'''
    text=text[:start]+replacement+text[end:];p.write_text(text,'utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='actual_final_ZIP_Windows_apply'},indent=2))

if __name__=='__main__':main()
