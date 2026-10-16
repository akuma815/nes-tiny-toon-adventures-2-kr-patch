"""Audit the initial session and append per-task handoffs; refuses duplicate records."""
import csv, hashlib, json, re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'qa/reports/initial_session_20261004.json'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main():
    assert not REPORT.exists(), 'Initial audit exists; preserve it'
    manifest=load(ROOT/'manifests/source_rom.json');rom=ROOT/manifest['path'];data=rom.read_bytes()
    assert sha(rom)==manifest['sha256'] and len(data)==manifest['size_bytes']
    extracted=load(ROOT/'extracted/text/table_20261004_001/text_tokens.json')
    units=extracted['units']
    with (ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==54 and len({r['entry_id'] for r in rows})==54
    for row,u in zip(rows,units):
        for k in ('entry_id','source_tokens','raw_hex','raw_sha256','source_sha256'):
            assert row[k]==u[k]
        assert row['status']=='untranslated' and row['translation_ko']==''
        assert bytes.fromhex(row['raw_hex'])==data[u['file_offset']:u['end_exclusive']]
    captures=[];empty_png=[]
    for folder in ('baseline_attract_002','baseline_start_001','baseline_game_001'):
        p=ROOT/'qa/screenshots'/folder;env=load(p/'environment.json')
        assert env['exit_code']==0 and env['source_sha256']==manifest['sha256']
        assert sha(p/'capture_survey_used.lua')==env['lua_sha256']
        assert sha(p/'config_used.json')==env['config_sha256']
        for name,expected in env['files'].items(): assert sha(p/name)==expected
        images=[]
        for png in sorted(p.glob('frame_*.png')):
            if png.stat().st_size==0:
                assert png.name=='frame_00001.png';empty_png.append(str(png.relative_to(ROOT)));continue
            with Image.open(png) as im: im.verify()
            images.append(png.name)
        captures.append({'path':str(p.relative_to(ROOT)), 'exit_code':0,'valid_png_count':len(images),
            'sha256_environment':sha(p/'environment.json'),'purpose':'adopted baseline' if folder!='baseline_start_001' else 'early Start input exploration; not gameplay entry evidence'})
    for folder in ('text_trace_003','text_consumer_001'):
        p=ROOT/'qa/logs'/folder;env=load(p/'environment.json')
        assert env['exit_code']==0 and (p/'trace_complete.txt').read_text()==str(env['frames'])
        assert sha(p/'capture_survey_used.lua')==env['lua_sha256']
        for name,expected in env['files'].items(): assert sha(p/name)==expected
    actual=list(csv.DictReader((ROOT/'qa/logs/text_trace_003/script_bank_reads.csv').open()))
    for row in actual: assert data[int(row['file_offset'],16)]==int(row['value'],16)
    before=list(csv.DictReader((ROOT/'qa/logs/text_consumer_001/consumer_reads.csv').open()))
    for row in before: assert data[int(row['file_offset'],16)]==int(row['value'],16)
    font=[]
    for folder,frame in [('baseline_attract_002',1200),('baseline_attract_002',1920),('baseline_game_001',1080)]:
        p=ROOT/'qa/screenshots'/folder/f'frame_{frame:05d}_ppu.bin'
        assert p.read_bytes()[:0x800]==data[0x36810:0x37010]
        font.append({'capture':str(p.relative_to(ROOT)),'font_128_tiles_match_original':True})
    first=ROOT.parent/'Tiny Toon Adventures'
    refs=['docs/HANDOFF.md','docs/HANDOFF_2026-10-04.md','docs/HAMTON_FONT_FIX_2026-10-04.md',
        'docs/PUBLIC_WORKLOG_2026-10-04.md','dist/TinyToonAdventures_KR_Patch_v1.0.1_20261004.zip',
        'original/rom/Tiny Toon Adventures (Japan).nes']
    first_refs={(first/p).relative_to(ROOT.parent).as_posix():sha(first/p) for p in refs}
    assert first_refs['Tiny Toon Adventures/original/rom/Tiny Toon Adventures (Japan).nes']=='73300dc1505564827ef95ba3e2a06c26aa48920e4981195f32b2101c185ef3dd'
    assert first_refs['Tiny Toon Adventures/dist/TinyToonAdventures_KR_Patch_v1.0.1_20261004.zip']=='d3bf3ae72fe6567fd5386aa7db2be07d94da1c1092d4ac1c3866cc31f2b4baa7'
    dated=ROOT/'docs/HANDOFF_2026-10-04.md'
    assert '## 작업 2' not in dated.read_text(encoding='utf-8')
    block='''

## 작업 2 — 원본 CHR·실행·대사 소비 경로 조사

### 완료 결과와 변경

1편 최신 참고 기준을 `docs/FIRST_GAME_REFERENCE.md`에 정리했다. 2편 헤더/CHR 재현 스크립트, 격리 Mesen 설정·실행기, 읽기 추적 Lua, 화면 모음 생성기, `docs/SURVEY.md`, `docs/LOCALIZATION_WORK_PLAN.md`, `docs/journal/2026-10-04.md`를 작성했다.

정적: 32 CHR 페이지/8,192타일의 decode→encode 전체 일치. PRG/CHR 구간과 벡터를 기록했다. 일본어 글꼴 후보 페이지16의 코드별 PNG를 보존했고, 도입부/홈 세 캡처의 실제 PPU 폰트128타일이 파일 `[0x36810,0x37010)`과 동일하다.

에뮬레이터: 원본 콜드 부팅 무입력5,400프레임 `baseline_attract_002`, Start720의3,000프레임 `baseline_game_001` 종료0. 자연 도입부와 홈 안내를 확인했다. `baseline_start_001`은 Start300의 초기 입력 탐색이며 게임 시작 근거는720 캡처다. source SHA 유지. Mesen은 자체 DB의 KONAMI-VRC-7/Famicom 설정을 적용했다고 stdout에 기록하며 원본 헤더와 별도로 보존한다.

대사: `text_trace_003`의 실제 bank2 read2,432개를 원본과 대조했다. 좁힌 `text_consumer_001` 실행 직전327개 예상 읽기 샘플도 원본과 대조했고, bank2 주 스트림01..09와 bank3 매크로81의 실제 임시 매핑을 연결했다. 실행 직전 샘플은 실제 read callback과 별도 증거다. PPU 쓰기 PC D09F가 보고하는 실제 쓰기 명령은 D09C의STA2007이며 프레임 끝 은행만으로 데이터 위치를 판정하지 않는다.

직접 장면 시각 검토: `baseline_intro_contact_sheet.png`의 타이틀/첫 두 문단/편지/버스터/몬타나6표본과 `baseline_home_contact_sheet.png`의 홈 진입/안내/대기6표본을 직접 확인했다. 원본 일본어 화면이며 한글 가독성 검증은 아니다.

빌드/패치 적용: 미수행. 전체 완주/다른 장면/실기/오디오 청취도 미수행.

### 실패와 미해결

baseline_attract_001은 처음7프레임 Start 및 실행 중 Lua 수정 문제로 채택 제외. frame1의0바이트 PNG는 시각 증거 제외. text_trace_001은 종료0/PPU 원시 로그를 얻었지만 wrapper의 최종 PNG 조건 실패로 전체 PASS가 아니다. text_trace_002는 넓은read 콜백 비용으로120초 타임아웃/종료4294967295, 정상 완료에서 제외. 이후 데이터 bank와 실제 읽기 명령으로 범위를 좁혀 완료했다. 자세한 이력은 일지에 남겼다.

**다음 작업 하나: 확인된 주 대사·매크로 테이블을 제어 토큰과 공유 참조를 보존해 가역 추출한다.**

## 작업 3 — 원본 대사·공통 문자열 가역 추출과 번역 원천 초기화

### 결과

`scripts/extract_text.py`가 소비 코드 fingerprint와 원본 SHA를 확인한다. 주 포인터 `[0x55A9,0x5609)`48슬롯/46고유 스트림, 데이터 `[0x5609,0x5A28)`1,055바이트. 매크로 포인터 `[0x61B1,0x61C3)`9슬롯/8고유 스트림, 데이터 `[0x61C3,0x61FF)`60바이트. 데이터1,115바이트/포인터114바이트 전부 커버하고 각각 바이트 동일 왕복 PASS.

`extracted/text/table_20261004_001/{text_tokens.json,original_text.csv,extraction_report.json}`와 번역 단일 원천 `workspace/translation/text_ja.csv`54행을 생성했다. 번역은 비어 있고 전부untranslated. 54행에는 중복 참조를 합친 대사·숫자 전용/공백 스트림·크레딧·매크로가 포함되므로54문장/전체 게임 총량이라고 부르지 않는다. 일부 문자 대응과 크레딧 프로파일은 미확정 토큰으로 보존했다. 이 초기화 CSV를 다음 추출로 덮어쓰지 않는다.

최초 검사에서 fingerprint 주소의16바이트 보정과 매크로 끝 경계2바이트 과대를 검출해 출력 전 수정했다. 최종 데이터에는 누락·겹침이 없고 raw/control/pointer가 원본과 같다. 최종 감사는 source/실행 입력/원천CSV/문서 링크/산출물 해시를 확인한다.

### 검증을 구분한 결과

- 정적/추출: 원본 SHA 유지, 등록한2테이블의 전체 데이터·포인터 왕복PASS,54고유ID/행 상태/원본 tokens 일치, 채택한 실행 파일 해시와 로그 식별PASS.
- 빌드/차분 패치/실제 적용: 미수행. build와dist에 한글 ROM/배포본 없음.
- 에뮬레이터/시각: 작업2의 원본 경로 증거를 인용한다. 모든54원천의 장면 확인은 미수행.
- 전체 완주/실기/최종 번역 검토/카페 업로드: 미수행.

### 재현

프로젝트루트/Windows/Python3.12/Pillow12.3.0/Mesen2.1.1. 원본 검증 후 README의새출력 명령을 사용한다. 추출 재현에는 `--initialize-translation`을 붙이지 않는다. 첫 초기화는 기존CSV가없을때만 가능하다. 원본과1편은수정하지않는다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verify_source.ps1
python .\\scripts\\survey_rom.py --output .\\extracted\\chr\\survey_repro_next
python .\\scripts\\run_survey_qa.py --output .\\qa\\screenshots\\baseline_attract_next --frames 5400
python .\\scripts\\run_survey_qa.py --output .\\qa\\screenshots\\baseline_game_next --frames 3000 --start 720
python .\\scripts\\run_survey_qa.py --script .\\scripts\\trace_text_consumer.lua --output .\\qa\\logs\\text_consumer_next --frames 3100
python .\\scripts\\extract_text.py --output .\\extracted\\text\\table_repro_next
```

**다음 작업 하나: 일본어/공통 매크로의 코드표와 도입부 첫 문단MAIN_05609의 실제 레이아웃을 확정해 한글 PoC 입력을 만든다.**

### 해시와 변경 파일 목록

전체 변경/생성 파일의 SHA는 [초기 세션 감사](../qa/reports/initial_session_20261004.json)에 기록한다. 이 보고서의자기해시는외부인계재작성순환을피해등록하지않는다.

| 대상 | SHA-256 |
|---|---|
'''
    for rel in ['manifests/source_rom.json','workspace/translation/text_ja.csv','scripts/extract_text.py',
        'extracted/text/table_20261004_001/text_tokens.json','extracted/text/table_20261004_001/extraction_report.json',
        'qa/screenshots/baseline_intro_contact_sheet.png','qa/screenshots/baseline_home_contact_sheet.png']:
        block+=f'| `{rel}` | `{sha(ROOT/rel)}` |\n'
    dated.write_text(dated.read_text(encoding='utf-8')+block,encoding='utf-8')
    (ROOT/'docs/HANDOFF.md').write_text('''# 작업 재개

최신 인계: [HANDOFF_2026-10-04.md](HANDOFF_2026-10-04.md), **작업3**을 따른다.

프로젝트 구성·원본 보존·1편 최신 작업 검토·CHR 전체 왕복·원본 실제 실행·대사 경로 추적·등록2테이블 가역 추출을 마쳤다. 현재 번역 원천54행은untranslated이며 한글ROM/패치없음. 54행은전체게임54문장이라는뜻이아니다.

**다음 작업 하나:** 일본어/공통 매크로의 코드표와 도입부 첫 문단MAIN_05609의 실제 레이아웃을 확정해 한글 PoC 입력을 만든다.

현재구조: [SURVEY](SURVEY.md). 구현순서: [LOCALIZATION_WORK_PLAN](LOCALIZATION_WORK_PLAN.md). 1편참고: [FIRST_GAME_REFERENCE](FIRST_GAME_REFERENCE.md). 작업기근거: [일지](journal/2026-10-04.md). 규칙: [AGENTS](../AGENTS.md).
''',encoding='utf-8')
    checked=[]
    for doc in [ROOT/'README.md',ROOT/'AGENTS.md',*sorted((ROOT/'docs').rglob('*.md'))]:
        text=doc.read_text(encoding='utf-8');assert '\ufffd' not in text
        for dest in re.findall(r'\]\(([^)]+)\)',text):
            dest=dest.strip('<>')
            if dest.startswith(('https://','http://','#')):continue
            target=(doc.parent/dest.split('#')[0]).resolve()
            assert target.exists() or target==REPORT,f'Broken link {doc}: {dest}'
            checked.append({'document':str(doc.relative_to(ROOT)),'target':dest})
    tracked=[ROOT/'README.md',ROOT/'AGENTS.md',ROOT/'.gitignore']
    for sub in ('docs','scripts','config','manifests','workspace/translation'):
        tracked.extend(p for p in sorted((ROOT/sub).rglob('*')) if p.is_file() and '__pycache__' not in p.parts)
    tracked.extend(ROOT/'extracted/text/table_20261004_001'/n for n in ('text_tokens.json','original_text.csv','extraction_report.json'))
    tracked.extend([ROOT/'extracted/chr/survey_20261004_001/rom_survey.json',
        ROOT/'qa/screenshots/baseline_intro_contact_sheet.png',ROOT/'qa/screenshots/baseline_home_contact_sheet.png'])
    report={'date':'2026-10-04','source_sha256':sha(rom),'status':'PASS for initial-session checks only',
        'evidence_classes':{'static':'Source, CHR roundtrip, registered text/pointer roundtrip, CSV and links PASS',
            'build_apply':'NOT PERFORMED','emulator':'Adopted original baseline and two narrow traces PASS',
            'direct_visual':'Two contact sheets, 12 original-screen samples reviewed; no Korean readability QA'},
        'captures':captures,'excluded_empty_first_frame_png':empty_png,'actual_bank_read_samples':len(actual),
        'pre_read_execution_samples':len(before),'font_matches':font,'extraction':extracted['report'],
        'excluded_or_partial_runs':['baseline_attract_001: wrong no-input condition and unidentifiable loaded Lua hash',
            'text_trace_001: emulator exit 0, raw PPU trace retained, wrapper final PNG assertion failed',
            'text_trace_002: timeout, no completion marker'],
        'first_game_references':first_refs,'local_markdown_links_checked':len(checked),'links':checked,
        'changed_and_generated_files':{str(p.relative_to(ROOT)):sha(p) for p in tracked},
        'tools':{'Mesen':'2.1.1+137ae7ce3bf3f539d007e2c4ef3cb3b6c97672a1',
            'source_copy':'../Tiny Toon Adventures/tools/mesen-2.1.1; binaries only, no shared settings or saves',
            'upstream':'https://github.com/SourMesen/Mesen2','license':'GPL-3.0; local QA only, not packaged',
            'files':{p.name:sha(p) for p in sorted((ROOT/'tools/mesen-2.1.1').glob('*')) if p.is_file() and p.name!='settings.json'}},
        'missing':'Full glyph map, credits font, global text/graphics population, Korean PoC, translation, build/apply, all-scene QA, release, final cafe worklog',
        'next_action':'Complete the kana/macro code map and MAIN_05609 layout as inputs to the first Korean PoC'}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert REPORT.exists() and sha(rom)==manifest['sha256']
    print(json.dumps({'status':report['status'],'translation_rows':len(rows),'links_checked':len(checked),
        'actual_read_samples':len(actual),'pre_read_samples':len(before),'report':str(REPORT)},indent=2))
if __name__=='__main__': main()
