"""Package unchanged049 with current support notes and private review; no game execution."""
from pathlib import Path
import copy, hashlib, json, zipfile
from seal_nonplay166 import R, sha

NAME='TinyToonAdventures2_KR_Review_049_20261007'

def main():
    old=R/'dist/TinyToonAdventures2_KR_Review_049_20261006'
    out=R/'dist'/NAME;archive=R/'dist'/f'{NAME}.zip'
    report=R/'qa/reports/nonplay168_package.json'
    assert not out.exists()and not archive.exists()and not report.exists()
    previous=json.loads((R/'qa/reports/review049_package_final132.json').read_text('utf-8'))
    assert previous['status']=='PASS'
    for f,h in previous['contents_sha256'].items():assert sha(old/f)==h
    prior_report=json.loads((old/'release_report.json').read_text('utf-8'))
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    assert sha(rom)==prior_report['target']['sha256']
    ssot=R/'workspace/translation/text_ja.csv';assert sha(ssot)==prior_report['translation_review']['CSV_sha256']
    inventory=json.loads((R/'workspace/translation/nonplay_inventory049_166.json').read_text('utf-8'))
    review=R/'workspace/review/nonplay049_20261007_167'
    review_manifest=json.loads((review/'artifact_manifest.json').read_text('utf-8'))
    for f,h in review_manifest['files'].items():assert sha(review/f)==h
    data={p.relative_to(old).as_posix():p.read_bytes()for p in old.rglob('*')if p.is_file()}
    latest=copy.deepcopy(prior_report)
    latest.update(name=NAME,date='2026-10-07',version='0.1.0-review049-docs168',status='DEVELOPMENT_REVIEW',
        artifact_policy='Private review for requesting user. Same049 ROM/patch/tools; current docs and review added.',actual_play_owner='user')
    latest['unperformed']=['user actual-play review','all branches','global corpus closure','outside7 candidate consumer/scope decisions',
        'all reset/state contexts and crossbuild compatibility','hardware','PCM listening','final wording/names/art decisions']
    latest['current049_state_reset']={'report':'qa/reports/state133_validation.json','sha256':sha(R/'qa/reports/state133_validation.json'),
        'scope':'One private226 state restore and one reset/reentry validated; not all contexts or crossbuild compatibility.'}
    latest['outside_candidates']=[{'id':i['id'],'state':i['state'],'decision':i['decision']}for i in inventory['outside_registered_candidates']]
    latest['global_corpus_closed']=False
    latest['known_visual_evidence_failure']={'work':163,'file':'frame_04410.png','different_pixels':7326,'whole_prefix_RGB_equality':False,'cause':'unresolved'}
    latest['previous_package_actual_apply']={'work':132,'checks':8,'final_ZIP_target_exact':True,'sha256':sha(R/'qa/reports/review049_package_final132.json')}
    latest['apply_verification']['scope']='Historical132 unchanged patch/helpers/tools. The new168 ZIP is tested separately after it is finalized.'
    latest['private_review']={'directory':'review','registered_units':54,'graphics':33,'outside_candidates':7,'reused_actual_images':21,'static_atlases':4,
        'ROM_free':True,'human_final_review':False,'source_manifest_sha256':sha(review/'artifact_manifest.json')}
    for f,scope in [('nonplay166_inventory.json','Static current049 source/CHR/pointer preservation only.'),
                    ('nonplay167_final.json','Private review data/embedded images/browser UI/ZIP only; no game runtime.'),
                    ('coverage151_validation.json','')]:
        p=R/'qa/reports'/f
        if not scope:continue
        assert p.is_file();latest['verification_reports'][p.stem]={'sha256':sha(p),'scope':scope}
    latest['status_scope']='Private packaging of unchanged049. Final168 ZIP apply recorded externally in qa/reports/nonplay168_final.json. No distribution or human approval.'
    data['release_report.json']=(json.dumps(latest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    notes='''# 타이니툰 어드벤처 2 — 검토용049 · 문서 갱신168

2026-10-07 사용자 검수를 위한 ROM 없는 개발 패키지다. ROM049·차분 패치·적용 도구는 기존132 검증본과 동일하며, 최신 원천 목록·지원 범위·검토 자료를 추가했다. 최종 공개 배포판이 아니다. 실제 플레이 검수는 사용자 담당이다.

생성형 타이틀·지도·매표소·게임오버, 등록45본문 초안, HUD·보너스·매표소·기차 간판·시간초과·다음라운드·시작·정지 문구를 포함한다.54원천은45초안과9기술/공유 항목이다. 전체 게임 번역률이나 일본어9문장 미번역을 뜻하지 않는다. 그림33문구와 고유명사·철자·생성형 그림의 최종 선택은 보류다.

일반 티켓 부족 안내는 ‘아쉽지만 / 티켓이 부족해!’다. 전용226/227 폰트를 사용하고 기존 공유196/197과macro 정의를 보존했다.049는 native clear 후 새 폰트를 선택한다.048의 clear 전 폰트 교체 결함은 채택하지 않았고 실패 자료를 보존했다.

기존049 검증: 정적3840 page/16 setup 계약·Expected Writes·독립 재빌드·IPS/Windows xdelta 적용, 조건을 명시한 부족/보유량/결제/출발/타이틀/대사 회귀가 있다. 작업133에서는049 전용226 폰트 상태복원과 한 번의 리셋 후 재입장을 검증했다. 모든 저장 상태·모든 리셋 조건·다른 빌드 저장상태 호환성을 검증한 것은 아니다. 이번168 작업은 게임을 실행하지 않는다.

알려진 한계:049 helper의 page당38cycles 추가로 idle 난수용 RAM22·CPU/일부 IRQ 값이 달라진다. 전체 CPU·게임 난수/입력 결과의 동일성을 주장하지 않는다.163의 frame04410.png는7326픽셀이 달랐고 원인은 미확정이다. 같은 구간 RAM/PPU/OAM/상태/매핑 일치를 전체 RGB 동일성으로 확대하지 않는다.

원본 CHR128뱅크/8192타일과 등록NT20개·별도 프린터12슬롯/5원천을 정적으로 조사했다. 등록 밖 후보7건(HOWTO, PAUSE, POW, 다른 CHR의PUSH START, RYO51, NT1C, 진단STAGE SELECT)은 보존·소비 미연결 상태다. 전역 원천 완결성·미사용 확정·최종 보존 승인으로 취급하지 않는다. 숨겨진 진단 UI를 활성화하지 않았다.

review/review.html은54원천·33그림·후보7건의 비플레이 검토 자료다.21게임 PNG는 기존자료 재사용(14역사빌드/7현재049)이며4원본CHR 아틀라스는 정적자료다. 실제 화면마다 빌드와seed/진단 조건을 적었다. 자료 생성이 새 플레이 검수나 사람 승인인 것은 아니다.

전체 플레이·다른 분기·실기·PCM 청음과 최종 문구/명칭/그림 결정은 남았다. 사용자검수안내.txt와 알려진한계.md를 참고한다. 원본 ROM/폰트파일/에뮬레이터를 포함하지 않는다. 도구와 글꼴의 라이선스는 tools/와licenses/에 보존했다. 네이버 카페 작업기는 전체 작업 완료 후 작성하며 외부 게시하지 않았다.
'''
    data['RELEASE_NOTES_KO.md']=notes.encode('utf-8')
    readme=f'''타이니툰 어드벤처 2 일본판 → 검토용 한글 개발049 (2026-10-07 문서 갱신)

1. ZIP을 모두 풀고 apply.cmd에 지원 원본 일본판 .nes를 드래그하거나 명령줄에서 실행합니다.
   apply.cmd "원본 일본판.nes" "새 결과049.nes"
2. 원본은 보존되고 기본 결과 이름에는 _KR이 붙습니다. 기존 결과 파일은 덮어쓰지 않습니다.
3. 패치 대상 원본:262160바이트 / SHA256 {latest['source']['sha256']}
4. 결과:499728바이트 / SHA256 {latest['target']['sha256']}
5. 다른 지역/수정본이나 기존 한글판에 덧씌우지 않습니다. ROM/에뮬레이터는 포함하지 않습니다.

이번 묶음의 ROM/패치/도구는 기존049와 동일합니다. xdelta 파일에20261006이 붙은 것은 검증한 차분 파일을 그대로 보존했기 때문입니다.
Windows 적용 도구는 원본/패치/도구/결과 해시를 확인합니다. 한글·공백 경로를 지원합니다.
실제 플레이는 사용자가 검수합니다. 새 파일 이름과 새로 시작한 게임으로 확인하고 다른 빌드 저장상태를 가져오지 않습니다.
사용자검수안내.txt, 알려진한계.md, RELEASE_NOTES_KO.md를 먼저 읽어 주세요.
문장·그림·범위 검토는 review/review.html에서 확인할 수 있습니다.
최종 공개 배포판이 아니며 전체 플레이·전역 원천·최종 문구/명칭/그림 검수가 남아 있습니다.
'''
    data['README_적용방법.txt']=readme.encode('utf-8')
    data['사용자검수안내.txt']='''현재049 사용자 플레이 검수 안내

검수 결과가 없는 항목을 자동 PASS로 처리하지 않습니다. 에뮬레이터 이름/버전, 적용 결과ROM SHA, 새게임/저장상태 여부, 진행 경로를 함께 기록해 주세요.

확인할 장면:
- 타이틀: 한글 철자·리본·숫자2·시작 입력과 법적 표시.
- 도입/놀이기구 안내: 말투·이름·줄바꿈·글자 잘림·출력 도중 다음 페이지 전환.
- HUD/지도/매표소/기차: 작은 글자 읽기·숫자·간판·공유 그림의 손상 여부.
- 성 입구: 일반 티켓 부족→보유량, 충분할 때 결제/출발, 금티켓 관련 분기. 기존 일부 QA는 초기 숫자seed였으므로 자연 플레이 결과를 구분합니다.
- 각 놀이기구와 보스/중간 안내/결과/게임오버/이어하기/엔딩·크레딧.
- 일시정지/재개/리셋/저장·복원 후 글꼴과 숫자 상태. 다른 빌드 저장상태 호환성은 미확인입니다.
- 실제 플레이 중 추가로 보인 일본어/영어 문구와 효과 그림. 후보 HOWTO/PAUSE/POW가 표시되면 장면과 입력을 기록합니다.

결과 기록 양식:
ROM SHA:
에뮬레이터/버전:
새게임 또는 저장/복원 조건:
장면/스테이지/진행 조건:
입력/재현 순서:
관측한 문구 또는 현상:
기대 결과:
스크린샷/세이브 파일 위치(가능하면):
판정: 미확인 / 통과 / 수정 필요

번역·이름·그림 수정은 문구ID 또는 보이는 문구와 수정안을 함께 적어 주세요. review/decisions_template.json은 빈 응답양식이며 승인 기록이 아닙니다. 완주하지 않은 기록을 전게임 완료로 표현하지 않습니다.
'''.encode('utf-8')
    data['알려진한계.md']='''# 현재049 지원 범위와 알려진 한계

실제 플레이는 사용자 담당이다. 현재49 검토본을 새 게임으로 시작한다. 원본과 결과의 정확한SHA는 release_report.json 및 적용안내를 따른다.

현재 확정된 결함으로 채택하지 않은 후보048은 보존하고049를 사용한다.049의 관측된 clear/font 전환은 수정되었지만 모든 분기/상태 검증은 아니다. 과거042/043/045/046/047 실제 화면과 현재049 화면은 검토자료에서 구분했다.

38cycles/page 추가에 따른 idle RNG/CPU/IRQ 차이, 작업163 한PNG7326픽셀 비교 실패/원인 미확정, 등록 밖7후보의 소비/범위 미확정, 전역 원천 폐쇄, 최종 말투·이름·그림 결정이 남는다. 정적조사·실제적용·제한된런타임·사람플레이는 별도의 검증이다.

작업133의 상태복원/리셋 재입장은 제한된049 환경에서 통과했다. 모든 상태/모든에뮬레이터/이전빌드 세이브호환/실기/PCM음질을 보장하지 않는다. 카트·수상 놀이기구 자동 플레이 실패와 씨드/진단 실행을 자연완주 증거로 표시하지 않는다.

네이버 카페 글과 공개 배포 확정은 전체작업 완료 후 진행한다. 이 묶음은 검토용이며 외부 게시/최종 승인이 아니다.
'''.encode('utf-8')
    for p in review.iterdir():
        if p.is_file():data['review/'+p.name]=p.read_bytes()
    data.pop('SHA256.txt')
    data['SHA256.txt']=(''.join(hashlib.sha256(b).hexdigest()+'  '+name+'\n'for name,b in sorted(data.items()))).encode('utf-8')
    assert not any(Path(f).suffix.lower()in['.nes','.rom','.bin','.ttf','.otf','.sav','.state']for f in data)
    out.mkdir()
    for f,b in data.items():
        p=out/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for f in sorted(data):z.write(out/f,(Path(NAME)/f).as_posix())
    with zipfile.ZipFile(archive)as z:
        assert z.testzip()is None and len(z.namelist())==len(data)
        for f,b in data.items():assert z.read(NAME+'/'+f)==b
    (archive.parent/(archive.name+'.sha256')).write_text(sha(archive)+'  '+archive.name+'\n','utf-8')
    result={'work':168,'status':'PASS_ROMFREE_PACKAGE_FINAL_APPLY_PENDING','archive':archive.relative_to(R).as_posix(),
        'archive_sha256':sha(archive),'files':len(data),'ROM_free':True,'current049_ROM_sha256':sha(rom),
        'CSV_sha256':sha(ssot),'unchanged_patch_helpers_tools_licenses':True,
        'contents_sha256':{f:sha(out/f)for f in sorted(data)},'actual_play_owner':'user','new_game_execution':False,
        'distribution_eligible':False,'human_approved':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:v for k,v in result.items()if k!='contents_sha256'},indent=2))

if __name__=='__main__':main()
