from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/coaster147_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/coaster147_validation.json').read_text('utf-8'));assert v['actual_PRG_data_reads_each']==137
 nxt='성의normal49 거절과gold4 입장을현재049/새047에서각동결입력·seed로실행하며실제reader를기록해,main0F/16..1C/22/28의원천전체byte·완성NT를연결한다.'
 paths=['qa/dialogue/coaster147_native_049/'+f for f in ['frame_01710.png','frame_02070.png','frame_02790.png','frame_04500.png']]
 vr=R/'qa/reports/coaster147_visual.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':147,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{p:sha(R/p)for p in paths},'observations':['1710 coaster title/rules and completed fee1 request readable','2070 departure readable','2790 initial coaster game/HUD normal006','4500 early rollercoaster gameplay/HUD'],'scope':'Short controller-only route; no winningbot/course completion/second or third segment claim; no human final approval'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail=f'''# 작업147 — 현재049 롤러코스터 실제 reader

[최종 검증](../qa/reports/coaster147_validation.json), [직접 화면](../qa/reports/coaster147_visual.json), [실행계획](../work/coaster147/run_plan.json), [검증](../scripts/verify_coaster147.py).

현재049/새047을각4500프레임기존짧은menu_coaster 입력으로실행했다. 동결142 reader관측기와검증기반을재사용했고RAM seed/state load/ROM write가없다. 기본티켓10장에서요금4장차감으로6장이되며현재root4/phase5/course0의초기 롤러코스터 구간플레이를확인했다. 실제게임스냅샷{len(v['gameplay_frames'])}개다. 117에서닫은winningbot/완주/후반구간실험을재개한작업이아니다.

312 wholePNG/PPU/OAM/mapping exact/2496CHR chunks currentROM exact. PRG data read137건씩의주소·값·PC·프레임·순서·문맥동일.81 cycle동일/41건+38/15건+76. helper16 writePC의같은STA byte확인·RAM22/IRQstack/A·flags·bus차이유지. 전체CPU/매IRQ시각/RNG/오디오동일성은주장하지않는다.

main1E(MAIN05849)설명/main24(MAIN058F2)제목/macro84(MACRO061D3)롤러코스터명전체원천byte를실제읽기주소로연결했다. native0B선택→1E/24상단→1D요금→2A출발과정의font193/196수명이유지된다. native-reader모델의titleNT20A6/rules2125·2165/depart22A8전체줄완성확인.1710설명/요금4·2070출발·2790초기게임·4500첫구간4PNG를직접검토했다. 현재RAW입력원천은기존130에서쓰던문구/그림과같고,이번차별점은실제reader·원천byte·font·NT연결이다.

변경: prepare_coaster147.py/run_coaster147.py/verify_coaster147.py/seal_coaster147.py,work/coaster147계획·log,qa/dialogue새047/현재049,최종/직접시각보고서,상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README·manifest/audit. 실제재사용142 observer/verifier및config/menu_coaster_001.json도동결SHA에포함. 신규실패없음·원본/1편/역사증거/ROM/CSV보존. ROM SHA `{v['ROM_sha256']}`,CSV SHA `{v['CSV_sha256']}`.

정적/해시/controller-only runtime/실제reader/whole영상/선택4PNG 직접 PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_coaster147.py`, `python scripts/run_coaster147.py`, `python scripts/verify_coaster147.py`;기존출력거부. 초기 롤러코스터 구간이상/자연전체완주/globalcorpus/HOWTO·PAUSE·POW/사람문체·명칭·그림최종/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

'''
 doc=R/'docs/COASTER049_NATIVE_READER.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업147 — 현재049 롤러코스터 reader reader\n\n각4500·312wholePNG/PPU/OAM/mapping·2496CHR exact. PRG137건/1E·24·macro84전체byte/전줄NT/티켓10→6/초기게임·4actualPNG. idle/stack/bus·cycle0/38/76보존. winningbot·완주stream재개없음/ROM·CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](COASTER049_NATIVE_READER.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(COASTER049_NATIVE_READER.md)','(../COASTER049_NATIVE_READER.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[롤러코스터049 실제reader147](docs/COASTER049_NATIVE_READER.md): 짧은메뉴·요금4·출발·첫구간;완주bot은닫힘.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업146 이후','작업147 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/coaster147_validation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'extracted/text/table_20261004_001/text_tokens.json',R/'config/menu_coaster_001.json',R/'scripts/verify_reader_pair142.py',R/'scripts/trace_train_reader142.lua',*(R/'scripts').glob('*147*')]
 for d in ['qa/dialogue/coaster147_native_047','qa/dialogue/coaster147_native_049','work/coaster147']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':147,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work147 handoff')
if __name__=='__main__':main()
