"""Reconcile latest user-requested opening055 evidence and canonical resume docs."""
from pathlib import Path
import json
import re
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    checks = {}
    for n in range(188, 196):
        p = R / f'manifests/nonplay{n}_assets.json'
        d = json.loads(p.read_text('utf-8'))
        for f, h in d['files'].items():
            assert sha(R / f) == h, f
        checks[str(n)] = {'manifest_sha256': sha(p), 'frozen_files': len(d['files']), 'all_exact': True}
    package = json.loads((R / 'qa/reports/opening11_195_package.json').read_text('utf-8'))
    assert package['status'] == 'PASS_ROMFREE_OPENING055_WINDOWS8_FINAL_ZIP_APPLY'
    assert sha(R / package['archive']) == package['archive_sha256']
    rom = R / 'build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes'
    assert sha(rom) == package['ROM_sha256']
    assert rom.read_bytes() == (R / 'build/opening11_193_rebuild055/TinyToon2_Opening11_PoC055.nes').read_bytes()
    source = json.loads((R / 'manifests/source_rom.json').read_text('utf-8'))
    assert sha(R / source['path']) == package['source_sha256'] == source['sha256']
    csv_sha = sha(R / 'workspace/translation/text_ja.csv')
    assert csv_sha == '43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    runtime = json.loads((R / 'qa/reports/opening11_194_validation.json').read_text('utf-8'))
    assert runtime['status'] == 'PASS_OPENING11_055_NINE_PAGES_THREE_LOOPS_USER_PAGE6_LAYOUT'
    audit = json.loads((R / 'qa/reports/opening11_195_audit.json').read_text('utf-8'))
    assert audit['status'] == 'PASS_PROJECT_ASSETS_SOURCE_AND_LOCAL_LINKS'
    report = R / 'qa/reports/opening11_196_integrity.json'
    assert not report.exists()
    report.write_text(json.dumps({
        'work': 196, 'status': 'PASS_FROZEN_188_195_CURRENT_OPENING055_RECONCILIATION',
        'manifests': checks, 'ROM055_sha256': sha(rom),
        'archive_sha256': package['archive_sha256'], 'source_sha256': source['sha256'],
        'CSV_sha256': csv_sha, 'source_and_first_game_refs_unchanged': True,
        'latest_opening_review': 'opening11_poc_055', 'stable_development': 'dialogue_kr_poc_051',
        'home054': 'CPU-only prototype, unadopted, not included in055',
        'project_local_links_audit': 'qa/reports/opening11_195_audit.json',
        'new_runtime': False,
        'limits': ['055 runtime evidence is194; no new055 Start/train tests',
                   'Human font approval and whole-game11px conversion incomplete',
                   'One expired historical external plugin-cache link separately reported']
    }, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    next_action = '055를 기준으로 홈 대표 한 줄의 11px 후보를 재구성하고, 실제 소비 경로와 연결해 검증한다.'
    body = f'''사용자 요청인 6문단 줄바꿈과 서명 오른쪽 정렬을 반영한 **055**를 최신 오프닝 검토본으로 정리했다. [실제 수정 화면](../workspace/review/opening11_194/page06_11px.png), [053/055 비교](../workspace/review/opening11_194/review.html), [ROM 없는 적용 ZIP](../{package['archive']}).

6문단은 `친구들도 데려와!` / `깜짝 놀랄 거다!` / 빈 줄 / 오른쪽 정렬 `의문의 대부호로부터`로 배치했다. Galmuri11 글자 모양은 유지했다. 원문·번역 CSV는 바꾸지 않았다. 053 대비 변경은 해당 문단의 전용 문자열·글꼴에 속한 508바이트이며 다른 8문단과 코드가 동일하다. 홈054는 CPU 검증 후보로 보존하며 055에 포함하지 않았다.

정적·빌드·CPU: [193](OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md)의 독립 ROM/IPS 재빌드와 9문단 최종6502 검증 PASS. 이번196에서는188~195의 고정 매니페스트를 전부 대조했다. [무결성 보고](../qa/reports/opening11_196_integrity.json), [변경 파일/해시 목록](../manifests/nonplay196_assets.json).

실제 에뮬레이터·장면: [194](OPENING11_PAGE6_LAYOUT_POC055_RUNTIME_194.md)의 새055 오프닝9000프레임에서9문단 각3회, 출력·대기·지우기2167 RGB표본과3024 상하타일 소비·30회 소거 PASS. 같은 프레임의053/055 비교2318쌍 중2086 전체PNG 동일,232는6문단 글자 영역 안에서만 달라졌다. 실제6문단 PNG를 직접 확인했다. 이 보고196의 새 에뮬레이터 실행은 없다.

패키지·적용: [195](OPENING11_PAGE6_LAYOUT_POC055_PACKAGE_195.md)의38파일 ROM 없는 ZIP, 실제Windows 적용8사례·최종ZIP 추출 후 적용 byte-exact PASS. ROM SHA `{sha(rom)}`, ZIP SHA `{package['archive_sha256']}`. [195 감사](../qa/reports/opening11_195_audit.json)는46개 고정 파일·2573 유효 링크·원본/1편 보존 PASS. 과거 외부3.3 스킬 캐시 링크1건 만료는 별도 보고했으며 프로젝트 로컬 누락 링크는 없다.

기준 개발본051, 이전053/054, 원본, CSV, 1편, 기존 검증 자료, 사용자Mesen 설정·세이브를 보존했다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 사용자 결정대로 원문 유지다. README·최신 HANDOFF·작업 계획의 재개 위치를055로 갱신하고 오늘 인계/journal을 추가했다.

제한: 전체 텍스트11px 전환·최종 사람의 글꼴/문체 승인·전체 플레이·오디오/하드웨어/저장 호환·전역 도달성은 미완료다. 055 Start/기차 검증은 새로 실행하지 않았고053 기록을055 결과로 간주하지 않는다. 홈054 실제 실행과 HTML 브라우저 렌더 QA는 미수행이다. 카페 완성 작업기 및 외부 게시도 아직 진행하지 않았다.

재현: `python scripts/audit_project_links184.py --manifest manifests/nonplay196_assets.json --output qa/reports/<new-audit-name>.json`. 기존 고정 보고를 덮어쓰지 않는다. 재개 기준은 아래 최신 HANDOFF를 따른다.'''
    records.seal(196, 'OPENING11_POC055_CURRENT_HANDOFF_AUDIT_196.md',
                 '요청6문단 수정055 패키지·근거·최신 인계 감사', body,
                 '6문단 줄묶음·오른쪽 서명055 검증/패키지 완료. 188~195 고정 해시와 원본/1편 보존 PASS. 기준051·최신 오프닝055·홈054 CPU후보를 구분했다.',
                 next_action,
                 [Path(__file__), report, R / 'qa/reports/opening11_195_audit.json',
                  *[R / f'manifests/nonplay{n}_assets.json' for n in range(188, 196)]])
    p = R / 'docs/HANDOFF.md'
    old = p.read_text('utf-8')
    marker = '아래는이전작업의역사기록이며상단재개위치를우선한다.'
    assert marker in old
    tail = old.split(marker, 1)[1]
    head = f'''# 진행 중 — 2026-10-09, 작업196 완료

최신 오프닝 검토본은 **opening11_poc_055**다. 사용자 요청대로 6문단의 ‘깜짝 놀랄 거다!’를 아래 줄로 묶고 ‘의문의 대부호로부터’를 한 줄 오른쪽 정렬로 바꿨다. 1행 ‘친구들도 데려와!’, 2행 ‘깜짝 놀랄 거다!’, 3행 빈 줄, 4행 오른쪽 서명이다. 글자 모양은 기존 Galmuri11을 유지했다. [실제 6문단 PNG](../workspace/review/opening11_194/page06_11px.png), [수정 전053/후055 비교](../workspace/review/opening11_194/review.html).

**기준 개발본 dialogue_kr_poc_051은 유지**한다. 055는 오프닝9문단만11px로 바꾼 시험판이며 053을 기반으로 6문단의 전용 문자열·글꼴508바이트만 수정했다. [055 ROM](../build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes) SHA `{sha(rom)}`. [빌드·CPU193](OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md), [실제 검증194](OPENING11_PAGE6_LAYOUT_POC055_RUNTIME_194.md).

055 실제 오프닝9000프레임에서9문단 각3회,2167 출력·대기·소거RGB표본,3024 상하타일 소비,30회 초기화 소거 PASS. 053과 같은 프레임2318쌍을 비교해2086 전체PNG 동일,232는6문단 글자 영역에만 차이가 있었다. 055 Start/기차는 새로 검증하지 않았다. 사람의 최종 글꼴 승인과 전체 텍스트11px 전환은 남아 있으며 실제 플레이는 사용자 담당이다.

[055 ROM 없는 적용 ZIP195](../{package['archive']})은38파일, Windows8사례와 최종ZIP 실제 적용 byte-exact PASS. [패키지 인계195](OPENING11_PAGE6_LAYOUT_POC055_PACKAGE_195.md), [고정 근거 감사196](OPENING11_POC055_CURRENT_HANDOFF_AUDIT_196.md). 기존 [053 ZIP188](../dist/TinyToonAdventures2_KR_Opening11_PoC053_20261009.zip)과 [051 검토 ZIP](../dist/TinyToonAdventures2_KR_Review_051_MovingStop_20261008.zip)은 각 버전의 역사 자료로 보존했다.

[홈054 후보191](HOME11_SINGLE_LINE_CANDIDATE054_191.md)는 정적·빌드·CPU만 PASS인 미채택 후보다. 실제 실행 미수행이며055에 포함하지 않았다. [소비 경로 정정192](HOME11_CONSUMER_AND_PAGE6_LAYOUT_CHOICE_192.md), [전체11px 계획190](GLOBAL_TEXT11_NEXT_CONSUMER_PLAN_190.md)을 다음 작업에서 따른다. 054를 EndFrame 뱅크 값만으로 잘못된 후크라고 판정하지 않는다.

원본·CSV·1편·051/053/054·기존 QA·사용자Mesen 설정과 세이브를 보존했다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 원문 유지다. 카페 완성 작업기는 전체 작업 후 작성하며 외부 게시하지 않는다. 전체 플레이/최종 미감·문체/오디오·하드웨어·저장 호환/전역 도달성은 미완료다.

**다음 작업 하나: {next_action}** [오늘 인계](HANDOFF_2026-10-09.md), [오늘 journal](journal/2026-10-09.md), [조사](SURVEY.md), [계획](LOCALIZATION_WORK_PLAN.md).

{marker}'''
    p.write_text(head + tail, 'utf-8')
    p = R / 'README.md'
    s = p.read_text('utf-8')
    s = re.sub(r'^> \*\*.*?\*\*', '> **2026-10-09 작업196 / 기준051 유지 / 최신 오프닝11px055: 6문단 줄묶음·오른쪽 서명 검증 및 패키지 완료 / 홈054 CPU후보**', s, count=1)
    block = f'''## 최신 오프닝11px 검토본 — 055

6문단의 ‘깜짝 놀랄 거다!’를 아래 줄로 묶고 ‘의문의 대부호로부터’를 한 줄 오른쪽 정렬로 수정했다. [실제 수정 화면](workspace/review/opening11_194/page06_11px.png), [비교 자료](workspace/review/opening11_194/review.html), [ROM 없는 적용 ZIP195]({package['archive']}), [최신 인계 감사196](docs/OPENING11_POC055_CURRENT_HANDOFF_AUDIT_196.md). 오프닝9문단3회·출력/대기/소거와 실제Windows 패치 적용 PASS. 전체 텍스트11px 전환과 사용자 플레이 검수는 남아 있다. 기준051과 홈054 CPU후보는 별도로 보존한다.

'''
    assert '## 최신 오프닝11px 검토본 — 055' not in s
    s = s.replace('# 현재 개발본 — 작업184 / 051', block + '# 현재 개발본 — 작업184 / 051', 1)
    p.write_text(s, 'utf-8')
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = p.read_text('utf-8')
    s = re.sub(r'^> \*\*.*?\*\*', '> **2026-10-09 작업196 / 기준051 / 최신 오프닝055 검증·패키지 완료 / 전체11px 전환 진행 중. 실제 플레이 사용자 담당.**', s, count=1)
    notice = '\n\n현재196: 사용자 요청6문단 수정055가 최신 오프닝 검토본이다. [근거·인계 감사196](OPENING11_POC055_CURRENT_HANDOFF_AUDIT_196.md). 기준051 유지, 홈054는 CPU후보·실제 실행 미수행이며055에 포함하지 않았다. 아래 각 계획의 당시 버전·수량은 역사 기록이다.'
    pos = s.index('\n\n')
    s = s[:pos] + notice + s[pos:]
    p.write_text(s, 'utf-8')
    print(json.dumps({'status': 'PASS_CURRENT055_HANDOFF196', 'ROM_sha256': sha(rom), 'archive_sha256': package['archive_sha256'], 'verified_manifests': len(checks)}, indent=2))


if __name__ == '__main__':
    main()
