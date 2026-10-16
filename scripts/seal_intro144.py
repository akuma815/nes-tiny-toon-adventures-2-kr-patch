from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/intro144_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/intro144_validation.json').read_text('utf-8'));assert v['actual_PRG_data_reads_each']==676
 nxt='138の54原帳に139..144の現在初期化・実際reader・完成NT・直接画像の別々の証拠を追記した新しい145原帳を作り、残る現在reader未接続の登録原文から次の一経路を選ぶ。'
 nxt='138の原帳を保存し、139..144を反映した新しい54原帳145を作り、現在の初期化・実際reader・完成NT・直接画像を区分して未接続原文の次の一経路を選ぶ。'
 nxt='138 원장을 보존하고 139..144를 반영한 새54원장145를 작성해, 현재초기화/실제reader/완성NT/직접PNG를구분한뒤 남은등록원천의reader 미연결 한경로를선택한다.'
 frames=[1080,1320,1560,1800,1920,2160,2520,2640,2880]
 paths=[f'qa/dialogue/intro144_native_049/frame_{f:05d}.png'for f in frames]
 vr=R/'qa/reports/intro144_visual.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':144,'status':'DIRECT_ALL_NINE_ACTUAL_INTRO_PNG_REVIEW','images':{p:sha(R/p)for p in paths},'observations':['All nine real intro paragraph PNGs readable; source scenes remain visible','Native1/2/4/7/9 two-lines,3/8 one-line,5 four-lines,6 three-lines retained','Buster name and native quotes/punctuation render in active per-page fonts'],'scope':'Direct nine selected complete images; partial/clear/next-page bounded pair evidence separate. No human final wording/name/graphics approval.'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail='''# 작업144 — 현재049 인트로9문단 실제 읽기와 완성

[최종 검증](../qa/reports/intro144_validation.json), [직접9화면](../qa/reports/intro144_visual.json), [실행계획](../work/intro144/run_plan.json), [검증v3](../scripts/verify_intro144_v3.py).

현재049와새047을각6000프레임냉부팅했다. 입력목록은빈배열이고Start/RAM seed/state load/ROM write가없다. 제목과9인트로문단의두번순환을같은동결142 reader로기록했다.실제PRG read676건씩의주소·값·PC·프레임·순서·문맥이같다.主본문01..09의각전체원천byte와공유버스터macro80/81원천(MACRO061C3)의전체범위가소비되었다. nativeID가진행해도실제물리주소로귀속한다. macro82가이경로에서관측되지않았다는사실을전역unused로해석하지않는다.

200 whole PNG/PPU/OAM/mapping exact 및현재ROM과1600CHR chunks exact. reader651건cycle동일/24건+1/1건+2는보고서에그대로보존한다. 全CPU/IRQ/RNG/오디오동일성아니다. helper42 writePC이동은같은STA 명령바이트로확인했다. intro전용06CF/C6/6F3초기화3종각2회도별도허용목록이다. RAM22/IRQstack/A·flags·bus차이는보고서에기록한다.

각font128/132/134/136/138/140/142/144/146은native-reader모델의모든줄과actualNT21E4+row64가완성시일치했다. 실제줄수는01/02/04/07/09가2줄,03/08이1줄,05가4줄,06이3줄이다. 완성시작은각1020/1320/1500/1740/1920/2100/2340/2640/2760의기록된snapshot이며exactprinterfinishcycle을뜻하지않는다.9개완성PNG1080/1320/1560/1800/1920/2160/2520/2640/2880을직접검토했고문장·버스터·원래장면·인용부호를확인했다.部分출력/지우기/다음문단수명은전체200paired자료로비교했다. 캡처118시점한계 유지.

검증v1은메뉴의writePCrelocation목록만재사용해인트로초기화3명령을놓쳤다. v2는이동STA byte를확인했지만무입력상태티켓0을잘못가정해최종숫자guard가실패했다. 실제native기본티켓10장은600부터설정되며두빌드동일하다. v3는관측대로10을검증했다. [v1관측](../qa/reports/intro144_verifier_v1_observation.json), [v2관측](../qa/reports/intro144_verifier_v2_observation.json) 및실패스크립트를보존했다. 보고서쓰기전검증가정실패이며실행자료/ROM변경없이해결했다.

변경: prepare_intro144.py/run_intro144.py/prepare_verify_intro144.py/v2/v3/verify_intro144.py/v2/v3/seal_intro144.py;config/intro_no_inputs144.json;work/intro144계획·log;qa/dialogue새047/현재049자료;최종/직접시각/관측보고서;본상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README;manifest/audit. 기존138원장/130인트로/역사QA·원본·1편·049·CSV보존. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변.

정적/해시/무입력runtime/실제reader/whole영상/9선택직접PNG PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_intro144.py`, `python scripts/run_intro144.py`, `python scripts/verify_intro144_v3.py`;기존출력거부. globalcorpus/全game/기타소비경로/사람문체·명칭·그림최종/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

'''
 for x,y in [('主본문','주본문'),('全CPU','전체CPU'),('部分출력','부분출력'),('全game','전체게임')]:detail=detail.replace(x,y)
 doc=R/'docs/INTRO049_NATIVE_READER.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업144 — 현재049 무입력 인트로9 실제reader\n\n각6000·200wholePNG/PPU/OAM/mapping·1600CHR exact.실제PRG676건/9main·macro버스터전체byte 소비 및모든줄완성NT·font128..146연결·9actualPNG직접검토.651cycle동일/24+1/1+2·idle/stack/bus차이유지.검증v1/v2가정실패보존/v3해결·기본티켓10/ROM·CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](INTRO049_NATIVE_READER.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(INTRO049_NATIVE_READER.md)','(../INTRO049_NATIVE_READER.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[인트로049 실제reader144](docs/INTRO049_NATIVE_READER.md): 전체9문단의실제원천byte·완성NT·직접9PNG·2순환.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업143 이후','작업144 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/intro144_validation.json',R/'qa/reports/intro144_verifier_v1_observation.json',R/'qa/reports/intro144_verifier_v2_observation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'extracted/text/table_20261004_001/text_tokens.json',R/'config/intro_no_inputs144.json',R/'scripts/trace_train_reader142.lua',R/'scripts/verify_reader_pair142.py',*(R/'scripts').glob('*144*')]
 for d in ['qa/dialogue/intro144_native_047','qa/dialogue/intro144_native_049','work/intro144']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':144,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work144 handoff')
if __name__=='__main__':main()
