"""Freeze opening/credits CPU evidence; verify resumed-work immutable artifacts."""
from pathlib import Path
import json,re,sys
import seal_nonplay171 as records
from seal_nonplay171 import R,sha
records.DATE='2026-10-09'
NAME='TEXT11_OPENING_CREDITS_IRQ_218.md'

def verify():
    count=0
    for work in (215,216,217,218):
        p=R/f'manifests/nonplay{work}_assets.json'
        q=json.loads(p.read_text('utf-8'))
        for rel,digest in q['files'].items():
            f=R/rel;assert f.is_file() and sha(f)==digest,(work,rel)
            count+=1
    identities={
      'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d',
      'workspace/translation/text_ja.csv':'43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f',
      'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes':'b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24',
      'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes':'7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce',
      'build/text11_candidate_062/TinyToon2_Text11_Candidate062.ips':'13023b6eb6b4a4bf61f112f8d3fa2b90f4543307931c361eec3de05bc2762b8d',
      'dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip':'377b16522c31f3516869c9eb14acb925799ceeefa1051d06508570770bc19575'}
    for rel,digest in identities.items():assert sha(R/rel)==digest,rel
    for f in [R/'docs'/NAME,R/'docs/TEXT11_IRQ_INJECTION_217.md',R/'docs/TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md']:
        for dest in re.findall(r'\]\(([^)]+)\)',f.read_text('utf-8')):
            if dest.startswith(('https://','http://')):continue
            assert (f.parent/dest.split('#')[0]).resolve().exists(),(f.name,dest)
    hand=(R/'docs/HANDOFF.md').read_text('utf-8')
    assert '작업218 완료' in hand.splitlines()[0] and '062' in hand and '063' in hand
    print(json.dumps({'status':'PASS_FROZEN_215_218_AND_UNCHANGED_SOURCE_CSV_051_062_IPS_ZIP',
                      'manifest_file_checks':count,'identity_checks':len(identities),'new_doc_links_exist':True}))

