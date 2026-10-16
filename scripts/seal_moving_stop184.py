"""Final frozen-asset preservation and051 handoff audit."""
from pathlib import Path
import json,re
from seal_nonplay171 import R,sha,seal

def main():
    out=R/'qa/reports/moving_stop184_preservation.json';assert not out.exists()
    checks=[]
    for work in (177,178,179,180,181,182,183):
        p=R/f'manifests/nonplay{work}_assets.json'
        data=json.loads(p.read_text('utf-8'))
        for name,digest in data['files'].items():assert sha(R/name)==digest,(work,name)
        checks.append({'work':work,'files':len(data['files']),'manifest_sha256':sha(p)})
    source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
    current=R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes';package=json.loads((R/'qa/reports/moving_stop183_package.json').read_text('utf-8'))
    assert sha(current)==package['ROM_sha256'] and sha(R/package['archive'])==package['archive_sha256']
    put={'work':184,'status':'PASS_FROZEN177_TO183_AND_ADOPTED051','prior_and_new_frozen_manifests':checks,'source_sha256':sha(R/source['path']),'adopted_ROM_sha256':sha(current),'archive_sha256':package['archive_sha256'],'user_applied050_preserved':True,'scope':'Declared frozen assets from177..183 only; source and game1 refs additionally checked by audits181..183. No new runtime/fullplay or final human approval.'}
    provenance=json.loads((R/'qa/issue181_user_stop/provenance.json').read_text('utf-8'));assert sha(Path(provenance['ROM_recent_path']))==provenance['ROM_sha256']
    out.write_text(json.dumps(put,ensure_ascii=False,indent=2)+'\n','utf-8')
    audits=[R/f'qa/reports/moving_stop184_audit{n}.json' for n in (181,182,183)]
    body=f'''[保全報告](../qa/reports/moving_stop184_preservation.json)で作業177..183の既存/新規固定資産をSHA検査した。原本·1편참고자료·사용자적용050 ROM 보존.현재051 SHA `{sha(current)}`,ZIP SHA `{package['archive_sha256']}`. 변경파일은본스크립트·보고·인계이며ROM/패치/CSV/QA화면은바꾸지않았다.

[181 감사](../qa/reports/moving_stop184_audit181.json)8617파일/[182 감사](../qa/reports/moving_stop184_audit182.json)4584파일/[183 감사](../qa/reports/moving_stop184_audit183.json)27파일 PASS. 각선언자산/원본/1편해시와프로젝트로컬문서링크2438개확인. 역사문서CASTLE_CURRENCY_QA의외부3.3스킬캐시링크1개는만료된기존환경참조로보고하며고정역사문서를고치거나모든외부링크정상을주장하지않는다. 현재3.4스킬의존재/SHA도보고에기록했다.

작업181의별도움직이는STOP 소비진단/오관측보존,182의글자수정·동일입력/독립재빌드,183의실Windows8+최종ZIP적용/ROM-free 결과를구분해현재README/HANDOFF/계획에051과최신적용묶음을연결했다. 사용자‘모든놀이기구HUD가같다’는관측도보존했다. 새전체게임플레이/직접사용자Mesen접속/최종사람승인/카페완성작업기/외부게시없음.

재검사: `python scripts/audit_project_links184.py --manifest manifests/nonplay183_assets.json --output qa/reports/NEW_AUDIT051.json`. 출력은새경로를쓴다. 본스크립트는최종인계덮어쓰기방지로현재경로재실행하지않는다. 다음검수는새051을초기화하여기차의고정정지뒤위아래로움직이는표지판을확인한다.'''
    # Use Korean for the public-facing handoff; no source artifacts are changed.
    body=body.replace('[保全報告]','[보존보고]').replace('で作業177..183の既存/新規固定資産をSHA検査した。','에서작업177..183의기존/새고정자산을SHA검사했다.')
    next_action='사용자가 새051 ROM을 열고 초기화/기차 재진입 후 위아래로 움직이는 정지 표지판을 검수한다.'
    seal(184,'MOVING_STOP051_FINAL_HANDOFF_AUDIT_184.md','051 최종인계·이전자산 보존 감사',body,'177..183고정자산해시/원본·1편/로컬링크 PASS.사용자적용050 보존,현재051+ROM-free ZIP183 인계.새플레이검수는사용자담당.',next_action,[Path(__file__),R/'scripts/audit_project_links184.py',out,*audits])
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업184','현재 개발051 / 작업184',1);p.write_text(s,'utf-8')
    p=R/'README.md';s=p.read_text('utf-8').replace('작업183 완료 / 움직이는','작업184 완료 / 움직이는',1).replace('현재 개발본 — 작업183 / 051','현재 개발본 — 작업184 / 051',1);p.write_text(s,'utf-8')
    print(json.dumps(put,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
