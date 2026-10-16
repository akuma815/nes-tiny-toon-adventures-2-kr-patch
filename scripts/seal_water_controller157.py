from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/water157_assets.json';doc=R/'docs/WATER_ADAPTIVE_ACTOR_AVOIDANCE.md';assert not m.exists()and not doc.exists()
 v=json.loads((R/'qa/reports/water157_controller_validation.json').read_text('utf-8'))
 assert v['frames']==9000 and v['actor_damage_events']==0 and not v['natural_clear_observed']
 nxt='157과 같은 입력으로 native 화면하단 이탈 코드·4016 읽기/쓰기·RAM52 소비를 직접 관측하고, 카메라 축 이름을 원본 소비 코드로 정정한다.'
 doc.write_text(f'''# 작업157 — 급류 후반 장애물 회피와 실패 경계

[검증](../qa/reports/water157_controller_validation.json), [36쌍 CPU 모델](../qa/reports/water157_bbox_model.json), [계획/재현 명령](../work/water157/run_plan.json), [입력 전수 기록](../qa/dialogue/water157_controller049/adaptive_inputs.csv), [v1 준비 오류](../qa/reports/water157_v1_preflight_error.json), [입력 시점 가정 오류](../qa/reports/water157_input_phase_assumption_error.json).

native 충돌상자 계산은 원본/049 36쌍 CPU 결과로 한정 검증했다. 이후 일정 속도의 미래 겹침 예측은 컨트롤러 가설이다. 고정156 입력을 3300까지 유지하고 이후 실제 컨트롤러만 조작했다. 메모리·ROM·저장상태 개입은 없다. 이전156의 1794개 스냅샷 자료가 같다. 8999회 최종 입력 요청과 native A 점프 2800/2890/3499/3607/3835를 관측했다. 객체 피해 0, 마지막 플레이 기록4023까지 체력3을 유지했으나 root8로 끝났고 자연 clear는 없다. 화면하단 이탈 원인은 다음 실제 코드 관측으로 검증한다.

RAM52와 이전 프레임 라벨 요청의 비교는1237 일치/8 불일치다. 이전 라벨이 항상 실제 입력이라는 가정을 폐기했고 입력 요청과 native 소비 시점의 완전한 대응은 미검증으로 남긴다. 실패한 v1 검증·준비 스크립트와 보고는 보존했다. 역사 CSV의 vertical_hi/lo는 RAM69/6D이며 축 이름 오류를 다음 작업에서 코드와 대조해 정정한다. 이번 시각 검토는 frame03990 실제 급류/HUD와 frame04050 전환 검은 화면 두 PNG에 한정하며 성공 장면 근거가 아니다.

변경 파일: prepare_water_controller157.py/v2.py, trace_water_controller157.lua, verify_water_controller157.py/v2.py, seal_water_controller157.py, work/water157, qa/dialogue/water157_controller049, qa/reports/water157_* 및 이 상세문서·날짜별인계·journal·README/SURVEY/PLAN/HANDOFF·manifest/audit. 원본/1편/기존실패 보존. ROM SHA `{v['ROM_sha256']}`, CSV SHA `{v['CSV_sha256']}` 불변. 각 산출물 SHA는 scoped manifest에 기록한다.

정적/CPU/실행/입력요청 기록 검증 PASS(각 한정범위). 자연완주와 요청-소비 타이밍 증명은 FAIL/미완료. 새 빌드/적용·reset/state·청음/실기·사람 최종 검토는 미수행. 전체corpus/HOWTO/PAUSE/POW/자연 전체게임/정식배포 미완료. 카페 원고·게시 없음. 재현은 계획의 명령에 새 QA 경로를 사용하고 동결 검증 스크립트의 출력도 새 이름으로 복제한다.

다음 작업 하나: {nxt}
''','utf-8')
 entry='\n\n## 작업157 — 급류 후반 객체 회피/미완주\n\n36CPU쌍/8999입력요청/추가3점프/피해0·체력3.4023 이후 경로 종료로 자연clear 실패. 입력시점8불일치와 카메라축 오류를 별도 미해결로 보존. ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER_ADAPTIVE_ACTOR_AVOIDANCE.md).\n\n다음 작업 하나: '+nxt+'\n'
 for name in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/name;s=p.read_text('utf-8')
  if name=='LOCALIZATION_WORK_PLAN.md':s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-07 현재개발049 / 작업157 완료.**',s,count=1)
  p.write_text(s+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text(p.read_text('utf-8')+entry.replace('(WATER_ADAPTIVE_ACTOR_AVOIDANCE.md)','(../WATER_ADAPTIVE_ACTOR_AVOIDANCE.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[급류 후반 회피157](docs/WATER_ADAPTIVE_ACTOR_AVOIDANCE.md): 객체 피해0, 자연clear 실패 및 입력시점 미해결.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업156 완료','작업157 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,Path(__file__),R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'scripts/run_menu_qa.py',R/'scripts/trace_water_damage154.lua',R/'config/water_first_hazard_steer156.json']
 for pat in ['scripts/*157*','qa/reports/water157_*','work/water157/*','qa/dialogue/water157_controller049/*']:files.extend(R.glob(pat))
 m.write_text(json.dumps({'work':157,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('SEALED157')
if __name__=='__main__':main()
