"""Validate live and archived evidence without rewriting historical reports."""
from pathlib import Path
import hashlib, json, re, sqlite3, zipfile
from archive_cleanup214 import R, digest

def main():
    report = json.loads((R / 'qa/reports/cleanup214_archive.json').read_text('utf-8'))
    deletion = json.loads((R / 'qa/reports/cleanup214_deletion.json').read_text('utf-8-sig'))
    assert deletion['status'] == 'PASS'
    archive = R / report['archive_path']
    assert digest(archive) == report['archive_sha256'] == deletion['archive_sha256']
    db = sqlite3.connect(f'file:{archive.as_posix()}?mode=ro',uri=True)
    assert db.execute('SELECT value FROM metadata WHERE key="state"').fetchone()[0] == 'VERIFIED'
    frozen = {}; live = archived = 0
    for work in range(197,214):
        p = R / f'manifests/nonplay{work}_assets.json'
        d = json.loads(p.read_text('utf-8'))
        for n,h in d['files'].items():
            if (R / n).is_file():
                assert digest(R / n) == h, (work,n)
                live += 1
            else:
                row = db.execute('SELECT sha256 FROM entries WHERE path=?',(n,)).fetchone()
                assert row and row[0] == h, (work,n)
                archived += 1
        frozen[str(work)] = {'manifest_sha256':digest(p),'files':len(d['files'])}
    compact = json.loads((R / 'work/cleanup214/deletion_plan.json').read_text('utf-8'))
    staged = R / compact['staging_path']
    retained = 0
    index = json.loads((R / 'manifests/cleanup214_retained_live.json').read_text('utf-8'))
    assert index['archive_sha256'] == report['archive_sha256']
    for n,h in index['files'].items():
        expected = db.execute('SELECT sha256 FROM entries WHERE path=?',(n,)).fetchone()[0]
        assert digest(R / n) == expected == h, n
        if staged.exists(): assert digest(staged / n) == h, n
        retained += 1
    assert retained == report['restored_live_files']
    expected = {
        'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d',
        'workspace/translation/text_ja.csv':'43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f',
        'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes':'b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24',
        'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes':'7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce',
        'build/text11_211_rebuild062/TinyToon2_Text11_Candidate062.nes':'7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce',
        'build/text11_candidate_062/TinyToon2_Text11_Candidate062.ips':'13023b6eb6b4a4bf61f112f8d3fa2b90f4543307931c361eec3de05bc2762b8d',
        'dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip':'377b16522c31f3516869c9eb14acb925799ceeefa1051d06508570770bc19575'}
    for n,h in expected.items(): assert digest(R / n) == h,n
    package = 'TinyToonAdventures2_KR_Text11_Candidate062_20261009'
    with zipfile.ZipFile(R / f'dist/{package}.zip') as z:
        assert z.testzip() is None
        assert len(z.namelist()) == 68
        assert not any(n.lower().endswith('.nes') for n in z.namelist())
        for n in z.namelist():
            if not n.endswith('/'):
                assert n.startswith(package+'/') and '..' not in n.split('/'), n
                assert hashlib.sha256(z.read(n)).hexdigest() == digest(R / 'dist' / n), n
    for n in ['build/dialogue_kr_poc_037/ui_korean_page_mapping.json',
              'build/ordinary11_candidate_059/ordinary11_plan.json',
              'qa/dialogue/cards033_actual_pages.json']:
        assert (R / n).is_file(), n
    links = 0; exceptions = []
    for p in [R/'README.md',R/'AGENTS.md',*sorted((R/'docs').rglob('*.md')),
              *sorted((R/'workspace/review').rglob('*.html')),*sorted((R/'dist').rglob('*.html'))]:
        text = p.read_text('utf-8-sig')
        refs = [a or b for a,b in re.findall(r'\]\((?:<([^>\n]+)>|([^()\n]+))\)',text)]
        refs += re.findall(r'(?:src|href)=["\']([^"\']+)',text)
        for n in refs:
            n = n.strip().split('#')[0].split('?')[0]
            if not n or re.match(r'(?:[a-z]+://|data:|mailto:|javascript:)',n): continue
            target = (p.parent/n).resolve()
            if target.is_relative_to(R):
                assert target.exists(), (p,n)
                links += 1
            elif not target.exists(): exceptions.append(str(target))
    db.close()
    smoke = json.loads((R/'qa/reports/cleanup214_restore_smoke_completed.json').read_text('utf-8-sig'))
    assert smoke['status'] == 'PASS_RESTORED_IDENTICAL_REUSE_TEST_COPY_RETAINED'
    assert digest(R/smoke['path']) == smoke['sha256']
    smoke_bytes = (R/smoke['path']).stat().st_size
    removed = sum(z['archived_files']-z['live_files'] for z in deletion['directories']) - 1
    deleted_bytes = sum(z['archived_bytes']-z['live_bytes'] for z in deletion['directories']) - smoke_bytes
    cache_files = sum(z['files'] for z in deletion['caches'])
    cache_bytes = sum(z['bytes'] for z in deletion['caches'])
    out = R / 'qa/reports/cleanup214_audit.json'
    result = {'work':214,'status':'PASS','frozen197_213':frozen,'frozen_asset_live_checks':live,'frozen_asset_archive_checks':archived,
              'restored_files_SHA256_checked':retained,'current_source_CSV_ROM_IPS_package_SHA256':expected,
              'package_CRC_and_all_68_payloads_exact':True,'project_links_checked':links,'missing_project_links':[],
              'historical_external_links_unavailable':sorted(set(exceptions)),
              'expanded_history_files_removed':removed,'expanded_history_bytes_removed':deleted_bytes,
              'cache_files_removed':cache_files,'cache_bytes_removed':cache_bytes,
              'actual_restore_smoke':'PASS_NEW_FILE_AND_IDENTICAL_EXISTING',
              'one_restore_test_PNG_retained_after_direct_deletion_policy_rejection':{'path':smoke['path'],'bytes':smoke_bytes,'sha256':smoke['sha256']},
              'net_payload_bytes_saved_excluding_temporary_inventory':deleted_bytes+cache_bytes-report['archive_bytes'],
              'runtime':'NOT_RUN','ROM_modification':'NONE','user_Mesen_and_saves':'NOT_TOUCHED'}
    if out.exists():
        old = json.loads(out.read_text('utf-8'))
        assert old['status'] == 'PASS' and old['current_source_CSV_ROM_IPS_package_SHA256'] == expected
        assert old['frozen197_213'] == frozen
        # Existing immutable audit remains unchanged; current link count may increase after sealing.
    else:
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('frozen197_213','current_source_CSV_ROM_IPS_package_SHA256')},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
