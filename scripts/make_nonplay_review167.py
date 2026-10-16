"""Refresh current049 private review and outside-candidate decisions without ROM edits."""
from pathlib import Path
import base64, copy, hashlib, html, json, re, zipfile
from seal_nonplay166 import R, sha, seal

OUT = R / 'workspace/review/nonplay049_20261007_167'
ARCHIVE = R / 'workspace/review/TinyToon2_Nonplay_Review_049_20261007.zip'

def main():
    report = R / 'qa/reports/nonplay167_package.json'
    assert not OUT.exists() and not ARCHIVE.exists() and not report.exists()
    old = R / 'workspace/review/translation049_20261006'
    manifest = json.loads((old/'artifact_manifest.json').read_text('utf-8'))
    for f,h in manifest['files'].items(): assert sha(old/f) == h
    inventory = json.loads((R/'workspace/translation/nonplay_inventory049_166.json').read_text('utf-8'))
    records = json.loads((old/'review_records.json').read_text('utf-8'))
    assert records['ROM_sha256'] == inventory['ROM_sha256'] and records['SSOT_sha256'] == inventory['SSOT_sha256']
    source = (old/'review.html').read_text('utf-8')
    records['artifact_policy'] = 'ROM-free private language/art/scope review for unchanged049. Actual gameplay QA belongs to user. No new gameplay execution.'
    records['actual_play_owner'] = 'user'
    records['human_review_complete'] = False
    records['outside_registered_candidates'] = copy.deepcopy(inventory['outside_registered_candidates'])
    records['limits'] = [
        'Registered54 units/33graphics are bounded inventories; global text corpus remains unresolved.',
        '21 actual screenshots retain131 provenance:14 historical043/045/046/047,7 current049. No new screenshots executed in167.',
        '133 validated049 private226 state restore and one reset/reentry only; crossbuild/allcontext compatibility not established.',
        '049 adds38cycles/page; idle RNG/CPU/IRQ differences remain. No wholeCPU or global gameplay identity claim.',
        'Seven outside candidates are preserved and unresolved; no human scope/retention decision or global unused proof.',
        '163 frame4410 differs7326 pixels. Whole-prefix RGB equality failed; capture/rendering cause unknown.',
        'Actual gameplay/fullplay/other branches/PCM/hardware evidence is user-owned and pending. Human language/art approval pending.',
        'No final release or NaverCafe article/post. No ROM/patch/font/emulator in this review archive.'
    ]
    for f in ['state133_validation.json','coverage151_validation.json','water163_hold_validation.json','nonplay166_inventory.json']:
        p=R/'qa/reports'/f
        if f == 'coverage151_validation.json' and not p.exists():
            matches=list((R/'qa/reports').glob('*151*'))
            # The source coverage ledger below is authoritative; no guessed report path is stored.
            continue
        assert p.is_file();records['technical_reports'][f]=sha(p)
    records['coverage_ledger151_sha256']=sha(R/'workspace/translation/coverage049_151.json')
    source = source.replace('<title>타이니툰 2 — 049 사람 검토자료</title>', '<title>타이니툰 2 — 049 비플레이 검토자료 · 2026-10-07</title>')
    source = source.replace('<h1>타이니툰 어드벤처 2 · 검토자료049</h1>', '<h1>타이니툰 어드벤처 2 · 비플레이 검토자료049</h1>')
    note = '<p class="banner">2026-10-07 갱신: 실제 플레이 검수는 사용자 담당입니다. 이번 자료에서는 새 에뮬레이터 실행 없이 문장·그림·범위 결정과 기존 근거를 검토합니다. 현재049와 번역 원천은 그대로입니다.</p>'
    source = source.replace('<h2>실제 화면 표본</h2>',note+'<h2>기존 실제 화면 표본 · 이번 작업에서 재실행하지 않음</h2>',1)
    # Replace the stale133-era status footer; leave54 SSOT unit cards/33 graphics untouched.
    footer = re.search(r'<h2>검토 기록 방법</h2><p>.*?</p>',source,re.S);assert footer
    replacement = '<h2>검토 기록 방법</h2><p>DECISIONS_PENDING.md에 문구 ID·수정 전/후·이유·장면을 기록해 주세요. decisions_template.json은 응답용 빈 양식이며 승인 기록이 아닙니다. 문장45개와 그림33개는 초안입니다. 049의 페이지 초기화에는38cycles가 추가되어 idle 난수·CPU 차이가 남습니다. 작업133은049의 전용226 폰트 저장/복원과 한 번의 리셋 후 재입장을 제한된 조건에서 검증했습니다. 모든 저장상태·다른 빌드 저장 호환성·PCM 청음·실기·전체 플레이 완료를 의미하지 않습니다. 실제 플레이 검수는 사용자 담당이고 공개 카페 작업기는 전체 작업 완료 후 작성합니다.</p>'
    source=source[:footer.start()]+replacement+source[footer.end():]
    source += '' # Keep the closed document structure and inject candidates before the footer.
    sections = '<h2 id="outside">등록 목록 밖의 후보 7건</h2><p>아래는 번역 추가·원문 보존 여부를 검토할 후보입니다. 원본 픽셀 발견, 실제 소비 경로, 최종 범위 결정을 구분했습니다. 미사용으로 확정하거나 문장54개·그림33개에 포함하지 않았습니다. 현재049에서는 관련 원천을 그대로 보존했습니다.</p>'
    for item in records['outside_registered_candidates']:
        sections += f'<details class="candidate" id="{item["id"]}"><summary>{html.escape(item["id"])} · {html.escape(item["text"])} · 보류</summary><p>{html.escape(item["facts"])}</p><p><strong>확인 한계:</strong> {html.escape(item["limit"])}</p><p><strong>작업 제안:</strong> {html.escape(item["proposal"])}</p><p class="note">근거 작업: {", ".join(str(w)for w in item["evidence_works"])} / 현재049 정적 보존 확인 / 사람 승인 없음</p></details>'
    sections += '<h2>후보가 있는 원본 CHR 페이지 · 정적 아틀라스</h2><p>아래 네 그림은 원본 타일을 순서대로 펼친 조사 자료입니다. 게임 화면·실제 장면·현재 한글판 표시 결과가 아닙니다. 배열과 회색은 해독 도구의 표시 방식입니다.</p><div class="gallery source-gallery">'
    static_images=[]
    for page,label in [('0F','POW 후보·별도 PUSH START'),('17','원본 타이틀·RYO51 후보'),('1D','HOW TO CONTROL 후보'),('1E','PAUSE·효과·원본 GAME OVER')]:
        p=R/f'extracted/chr/survey_20261004_001/chr_page_{page}.png';assert p.is_file()
        static_images.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'type':'Original CHR static atlas; not gameplay','page_hex':page,'label':label})
        sections+=f'<figure><img class="static-source" alt="정적 CHR {page}: {html.escape(label)}" src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"><figcaption>정적 원본 CHR {page} · {html.escape(label)}<br>실제 게임 표시 증거 아님</figcaption></figure>'
    sections+='</div><h2>유지해야 할 비교 실패</h2><p>작업163의 frame04410.png는7326픽셀이 달랐습니다. 같은 구간의 RAM·PPU·OAM·상태·매핑 일치는 픽셀 일치를 보장하지 않았습니다. 원인은 미확정이며 전체 RGB 동일 주장은 실패 상태로 유지합니다. 비교 실패를 번역 결함 확정이나 정상 확정으로 바꾸지 않았습니다.</p>'
    source=source.replace('<h2>검토 기록 방법</h2>',sections+'<h2>검토 기록 방법</h2>',1)
    source=source.replace('details.unit{','details.candidate{background:white;border:1px solid #ccd6e4;border-radius:8px;margin:12px 0;padding:14px}details.unit{',1)
    assert source.count('class="unit"')==54 and source.count('class="candidate"')==7
    assert source.count('class="static-source"')==4 and source.count('<figure>')==25
    records['static_source_images']=static_images
    decisions={'work':167,'ROM_sha256':records['ROM_sha256'],'SSOT_sha256':records['SSOT_sha256'],
        'actual_play_owner':'user','human_approved':False,'instructions':'Blank response template. Filled proposals are not automatically applied or approved. Record explicit decision and reason.',
        'wording_and_art':{'state':'pending','changes':[]},
        'outside_candidates':[{'id':i['id'],'decision':'pending','reason':'','requested_text':'','options':['preserve_original_for_this_scope','investigate_consumer','translate_after_consumer_connected']}for i in records['outside_registered_candidates']],
        'gameplay_results':[]}
    pending='''# 現在049 非플레이 결정 기록

이 파일과 JSON은 응답 양식이며 최종 승인 기록이 아니다. 실제 플레이는 사용자 담당이다. 문장54개(45초안/9기술·공유), 그림33문구와 등록 밖 후보7건을 분리한다.

- 문장·명칭: ID, 수정 전/후, 이유, 적용 장면을 기록한다.
- 생성형 그림: 타이틀/지도/매표소/게임오버의 실제 표시와 한글 철자·가독성을 확인한다. 읽기용 라벨만으로 그림을 승인하지 않는다.
- MAIN_05805의 ‘도’ 생략, MAIN_05833의 말투, MAIN_05882의 도전 표현, MAIN_05999의 PACKAGE D. 직함, 고유명사·타이틀 표기에는 최종 사람 선택이 남아 있다.
- 후보7건은 보존 초안이며 전역 영어 보존·미사용 확정이 아니다. HOWTO/PAUSE/POW를 번역하려면 먼저 글자 소비와 공유 타일 영향을 연결한다.
- NT1C와 진단 STAGE SELECT는 소비 미연결 상태다. 일반 UI로 임의 활성화하지 않는다.
- 사용자 플레이 결과는 별도로 기록한다. 이번 자료 생성은 플레이 검수나 문구 승인으로 처리하지 않는다.

결정 예시: `ID: HOWTO / 결정: 이번 범위 원문 보존 / 이유: ...` 또는 `ID: MAIN_... / 수정: ... / 이유: ...`.
'''.replace('現在049 非플레이','현재049 비플레이')
    OUT.mkdir()
    for name,value in [('review_records.json',records),('decisions_template.json',decisions),('source_inventory.json',inventory)]:
        (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf-8')
    (OUT/'review.html').write_text(source,'utf-8');(OUT/'DECISIONS_PENDING.md').write_text(pending,'utf-8')
    (OUT/'README.txt').write_text('타이니툰 어드벤처2 현재049 비플레이 검토자료 (2026-10-07)\nreview.html을 브라우저에서 열면54원천·33그림·미연결7후보를 검토할 수 있습니다.21실제화면은 기존자료 재사용이고4원본타일아틀라스는 정적자료입니다. ROM/패치/폰트/에뮬레이터는 포함하지 않습니다. 문구·범위 승인과 실제플레이 완료는 보류 상태입니다. decisions_template.json은 빈 응답양식입니다.\n','utf-8')
    mf={'work':167,'ROM_sha256':records['ROM_sha256'],'SSOT_sha256':records['SSOT_sha256'],'ROM_free':True,
        'human_review_complete':False,'files':{p.name:sha(p)for p in sorted(OUT.iterdir())if p.is_file()}}
    (OUT/'artifact_manifest.json').write_text(json.dumps(mf,indent=2)+'\n','utf-8')
    with zipfile.ZipFile(ARCHIVE,'x',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for p in sorted(OUT.iterdir()): z.write(p,(Path(OUT.name)/p.name).as_posix())
    with zipfile.ZipFile(ARCHIVE)as z:
        assert z.testzip()is None and len(z.namelist())==7
        assert all(Path(n).suffix in ['.json','.html','.txt','.md'] for n in z.namelist())
        for p in OUT.iterdir():assert z.read((Path(OUT.name)/p.name).as_posix())==p.read_bytes()
    result={'work':167,'status':'PASS_ROMFREE_RECORDS_ZIP_RENDER_PENDING','archive':ARCHIVE.relative_to(R).as_posix(),
        'archive_sha256':sha(ARCHIVE),'registered_units':54,'graphics':33,'outside_candidates':7,'actual_images_reused':21,
        'static_atlas_images':4,'new_game_execution':False,'human_approved':False,'ROM_sha256':records['ROM_sha256'],
        'SSOT_sha256':records['SSOT_sha256'],'render':'separate browser check pending'}
    report.write_text(json.dumps(result,indent=2)+'\n','utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
