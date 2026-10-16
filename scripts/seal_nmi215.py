"""Record the new conditional NMI-budget defect before attempting a new candidate."""
import json,re
from pathlib import Path
import seal_nonplay171 as records
from seal_nonplay171 import R
records.DATE='2026-10-09'
p=R/'qa/reports/nmi215_transfer_budget.json';q=json.loads(p.read_text('utf-8'))
next_action='별도063에서 기존 native opcode4의 언롤 VRAM 전송을 즉시출력 큐에 적용하고, 모든 기존 문단/skip/큐/CPU 및 NMI prefix를 비교한다.'
body='''062의 실제 패킷을 원본과 같은 D068 VRAM 소비기에 넣고 NMI FE83→FECD까지 최종6502 명령을 실행했다. [CPU 측정](../qa/reports/nmi215_transfer_budget.json). NMI 진입7사이클과 OAM DMA513/514를 포함한231개 일반 즉시출력 입력×8조건, 크레딧327호출×8조건, 두 타일 출력×8조건이다. queue주소/값/초기화와 stack소비는 CPU 모델에서 일치했다. DMA 길이는 두 끝값으로 측정했으며 실제 시작 parity를 모델링한 실행은 아니다.

NTSC 약2273사이클의 갱신 구간은 [NESdev frame/NMI](https://www.nesdev.org/wiki/The_frame_and_NMIs), DMA513/514는 [PPU registers](https://www.nesdev.org/wiki/PPU_registers)에서 확인했다. 두 원천 MAIN_05849(1E)·MAIN_05882(20)의 전체 즉시출력은 렌더 복원 조건1D=0에서 이 값보다 늦다. 최악 MAIN_05882는2317~2319사이클, 두타일 점진출력955~957, 크레딧 최대1631~1633이다. 최악값의 경계초과는 약46사이클이다. 1D=2에서는 렌더가 계속 꺼져 있으므로 같은 시각을 visible corruption으로 해석하지 않는다.

이는 **조건부 CPU 전송예산 결함**이며 실제 사용자 조작에서1D/IRQ가 같은지, 실제 화면 손상이 생겼는지는 미확인이다. IRQ/DMC/명령경계 지연은 제외되어 안전 마진 주장도 하지 않는다. NMI 전체/음악/게임 갱신 tail, 부분skip와 다른큐 동시발행은 별도다. 기존211의 큐 바이트/동기CPU 통과는 VBlank 시점 검증이 아니었다. 원본2편과 최종062의 D068/F9E6/FE83 소비기 범위는 동일하다.

조사 중 inline disassembly 명령은 PowerShell 인용 오류로 실행되지 않아 별도 dump_transfer215.py로 정상 덤프했다. ROM/CSV/폰트/051/062/기존ZIP/사용자Mesen/세이브를 변경하지 않았다. 새 에뮬레이터·컨트롤러/플레이 실행은 없다. 작업214의 검증사본 삭제 정책차단도 재시도하지 않았다.

원래 소비기는 opcode4에서 큐에 담긴RTS 주소를 사용해 D0BC..D138의32타일 언롤 루틴 일부를 실행할 수 있다. 폰트/문장/좌표/최종값을 유지하고 즉시출력의 각 행을 이 기존 전송 형태로 바꾸는 별도063을 검증한다. 이 계획은 코드 변경 전 가설이며 현재062의 실제 검수/채택은 보류된다.'''
records.seal(215,'TEXT11_NMI_PREFIX_BUDGET_215.md','062 즉시출력 두 문단의 조건부 NMI 전송예산 초과',body,
 '062 CPU prefix에서1E/20 즉시출력 NTSC 기준초과(최대2319). 실제 화면/IRQ/DMC 미검증.062 보존,별도063 native언롤 큐 개선 준비.',next_action,
 [Path(__file__),R/'scripts/audit_nmi215.py',R/'scripts/inspect_nmi215.py',R/'scripts/dump_transfer215.py',p,
  R/'work/nmi215/fixed_F800_FFFF.txt',R/'work/nmi215/native_transfer_and_prerequisites.txt'])
for n in ('HANDOFF.md','LOCALIZATION_WORK_PLAN.md'):
 f=R/'docs'/n;s=f.read_text('utf-8')
 if n=='HANDOFF.md':
  header,tail=s.split('\n',1);s=header+'\n\n**작업215 새 조사:** 062 즉시출력1E/20은 조건부 CPU NMI 예산을 넘는다. 실제 손상은 미관측이며062는 미채택이다. [측정·한계](TEXT11_NMI_PREFIX_BUDGET_215.md). 별도063에서 기존 native 언롤 전송을 검증한다.\n'+tail
 else:s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 작업215 / 기준051·062 미채택 / 즉시출력2문단 조건부 NMI 예산 초과·063 개선 조사. 실제 플레이 사용자 담당.**',s,count=1)
 f.write_text(s,'utf-8')
print('215 handoff sealed')
