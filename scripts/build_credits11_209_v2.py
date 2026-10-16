"""060:059 preserved, all three credits enlarged with original progressive call counts."""
from pathlib import Path
import argparse
import csv
import json
from asm6502 import assemble
from dialogue_ips import make, apply
from build_ordinary11_204 import GUARD
from seal_nonplay171 import R, sha

WRAPPER = '''
 PHP
 PHA
 LDA #$08
 JSR $FDD3
 PLA
 PLP
 JSR $B700
 PHP
 PHA
 JSR $FDDB
 PLA
 PLP
 RTS
'''
DISPATCH = '''
 PHP
 PHA
 LDA $18
 CMP #$07
 BNE @ordinary
 LDA $06CF
 CMP #$2D
 BCC @ordinary
 CMP #$30
 BCS @ordinary
 LDA $C6
 CMP #$C9
 BNE @ordinary
 LDA $06CF
 ASL A
 TAY
 LDA $9599,Y
 CMP $06CD
 BNE @ordinary
 LDA $959A,Y
 CMP $06CE
 BNE @ordinary
 LDA $06CF
 CMP #$2D
 BEQ @initial
 PLA
 PLP
 JMP $B900
initial:
 PLA
 PLP
 JMP $BB00
ordinary:
 PLA
 PLP
 JMP $B800
'''
DESCRIPTOR = '''
 LDA $06CF
 SEC
 SBC #$2D
 ASL A
 TAY
 LDA $AA00,Y
 STA $06
 LDA $AA01,Y
 STA $07
 LDA $06C4
 ASL A
 ASL A
 TAY
 LDA ($06),Y
 TAX
 INY
 LDA ($06),Y
 PHA
 INY
 LDA ($06),Y
 STA $03
 STX $06
 PLA
 STA $07
 LDA $03
 ASL A
 TAY
 LDA $9F80,Y
 STA $08
 LDA $9F81,Y
 STA $09
 RTS
'''
TYPED = '''
 JSR $BA80
 LDA $06C3
 CMP $03
 BCS @line_end
 TAY
 LDA ($08),Y
 STA $04
 INY
 LDA ($08),Y
 STA $05
 INC $06C3
 CMP $04
 BEQ @empty
 LDA $06D1
 CLC
 ADC $04
 STA $00
 LDA $06D2
 ADC #$00
 STA $01
 LDY $04
 JSR $BA00
 LDA $00
 CLC
 ADC #$20
 STA $00
 LDA $01
 ADC #$00
 STA $01
 LDA $05
 CLC
 ADC #$1B
 STA $05
 LDA $04
 CLC
 ADC #$1B
 TAY
 JSR $BA00
empty:
 SEC
 RTS
line_end:
 LDA $06C4
 CLC
 ADC #$01
 PHA
 JSR $93B5
 PLA
 STA $06C4
 LDA #$00
 STA $06C3
 LDA #$07
 STA $58
 LDA $06CF
 SEC
 SBC #$2D
 TAX
 LDA $06C4
 CMP $9FC6,X
 BCC @empty
 LDA #$00
 STA $06C3
 STA $06C4
 INC $06CF
 LDA #$60
 STA $58
 CLC
 RTS
'''
EMIT = '''
 LDX $1E
 LDA #$01
 STA $0100,X
 INX
 LDA $01
 STA $0100,X
 INX
 LDA $00
 STA $0100,X
 INX
pixels:
 LDA ($06),Y
 STA $0100,X
 INX
 INY
 CPY $05
 BCC @pixels
 LDA #$FF
 STA $0100,X
 INX
 STX $1E
 LDA #$00
 STA $0100,X
 RTS
'''
INITIAL = '''
 JSR $FF31
 LDA $FF
 AND #$7B
 STA $2000
 LDA #$00
 STA $06C3
 STA $06C4
line:
 JSR $BA80
 BIT $2002
 LDA $06D2
 STA $2006
 LDA $06D1
 STA $2006
 LDY #$00
top:
 LDA ($06),Y
 STA $2007
 INY
 CPY #$1B
 BCC @top
 BIT $2002
 LDA $06D1
 CLC
 ADC #$20
 TAX
 LDA $06D2
 ADC #$00
 STA $2006
 STX $2006
bottom:
 LDA ($06),Y
 STA $2007
 INY
 CPY #$36
 BCC @bottom
 LDA $06C4
 CLC
 ADC #$01
 PHA
 JSR $93B5
 PLA
 STA $06C4
 CMP #$0E
 BCC @line
 LDA #$00
 STA $06C3
 STA $06C4
 JMP $FF17
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    out = ap.parse_args().output.resolve()
    out.relative_to(R / 'build')
    assert not out.exists()
    prior = R / 'build/ordinary11_candidate_059'
    target = prior / 'TinyToon2_Ordinary11_Candidate059.nes'
    original = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    assert sha(target) == '8b44d79b19c490dc6c5e2f3dcf73d08d1716ab981b62878067043a5600f59930'
    assert sha(original) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    old = target.read_bytes()
    new = bytearray(old)
    src = original.read_bytes()
    ranges = []
    def put(bank, pc, value):
        assert 0x8000 <= pc and pc + len(value) <= 0xc000
        p = 16 + bank * 8192 + pc - 0x8000
        new[p:p + len(value)] = value
        ranges.append([p, p + len(value)])
    listing = {}
    for label, bank, pc, limit, code in [
        ('wrapper', 18, 0x9630, 0x9690, WRAPPER),
        ('wrapper_mirror', 8, 0x9630, 0x9690, WRAPPER),
        ('dispatch', 8, 0xb700, 0xb800, DISPATCH),
        ('ordinary_guard', 8, 0xb800, 0xb900, GUARD.replace('$PRINTER', '$B300').replace('$FALLBACK', '$96F0')),
        ('credits_typed', 8, 0xb900, 0xba00, TYPED),
        ('packet', 8, 0xba00, 0xba80, EMIT),
        ('descriptor', 8, 0xba80, 0xbb00, DESCRIPTOR),
        ('initial_direct', 8, 0xbb00, 0xbc00, INITIAL)]:
        raw, text, symbols = assemble(code, pc)
        assert pc + len(raw) <= limit, label
        put(bank, pc, raw)
        listing[label] = {'PC': pc, 'bytes': len(raw), 'listing': text, 'symbols': symbols}
    assert old[0x26458:0x2645b] == bytes.fromhex('20 5e 92')
    put(18, 0xa448, bytes.fromhex('20 30 96'))
    measured = json.loads((R / 'qa/reports/credits11_202_capacity.json').read_text('utf-8'))['cases'][1]
    assert measured['shared_three_page_tiles'] == 106
    native = json.loads((R / 'build/dialogue_kr_poc_037/ui_korean_page_mapping.json').read_text('utf-8'))
    rows = {r['entry_id']: r for r in csv.DictReader((R / 'workspace/translation/text_ja.csv').open(encoding='utf-8-sig'))}
    font = (R / 'workspace/review/credits11_202/credits11_latin16_font.chr').read_bytes()
    assert len(font) == 2048
    fontoff = 0x40010 + 201 * 1024
    new[fontoff:fontoff + 2048] = font
    ranges.append([fontoff, fontoff + 2048])
    descriptor_pc = 0xaa06
    payload_pc = 0xaa06 + 35 * 4
    zero_pc = payload_pc
    put(8, zero_pc, bytes(54))
    payload_pc += 54
    pages = []
    for index, z in enumerate(measured['pages']):
        text = rows[z['entry_id']]['translation_ko']
        assert z['unaltered_text'] == text
        previous = next(p for p in native if p['profile']['entry_id'] == z['entry_id'])
        slot = 45 + index
        assert previous['profile']['slot'] == slot
        nativecounts = [line['expanded_tiles'] for line in previous['layout']]
        assert len(nativecounts) == len(z['lines'])
        put(8, 0xaa00 + index * 2, descriptor_pc.to_bytes(2, 'little'))
        descriptors = []
        for y, count in enumerate(nativecounts):
            assert 1 <= count <= 32
            upper, lower = z['NT_rows'][y * 2:y * 2 + 2]
            assert not any(upper[27:]) and not any(lower[27:])
            data = bytes(upper[:27] + lower[:27])
            at = payload_pc if any(data) else zero_pc
            if any(data):
                put(8, at, data)
                payload_pc += len(data)
            put(8, descriptor_pc, at.to_bytes(2, 'little') + bytes((count, 0)))
            descriptor_pc += 4
            descriptors.append({'line': y, 'NT_top': previous['profile']['NT'] + y * 64,
                                'data_PC': at, 'native_event_count': count, 'tiles': list(data)})
        put(8, 0x9fc6 + index, bytes((len(descriptors),)))
        pointer = int.from_bytes(old[0x255a9 + slot * 2:0x255ab + slot * 2], 'little')
        pages.append({'entry_id': z['entry_id'], 'page': slot, 'original_pointer': pointer,
                      'font_bank': 201, 'font_file_offset': fontoff, 'root': 7,
                      'original_text': text, 'width_pixels': 216, 'columns': 27,
                      'NT_top_origin': previous['profile']['NT'], 'lines': z['lines'],
                      'NT_rows': [line[:27] for line in z['NT_rows']], 'descriptors': descriptors,
                      'native_calls': sum(nativecounts) + len(nativecounts)})
    assert payload_pc < 0xb100, hex(payload_pc)
    maps = 0xbd00
    for count in range(1, 33):
        put(8, 0x9f80 + count * 2, maps.to_bytes(2, 'little'))
        span = bytes(27 * i // count for i in range(count + 1))
        put(8, maps, span)
        maps += len(span)
    assert maps < 0xc000
    diff = [i for i, (x, y) in enumerate(zip(old, new)) if x != y]
    assert all(any(lo <= i < hi for lo, hi in ranges) for i in diff)
    assert new[:16] == old[:16] and new[0x3c010:0x60010] == old[0x3c010:0x60010]
    ordinary = json.loads((prior / 'ordinary11_plan.json').read_text('utf-8'))
    opening = json.loads((prior / 'opening11_plan.json').read_text('utf-8'))
    for z in ordinary['pages'] + opening['pages']:
        p = z['font_file_offset']
        assert new[p:p + 2048] == old[p:p + 2048]
        p = 0x10010 + z['stream_pointer'] - 0x8000
        n = len(bytes.fromhex(z['body_hex']))
        assert new[p:p + n] == old[p:p + n]
    writes = json.loads((prior / 'expected_writes.json').read_text('utf-8'))
    model = bytearray(src)
    owned = set()
    # New private code fits the already owned expansion writes.
    for w in writes:
        p, n = w['file_offset'], w['length']
        area = set(range(p, p + n))
        assert not owned & area and src[p:p + n] == bytes.fromhex(w['expected_hex'])
        owned |= area
        w['final_hex'] = bytes(new[p:p + n]).hex()
        model[p:p + n] = bytes.fromhex(w['final_hex'])
    assert model == new, 'Private patches must remain within source ExpectedWrites'
    assert apply(src, make(src, new)) == new
    out.mkdir()
    name = 'TinyToon2_Text11_Candidate060'
    (out / (name + '.nes')).write_bytes(new)
    (out / (name + '.ips')).write_bytes(make(src, new))
    report = {'work': 209, 'output_rom': name + '.nes', 'output_sha256': sha(out / (name + '.nes')),
              'IPS_sha256': sha(out / (name + '.ips')), 'prior059_sha256': sha(target),
              'source_sha256': sha(original), 'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'),
              'output_size': len(new), 'registered45_11px': True, 'ordinary_preserved': 33,
              'opening_preserved': 9, 'credits11px': 3, 'font_slots': 106,
              'native_progressive_credit_call_counts': [z['native_calls'] for z in pages],
              'changed_bytes_vs059': len(diff), 'runtime060': 'NOT_RUN', 'CPU': 'PENDING',
              'distribution_eligible': False, 'adopted': False,
              'limits': ['Native controller/fullplay not run; asynchronousNMI/IRQ hardware rendering unverified',
                         'Credit11px Latin16 spacing is development candidate; names/legal text preserved but original glyph bitmaps enlarged',
                         'Initial guard consumer and new private bank code other reachability not globally closed']}
    plan = {'pages': pages, 'font_hex': font.hex(), 'font_slots': 106,
            'initial_consumer': 0xa448, 'initial_direct_PC': 0xbb00, 'typed_PC': 0xb900,
            'descriptors_end': descriptor_pc, 'payload_end': payload_pc, 'maps_end': maps,
            'listing': listing, 'allowed_ranges_vs059': ranges}
    for n, value in [('build_report.json', report), ('credits11_plan.json', plan),
                     ('ordinary11_plan.json', ordinary), ('opening11_plan.json', opening), ('expected_writes.json', writes)]:
        (out / n).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    (out / 'builder_used.py').write_bytes(Path(__file__).read_bytes())
    (out / 'translation_used.csv').write_bytes((R / 'workspace/translation/text_ja.csv').read_bytes())
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
