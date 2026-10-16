"""Seal059 source/CPU and static ROM previews with five explicit title-frame models."""
from pathlib import Path
import html
import json
from PIL import Image
from extract_title_png import decode
from verify_ordinary11_204 import progressive, pixels, initial, run, queue
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    folder = R / 'build/ordinary11_candidate_059'
    path = folder / 'TinyToon2_Ordinary11_Candidate059.nes'
    rom = path.read_bytes()
    plan = json.loads((folder / 'ordinary11_plan.json').read_text('utf-8'))
    cpu_path = R / 'qa/reports/ordinary11_204_CPU.json'
    cpu = json.loads(cpu_path.read_text('utf-8'))
    assert cpu['status'] == 'PASS_FINAL059_33_ORDINARY_AND_NINE_OPENING_CPU'
    review = R / 'workspace/review/ordinary11_204'
    review.mkdir(exist_ok=False)
    cards = []
    for z in plan['pages']:
        writes, _, _ = progressive(rom, z)
        im = pixels(rom, z, writes)
        ref = Image.open(folder / ('static_' + z['entry_id'] + '.png'))
        assert im.tobytes() == ref.tobytes()
        rgb = Image.new('RGB', im.size)
        rgb.putdata([(255, 254, 255) if i else (0, 0, 0) for i in im.get_flattened_data()])
        name = z['entry_id'] + '.png'
        rgb.save(review / name)
        cards.append(f'<article><h2>{z["entry_id"]} · {html.escape(z["family"])}</h2><p>{z["width_pixels"]}px · {z["font_slots_allocated"]}/128슬롯 · font {z["font_bank"]}</p><img class="text" src="{name}" alt="최종ROM/CPU 정적 문자 복원"><pre>{html.escape(z["original_text"])}</pre></article>')
    native_cards = json.loads((R / 'qa/dialogue/cards033_actual_pages.json').read_text('utf-8'))
    models = []
    for entry in native_cards:
        ride = entry['ride']
        rule = next(z for z in plan['pages'] if z['page'] == 0x1d + ride)
        title = next(z for z in plan['pages'] if z['page'] == 0x23 + ride)
        native = R / entry['source_image']
        oldppu = native.with_name(native.stem + '_ppu.bin').read_bytes()
        oldimage = Image.open(native).convert('RGB')
        # Derive the existing palette from actual unchanged high-tile native art.
        colors = {}
        for y in range(32, 136):
            for x in range(32, 224):
                code = oldppu[0x2000 + (y // 8) * 32 + x // 8]
                if code < 128:
                    continue
                bits = decode(oldppu[code * 16:code * 16 + 16])
                value = bits[(y % 8) * 8 + x % 8]
                a = oldppu[0x23c0 + (y // 32) * 8 + x // 32]
                shift = ((y // 8 % 4) // 2) * 4 + ((x // 8 % 4) // 2) * 2
                pal = (a >> shift) & 3
                key = pal, value
                color = oldimage.getpixel((x, y))
                assert key not in colors or colors[key] == color
                colors[key] = color
        assert colors[0, 0] == (0, 0, 0) and min(colors[0, 2]) > 240
        nt = bytearray(oldppu)
        changed = set()
        for z in (title, rule):
            m = initial(rom, z, ride=ride)
            run(m, 0x925e)
            for addr, code in queue(m.ram).items():
                nt[addr] = code
                changed.add(addr)
        allowed = {z['NT_top_origin'] + y * 32 + x for z in (title, rule)
                   for y in range(len(z['NT_rows'])) for x in range(z['columns'])}
        allowed |= {int(k) for k in plan['title_frame_repair_cells']}
        assert changed == allowed
        image = Image.new('RGB', (192, 104))
        for y in range(32, 136):
            for x in range(32, 224):
                code = nt[0x2000 + (y // 8) * 32 + x // 8]
                data = rom[title['font_file_offset'] + code * 16:title['font_file_offset'] + code * 16 + 16] if code < 128 else oldppu[code * 16:code * 16 + 16]
                value = decode(data)[(y % 8) * 8 + x % 8]
                a = oldppu[0x23c0 + (y // 32) * 8 + x // 32]
                shift = ((y // 8 % 4) // 2) * 4 + ((x // 8 % 4) // 2) * 2
                pal = (a >> shift) & 3
                image.putpixel((x - 32, y - 32), colors[pal, value])
        image.save(review / f'model_ride{ride:02d}.png')
        # Letter/border under both halves uses the original black/white palette.
        for y in (5, 6, 7):
            for x in range(6, 26):
                a = oldppu[0x23c0 + y // 4 * 8 + x // 4]
                pal = (a >> ((y % 4 // 2) * 4 + (x % 4 // 2) * 2)) & 3
                assert pal == 0 and oldppu[0x3f02 + 4 * pal] == 0x20
        models.append({'ride': ride, 'file': f'model_ride{ride:02d}.png', 'actual_game_capture': False,
                       'source_geometry_only': entry['source_image'], 'native_title_palette_rows5_6_7_same': True,
                       'CPU_changed_cells_only_text_and_three_frame_commands': len(changed)})
    modelhtml = ''.join(f'<article><h2>놀이기구{z["ride"]} 이름·설명 동시 배치</h2><img src="{z["file"]}" alt="정적 카드 모형"><p>과거033의 NT/원래 목재 타일·팔레트에 최종059 CPU가 만든 문자/테두리 명령을 적용해 복원한 정적 모형입니다. 실제059 실행 화면이 아닙니다.</p></article>' for z in models)
    (review / 'review.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>059 일반대사11px 정적 검토</title><style>body{font-family:sans-serif;max-width:960px;margin:24px auto;padding:0 16px;background:#202027;color:white}article{padding:16px 0;border-top:1px solid #777}img{width:576px;max-width:100%;image-rendering:pixelated}pre{white-space:pre-wrap}</style><h1>059 — 일반33개·오프닝9개 확대 후보</h1><p>이 페이지는 ROM/최종CPU로 복원한 정적 배치와 상단창 모형입니다. 실제059 Mesen 실행 캡처가 아닙니다. 출력 중·NMI/IRQ·CHR256 실시간 매핑·다른 화면 전환 검수는 미수행입니다.</p><p>이름160px/설명184px, 놀이기구별 이름+설명5개 공유 글꼴. 이름 칸 아래 테두리를 한 타일 내렸습니다.33개 일반문단·1000F8·FA6selector×2문단·1071건너뛰기 경계와4320초기화/1556비대상 CPU검사를 통과했습니다. HUD·정지 등 작은 그림과 크레딧3개는 기존 크기입니다.</p>''' + modelhtml + ''.join(cards) + '</html>', 'utf-8')
    report = R / 'qa/reports/ordinary11_204_static_review.json'
    assert not report.exists()
    report.write_text(json.dumps({'work': 204, 'status': 'PASS_ROM_CPU_THIRTYTHREE_TEXT_AND_FIVE_STATIC_CARD_MODELS',
                                  'ROM_sha256': sha(path), 'models': models, 'actual_game_capture': False,
                                  'browser_render_QA': False, 'files': {f.relative_to(R).as_posix(): sha(f) for f in review.iterdir() if f.is_file()}}, indent=2) + '\n', 'utf-8')
    body = f'''[059 ROM](../build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes) SHA `{sha(path)}`를 만들었다. [정적 배치와5개 상단창 모형](../workspace/review/ordinary11_204/review.html), [최종CPU](../qa/reports/ordinary11_204_CPU.json), [복원·모형 검사](../qa/reports/ordinary11_204_static_review.json). 기존055의 수정6문단 포함 오프닝9개, 홈/매표소/성/놀이기구 안내·이름/요금·보유/시작33개를11px 후보로 구성했다. 등록42개 후보이지 전게임 완료 분모나 실제059 실행 성공이 아니다.

058에서 발견한 동시거주/기하를 수정했다. 각 놀이기구의 제목+설명은 같은 odd233/235/237/239/241 페어를 공유한다. 실제033 NT에 따라 제목20열160px, 설명23열184px, 하단21열168px이다. 이름의11px 높이에 맞춰 아랫테두리를 한 타일 내려 row7에 원래8B/8C/C4를 쓰고 row6 양옆에는 원래 row5의88/C2 세로선을 쓴다. 이름 완성 즉시 큐에36바이트/3명령을 추가한다. 본문의 글자/모든 크레딧·제공·법적 문구/타이틀·HUD·정지 등 기존 그림은 유지하며 이름칸의 필요한 기하만 조정했다.

033의5개 원래NT/실제PNG에서 border provider와 row5/6/7의 black0F/white20 팔레트 일치를 확인했다. 최종059 font/CPU 큐를 해당NT에 적용한 것은 정적 모형이며059 실행 캡처가 아니다. 두 순서(설명→제목,제목→설명)의 실제 초기화6502를 실행한 뒤 이전 문구가 같은font로 픽셀exact 유지됨을 검사했다. 모든 모형 변경NT는 문자 셀과 명시한3개 테두리 명령뿐이다. 이 증명이 비동기 실제 화면/전환 검사를 대신하지 않는다.

숫자: F8의0..999/선행 빈칸과 FA의6selector 요금을 원래 reader 값으로 확인했다. FD의 새 private 스트림 토큰을8px 폭 숫자 상하 타일로 읽으며 bitmap 값은 같은 Galmuri11@12다. 한글12×16셀/잉크11px, 숫자는 원래 글꼴 잉크 높이를 따르므로 모든 숫자가 정확히11px 높이라는 주장은 아니다. 공통 가격/출발 font196을 함께 만들고 보유2B만254/255로 분리했다. native15의 추가 ride font190도 같은 문구로 연결했다. 크레딧3개는8px 그대로다.

CPU:33문단/1042값 조건(1000F8+FA6×2 포함)의 점진·즉시 출력과 최종font pixel exact.1071기본값 건너뛰기 경계의 남은 출력,4320 native init ABI/사이클(선언 글꼴값 제외),1556비대상 A/X/Y/P/SP·RAM·큐,050 booth retention10조건,5쌍 title/rule 동시거주,기존9오프닝 최종CPU PASS. NMI/IRQ 분리 모델만으로 전송 예산 성공을 주장하지 않는다.

정적·빌드·적용: immutable 원본ExpectedWrite/비중첩/전체 모델/diff 허용범위/IPS 실적용 exact. 독립059ROM·IPS exact.524304바이트/PRG256KiB/CHR256KiB다.057 대비기존영역10832바이트와24576바이트 확장. 원문/CSV/원래CHR128KiB/보호그림/fixedIRQ는 그대로다. 변경·SHA는 [204매니페스트](../manifests/nonplay204_assets.json). 최초203 verifier의 phase0 기대값 정정은203 실패기록에 유지하며058을 덮어쓰지 않았다.

에뮬레이터/직접장면:059 새실행없음. 실제 선택/교환·카드/건너뛰기·소거·CHR256 매핑·NMI/IRQ·폰트수명·크레딧 스크롤/16bit커서·전역 도달성·최종사람 미감·전체플레이·오디오/하드웨어/저장호환 미완료.059는 미채택 개발 후보다. 사용자 담당 플레이를 자동컨트롤러 실험으로 대체하지 않았다. 정적 모형33PNG/5개카드와 과거033 화면을 분리한다.

원본/1편/CSV/051/055/057/실패058/056·사용자Mesen/세이브·기존 QA와 원문유지6건을 보존했다. 카페완성 작업기/게시 없음. 재현: `python scripts/build_ordinary11_204.py --output build/<new-directory>`로 새경로에 빌드한다. 현재검사기는 고정059와기존보고를 보존하므로 재검사는 대상/출력경로를 정한 복제에서 시행한다.'''
    records.seal(204, 'ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md', '일반33개11px059·카드 글꼴공유/이름칸 수정·최종CPU', body,
                 '42등록문단 후보(오프닝9+일반33).F8천값/FA6×2/1071skip/4320init/1556fallback/5쌍 카드공유 PASS.160/184px·이름 테두리 수정.새059 실행 없음.',
                 '059 개발 후보의 ROM 없는 적용 패키지를 만들고 Windows 적용/최종 ZIP을 검증한 뒤 현재 인계를 갱신한다.',
                 [Path(__file__), R / 'scripts/build_ordinary11_204.py', R / 'scripts/verify_ordinary11_204.py', cpu_path, report,
                  *[f for directory in (folder, R / 'build/ordinary11_204_rebuild059', review) for f in directory.iterdir() if f.is_file()],
                  R / 'qa/dialogue/cards033_actual_pages.json',
                  *[R / z['source_image'] for z in native_cards],
                  *[(R / z['source_image']).with_name(Path(z['source_image']).stem + '_ppu.bin') for z in native_cards]])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = p.read_text('utf-8').replace('현재 개발049 / 작업204', '기준051 / 오프닝055 / 일반33개059 CPU후보 / 작업204', 1)
    p.write_text(s, 'utf-8')
    print(json.dumps({'status': 'PASS204_SEALED059', 'static_card_models': 5, 'ordinary33': True}, indent=2))


if __name__ == '__main__':
    main()
