"""062 ROM-free development package; actual Windows helper and extracted ZIP proof."""
from pathlib import Path
import json
import shutil
import subprocess
import zipfile
import release_apply_helpers132 as helpers
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def put(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def main():
    records.DATE = '2026-10-09'
    name = 'TinyToonAdventures2_KR_Text11_Candidate062_20261009'
    out = R / 'dist' / name
    archive = out.with_suffix('.zip')
    assert not out.exists() and not archive.exists()
    target = R / 'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes'
    source = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    frozen = json.loads((R / 'manifests/nonplay211_assets.json').read_text('utf-8'))
    for p, h in frozen['files'].items():
        assert sha(R / p) == h, p
    assert sha(target) == '7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce'
    assert sha(source) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    prior = R / 'dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009'
    proof = json.loads((R / 'qa/reports/ordinary11_206_package.json').read_text('utf-8'))
    out.mkdir()
    for p in ['apply.cmd', 'tools/xdelta3.exe', 'tools/README_xdelta3.md', 'tools/LICENSE_xdelta3.txt',
              'licenses/Galmuri_OFL.md', 'licenses/Galmuri11_v2.40.4_OFL.txt']:
        assert sha(prior / p) == proof['contents_sha256'][p]
        (out / p).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(prior / p, out / p)
    patchname = name + '.xdelta'
    patch = out / patchname
    subprocess.run([str(out / 'tools/xdelta3.exe'), '-e', '-s', str(source), str(target), str(patch)],
                   check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    assert sha(prior / 'apply.ps1') == proof['contents_sha256']['apply.ps1']
    script = (prior / 'apply.ps1').read_text('utf-8-sig')
    oldpatch = prior.name + '.xdelta'
    for before, after in [(oldpatch, patchname), (proof['contents_sha256'][oldpatch], sha(patch)),
                          (proof['ROM_sha256'], sha(target)), ('일반대사11px 후보059', '텍스트11px 후보062')]:
        assert before in script
        script = script.replace(before, after)
    assert '-ne 524304' in script and target.stat().st_size == 524304
    helpers.windows_text(out / 'apply.ps1', script)
    helpers.windows_text(out / 'README_적용방법.txt', f'''타이니툰 어드벤처2 일본판 — 텍스트11px 개발 후보062 (2026-10-09)

일본판 깨끗한 원본ROM을 apply.cmd에 드래그하거나 아래처럼 실행하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_Text11_Candidate062.nes"
원본262160바이트 SHA-256 {sha(source)}
결과524304바이트 SHA-256 {sha(target)}
기존 한글판이나 이전 후보ROM에 적용하지 마세요. 새 파일 경로로 출력하며 원본/기존파일을 덮어쓰지 않습니다.

오프닝9+일반33+크레딧3, 등록45문자열을11px로 확대한 개발 후보다.
HUD·정지 표지판 등 작은그림은 기존 크기를 유지했습니다.
오프닝6문단은 ‘깜짝 놀랄 거다!’를 한 줄로 묶고 ‘의문의 대부호로부터’를 오른쪽 정렬했습니다.
크레딧 한글12px·공백8px·영문16px 간격안은 개발후보이며 이름/KONAMI/법적 문자열은 그대로입니다.
숫자는8px 타일 간격으로 출력하며 글자 종류에 따라 실제 획높이는 다릅니다.

정적·동기CPU·독립ROM/IPS재빌드·Windows적용만 검증했습니다.
062 실제 에뮬레이터/플레이·CHR256 실제매핑·NMI/IRQ·글꼴수명·소거/전환·크레딧스크롤 가독성은 미검수입니다.
review/review.html은 ROM문자 디코딩PNG와 상단창 모형이며 실제062 게임 캡처가 아닙니다.
062는 미채택 개발후보이고 전체게임완료/전역텍스트발견/최종문체·명칭/폰트승인/공개배포를 뜻하지 않습니다.
현재 기준051, 이전 검증본과 원본·CSV·사용자Mesen/세이브는 보존했습니다.
HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 사용자결정대로 원문유지입니다.

실제 검수: 새062 ROM을 열어 초기화한 뒤 오프닝 완성/건너뛰기, 홈·선택·매표소 교환,
놀이기구 이름/규칙/가격/보유/입장, 성, 크레딧의 출력·대기·지우기·화면전환을 확인해주세요.
이전 후보 세이브스테이트 호환은 확인하지 않았습니다. 실제플레이 검수는 사용자담당입니다.
ROM없는 개인 개발검토 패키지입니다. 카페완성 작업기/외부게시를 진행하지 않았습니다.
''')
    (out / 'RELEASE_NOTES_KO.md').write_text('''# 텍스트11px 개발 후보062

059의 오프닝9+일반33개를 유지하고 크레딧3개도 확대했다. 제작진 이름과 권리 문자열은 같으며 글자 그림은 새11px로 바뀌었다. 크레딧106타일 공유글꼴, 줄별 포인터와 이벤트커서, 원래모드5/6·16px 줄간격을 사용한다. 첫페이지는 게임의NMI/렌더중지 루틴을 통해 직접NT전송하고 다음NMI를 기다린다. 진행문단은원래문자 호출수와carry/58대기/종료를유지해 최대62바이트 큐로 나눈다.

062 동기CPU: 기존42문자 검사/1042수치상태·1071skip·4320init·1556fallback·교환050보존10·놀이기구5창동시거주, 크레딧3글꼴복원·초기756셀·진행169/158호출·4000frame 원래스크롤상태 PASS. 원본ExpectedWrite/IPS/독립재빌드 exact. 실제화면·비동기NMI/IRQ·CHR256매핑·상단창소거·글꼴수명·전체플레이/최종사람검수는미수행이다. CPU스케줄의frame은실제에뮬레이터frame이아니다.

HUD·정지 등 작은그림/번역CSV/원문유지6건은 그대로다. 숫자의8px간격과일부글자획높이는별도다.060/061은CPU거부본으로보존하고062만개발검토후보로안내한다. 정식배포나최종채택을하지않았다.
''', 'utf-8')
    shutil.copytree(R / 'workspace/review/text11_211', out / 'review')
    proofs = [('text11_211_ordinary_CPU.json', 'ordinary_CPU.json'),
              ('credits11_211_CPU.json', 'credits_CPU.json'),
              ('text11_211_static_review.json', 'static_decode_validation.json')]
    for old, new in proofs:
        shutil.copyfile(R / 'qa/reports' / old, out / 'review' / new)
    put(out / 'scope_policy062.json', {'ROM_sha256': sha(target), 'registered11px': 45,
        'opening': 9, 'ordinary': 33, 'credits': 3, 'compact_bitmap_graphics_unchanged': True,
        'original_retentions': ['HOWTO', 'PAUSE', 'POW', 'RYO51', 'NT1C', 'diagnostic STAGE SELECT'],
        'source_CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'),
        'registered_inventory_global_game_completeness': False})
    put(out / 'release_report.json', {'name': name, 'date': '2026-10-09',
        'status': 'DEVELOPMENT_CPU_ONLY_TEXT11_062', 'ROM_free': True, 'distribution_eligible': False,
        'source': {'bytes': source.stat().st_size, 'sha256': sha(source)},
        'target': {'build': 'text11_candidate_062', 'bytes': target.stat().st_size, 'sha256': sha(target)},
        'patch': {'file': patchname, 'sha256': sha(patch)}, 'registered11px': 45,
        'runtime062': 'NOT_RUN', 'actual_game_captures_in_package': False, 'adopted': False})
    helpers.SOURCE_SHA, helpers.TARGET_SHA, helpers.PATCH = sha(source), sha(target), patchname
    qa = R / 'qa/release/text11_212_apply062'
    checks = helpers.check_apply(out, qa, source, target)
    shutil.copyfile(qa / 'apply_verification.json', out / 'Windows_apply_verification.json')
    files = sorted(p for p in out.rglob('*') if p.is_file())
    (out / 'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files), 'utf-8')
    files = sorted(p for p in out.rglob('*') if p.is_file())
    assert all(p.suffix.lower() not in ('.nes', '.mss', '.bin', '.ips', '.chr') for p in files)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in files:
            item = zipfile.ZipInfo(name + '/' + p.relative_to(out).as_posix(), (2026, 10, 9, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, p.read_bytes())
    extracted = qa / '최종 ZIP 추출'
    extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == {name + '/' + p.relative_to(out).as_posix() for p in files}
        for p in files:
            assert z.read(name + '/' + p.relative_to(out).as_posix()) == p.read_bytes()
        z.extractall(extracted)
    result = extracted / '062 결과.nes'
    final = helpers.apply(extracted / name, source, extracted, result)
    assert final['exit_code'] == 0 and result.read_bytes() == target.read_bytes(), final
    for p in files:
        assert (extracted / name / p.relative_to(out)).read_bytes() == p.read_bytes()
    hashfile = archive.with_suffix('.zip.sha256')
    hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n', 'ascii')
    evidence = R / 'qa/reports/text11_212_package.json'
    assert not evidence.exists()
    put(evidence, {'work': 212, 'status': 'PASS_ROMFREE_CPU_ONLY062_WINDOWS8_FINAL_ZIP_APPLY',
        'archive': archive.relative_to(R).as_posix(), 'archive_sha256': sha(archive),
        'ROM_sha256': sha(target), 'source_sha256': sha(source), 'files': len(files),
        'contents_sha256': {p.relative_to(out).as_posix(): sha(p) for p in files},
        'Windows_helper_checks': checks, 'final_ZIP_apply': final, 'final_output_sha256': sha(result),
        'source_unchanged': sha(source) == helpers.SOURCE_SHA, 'final_ZIP_payload_unchanged': True,
        'ROM_free': True, 'runtime062': 'NOT_RUN', 'adopted': False})
    body = f'''[등록45개11px062 적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}`. [적용방법](../dist/{name}/README_적용방법.txt), [정적 검토](../dist/{name}/review/review.html), [검사보고](../qa/reports/text11_212_package.json). 원본일본판262160바이트에서062524304바이트 SHA `{sha(target)}`로적용한다.ROM은패키지에없다.

Windows8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음)와최종ZIP 추출본실적용byte-exact PASS.한글·공백경로/ZIP CRC/정확한payload목록·적용후payload불변 PASS.총{len(files)}파일에45정적문자PNG·5창모형·CPU보고·라이선스·적용도구를포함했다.실제062캡처는포함하지않았다.

정적/CPU/재빌드근거는 [211](TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md)의정확한062에연결한다.실제062에뮬레이터·NMI/IRQ·CHR256·소거/전환·크레딧가독성·최종미감/문체·전체플레이검수는미수행이고062미채택개발후보다.원본·CSV·1편·기존성공/실패파일·사용자Mesen/세이브는수정하지않았다.작은그림과원문유지6건은그대로다.카페완성작업기/게시없음. [212매니페스트](../manifests/nonplay212_assets.json).

크레딧3개의정적062PNG를직접열어번역제목과이름/KONAMI/법적문구배치를검토했다.이직접이미지확인은정적자료에만해당한다.재현은기존출력을덮어쓰지않는새패키지/QA경로를사용한스크립트복제에서수행한다.사용자검수는새062 ROM 초기화후완성/건너뛰기/교환/설명·입장/크레딧을확인한다.'''
    records.seal(212, 'TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md', '062 등록45개11px 개발 적용패키지·Windows 실적용', body,
        '062 ROM없는 개발ZIP/Windows8/최종ZIP실적용 exact PASS.45문자·5모형·CPU·라이선스포함.실제062미수행·미채택,작은그림보존.',
        '197~212 고정근거·원본/CSV·프로젝트 링크를감사하고062와사용자실제검수목록을정본인계에반영한다.',
        [Path(__file__), evidence, archive, hashfile, qa / 'apply_verification.json', *files])
    print(json.dumps({'status': 'PASS', 'archive': archive.relative_to(R).as_posix(), 'sha256': sha(archive), 'files': len(files)}, indent=2))


if __name__ == '__main__':
    main()
