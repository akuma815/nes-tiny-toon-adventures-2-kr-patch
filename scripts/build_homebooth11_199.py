"""057: opening055 plus twelve lower home/booth strings, typed and skip renderers."""
from pathlib import Path
import argparse
import csv
import json
from PIL import Image, ImageDraw, ImageFont
from asm6502 import assemble
from extract_title_png import encode, decode
from dialogue_ips import make, apply
from seal_nonplay171 import R, sha

GUARD = '''
    PHP
    PHA
    LDA $18
    CMP #$08
    BNE @fallback
    LDA $06CF
    CMP #$0A
    BCC @fallback
    CMP #$16
    BCS @fallback
    SEC
    SBC #$0A
    TAY
    LDA $96F0,Y
    CMP $C6
    BNE @fallback
    LDA $06CF
    ASL A
    TAY
    LDA $9599,Y
    CMP $06CD
    BNE @fallback
    LDA $959A,Y
    CMP $06CE
    BNE @fallback
    PLA
    PLP
    LDA #$08
    JSR $FDD3
    JSR $PRINTER
    PHP
    PHA
    JSR $FDDB
    PLA
    PLP
    RTS
fallback:
    PLA
    PLP
    JMP $FALLBACK
'''

INSTANT = '''
line:
    LDA $06C3
    STA $02
    LDX $1E
    LDA #$01
    STA $0100,X
    INX
    LDA $06C1
    STA $0100,X
    INX
    LDA $06C0
    STA $0100,X
    INX
top:
    JSR $9880
    CMP #$80
    BCS @top_end
    STA $0100,X
    INX
    JSR $9880
    JMP @top
top_end:
    LDA #$FF
    STA $0100,X
    INX
    LDA $02
    STA $06C3
    LDA #$01
    STA $0100,X
    INX
    LDA $06C0
    CLC
    ADC #$20
    STA $00
    LDA $06C1
    ADC #$00
    STA $0100,X
    INX
    LDA $00
    STA $0100,X
    INX
bottom:
    JSR $9880
    CMP #$80
    BCS @bottom_end
    JSR $9880
    STA $0100,X
    INX
    JMP @bottom
bottom_end:
    STA $00
    LDA #$FF
    STA $0100,X
    INX
    STX $1E
    JSR $93B5
    LDA $00
    CMP #$FE
    BEQ @line
    LDA #$00
    STA $0100,X
    STA $06C3
    STA $06C4
    RTS
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    out = a.output.resolve()
    out.relative_to(R / 'build')
    assert not out.exists()
    prior = R / 'build/opening11_poc_055'
    srcpath = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    prior_rom = prior / 'TinyToon2_Opening11_PoC055.nes'
    assert sha(prior_rom) == '8346499ca4240ffad350e3977f792735563779b8c749744a8d9b413ea0b44086'
    assert sha(srcpath) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    old = prior_rom.read_bytes()
    src = srcpath.read_bytes()
    new = bytearray(old)
    rows = list(csv.DictReader((R / 'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')))
    selected = [r for r in rows if r['kind'] == 'main' and r['status'] == 'draft'
                and 10 <= int(r['reference_ids'].split(',')[0], 16) <= 21]
    assert len(selected) == 12
    fontpath = R / 'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'
    assert sha(fontpath) == 'e24256f42e43713d2ea086a1e1669d78b968f5b3cc547e5c157f0606ffa5def1'
    face = ImageFont.truetype(str(fontpath), 12)
    ranges = []
    def put(bank, pc, data):
        assert 0x8000 <= pc and pc + len(data) <= 0xc000
        # pc may address private9 or canonical19 via the second mapped8K window.
        p = 16 + bank * 8192 + pc - 0x8000
        new[p:p + len(data)] = data
        ranges.append([p, p + len(data)])
    typed, tl, ts = assemble(GUARD.replace('$PRINTER', '$9800').replace('$FALLBACK', '$93E1'), 0x9630)
    instant_guard, gl, gs = assemble(GUARD.replace('$PRINTER', '$9700').replace('$FALLBACK', '$96FC'), 0x9690)
    fast, fl, fs = assemble(INSTANT, 0x9700)
    assert 0x9630 + len(typed) <= 0x9690
    assert 0x9690 + len(instant_guard) <= 0x96f0
    assert 0x9700 + len(fast) < 0x9800
    for bank in (18, 8):
        put(bank, 0x9630, typed)
        put(bank, 0x9690, instant_guard)
    put(18, 0x96fc, bytes.fromhex('a9 00 85 02 4c 62 92'))
    put(8, 0x9700, fast)
    assert old[0x25c91:0x25c94] == bytes.fromhex('20 e1 93')
    put(18, 0x9c81, bytes.fromhex('20 30 96'))
    assert old[0x2526e:0x25271] == bytes.fromhex('a9 00 85')
    put(18, 0x925e, bytes.fromhex('4c 90 96'))
    stream = 0xa100
    pages = []
    masks = []
    fonts = []
    for r in selected:
        page = int(r['reference_ids'], 16)
        lines = r['translation_ko'].split('\n')
        assert 1 <= len(lines) <= 2 and all(len(s) <= 14 for s in lines), (r['entry_id'], lines)
        im = Image.new('L', (168, len(lines) * 16))
        d = ImageDraw.Draw(im)
        for y, line in enumerate(lines):
            left = (168 - len(line) * 12) // 2
            for x, ch in enumerate(line):
                g = Image.new('L', (16, 16))
                ImageDraw.Draw(g).text((0, -1), ch, font=face, fill=2)
                assert ch.isspace() or g.getbbox(), (r['entry_id'], ch)
                d.text((left + x * 12, y * 16 - 1), ch, font=face, fill=2)
        assert set(im.get_flattened_data()) <= {0, 2}
        slots = {bytes(64): 0}
        font = bytearray(2048)
        codes = [[] for _ in range(len(lines) * 2)]
        body = bytearray()
        for y in range(len(lines)):
            for x in range(21):
                for half in range(2):
                    bits = bytes(im.crop((x * 8, y * 16 + half * 8, x * 8 + 8, y * 16 + half * 8 + 8)).get_flattened_data())
                    if bits not in slots:
                        code = len(slots)
                        assert code < 128
                        slots[bits] = code
                        raw = encode(bits)
                        assert decode(raw) == bits
                        font[code * 16:code * 16 + 16] = raw
                    code = slots[bits]
                    codes[y * 2 + half].append(code)
                    body.append(code)
            body.append(254 if y < len(lines) - 1 else 255)
        assert stream + len(body) < 0xc000 and len(body) < 256
        bank = old[0x5710 + page * 2]
        fonts.append(bank)
        assert [i for i in range(48) if old[0x5710 + i * 2] == bank] == [page], (page, bank)
        offset = 0x40010 + bank * 1024
        new[offset:offset + 2048] = font
        ranges.append([offset, offset + 2048])
        put(8, 0x9900 + page * 2, stream.to_bytes(2, 'little'))
        put(8, stream, body)
        pointer = int.from_bytes(old[0x255a9 + page * 2:0x255ab + page * 2], 'little')
        assert pointer == int(r['file_offset']) - 0x4010 + 0x8000
        pages.append({'page': page, 'entry_id': r['entry_id'], 'root': 8, 'original_pointer': pointer,
                      'original_text': r['translation_ko'], 'lines': lines, 'font_bank': bank,
                      'font_file_offset': offset, 'font_hex': font.hex(), 'font_unique_tiles': len(slots),
                      'stream_pointer': stream, 'body_hex': body.hex(), 'NT_top_origin': 0x22a8,
                      'NT_rows': codes, 'columns': 21, 'width_pixels': 168, 'cell': [12, 16]})
        masks.append((r['entry_id'], im))
        stream += len(body)
    put(18, 0x96f0, bytes(fonts))
    opening = json.loads((prior / 'opening11_plan.json').read_text('utf-8'))
    for z in opening['pages']:
        off = z['font_file_offset']
        assert new[off:off + 2048] == old[off:off + 2048]
        p = 0x10010 + z['stream_pointer'] - 0x8000
        n = len(bytes.fromhex(z['body_hex']))
        assert new[p:p + n] == old[p:p + n]
    assert new[:16] == old[:16] and new[0x3e010:0x40010] == old[0x3e010:0x40010]
    # Only12 identified font pairs and declared native/private code/data change.
    diff = [i for i, (a, b) in enumerate(zip(old, new)) if a != b]
    assert all(any(lo <= i < hi for lo, hi in ranges) for i in diff)
    writes = json.loads((prior / 'expected_writes.json').read_text('utf-8'))
    model = bytearray(src)
    owned = set()
    for w in writes:
        p, n = w['file_offset'], w['length']
        area = set(range(p, p + n))
        assert not area & owned and src[p:p + n] == bytes.fromhex(w['expected_hex'])
        owned |= area
        w['final_hex'] = bytes(new[p:p + n]).hex()
        model[p:p + n] = bytes.fromhex(w['final_hex'])
    assert model == new and apply(src, make(src, bytes(new))) == new
    out.mkdir()
    name = 'TinyToon2_HomeBooth11_Candidate057'
    (out / (name + '.nes')).write_bytes(new)
    (out / (name + '.ips')).write_bytes(make(src, bytes(new)))
    report = {'work': 199, 'output_rom': name + '.nes', 'output_sha256': sha(out / (name + '.nes')),
              'IPS_sha256': sha(out / (name + '.ips')), 'source_sha256': sha(srcpath), 'prior055_sha256': sha(prior_rom),
              'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'), 'output_size': len(new),
              'modified_bytes_vs055': len(diff), 'ordinary_entries_added': 12, 'opening9_055_data_unchanged': True,
              'HUD_STOP_compact_graphics_fixedIRQ_header_preserved': True,
              'scope': '057 development:055 opening9 + twelve home/booth lower text entries. No prose or bitmap changes.',
              'runtime': 'NOT_RUN; no new automatic play/controller experiment',
              'limits': ['No new Mesen/visual proof057; not final adoption/release',
                         'Other33 ordinary population now has21 entries remaining; credits3 separate',
                         'Canonical raw opening cave reuse and new private9 payload global reachability unresolved']}
    plan = {'pages': pages, 'typed_wrapper': 0x9630, 'instant_wrapper': 0x9690, 'instant_printer': 0x9700,
            'guard_font_table_PC': 0x96f0, 'native925E_fallback_PC': 0x96fc, 'allowed_ranges_vs055': ranges,
            'listing': {'typed': tl, 'instant_guard': gl, 'instant': fl},
            'symbols': {'typed': ts, 'instant_guard': gs, 'instant': fs}}
    for n, d in [('build_report.json', report), ('expected_writes.json', writes), ('homebooth11_plan.json', plan), ('opening11_plan.json', opening)]:
        (out / n).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    (out / 'builder_used.py').write_bytes(Path(__file__).read_bytes())
    (out / 'translation_used.csv').write_bytes((R / 'workspace/translation/text_ja.csv').read_bytes())
    for entry, im in masks:
        im.save(out / ('static_' + entry + '.png'))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
