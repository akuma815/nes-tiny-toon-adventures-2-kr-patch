from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/cart146_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/cart146_validation.json').read_text('utf-8'));assert v['actual_PRG_data_reads_each']==142
 nxt='현재049/새047에서RAM seed 없는기본10장 롤러코스터메뉴·요금·출발경로를실행해,MAIN05849(rule1E)/MAIN058F2(title24)의실제reader/전줄NT완성과초기게임폰트수명을연결한다.'
 paths=['qa/dialogue/cart146_native_049/'+f for f in ['frame_01710.png','frame_02070.png','frame_02790.png','frame_04500.png']]
 vr=R/'qa/reports/cart146_visual.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':146,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{p:sha(R/p)for p in paths},'observations':['1710 cart title/rules and completed fee1 request readable','2070 departure readable','2790 initial cart game/HUD normal009','4500 still first segment gameplay/HUD'],'scope':'Short controller-only route; no winningbot/course completion/second or third segment claim; no human final approval'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail=f'''# 작업146 — 현재049 쇼킹 카트 실제 reader

[최종 검증](../qa/reports/cart146_validation.json), [직접 화면](../qa/reports/cart146_visual.json), [실행계획](../work/cart146/run_plan.json), [검증](../scripts/verify_cart146.py).

현재049/새047을각4500프레임기존짧은menu_cart 입력으로실행했다. 동결142 reader관측기와검증기반을재사용했고RAM seed/state load/ROM write가없다. 기본티켓10장에서요금1장차감으로9장이되며현재root4/phase5/course1의첫카트구간플레이를확인했다. 실제게임스냅샷{len(v['gameplay_frames'])}개다. 117에서닫은winningbot/완주/후반구간실험을재개한작업이아니다.

339 wholePNG/PPU/OAM/mapping exact/2712CHR chunks currentROM exact. PRG data read142건씩의주소·값·PC·프레임·순서·문맥동일.100 cycle동일/27건+38/15건+76. helper18 writePC의같은STA byte확인·RAM22/IRQstack/A·flags·bus차이유지. 전체CPU/매IRQ시각/RNG/오디오동일성은주장하지않는다.

main1F(MAIN05867)설명/main25(MAIN058F6)제목/macro85(MACRO061DE)카트명전체원천byte를실제읽기주소로연결했다. native0C선택→1F/25상단→1D요금→2A출발과정의font193/196수명이유지된다. native-reader모델의titleNT20A6/rules2125·2165/depart22A8전체줄완성확인.1710설명/요금1·2070출발·2790초기게임·4500첫구간4PNG를직접검토했다. 현재RAW입력원천은기존130에서쓰던문구/그림과같고,이번차별점은실제reader·원천byte·font·NT연결이다.

변경: prepare_cart146.py/run_cart146.py/verify_cart146.py/seal_cart146.py,work/cart146계획·log,qa/dialogue새047/현재049,최종/직접시각보고서,상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README·manifest/audit. 실제재사용142 observer/verifier및config/menu_cart_001.json도동결SHA에포함. 신규실패없음·원본/1편/역사증거/ROM/CSV보존. ROM SHA `{v['ROM_sha256']}`,CSV SHA `{v['CSV_sha256']}`.

정적/해시/controller-only runtime/실제reader/whole영상/선택4PNG 직접 PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_cart146.py`, `python scripts/run_cart146.py`, `python scripts/verify_cart146.py`;기존출력거부. 첫카트구간이상/자연전체완주/globalcorpus/HOWTO·PAUSE·POW/사람문체·명칭·그림최종/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

'''
 doc=R/'docs/CART049_NATIVE_READER.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업146 — 현재049 짧은카트경로 reader\n\n각4500·339wholePNG/PPU/OAM/mapping·2712CHR exact. PRG142건/1F·25·macro85전체byte/전줄NT/티켓10→9/초기게임·4actualPNG. idle/stack/bus·cycle0/38/76보존. winningbot·완주stream재개없음/ROM·CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](CART049_NATIVE_READER.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(CART049_NATIVE_READER.md)','(../CART049_NATIVE_READER.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[쇼킹 카트049 실제reader146](docs/CART049_NATIVE_READER.md): 짧은메뉴·요금1·출발·첫구간;완주bot은닫힘.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업145 이후','작업146 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/cart146_validation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'extracted/text/table_20261004_001/text_tokens.json',R/'config/menu_cart_001.json',R/'scripts/verify_reader_pair142.py',R/'scripts/trace_train_reader142.lua',*(R/'scripts').glob('*146*')]
 for d in ['qa/dialogue/cart146_native_047','qa/dialogue/cart146_native_049','work/cart146']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':146,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work146 handoff')
if __name__=='__main__':main()
