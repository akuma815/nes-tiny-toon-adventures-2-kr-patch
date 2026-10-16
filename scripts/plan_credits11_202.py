"""Credits144-to106 tile alignment alternative; static glyph source kept unchanged."""
from pathlib import Path
import csv
import html
import json
from PIL import Image, ImageDraw, ImageFont
from extract_title_png import encode, decode
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    report = R / 'qa/reports/credits11_202_capacity.json'
    assert not report.exists()
    folder = R / 'workspace/review/credits11_202'
    folder.mkdir(exist_ok=False)
    rows = [r for r in csv.DictReader((R / 'workspace/translation/text_ja.csv').open(encoding='utf-8-sig'))
            if r['entry_id'] in ('MAIN_05939', 'MAIN_05999', 'MAIN_059E7')]
    font = R / 'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'
    face = ImageFont.truetype(str(font), 12)
    cases = []
    cards = []
    for latin in (12, 16):
        slots = {bytes(64): 0}
        atlas = bytearray(2048)
        pages = []
        for r in rows:
            lines = r['translation_ko'].split('\n')
            im = Image.new('L', (256, len(lines) * 16))
            d = ImageDraw.Draw(im)
            widths = []
            for y, line in enumerate(lines):
                x = 0
                for c in line:
                    advance = 8 if c.isspace() else 12 if '\uac00' <= c <= '\ud7a3' else latin
                    glyph = Image.new('L', (16, 16))
                    ImageDraw.Draw(glyph).text((0, -1), c, font=face, fill=2)
                    box = glyph.getbbox()
                    assert c.isspace() or box
                    assert box is None or box[2] <= advance
                    d.text((x, y * 16 - 1), c, font=face, fill=2)
                    x += advance
                assert x <= 256
                widths.append(x)
            codes = []
            for y in range(0, im.height, 8):
                line = []
                for x in range(0, 256, 8):
                    bits = bytes(im.crop((x, y, x + 8, y + 8)).get_flattened_data())
                    if bits not in slots:
                        code = len(slots)
                        slots[bits] = code
                        raw = encode(bits)
                        assert decode(raw) == bits
                        if code < 128:
                            atlas[code * 16:code * 16 + 16] = raw
                    line.append(slots[bits])
                codes.append(line)
            pages.append({'entry_id': r['entry_id'], 'unaltered_text': r['translation_ko'],
                          'lines': lines, 'line_widths': widths, 'line_count': len(lines), 'NT_rows': codes,
                          'fullwidth_paired_stream_bytes': 65 * len(lines)})
            rgb = Image.new('RGB', im.size)
            rgb.putdata([(255, 254, 255) if i else (0, 0, 0) for i in im.get_flattened_data()])
            name = f'{r["entry_id"]}_latin{latin}.png'
            rgb.save(folder / name)
        if len(slots) <= 128:
            # Independent serialized font reconstruction of all three complete pages.
            for z in pages:
                im = Image.new('L', (256, len(z['NT_rows']) * 8))
                for y, row in enumerate(z['NT_rows']):
                    for x, code in enumerate(row):
                        im.paste(Image.frombytes('L', (8, 8), decode(atlas[code * 16:code * 16 + 16])), (x * 8, y * 8))
                rgb = Image.open(folder / f'{z["entry_id"]}_latin{latin}.png').convert('RGB')
                assert list(rgb.get_flattened_data()) == [(255, 254, 255) if i else (0, 0, 0) for i in im.get_flattened_data()]
            (folder / f'credits11_latin{latin}_font.chr').write_bytes(atlas)
        cases.append({'Latin_advance': latin, 'Hangul_advance': 12, 'space_advance': 8,
                      'same_face_size_and_glyph_shapes': True, 'shared_three_page_tiles': len(slots),
                      'fits128': len(slots) <= 128, 'font_decode_all_pages_exact': len(slots) <= 128,
                      'pages': pages})
    assert [z['shared_three_page_tiles'] for z in cases] == [144, 106]
    for r in rows:
        cards.append(f'<article><h2>{r["entry_id"]}</h2><div><section><h3>영문12px 간격 ·144/128 초과</h3><img src="{r["entry_id"]}_latin12.png"></section><section><h3>영문16px 간격 ·106/128 충족</h3><img src="{r["entry_id"]}_latin16.png"></section></div><pre>{html.escape(r["translation_ko"])}</pre></article>')
    (folder / 'review.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>크레딧11px 간격·용량 비교202</title><style>body{font-family:sans-serif;background:#202027;color:white;margin:24px}article{padding:16px 0;border-top:1px solid #777}article>div{display:flex;flex-wrap:wrap;gap:24px}img{width:512px;max-width:100%;image-rendering:pixelated}pre{white-space:pre-wrap}</style><h1>크레딧11px — 타일 간격 용량안</h1><p>새로 그린 정적 후보이며 실제 게임 화면이 아닙니다. 글자 모양은 동일한 Galmuri11@12px입니다. 한글12px·공백8px 간격을 유지하고 영문 간격만12px 또는16px로 비교했습니다. 오른쪽106타일안은 전체3문단 폰트를2KiB에 직렬화한 뒤 모든 픽셀을 복원했습니다. 이름·제공·법적 문구·빈 행은 모두 보존했습니다. 최종 배치 승인이나 크레딧 스크롤 구현은 아직 없습니다.</p>''' + ''.join(cards) + '</html>', 'utf-8')
    d = {'work': 202, 'status': 'PASS_STATIC_CREDITS_SHARED106_FONT_ROUNDTRIP_OPTION',
         'cases': cases, 'font_sha256': sha(font), 'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'),
         'width': 256, 'height_per_line': 16, 'ROM_changed': False, 'actual_game_capture': False,
         'choice_adopted': False, 'remaining': ['16bit cursor/line pointer implementation',
                                              'Queue pacing across first chunk/scrolling updates',
                                              'Native mode5/6 nametable transition and scroll consumption',
                                              'Human spacing review and actual credits scene']}
    report.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = '''[크레딧 정적 비교](../workspace/review/credits11_202/review.html), [슬롯/왕복 보고](../qa/reports/credits11_202_capacity.json).201의3문단 글꼴144/128 초과에 대해 글자 모양을 바꾸지 않는 대안을 계산했다. Galmuri11@12px·한글12px·공백8px을 유지하고 영문 advance를16px로 하면 타일 위상이 일정해져3문단 전체 합집합106개가 된다.2KiB/128슬롯 안에 들어가고 독립2bpp 복원으로3문단 모든 픽셀이 같다.12px 영문 간격안144개와 둘 다 보존했다.

영문 획을 늘리거나 글꼴을 대체하지 않았으며 제작진 이름·KONAMI·법적 문구·빈행의 문자열은 동일하다. 모든 줄은256px 안에 들며 원래32칸 공백도 유지한다. 이는 줄 배치의 기술 대안이지 사용자의 최종 미감 선택을 대신하지 않는다.16px 영문 간격안은 미채택이며 ROM에 삽입하지 않았다.

폰트 용량 문제에는106타일 해법이 있지만 긴 스트림의8bit cursor 초과와 초기 즉시 출력 큐는 별도 문제다. 전체32타일 상하 행을 단순 연결하면65×14=910바이트가 돼 기존 커서를 그대로 쓰면 안 된다.16bit 커서/줄별 포인터와 전송 분할, native5/6 NT 주소 전환·스크롤·폰트 수명 확인이 필요하다. 글자나 법적 고지를 생략하는 방법은 사용하지 않는다.

정적/직렬화·독립복원만 PASS. 새ROM/패치/에뮬레이터/자동 플레이/직접 장면·HTML 렌더 QA 없음. 원본·1편·CSV·051/055/057·사용자Mesen/세이브·그림·원문유지6건은 그대로다. 카페완성 작업기/게시 없음. 변경·해시는 [202매니페스트](../manifests/nonplay202_assets.json). 재현은 기존출력을 덮어쓰지 않으며 새경로를 정한 복제에서 수행한다.'''
    records.seal(202, 'CREDITS11_SHARED_FONT106_SPACING_OPTION_202.md', '크레딧11px 영문 간격 대안·106타일 왕복', body,
                 '같은 글자 모양·문구 보존. 영문16px 간격이면144→106/128,2KiB 직렬화3문단 픽셀exact. 미채택 정적안, 긴커서/전송/실제스크롤 남음.',
                 '197~202 고정근거·원본/링크를 감사하고057 CPU후보와 남은21개·크레딧 설계를 최신 인계에 반영한다.',
                 [Path(__file__), report, *[f for f in folder.iterdir() if f.is_file()]])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = p.read_text('utf-8').replace('현재 개발049 / 작업202', '기준051 / 057 CPU후보 / 크레딧106타일 정적안 / 작업202', 1)
    p.write_text(s, 'utf-8')
    print(json.dumps({'status': d['status'], 'all_three_credits_tiles': 106, 'font_KiB': 2}, indent=2))


if __name__ == '__main__':
    main()
