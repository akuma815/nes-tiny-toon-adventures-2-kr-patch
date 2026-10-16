"""Current049 source census and preservation; no emulator, ROM or SSOT mutation."""
from pathlib import Path
import collections, csv, hashlib, json
from extract_text import tokens
from title_codec import unpack
from seal_nonplay166 import R, sha, seal

def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    out = R / 'workspace/translation/nonplay_inventory049_166.json'
    report = R / 'qa/reports/nonplay166_inventory.json'
    assert not out.exists() and not report.exists()
    meta = json.loads((R / 'manifests/source_rom.json').read_text('utf-8'))
    source = R / meta['path']; s = source.read_bytes()
    rom = R / 'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'; c = rom.read_bytes()
    ssot = R / 'workspace/translation/text_ja.csv'
    assert sha(source) == meta['sha256'] == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(rom) == '31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa'
    assert sha(ssot) == '43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    original = json.loads((R / 'extracted/text/table_20261004_001/text_tokens.json').read_text('utf-8'))
    rows = list(csv.DictReader(ssot.open(encoding='utf-8-sig', newline='')))
    by = {r['entry_id']: r for r in rows}; assert len(by) == len(rows) == 54
    tables = []
    for table in original['tables']:
        units = sorted([u for u in original['units'] if u['kind'] == table['kind']], key=lambda u: u['file_offset'])
        covered = []
        for u in units:
            raw = s[u['file_offset']:u['end_exclusive']]
            assert digest(raw) == u['raw_sha256'] == by[u['entry_id']]['raw_sha256']
            assert tokens(raw, u['kind']) == u['tokens']
            assert by[u['entry_id']]['source_tokens'] == u['source_tokens']
            covered.extend(range(u['file_offset'], u['end_exclusive']))
        assert covered == list(range(table['data_start'], table['data_end_exclusive']))
        ptrs = b''.join(t['cpu_pointer'].to_bytes(2, 'little') for t in table['slots'])
        assert ptrs == s[table['pointer_start']:table['pointer_end_exclusive']]
        for t in table['slots']:
            assert t['cpu_pointer'] - 0x3ff0 == t['target_file_offset']
        tables.append({k: table[k] for k in ['kind', 'pointer_slots', 'unique_targets', 'data_start', 'data_end_exclusive', 'data_bytes']})
    review = json.loads((R / 'workspace/review/translation049_20261006/review_records.json').read_text('utf-8'))
    assert review['ROM_sha256'] == sha(rom) and review['SSOT_sha256'] == sha(ssot)
    assert len(review['graphics']) == 33
    for g in review['graphics']:
        if 'plan' in g: assert sha(R / g['plan']) == g['plan_sha256']
    chr_banks = []
    for bank in range(128):
        a = s[0x20010 + bank * 1024:0x20010 + (bank + 1) * 1024]
        b = c[0x40010 + bank * 1024:0x40010 + (bank + 1) * 1024]
        assert len(a) == len(b) == 1024
        chr_banks.append({'bank': bank, 'source_file_offset_hex': f'{0x20010+bank*1024:X}',
                          'current_file_offset_hex': f'{0x40010+bank*1024:X}', 'source_sha256': digest(a),
                          'current_sha256': digest(b), 'equal': a == b, 'different_bytes': sum(x != y for x, y in zip(a, b))})
    changes = {b['bank']: b['different_bytes'] for b in chr_banks if not b['equal']}
    assert changes == {18:214,80:202,81:91,82:98,92:873,93:924,94:441,100:648,101:189,102:239}
    nt_catalog = json.loads((R / 'work/graphics_population_001/native_NT_catalog.json').read_text('utf-8'))['assets']
    assert len(nt_catalog) == 20
    nt = []
    for a in nt_catalog:
        offset = a['source_file_offset']; n = a['encoded_length']; raw = s[offset:offset+n]
        assert digest(raw) == a['encoded_sha256']
        cells, consumed = unpack(raw); assert consumed == n and len(cells) == a['decoded_cells']
        pointer_offset = 0x40d1+a['selector'] if a['selector'] < 0x1e else 0x4243+a['selector']-0x1e
        ptr = int.from_bytes(s[pointer_offset:pointer_offset+2], 'little')
        mapped = ptr-0x3ff0 if a['selector'] < 0x1e else 0x20010+18*1024+ptr-0x1000
        assert mapped == offset
        nt.append({'selector_hex': f"{a['selector']:02X}", 'source_file_offset_hex': f'{offset:X}',
                   'encoded_bytes': n, 'source_sha256': digest(raw), 'decoded_cells': len(cells),
                   'consumer_state': 'unlinked; not excluded' if a['selector'] == 0x1c else 'historical named/alternate consumer; scope is in109..112'})
    printer = json.loads((R / 'qa/reports/printer113_catalog.json').read_text('utf-8'))
    assert s[0x4123:0x41db] == c[0x24123:0x241db]
    printer_records = []
    for p in printer['catalog']:
        a = p['source_offset']; n = p['encoded_length']
        assert digest(s[a:a+n]) == p['source_sha256'] and s[a:a+n] == c[a+0x20000:a+0x20000+n]
        printer_records.append({k:p[k] for k in ['index','pointer_CPU','classification','encoded_length','source_offset','source_sha256']})
    # Work103 supply bounds are historical047. We do NOT upgrade those runtime claims to049.
    candidates = [
        {'id':'HOWTO','text':'HOW TO CONTROL','banks':[116,117], 'evidence_works':[99,100],
         'facts':'Source banks used for ride decoration; selector10 has zero label tiles90..96. Historical047 bounded path reads decoration, not label.',
         'limit':'Other consumers/branches remain unresolved. Bank use does not prove label use.', 'proposal':'원문 보존 초안. 글자 소비가 연결되면 번역 대상으로 추가.'},
        {'id':'PAUSE','text':'PAUSE','banks':[120,121], 'evidence_works':[49,101,102,103],
         'facts':'Historical042 native pause/resume and bounded047 animation/IRQ suppliers do not select label banks.',
         'limit':'Indexed/indirect alternatives are not globally closed; not a proven unused graphic.', 'proposal':'원문 보존 초안. 실제 일시정지 글자 소비가 연결되면 번역.'},
        {'id':'POW','text':'POW / BOOM effect candidates','banks':[61], 'evidence_works':[96,97,98,120,123],
         'facts':'Same bank61 has a proven flag consumer; river bank61 supplies rope art. Fireworks9D..A2 use bank54.',
         'limit':'No consumer proves the selected effect tiles. Flag/rope observations are not POW display evidence.', 'proposal':'효과음 그림은 원문 보존 초안. 미사용 확정은 하지 않음.'},
        {'id':'PUSH_START_PAGE0F','text':'PUSH START','banks':[63], 'evidence_works':[166],
         'facts':'Raw source CHR page0F contains these letter pixels; all source bank63 bytes retained in049.',
         'limit':'CHR atlas visual candidate only. Independent from preserved title-page PUSH START. Live consumer not linked.', 'proposal':'독립 소비 조사 후보. 타이틀 보존 결정을 이 후보에 자동 적용하지 않음.'},
        {'id':'RYO51_PAGE17','text':'RYO51','banks':[95], 'evidence_works':[166],
         'facts':'Raw source CHR page17 has signature-like RYO51 pixels; source bank95 is byte exact in049.',
         'limit':'Authorship/visible consumer unconfirmed. Same bank contains protected title sprite resources.', 'proposal':'서명·크레딧 추정이므로 보존 초안. 소비와 의미 확인 전 편집하지 않음.'},
        {'id':'NT1C','text':'unclassified nametable1C','banks':[], 'evidence_works':[109,112,119],
         'facts':'Native pointer8BF9/source4C09 defines99 bytes ->1024 cells. Current24C09 is identical.',
         'limit':'No connected native caller/live rendering font. Tile resemblance does not establish decorative-only or unused.', 'proposal':'원천 보존. 신규 문구로 세지 않고 소비 미연결 데이터로 관리.'},
        {'id':'DIAGNOSTIC_STAGE_SELECT','text':'STAGE SELECT / 1 0','banks':[124], 'evidence_works':[110,113],
         'facts':'8113 queue index9/81B2 decodes under candidate font124. Named callerCD52 skipped by default root3 entry.',
         'limit':'Actual visible font/consumer and all reachability remain unproved. Diagnostic candidate, not an inserted translation.', 'proposal':'숨겨진 진단 UI는 보존 초안. 일반 UI를 임의로 켜거나 삽입하지 않음.'}
    ]
    assert s[0x4c09:0x4c6c] == c[0x24c09:0x24c6c]
    for item in candidates:
        item['state'] = 'preserved_unresolved'
        item['decision'] = 'pending'; item['human_approved'] = False
        item['current049_static_bank_preservation_exact'] = all(chr_banks[b]['equal'] for b in item['banks'])
        assert item['current049_static_bank_preservation_exact']
        item['bank_hashes'] = [chr_banks[b] for b in item['banks']]
    inventory = {'work':166,'build':'dialogue_kr_poc_049','ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),
        'source_sha256':sha(source),'registered_text':{'units':54,'draft':45,'technical_shared':9,'tables':tables,
         'all_registered_source_bytes_and_pointers_covered_exact':True,'status_counts':dict(collections.Counter(r['status'] for r in rows)),
         'technical_ids':[r['entry_id'] for r in rows if r['status']=='untranslated'],
         'limit':'Nine are technical/shared units, not nine untranslated Japanese paragraphs. Only these two renderer tables closed.'},
        'registered_graphics':review['graphics'],'source_CHR':{'banks':128,'tiles':8192,'changed_banks':10,'unchanged_banks':118,
         'different_bytes':sum(changes.values()),'records':chr_banks,'limit':'All original CHR bytes inventoried. Human visual atlas scan discovers candidates, not global language/consumer closure.'},
        'source_NT':nt,'alternate_printer':{'pointer_slots':12,'unique_targets':5,'current049_code_and_catalog_preserved':True,'records':printer_records},
        'outside_registered_candidates':candidates,'outside_candidate_count':7,'global_corpus_closed':False,
        'all_unused_proven':False,'human_approved':False,'actual_play_owner':'user','emulator_runs':0,
        'build_changes':False,'translation_changes':False,'release_eligible':False}
    out.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n','utf-8')
    result = {'work':166,'status':'PASS_BOUNDED_CURRENT049_SOURCE_CENSUS_PRESERVATION',
        'inventory':out.relative_to(R).as_posix(),'inventory_sha256':sha(out),
        'registered_units':54,'registered_graphics':33,'source_CHR_banks':128,'unchanged_CHR_banks':118,'changed_CHR_banks':10,
        'changed_CHR_bytes':sum(changes.values()),'source_NT_streams':20,'alternate_printer_slots':12,'alternate_printer_unique_targets':5,
        'unresolved_outside_candidates':7,'global_corpus_closed':False,'ROM_sha256':sha(rom),'CSV_sha256':sha(ssot),
        'new_emulator_or_CPU_runtime':False,'human_approved':False,'limits':['Static census/preservation only; no new actual play or scene visual validation.','Historical047 consumer observations remain scoped047; byte preservation is current049 static evidence only.','No candidate deleted, translated, excluded as unused, or human-approved automatically.']}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    body = f'''[現在049原천목록](../{out.relative_to(R).as_posix()})과 [정적 검증 보고](../{report.relative_to(R).as_posix()})를 작성했다. 등록 본문은 48 포인터/46 본문 + 9 포인터/8 공유 단위 = 54개이다. 원천 두 연속 영역 1055+60바이트와 114 포인터 바이트를 전체 대조했으며 누락·중첩이 없다. 이는 등록된 두 테이블의 완결성이다. 전체 게임의 원천 목록 완결성을 뜻하지 않는다. 45개는 번역 초안이며 나머지 9개는 기술/공유 단위다.

그림 문구 33개를 현재 검토 기록 및 각 삽입 계획 SHA와 대조했다. 원본 CHR 128개 1KiB 뱅크/8192 타일을 현재049의 원본 대응 위치와 전수 대조했다. 118뱅크는 동일, 10뱅크는 총3919바이트 변경이다. 변경 뱅크는18/80/81/82/92/93/94/100/101/102이며 각 바이트 차이 수와 양측 SHA를 목록에 기록했다. HOWTO116/117, PAUSE120/121, POW61, 별도 PUSH START63, RYO51의95는 현재049에서도 동일하다.

원본 NT20개를 포인터와 압축 형식으로 다시 해석했다. 별도8113 프린터12슬롯/5원천도 현재049에서 보존됨을 확인했다. 미연결 후보는 HOWTO, PAUSE, POW, CHR0F PUSH START, CHR17 RYO51, NT1C, 진단 STAGE SELECT의7건으로 통합했다. 새 두 픽셀 후보는 원천 아틀라스에서 발견한 후보이며 실제 표시 문구로 등록하지 않았다. 각 후보의 소비 근거·한계·원문 보존 제안을 분리했다. 전역 미사용/제외/최종 원문 보존 승인으로 확정하지 않았다. 기존047/042 소비 관찰은 해당 빌드의 역사 증거로 유지했다.

변경 파일은 새 inventory/검증기/보고와 인계문서 및manifest이다. ROM SHA `{sha(rom)}`, CSV SHA `{sha(ssot)}` 불변. manifest에 신규와 사용 근거의 SHA를 고정한다. 재현: `python scripts/inventory_nonplay166.py` (출력 보호로 기존 파일이 있으면 중단; 별도 복사한 조사 디렉터리에서 실행), `python scripts/audit_scoped_work.py --manifest manifests/nonplay166_assets.json --output qa/reports/nonplay166_session.json`. 정적 바이트/테이블/토큰 검증 PASS. 신규 CPU 실행·빌드·적용·에뮬레이터·플레이·청음·사람 최종 승인 없음. 실제 플레이는 사용자 담당이다.'''.replace('現在049原천목록','현재049 원천목록')
    refs = [out, report, Path(__file__), source, rom, ssot,
        R/'extracted/text/table_20261004_001/text_tokens.json',R/'work/graphics_population_001/native_NT_catalog.json',
        R/'workspace/review/translation049_20261006/review_records.json',R/'qa/reports/printer113_catalog.json']
    refs.extend(R/g['plan'] for g in review['graphics'] if 'plan' in g)
    seal(166,'CURRENT049_NONPLAY_SOURCE_INVENTORY.md','현재049 원천 전수 목록·미연결 후보 통합',body,
        '등록54본문·33그림, 원본CHR128뱅크와NT20/별도프린터12슬롯 정적 대조. 후보7건 보존·미연결 유지. ROM/CSV 불변.',
        '현재049 문장·그림 검토자료와 후보7건을 통합한 비플레이 결정 자료를 만들고 PC/모바일 표시 및 ZIP 무결성을 확인한다.',refs)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
