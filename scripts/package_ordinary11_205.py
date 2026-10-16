"""ROM-free059 CPU-only development package, actual Windows8/finalZIP apply proof."""
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
    name = 'TinyToonAdventures2_KR_Ordinary11_Candidate059_20261009'
    out = R / 'dist' / name
    archive = out.with_suffix('.zip')
    assert not out.exists() and not archive.exists()
    target = R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes'
    source = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    cpu = R / 'qa/reports/ordinary11_204_CPU.json'
    v = json.loads(cpu.read_text('utf-8'))
    assert v['status'] == 'PASS_FINAL059_33_ORDINARY_AND_NINE_OPENING_CPU'
    assert sha(target) == v['ROM_sha256'] == '8b44d79b19c490dc6c5e2f3dcf73d08d1716ab981b62878067043a5600f59930'
    assert sha(source) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    frozen = json.loads((R / 'manifests/nonplay204_assets.json').read_text('utf-8'))
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
                          (proof['ROM_sha256'], sha(target)), ('오프닝11px PoC055', '일반대사11px 후보059')]:
        assert before in s
        s = s.replace(before, after)
    helpers.windows_text(out / 'apply.ps1', s)
    helpers.windows_text(out / 'README_적용방법.txt', f'''타이니툰 어드벤처2 일본판 — 일반대사11px 개발 후보059 (2026-10-09)

깨끗한 일본판 원본ROM을 apply.cmd에 드래그하거나 아래처럼 실행하세요.
  apply.cmd "원본 게임.nes" "TinyToon2_Ordinary11_Candidate059.nes"
원본262160바이트 SHA-256 {sha(source)}
결과524304바이트 SHA-256 {sha(target)}
기존 한글판에 덧씌우지 않습니다. 원본과 기존 출력은 덮어쓰지 않습니다.
결과 이름 생략 시 원본이름_KR.nes로 생성됩니다.

055 오프닝9개(사용자 수정6문단 포함)에 일반대사33개의11px 후보를 추가했습니다.
홈·선택명·매표소·성 입구·놀이기구 이름/설명·요금/보유티켓/부족/출발 문구가 대상입니다.
HUD·정지 표지판 등 작은 그림 글자는 이전 크기입니다.
크레딧3개는 아직8px입니다. 등록42개 확대 후보이지 전게임 텍스트 인벤토리 완결 주장은 아닙니다.
전체 텍스트11px 전환 완료본이나 정식 배포본이 아닙니다.

059은 최종6502 CPU/독립 재빌드/실제 패치 적용 검사만 통과한 개발 후보입니다.
새059 실제 Mesen 실행·화면·NMI/IRQ 전송 예산 검수는 미수행입니다.
이전055 실제 오프닝 근거를059 전체 실행 근거로 취급하지 않습니다.
review/review.html과 PNG는 ROM의 CHR/NT로 복원한 정적 배치이며 실제 캡처가 아닙니다.

사용자 검토 시 새059ROM을 열고 초기화해 홈/선택명, 매표소 교환 후 대사, 성 입구, 놀이기구 안내/요금/보유/시작 문구를 확인하세요.
문장 완성, 출력 도중 버튼 건너뛰기, 창 지우기/다음 선택, 교환 후 대사 글꼴을 함께 확인할 대상입니다.
놀이기구별 이름+설명은 같은 글꼴을 공유하고 이름 칸 아래 테두리를 한 타일 내렸습니다.
숫자는 같은Galmuri11 글꼴의8px 간격으로 원래 값을 보존합니다. 모든 숫자 잉크가11px 높이라는 뜻은 아닙니다.
CHR를232→256KiB로 확장했으므로 실제 매핑과NMI/IRQ 전송 시점도 확인할 대상입니다.
기존 버전 저장상태 호환은 확인하지 않았습니다.

원본·051·055·이전 후보·CSV·사용자Mesen 설정/세이브를 보존했습니다.
HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 사용자 결정대로 원문 유지입니다.
최종 글꼴/문구/명칭 승인·전체 플레이·오디오/하드웨어/저장 호환·전역 도달성은 미완료입니다.
ROM이 없는 개인 개발검토 패키지입니다. 카페 완성 작업기나 외부 게시를 진행하지 않았습니다.
''')
    (out / 'RELEASE_NOTES_KO.md').write_text('''# 059 — 일반대사33개11px 개발 후보

055의 수정6문단과 오프닝9개를 보존하고 일반33개를11px로 배치했다. 문구·번역CSV·HUD/정지 등 그림은 동일하다. 놀이기구별 이름+설명5개 공유 글꼴, 이름160/설명184/하단168px, 이름칸 아래 테두리 한 타일 확장을 적용했다. 공통 가격/시작196과 보유254를 분리하고 숫자는8px 타일 경계에 고정한다. 실패056/058은 별도 보존했다.

최종CPU33문단/1042변수상태(F8천값·FA6×2)/1071skip/4320init/1556fallback/050보존10/카드5쌍 동시거주 PASS. 독립ROM/IPS·원본ExpectedWrite·IPS exact. PNG는 최종ROM/CPU의 정적 복원 또는 원래NT 기하로 만든 모형이며 실제059 실행 캡처가 아니다. 새059 Mesen/CHR256 매핑/NMI/IRQ/소거·화면전환 검수는 미수행이다. 크레딧3개는8px이고 전체11px/사람 최종승인/전체플레이는 미완료다.
''', 'utf-8')
    shutil.copytree(R / 'workspace/review/ordinary11_204', out / 'review')
    shutil.copyfile(cpu, out / 'review/CPU_validation.json')
    shutil.copyfile(R / 'qa/reports/ordinary11_204_static_review.json', out / 'review/static_decode_validation.json')
    plan = json.loads((target.parent / 'ordinary11_plan.json').read_text('utf-8'))
    put(out / 'review/consumer_layout.json', {
        'ROM_sha256': sha(target), 'actual_capture': False, 'cell': [12, 16],
        'font_source': json.loads((R / 'workspace/fonts/galmuri11_candidate185/font_source.json').read_text('utf-8')),
        'pages': [{k: z[k] for k in ('entry_id', 'page', 'original_text', 'font_bank', 'font_slots_allocated',
                                    'width_pixels', 'NT_top_origin')} for z in plan['pages']]})
    policy = json.loads((old / 'scope_policy055.json').read_text('utf-8'))
    policy['current_ROM_sha256'] = sha(target)
    policy['change_scope'] = '055 opening9 preserved;33 ordinary11px entries, five title/rule shared fonts and title frame resized. CPU-only059; compact bitmap text unchanged.'
    policy.pop('user_page6_layout_request', None)
    put(out / 'scope_policy059.json', policy)
    put(out / 'release_report.json', {
        'name': name, 'date': '2026-10-09', 'status': 'DEVELOPMENT_CPU_ONLY_ORDINARY11_059',
        'distribution_eligible': False, 'ROM_free': True,
        'source': {'bytes': source.stat().st_size, 'sha256': sha(source)},
        'target': {'build': 'ordinary11_candidate_059', 'bytes': target.stat().st_size, 'sha256': sha(target)},
        'patch': {'file': patchname, 'bytes': patch.stat().st_size, 'sha256': sha(patch)},
        'CPU_validation': {'file': 'review/CPU_validation.json', 'sha256': sha(cpu)},
        'runtime059': 'NOT_RUN', 'actual_game_captures_in_package': False,
        'ordinary_entries_built_CPU': 33, 'opening_entries_preserved': 9, 'remaining_credits': 3,
        'global11px_fullplay_or_human_final_approval': False})
    helpers.PATCH = patchname
    helpers.TARGET_SHA = sha(target)
    helpers.SOURCE_SHA = sha(source)
    qa = R / 'qa/release/ordinary11_205_apply059'
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
    result = extracted / '새059 결과.nes'
    final = helpers.apply(extracted / name, source, extracted, result)
    assert final['exit_code'] == 0 and result.read_bytes() == target.read_bytes(), final
    for p in files:
        assert (extracted / name / p.relative_to(out)).read_bytes() == p.read_bytes()
    hashfile = archive.with_suffix('.zip.sha256')
    hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n', 'ascii')
    evidence = R / 'qa/reports/ordinary11_205_package.json'
    assert not evidence.exists()
    put(evidence, {'work': 205, 'status': 'PASS_ROMFREE_CPU_ONLY059_WINDOWS8_FINAL_ZIP_APPLY',
                   'archive': archive.relative_to(R).as_posix(), 'archive_sha256': sha(archive),
                   'ROM_sha256': sha(target), 'source_sha256': sha(source), 'files': len(files),
                   'contents_sha256': {p.relative_to(out).as_posix(): sha(p) for p in files},
                   'Windows_helper_checks': checks, 'final_ZIP_apply': final, 'final_output_sha256': sha(result),
                   'source_unchanged': sha(source) == helpers.SOURCE_SHA, 'final_ZIP_payload_unchanged': True,
                   'ROM_free': True, 'runtime059': 'NOT_RUN', 'distribution_eligible': False})
    body = f'''[059 개발검토용 적용ZIP](../dist/{archive.name}) SHA `{sha(archive)}`를 만들었다. [사용법](../dist/{name}/README_적용방법.txt), [정적 배치와 카드 모형](../dist/{name}/review/review.html), [패키지 검사](../qa/reports/ordinary11_205_package.json). 원본 일본판에서059 전체 차분을 적용한다. ROM SHA `{sha(target)}`. 원본·055·051·057·실패056/058·CSV·1편·사용자Mesen/세이브는 보존한다.

정적·CPU는 [204](ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md)의 정확한059에 연결한다. 패키지는 ROM 없이{len(files)}파일, 폰트·xdelta 라이선스·33개 정적문자PNG·5개 상단창 모형·CPU·소비 배치·적용 도구를 포함한다. 실제 게임 캡처를 포함하지 않았으며059을 ‘CPU/빌드 검증 후 실제 실행 미수행’ 개발 후보로 표시했다. ROM 최종 채택/공개배포/전역11px/사람최종검수 성공으로 취급하지 않는다.

Windows8사례(정상/기존출력/원본=출력/동일크기 타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백 경로의 최종ZIP 추출본apply.cmd 적용이 byte-exact059 PASS. ZIP CRC·정확한 파일목록·전체payload·적용 후payload 불변·ROM-free PASS. 변경·해시는 [205매니페스트](../manifests/nonplay205_assets.json).

새 에뮬레이터·컨트롤러·플레이·실제장면/HTML 렌더 검증 없음. 059 실제 출력·대기·소거·선택·교환·상단창 테두리/동시거주·CHR256 매핑·NMI/IRQ 예산 검수가 남는다. 크레딧3개는8px다. HUD·정지 등 그림과 원문유지6건은 그대로다. 카페 완성 작업기/외부 게시 없음.

재현: 패키지 스크립트는 기존 경로를 덮어쓰지 않는다. 새 패키지명/QA 결과경로를 정한 복제에서 재현한다. 사용자 검토는 원본을apply.cmd에 넣고 새059을 초기화하여 홈·매표소 대사의 완성/건너뛰기/지우기/교환을 확인한다. 이를 이미 수행한 것으로 기록하지 않는다.'''
    records.seal(205, 'ORDINARY11_CANDIDATE059_APPLY_PACKAGE_205.md', '일반대사11px059 개발 후보 패키지·Windows 실적용', body,
                 'ROM 없는 CPU후보059 패키지, Windows8/최종ZIP 실적용 exact PASS. 실제059 실행 미수행을 명시, 정적PNG/라이선스 포함.',
                 '197~205 고정근거와 원본/링크를 감사하고 최신059 후보와 남은 크레딧을 정본 인계에 반영한다.',
                 [Path(__file__), R / 'scripts/release_apply_helpers132.py', evidence, archive, hashfile,
                  qa / 'apply_verification.json', *files])
    f = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = f.read_text('utf-8').replace('현재 개발049 / 작업205', '기준051 / 오프닝055 / 일반33개059 CPU패키지 / 작업205', 1)
    f.write_text(s, 'utf-8')
    print(json.dumps({'status': 'PASS', 'archive': archive.relative_to(R).as_posix(),
                      'archive_sha256': sha(archive), 'files': len(files)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
