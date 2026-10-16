"""Final059: all33 entries/1000F8/sixFA, all default skip points and native fallback."""
from pathlib import Path
import json
from PIL import Image, ImageFont
from extract_title_png import decode
from compile_ui_card_group import variable_codes
from plan_text11_190 import F8_values
from plan_remaining_text11_201_v2 import draw
from verify_home11_cpu191 import run, paragraph
from verify_opening11_cpu186_v2 import Memory
from verify_homebooth11_199 import queue, native_init
from verify_ui_native_latch_hooks import irq
from seal_nonplay171 import R, sha


def initial(rom, z, number=0, ride=0):
    m = Memory(rom)
    r = m.ram
    r[0x18] = 8
    r[0x6cf] = z['page']
    r[0xc6] = z['font_bank']
    r[0x6cd:0x6cf] = z['original_pointer'].to_bytes(2, 'little')
    r[0x6d1:0x6d3] = z['NT_top_origin'].to_bytes(2, 'little')
    r[0x6c0:0x6c2] = z['NT_top_origin'].to_bytes(2, 'little')
    r[0x2b] = 0x32
    r[0x25] = ride
    r[0x7d0:0x7d3] = bytes((number % 10, number // 10 % 10, number // 100))
    return m


def pixels(rom, z, writes):
    im = Image.new('L', (z['width_pixels'], len(z['NT_rows']) * 8))
    base = z['font_file_offset']
    for y in range(len(z['NT_rows'])):
        for x in range(z['columns']):
            code = writes[z['NT_top_origin'] + y * 32 + x]
            im.paste(Image.frombytes('L', (8, 8), decode(rom[base + code * 16:base + code * 16 + 16])), (x * 8, y * 8))
    return im


def progressive(rom, z, number=0, ride=0):
    m = initial(rom, z, number, ride)
    r = m.ram
    body = bytes.fromhex(z['body_hex'])
    writes = {}
    cursor = 0
    max_cycles = 0
    calls = 0
    while cursor < len(body):
        first = body[cursor]
        r[0x1e] = 0
        r[0x100:0x140] = bytes(64)
        c = run(m, 0x93e1)
        calls += 1
        max_cycles = max(max_cycles, c.processorCycles)
        assert m.banks == [18, 19] and r[0x2b] == 0x32 and r[0x6c4] == 0
        if first < 128 or first == 253:
            assert r[0x1e] == 10 and c.p & 1
            for at in (0x100, 0x105):
                assert r[at] == 1 and r[at + 4] == 255
                addr = r[at + 1] * 256 + r[at + 2]
                writes[addr] = r[at + 3]
            cursor += 2
        else:
            assert first in (254, 255) and r[0x1e] == 0
            assert bool(c.p & 1) == (first == 254)
            cursor += 1
        assert r[0x6c3] == (0 if first == 255 else cursor)
    assert r[0x6cf] == z['page'] + 1
    return writes, calls, max_cycles


def main():
    folder = R / 'build/text11_candidate_062'
    path = folder / 'TinyToon2_Text11_Candidate062.nes'
    rom = path.read_bytes()
    old = (R / 'build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes').read_bytes()
    plan = json.loads((folder / 'ordinary11_plan.json').read_text('utf-8'))
    out = R / 'qa/reports/text11_211_ordinary_CPU.json'
    assert not out.exists()
    source = (R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes').read_bytes()
    prices = [''.join(' ' if c == 0 else str(c - 0x70) for c in variable_codes(source, ride)) for ride in range(6)]
    tickets = F8_values(source)
    face = ImageFont.truetype(str(R / 'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'), 12)
    results = []
    snapshots = {}
    for z in plan['pages']:
        variants = [(0, i) for i in range(6)] if z['variable'] == 'FA' else [(n, 0) for n in range(1000)] if z['variable'] == 'F8' else [(0, 0)]
        worst = 0
        for number, ride in variants:
            typed, calls, cycles = progressive(rom, z, number, ride)
            m = initial(rom, z, number, ride)
            c = run(m, 0x925e)
            immediate = queue(m.ram)
            frame = {int(k): v for k, v in plan['title_frame_repair_cells'].items()} if z['family'] == 'ride_upper_title' else {}
            assert immediate == {**typed, **frame}, (z['entry_id'], number, ride)
            assert m.banks == [18, 19] and m.ram[0x2b] == 0x32 and m.ram[0x6cf] == z['page']
            assert m.ram[0x6c3] == m.ram[0x6c4] == 0 and m.ram[0x1e] <= 112
            template = z['original_text'].replace('{variable_FA}', '\x01' + prices[ride] + '\x02').replace('{variable_F8}', '\x01' + tickets[number] + '\x02')
            expected, _, _ = draw(template, z['width_pixels'], face)
            assert pixels(rom, z, typed).tobytes() == expected.tobytes(), (z['entry_id'], number, ride)
            worst = max(worst, c.processorCycles)
            if number == 0 and ride == 0:
                snapshots[z['entry_id']] = typed
        # Every partial output boundary with default variables, including afterFE.
        m = initial(rom, z)
        printed = {}
        body = bytes.fromhex(z['body_hex'])
        cursor = 0
        skips = 0
        while True:
            q = initial(rom, z)
            q.ram[:] = m.ram
            q.ram[0x1e] = 0
            q.ram[0x100:0x1c0] = bytes(0xc0)
            run(q, 0x925e)
            rest = queue(q.ram)
            frame = {int(k): v for k, v in plan['title_frame_repair_cells'].items()} if z['family'] == 'ride_upper_title' else {}
            assert {**printed, **rest} == {**snapshots[z['entry_id']], **frame}, (z['entry_id'], cursor)
            skips += 1
            if body[cursor] == 255:
                break
            m.ram[0x1e] = 0
            m.ram[0x100:0x140] = bytes(64)
            run(m, 0x93e1)
            if body[cursor] < 128 or body[cursor] == 253:
                for at in (0x100, 0x105):
                    addr = m.ram[at + 1] * 256 + m.ram[at + 2]
                    printed[addr] = m.ram[at + 3]
                cursor += 2
            else:
                assert body[cursor] == 254
                cursor += 1
        # Lower five-row geometry is independently bounded; upper lifetime pending.
        if not z['family'].startswith('ride_upper'):
            cleared = {0x22a7 + y * 32 + x for y in range(5) for x in range(22)}
            assert set(snapshots[z['entry_id']]) <= cleared
        results.append({'entry_id': z['entry_id'], 'variant_cases': len(variants), 'progressive_calls': calls,
                        'all_variant_glyph_pixels_exact': True, 'all_variant_instant_equals_typed': True,
                        'all_default_skip_boundaries': skips, 'max_instant_cycles': worst,
                        'max_typed_cycles': cycles, 'font_slots': z['font_slots_allocated'],
                        'actual_upper_window_clear_and_NMI_budget': 'NOT_VERIFIED'})
    # Established second native15 font190 uses the same new sentence pixels.
    z15 = next(z for z in plan['pages'] if z['page'] == 21)
    m = initial(rom, z15)
    m.ram[0xc6] = 190
    run(m, 0x925e)
    assert queue(m.ram) == snapshots[z15['entry_id']]
    intro_plan = json.loads((folder / 'opening11_plan.json').read_text('utf-8'))
    intro = [paragraph(rom, z, 0x95f9, 7, 0x21e4, 24)[0] for z in intro_plan['pages']]
    # Original initializer ABI/cycles, with the explicitly changed font values only.
    init_count = 0
    retention = 0
    for slot in range(48):
        for mode in (0, 1, 4):
            for ride in (0, 3, 6):
                for active in (90, 130, 162, 188, 196):
                    for phase in (0, 3):
                        ca, ma = native_init(old, slot, mode, ride, active, phase)
                        cb, mb = native_init(rom, slot, mode, ride, active, phase)
                        assert (ca.a, ca.x, ca.y, ca.p, ca.sp, ca.processorCycles) == (cb.a, cb.x, cb.y, cb.p, cb.sp, cb.processorCycles)
                        assert ma.banks == mb.banks
                        for i in range(0x800):
                            if i in (0xc6, 0x6f3, 0x34) or 0x100 <= i < 0x200:
                                continue
                            assert ma.ram[i] == mb.ram[i], (slot, mode, ride, active, phase, i)
                        oldfont = old[0x5710 + slot * 2]
                        newfont = rom[0x5710 + slot * 2]
                        expected = newfont if ma.ram[0xc6] == oldfont else ma.ram[0xc6]
                        #010 deliberately retains the resident font during clear,
                        #even when it happens to equal the old table font196.
                        if slot in (0x29, 0x2b) and phase == 0:
                            expected = active
                        assert mb.ram[0xc6] == mb.ram[0x6f3] == expected
                        expectedtop = newfont if oldfont != newfont and ma.ram[0x34] == oldfont else ma.ram[0x34]
                        assert mb.ram[0x34] == expectedtop
                        if slot == 0x23 and ride == 6 and mode == 4:
                            assert mb.ram[0xc6] == active
                            retention += 1
                        init_count += 1
    assert irq(old) == irq(rom)
    # Title/rule co-residence: both orders use exactly one per-ride font pair.
    coexistence = []
    native_cards = json.loads((R / 'qa/dialogue/cards033_actual_pages.json').read_text('utf-8'))
    for ride in range(1, 6):
        rule = next(z for z in plan['pages'] if z['page'] == 0x1d + ride)
        title = next(z for z in plan['pages'] if z['page'] == 0x23 + ride)
        assert rule['font_bank'] == title['font_bank']
        assert rule['columns'] == 23 and title['columns'] == 20
        assert set(snapshots[rule['entry_id']]).isdisjoint(snapshots[title['entry_id']])
        for order in ((rule, title), (title, rule)):
            live = {}
            for z in order:
                mode = 2 if z['family'] == 'ride_upper_rule' else 3
                c, m = native_init(rom, z['page'], mode, ride, 196, 3)
                assert m.ram[0x34] == m.ram[0xc6] == z['font_bank']
                live.update(snapshots[z['entry_id']])
                for before in order[:order.index(z) + 1]:
                    expected, _, _ = draw(before['original_text'], before['width_pixels'], face)
                    assert pixels(rom, before, live).tobytes() == expected.tobytes()
        actual = next(z for z in native_cards if z['ride'] == ride)
        native = R / actual['source_image']
        oldppu = native.with_name(native.stem + '_ppu.bin').read_bytes()
        assert oldppu[0x20a5] == 0x88 and oldppu[0x20ba] == 0xc2
        assert oldppu[0x20c5] == 0x8b and oldppu[0x20da] == 0xc4
        assert all(oldppu[0x20c6 + i] == 0x8c for i in range(20))
        assert set(snapshots[title['entry_id']]) == {0x20a6 + y * 32 + x for y in range(2) for x in range(20)}
        coexistence.append({'ride': ride, 'font_pair': [rule['font_bank'], rule['font_bank'] + 1],
                            'both_initializer_orders_and_live_pixels_exact': True,
                            'title20_rules23_columns': True, 'frame_repair_original_native_tile_providers': True})
    # Nontarget ABI including cached native reader states.
    test = plan['pages'][0]
    configs = [(root, slot, 130, test['original_pointer']) for root in range(16) for slot in range(48)
               if not (root == 8 and slot == 10)]
    configs += [(8, 10, f, test['original_pointer']) for f in (90, 128, 150, 162, 188, 196, 255)]
    configs += [(8, 10, 130, p) for p in (0x973d, 0x9740, 0x9743, 0x9746)]
    fallback = 0
    for root, slot, font, pointer in configs:
        for pc in (0x93e1, 0x925e):
            both = []
            for image in (old, rom):
                m = initial(image, test)
                r = m.ram
                r[0x18], r[0x6cf], r[0xc6] = root, slot, font
                r[0x6cd:0x6cf] = pointer.to_bytes(2, 'little')
                c = run(m, pc, 0x49, 0x75)
                both.append((c, m))
            (ca, ma), (cb, mb) = both
            assert (ca.a, ca.x, ca.y, ca.p, ca.sp) == (cb.a, cb.x, cb.y, cb.p, cb.sp), (root, slot, font, pointer, pc)
            assert ma.ram[:0x100] == mb.ram[:0x100], (root, slot, font, pointer, pc)
            assert ma.ram[0x100:0x1c0] == mb.ram[0x100:0x1c0]
            assert ma.ram[0x200:0x800] == mb.ram[0x200:0x800]
            assert ma.banks == mb.banks == [18, 19]
            fallback += 1
    for ext in ('.nes', '.ips'):
        name = 'TinyToon2_Text11_Candidate062' + ext
        assert (folder / name).read_bytes() == (R / 'build/text11_211_rebuild062' / name).read_bytes()
    d = {'work': 211, 'status': 'PASS_FINAL062_33_ORDINARY_AND_NINE_OPENING_CPU', 'ROM_sha256': sha(path),
         'ordinary33': results, 'variant_total': sum(z['variant_cases'] for z in results),
         'F8_cases': 1000, 'FA_six_selector_entries': 2,
         'all_default_skip_boundaries': sum(z['all_default_skip_boundaries'] for z in results),
         'native_init_ABI_cycles_cases': init_count, 'booth050_retention_cases': retention,
         'fallback_ABI_RAM_queue_cases': fallback, 'native15_font190_alias': True,
         'five_ride_title_rule_coexistence': coexistence, 'title_frame_repair_extra_queue_bytes': 36,
         'opening9_finalCPU': intro, 'IRQ_register_writes_cycles_exact055': True,
         'independent_ROM_IPS_exact': True, 'runtime062': 'NOT_RUN', 'distribution_eligible': False,
         'limits': ['Upper window clear/paired font residence andCHR256 emulator mapping unverified',
                    'CPU only; asynchronousNMI/IRQ timing and whole-game play not verified',
                    'Credits11px separately verified in credits11_211_CPU; bitmap/HUD/signs unchanged; registered inventory is not global closure']}
    out.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({k: v for k, v in d.items() if k not in ('ordinary33', 'opening9_finalCPU')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
