"""Resolve numeral combinatorial font demand; measure remaining21+credits, no ROM edit."""
from pathlib import Path
import csv
import html
import json
import re
from PIL import Image, ImageDraw, ImageFont
from extract_title_png import encode, decode
from compile_ui_card_group import variable_codes
from plan_text11_190 import F8_values, family
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def draw(text, width, face, credits=False):
    lines = text.split('\n')
    image = Image.new('L', (width, len(lines) * 16))
    d = ImageDraw.Draw(image)
    variable_fields = []
    for y, raw in enumerate(lines):
        units = []
        for chunk in re.split('(\x01[^\x02]*\x02)', raw):
            var = chunk.startswith('\x01')
            if var:
                chunk = chunk[1:-1]
            for c in chunk:
                advance = 8 if var or (credits and c.isspace()) else 12
                units.append((c, advance, var))
        span = sum(w for _, w, _ in units)
        assert span <= width, (raw, span, width)
        left = 0 if credits else (width - span) // 2
        if any(v for _, _, v in units):
            preceding = 0
            for _, w, var in units:
                if var:
                    break
                preceding += w
            shift = (-(left + preceding) + 4) % 8 - 4
            left += shift
        assert 0 <= left and left + span <= width
        x = left
        field = []
        for c, advance, var in units:
            g = Image.new('L', (16, 16))
            ImageDraw.Draw(g).text((0, -1), c, font=face, fill=2)
            box = g.getbbox()
            assert c.isspace() or box
            assert box is None or box[2] <= advance, (c, box, advance)
            d.text((x, y * 16 - 1), c, font=face, fill=2)
            if var:
                assert x % 8 == 0
                field.append({'char': c, 'x': x, 'y': y * 16})
            x += advance
        variable_fields.extend(field)
    assert set(image.get_flattened_data()) <= {0, 2}
    tiles = {bytes(64)}
    for y in range(0, image.height, 8):
        for x in range(0, image.width, 8):
            bits = bytes(image.crop((x, y, x + 8, y + 8)).get_flattened_data())
            assert decode(encode(bits)) == bits
            tiles.add(bits)
    return image, tiles, variable_fields


