"""Final056 CPU: both render paths at every skip boundary, init/font retention and clear."""
from pathlib import Path
import json
from asm6502 import MPU
from verify_opening11_cpu186_v2 import Memory
from verify_home11_cpu191 import paragraph, run
from verify_ui_native_latch_hooks import Memory as FullMemory, irq
from seal_nonplay171 import R, sha


def initial(rom, z):
    m = Memory(rom)
    r = m.ram
    r[0x18] = 8
    r[0x6cf] = z['page']
    r[0xc6] = z['font_bank']
    r[0x6cd:0x6cf] = z['original_pointer'].to_bytes(2, 'little')
    r[0x6d1:0x6d3] = (0x22a8).to_bytes(2, 'little')
    r[0x6c0:0x6c2] = (0x22a8).to_bytes(2, 'little')
    r[0x2b] = 0x32
    return m


def queue(r):
    out = {}
    i = 0x100
    end = 0x100 + r[0x1e]
    while i < end:
        assert r[i] == 1
        addr = r[i + 1] * 256 + r[i + 2]
        i += 3
        while r[i] != 255:
            assert i < end
            out[addr] = r[i]
            addr += 1
            i += 1
        i += 1
    assert i == end and r[end] == 0
    return out


def native_init(rom, slot, mode, ride, active, phase):
    m = FullMemory(rom)
    r = m.ram
    r[0x18] = 8
    r[0x2b] = 0x32
    r[0x6cf] = slot
    r[0x25] = ride
    r[0xc6] = r[0x6f3] = active
    r[0x34] = 204 if ride == 6 else 193
    r[0x6df] = phase
    r[0x6d0] = 0x0e if ride == 6 else 0x10
    c = MPU(memory=m)
    m.cpu = c
    c.pc = 0x9417
    c.a = mode
    c.sp = 0xfd
    c.p = 0x34
    r[0x1fe:0x200] = bytes.fromhex('ff c0')
    steps = 0
    while c.pc != 0xc100:
        c.step()
        steps += 1
        assert steps < 10000
    return c, m