def main():
    if '--verify' in sys.argv:verify();return
    report=R/'qa/reports/irq218_opening_credits.json';q=json.loads(report.read_text('utf-8'))
    assert q['typed_calls']==852 and q['IRQ_injections']==149824
    next_action='ユーザーの062実画面検査結果を受け、再現箇所を一つに絞って修正する。'
    next_action='사용자의062 실제 화면 검수 결과를 받아 첫 재현 장면 하나의 출력·소거·글꼴 매핑을 조사한다.'
    body='''오프닝9개와 진행 크레딧2개의852출력 호출에 원래 IRQ 벡터FA5B를 주입했다. 모든 본문 커서에서 mode0의 종료/ack 콜백을, 첫 호출과 출력 없는 개행·종료 호출에서는5종 콜백을 검사했다. 각 호출의 PC 첫/마지막 방문 경계가 대상이다. 첫 크레딧 A448→A44B 직접출력에서도 mode0만 검사했다. 총149,824주입에서 CPU 레지스터·PRG·큐·본문 상태·C6 래치 복귀를 통과했고 최저 SP240이었다. 이 기준의192바이트 큐 뒤 범위 여유는48바이트다. [218 CPU 보고](../qa/reports/irq218_opening_credits.json).

기준 출력 결과는 오프닝9와 크레딧2의 NT 좌표/타일에 정확히 일치했다. 첫 크레딧 기준 출력756셀·렌더중지·2000 복원도211의native경로와 같았다. 이 기준 출력은 IRQ를 PPU 모델에 섞어 실행한 결과가 아니다. 첫 크레딧의 mode0 콜백은 IRQ acknowledge/disable만 수행하므로 RAM·레지스터·PRG 보존만 검사했고, PPU/CHR를 바꾸는 다른 콜백은 직접출력 도중 주입하지 않았다. 실제 초기 크레딧의 IRQ enable/context와 발생시각은 아직 증명하지 않았다.

[217 일반33대사](TEXT11_IRQ_INJECTION_217.md)의62,940주입과 함께 이번 재개에서 총212,764 한정 IRQ 주입을 수행했다. 서로 다른 콜백·커서 표본 방식이므로 ‘전게임 모든 인터럽트 조합 통과’로 표현하지 않는다. [216 NMI 실제진입점 정정](TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md)의231전체/1071부분 출력 조건은CPU prefix시간초과0이나명목여유44사이클이다.215의잘못된 fallback 직접호출 초과판단은철회했으며실패원문은유지했다.063이나새패치는만들지않았다.

변경: audit_irq218.py, seal_irq218.py,218CPU보고,본인계,날짜별인계/SURVEY/계획/journal/README/HANDOFF. 원본·번역CSV·051·062·IPS·기존ZIP·과거보고·사용자Mesen/세이브는변경없다. [218 매니페스트](../manifests/nonplay218_assets.json)와 verify 명령으로215~218 봉인 해시/핵심6파일 동일/신규인계 링크를 확인한다.

재현: python -B scripts/audit_irq218.py (고정 보고 덮어쓰기 방지,새출력경로 복제에서 재현). 봉인 검증: python -B scripts/seal_irq218.py --verify. 원본 검증: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1. py651.2.0 모델. 정적·CPU 검사만 수행했으며 이번 작업에서새빌드/적용/에뮬레이터/화면/플레이검사는하지않았다. 기존211/212 빌드·적용결과는기존근거의해당범위만유지한다.

남은 판정:062 실제폰트/줄바꿈·출력중건너뛰기·티켓교환후대사·상단창소거/전환·놀이기구/크레딧가독성·CHR256 실제매핑. 전체NMI tail·실제 VRC7 IRQ 타이밍·DMC·PPU와의상호작용은미증명이고이번CPU표본검사로안전승인하지않는다. 사용자가실제플레이검수를담당하므로새자동플레이는실행하지않는다.062는미채택개발후보이며완성작업기/외부게시도진행하지않았다. 검수에서는새062 ROM으로초기화하고이전세이브스테이트호환은기대하지않는다.'''
    files=[Path(__file__),R/'scripts/audit_irq218.py',report,R/'manifests/nonplay217_assets.json',
           R/'build/text11_candidate_062/opening11_plan.json',R/'build/text11_candidate_062/credits11_plan.json']
    records.seal(218,NAME,'오프닝·크레딧 IRQ CPU 검증과 재개 인계',body,
      '852출력 호출·149,824 한정IRQ 주입 PASS. 재개 총212,764주입.062/패키지 불변·실제 검수 대기.',next_action,files)
    f=R/'docs/HANDOFF.md';s=f.read_text('utf-8');lines=s.splitlines()
    lines.insert(2,'**작업218 재개 검증:** 실제 진입점 NMI prefix와 일반대사·오프닝·크레딧의 한정 IRQ CPU 검사를 마쳤다. 원본/CSV/051/062/IPS/ZIP은 불변이며062는 실제 검수 전 개발 후보다. [검증 범위·남은 실제 확인](TEXT11_OPENING_CREDITS_IRQ_218.md).')
    f.write_text('\n'.join(lines)+'\n','utf-8')
    f=R/'docs/LOCALIZATION_WORK_PLAN.md';s=f.read_text('utf-8');s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 작업218 / 기준051·062 미채택 / 한정 NMI·IRQ CPU 검사 완료. 실제 플레이 사용자 담당.**',s,count=1);f.write_text(s,'utf-8')
    f=R/'README.md';f.write_text('> **작업218:** 062의 한정 NMI·IRQ CPU 검증 추가, ROM/IPS/ZIP 불변. 실제 화면 검수는 사용자 담당. [최신 인계](docs/TEXT11_OPENING_CREDITS_IRQ_218.md)\n\n'+f.read_text('utf-8'),'utf-8')
    verify()

if __name__=='__main__':main()
