"""058 all33 ordinary draft entries plus opening055, excluding compact graphic text."""
from pathlib import Path
import argparse
import csv
import json
from PIL import ImageFont
from asm6502 import assemble
from extract_title_png import encode, decode
from dialogue_ips import make, apply
from plan_remaining_text11_201_v2 import draw
from plan_text11_190 import family
from seal_nonplay171 import R, sha
from build_homebooth11_199 import INSTANT

GUARD = '''
    PHP
    PHA
    LDA $18
    CMP #$08
    BNE @fallback
    LDA $06CF
    CMP #$0A
    BCC @fallback
    CMP #$2D
    BCS @fallback
    CMP #$23
    BEQ @fallback
    ASL A
    TAY
    LDA $9599,Y
    CMP $06CD
    BNE @fallback
    LDA $959A,Y
    CMP $06CE
    BNE @fallback
    LDA #$08
    JSR $FDD3
    LDY $06CF
    LDA $99C0,Y
    CMP $C6
    BEQ @target
    CPY #$15
    BNE @restore
    LDA $C6
    CMP #$BE
    BNE @restore
target:
    PLA
    PLP
    JSR $PRINTER
    PHP
    PHA
    JSR $FDDB
    PLA
    PLP
    RTS
restore:
    JSR $FDDB
fallback:
    PLA
    PLP
    JMP $FALLBACK
'''

READER = '''
    LDA $06C4
    BEQ @raw
    DEC $06C4
    LDA $06C4
    PHA
    LDA #$00
    STA $06C4
    PLA
    RTS
raw:
    LDA $06CF
    ASL A
    TAY
    LDA $9900,Y
    STA $06
    LDA $9901,Y
    STA $07
    LDY $06C3
    LDA ($06),Y
    INC $06C3
    CMP #$FD
    BEQ @variable
    RTS
variable:
    LDY $06C3
    LDA ($06),Y
    INC $06C3
    CMP #$10
    BEQ @FA_tens
    CMP #$11
    BEQ @FA_ones
    CMP #$00
    BEQ @hundreds
    CMP #$01
    BNE @ones
    LDA $07D2
    BNE @tens
    LDA $07D1
    BEQ @blank
tens:
    LDA $07D1
    JMP @digit
hundreds:
    LDA $07D2
    BEQ @blank
    JMP @digit
ones:
    LDA $07D0
    JMP @digit
FA_tens:
    LDA $25
    ASL A
    TAY
    INY
    LDA $9370,Y
    BEQ @blank
    JMP @digit
FA_ones:
    LDA $25
    ASL A
    TAY
    LDA $9370,Y
    BNE @digit
    LDA $9371,Y
    BEQ @blank
    LDA #$00
digit:
    ASL A
    CLC
    ADC #$01
    PHA
    CLC
    ADC #$02
    STA $06C4
    PLA
    RTS
blank:
    LDA #$01
    STA $06C4
    LDA #$00
    RTS
'''

