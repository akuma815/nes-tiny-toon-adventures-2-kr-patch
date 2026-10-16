"""Decode the unconnected NT1C, keeping font assumptions distinct from consumers."""
from pathlib import Path
import collections
import hashlib
import json
from title_codec import unpack
from verify_dialogue_home import MPU
from verify_booth_native_decoder import Ports

R = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out = R / 'qa/reports/candidate119_NT1C.json'
    assert not out.exists()
    source = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    current = R / 'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
    src, rom = source.read_bytes(), current.read_bytes()
    assert sha(source) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(current) == '82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
    pointer = int.from_bytes(src[0x40ed:0x40ef], 'little')
    assert pointer == 0x8bf9
    start = 0x4010 + pointer - 0x8000
    nt, n = unpack(src[start:0x8010])
    assert start == 0x4c09 and n == 99 and set(nt) == set(range(0x2000, 0x2400))
    assert src[start:start+n] == rom[start+0x20000:start+0x20000+n]
    cases = []
    for flags in range(256):
        if flags & 8:
            continue
        states = []
        for data in (src, rom):
            mem = Ports(data); cpu = MPU(memory=mem); mem.cpu = cpu
            cpu.pc = 0x803f; cpu.p = flags; cpu.sp = 0xfd
            mem.ram[:2] = pointer.to_bytes(2, 'little')
            instructions = 0
            while cpu.pc != 0x80be:
                cpu.step(); instructions += 1
                assert instructions < 50000
            assert len(mem.nt) == 1024 and {a: v for a, v, t in mem.nt} == nt
            states.append((cpu.a, cpu.x, cpu.y, cpu.p, cpu.sp, cpu.processorCycles,
                           instructions, bytes(mem.ram), mem.nt))
        assert states[0] == states[1]
        cases.append({'flags': flags, 'cycles': states[0][5], 'instructions': states[0][6]})
    howto = set(range(0x90, 0x97))
    # Source extraction crop x80..127,y0..31 -> 6x4 tiles on a 16-tile-wide page.
    pause_local = [row * 16 + col for row in range(4) for col in range(10, 16)]
    pause_bg = {0x80 + x for x in pause_local}
    tilecells = {a: v for a, v in nt.items() if a < 0x23c0}
    overlaps = {label: [{'NT_hex': f'{a:04X}', 'tile_hex': f'{v:02X}'}
                         for a, v in tilecells.items() if v in wanted]
                for label, wanted in [('HOWTO_assuming_bank116_at0800', howto),
                                      ('PAUSE_assuming_bank120_at0800', pause_bg)]}
    assert all(not cells for cells in overlaps.values())
    high = [{'NT_hex': f'{a:04X}', 'tile_hex': f'{v:02X}'} for a, v in tilecells.items() if v >= 0x80]
    assert len(high) == 48 and {int(x['tile_hex'], 16) for x in high} == set(range(0xb0, 0xba))
    references = ['qa/reports/candidate099_bank_nt.json', 'qa/reports/pause101_supply_bounds.json',
                  'qa/reports/animation102_bank36.json', 'qa/reports/latch103_supply.json',
                  'qa/reports/nt112_supplier_bounds.json',
                  'workspace/review/consumer047_104_20261005/consumer_records.json']
    result = {'work': 119, 'status': 'PASS_NT1C_DECODER_AND_CONDITIONAL_TILE_BOUNDS',
              'source_sha256': sha(source), 'ROM047_sha256': sha(current),
              'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'),
              'source_pointer_file_offset_hex': '40ED', 'native_pointer_CPU_hex': '8BF9',
              'source_stream_file_offset_hex': '4C09', 'current_stream_file_offset_hex': '24C09',
              'encoded_bytes': n, 'encoded_sha256': hashlib.sha256(src[start:start+n]).hexdigest(),
              'decoded_cells': 1024, 'tile_cells': 960, 'attribute_cells': 64,
              'D_clear_CPU_case_pairs': len(cases), 'cases': cases,
              'tile_histogram': {f'{k:02X}': v for k, v in sorted(collections.Counter(tilecells.values()).items())},
              'high_tile_cells': high, 'conditional_candidate_intersections': overlaps,
              'raw_source_bounds_preserved': {p: sha(R / p) for p in references},
              'limits': ['NT1C font producer and actual 8025 invocation remain unconnected. No actual display or language identification for its remaining tiles.',
                         'Zero intersections assume the named background bank at0800. Does not exclude different font mappings, sprite overlay, extra PPU commands or other scenes.',
                         'CPU tests start at803F with a deliberately supplied source pointer, not a natural caller. D-set, async IRQ/NMI and real PPU excluded.',
                         'HOWTO/PAUSE candidate preservation and review decisions remain pending. No global-unused or full-corpus closure.',
                         'No emulator run, new build/apply or original/ROM/CSV edit.'],
              'release_eligible': False}
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(result['status'], 'CPU pairs', len(cases), 'NT cells', len(nt), 'candidate intersections 0')

if __name__ == '__main__':
    main()
