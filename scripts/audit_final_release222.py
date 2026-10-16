"""Final live/archive proof after cleanup; never overwrites historical verification."""
from pathlib import Path
import json,sqlite3,zipfile,hashlib,subprocess
from seal_nonplay171 import R,sha

def main():
    cleanup=json.loads((R/'qa/reports/cleanup222_deletion.json').read_text('utf-8-sig'))
    plan=json.loads((R/'work/cleanup222/final_plan.json').read_text('utf-8-sig'))
    archive_proof=json.loads((R/'qa/reports/obsolete_distribution223_archive.json').read_text('utf-8'))
    assert cleanup['status']=='DELETED_LOSSLESS_HISTORY_AND_DISPOSABLE_CACHES'
    assert sha(R/archive_proof['archive'])==archive_proof['archive_sha256']
    databases={}
    for number in ('214','222'):
        p=R/plan['archive'+number];assert sha(p)==plan['archive'+number+'_sha256']
        databases[number]=sqlite3.connect(f'file:{p.as_posix()}?mode=ro',uri=True)
    objects=0
    for h,size,data in databases['222'].execute('SELECT sha256,raw_bytes,data FROM objects'):
        import zlib
        raw=zlib.decompress(data);assert len(raw)==size and hashlib.sha256(raw).hexdigest()==h;objects+=1
    assert databases['222'].execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    live=archived=0
    def verify_file(rel,digest):
        nonlocal live,archived
        if (R/rel).is_file() and sha(R/rel)==digest:live+=1;return
        for db in databases.values():
            row=db.execute('SELECT sha256 FROM entries WHERE path=?',(rel,)).fetchone()
            if row and row[0]==digest:archived+=1;return
        if rel in archive_proof['files'] and archive_proof['files'][rel]['sha256']==digest:
            archived+=1;return
        raise AssertionError(('Missing immutable asset',rel,digest))
    manifests={}
    for number in range(197,222):
        p=R/f'manifests/nonplay{number}_assets.json'
        if not p.exists():continue
        q=json.loads(p.read_text('utf-8'));manifests[str(number)]={'files':len(q['files']),'sha256':sha(p)}
        for rel,digest in q['files'].items():verify_file(rel,digest)
    for group in plan['groups']:
        for entry in group['retain']:assert (R/entry['path']).is_file() and sha(R/entry['path'])==entry['sha256']
        if group['kind']=='DISPOSABLE_ISOLATED_BROWSER_CACHE':assert not (R/group['path']).exists()
    assert not (R/plan['staging']).exists()
    old_deleted=json.loads((R/'qa/reports/obsolete_distribution223_deletion.json').read_text('utf-8-sig'))
    for item in archive_proof['roots']:assert not (R/item['path']).exists()
    packages={}
    for proof_file in ('release220_verified.json','publication221_verified.json'):
        q=json.loads((R/'qa/reports'/proof_file).read_text('utf-8'));archive=R/q['archive'];assert sha(archive)==q['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None and len(z.namelist())==q['files']
            assert all(not name.lower().endswith(('.nes','.mss','.sqlite','.sav')) for name in z.namelist())
            for name in z.namelist():
                rel=name.split('/',1)[1];assert hashlib.sha256(z.read(name)).hexdigest()==q['contents_sha256'][rel]
        packages[proof_file]={'archive':q['archive'],'sha256':sha(archive),'files':q['files'],'CRC_payload_ROMfree':'PASS'}
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(R/'workspace/translation/text_ja.csv')=='43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    assert sha(R/'build/release_v1_0_220/TinyToon2_KR_v1.0.nes')==sha(R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes')=='7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce'
    # Exercise the actual restore CLI on one small historical QA image, retained
    # afterwards as proof of recovery and as the linked second-sign example.
    sample='qa/dialogue/moving_stop182_051/frame_04272.png';absent=not (R/sample).exists()
    row=databases['222'].execute('SELECT sha256,bytes FROM entries WHERE path=?',(sample,)).fetchone();assert row
    subprocess.run(['python','-B',str(R/'scripts/restore_history222.py'),'--file',sample],check=True,capture_output=True)
    assert sha(R/sample)==row[0]
    removed=plan['stats']['removed_files']+plan['stats']['cache_files']+old_deleted['files']
    gross=plan['stats']['removed_bytes']+plan['stats']['cache_bytes']+old_deleted['bytes']
    added=plan['archive222_bytes']+archive_proof['archive_bytes']+(row[1] if absent else 0)
    q={'work':222,'status':'PASS_FINAL_RELEASE_PUBLICATION_LOSSLESS_CLEANUP',
       'frozen_manifests':manifests,'live_asset_checks':live,'archived_asset_checks':archived,'archive222_objects_verified':objects,
       'packages':packages,'source_CSV_ROM_unchanged':True,'retained_file_checks':plan['stats']['retained_files'],
       'removed_files':removed,'gross_removed_bytes':gross,'new_archives_and_restore_bytes':added,
       'net_payload_bytes_saved':gross-added,'actual_restore_smoke':{'file':sample,'was_absent':absent,'sha256':row[0],'retained_as_QA_evidence':True},
       'blocked214_folder_not_touched':True,'new_gameplay_or_cafe_upload':False}
    out=R/'qa/reports/final_release222_audit.json';assert not out.exists();out.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:q[k] for k in ('status','live_asset_checks','archived_asset_checks','removed_files','net_payload_bytes_saved','actual_restore_smoke')},ensure_ascii=False))

if __name__=='__main__':main()
