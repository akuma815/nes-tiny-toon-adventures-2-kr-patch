"""Freeze scoped IRQ evidence and update canonical handoff."""
from pathlib import Path
import json,re
import seal_nonplay171 as records
from seal_nonplay171 import R
records.DATE='2026-10-09'
report=R/'qa/reports/irq217_injection.json'
q=json.loads(report.read_text('utf-8'))
assert q['IRQ_injections']==62940 and q['full_producer_continuations']==66
next_action='오프닝9개와 크레딧3개의 출력 경로에서 IRQ 마스크와 복귀 상태를 한정 CPU 모델로 확인한다.'
body='''062의 일반 대사33개에 티켓999·놀이기구5를 넣고 즉시출력925E와 첫 글자출력93E1의66상태를 검사했다. 각 PC의 첫/마지막 방문 명령 경계에서 원래 IRQ 벡터FA5B를 주입했다. 콜백은 mode0/phase0, mode1/phase0·1, mode4/phase0·1의5경로다. 총62,940주입에서 PC·A·X·Y·SP·P와 PRG 은행은 IRQ 전후 같았고192바이트 출력 버퍼는 보존됐다. 최저 SP239로 이 버퍼 뒤47바이트의 범위 여유가 있었다. 이는 CPU 스택 검사 결과이며 화면/타이밍 안전성을 뜻하지 않는다.

각66상태에서 PRG 은행을 전환한 중간에 IRQ를 넣은 뒤 끝까지 출력해 원래 결과와 큐·본문 상태·글꼴 래치·레지스터·PRG 복귀를 비교했다. native IRQ가 사용하는41/45/46/47/C7은 별도 허용하고 출력 루틴이 이 주소들을 읽지 않음을 확인했다. IRQ가 C6를6F3에서 되돌리는 경로도 검사했고 C6의 예상치 못한 변경은 허용하지 않았다. 실제 스택이 사용하는 슬롯만 IRQ 전후 RAM 비교에서 제외했으며 큐 영역은 별도로 전체 비교했다.

051과062의 고정 IRQ 코드FA5B~FD18이 바이트 동일했고, 각 상태의 중간 은행 전환 위치에서5콜백의 CPU 사이클/레지스터복귀/하드웨어쓰기 결과가 동일했다. IRQ 사이클은82/430/414/415/229이다. 이는 해당 경계에 주입했을 때의 코드 동작 증거이며 실제 VRC7 IRQ 발생 시각이나 현재 플레이에서 그 콜백이 실행되는 조건을 증명하지 않는다.

정적·CPU: 위 범위 PASS. 새 빌드/패치 적용: 수행하지 않음,062·IPS·ZIP 변경 없음. 새 에뮬레이터/장면/플레이: 미수행, 사용자 담당. 오프닝·크레딧, 모든 루프 반복/본문 커서, 비동기 NMI와 겹침, DMC, PPU/실제 CHR 매핑은 이 검사 밖이다.062는 미채택 개발 후보다. [216 NMI 정정](TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md)의 명목44사이클 여유에 IRQ 시간이 자동으로 더해지는 것으로 해석하지 않는다.

변경 파일: audit_irq217.py, seal_irq217.py, [CPU 보고](../qa/reports/irq217_injection.json), 본 인계와 날짜별 인계/SURVEY/계획/journal/README. SHA는 [217 매니페스트](../manifests/nonplay217_assets.json)에 원본·CSV·051·062·IPS·ZIP까지 기록한다. 과거215/216 보고/문서는 보존한다. 이번 보조 조회에서 PowerShell python-c 인용과 rg wildcard 경로가 실패했지만 디스크 파일을 바꾸지 않았고 파일 스크립트/직접 읽기로 교정했다.

재현: python -B scripts/audit_irq217.py. 고정 보고가 이미 있으면 덮어쓰기 방지 assert가 있으므로 새 보고 경로의 스크립트 복제에서 재현한다. py651.2.0 NMOS6502 모델을 사용한다. 공개 작업기에는 CPU 모델 검사로만 소개하고 실제 플레이 통과로 표기하지 않는다.'''
assets=[Path(__file__),R/'scripts/audit_irq217.py',report,
 R/'manifests/nonplay216_assets.json',
 R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes',
 R/'workspace/translation/text_ja.csv',
 R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes',
 R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes',
 R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.ips',
 R/'dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip']
records.seal(217,'TEXT11_IRQ_INJECTION_217.md','일반 대사33개 IRQ 경계 주입·복귀 CPU 검증',body,
 '66출력 상태·62,940 IRQ 주입 PASS, 중간 은행66회 출력 완료 동일.051과 콜백 동일.062 불변·실제 검수 남음.',next_action,assets)
f=R/'docs/LOCALIZATION_WORK_PLAN.md';s=f.read_text('utf-8');s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 작업217 / 기준051·062 미채택 / 일반 대사 IRQ CPU 검사 PASS. 실제 플레이 사용자 담당.**',s,count=1);f.write_text(s,'utf-8')
print('217 handoff sealed')
