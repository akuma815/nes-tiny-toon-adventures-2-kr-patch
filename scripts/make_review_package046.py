"""Frozen ROM-free review046 package and actual Windows apply evidence."""
from pathlib import Path
import json,hashlib,shutil,subprocess,csv
import release_apply_helpers as helper
R=Path(__file__).resolve().parents[1]
NAME='TinyToonAdventures2_KR_Review_046_20261005'
PATCH=NAME+'.xdelta'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));src=R/source['path'];target=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes'
 build=json.loads((target.parent/'build_report.json').read_text('utf-8'));assert sha(src)==source['sha256']==build['source_sha256'] and sha(target)==build['output_sha256']
 assert src.stat().st_size==262160 and target.stat().st_size==499728
 reports={}
 for name in ('stop080_validation','stop081_regression','start077_validation','start078_regression','notices074_runtime','notices075_natural','review082_session'):
  p=R/'qa/reports'/f'{name}.json';j=json.loads(p.read_text('utf-8'));assert j['status']=='PASS';reports[name]={'sha256':sha(p),'scope':j.get('scope','See frozen report and project handoff')}
 csvpath=R/'workspace/translation/text_ja.csv';rows=list(csv.DictReader(csvpath.open(encoding='utf-8-sig')));assert len(rows)==54 and sum(x['status']=='draft'for x in rows)==45
 out=R/'dist'/NAME;qa=R/'qa/apply/2편 개발046 한글 공백 적용 검증 20261005_083';proof=R/'qa/reports/review046_package_final.json'
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
 notes='''# 타이니툰 어드벤처 2 — 검토용 개발본046

사용자 검토용 개발 초안이다. 최종 사람 번역·명칭 검토와 전체 자연 플레이는 완료되지 않았다. 이 묶음은 ROM 없는 차분 패치와 적용 도구이며 공개 최종판 자격을 뜻하지 않는다.

기존 타이틀·본문·지도·매표소·게임오버·HUD·기차 간판에 더해 다음 라운드!, 시간 초과!, 시작!, 정지 표지를 삽입했다. 원본 그래픽에서 실제 소비 뱅크와 타일·루틴을 연결한 뒤 전용 뱅크를 배정했다. 타이틀/지도/매표소/게임오버에는 생성형 이미지를 사용했고, 작은 안내 4개는 Galmuri7 비트맵으로 제작했다. 생성 이미지와 실제 게임 화면의 근거를 구분한다.

등록 원천54개는 번역 초안45개와 기술 공유9개다. 기술 공유는 숫자와 macro 등이며 미번역 일본어 문장9개라는 뜻이 아니다. 현재 번역 문구와 고유명사는 초안이다. 별도의 사람 검토 HTML/ZIP은 프로젝트 workspace/review에 있다.

현재046은 기차 STOP 표지의 실제 PPU 읽기20,560행, 302개 화면, 정확한 글자·RGB 변경 범위를 확인했다. 다른 세 코스의 852개 화면과 같은 시점 RAM/OAM/PPU/뱅크 매핑4260파일은045와 바이트 일치다. 시작 및 다음 라운드/시간 초과의 자연 진행 검증은 각각045/044의 동결 증거를 계승한다. 모든 수치를 전체 게임 완주 횟수로 해석하지 않는다.

원본부터의 Expected Writes, 독립 재빌드, IPS 실제 적용을 검증했다. 이번 묶음은 Windows apply.cmd 실제 실행8개 검사와 최종 ZIP 추출 재적용을 별도로 검증한다. 이전043 reset/save-state/오디오 조사는 역사적 증거다. 오디오 레지스터 순서와 DMC 원본 바이트 보존을 확인했으나146개 실제 출력 위상 차이가 남아 있어 PCM 동일성 또는 청음 통과를 주장하지 않는다.

PUSH START와 회사/저작권, 크레딧 영문 제작진 이름, 기차 M 표시는 현재 개발 결정에 따라 보존했다. PAUSE/HOW TO CONTROL 및 POW 후보는 조사된 경로에서 소비 연결이 확인되지 않았으며 전역 미사용이나 최종 사람 보존 승인을 뜻하지 않는다.

미수행: 전체 자연 플레이/모든 코스 완주·분기/실기/PCM 청음/현재046 reset-save-state 회귀/최종 사람 번역·명칭 검토/전역 corpus 폐쇄. 이전 빌드 저장상태 호환성은 미검증이므로 새 ROM을 타이틀부터 실행한다. 카트 첫 구간 자연 클리어는 확인했으나3개 구간 전체 완주를 주장하지 않는다.

네이버 카페 작업기는 모든 작업이 끝난 뒤 작성한다. 이 묶음과 자료는 외부에 게시하지 않았다. 게임·캐릭터·상표 권리는 각 권리자에게 있으며 Galmuri와 xdelta 라이선스를 동봉했다.
'''
 (out/'RELEASE_NOTES_KO.md').write_text(notes,'utf-8')
 helper.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처 2 — 검토용 개발본046 (2026-10-05)

