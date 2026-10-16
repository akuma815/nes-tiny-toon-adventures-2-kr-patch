"""Verify current retained files and virtual historical manifests after lossless cleanup."""
import hashlib, json, zipfile
from prepare_cleanup230 import R, PLAN, digest

def audit():
    plan=json.loads(PLAN.read_text('utf-8'));archive=R/plan['archive'];assert digest(archive)==plan['archive_sha256']
    for item in plan['roots']:assert not (R/item['path']).exists(),'Superseded target remains: '+item['path']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())==set(plan['archived_files'])
        for rel,expected in plan['archived_files'].items():
            raw=z.read(rel);assert len(raw)==expected['bytes'] and hashlib.sha256(raw).hexdigest()==expected['sha256'],rel
    for rel,expected in plan['kept_files'].items():assert (R/rel).is_file() and digest(R/rel)==expected['sha256'],'Retained file changed: '+rel
    virtual=0
    for work in (225,227,228,229):
        m=json.loads((R/f'manifests/nonplay{work}_assets.json').read_text('utf-8'))
        for rel,expected in m['files'].items():
            actual=plan['archived_files'][rel]['sha256'] if rel in plan['archived_files'] else digest(R/rel)
            assert actual==expected,rel;virtual+=1
    latest=[
      'dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip',
      'dist/TinyToon2_KR_Worklog_AuthorVoice_20261009.zip',
      'dist/TinyToon12_TechnicalGuide_Reader_20261009.zip']
    for rel in latest:
        with zipfile.ZipFile(R/rel) as z:
            assert z.testzip() is None
            assert all(not n.lower().endswith(('.nes','.sav','.mss')) for n in z.namelist()),rel
    assert sorted(p.name for p in (R/'dist').glob('*.zip'))==sorted(p.split('/')[-1] for p in latest)
    for folder in ('workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009','workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009',
                   'qa/publication/author_voice229_verified','qa/publication/reader228_guide'):
        assert (R/folder).is_dir(),folder
    return {'work':230,'status':'PASS','removed_files':len(plan['archived_files']),'removed_roots':len(plan['roots']),
      'original_bytes_archived':plan['stats']['selected_bytes'],'archive_bytes':plan['archive_bytes'],
      'archive_only_bytes_reduction':plan['stats']['selected_bytes']-plan['archive_bytes'],
      'space_metric_scope':'Selected source files minus archive; excludes new handoff/index/script bytes',
      'archive_sha256':plan['archive_sha256'],'archive_payload_SHA_verified':len(plan['archived_files']),
      'retained_files_SHA_verified':len(plan['kept_files']),'historical_manifest_entries_verified_current_or_archive':virtual,
      'latest_public_ZIPs':{rel:digest(R/rel) for rel in latest},'archive_contains_ROM':True,'archive_public_upload':False,
      'game_build_executed':False,'game_apply_executed':False,'emulator_executed':False,'native_page_changed':False}

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False))
