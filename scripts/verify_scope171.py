"""Verify final171 ZIP, execute real Windows apply, and record the resumed session."""
from pathlib import Path
import json, shutil, zipfile
from release_apply_helpers132 import apply as windows_apply
from seal_nonplay171 import R, sha, seal

def main():
    report = R / 'qa/reports/nonplay171_final.json'
    root = R / 'qa/apply/2편 개발049 범위확정 한글 공백 적용 검증 20261008_171'
    assert not report.exists() and not root.exists()
    pkg = json.loads((R / 'qa/reports/nonplay171_package.json').read_text('utf-8'))
    archive = R / pkg['archive']; assert sha(archive) == pkg['archive_sha256']
    root.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == 21
        for n in z.namelist(): assert (root / n).resolve().is_relative_to(root.resolve())
        z.extractall(root)
    extracted = root / archive.stem
    for f, h in pkg['contents_sha256'].items(): assert sha(extracted / f) == h
    sums = (extracted / 'SHA256.txt').read_text('utf-8').splitlines(); assert len(sums) == 20
    for line in sums:
        h, f = line.split('  ', 1); assert sha(extracted / f) == h
    release = json.loads((extracted / 'release_report.json').read_text('utf-8'))
    projection = extracted / release['scope_decision']['file']
    authoritative = R / release['scope_decision']['authoritative_record']
    assert sha(projection) == release['scope_decision']['sha256']
    assert sha(authoritative) == release['scope_decision']['authoritative_sha256']
    assert json.loads(projection.read_text('utf-8')) == json.loads(authoritative.read_text('utf-8'))
    review = R / 'workspace/review/nonplay049_20261007_170'
    for p in review.iterdir():
        if p.is_file(): assert (extracted / 'review' / p.name).read_bytes() == p.read_bytes()
    assert release['outside_population_summary']['explicit_user_retention'] == 3
    assert release['outside_population_summary']['connected_existing_title_retention'] == 1
    assert release['outside_population_summary']['still_unresolved_count'] == 3
    assert not release['distribution_eligible'] and not release['translation_review']['human_final_review']
    source_meta = json.loads((R / 'manifests/source_rom.json').read_text('utf-8'))
    original = R / source_meta['path']; source = root / '검증 원본 일본판.nes'; target = root / '새 결과 검토049.nes'
    assert sha(original) == source_meta['sha256']; shutil.copy2(original, source)
    observation = windows_apply(extracted, source, root, target)
    (root / 'apply_observation.json').write_text(json.dumps(observation, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    assert observation['exit_code'] == 0, observation
    rom = R / 'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    ssot = R / 'workspace/translation/text_ja.csv'
    assert target.read_bytes() == rom.read_bytes() and sha(target) == pkg['ROM_sha256']
    assert sha(source) == sha(original) == source_meta['sha256'] and sha(ssot) == pkg['SSOT_sha256']
    for f, h in pkg['contents_sha256'].items(): assert sha(extracted / f) == h
    assert sha(archive) == pkg['archive_sha256']
    result = {'work':171, 'status':'PASS_SCOPE_PACKAGE_FINAL_ZIP_ACTUAL_WINDOWS_APPLY',
        'archive':pkg['archive'], 'archive_sha256':sha(archive), 'ZIP_files':21, 'SHA256_manifest_files':20,
        'ROM_free':True, 'actual_final_ZIP_Windows_apply':observation, 'unicode_space_paths':True,
        'target_byte_exact':True, 'output_bytes':target.stat().st_size, 'source_payload_archive_unchanged':True,
        'exact_review170':True, 'scope_source_and_projection_hashes_verified':True, 'scope_JSON_equal':True,
        'approved_retention':['HOWTO','PAUSE','POW'], 'title_prompt_connected':True,
        'unresolved_candidates':['RYO51_PAGE17','NT1C','DIAGNOSTIC_STAGE_SELECT'],
        'ROM_sha256':sha(rom), 'SSOT_sha256':sha(ssot), 'actual_play_owner':'user',
        'new_emulator_or_gameplay':False, 'human_final_review':False, 'distribution_eligible':False}
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = f'''2026-10-08 사용자의 **‘다시 진행’**으로 비플레이 작업을 재개했다. 전날170 마감 지시는 이 재개 지시로 해제됐다. 실제 플레이 검수 사용자 담당과 자동 플레이 실험 금지는 그대로다.

[새 검토용171 ZIP](../{pkg['archive']})에169의 HOWTO·PAUSE·POW 이번 범위 원문 유지 결정과 최신170 검토자료를 반영했다. 기존168/170 자료를 보존했다. 패치·apply.cmd/ps1·xdelta3·도구/글꼴 라이선스는168과 바이트 동일하다. 등록54원천/45본문초안·9기술공유/33그림, 기존실제21PNG·정적4아틀라스를 변경하지 않았다. 발견7=명시적보존3+기존타이틀보존연결1+소비/의미 미확정3이다. 최종 전체문구/명칭/그림/배포승인은false다.

[최종 검증 보고](../{report.relative_to(R).as_posix()}): ZIP21파일 CRC/압축전후 내용과20파일 SHA목록을 검증했다. 최종ZIP을 새 한글·공백경로에 풀어 실제 Windows apply.cmd를 실행한 결과 exit0,499728바이트 전체가 현재049와 동일했다. 원본·패치·도구·ZIP·CSV 불변. 내장170 검토자료8파일이 기존 검증본과 바이트 동일하므로170의 PC/모바일 표시 근거를 재사용하며 브라우저 검사도 반복하지 않았다.

171v1의 원장/검토JSON raw SHA 동일 가정은 preflight에서 실패했다. 원장169는CRLF, 검토170의 파생 파일은LF였고 전체 JSON은 동일했다. 기존파일은 수정하지 않았다. v1스크립트/실패보고를 보존하고v2에서 원장SHA와검토manifest/SHA를각각확인한뒤 전체JSON동일성을 검사했다. 패키지의SHA는 실제 내장된검토파일을 가리키며 원장SHA는별도보존한다. 실패는게임/번역결함이 아니다.

정적/패키지 검증과 실제적용만 수행했다. 신규ROM재빌드·CPU하네스·에뮬레이터·직접게임장면·플레이·청음·사람최종검수 없음. 38cycles/page idle/RNG/CPU차이·163 RGB7326픽셀 실패/원인미확정, 전역원천폐쇄와미연결3후보, 전체플레이/최종말투·명칭·그림/실기·PCM은잔여다. HOWTO/PAUSE/POW 추가번역은이번범위원문유지결정으로닫았다. 카페완성작업기는전체완료후이며외부게시없음.

ZIP SHA `{sha(archive)}`, ROM `{sha(rom)}`, CSV `{sha(ssot)}`. 재현생성 `python scripts/package_scope171_v2.py`; 최종ZIP실제적용/봉인 `python scripts/verify_scope171.py`; 감사 `python scripts/audit_scoped_work.py --manifest manifests/nonplay171_assets.json --output qa/reports/nonplay171_session.json`. 기존출력을보호하므로재실행복제는새출력경로를사용한다. 변경:새171패키지/해시사이드카·생성/검증/날짜별봉인기·실패/성공보고·적용QA·인계/조사/계획/journal/canonical·manifest/audit. 각사용파일SHA는manifest다.'''
    files = [Path(__file__), R/'scripts/package_scope171.py', R/'scripts/package_scope171_v2.py',
        R/'scripts/release_apply_helpers132.py', R/'qa/reports/nonplay171_v1_preflight_failure.json',
        R/'qa/reports/nonplay171_package.json', report, archive, archive.with_name(archive.name + '.sha256'),
        authoritative, R/'workspace/translation/nonplay_inventory049_169.json',
        R/'qa/reports/nonplay170_final_stop.json', R/'qa/reports/nonplay168_final.json', rom, ssot]
    folder = R / 'dist' / archive.stem
    files.extend(p for p in folder.rglob('*') if p.is_file())
    files.extend(p for p in root.rglob('*') if p.is_file())
    seal(171, 'CURRENT049_SCOPE_APPLY_PACKAGE_171.md', '原文 보존 결정 반영·최신 적용 패키지171'.replace('原文','원문'), body,
        '사용자 재개.169보존3/타이틀연결1/미연결3와검토170을21파일ROM없는ZIP에동기화. 최종ZIP한글/공백실제Windows적용 byte-exact PASS. ROM/CSV불변·게임실행없음.',
        '미연결 RYO51/NT1C/진단STAGE SELECT의 현재 정적 근거와 범위 선택지를 묶고, 실제 소비 연결 또는 원천 보존에 필요한 결정 근거를 정리한다.', files)
    p = R / 'docs/HANDOFF.md'; text = p.read_text('utf-8')
    text = text.replace('2026-10-07 사용자의 “오늘은 마무리 하자”로 작업을 중단했다. 사용자 재개 지시 전 자동 재개하지 않는다. 오늘166..170의 비플레이 작업을 마감했다.',
        '2026-10-08 사용자의 “다시 진행”으로 비플레이 작업을 재개했다. 실제플레이는사용자담당이다. 전날166..170마감자료와이전패키지는보존하고171에서보존범위결정/검토자료를새적용묶음에반영했다.',1)
    text = text.replace('비플레이 잔여는168패키지문서의169/170반영, RYO51/NT1C/진단STAGE SELECT 소비·의미/전역corpus,',
        '171의최신적용패키지반영은완료했다. 비플레이 잔여는 RYO51/NT1C/진단STAGE SELECT 소비·의미/전역corpus,',1)
    text = text.replace('최신170 [비플레이 검토HTML]',
        '최신171 [ROM없는적용ZIP](../dist/TinyToonAdventures2_KR_Review_049_Scope171_20261008.zip)과 [패키지171 인계](CURRENT049_SCOPE_APPLY_PACKAGE_171.md)를따른다. 최신170 [비플레이 검토HTML]',1)
    p.write_text(text, 'utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'actual_final_ZIP_Windows_apply'}, indent=2))

if __name__ == '__main__': main()
