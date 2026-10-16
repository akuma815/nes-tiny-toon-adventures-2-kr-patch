"""ROM-free adopted049 review package; actual Windows apply/ZIP round trip."""
from pathlib import Path
import csv,hashlib,json,shutil,subprocess
import release_apply_helpers132 as helper
R=Path(__file__).resolve().parents[1]
NAME='TinyToonAdventures2_KR_Review_049_20261006';PATCH=NAME+'.xdelta'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));src=R/source['path'];target=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
 build=json.loads((target.parent/'build_report.json').read_text('utf-8'));assert sha(src)==source['sha256']==build['source_sha256'] and sha(target)==build['output_sha256']
 assert src.stat().st_size==262160 and target.stat().st_size==499728
 reports={}
 for name in ['clear128_validation','clear129_validation','pages130_validation','review049_validation131','review049_131_session']:
  p=R/'qa/reports'/f'{name}.json';j=json.loads(p.read_text('utf-8'));assert j['status']=={'clear128_validation': 'PASS_BOUNDED_CPU_BUILD_REAL_APPLY', 'clear129_validation': 'PASS_BOUNDED049_SHORTAGE_LIFETIME_AND_SUCCESS_BRANCH_WITH_RNG_DIFFERENCE', 'pages130_validation': 'PASS_BOUNDED_PAGE_REGRESSION_ADOPT_DEVELOPMENT049', 'review049_validation131': 'PASS', 'review049_131_session': 'PASS'}[name];reports[name]={'sha256':sha(p),'scope':j.get('scope','See frozen report and current handoff')}
 csvpath=R/'workspace/translation/text_ja.csv';rows=list(csv.DictReader(csvpath.open(encoding='utf-8-sig')));assert len(rows)==54 and sum(x['status']=='draft' for x in rows)==45 and sha(csvpath)==build['CSV_sha256']
 out=R/'dist'/NAME;qa=R/'qa/apply/2편 개발049 한글 공백 적용 검증 20261006_132';proof=R/'qa/reports/review049_package_final132.json'
 assert not any(p.exists() for p in (out,qa,proof))
 (out/'tools').mkdir(parents=True);(out/'licenses').mkdir()
 F=R.parent/'Tiny Toon Adventures';vendor=F/'dist/TinyToonAdventures_KR_Patch_v1.0_20261004'
 vendorfiles=['tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md'];provenance={n:sha(vendor/n) for n in vendorfiles}
 for n in vendorfiles:shutil.copy2(vendor/n,out/n)
 tool=out/'tools/xdelta3.exe';v=subprocess.run([str(tool),'-V'],capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);version=(v.stdout+v.stderr).decode('utf-8','replace');assert '3.2.0' in version and 'Apache' in version
 subprocess.run([str(tool),'-e','-9','-S','none','-A','-s',str(src),str(target),str(out/PATCH)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 values={'@SOURCE_SHA@':sha(src),'@TARGET_SHA@':sha(target),'@PATCH_NAME@':PATCH,'@PATCH_SHA@':sha(out/PATCH),'@XDELTA_SHA@':sha(tool)}
 text=(F/'workspace/release/apply_xdelta.ps1.in').read_text('utf-8');assert '524304' in text
 text=text.replace('524304','499728').replace('Tiny Toon Adventures 일본판','Tiny Toon Adventures 2 일본판').replace('타이니 툰 어드벤처스 한글 패치를 적용했습니다.','타이니툰 어드벤처 2 검토용049 패치를 적용했습니다.')
 for a,b in values.items():text=text.replace(a,b)
 assert not any(a in text for a in values);helper.windows_text(out/'apply.ps1',text)
 cmd=(F/'workspace/release/apply.cmd.in').read_text('utf-8').replace('Tiny Toon Adventures Japan','Tiny Toon Adventures 2 Japan').replace('Tiny Toon Adventures (Japan).nes','Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes');helper.windows_text(out/'apply.cmd',cmd,bom=False)
 notes='''# 타이니툰 어드벤처 2 — 검토용 개발본049

현재 개발본을 요청 사용자가 검토할 수 있게 만든 ROM 없는 차분 패치다. 최종 번역·명칭·그림의 사람 검토는 미완료이며 정식 공개 배포본이 아니다. 원본 일본판에만 적용하며 기존 한글판에 덧씌우지 않는다.

생성형 타이틀·지도·매표소·게임오버 그림, 등록45본문 초안과 놀이기구 안내·크레딧·HUD·보너스·기차 간판·시간 초과·다음 라운드·시작·정지 표지를 포함한다. 작은 안내 문구는 Galmuri7 비트맵이다. 등록54원천은45초안과9기술공유 항목이며 전체 전역corpus 비율이나 미번역 일본어9문장을 뜻하지 않는다.

047 이후 일반 티켓 부족 문장만 ‘아쉽지만 / 티켓이 부족해!’로 다듬었다. 전용226/227 폰트를 사용하며 기존 공유196/197과 macro 정의를 보존했다. 후보048은 대사 지우기 전에 폰트가 바뀌어 남은 글자가 섞이는 결함으로 거부했다. 049는 해당29/2B 문단의 native clear 전 활성폰트를 유지하고 clear 후 새폰트를 선택한다. 이전047/실패048 산출물과 실패 기록을 보존했다.

049의 정적 CPU3840 page/16 setup 계약, 전체 Expected Writes, 독립재빌드11파일과 실제IPS 적용이 검증됐다. 초기 일반티켓3 seed의 부족/다음 보유량과4 seed의4→0 결제/출발을 실제 실행했다. 부족41화면은 수정된 둘째 줄만 바뀌었고261화면은 그대로였다. 성공302화면은047과 전체PNG/PPU/OAM 동일했다. 추가로 타이틀·도입9문단·홈/매표소·성입구·seed 크레딧5짝1503화면의 전체PNG/PPU/OAM/매핑 회귀를 확인했다. 이 수치는 해당 입력/seed 범위이며 자연 통화획득이나 자연 엔딩·전게임완주 증거가 아니다.

helper에 page당38cycles가 추가돼 idle 난수용RAM22와 CPU A/P/일부 idle PC/IRQ 저장값이 달라졌다. 관측된 보호상태·픽셀 계약은 통과했지만 전체 CPU나 모든 게임 난수/입력 결과가 같다는 주장은 하지 않는다. 현재049 reset/save-state와 이전 빌드 저장상태 호환성은 아직 검증하지 않았으므로 새로 타이틀부터 실행한다.

ROM 없는049 번역 검토 HTML/ZIP은 별도 검토자료다. 실제PNG21장(역사043/045/046/047 14장과 현재049 7장)의 ROM/seed 출처를 구분했다. 본 패치ZIP에는 ROM·폰트 PNG/TTF·에뮬레이터·검토HTML이 들어 있지 않으며 Windows 적용 도구와 도구/폰트 라이선스를 포함한다.

한계: 전체 자연플레이·모든분기·전역 원천폐쇄·HOWTO/PAUSE/common POW 실제 소비경로·현재049 reset/save-state·실기·PCM청음·사람 문구/고유명사/그림 검토가 남았다. 과거 카트 두번째 마지막2F 시간초과를 완주 성공으로 표현하지 않는다. 이전 오디오 관측도 각 빌드 범위이며 PCM 동일성을 증명하지 않는다. PUSH START/회사·저작권/제작진 영문이름/기차M은 현재 개발결정 범위에서 보존했고 전역 영어 보존 승인이 아니다.

네이버 카페 작업기는 모든 작업이 끝난 뒤 작성한다. 현재 외부 게시를 하지 않았다. 게임·캐릭터·상표 권리는 각 권리자에게 있다. 이 묶음의 통과 상태는 포장과 실제 Windows 적용 검사이며 최종 배포 자격이나 사람 승인이 아니다.
'''
 (out/'RELEASE_NOTES_KO.md').write_text(notes,'utf-8')
 helper.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처 2 — 검토용 개발본049 (2026-10-06)

ZIP을 모두 풀고 일본판 원본 NES ROM을 준비하세요. ROM은 포함하지 않습니다.
1. apply.cmd에 일본판 원본을 끌어 놓으세요.
2. 같은 폴더에 <원본명>_KR.nes가 생깁니다. 기존 파일을 덮어쓰지 않습니다.
3. 새 ROM을 타이틀부터 실행해 검토하세요. 빌드 간 저장상태 호환성은 미검증입니다.

출력 이름을 지정할 수도 있습니다:
apply.cmd "Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" "TinyToon2_KR_Review049.nes"

Windows x64와 기본 Windows PowerShell이 필요합니다. Python이나 별도 패치 도구 설치는 필요 없습니다.
원본·패치·도구·결과 SHA를 자동 검사하며 기존 결과/동일 경로/잘못된 원본/이미 적용한 ROM/손상된 도구·패치를 거절합니다.
원본: 262160바이트 / SHA-256 {sha(src).upper()}
결과: 499728바이트 / SHA-256 {sha(target).upper()}

등록54원천/45초안/33그림 문구 검토용이며 최종 사람승인·전게임완주·정식배포는 미완료입니다.
049의 추가 page38cycles와 난수용RAM/CPU 차이 등 검증 한계는 RELEASE_NOTES_KO.md를 확인하세요.
''')
 release={'name':NAME,'date':'2026-10-06','version':'0.1.0-review049','status':'ASSEMBLED_APPLY_PENDING','artifact_policy':'development review for requesting user','distribution_eligible':False,'source':{'file':src.name,'bytes':src.stat().st_size,'sha256':sha(src)},'target':{'bytes':target.stat().st_size,'sha256':sha(target),'build':'dialogue_kr_poc_049'},'patch':{'file':PATCH,'bytes':(out/PATCH).stat().st_size,'sha256':sha(out/PATCH)},'verification_reports':reports,'ROM_free':True,'translation_review':{'registered_units':54,'draft':45,'technical_shared_units':9,'graphics_phrases':33,'CSV_sha256':sha(csvpath),'human_final_review':False,'global_corpus_complete':False},'tools':{'xdelta_version_output':version,'provenance':'First-game verified files copied read-only; xdelta3.2.0 Apache2.0','files_sha256':provenance},'unperformed':['whole natural play','all branches','global corpus closure','HOWTO/PAUSE/common POW native consumer','current049 reset/save-state regression','hardware','PCM listening','final human review'],'known_behavior_difference':'Additional38page cycles changes idle RAM22/CPU details; global random/gameplay identity unproved','old_savestate_compatibility':'Not verified','external_posted':False}
 helper.write_json(out/'release_report.json',release);helper.NAME=NAME;helper.PATCH=PATCH;helper.SOURCE_SHA=sha(src);helper.TARGET_SHA=sha(target)
 helper.check_apply(out,qa,src,target)
 release['status']='PASS';release['status_scope']='ROM-free packaging and actual Windows apply only; distribution eligibility/human approval false';release['apply_verification']={'status':'PASS','checks':8,'unicode_space_paths':True,'byte_for_byte_target_match':True,'source_unchanged':True}
 helper.write_json(out/'release_report.json',release);helper.seal_package(out,qa,proof,src,target)
 for n,h in provenance.items():assert sha(vendor/n)==h
 assert sha(csvpath)==build['CSV_sha256']
if __name__=='__main__':main()