PRINTER = '''
    JSR $B100
    TAY
    CMP #$FF
    BEQ @terminator
    CMP #$FE
    BEQ @terminator
    JSR $9227
    CLC
    LDA $06C0
    ADC #$1F
    STA $06C0
    LDA $06C1
    ADC #$00
    STA $06C1
    JSR $B100
    JSR $9227
    SEC
    LDA $06C0
    SBC #$20
    STA $06C0
    LDA $06C1
    SBC #$00
    STA $06C1
    SEC
    RTS
terminator:
    JMP $93F0
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    a = ap.parse_args()
    out = a.output.resolve()
    out.relative_to(R / 'build')
    assert not out.exists()
    prior = R / 'build/homebooth11_candidate_057'
    original = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    old = (prior / 'TinyToon2_HomeBooth11_Candidate057.nes').read_bytes()
    assert sha(prior / 'TinyToon2_HomeBooth11_Candidate057.nes') == 'e2e388fe12d97c6a691e17174ba4cd368720788c140f3d60b4eccb70ef45ecef'
    assert sha(original) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    src = original.read_bytes()
    new = bytearray(old)
    new.extend(bytes(0x80010 - len(new)))
    new[5] = 32
    ranges = [[5, 6], [len(old), len(new)]]
    def put(bank, pc, data):
        p = 16 + bank * 8192 + pc - 0x8000
        assert 0x8000 <= pc and pc + len(data) <= 0xc000
        new[p:p + len(data)] = data
        ranges.append([p, p + len(data)])
    typed, tl, ts = assemble(GUARD.replace('$PRINTER', '$B300').replace('$FALLBACK', '$96F0'), 0x9630)
    fastguard, gl, gs = assemble(GUARD.replace('$PRINTER', '$B400').replace('$FALLBACK', '$96FC'), 0x9690)
    reader, rl, rs = assemble(READER, 0xb100)
    printer, pl, ps = assemble(PRINTER, 0xb300)
    instant, il, iss = assemble(INSTANT.replace('$9880', '$B100'), 0xb400)
    assert 0x9630 + len(typed) <= 0x9690 and 0x9690 + len(fastguard) <= 0x96f0
    assert 0xb100 + len(reader) < 0xb300 and 0xb300 + len(printer) < 0xb400 and 0xb400 + len(instant) < 0xb600
    for bank in (18, 8):
        put(bank, 0x9630, typed)
        put(bank, 0x9690, fastguard)
    put(18, 0x96f0, bytes.fromhex('20 7c 93 4c e4 93'))
    assert old[0x253f1:0x253f4] == bytes.fromhex('20 7c 93')
    put(18, 0x93e1, bytes.fromhex('4c 30 96'))
    put(8, 0xb100, reader)
    put(8, 0xb300, printer)
    put(8, 0xb400, instant)
    # Existing0579C81 and925E calls enter the new guards; other93E1 callers now join.
    assert new[0x25c91:0x25c94] == bytes.fromhex('20 30 96')
    assert new[0x2526e:0x25271] == bytes.fromhex('4c 90 96')
    fontpath = R / 'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'
    face = ImageFont.truetype(str(fontpath), 12)
    rows = [r for r in csv.DictReader((R / 'workspace/translation/text_ja.csv').open(encoding='utf-8-sig'))
            if r['kind'] == 'main' and r['status'] == 'draft'
            and 10 <= int(r['reference_ids'].split(',')[0], 16) <= 44]
    assert len(rows) == 33
    upper_banks = iter(range(233, 252, 2))
    fonts = {}
    pages = []
    stream = 0xa100
    guardfonts = bytearray(48)
    masks = []
    for r in rows:
        page = int(r['reference_ids'].split(',')[0], 16)
        aliases = [int(i, 16) for i in r['reference_ids'].split(',')]
        group = family(page)
        width = 192 if group.startswith('ride_upper') else 168
        columns = width // 8
        text = r['translation_ko']
        variable = 'FA' if '{variable_FA}' in text else 'F8' if '{variable_F8}' in text else None
        example = text.replace('{variable_FA}', '\x01  \x02').replace('{variable_F8}', '\x01  0\x02')
        image, tiles, fields = draw(example, width, face)
        assert len(text.split('\n')) <= 2
        bank = next(upper_banks) if group.startswith('ride_upper') else 254 if page == 0x2b else old[0x5710 + page * 2]
        slots = fonts.setdefault(bank, {'bits': {bytes(64): 0}, 'data': bytearray(2048), 'next': 1})
        if variable and slots['next'] == 1:
            for n in range(10):
                glyph, _, _ = draw('\x01' + str(n) + '\x02', 8, face)
                for half in range(2):
                    bits = bytes(glyph.crop((0, half * 8, 8, half * 8 + 8)).get_flattened_data())
                    code = 2 * n + half + 1
                    raw = encode(bits)
                    assert decode(raw) == bits
                    slots['data'][code * 16:code * 16 + 16] = raw
                    slots['bits'].setdefault(bits, code)
            slots['next'] = 21
        field_positions = {(f['x'] // 8, f['y'] // 16): i for i, f in enumerate(fields)}
        codes = [[] for _ in range(image.height // 8)]
        body = bytearray()
        for y in range(image.height // 16):
            for x in range(columns):
                if (x, y) in field_positions:
                    i = field_positions[x, y]
                    body.extend((253, (0x10 + i) if variable == 'FA' else i))
                    # Initial sample uses native leading blanks and trailing zero forF8.
                    c = fields[i]['char']
                    pair = [0, 0] if c == ' ' else [2 * int(c) + 1, 2 * int(c) + 2]
                    for half in range(2):
                        codes[y * 2 + half].append(pair[half])
                    continue
                for half in range(2):
                    bits = bytes(image.crop((x * 8, y * 16 + half * 8, x * 8 + 8, y * 16 + half * 8 + 8)).get_flattened_data())
                    if bits not in slots['bits']:
                        code = slots['next']
                        assert code < 128, (r['entry_id'], bank, code)
                        slots['next'] += 1
                        slots['bits'][bits] = code
                        raw = encode(bits)
                        assert decode(raw) == bits
                        slots['data'][code * 16:code * 16 + 16] = raw
                    code = slots['bits'][bits]
                    codes[y * 2 + half].append(code)
                    body.append(code)
            body.append(254 if y < image.height // 16 - 1 else 255)
        assert len(body) < 256 and stream + len(body) < 0xb100
        for native in aliases:
            guardfonts[native] = bank
            put(8, 0x9900 + native * 2, stream.to_bytes(2, 'little'))
            p = 0x5710 + native * 2
            new[p] = bank
            ranges.append([p, p + 1])
        put(8, stream, body)
        pointer = int.from_bytes(old[0x255a9 + page * 2:0x255ab + page * 2], 'little')
        origin = 0x2125 if group == 'ride_upper_rule' else 0x20a6 if group == 'ride_upper_title' else 0x22a8
        pages.append({'page': page, 'aliases': aliases, 'entry_id': r['entry_id'], 'root': 8, 'family': group,
                      'original_pointer': pointer, 'original_text': text, 'variable': variable,
                      'font_bank': bank, 'font_file_offset': 0x40010 + bank * 1024,
                      'stream_pointer': stream, 'body_hex': body.hex(), 'NT_top_origin': origin,
                      'NT_rows': codes, 'columns': columns, 'width_pixels': width, 'cell': [12, 16],
                      'variable_fields': fields, 'static_sample': example})
        masks.append((r['entry_id'], image))
        stream += len(body)
    assert len([z for z in pages if z['family'].startswith('ride_upper')]) == 10
    put(8, 0x99c0, guardfonts)
    for bank, f in fonts.items():
        off = 0x40010 + bank * 1024
        new[off:off + 2048] = f['data']
        ranges.append([off, off + 2048])
    # Native15 has an already-established second lower font190 in ride context.
    f15 = fonts[188]['data']
    off190 = 0x40010 + 190 * 1024
    new[off190:off190 + 2048] = f15
    ranges.append([off190, off190 + 2048])
    for z in pages:
        z['font_hex'] = bytes(fonts[z['font_bank']]['data']).hex()
        z['font_slots_allocated'] = fonts[z['font_bank']]['next']
    opening = json.loads((prior / 'opening11_plan.json').read_text('utf-8'))
    for z in opening['pages']:
        p = z['font_file_offset']
        assert new[p:p + 2048] == old[p:p + 2048]
        p = 0x10010 + z['stream_pointer'] - 0x8000
        n = len(bytes.fromhex(z['body_hex']))
        assert new[p:p + n] == old[p:p + n]
    # Source and native graphical CHR are preserved; only selected text font pairs differ.
    assert new[:5] == old[:5] and new[6:16] == old[6:16]
    assert new[0x3e010:0x40010] == old[0x3e010:0x40010]
    assert new[0x40010:0x60010] == old[0x40010:0x60010]
    diff = [i for i, (x, y) in enumerate(zip(old, new)) if x != y]
    assert all(any(lo <= i < hi for lo, hi in ranges) for i in diff)
    writes = json.loads((prior / 'expected_writes.json').read_text('utf-8'))
    model = bytearray(src)
    owned = set()
    for w in writes:
        p, n = w['file_offset'], w['length']
        if p == 0x20010:
            n = len(new) - p
            w['length'] = n
        area = set(range(p, p + n))
        assert not area & owned and src[p:p + n] == bytes.fromhex(w['expected_hex'])
        owned |= area
        w['final_hex'] = bytes(new[p:p + n]).hex()
        model[p:p + n] = bytes.fromhex(w['final_hex'])
    assert model == new and apply(src, make(src, bytes(new))) == new
    out.mkdir()
    name = 'TinyToon2_Ordinary11_Candidate058'
    (out / (name + '.nes')).write_bytes(new)
    (out / (name + '.ips')).write_bytes(make(src, bytes(new)))
    report = {'work': 203, 'output_rom': name + '.nes', 'output_sha256': sha(out / (name + '.nes')),
              'IPS_sha256': sha(out / (name + '.ips')), 'source_sha256': sha(original),
              'prior057_sha256': sha(prior / 'TinyToon2_HomeBooth11_Candidate057.nes'),
              'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'), 'output_size': len(new),
              'ordinary_entries': 33, 'opening_entries_preserved': 9, 'credits_remaining8px': 3,
              'CHR_KiB': 256, 'modified_old_bytes_vs057': len(diff), 'new_padding_bytes': len(new) - len(old),
              'runtime': 'NOT_RUN', 'CPU': 'PENDING', 'distribution_eligible': False,
              'scope': '058 unverified development candidate:42registered ordinary/opening drafts11px. Credits and compact bitmap text unchanged.',
              'limits': ['Final CPU and runtime font life/geometry/NMI/IRQ/CHR256 mapping required',
                         'No new controller/gameplay experiment; user owns play review',
                         'New guard/private payload reachability not globally closed']}
    plan = {'pages': pages, 'typed_wrapper': 0x9630, 'instant_wrapper': 0x9690,
            'reader_PC': 0xb100, 'printer_PC': 0xb300, 'instant_PC': 0xb400,
            'allowed_ranges_vs057': ranges, 'stream_end': stream,
            'font_banks': {str(k): f['next'] for k, f in fonts.items()},
            'listing': {'typed': tl, 'instant_guard': gl, 'reader': rl, 'printer': pl, 'instant': il},
            'symbols': {'typed': ts, 'instant_guard': gs, 'reader': rs, 'printer': ps, 'instant': iss}}
    for n, value in [('build_report.json', report), ('ordinary11_plan.json', plan), ('opening11_plan.json', opening), ('expected_writes.json', writes)]:
        (out / n).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    (out / 'builder_used.py').write_bytes(Path(__file__).read_bytes())
    (out / 'translation_used.csv').write_bytes((R / 'workspace/translation/text_ja.csv').read_bytes())
    for entry, im in masks:
        im.save(out / ('static_' + entry + '.png'))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
