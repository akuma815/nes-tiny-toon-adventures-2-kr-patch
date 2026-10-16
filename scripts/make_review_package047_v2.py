"""Frozen ROM-free review047 package and actual Windows apply evidence."""
from pathlib import Path
import json,hashlib,shutil,subprocess,csv
import release_apply_helpers as helper
R=Path(__file__).resolve().parents[1]
NAME='TinyToonAdventures2_KR_Review_047_20261005'
PATCH=NAME+'.xdelta'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));src=R/source['path'];target=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
 build=json.loads((target.parent/'build_report.json').read_text('utf-8'));assert sha(src)==source['sha256']==build['source_sha256'] and sha(target)==build['output_sha256']
 assert src.stat().st_size==262160 and target.stat().st_size==499728
 reports={}
 for name in ('stop080_validation','stop081_regression','start077_validation','start078_regression','notices074_runtime','notices075_natural','gate090_validation','gate091_validation','review092_session'):
  p=R/'qa/reports'/f'{name}.json';j=json.loads(p.read_text('utf-8'));assert j['status']=={'stop080_validation':'PASS_STOP046_NATIVE_TRAIN','start077_validation':'PASS_START045_NATURAL_CART','notices075_natural':'PASS_NATURAL_NOTICES_AND_HOME_RETURN','gate090_validation':'PASS_STATIC_BUILD_REBUILD_IPS_APPLY_RUNTIME_PENDING','gate091_validation':'PASS_GATE047_NATURAL_RUNTIME'}.get(name,'PASS');reports[name]={'sha256':sha(p),'scope':j.get('scope','See frozen report and project handoff')}
 csvpath=R/'workspace/translation/text_ja.csv';rows=list(csv.DictReader(csvpath.open(encoding='utf-8-sig')));assert len(rows)==54 and sum(x['status']=='draft'for x in rows)==45
 out=R/'dist'/NAME;qa=R/'qa/apply/2편 개발047 한글 공백 적용 검증 20261005_093';proof=R/'qa/reports/review047_package_final.json'
 assert not any(p.exists()for p in (out,qa,proof))
 (out/'tools').mkdir(parents=True);(out/'licenses').mkdir()
 F=R.parent/'Tiny Toon Adventures';vendor=F/'dist/TinyToonAdventures_KR_Patch_v1.0_20261004'
 vendorfiles=['tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md'];provenance={n:sha(vendor/n)for n in vendorfiles}
 for n in vendorfiles:shutil.copy2(vendor/n,out/n)
 tool=out/'tools/xdelta3.exe';v=subprocess.run([str(tool),'-V'],capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);version=(v.stdout+v.stderr).decode('utf-8','replace');assert '3.2.0'in version and 'Apache'in version
 subprocess.run([str(tool),'-e','-9','-S','none','-A','-s',str(src),str(target),str(out/PATCH)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 values={'@SOURCE_SHA@':sha(src),'@TARGET_SHA@':sha(target),'@PATCH_NAME@':PATCH,'@PATCH_SHA@':sha(out/PATCH),'@XDELTA_SHA@':sha(tool)}
 text=(F/'workspace/release/apply_xdelta.ps1.in').read_text('utf-8');assert '524304'in text
 text=text.replace('524304','499728').replace('Tiny Toon Adventures 일본판','Tiny Toon Adventures 2 일본판').replace('타이니 툰 어드벤처의 한글 패치를','타이니툰 어드벤처 2 검토용 한글 패치를')
 for a,b in values.items():text=text.replace(a,b)
 assert not any(a in text for a in values)
 helper.windows_text(out/'apply.ps1',text)
 cmd=(F/'workspace/release/apply.cmd.in').read_text('utf-8').replace('Tiny Toon Adventures Japan','Tiny Toon Adventures 2 Japan').replace('Tiny Toon Adventures (Japan).nes','Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes')
 helper.windows_text(out/'apply.cmd',cmd,bom=False)
 notes='# 타이니툰 어드벤처 2 — 검토용 개발본047\n\n요청 사용자 검토용 개발 초안이다. 최종 번역·명칭·디자인의 사람 승인과 전체 자연 플레이·전역 원천 폐쇄는 미완료다. ROM 없는 차분 패치와 Windows 적용 도구이며 최종 공개판 자격은 없다.\n\n생성형 타이틀·지도·매표소·게임오버 그림, 등록 본문45초안, 놀이기구 안내·크레딧·HUD·보너스·기차 간판·시간 초과!·다음 라운드!·시작!·정지 표지를 포함한다. 작은 안내는 Galmuri7 비트맵이며 AI 제작이라고 주장하지 않는다. 일본판 원본에서 실제 소비 루틴·뱅크·타일을 연결한 후 삽입했다.\n\n047은 성 입구 MAIN_057C1을 ‘골드 티켓 4장이 있으면 / 입장할 수 있어요’로 다듬었다. 046 대비129바이트가 해당 문장과 전용175/176폰트 안에서만 달라진다. CPU·매퍼·헤더·다른 원천과 그림은 그대로다. CSV SHA는 release_report.json에 있다. 등록54원천은45초안과9기술공유이며 미번역 일본어 문장9개가 남았다는 뜻이 아니다. 별도047 사람검토 HTML/ZIP은 프로젝트 workspace/review에 있다.\n\n현재047과046을 동일한 controller-only 입력으로 각각5400frames 실행했다.396화면 중360전체pixel exact,36대사두행만 변경, OAM/전체state/주소mapping과native폰트 PPU 및 보호영역을 검증했다. native reader151회로 출력 scratch/buffer glyph쌍과 스택A 차이를 제약했다. 완성 문장은 실제NT코드와 RGB를 독립재구성했다. 이는 골드0 입장불가 경로이며 자연적으로 골드4를 획득한 입장을 뜻하지 않는다.\n\n앞선046의 정지 표지302화면·실제PPU읽기20560행 및 다른3코스852화면/4260파일 보존,045/044의 시작·다음라운드·시간초과 자연관측을 역사적 증거로 계승한다. 새047 저장상태/리셋 실행은 아직 수행하지 않았다.046의 동일빌드 저장·복원/리셋검증은 그 빌드에 한정된다. 빌드 간 저장상태 호환성을 주장하지 않으므로 타이틀부터 실행한다.\n\n원본부터9 Expected Writes/전체출력·제어/매크로·숫자4·960setupABI·IRQ시점·독립재빌드9파일·실제IPS적용을 검증했다. 이 xdelta 묶음은 한국어·공백 경로에서 Windows apply.cmd8검사와 최종ZIP추출 재적용을 별도로 실행한다.\n\n카트 첫 구간 자연클리어는 확인했으나 두번째 마지막2F 적은 반복 실험에서도 시간초과했고3구간 전체완주는 미완료다. 이 실패를 보존했으며 검증 통과로 표현하지 않는다. 오디오의 레지스터 순서/DMC원본바이트는 이전빌드에서 보존 확인했지만146출력위상 관측차이가 남아 PCM동일성/청음 통과는 주장하지 않는다.\n\nPUSH START·회사/저작권·제작진 영문이름·기차M은 현재 개발결정에 따라 보존했다. PAUSE/HOW TO CONTROL/POW 후보는 제한된 조사이며 전역 미사용이나 최종사람 보존 승인이 아니다.\n\n미수행: 전게임 자연완주·모든분기·전역corpus폐쇄·현재047 신규리셋/저장상태·실기·PCM청음·최종사람검토. 네이버 카페 작업기는 모든 작업이 끝난 뒤 작성하며 외부에 게시하지 않았다. 게임/캐릭터/상표 권리는 각 권리자에게 있고 xdelta/Galmuri 라이선스를 동봉했다.\n'
 (out/'RELEASE_NOTES_KO.md').write_text(notes,'utf-8')
 helper.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처 2 — 검토용 개발본047 (2026-10-05)

ZIP을 모두 풀고 일본판 원본 NES ROM을 준비하세요. ROM은 포함하지 않습니다.

1. apply.cmd에 일본판 원본을 끌어 놓으세요.
2. 같은 폴더에 <원본명>_KR.nes가 생깁니다. 기존 파일을 덮어쓰지 않습니다.
3. 새 ROM을 타이틀부터 실행하여 검토하세요.

명령으로 출력 이름을 지정할 수 있습니다:
apply.cmd "Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" "TinyToon2_KR_Review047.nes"

Windows x64와 기본 Windows PowerShell이 필요합니다. Python이나 별도 패치 도구 설치는 필요 없습니다. 원본·패치·도구·결과의 해시를 자동 검사합니다.
원본: 262160바이트 / SHA-256 {sha(src).upper()}
결과: 499728바이트 / SHA-256 {sha(target).upper()}

잘못된 원본, 이미 적용한 ROM, 손상된 도구/패치, 기존 결과, 원본과 같은 출력 경로를 거절합니다. 기존 한글 ROM에 덧씌우지 마세요. 이전 빌드 저장상태 호환성은 미검증입니다. 검증 한계와 번역 검토 범위는 RELEASE_NOTES_KO.md를 확인하세요.

이 묶음은 검토용 초안입니다. 최종 배포본이 아니며 ROM·폰트 PNG/TTF·에뮬레이터는 포함하지 않습니다.
''')
 release={'name':NAME,'date':'2026-10-05','version':'0.1.0-review047','status':'ASSEMBLED_APPLY_PENDING','artifact_policy':'development review for requesting user','distribution_eligible':False,'source':{'file':src.name,'bytes':src.stat().st_size,'sha256':sha(src)},'target':{'bytes':target.stat().st_size,'sha256':sha(target),'build':'dialogue_kr_poc_047'},'patch':{'file':PATCH,'bytes':(out/PATCH).stat().st_size,'sha256':sha(out/PATCH)},'verification_reports':reports,'ROM_free':True,'translation_review':{'registered_units':54,'draft':45,'technical_shared_units':9,'graphics_phrases':33,'CSV_sha256':sha(csvpath),'human_final_review':False,'global_corpus_complete':False},'tools':{'xdelta_version_output':version,'provenance':'First-game verified files copied read-only; xdelta3.2.0 Apache2.0','files_sha256':provenance},'unperformed':['whole natural play','all rooms/branches','PCM listening','current047 reset/save-state regression','hardware','final human language/terminology review','global corpus closure'],'old_savestate_compatibility':'Not verified','external_posted':False}
 helper.write_json(out/'release_report.json',release);helper.NAME=NAME;helper.PATCH=PATCH;helper.SOURCE_SHA=sha(src);helper.TARGET_SHA=sha(target)
 helper.check_apply(out,qa,src,target)
 release['status']='PASS';release['status_scope']='ROM-free packaging and actual Windows apply only; final distribution eligibility remains false';release['apply_verification']={'status':'PASS','checks':8,'unicode_space_paths':True,'byte_for_byte_target_match':True,'source_unchanged':True}
 helper.write_json(out/'release_report.json',release);helper.seal_package(out,qa,proof,src,target)
 for n,h in provenance.items():assert sha(vendor/n)==h
 assert sha(csvpath)==release['translation_review']['CSV_sha256']
if __name__=='__main__':main()