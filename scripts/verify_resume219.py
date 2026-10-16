"""Final resumed-session closure; frozen hashes independent of old handoff headers."""
import ast,json,re
from pathlib import Path
from seal_nonplay171 import R,sha

def main():
    count=0
    for work in range(215,220):
        q=json.loads((R/f'manifests/nonplay{work}_assets.json').read_text('utf-8'))
        for rel,digest in q['files'].items():
            assert (R/rel).is_file() and sha(R/rel)==digest,(work,rel)
            count+=1
    # Use the exact sealed identity constants, without invoking its stale
    # assertion that the mutable canonical handoff must still name work218.
    tree=ast.parse((R/'scripts/seal_irq218.py').read_text('utf-8'))
    assignments=[n for n in ast.walk(tree) if isinstance(n,ast.Assign)
                 and any(isinstance(t,ast.Name) and t.id=='identities' for t in n.targets)]
    assert len(assignments)==1
    identities=ast.literal_eval(assignments[0].value)
    for rel,digest in identities.items():assert sha(R/rel)==digest,rel
    for work,name in [(216,'TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md'),
                      (217,'TEXT11_IRQ_INJECTION_217.md'),(218,'TEXT11_OPENING_CREDITS_IRQ_218.md'),
                      (219,'TEXT11_IRQ_STACK_GAP_CORRECTION_219.md')]:
        f=R/'docs'/name
        for dest in re.findall(r'\]\(([^)]+)\)',f.read_text('utf-8')):
            if dest.startswith(('https://','http://')):continue
            assert (f.parent/dest.split('#')[0]).resolve().exists(),(work,dest)
    hand=(R/'docs/HANDOFF.md').read_text('utf-8')
    assert '작업219 완료' in hand.splitlines()[0]
    for marker in ('062','063','사용자','48/49'):assert marker in hand,marker
    result={'work':219,'status':'PASS_FROZEN_215_219_AND_UNCHANGED_ARTIFACTS',
            'manifest_file_checks':count,'source_CSV_051_062_IPS_ZIP_identity_checks':len(identities),
            'new_handoff_links_exist':True,
            'tooling_correction':'seal_irq218.py --verify passed at218. After219 it rejects its stale required current218 header; its preceding hash/link checks pass. Use verify_resume219.py now.',
            'validation_scope':'Static hashes, CPU reports and handoff consistency; no new emulator/play/build/apply.'}
    out=R/'qa/reports/resume219_final_verification.json'
    if out.exists():assert json.loads(out.read_text('utf-8'))==result
    else:out.write_text(json.dumps(result,indent=2)+'\n','utf-8')
    doc=R/'docs/TEXT11_RESUME219_FINAL_VERIFICATION.md'
    note='''# 作業219追加検証

'''
    note='''# 작업219 추가 검증·재현 명령 정정

`python -B scripts/verify_resume219.py`로215~219 봉인45파일, 원본/CSV/051/062/IPS/ZIP6파일, 신규 인계 링크와 현재219 인계를 확인했다. 모두 통과했다. [최종 보고](../qa/reports/resume219_final_verification.json).

218의`seal_irq218.py --verify`는218 당시 통과했으나219 인계 후 다시 실행하면 현재 헤더를218로 고정한 마지막 assert에서 실패한다. 파일 해시나 링크가 바뀐 실패는 아니다. 봉인218 스크립트를 보존하고 위 최신 검사기를 추가했다. [219 수치 정정 문서](TEXT11_IRQ_STACK_GAP_CORRECTION_219.md)의 이전 재현 명령보다 이 추가 문서의 명령을 사용한다. 검사기/보고/문서 SHA는 [추가 봉인](../manifests/nonplay219_resume_verification_assets.json)에 있다.

062는 수정하지 않은11px 개발후보다. 모델의 한정 NMI/IRQ 검사만 통과했고 실제 화면 검수는 사용자 담당이다. 다음 작업 하나: 사용자062 재현 장면 하나의 결과를 받아 조사한다.
'''
    if doc.exists():assert doc.read_text('utf-8')==note
    else:doc.write_text(note,'utf-8')
    manifest=R/'manifests/nonplay219_resume_verification_assets.json'
    payload={'work':219,'files':{p.relative_to(R).as_posix():sha(p) for p in [Path(__file__),out,doc]}}
    if manifest.exists():assert json.loads(manifest.read_text('utf-8'))==payload
    else:manifest.write_text(json.dumps(payload,indent=2)+'\n','utf-8')
    for p in [R/'docs/HANDOFF.md',R/'docs/HANDOFF_2026-10-09.md',R/'docs/journal/2026-10-09.md']:
        text=p.read_text('utf-8');link='../TEXT11_RESUME219_FINAL_VERIFICATION.md' if p.parent.name=='journal' else 'TEXT11_RESUME219_FINAL_VERIFICATION.md'
        entry=f'\n\n작업219 추가 검증: 이전218 검사기의 현재 인계 헤더 고정 조건은219 이후 맞지 않아 최신 `python -B scripts/verify_resume219.py`를 사용한다. 봉인45파일·핵심6파일·신규링크 PASS. [명령 정정과 최종 근거]({link}).\n'
        if entry not in text:p.write_text(text+entry,'utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