def main():
    records.DATE = '2026-10-09'
    report = R / 'qa/reports/text11_201_remaining.json'
    assert not report.exists()
    review = R / 'workspace/review/text11_remaining201_v2'
    review.mkdir(exist_ok=False)
    rows = list(csv.DictReader((R / 'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')))
    source = (R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes').read_bytes()
    face = ImageFont.truetype(str(R / 'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'), 12)
    prices = [''.join(' ' if v == 0 else str(v - 0x70) for v in variable_codes(source, ride)) for ride in range(6)]
    tickets = F8_values(source)
    results = []
    cards = []
    font196_union = {bytes(64)}
    credits_union = {bytes(64)}
    for r in rows:
        if r['kind'] != 'main' or r['status'] != 'draft' or not r['translation_ko']:
            continue
        slot = int(r['reference_ids'].split(',')[0], 16)
        if slot <= 21:
            continue
        group = family(slot)
        text = r['translation_ko']
        credits = group == 'credits_scroll'
        width = 256 if credits else 192 if group.startswith('ride_upper') else 168
        variants = [text]
        if '{variable_FA}' in text:
            values = prices[5:] if slot == 0x1a else prices
            variants = [text.replace('{variable_FA}', '\x01' + v + '\x02') for v in values]
        elif '{variable_F8}' in text:
            variants = [text.replace('{variable_F8}', '\x01' + v + '\x02') for v in tickets]
        alltiles = {bytes(64)}
        outside_by_variant = []
        stable_digits = {}
        field_count = 0
        sample = None
        for variant in variants:
            image, tiles, fields = draw(variant, width, face, credits)
            alltiles |= tiles
            if sample is None:
                sample = image
            # For every numeral at every position, its own two aligned tiles
            # depend solely on its char, not either neighboring digit.
            outside = bytearray(image.tobytes())
            for f in fields:
                x, y, c = f['x'], f['y'], f['char']
                bits = bytes(image.crop((x, y, x + 8, y + 16)).get_flattened_data())
                assert c not in stable_digits or stable_digits[c] == bits
                stable_digits[c] = bits
                for yy in range(y, y + 16):
                    outside[yy * width + x:yy * width + x + 8] = bytes(8)
            outside_by_variant.append(bytes(outside))
            field_count += len(fields)
        assert all(z == outside_by_variant[0] for z in outside_by_variant)
        if slot in (0x1d, 0x2a):
            font196_union |= alltiles
        if credits:
            credits_union |= alltiles
        paired_length = (width // 8 * 2 + 1) * len(text.split('\n'))
        result = {'entry_id': r['entry_id'], 'family': group, 'native_ids': r['reference_ids'],
                  'original_text': text, 'proposed_width': width, 'line_count': len(text.split('\n')),
                  'variant_count': len(variants), 'font_tiles_union': len(alltiles), 'fits128': len(alltiles) <= 128,
                  'numeral_advance': 8 if stable_digits else None, 'Hangul_advance': 12,
                  'all_variant_other_pixels_exact': True, 'isolated_numeral_chars': ''.join(sorted(stable_digits)),
                  'variable_field_checks': field_count, 'paired_stream_length': paired_length,
                  'cursor8bit_fits': paired_length < 256,
                  'actual_geometry_font_lifetime_verified11px': False, 'ROM_implemented': False}
        results.append(result)
        rgb = Image.new('RGB', sample.size)
        rgb.putdata([(255, 254, 255) if i else (0, 0, 0) for i in sample.get_flattened_data()])
        png = r['entry_id'] + '.png'
        rgb.save(review / png)
        cards.append(f'<article><h2>{r["entry_id"]} · {group}</h2><p>{width}px · {result["line_count"]}줄 · 합집합{len(alltiles)}/128 · 값{len(variants)}개. {"글꼴 용량 충족" if result["fits128"] else "용량 재설계 필요"}</p><img src="{png}" alt="정적 후보"><pre>{html.escape(text)}</pre></article>')
    assert len(results) == 24 and sum(x['family'] != 'credits_scroll' for x in results) == 21
    upper = [z for z in results if z['family'].startswith('ride_upper')]
    assert len(upper) == 10
    f8 = next(z for z in results if z['entry_id'] == 'MAIN_05929')
    assert f8['variant_count'] == 1000 and f8['variable_field_checks'] == 3000 and f8['fits128']
    d = {'work': 201, 'status': 'PASS_STATIC_REMAINING24_LAYOUT_NUMERAL_ISOLATION_BUDGET',
         'ordinary_remaining': 21, 'credits_remaining': 3, 'pages': results,
         'font196_price_departure_union': len(font196_union), 'font196_price_departure_fits128': len(font196_union) <= 128,
         'credits201_three_stream_union': len(credits_union), 'credits201_fits128': len(credits_union) <= 128,
         'current_CHR_KiB': 232, 'proposed_CHR_KiB': 256,
         'proposed_top10_pair_starts': list(range(233, 252, 2)),
         'proposed_possession_pair_start': 254, 'native_CHR_ids_8bit_fits': True,
         'numeral_strategy': 'Rasterize sameGalmuri11@12,8px advance aligned to8px tiles; Hangul12x16 unchanged; do not change nativeFA/F8 values/leading blanks',
         'runtime_and_ROM_edits': False, 'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'),
         'limits': ['Upper192 and credits256 are measured native output extents, not11px UI life proof',
                    'Proposed CHR layout needs consumer init/odd top latch/050 refresh/mapper runtime verification',
                    'Credits long streams need16bit cursor or line pointer and paced queue rather than byte-wrap',
                    '057 representative actual NMI/IRQ/font residence unverified; do not call24 entries done']}
    report.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    (review / 'review.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>나머지 텍스트11px 정적 설계201</title><style>body{font-family:sans-serif;max-width:900px;margin:24px auto;padding:0 16px;background:#202027;color:white}article{padding:16px 0;border-top:1px solid #777}img{width:768px;max-width:100%;image-rendering:pixelated}pre{white-space:pre-wrap}</style><h1>나머지 일반21개·크레딧3개 — 정적 설계</h1><p>폰트와 번역에서 만든 후보이며 ROM에 넣거나 실제 게임에서 검증하지 않았습니다. 그림/HUD/정지 표지판은 이번 확대 대상에서 제외했습니다. 숫자는 같은 글꼴의8px 폭으로 타일 경계에 맞춰1000가지 값에서 글꼴 조합 폭발을 줄였습니다. 글꼴의 숫자 잉크 높이는 한글11px와 같다고 주장하지 않습니다.</p>''' + ''.join(cards) + '</html>', 'utf-8')
    body = f'''057의 홈·매표소 후보 이후 남은 일반21개와 크레딧3개의 정적 확대 설계를 계산했다. [24개 정적배치](../workspace/review/text11_remaining201_v2/review.html), [모든 값/용량 보고](../qa/reports/text11_201_remaining.json). 실제 게임 캡처나 새ROM 구현이 아니다. 번역CSV·원본·057·055·HUD/정지 등 그림은 변경하지 않았다. 첫201 시도는 크레딧의M 글리프가9px 폭이라8px ASCII 셀의 클리핑 검사를 통과하지 못했다. 실패 스크립트와 이미 생성된 정적PNG를 보존했고, v2는 숫자만8px·크레딧 공백8px·실제 문자12px로 정해 모든 글자 획을 보존했다.

190에서 보유 티켓F8는12px 숫자를 이어그려1000가지 수의 타일 합집합175개가 됐다. 같은 Galmuri11@12px에서 숫자 advance만8px로 하고8px 타일 경계에 맞추면 합집합은 **{f8['font_tiles_union']}타일**로 줄어128 안에 든다. 원래 native F8 reader를 실행한0..999의3자리·선행 빈칸은 그대로이며 문구는 같다.3000자리의 각 숫자 상하 타일이 이웃 숫자와 무관하고, 숫자 영역 밖 모든 픽셀이1000경우 동일함을 검사했다. 한글12×16셀/잉크11px 유지, 숫자는 해당 글꼴의 실제 잉크 높이를 따르며11px로 억지 확대하지 않았다. FA의6개 원래 요금 값도 같은 방식으로 검사했다.

가격1D와 출발2A의 font196 합집합은{len(font196_union)}타일이다. 보유2B는 새254/255 페어로 분리하고 상단 안내·놀이기구 이름10개는 odd233/235/.../251로 분리하는 용량안이 있다. 현재232KiB CHR를256KiB로 확장하면 이22KiB 글꼴과 정렬 간격을 담을 수 있다. 이는 구체적인 슬롯/저장 예산안이지 mapper·동시 상하 폰트 수명 검증 완료가 아니다. 기존050의 매표소 갱신 보존과 각 odd top latch, 실제 창과 clear 경계를 확인한 뒤 후크에 연결해야 한다.

크레딧3개의 같은 글꼴 합집합은{len(credits_union)}타일/128로 {'충족' if len(credits_union) <= 128 else '초과'}한다. 모든 제작진/제공/KONAMI/법적 문구·빈행은 보존했다. 일반 대사 byte cursor로 변환하면 크레딧 스트림은256바이트를 넘으며 초기 즉시 출력도 큐 예산을 다시 정해야 한다.16bit 커서 또는 줄별 포인터와 프레임별 전송이 필요하므로 문구를 잘라 넣거나 조용히 글꼴을 생략하지 않는다.

정적/CPU: 모든24개 후보의 글리프·2bpp 왕복/폭/변수 합집합을 검사했다. 새로운 ROM·패치·에뮬레이터·자동 컨트롤러·장면 시각검증·HTML브라우저 렌더 QA는 없다. 창 폭192px/크레딧256px은 원래 타일 출력 예산이며 실제11px 줄 배치/지우기·스크롤·NMI/IRQ·폰트수명이 확인된 것으로 확대하지 않는다.057의2줄 즉시출력/NMI 및 실제 홈·교환 소비가 아직 확인되지 않았으므로 공유 카드까지 실제 성공으로 주장하지 않는다.

변경 파일/해시는 [201매니페스트](../manifests/nonplay201_assets.json). 원본/1편/CSV/051/055/057·사용자Mesen/세이브·이전 자료 보존. 원문 유지6건·그림 크기 그대로다. 카페완성 작업기/외부 게시 없음. 재현 스크립트는 고정된 결과를 덮어쓰지 않으며 새출력 경로를 정한 복제에서 재현한다.'''
    records.seal(201, 'TEXT11_REMAINING_NUMERALS_CARDS_CREDITS_DESIGN_201.md', '남은 일반21개·크레딧3개 확대 설계와 숫자 용량 해결안', body,
                 f'F8 1000값 숫자3000자리 고정타일 분리,175→{f8["font_tiles_union"]}/128. 상단10페어·보유254/255 저장안, 크레딧{len(credits_union)}/128·긴커서/전송 재설계 필요. 새ROM/실행 없음.',
                 '057 홈·매표소의 실제 출력/건너뛰기·NMI/IRQ·소거·교환 폰트 수명 근거를 확보한 뒤 나머지21개 소비기에 확대한다.',
                 [Path(__file__), R / 'scripts/plan_remaining_text11_201.py', report, R / 'scripts/plan_text11_190.py', R / 'scripts/compile_ui_card_group.py',
                  *[f for folder in (review, R / 'workspace/review/text11_remaining201') for f in folder.iterdir() if f.is_file()]])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = p.read_text('utf-8').replace('현재 개발049 / 작업201', '기준051 / 057 CPU후보 / 그림 제외11px 확대 설계 / 작업201', 1)
    p.write_text(s, 'utf-8')
    print(json.dumps({k: d[k] for k in ('status', 'font196_price_departure_union', 'credits201_three_stream_union')}, indent=2))


if __name__ == '__main__':
    main()