ZIP을 모두 풀고 일본판 원본 NES ROM을 준비하세요. ROM은 포함하지 않습니다.

1. apply.cmd에 일본판 원본을 끌어 놓으세요.
2. 같은 폴더에 <원본명>_KR.nes가 생깁니다. 기존 파일을 덮어쓰지 않습니다.
3. 새 ROM을 타이틀부터 실행하여 검토하세요.

명령으로 출력 이름을 지정할 수 있습니다:
apply.cmd "Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" "TinyToon2_KR_Review046.nes"

Windows x64와 기본 Windows PowerShell이 필요합니다. Python이나 별도 패치 도구 설치는 필요 없습니다. 원본·패치·도구·결과의 해시를 자동 검사합니다.
원본: 262160바이트 / SHA-256 {sha(src).upper()}
결과: 499728바이트 / SHA-256 {sha(target).upper()}

잘못된 원본, 이미 적용한 ROM, 손상된 도구/패치, 기존 결과, 원본과 같은 출력 경로를 거절합니다. 기존 한글 ROM에 덧씌우지 마세요. 이전 빌드 저장상태 호환성은 미검증입니다. 검증 한계와 번역 검토 범위는 RELEASE_NOTES_KO.md를 확인하세요.

이 묶음은 검토용 초안입니다. 최종 배포본이 아니며 ROM·폰트 PNG/TTF·에뮬레이터는 포함하지 않습니다.
''')
 release={'name':NAME,'date':'2026-10-05','version':'0.1.0-review046','status':'ASSEMBLED_APPLY_PENDING','artifact_policy':'development review for requesting user','distribution_eligible':False,'source':{'file':src.name,'bytes':src.stat().st_size,'sha256':sha(src)},'target':{'bytes':target.stat().st_size,'sha256':sha(target),'build':'dialogue_kr_poc_046'},'patch':{'file':PATCH,'bytes':(out/PATCH).stat().st_size,'sha256':sha(out/PATCH)},'verification_reports':reports,'ROM_free':True,'translation_review':{'registered_units':54,'draft':45,'technical_shared_units':9,'graphics_phrases':33,'CSV_sha256':sha(csvpath),'human_final_review':False,'global_corpus_complete':False},'tools':{'xdelta_version_output':version,'provenance':'First-game verified files copied read-only; xdelta3.2.0 Apache2.0','files_sha256':provenance},'unperformed':['whole natural play','all rooms/branches','PCM listening','current046 reset/save-state regression','hardware','final human language/terminology review','global corpus closure'],'old_savestate_compatibility':'Not verified','external_posted':False}
 helper.write_json(out/'release_report.json',release);helper.NAME=NAME;helper.PATCH=PATCH;helper.SOURCE_SHA=sha(src);helper.TARGET_SHA=sha(target)
 helper.check_apply(out,qa,src,target)
 release['status']='PASS';release['status_scope']='ROM-free packaging and actual Windows apply only; final distribution eligibility remains false';release['apply_verification']={'status':'PASS','checks':8,'unicode_space_paths':True,'byte_for_byte_target_match':True,'source_unchanged':True}
 helper.write_json(out/'release_report.json',release);helper.seal_package(out,qa,proof,src,target)
 for n,h in provenance.items():assert sha(vendor/n)==h
 assert sha(csvpath)==release['translation_review']['CSV_sha256']
if __name__=='__main__':main()