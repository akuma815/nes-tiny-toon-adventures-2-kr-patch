from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/water154_assets.json';assert not m.exists()
 p=R/'qa/reports/water154_damage_validation_v2.json';v=json.loads(p.read_text('utf-8'))
 nxt='첫 native 장애물 충돌2910보다20프레임 앞선2890에 A8프레임만 추가한3300프레임 경로로 실제회피·체력·통나무재착지를 확인한다. RAM/ROM/좌표/시간조작없음.'
 detail=f'''# 작업154 — 급류 실제 피해 소비와 회피 모델

[최종검증v2](../qa/reports/water154_damage_validation_v2.json), [관측계획](../work/water154/run_plan.json), [관측준비](../scripts/prepare_water_damage154.py), [검증v2](../scripts/verify_water_damage154_v2.py), [모델시간 정정](../qa/reports/water154_model_cycle_correction.json).

현재049의153과동일컨트롤러입력으로4200프레임을실행했다. state0430=6과health07C0변경전에실제PC/물리PRG/직전3byte/전체RAM/register/mapper/caller/플레이어와통나무좌표를읽기전용기록했다.153과1812개동일시점snapshot산출물이exact이므로관측추가가게임값을바꾸지않았다. 6변경이source/current단일명령CPU와동일RAM출력에연결된다.

세충돌frame라벨2910/3511/3867은모두fixedE6B5→E6E4 STA0430이며actor슬롯15/15/12, type44hex/art6Chex다. supportC1=1에서맞았으므로물에빠짐이나급류지형A8E2피해로설명하지않는다.다음riverAC95 DEC07C0에서3→2→1→0을기록했다. nativeID/그림명은type44/art6C값에한정하며POW나정식장애물이름으로추정하지않는다.

각실제actor상태를CPU모델E6B5전체에재생했다.원본/current 24쌍(3충돌×Y상승0/8/16/24/32/40/48/56픽셀)은각각같은전체RAM/register결과다.0상승은모두충돌,8이상은해당순간충돌없음이다. 이는오프라인좌표fixture로서runtime좌표쓰기나자연점프전체궤적검증이아니다.다음에는관측2910앞의2890 A8프레임만추가해회피·재착지를확인한다.

v1 CPU출력에서핀한py65-1.2.0의DEC absolute(CE) cycle항목이3임을발견했다. [공식1.2.0 소스](https://github.com/mnaberez/py65/blob/1.2.0/py65/devices/mpu6502.py)의항목과로컬1133행이같고, [Visual6502 실측명령목록](https://www.nesdev.org/wiki/Visual6502wiki/6502_all_256_Opcodes)의해당명령은6cycles다. v2 CPU인스턴스의table복사본에서CE만6으로교정했다. 동결라이브러리/ROM/실Mesen추적은변경하지않았다. 단일STA는4/DEC는6 nominalCPU모델cycles이고실IRQ/DMC포함값과동일하다고하지않는다. v1보고/코드/정정원장은보존했다. 기존동결CPU시간추정치는해당핀모델에귀속하며새모델로자동재승인하지않는다.

변경: prepare_water_damage154.py,trace_water_damage154.lua,verify_water_damage154.py/v2,seal_water_damage154.py,새QA·계획·v1/v2/정정보고서,상세·인계/journal·canonical·manifest/audit. ROM SHA `{v['ROM_sha256']}`,CSV SHA `{v['CSV_sha256']}`불변. 원본/1편/실패153·역사자료보존. 재현은계획명령의새QA경로와최종v2검증기복제로수행한다. 정적/환경SHA/읽기전용runtime/1812snapshot동일·6명령·24geometry CPU쌍 PASS. 새직접PNG검토없음(153의4PNG근거유지),새build/apply/reset/state/청음/실기/사람최종없음. 자연clear·전역corpus·소비후보·정식배포미완료.카페완성기사/게시없음.

다음 작업 하나: {nxt}
'''
 doc=R/'docs/WATER_ACTUAL_DAMAGE_CONSUMER.md';assert not doc.exists();doc.write_text(detail,'utf-8')
 entry='\n\n## 작업154 — 급류 실제피해와회피모델\n\n실제3피해=type44/art6C의E6E4충돌/AC95체력차감.153snapshot1812동일·6명령/24geometry CPU쌍.8픽셀상승해당순간회피.핀py65 CE cycle3→instance6정정·v1보존.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER_ACTUAL_DAMAGE_CONSUMER.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  q=R/'docs'/n;q.write_text(q.read_text('utf-8')+entry,'utf-8')
 q=R/'docs/journal/2026-10-07.md';q.write_text(q.read_text('utf-8')+entry.replace('(WATER_ACTUAL_DAMAGE_CONSUMER.md)','(../WATER_ACTUAL_DAMAGE_CONSUMER.md)'),'utf-8')
 q=R/'README.md';q.write_text(q.read_text('utf-8')+'\n\n[급류 실제피해154](docs/WATER_ACTUAL_DAMAGE_CONSUMER.md): 장애물충돌주소·회피CPU조건.\n','utf-8')
 q=R/'docs/HANDOFF.md';s=q.read_text('utf-8').replace('작업153 완료','작업154 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);q.write_text(s+entry,'utf-8')
 files=[doc,p,R/'qa/reports/water154_damage_validation.json',R/'qa/reports/water154_model_cycle_correction.json',R/'config/water_jump_probe153.json',R/'scripts/run_menu_qa.py',R/'scripts/trace_water_progress153_v2.lua',R/'scripts/analyze_river120_v2.py',R/'scripts/verify_gate_font_tag_hooks.py',R/'tools/python/py65-1.2.0/py65/devices/mpu6502.py',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*154*')]
 for d in ['qa/dialogue/water154_damage049','work/water154']:files.extend((R/d).iterdir())
 hp=R/'qa/dialogue/water153_jump049_v2/environment.json';he=json.loads(hp.read_text('utf-8'));files.append(hp);files.extend(hp.parent/f for f in he['files']if f.startswith('frame_')and(hp.parent/f).name in json.loads((R/'qa/dialogue/water154_damage049/environment.json').read_text('utf-8'))['files'])
 m.write_text(json.dumps({'work':154,'files':{q.relative_to(R).as_posix():sha(q)for q in sorted(set(files))if q.is_file()}},indent=2)+'\n','utf-8');print('PASS154 handoff')
if __name__=='__main__':main()
