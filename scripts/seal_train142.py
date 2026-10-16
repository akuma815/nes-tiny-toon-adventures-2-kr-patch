from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/train142_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/train142_validation.json').read_text('utf-8'));assert v['actual_PRG_data_reads_each']==159
 nxt='急流타기 메뉴 경로를 현재049와 새047에서 동일 입력으로 실행해, RAM seed 없이 실제 reader/상단21·27/하단요금·출발/게임진입의 폰트 수명을 확인한다.'
 nxt=nxt.replace('急流타기','급류타기')
 paths=['qa/dialogue/train142_native_049/'+f for f in ['frame_01620.png','frame_01710.png','frame_02010.png','frame_02070.png','frame_02790.png','frame_04260.png']]
 vr=R/'qa/reports/train142_visual.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':142,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{p:sha(R/p)for p in paths},'observations':['1620 title/rules and lower fee beginning','1710 completed fee2 and request readable','2010 partial 출 during new lower departure','2070 complete 출발! readable','2790 actual train gameplay and HUD normal008','4260 returned map/어디로 갈까? readable'],'scope':'Direct selected real PNGs; no complete train course, hardware or human language approval'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail='''# 작업142 — 현재049 기차 메뉴·요금·출발·플레이

[최종 검증](../qa/reports/train142_validation.json), [직접 화면](../qa/reports/train142_visual.json), [실행 계획](../work/train142/run_plan.json), [reader 관측](../scripts/trace_train_reader142.lua), [검증](../scripts/verify_train142.py).

현재049/새047을 같은 메뉴기차 입력과 읽기전용 관측기로 각각4500프레임 실행했다. RAM seed/state load/ROM write 없이 냉부팅 기본티켓10장으로 진행했다. 요금2장 차감 후8장이 되고, 기차 초기 플레이를 거쳐 지도에 돌아왔다. 이 입력은 기차 완주에 성공한 플레이가 아니다. 63개 실제 root4/phase5/course2 게임 스냅샷을 확인했다.

339 whole PNG/PPU/OAM/CHR mapping이 같고, 현재ROM과2712 CHR chunks가 일치한다. 실제 PRG data read159건씩의 주소·값·PC·프레임·순서·문맥이 같다.107건 cycle동일/42건+38/10건+76은보고서에남긴다. 한프레임의여러page초기화에따른누적시간차이를동일실행으로포장하지않는다. helper20개write PC의동일STA 바이트확인/RAM22·stack/A·flags·bus차이는별도다. 전체CPU/IRQ/RNG/오디오동일성은아니다.

현재 main20(MAIN05882) 기차설명/main26(MAIN058FA) 제목/macro86(MACRO061E9)의전체source byte범위가실제로읽혔다. native0D선택/20·26상단/1D요금/2A출발을따른다. 실제headerfont193과lower196을구분한다. native reader모델의title padding포함12glyph를NT20A6,설명2줄을2125/2165,출발을22A8에서확인했다. header1578부터/lower2019부터완성NT가일치한다. 역사plan의일반적인NT주소를현재완성위치로자동적용하지않았다.

직접1620부분요금/1710완성요금2·티켓내기/2010부분출발/2070완성/2790기차HUD008/4260다음지도6PNG를검토했다. 캡처118의시점한계는유지한다. 新실행의ROM hash와원본hash/설정/Lua/입력 및 전체기록해시를확인했다. 신규실패없음.

변경: prepare_train142.py/trace_train_reader142.lua/run_train142.py/verify_reader_pair142.py/verify_train142.py/seal_train142.py;work/train142계획·log;qa/dialogue새047/현재049;최종/직접시각보고서;본상세·datedhandoff/journal/SURVEY/PLAN/HANDOFF/README;manifest/audit.원본/1편/역사증거/ROM049/CSV불변. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`.個別SHAはmanifest/environmentに記録する。

정적/해시/controller-only runtime/실제 reader/whole영상/선택6PNG 직접 PASS. 신규 build/apply/state/reset/PCM청음/하드웨어 없음. 재현 `python scripts/prepare_train142.py`, `python scripts/run_train142.py`, `python scripts/verify_train142.py`;기존출력거부. 전체기차/게임완주·globalcorpus·HOWTO/PAUSE/POW·사람최종문체/명칭/그림·정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

'''
 detail=detail.replace('個別SHAはmanifest/environmentに記録する。','개별SHA는manifest/environment에기록한다.').replace('新실행','새 실행')
 doc=R/'docs/TRAIN049_NATIVE_READER.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업142 — 현재049 기차 controller-only reader\n\n새047/049 각4500·339wholePNG/PPU/OAM/mapping·2712CHR exact.실제PRG159건·20/26/macro86 전체byte소비와title/rules/departNT완성확인.티켓10→8/초기기차63snapshot/지도복귀·직접6PNG. cycle0/38/76과idle/stack/bus차이유지·ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](TRAIN049_NATIVE_READER.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(TRAIN049_NATIVE_READER.md)','(../TRAIN049_NATIVE_READER.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[기차049 검증142](docs/TRAIN049_NATIVE_READER.md): 실제reader·요금2·title/rules/depart/초기플레이·지도복귀.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업141 이후','작업142 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/train142_validation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'extracted/text/table_20261004_001/text_tokens.json',R/'config/menu_train_001.json',*(R/'scripts').glob('*142*')]
 for d in ['qa/dialogue/train142_native_047','qa/dialogue/train142_native_049','work/train142']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':142,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work142 handoff')
if __name__=='__main__':main()
