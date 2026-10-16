# 작업216 — 실제062 출력 진입점 NMI 검증·215 판단 정정

**작업215의 ‘등록11px 두 문단 NMI 초과’ 판단을 철회한다.** 그 측정은 patched925E→9690→B400 진입점이 아니라 남겨 둔 native fallback96FC를 직접 호출했다. [215 원래 조사](TEXT11_NMI_PREFIX_BUDGET_215.md)는 실패 이력으로 보존한다.063은 만들지 않았고062 바이트/패키지는 그대로다.

[216 실제 진입점 CPU 보고](../qa/reports/nmi216_actual_entry_budget.json)는925E의최종기계코드 `JMP $9690`와각등록본문에서B400 경로 진입/96FC 미방문을 확인한다. 초기 추적assert에925E의ROM파일offset2526E와16바이트헤더를 혼동한926E를 포함해 실패했으며 실제명령/주소로 정정 후 통과했다. 이 오류는ROM을수정하지않았다.

전체 즉시출력231조건+부분skip1071조건에nativeFE83→FECD prefix를 실행했다. OAM DMA513/514 포함,1D의렌더 유지/복원 두 조건과IRQ enable0/1 seed를 조합했다. 실제 출력 패킷은모두원래네임테이블 주소/값으로소비됐다. 노출 렌더복원 기준최대2229사이클로[NTSC 약2273](https://www.nesdev.org/wiki/The_frame_and_NMIs)보다44사이클 작다. packet은최대108바이트/92셀이다. 렌더 유지1D=2 경로까지 포함한CPU prefix 최대는2237이다. [DMA 자료](https://www.nesdev.org/wiki/PPU_registers).

원본/062 mapper는85(VRC7)다. 1편mapper값을2편에적용하지않았다. [mapper85](https://www.nesdev.org/wiki/INES_Mapper_085), [VRC IRQ 일반모델/실리콘구별 주의](https://www.nesdev.org/wiki/VRC_IRQ). 기존033의5놀이기구RAM1786개를읽고상단텍스트조건65개/5컨텍스트를묶었다.40=4·첫reload82를현재CPU prefix에seed한50조건에서는일반prescaler 모델상의첫IRQ가prefix보다늦다. 기존RAM은실제062실행증거가아니며VRC7실리콘의세부카운터차이를검증한것도아니다.

**한계:** 44사이클은nominal headroom이고안전마진승인이아니다. 명령경계NMI지연/PPU서브사이클·DMC steal·실제IRQ선·전체NMI tail·모든큐병합·현재062실제매핑/가독성은미검증이다. 사용자실제플레이검수는계속남는다. ‘시간초과0’은명명한CPU조건에한정된다. 마지막PPU쓰기와렌더복원시각은각컨텍스트에따로기록했다.

변경:216 조사/인계스크립트,CPU보고와README/HANDOFF/계획/날짜별인계/journal. 원본·CSV·051·062·055의검증자료·기존ZIP·사용자Mesen/세이브를보존했다. 새emulator/컨트롤러/플레이없음. 재현은기존결과를덮어쓰지않는새출력경로의복제에서행한다. 작업214의삭제예외PNG는재시도하지않았다.

다음 작업 하나: 062의 출력/mapper복귀 중 IRQ를 주입하는 한정 CPU 검증으로 큐·레지스터·뱅크 복귀의 조합을 검사한다.
