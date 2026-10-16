"""Package unchanged049 with six explicit original-retention decisions and review173."""
from pathlib import Path
import hashlib, json, zipfile
from seal_nonplay171 import R, sha

NAME='TinyToonAdventures2_KR_Review_049_Scope173_20261008'
OUT=R/'dist'/NAME

def main():
    archive=OUT.with_suffix('.zip');report=R/'qa/reports/nonplay173_package.json'
    assert not any(p.exists() for p in [OUT,archive,report])
    prior=json.loads((R/'qa/reports/nonplay171_package.json').read_text('utf-8'))
    final=json.loads((R/'qa/reports/nonplay171_final.json').read_text('utf-8'))
    old=R/'dist'/Path(prior['archive']).stem
    assert sha(R/prior['archive'])==prior['archive_sha256']==final['archive_sha256']
    for f,h in prior['contents_sha256'].items():assert sha(old/f)==h
    review=R/'workspace/review/nonplay049_20261008_173'
    mf=json.loads((review/'artifact_manifest.json').read_text('utf-8'))
    for f,h in mf['files'].items():assert sha(review/f)==h
    ui=R/'qa/review/nonplay049_173_render/render_report.json'
    assert json.loads(ui.read_text('utf-8'))['status']=='PASS'
    records=json.loads((review/'review_records.json').read_text('utf-8'))
    combined=json.loads((review/'scope_decisions.json').read_text('utf-8'))
    all_decisions=[]
    for s in combined['sources']:
        assert sha(review/s['file'])==s['sha256']
        all_decisions+=json.loads((review/s['file']).read_text('utf-8'))['decisions']
    assert combined['decisions']==all_decisions and len(all_decisions)==6
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';ssot=R/'workspace/translation/text_ja.csv'
    assert sha(rom)==records['ROM_sha256']==prior['ROM_sha256']
    assert sha(ssot)==records['SSOT_sha256']==prior['SSOT_sha256']
    assert records['outside_population_summary']['still_unresolved_count']==0
    data={p.relative_to(old).as_posix():p.read_bytes() for p in old.rglob('*') if p.is_file() and not p.is_relative_to(old/'review')}
    release=json.loads(data['release_report.json'])
    release.update(name=NAME,date='2026-10-08',version='0.1.0-review049-scope173',status='DEVELOPMENT_REVIEW',
        artifact_policy='Private review173; six named source records original-retained by explicit user decisions169/173. Unchanged049 patch/helpers/tools.',
        distribution_eligible=False,global_corpus_closed=False,actual_play_owner='user')
    release['outside_candidates']=[{k:d[k] for k in ['id','state','decision','human_approved']} for d in records['outside_registered_candidates']]
    release['outside_population_summary']=records['outside_population_summary']
    release['scope_decision']={'file':'review/scope_decisions.json','sha256':sha(review/'scope_decisions.json'),
        'sources':combined['sources'],'projection_decisions_exact':True,'approved_by':'user','answer':'이번 범위에서는 원문 유지',
        'IDs':[d['id'] for d in all_decisions],
        'limit':'Six named records only. Consumer uncertainty6 remains; not global unused/corpus or final wording/art/play/release approval.'}
    release['private_review'].update(source_work=173,user_retention=6,unresolved_candidates=0,
        source_manifest_sha256=sha(review/'artifact_manifest.json'),human_final_review=False)
    release['unperformed']=['user actual-play review','all branches','global corpus closure','six original-retained consumers',
        'all reset/state contexts and crossbuild compatibility','hardware','PCM listening','final wording/names/art decisions']
    release['previous_package_actual_apply171']={'report':'qa/reports/nonplay171_final.json','sha256':sha(R/'qa/reports/nonplay171_final.json'),
        'scope':'Historical application of identical binary payload; final173 ZIP separately verified.'}
    release['apply_verification']['scope']='Historical132 eight checks. Final173 ZIP application: qa/reports/nonplay173_final.json.'
    release['status_scope']='Private package only. Final173 actual Windows apply proof external in qa/reports/nonplay173_final.json; no public distribution approval.'
    release['verification_reports']['review173_browser']={'sha256':sha(ui),'scope':'Private HTML desktop/mobile only, no new game execution.'}
    data['release_report.json']=(json.dumps(release,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    notes='''# 타이니툰 어드벤처 2 — 검토용049 · 보존 범위 반영173

사용자 검수용 ROM 없는 개발 패키지다. 결과 ROM·패치·적용 도구는 검증한049와 동일하다. 등록54원천은45본문초안과9기술/공유 단위이며 일본어9문장 미번역이나 전체 게임 번역률을 뜻하지 않는다. 그림33문구·말투·이름·생성형 타이틀의 최종 판단과 실제 플레이는 사용자 검수가 남아 있다.

이번 범위의 원문 유지 확정6건: HOWTO·PAUSE·POW(사용자 결정169), RYO51·NT1C·진단 STAGE SELECT(사용자 결정173). review/scope_decisions169.json과 scope_decisions173.json은 원본 결정 기록이고 scope_decisions.json은 읽기용 합본이다. 실제 표시가 있어도 이6건은 추가 번역하지 않는다. 소비 미연결6건의 기술 상태는 그대로이며 미사용/전역 영어 보존/전체 게임 승인을 뜻하지 않는다. 기존 타이틀 PUSH START는 스프라이트8E/CHR63 소비에 연결된 기존 보존 안내다. 발견7건의 번역 범위 미결정은0이다.

049 일반 티켓 부족 안내는 ‘아쉽지만 / 티켓이 부족해!’이며 전용226/227 폰트를 native clear 이후 선택한다. 공유196/197과macro를 보존했고 실패048은 채택하지 않았다. helper의38cycles/page 추가에 따른 idle RNG/RAM22·CPU/IRQ 차이는 알려진 한계다.

기존 검증은 정적 계약·독립 재빌드·IPS/Windows xdelta 적용과 명시 조건의 제한된 실제 장면 회귀다. 작업133의 상태복원과 리셋 후 재입장은 한정049 조건이다. 모든 상태·다른 빌드 저장 호환성·전게임 완주·모든 분기·실기·PCM청음을 검증한 것은 아니다. 작업163의 frame04410 PNG7326픽셀 차이/원인 미확정도 보존한다. raw RAM/PPU/OAM/상태 일치를 전체RGB 동일성으로 확대하지 않는다.

review/review.html은 등록54원천·33그림·발견7건을 담았다.21실제게임 PNG는 기존 근거 재사용(14역사빌드/7현재049),4CHR 아틀라스는 정적자료다. 이번 작업은 문서/ZIP과 실제 Windows 패치 적용 검증이며 새 게임 실행은 없다. 지원 원본/결과 해시와 적용법은 README_적용방법.txt를 따른다. 실제 플레이는 사용자 담당이다.

ROM·글꼴 파일·에뮬레이터를 포함하지 않으며 기존 도구/글꼴 라이선스를 보존했다. 최종 공개 배포와 네이버 카페 완성 작업기는 사용자 검수와 전체 작업 완료 후 진행한다. 외부 게시하지 않았다.
'''
    data['RELEASE_NOTES_KO.md']=notes.encode('utf-8')
    text=data['README_적용방법.txt'].decode('utf-8').replace('반영171','반영173')
    text=text[:text.index('\nHOWTO·PAUSE·POW는')]
    text+='\nHOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT는 이번 범위에서 원문 유지로 확정됐습니다. 최신173 검토자료와 원본 결정 기록169/173을 포함합니다. 발견7건의 범위 미결정은0이며 전체 최종 승인과 소비 미확정6건은 별도입니다.\n'
    data['README_적용방법.txt']=text.encode('utf-8')
    guide=data['사용자검수안내.txt'].decode('utf-8').replace('HOWTO/PAUSE/POW는 승인된 원문 유지 대상입니다.','HOWTO/PAUSE/POW/RYO51/NT1C/진단 STAGE SELECT는 이번 범위에서 승인된 원문 유지 대상입니다.')
    data['사용자검수안내.txt']=guide.encode('utf-8')
    data['알려진한계.md']='''# 현재049 지원 범위와 알려진 한계 ·173

실제 플레이는 사용자 담당이다. 원본/결과 SHA를 확인하고 새 게임으로 시작한다. 모든 분기/완주·다른 빌드 저장상태 호환성·실기·PCM청음과 최종 말투·이름·그림 검수는 미완료다.

HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT는 명시적 사용자 선택으로 이번 범위 원문 유지다. 소비 미연결6건은 기술 상태로 남지만 추가 번역 잔여로 세지 않는다. 타이틀 PUSH START는 기존 보존 안내 소비에 연결됐다. 발견7건의 번역 범위 미결정은0이나 전역 원천 목록 완결성은 미확정이다.

049의38cycles/page 추가에 따른 idle 난수/CPU/IRQ 차이와163 PNG7326픽셀 비교 실패/원인 미확정을 유지한다. 작업133 상태복원/리셋 재입장 통과는 그049 조건만이다. 정적·빌드·실제적용·한정런타임·사용자플레이 근거를 구분한다. 과거 실패나 씨드/진단 결과를 자연완주로 표현하지 않는다.

이 묶음은 검토용이다. 카페 완성 작업기와 공개 배포 확정은 전체 작업 완료 후 진행한다. 전체 승인이나 외부 게시 기록이 아니다.
'''.encode('utf-8')
    for p in review.iterdir():
        if p.is_file():data['review/'+p.name]=p.read_bytes()
    data.pop('SHA256.txt')
    data['SHA256.txt']=''.join(hashlib.sha256(b).hexdigest()+'  '+f+'\n' for f,b in sorted(data.items())).encode('utf-8')
    assert len(data)==23
    assert not any(Path(f).suffix.lower() in ['.nes','.rom','.bin','.ttf','.otf','.sav','.state'] for f in data)
    unchanged=['apply.cmd','apply.ps1',release['patch']['file'],*release['tools']['files_sha256']]
    for f in unchanged:assert data[f]==(old/f).read_bytes()
    OUT.mkdir()
    for f,b in data.items():
        p=OUT/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(data):z.write(OUT/f,NAME+'/'+f)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==23
        for f,b in data.items():assert z.read(NAME+'/'+f)==b
    archive.with_name(archive.name+'.sha256').write_text(sha(archive)+'  '+archive.name+'\n','utf-8')
    result={'work':173,'status':'PASS_ROMFREE_SCOPE_PACKAGE_FINAL_APPLY_PENDING','archive':archive.relative_to(R).as_posix(),
        'archive_sha256':sha(archive),'files':23,'ROM_free':True,'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),
        'unchanged_binary_payload':unchanged,'exact_review173':True,'approved_retention':6,'unresolved_scope_decisions':0,
        'consumer_uncertainty':6,'new_game_execution':False,'distribution_eligible':False,'human_final_review':False,
        'contents_sha256':{f:sha(OUT/f) for f in sorted(data)}}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='contents_sha256'},indent=2))

if __name__=='__main__':main()
