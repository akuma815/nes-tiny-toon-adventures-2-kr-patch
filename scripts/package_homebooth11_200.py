"""ROM-free057 CPU-only development package, actual Windows8/finalZIP apply proof."""
from pathlib import Path
import json
import shutil
import subprocess
import zipfile
import seal_nonplay171 as records
from seal_nonplay171 import R, sha
import release_apply_helpers132 as helpers


def put(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def main():
    records.DATE = '2026-10-09'
    name = 'TinyToonAdventures2_KR_HomeBooth11_Candidate057_20261009'
    out = R / 'dist' / name
    archive = out.with_suffix('.zip')
    assert not out.exists() and not archive.exists()
    target = R / 'build/homebooth11_candidate_057/TinyToon2_HomeBooth11_Candidate057.nes'
    source = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    cpu = R / 'qa/reports/homebooth11_199_CPU.json'
    v = json.loads(cpu.read_text('utf-8'))
    assert v['status'] == 'PASS_FINAL057_TYPED_SKIP_CLEAR_INIT_FONT_RETENTION_CPU'
    assert sha(target) == v['ROM_sha256'] == 'e2e388fe12d97c6a691e17174ba4cd368720788c140f3d60b4eccb70ef45ecef'
    assert sha(source) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    frozen = json.loads((R / 'manifests/nonplay199_assets.json').read_text('utf-8'))
    for f, h in frozen['files'].items():
        assert sha(R / f) == h, f
    old = R / 'dist/TinyToonAdventures2_KR_Opening11_PoC055_Layout6_20261009'
    proof = json.loads((R / 'qa/reports/opening11_195_package.json').read_text('utf-8'))
    out.mkdir()
    copied = ['apply.cmd', 'tools/xdelta3.exe', 'tools/README_xdelta3.md', 'tools/LICENSE_xdelta3.txt',
              'licenses/Galmuri_OFL.md', 'licenses/Galmuri11_v2.40.4_OFL.txt']
    for n in copied:
        assert sha(old / n) == proof['contents_sha256'][n]
        p = out / n
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(old / n, p)
    patchname = name + '.xdelta'
    patch = out / patchname
    subprocess.run([str(out / 'tools/xdelta3.exe'), '-e', '-s', str(source), str(target), str(patch)],
                   check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    assert sha(old / 'apply.ps1') == proof['contents_sha256']['apply.ps1']
    s = (old / 'apply.ps1').read_text('utf-8-sig')
    oldpatch = old.name + '.xdelta'
    for before, after in [(oldpatch, patchname), (proof['contents_sha256'][oldpatch], sha(patch)),
                          (proof['ROM_sha256'], sha(target)), ('오프닝11px PoC055', '홈·매표소11px 후보057')]:
        assert before in s
        s = s.replace(before, after)
    helpers.windows_text(out / 'apply.ps1', s)
    helpers.windows_text(out / 'README_적용방법.txt', f'''타이니툰 어드벤처2 일본판 — 홈·매표소11px 개발 후보057 (2026-10-09)

깨끗한 일본판 원본ROM을 apply.cmd에 드래그하거나 아래처럼 실행하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_HomeBooth11_Candidate057.nes"
원본262160바이트 SHA-256 {sha(source)}
결과499728바이트 SHA-256 {sha(target)}
기존 한글판에 덧씌우지 않습니다. 원본과 기존 출력은 덮어쓰지 않습니다.
결과 이름 생략 시 원본이름_KR.nes로 생성됩니다.

055 오프닝9개(사용자 수정6문단 포함)에 홈·선택명·매표소12개 대사11px를 추가했습니다.
HUD·정지 표지판 등 작은 그림 글자는 이전 크기입니다.
나머지 일반대사/놀이기구 안내21개와 크레딧3개는 아직8px입니다.
전체 텍스트11px 전환 완료본이나 정식 배포본이 아닙니다.

057은 최종6502 CPU/독립 재빌드/실제 패치 적용 검사만 통과한 개발 후보입니다.
새057 실제 Mesen 실행·화면·NMI/IRQ 전송 예산 검수는 미수행입니다.
이전055 실제 오프닝 근거를057 전체 실행 근거로 취급하지 않습니다.
review/review.html과 PNG는 ROM의 CHR/NT로 복원한 정적 배치이며 실제 캡처가 아닙니다.

사용자 검토 시 새057ROM을 열고 초기화해 홈 대사와 선택명, 매표소 환영/교환/부족/작별 대사를 확인하세요.
문장 완성, 출력 도중 버튼 건너뛰기, 창 지우기/다음 선택, 교환 후 대사 글꼴을 함께 확인할 대상입니다.
특히 두 줄 즉시 출력은 최대10165 CPU cycles여서 실제 인터럽트 시점 검수가 필요합니다.
기존 버전 저장상태 호환은 확인하지 않았습니다.

원본·051·055·이전 후보·CSV·사용자Mesen 설정/세이브를 보존했습니다.
HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 사용자 결정대로 원문 유지입니다.
최종 글꼴/문구/명칭 승인·전체 플레이·오디오/하드웨어/저장 호환·전역 도달성은 미완료입니다.
ROM이 없는 개인 개발검토 패키지입니다. 카페 완성 작업기나 외부 게시를 진행하지 않았습니다.
''')
    (out / 'RELEASE_NOTES_KO.md').write_text('''# 057 — 홈·매표소12개11px 개발 후보

055의 수정6문단과 오프닝9개를 보존하고12개 일반대사/선택명을168px 창 안에11px로 배치했다. 문구·번역CSV·HUD/정지 등 그림은 동일하다. 점진 출력과 즉시 출력925E를 함께 수정했고 범위 판정 전후P를 보존한다. 실패056은 별도로 보존했다.

최종CPU352 skip/4320 init/1556 fallback/050 매표소 글꼴 보존10조건/원래5행clear PASS. 독립ROM/IPS 재빌드와 원본ExpectedWrite/IPS 적용 PASS. 모든 정적PNG는 최종ROM CHR를 복원한 것으로 원천과 픽셀이 같다. 새057 실제 장면·NMI/IRQ 시점 검사는 미수행이다. 전체11px 전환은 미완료이며 일반21개와 크레딧3개가 남는다. 최종배포 대상이 아니다.
''', 'utf-8')
    shutil.copytree(R / 'workspace/review/homebooth11_199', out / 'review')
    shutil.copyfile(cpu, out / 'review/CPU_validation.json')
    shutil.copyfile(R / 'qa/reports/homebooth11_199_review.json', out / 'review/static_decode_validation.json')
    plan = json.loads((target.parent / 'homebooth11_plan.json').read_text('utf-8'))
    put(out / 'review/consumer_layout.json', {
        'ROM_sha256': sha(target), 'actual_capture': False, 'cell': [12, 16],
        'font_source': json.loads((R / 'workspace/fonts/galmuri11_candidate185/font_source.json').read_text('utf-8')),
        'pages': [{k: z[k] for k in ('entry_id', 'page', 'original_text', 'lines', 'font_bank', 'font_unique_tiles',
                                    'width_pixels', 'NT_top_origin')} for z in plan['pages']]})
    policy = json.loads((old / 'scope_policy055.json').read_text('utf-8'))
    policy['current_ROM_sha256'] = sha(target)
    policy['change_scope'] = '055 opening preserved; twelve lower home/booth11px entries. CPU-only057. Compact bitmap text remains original size.'
    policy.pop('user_page6_layout_request', None)
    put(out / 'scope_policy057.json', policy)
    put(out / 'release_report.json', {
        'name': name, 'date': '2026-10-09', 'status': 'DEVELOPMENT_CPU_ONLY_HOME_BOOTH11_057',
        'distribution_eligible': False, 'ROM_free': True,
        'source': {'bytes': source.stat().st_size, 'sha256': sha(source)},
        'target': {'build': 'homebooth11_candidate_057', 'bytes': target.stat().st_size, 'sha256': sha(target)},
        'patch': {'file': patchname, 'bytes': patch.stat().st_size, 'sha256': sha(patch)},
        'CPU_validation': {'file': 'review/CPU_validation.json', 'sha256': sha(cpu)},
        'runtime057': 'NOT_RUN', 'actual_game_captures_in_package': False,
        'remaining_registered_ordinary': 21, 'remaining_credits': 3,
        'global11px_fullplay_or_human_final_approval': False})
    helpers.PATCH = patchname
    helpers.TARGET_SHA = sha(target)
    helpers.SOURCE_SHA = sha(source)
    qa = R / 'qa/release/homebooth11_200_apply057'
    checks = helpers.check_apply(out, qa, source, target)
    shutil.copyfile(qa / 'apply_verification.json', out / 'Windows_apply_verification.json')
    files = sorted(p for p in out.rglob('*') if p.is_file())
    (out / 'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files), 'utf-8')
    files = sorted(p for p in out.rglob('*') if p.is_file())
    assert all(p.suffix.lower() not in ('.nes', '.mss', '.bin', '.ips') for p in files)
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
    result = extracted / '새057 결과.nes'
    final = helpers.apply(extracted / name, source, extracted, result)
    assert final['exit_code'] == 0 and result.read_bytes() == target.read_bytes(), final
    for p in files:
        assert (extracted / name / p.relative_to(out)).read_bytes() == p.read_bytes()
    hashfile = archive.with_suffix('.zip.sha256')
    hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n', 'ascii')
    evidence = R / 'qa/reports/homebooth11_200_package.json'
    assert not evidence.exists()
    put(evidence, {'work': 200, 'status': 'PASS_ROMFREE_CPU_ONLY057_WINDOWS8_FINAL_ZIP_APPLY',
                   'archive': archive.relative_to(R).as_posix(), 'archive_sha256': sha(archive),
                   'ROM_sha256': sha(target), 'source_sha256': sha(source), 'files': len(files),
                   'contents_sha256': {p.relative_to(out).as_posix(): sha(p) for p in files},
                   'Windows_helper_checks': checks, 'final_ZIP_apply': final, 'final_output_sha256': sha(result),
                   'source_unchanged': sha(source) == helpers.SOURCE_SHA, 'final_ZIP_payload_unchanged': True,
                   'ROM_free': True, 'runtime057': 'NOT_RUN', 'distribution_eligible': False})
    body = f'''[057 개발검토용 적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}`를 만들었다. [사용법](../dist/{name}/README_적용방법.txt), [정적 배치](../dist/{name}/review/review.html), [패키지 검사](../qa/reports/homebooth11_200_package.json). 원본 일본판에서057 전체 차분을 적용한다. ROM SHA `{sha(target)}`. 원본·055·051·실패056·CSV·1편·사용자Mesen/세이브는 보존한다.

정적·CPU는 [199](HOME_BOOTH11_CANDIDATE057_TYPED_SKIP_CPU_199.md)의 정확한057에 연결한다. 패키지는 ROM 없이{len(files)}파일, 폰트·xdelta 라이선스·12개 정적PNG·CPU·소비 배치·적용 도구를 포함한다. 실제 게임 캡처를 포함하지 않았으며057을 ‘CPU/빌드 검증 후 실제 실행 미수행’ 개발 후보로 표시했다. ROM 최종 채택/공개배포/전역11px/사람최종검수 성공으로 취급하지 않는다.

Windows8사례(정상/기존출력/원본=출력/동일크기 타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백 경로의 최종ZIP 추출본apply.cmd 적용이 byte-exact057 PASS. ZIP CRC·정확한 파일목록·전체payload·적용 후payload 불변·ROM-free PASS. 변경·해시는 [200매니페스트](../manifests/nonplay200_assets.json).

새 에뮬레이터·컨트롤러·플레이·실제장면/HTML 렌더 검증 없음. 057 홈/매표소의 실제 출력·대기·소거·선택·교환과2줄 즉시출력 NMI/IRQ 예산 검수가 남는다. 일반21개와 크레딧3개는8px다. HUD·정지 등 그림과 원문유지6건은 그대로다. 카페 완성 작업기/외부 게시 없음.

재현: 패키지 스크립트는 기존 경로를 덮어쓰지 않는다. 새 패키지명/QA 결과경로를 정한 복제에서 재현한다. 사용자 검토는 원본을apply.cmd에 넣고 새057을 초기화하여 홈·매표소 대사의 완성/건너뛰기/지우기/교환을 확인한다. 이를 이미 수행한 것으로 기록하지 않는다.'''
    records.seal(200, 'HOME_BOOTH11_CANDIDATE057_APPLY_PACKAGE_200.md', '홈·매표소11px057 개발 후보 패키지·Windows 실적용', body,
                 'ROM 없는 CPU후보057 패키지, Windows8/최종ZIP 실적용 exact PASS. 실제057 실행 미수행을 명시, 정적PNG/라이선스 포함.',
                 '나머지21개 일반대사의 실제 창 기하·동적숫자·상단 공유글꼴 용량을 검사해 다음 확대 설계를 고정한다.',
                 [Path(__file__), R / 'scripts/release_apply_helpers132.py', evidence, archive, hashfile,
                  qa / 'apply_verification.json', *files])
    f = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = f.read_text('utf-8').replace('현재 개발049 / 작업200', '기준051 / 오프닝055 / 홈·매표소057 CPU패키지 / 작업200', 1)
    f.write_text(s, 'utf-8')
    print(json.dumps({'status': 'PASS', 'archive': archive.relative_to(R).as_posix(),
                      'archive_sha256': sha(archive), 'files': len(files)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