def main():
    folder = R / 'build/homebooth11_candidate_056'
    rompath = folder / 'TinyToon2_HomeBooth11_Candidate056.nes'
    rom = rompath.read_bytes()
    old = (R / 'build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes').read_bytes()
    p = json.loads((folder / 'homebooth11_plan.json').read_text('utf-8'))
    out = R / 'qa/reports/homebooth11_198_CPU.json'
    assert not out.exists()
    typed = []
    skip_cases = []
    clear = set()
    m = Memory(rom)
    run(m, 0x920a)
    for y in range(5):
        m.ram[0x1e] = 0
        run(m, 0x919a)
        assert m.ram[0x100] == 1 and m.ram[0x1e] == 26
        addr = m.ram[0x101] * 256 + m.ram[0x102]
        assert addr == 0x22a7 + y * 32
        assert not any(m.ram[0x103:0x119])
        clear.update(range(addr, addr + 22))
    worst_queue = 0
    for z in p['pages']:
        info, writes = paragraph(rom, z, 0x9630, 8, 0x22a8, 21)
        assert set(writes) <= clear
        typed.append(info)
        body = bytes.fromhex(z['body_hex'])
        # Every valid progressive output boundary before finalFF is a skip point.
        m = initial(rom, z)
        cursor = 0
        printed = {}
        cases = 0
        max_cycles = 0
        while True:
            q = initial(rom, z)
            q.ram[:] = m.ram
            q.ram[0x1e] = 0
            q.ram[0x100:0x1c0] = bytes(0xc0)
            c = run(q, 0x925e)
            rest = queue(q.ram)
            assert {**printed, **rest} == writes, (z['entry_id'], cursor)
            assert q.ram[0x6cf] == z['page'] and q.ram[0x6c3] == q.ram[0x6c4] == 0
            assert q.banks == [18, 19] and q.ram[0x2b] == 0x32
            assert q.ram[0xc6] == z['font_bank']
            assert q.ram[0x1e] <= 100
            assert not any(q.ram[0x100 + q.ram[0x1e] + 1:0x1c0])
            assert set(rest) <= clear
            max_cycles = max(max_cycles, c.processorCycles)
            worst_queue = max(worst_queue, q.ram[0x1e])
            cases += 1
            if body[cursor] == 255:
                break
            m.ram[0x1e] = 0
            m.ram[0x100:0x140] = bytes(64)
            run(m, 0x9630)
            if body[cursor] < 128:
                for at in (0x100, 0x105):
                    a = m.ram[at + 1] * 256 + m.ram[at + 2]
                    printed[a] = m.ram[at + 3]
                cursor += 2
            else:
                assert body[cursor] == 254
                cursor += 1
        skip_cases.append({'entry_id': z['entry_id'], 'all_skip_boundaries': cases,
                           'remaining_NT_exact': True, 'max_instant_cycles': max_cycles})
    intro_plan = json.loads((folder / 'opening11_plan.json').read_text('utf-8'))
    intro = [paragraph(rom, z, 0x95f9, 7, 0x21e4, 24)[0] for z in intro_plan['pages']]
    # Native initializers, including050 booth possession refresh, remain byte/cycle exact.
    init_cases = 0
    retained_refresh = 0
    for slot in range(48):
        for mode in (0, 1, 4):
            for ride in (0, 3, 6):
                for active in (90, 130, 162, 188, 196):
                    for phase in (0, 3):
                        ca, ma = native_init(old, slot, mode, ride, active, phase)
                        cb, mb = native_init(rom, slot, mode, ride, active, phase)
                        assert (ca.a, ca.x, ca.y, ca.p, ca.sp, ca.processorCycles) == (cb.a, cb.x, cb.y, cb.p, cb.sp, cb.processorCycles)
                        assert ma.ram[:0x100] == mb.ram[:0x100] and ma.ram[0x200:0x800] == mb.ram[0x200:0x800]
                        assert ma.banks == mb.banks
                        if slot == 0x23 and ride == 6 and mode == 4:
                            assert mb.ram[0xc6] == active
                            retained_refresh += 1
                        init_cases += 1
    # Nontarget slow/instant ABI, persistent RAM and native queue match055.
    fallback = 0
    test = p['pages'][0]
    configs = [(root, slot, test['font_bank'], test['original_pointer'])
               for root in range(16) for slot in range(48) if not (root == 8 and slot == 10)]
    configs += [(8, 10, font, test['original_pointer']) for font in (90, 128, 150, 162, 188, 196, 255)]
    configs += [(8, 10, 130, ptr) for ptr in (0x973d, 0x9740, 0x9743, 0x9746)]
    for root, slot, font, ptr in configs:
        for pa, pb in ((0x93e1, 0x9630), (0x925e, 0x925e)):
            both = []
            for image, pc in ((old, pa), (rom, pb)):
                m = initial(image, test)
                r = m.ram
                r[0x18], r[0x6cf], r[0xc6] = root, slot, font
                r[0x6cd:0x6cf] = ptr.to_bytes(2, 'little')
                c = run(m, pc, 0x49, 0x75)
                both.append((c, m))
            (ca, ma), (cb, mb) = both
            assert (ca.a, ca.x, ca.y, ca.p, ca.sp) == (cb.a, cb.x, cb.y, cb.p, cb.sp), (root, slot, font, ptr, pa)
            assert ma.ram[:0x100] == mb.ram[:0x100]
            assert ma.ram[0x100:0x1c0] == mb.ram[0x100:0x1c0]
            assert ma.ram[0x200:0x800] == mb.ram[0x200:0x800]
            assert ma.banks == mb.banks == [18, 19]
            fallback += 1
    assert irq(old) == irq(rom)
    for ext in ('.nes', '.ips'):
        name = 'TinyToon2_HomeBooth11_Candidate056' + ext
        assert (folder / name).read_bytes() == (R / 'build/homebooth11_198_rebuild056' / name).read_bytes()
    d = {'work': 198, 'status': 'PASS_FINAL056_TYPED_SKIP_CLEAR_INIT_FONT_RETENTION_CPU',
         'ROM_sha256': sha(rompath), 'typed12': typed, 'skip12': skip_cases,
         'skip_boundaries_total': sum(x['all_skip_boundaries'] for x in skip_cases),
         'max_skip_queue_bytes': worst_queue, 'clear_cells': len(clear),
         'all_output_cells_inside_original5row_clear': True,
         'opening9_finalCPU': intro, 'native_init_exact_cases': init_cases,
         'booth050_font_retention_cases': retained_refresh, 'fallback_ABI_RAM_queue_cases': fallback,
         'IRQ_register_write_cycles_exact055': True, 'independent_ROM_IPS_byte_exact': True,
         'runtime056': 'NOT_RUN',
         'limits': ['CPU excludes NMI/IRQ preemption and actual PPU font residence',
                    'Instant code is longer; frame/NMI budget not yet proven',
                    'Whole-game11px unfinished; no user font/visual approval or release claim']}
    out.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({k: v for k, v in d.items() if k not in ('typed12', 'skip12', 'opening9_finalCPU')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
