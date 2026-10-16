"""ROM-free review043 package; technical/apply evidence does not grant final release eligibility."""
from pathlib import Path
import json,hashlib,shutil,subprocess,csv
import release_apply_helpers as helper
R=Path(__file__).resolve().parents[1]
NAME='TinyToonAdventures2_KR_Review_043_20261005'
PATCH='TinyToonAdventures2_KR_Review_043_20261005.xdelta'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));src=R/source['path'];target=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';build=json.loads((target.parent/'build_report.json').read_text('utf-8'));assert sha(src)==source['sha256']==build['source_sha256'] and sha(target)==build['output_sha256']
 reports={}
 for name in ('train043_validation','engine_closure052','castle_currency053','castle_hud054_validation','train_sign051_session'):
  p=R/'qa/reports'/f'{name}.json';j=json.loads(p.read_text('utf-8'));assert j['status']=='PASS';reports[name]={'sha256':sha(p),'scope':j.get('status_scope',j.get('scope','See project handoff'))}
 csvrows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')));assert len(csvrows)==54 and sum(x['status']=='draft'for x in csvrows)==45
 out=R/'dist'/NAME;qa=R/'qa/apply/2편 개발판 한글 공백 적용 검증 20261005_001';proof=R/'qa/reports/review043_package_final.json';assert not any(p.exists()for p in (out,qa,proof))
 (out/'tools').mkdir(parents=True);(out/'licenses').mkdir()
 F=R.parent/'Tiny Toon Adventures';vendor=F/'dist/TinyToonAdventures_KR_Patch_v1.0_20261004';vendorfiles=['tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md'];provenance={n:sha(vendor/n)for n in vendorfiles}
 for n in vendorfiles:shutil.copy2(vendor/n,out/n)
 tool=out/'tools/xdelta3.exe';v=subprocess.run([str(tool),'-V'],capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);version=(v.stdout+v.stderr).decode('utf-8','replace');assert '3.2.0'in version and 'Apache'in version
 subprocess.run([str(tool),'-e','-9','-S','none','-A','-s',str(src),str(target),str(out/PATCH)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 values={'@SOURCE_SHA@':sha(src),'@TARGET_SHA@':sha(target),'@PATCH_NAME@':PATCH,'@PATCH_SHA@':sha(out/PATCH),'@XDELTA_SHA@':sha(tool)}
 text=(F/'workspace/release/apply_xdelta.ps1.in').read_text('utf-8').replace('524304','491536').replace('Tiny Toon Adventures 일본판','Tiny Toon Adventures 2 일본판').replace('타이니 툰 어드벤처스 한글 패치를','타이니툰 어드벤처 2 검토용 한글 패치를')
 for a,b in values.items():text=text.replace(a,b)
 helper.windows_text(out/'apply.ps1',text);cmd=(F/'workspace/release/apply.cmd.in').read_text('utf-8').replace('Tiny Toon Adventures Japan','Tiny Toon Adventures 2 Japan').replace('Tiny Toon Adventures (Japan).nes','Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes');helper.windows_text(out/'apply.cmd',cmd,bom=False)
 notes="""# 타이니툰 어드벤처 2 — 검토용 개발판043

이 패키지는 사용자 검토를 위한 개발판입니다. 최종 배포본/릴리즈 후보가 아닙니다. 전체 자연 플레이와 최종 사람 번역 검토는 끝나지 않았습니다.

타이틀·도입·홈·지도·매표소·성/놀이기구 안내·크레딧·게임 HUD·보너스·게임오버·기차 간판을 한글 초안으로 삽입했습니다. 생성형 이미지 타이틀/지도/매표소/게임오버와 Galmuri7 본문/작은 UI를 실제 ROM에 반영했습니다. 생성본 자체와 게임 화면의 검증을 구분했습니다.

등록 본문46개에는 실제 호출 기록이 있습니다. 등록54원천45draft/9기술공유는 전체 게임 완료율이 아닙니다. 기술공유9개는 숫자 변수/원천 macro이며 해당 이름·단어는 소비 글꼴에서 처리했습니다. 원천 Montana macro는 등록본문에서 참조되지 않는 범위만 확인했습니다.

PUSH START·회사/저작권표시·크레딧 영문 제작진 이름과 기차의 장식 M은 기존 작업 결정대로 보존했습니다. PAUSE/HOW TO CONTROL 후보 그래픽은 조사한 시연·마지막 장면·네 pause 경로에서 표시되지 않았으며 원본을 보존했습니다. 전역 미사용을 확정하지 않습니다. 이 보존 결정의 최종 사람 검토도 남아 있습니다.

원본으로부터 새 빌드·ExpectedWrites·독립 재빌드·실제 IPS 적용 결과 해시를 확인했습니다. Mesen2.1.1에서043 회귀6,005화면/637,476 IRQ 기록과 실제6장면을 확인했습니다. 추가로 자동시연18,000프레임, 마지막 엔진12,000프레임, 성 일반50/49 분기, 실제 성 HUD293화면/146,750 시점을 확인했습니다. 표본 수는 겹칠 수 있어 단순 합계로 전체 완주를 주장하지 않습니다.

금액/골드/크레딧/보너스 상태 초기화와 기차 체력 보충은 명시한 진단입니다. 정상 플레이의 수집/완주와 구분합니다. 성 HUD 획잘림 의심은 픽셀 대조로 해소됐고 불필요한 ROM 수정은 하지 않았습니다.

미수행: 전체 자연 플레이·모든 방/분기·오디오·reset/save-state 회귀·실기·최종 사람 번역/명칭 검토·전체 corpus 전역 폐쇄. 이전 빌드의 세이브 상태 호환성은 검증하지 않았으므로 새 ROM을 타이틀부터 시작해 검토하세요.

검토할 때에는 문구와 해당 장면, 사용한 원본/결과 해시, 시작 방법과 재현 입력을 함께 기록해 주세요. 이 문서는 웹이나 카페에 게시하지 않았습니다.

게임/캐릭터/상표의 권리는 각 권리자에게 있습니다. 비공식 팬 번역이며 ROM을 포함하지 않습니다. Galmuri와 xdelta 라이선스는 동봉했습니다.
"""
 (out/'RELEASE_NOTES_KO.md').write_text(notes,'utf-8')
 helper.windows_text(out/'README_적용방법.txt',f"""타이니툰 어드벤처 2 — 검토용 개발판043 (2026-10-05)

이 파일은 검토용 개발판이며 최종판이 아닙니다. ZIP을 모두 풀고 일본판 원본 NES ROM을 준비하세요. ROM은 포함하지 않습니다.

1. apply.cmd에 일본판 원본을 끌어 놓으세요.
2. 같은 폴더에 <원본명>_KR.nes가 생깁니다. 기존 파일은 덮어쓰지 않습니다.
3. 새 ROM을 타이틀부터 실행하여 검토하세요.

명령으로 결과 이름을 지정할 수도 있습니다:
apply.cmd "Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" "TinyToon2_KR_Review043.nes"

Windows x64/기본 Windows PowerShell이 필요합니다. Python이나 별도 패치 도구 설치는 필요 없습니다. 원본/패치/도구/결과 해시를 자동 검사합니다.

원본: 262160바이트 / SHA-256 {sha(src).upper()}
결과: 491536바이트 / SHA-256 {sha(target).upper()}

기존 한글 ROM에 덧씌우지 말고 위 원본에 적용하세요. 잘못된 판본과 기존 결과/손상 패치·도구는 거절합니다. 이전 빌드의 세이브 상태 호환성은 미검증입니다. 전체 플레이/실기/최종 번역 검토 범위는 RELEASE_NOTES_KO.md를 읽어 주세요.

원본 ROM·수정 ROM·폰트 PNG/TTF·에뮬레이터를 포함하지 않습니다.
""")
 release={'name':NAME,'date':'2026-10-05','version':'0.1.0-review043','status':'ASSEMBLED_APPLY_PENDING','artifact_policy':'development/PoC pre-release review candidate for requesting user; not release-candidate/final','distribution_eligible':False,'source':{'file':src.name,'bytes':src.stat().st_size,'sha256':sha(src)},'target':{'bytes':target.stat().st_size,'sha256':sha(target),'build':'dialogue_kr_poc_043'},'patch':{'file':PATCH,'bytes':(out/PATCH).stat().st_size,'sha256':sha(out/PATCH)},'verification_reports':reports,'ROM_free':True,'translation_review':{'registered_units':54,'draft':45,'technical_shared_units':9,'human_final_review':False,'global_corpus_complete':False},'tools':{'xdelta_version_output':version,'provenance':'First-game verified package copied read-only; actual3.2.0/Apache2.0','files_sha256':provenance},'unperformed':['whole natural play','all rooms/branches','audio','reset/save-state regression','hardware','final human language/terminology review','global corpus closure'],'old_savestate_compatibility':'Not verified','external_posted':False}
 helper.write_json(out/'release_report.json',release);helper.NAME=NAME;helper.PATCH=PATCH;helper.SOURCE_SHA=sha(src);helper.TARGET_SHA=sha(target)
 apply=helper.check_apply(out,qa,src,target);release['status']='PASS';release['status_scope']='ROM-free packaging and actualWindows apply only; finaldistribution eligibility remains false';release['apply_verification']={'status':'PASS','checks':8,'unicode_space_paths':True,'byte_for_byte_target_match':True,'source_unchanged':True};helper.write_json(out/'release_report.json',release);helper.seal_package(out,qa,proof,src,target)
 for n,h in provenance.items():assert sha(vendor/n)==h
if __name__=='__main__':main()
