from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/gatereader149_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/gatereader149_validation.json').read_text('utf-8'))
 assert v['status']=='PASS_BOUNDED_SEEDED_CASTLE_READER'
 images=['gatereader148_normal49_049_resume/frame_'+n+'.png'for n in ['01860','02160','02490','03330']]+['gatereader148_gold4_049/frame_'+n+'.png'for n in ['02160','02610','04500']]
 visual=R/'qa/reports/gatereader149_visual.json';assert not visual.exists()
 visual.write_text(json.dumps({'work':149,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{'qa/dialogue/'+p:sha(R/'qa/dialogue'/p)for p in images},'observations':['normal49: gold4 requirement, insufficient tickets, normal50 offer and farewell readable','gold4: welcome, castle title/rules/departure and actual game HUD readable'],'human_approved':False,'capture_scope':'Seven unedited emulator PNGs; not wholeplay or exact RAM/PNG timing'},ensure_ascii=False,indent=2)+'\n','utf-8')
 nxt='현재049 티켓부족 경로를 실제 PRG 읽기 관측기로 실행하여 변경한 MAIN0590C의 원천 바이트·전용226/227 폰트·완성문·clear를 연결한다.'
 detail=f'''# 작업149 — 성 입장 실제 읽기 검증 재개

[실행 계획](../work/gatereader149/resume_plan_20261007.json), [검증 보고서](../qa/reports/gatereader149_validation.json), [직접 화면](../qa/reports/gatereader149_visual.json), [재개 실행](../scripts/resume_gate_reader149.py), [검증 코드](../scripts/verify_gate_reader149.py).

2026-10-07 사용자 “다시 진행”으로 작업을 재개했다. 완료된148 normal49/047의 동결 환경 및3154개 선언 파일 해시를 다시 확인해 재사용했다. 중단된049의685개 파일은 보존하고 새049_resume에6000프레임을 실행했다. 아직 없던 gold4/047·049는 각9000프레임 새로 실행했다. 동결094 입력과1000프레임 초기 통화 seed를 사용했으며 자연 획득이나 자연 성 완주 검증이 아니다.

normal49는524개, gold4는786개 whole PNG·PPU·OAM·mapping 일치. 실제CHR10480개1KiB 조각은 현재ROM과 같다. actual PRG 읽기222/179건의 주소·값·PC·프레임·문맥·순서가 각각047과 일치했다. 모든읽기PC의 B1 06 명령과 물리주소→원천unit를 검증했다. normal49의 cycle차는184건0/9건1/29건2; gold4는134건0/35건38/10건76이다. 전체CPU·IRQ·RNG·오디오 동일성을 주장하지 않으며 RAM22/IRQstack·CPU/bus차이는 보고서에 유지했다.

성명0F·주의16·골드요금17·부족18·작별19·일반50제안1A·질문1B·환영1C·설명22·제목28의 원천 전체바이트를 실제읽기로 확인했다. 고정/매크로 native reader가 확장한13개 경로별 페이지의 모든줄과 font154/173/175/177/179/181/185/193/196 실제NT를 연결했다. 1A는 FA 동적숫자가 있어 zero-RAM reader의 전줄NT 주장에서 제외했다. 실제PNG에는 일반티켓50장 제안이 읽히며 원천읽기는 완전하다. normal49/골드0 그대로 지도복귀(root8), gold4/normal10 그대로 성게임(root4/phase5/course4)이 확인됐다.

7개 실제PNG에서 골드요금·부족·50장제안·작별·환영·제목/설명/출발·게임HUD를 직접 검토했다. 사람 문체·명칭·그림 최종승인은 false이다.

변경: resume_gate_reader149.py, verify_gate_reader149.py, seal_gate_reader149.py, work/gatereader149 계획/log, 새QA3폴더, 최종·시각보고서, 상세·날짜별인계·journal·README·SURVEY·PLAN·HANDOFF, manifest/audit. 원본·1편·중단148·역사증거·ROM·CSV 보존. ROM SHA `{v['routes'][0]['ROM_sha256']}`, CSV SHA `{v['CSV_sha256']}`. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`.

재현: `python scripts/resume_gate_reader149.py` 후 `python scripts/verify_gate_reader149.py`. 실행계획과QA가 존재하면 거부하므로 재현시 새작업ID/출력을 지정해야 한다. 원본 검증 `powershell -File scripts/verify_source.ps1` PASS. 정적/동결SHA·명시seed runtime·실제reader/CHR/NT·whole화면대조·직접7PNG PASS. 신규build/apply/state/reset/청음/실기 미수행. 자연전체완주·global corpus·HOWTO/PAUSE/POW 소비·사람최종·정식배포 미완료. 카페용 완성기사나 외부게시 없이 근거를 journal에 기록한다.

다음 작업 하나: {nxt}
'''
 doc=R/'docs/CASTLE049_SOURCE_READER_RESUME.md';assert not doc.exists();doc.write_text(detail,'utf-8')
 entry='\n\n## 작업149 — 성 입장 reader 재개\n\n일반49/골드4 경로 각각6000/9000프레임. 합1310 whole화면·10480CHR 일치, actual PRG222/179 읽기·10원천unit·13경로별 전줄NT 연결. 일반49 거절복귀/골드4 성진입·7실제PNG 확인. 중단148 보존, ROM·CSV 불변.\n\n[상세 변경·SHA·검증구분·재현·한계](CASTLE049_SOURCE_READER_RESUME.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text((p.read_text('utf-8')if p.exists()else '# 인계 2026-10-07\n')+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text((p.read_text('utf-8')if p.exists()else '# 작업 경과 2026-10-07\n')+entry.replace('(CASTLE049_SOURCE_READER_RESUME.md)','(../CASTLE049_SOURCE_READER_RESUME.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[현재049 성 입장 실제읽기149](docs/CASTLE049_SOURCE_READER_RESUME.md): 중단148 보존·재개 검증.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');s=s.replace('# 세션 종료 — 2026-10-06, 작업148 중단','# 진행 중 — 2026-10-07, 작업149 완료',1)
 old='사용자의 “오늘은 여기까지” 지시로 작업148을 중단하고 소유 실행을 종료했다. 새로운 재개 지시 전에는 자동 진행하지 않는다. 마지막 완전히 닫힌 작업은147이다.'
 assert old in s;s=s.replace(old,'2026-10-07 사용자의 “다시 진행”으로 재개했다. 작업148 중단 자료는 보존했고 작업149에서 새049 실행과 골드4 경로를 검증했다. 별도 중단 지시 전까지 허가된 개발 작업을 계속한다.',1)
 import re
 s=re.sub(r'\*\*다음 작업 하나\(사용자 재개 지시 후\):.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1)
 s=s.replace('[오늘 인계](HANDOFF_2026-10-06.md), [오늘 journal](journal/2026-10-06.md)','[오늘 인계](HANDOFF_2026-10-07.md), [오늘 journal](journal/2026-10-07.md)',1);p.write_text(s+entry,'utf-8')
 files=[doc,visual,R/'qa/reports/gatereader149_validation.json',R/'scripts/verify_reader_pair142.py',R/'scripts/verify_dialogue_home.py',R/'scripts/trace_booth_reader141.lua',R/'scripts/run_branch_reader141.py',R/'extracted/text/table_20261004_001/text_tokens.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*149*')]
 for d in ['qa/dialogue/gatereader148_normal49_047','qa/dialogue/gatereader148_normal49_049_resume','qa/dialogue/gatereader148_gold4_047','qa/dialogue/gatereader148_gold4_049','work/gatereader149']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':149,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work149 handoff')
if __name__=='__main__':main()
