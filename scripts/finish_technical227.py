"""Post-cleanup check and dated addendum without rewriting sealed evidence."""
import json,re
from seal_nonplay171 import R,sha
q=json.loads((R/'qa/reports/technical227_cache_cleanup.json').read_text('utf-8-sig'))
assert q['status']=='DELETED_OWN_FINISHED_RENDER_CACHE' and not (R/q['target']).exists()
m=json.loads((R/'manifests/nonplay227_assets.json').read_text('utf-8'))
for rel,digest in m['files'].items():assert sha(R/rel)==digest,rel
assert sha(R/'dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip')=='0e470e45968cb388f296a3103c0004641ede834f14872921d087250d9f0c0aaa'
assert sha(R/'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip')=='32ac4f3938ea0659216e1fae61a6ad6463ed2091c8470a0af5db360a686e1e9c'
assert sha(R/'workspace/translation/text_ja.csv')=='43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
entry=f'''\n\n### 작업227 마무리 — 렌더 캐시 정리

종료된 자체 기술지침 렌더의 browser_profile만 정확 경로로 삭제했다. {q['removed_files']}파일/{q['removed_bytes']:,}바이트이며 렌더 보고·4PNG·게시원천·최종ZIP은 보존했다. 정리 후227 봉인 파일 {len(m['files'])}개 SHA 및 기존 게임 배포/작업기ZIP·번역CSV 불변 확인 PASS. 캐시 정리 실행은 powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cleanup_technical227.ps1, 마무리검사는 python -B scripts/finish_technical227.py다. [캐시정리보고](../qa/reports/technical227_cache_cleanup.json). 새게임/카페게시없음.

다음 작업 하나: 사용자가 완성한 기술 지침 본문과 설명도2개를 게시 위치에 배치하고 배포 후 제보를 수집한다.
'''
for rel in ('docs/HANDOFF_2026-10-09.md','docs/HANDOFF.md','docs/journal/2026-10-09.md'):
    p=R/rel;txt=entry if '/journal/' not in rel else entry.replace('(../qa/', '(../../qa/')
    p.write_text(p.read_text('utf-8')+txt,'utf-8')
assets=[R/'scripts/cleanup_technical227.ps1',R/'scripts/finish_technical227.py',R/'qa/reports/technical227_cache_cleanup.json']
out=R/'manifests/technical227_post_cleanup_assets.json';assert not out.exists()
out.write_text(json.dumps({'work':227,'status':'PASS_POST_CLEANUP','sealed227_sha256':sha(R/'manifests/nonplay227_assets.json'),
 'files':{p.relative_to(R).as_posix():sha(p) for p in assets}},ensure_ascii=False,indent=2)+'\n','utf-8')
for p in (R/'docs/HANDOFF.md',R/'README.md'):
    top=p.read_text('utf-8').split('## 이전 작업 당시의 역사 기록')[0]
    for rel in re.findall(r'\]\(([^)]+)\)',top):
        if rel.startswith('https://'):continue
        assert (p.parent/rel).is_file(),(p.name,rel)
print('PASS sealed227 hashes, retained releases/CSV, exact cache cleanup and current links')
