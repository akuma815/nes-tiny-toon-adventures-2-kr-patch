from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/water143_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/water143_validation.json').read_text('utf-8'));assert v['actual_PRG_data_reads_each']==150
 nxt='무입력 인트로9문단을 현재049/새047에서6000프레임 실행하며 물리PRG 읽기를 추가해,현재 font128..146과각문단·macro의실제소비및완성NT를연결한다.'
 paths=['qa/dialogue/water143_native_049/'+f for f in ['frame_01710.png','frame_02010.png','frame_02070.png','frame_02790.png','frame_04320.png']]
 vr=R/'qa/reports/water143_visual.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':143,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{p:sha(R/p)for p in paths},'observations':['1710 title/rules and completed fee3 request readable','2010 partial departure 출','2070 complete 출발! readable','2790 water gameplay/HUD normal007','4320 map return readable'],'scope':'Selected actual PNG review; no whole water course, hardware, audio or human final language approval'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail='''# 작업143 — 현재049 급류타기 메뉴와 실제 reader

[최종 검증](../qa/reports/water143_validation.json), [직접 화면](../qa/reports/water143_visual.json), [실행 계획](../work/water143/run_plan.json), [검증](../scripts/verify_water143.py).

142의 동결 읽기전용 관측기/검증 기반을 사용해 현재049와 새047을 급류 메뉴 입력으로 각각4500프레임 실행했다. 냉부팅 기본티켓10장으로 진행하며 RAM seed/state load/ROM write가 없다. 요금3장 차감으로7장이 되고, 초기 급류 플레이를 거쳐 지도에 복귀했다. 실제course3/root4/phase5 게임 스냅샷은63개이며 급류 완주는 아니다.

312 whole PNG/PPU/OAM/mapping exact, 현재ROM과2496 CHR chunks가 일치한다. 실제 PRG data read150건씩의 주소·값·PC·프레임·순서·문맥이 같고96건cycle동일/39건+38/15건+76이다. helper18 writePC 이동은 같은STA 바이트로 확인했다. RAM22/IRQstack/A·flags/bus차이를유지하고全CPU/IRQ/RNG/오디오동일성은주장하지않는다.

main21(MAIN058A6) 설명/main27(MAIN058FE) 제목/macro87(MACRO061EF)의 원천 전체byte가 실제로 소비되었다. native0E선택/21·27상단/1D요금/2A출발을따른다. font193 상단과196 하단을구분해 titleNT20A6/rules2125·2165는1578부터,출발22A8은2019부터native-reader모델의모든glyph와완성NT가일치한다. 요금·출발부분출력/지우기후폰트/다음지도는전체paired영상및선택직접화면으로확인했다.

직접1710 완성요금3/2010부분출발/2070완성/2790급류HUD007/4320지도5actualPNG를검토했다. 캡처118시점한계 유지. 신규실패없음. 원본/1편/역사QA/현재049/CSV보존.

변경: prepare_water143.py/run_water143.py/verify_water143.py/seal_water143.py;work/water143계획·log;qa/dialogue새047/현재049;최종/직접시각보고서;본상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README·manifest/audit. 실제재사용141/142 observer와검증스크립트도manifest SHA로동결한다. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변.

정적/해시/controller-only runtime/실제reader/whole영상/선택5PNG 직접 PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_water143.py`, `python scripts/run_water143.py`, `python scripts/verify_water143.py`;기존출력거부. 全급류/게임완주/globalcorpus/HOWTO·PAUSE·POW/사람문체·명칭·그림최종검토/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

'''.replace('全CPU','전체CPU').replace('全급류','전체 급류')
 doc=R/'docs/WATER049_NATIVE_READER.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업143 — 현재049 급류 controller-only reader\n\n새047/049 각4500·312wholePNG/PPU/OAM/mapping·2496CHR exact.실제PRG150건/21·27·macro87전체byte와title/rules/departNT완성확인.티켓10→7/초기급류63snapshot/지도복귀·직접5PNG. cycle0/38/76/idle·stack·bus차이유지·ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER049_NATIVE_READER.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(WATER049_NATIVE_READER.md)','(../WATER049_NATIVE_READER.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[급류049 검증143](docs/WATER049_NATIVE_READER.md): 실제reader·요금3·title/rules/depart/초기플레이·지도복귀.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업142 이후','작업143 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/water143_validation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'extracted/text/table_20261004_001/text_tokens.json',R/'config/menu_water_001.json',R/'scripts/verify_reader_pair142.py',R/'scripts/trace_train_reader142.lua',*(R/'scripts').glob('*143*')]
 for d in ['qa/dialogue/water143_native_047','qa/dialogue/water143_native_049','work/water143']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':143,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work143 handoff')
if __name__=='__main__':main()
