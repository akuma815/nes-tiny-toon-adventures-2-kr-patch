"""Seal057 CPU/build proof and static decoded-ROM font previews, not game screenshots."""
from pathlib import Path
import html
import json
from PIL import Image
from extract_title_png import decode
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    b = R / 'build/homebooth11_candidate_057'
    rom = (b / 'TinyToon2_HomeBooth11_Candidate057.nes').read_bytes()
    plan = json.loads((b / 'homebooth11_plan.json').read_text('utf-8'))
    cpu = json.loads((R / 'qa/reports/homebooth11_199_CPU.json').read_text('utf-8'))
    assert cpu['status'] == 'PASS_FINAL057_TYPED_SKIP_CLEAR_INIT_FONT_RETENTION_CPU'
    review = R / 'workspace/review/homebooth11_199'
    review.mkdir(exist_ok=False)
    cards = []
    for z in plan['pages']:
        im = Image.new('L', (168, len(z['NT_rows']) * 8))
        off = z['font_file_offset']
        for y, row in enumerate(z['NT_rows']):
            for x, c in enumerate(row):
                raw = rom[off + c * 16:off + c * 16 + 16]
                tile = Image.frombytes('L', (8, 8), decode(raw))
                im.paste(tile, (x * 8, y * 8))
        source = Image.open(b / ('static_' + z['entry_id'] + '.png'))
        assert im.tobytes() == source.tobytes()
        rgb = Image.new('RGB', im.size)
        rgb.putdata([(255, 254, 255) if i else (0, 0, 0) for i in im.get_flattened_data()])
        name = z['entry_id'] + '.png'
        rgb.save(review / name)
        cards.append(f'<article><h2>{html.escape(z["entry_id"])} · ID {z["page"]:02X}</h2><p>168px · {len(z["lines"])}줄 · {z["font_unique_tiles"]}/128타일</p><img src="{name}" alt="ROM에서 복원한 정적 글자 배치"><pre>{html.escape(chr(10).join(z["lines"]))}</pre></article>')
    (review / 'review.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>057 홈·매표소11px 정적 검토</title><style>body{font-family:sans-serif;max-width:900px;margin:24px auto;padding:0 16px;background:#202027;color:white}article{padding:18px 0;border-top:1px solid #777}img{width:504px;max-width:100%;image-rendering:pixelated}pre{white-space:pre-wrap}</style><h1>홈·매표소 12개 대사 — 057</h1><p>057 ROM의 CHR와 네임테이블 계획으로 복원한 정적 배치입니다. 실제 게임 화면 캡처가 아닙니다. Galmuri11 글자 모양을 유지하며 기존168px 대사창에 배치했습니다. 실제 표시·출력 중·지우기·선택지 전환·교환 검수는 미수행입니다.</p><p>점진 출력과 모든352 건너뛰기 경계, 기존5행 지우기 범위,4320 초기화 상태,1556 비대상 분기를 최종6502 모델로 확인했습니다. CPU 검사가 실제 NMI/IRQ 시점과 화면 검수를 대신하지 않습니다. HUD·정지 등 작은 그림은 변경하지 않았습니다.</p>''' + ''.join(cards) + '</html>', 'utf-8')
    report = R / 'qa/reports/homebooth11_199_review.json'
    assert not report.exists()
    report.write_text(json.dumps({'work': 199, 'status': 'PASS_ROM_FONT_DECODE_MATCHES_TWELVE_STATIC_LAYOUTS',
                                  'ROM_sha256': sha(b / 'TinyToon2_HomeBooth11_Candidate057.nes'),
                                  'files': {f.relative_to(R).as_posix(): sha(f) for f in review.iterdir() if f.is_file()},
                                  'actual_game_capture': False, 'browser_render_QA': False}, indent=2) + '\n', 'utf-8')
    body = f'''[057 ROM](../build/homebooth11_candidate_057/TinyToon2_HomeBooth11_Candidate057.nes) SHA `{cpu['ROM_sha256']}`를 만들었다. 사용자 조정6문단을 포함하는055를 기반으로 홈·선택명·매표소12개 대사를11px로 추가했다. [정적 검토HTML](../workspace/review/homebooth11_199/review.html), [최종CPU 보고](../qa/reports/homebooth11_199_CPU.json), [ROM 글꼴 복원 검사](../qa/reports/homebooth11_199_review.json). 검토 PNG는 실제 게임 캡처가 아니라 ROM 데이터로 복원한 정적 문자 배치다.

글자원천은 기존 Galmuri11 v2.40.4/TTF12px/12×16셀, 한글 잉크11px다. 모든 문구와 번역CSV를 그대로 유지하고168px/최대2줄에 배치했다. 비0 글리프 누락·슬롯128 초과·창 경계 초과가 없다. ROM CHR의 독립2bpp 복원과 편집 원천의 모든 픽셀이 동일하다. HUD·정지·기존 그림·헤더·fixedIRQ·오프닝055의9개 글꼴/본문은 보존했다.

056의 비대상V 플래그 실패를 해결했다. 대상 판정 전P/A를 저장하고 대상/비대상 분기에서 복원한다. 점진 출력9C81과 즉시 출력925E 양쪽에 root8·ID0A..15·폰트·완성 원래 포인터 조건을 적용한다. 다른 출력기는 기존 경로로 되돌린다. 대상 밖 원래 레지스터/게임RAM/큐가1556조건에서 같았다.

최종6502:12문단 점진 상하 출력과 모든352 건너뛰기 경계의 남은 출력이 정확하다. 즉시 출력은 줄별 상·하 연속 전송 명령을 사용해 최대100바이트이며 줄/문단 cursor를 유지한다. 상하 모든 글자 셀은 원래22타일×5행/110셀 지우기 안에 있다. 기존 초기화4320조건의P/A/X/Y/SP·RAM·뱅크·사이클이055와 같고,050 매표소 숫자 갱신의 하단 글꼴 보존10조건 PASS. 기존IRQ 명령·레지스터 쓰기 사이클과 오프닝9문단 최종CPU도 보존했다. 새 점진 wrapper 최대506cycles, 즉시 출력 최대10165cycles이며 원래와 동일한 실행시간이라고 주장하지 않는다.

정적/빌드/적용: immutable 원본 ExpectedWrite·중첩0·최종 전체diff 허용 범위·IPS 실적용 exact PASS. 독립057 ROM/IPS 재빌드 exact PASS. 055 대비11313바이트이며12개 전용 글꼴·조건래퍼·새 스트림·즉시 출력 명령에 한정한다. CHR 크기/원문/대사 의미는 변경하지 않았다. 변경·해시는 [199매니페스트](../manifests/nonplay199_assets.json).

에뮬레이터/직접 장면: 새057 실행 없음. 출력 중/대기/소거·선택지 전환·교환의 실제 폰트 수명과 NMI/IRQ 전송 예산은 아직 미검증이다. 특히2줄 즉시 출력10165cycles의 비동기 예산은 CPU 단독 검사로 보장할 수 없다. 사용자 담당 플레이를 자동 컨트롤러 실험으로 대체하지 않았다. 정적 글자 배치와 CPU 성공을 실제 장면 검증으로 표현하지 않는다. 057은 미채택 개발 후보이며 최종 배포본이 아니다.

범위: 등록45초안 중 오프닝9+홈·매표소12=21개를11px 후보로 구성했다. 이번12개는 CPU/빌드 근거뿐이며 새057 전체21개의 실제 실행 성공을 뜻하지 않는다. 나머지 일반21개와 크레딧3개는 아직8px다. 상단 공유 카드/동적숫자/크레딧 문제와 전역private PRG 도달성은 남는다. 전체인벤토리·전체플레이·최종사람 글꼴/문체승인·오디오/하드웨어/저장호환 미완료다.

원본/1편/CSV/051/055/실패056/이전054/사용자Mesen·세이브·기존QA는 보존했다. 원문 유지6건도 그대로다. 카페완성 작업기/외부 게시 없음. 재현은 `python scripts/build_homebooth11_199.py --output build/<new-directory>`로 새 빈 경로를 사용한다. 현재 CPU 검사기는 고정057만 읽고 기존 보고를 덮어쓰지 않으므로 재검사는 대상·결과 경로를 새로 정한 복제에서 수행한다.'''
    records.seal(199, 'HOME_BOOTH11_CANDIDATE057_TYPED_SKIP_CPU_199.md', '홈·매표소12개11px 후보057 점진/건너뛰기 CPU 검증', body,
                 '055기반12개11px057.352 skip/4320 init/1556 fallback/050 retention/원래5행clear PASS. 독립ROM·IPS exact, 새실제 실행 없음.',
                 '057 개발 후보를 ROM 없는 적용 패키지로 만들고 Windows 적용·최종 ZIP을 검증한다.',
                 [Path(__file__), R / 'scripts/build_homebooth11_199.py', R / 'scripts/verify_homebooth11_199.py',
                  R / 'qa/reports/homebooth11_199_CPU.json', report,
                  *[f for folder in (b, R / 'build/homebooth11_199_rebuild057', review) for f in folder.iterdir() if f.is_file()]])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = p.read_text('utf-8').replace('현재 개발049 / 작업199', '기준051 / 오프닝055 / 홈·매표소057 CPU후보 / 작업199', 1)
    p.write_text(s, 'utf-8')
    print(json.dumps({'status': 'PASS199_SEALED057_STATIC_CPU', 'static_review': review.relative_to(R).as_posix()}, indent=2))


if __name__ == '__main__':
    main()
