"""Execute final060 credits, original caller schedule and screen-off PPU writes."""
from pathlib import Path
import json
from PIL import Image
from asm6502 import MPU
from extract_title_png import decode
from verify_ui_native_latch_hooks import Memory
from verify_homebooth11_199 import queue
from seal_nonplay171 import R, sha


class Bus(Memory):
    def __init__(self, rom):
        super().__init__(rom)
        self.banks[:2] = [18, 19]
        self.nt = {}
        self.address = 0
        self.high = True
        self.mask = 0x1e
        self.control = 0x90
        self.lowest_SP = 255
        self.queue_high = 0
        self.trace = []

    def __getitem__(self, at):
        if at == 0x2002:
            self.high = True
            return 0x80
        return super().__getitem__(at)

    def __setitem__(self, at, value):
        if self.cpu:
            self.lowest_SP = min(self.lowest_SP, self.cpu.sp)
        if at == 0x2000:
            self.control = value
            self.trace.append((at, value))
        elif at == 0x2001:
            self.mask = value
            self.trace.append((at, value))
        elif at == 0x2006:
            self.address = ((value & 63) << 8) if self.high else self.address | value
            self.high = not self.high
        elif at == 0x2007:
            assert not self.control & 128 and not self.mask & 24, 'Direct NT write requires NMI/render disabled'
            self.nt[self.address] = value
            self.address += 32 if self.control & 4 else 1
        if at == 0x1e:
            self.queue_high = max(self.queue_high, value)
        super().__setitem__(at, value)


def execute(m, pc, a=0, p=0x34):
    cpu = MPU(memory=m)
    m.cpu = cpu
    cpu.pc = pc
    cpu.a = a
    cpu.p = p
    cpu.sp = 0xfd
    m.ram[0x1fe:0x200] = bytes.fromhex('ff c0')
    steps = 0
    while cpu.pc != 0xc100:
        cpu.step()
        steps += 1
        assert steps < 30000, hex(cpu.pc)
    assert cpu.sp == 255
    return cpu


def initial(rom, page):
    m = Bus(rom)
    r = m.ram
    r[0x18] = 7
    r[0x2b] = 0x32
    r[0x6cf] = page['page']
    r[0xc6] = 201
    r[0x6cd:0x6cf] = page['original_pointer'].to_bytes(2, 'little')
    for at in (0x6c0, 0x6d1):
        r[at:at + 2] = page['NT_top_origin'].to_bytes(2, 'little')
    r[0xff] = 0x90
    r[0xfe] = 0x1e
    return m


def expected(page):
    return {page['NT_top_origin'] + y * 32 + x: v for y, row in enumerate(page['NT_rows']) for x, v in enumerate(row)}


def pixels(rom, page, writes):
    image = Image.new('L', (216, len(page['NT_rows']) * 8))
    base = page['font_file_offset']
    for y, row in enumerate(page['NT_rows']):
        for x in range(27):
            code = writes[page['NT_top_origin'] + y * 32 + x]
            image.paste(Image.frombytes('L', (8, 8), decode(rom[base + code * 16:base + (code + 1) * 16])), (x * 8, y * 8))
    return image


def main():
    folder = R / 'build/text11_candidate_060'
    target = folder / 'TinyToon2_Text11_Candidate060.nes'
    rom = target.read_bytes()
    prior = (R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes').read_bytes()
    plan = json.loads((folder / 'credits11_plan.json').read_text('utf-8'))
    output = R / 'qa/reports/credits11_209_CPU.json'
    assert not output.exists()
    first = plan['pages'][0]
    init = initial(rom, first)
    # Exact patched initial callsite, returning atA44B before selector2E.
    cpu = MPU(memory=init)
    init.cpu = cpu
    cpu.pc = 0xa448
    steps = 0
    while cpu.pc != 0xa44b:
        cpu.step()
        steps += 1
        assert steps < 30000
    assert init.nt == expected(first)
    assert init.ram[0x1e] == 0
    assert init.ram[0x6cf] == 45 and init.ram[0x6c3] == init.ram[0x6c4] == 0
    assert init.banks[:2] == [0x32, 0x33]
    assert init.control == 0x90 and init.mask == 0x1e
    assert init.trace[0] == (0x2000, 0x10)
    assert init.trace[-2:] == [(0x2000, 0x90), (0x2001, 0x1e)], init.trace
    assert init.lowest_SP > init.queue_high
    pages = []
    for z in plan['pages'][1:]:
        m = initial(rom, z)
        old = initial(prior, z)
        writes = {}
        oldcalls = 0
        calls = 0
        max_queue = 0
        max_cycles = 0
        terminators = []
        while True:
            for bus in (old, m):
                bus.ram[0x1e] = 0
                bus.ram[0x100:0x1c0] = bytes(0xc0)
            ca = execute(old, 0x93e1)
            cb = execute(m, 0x93e1)
            calls += 1
            oldcalls += 1
            # Preserve native per-call continue/end and delay, not merely final text.
            assert bool(ca.p & 1) == bool(cb.p & 1), (z['entry_id'], calls)
            assert old.ram[0x58] == m.ram[0x58], (z['entry_id'], calls)
            assert old.ram[0x6cf] == m.ram[0x6cf]
            now = queue(m.ram)
            assert set(now) <= set(expected(z))
            assert all(expected(z)[at] == v for at, v in now.items())
            writes.update(now)
            max_queue = max(max_queue, m.ram[0x1e])
            max_cycles = max(max_cycles, cb.processorCycles)
            assert m.ram[0x1e] <= 62
            assert m.lowest_SP > m.queue_high
            assert m.banks[:2] == [0x32, 0x33]
            if not ca.p & 1:
                break
        assert calls == z['native_calls']
        assert writes == expected(z)
        assert m.ram[0x6c3] == m.ram[0x6c4] == 0
        pages.append({'entry_id': z['entry_id'], 'calls': calls,
                      'native_continue_end_delay_every_call_exact': True,
                      'max_queue_bytes': max_queue, 'lowest_SP': m.lowest_SP,
                      'stack_queue_no_overlap': True, 'max_cycles': max_cycles,
                      'all_27_column_top_bottom_NT_exact': True})
    # All serialized glyphs match the immutable static source pixels.
    for z in plan['pages']:
        reference = Image.open(R / f'workspace/review/credits11_202/{z["entry_id"]}_latin16.png').convert('RGB').crop((0, 0, 216, len(z['NT_rows']) * 8))
        image = pixels(rom, z, expected(z))
        restored = Image.new('RGB', image.size)
        restored.putdata([(255, 254, 255) if b else (0, 0, 0) for b in image.get_flattened_data()])
        assert restored.tobytes() == reference.tobytes()
    # Whole native ending update executes once every declared frame; exact scroll and transitions.
    scheduled = []
    for image in (prior, rom):
        m = initial(image, plan['pages'][1])
        m.ram[0x6df] = 0
        events = []
        for frame in range(4000):
            r = m.ram
            r[0x1b] = frame & 255
            r[0x1e] = 0
            r[0x100:0x1c0] = bytes(0xc0)
            execute(m, 0xa492)
            events.append((r[0x6df], r[0xfc], r[0xff], r[0x6cf], r[0x58]))
        scheduled.append(events)
    assert scheduled[0] == scheduled[1]
    for ext in ('.nes', '.ips'):
        name = 'TinyToon2_Text11_Candidate060' + ext
        assert (folder / name).read_bytes() == (R / 'build/text11_209_rebuild060' / name).read_bytes()
    report = {'work': 209, 'status': 'PASS_FINAL060_CREDITS3_NATIVE_CALLS_SCROLL_CPU',
              'ROM_sha256': sha(target), 'initial_direct_tile_writes': len(init.nt),
              'initial_screen_NMI_off_and_register_restore_CPU': True,
              'initial_queue_bytes': init.ram[0x1e], 'initial_cycles': cpu.processorCycles,
              'initial_min_SP': init.lowest_SP, 'progressive': pages,
              'native_ending_schedule_frames_equal059': 4000,
              'all_three_font_pixels_exact_static202': True,
              'names_legal_literal_text_preserved_bitmap_enlarged': True,
              'independent_ROM_IPS_exact': True, 'runtime060': 'NOT_RUN', 'adopted': False,
              'limits': ['Synchronous CPU and minimal2006/2007 bus model, not actual PPU/NMI transfer or screen capture',
                         'Native initializer after A44B hardware, actual aliasing/scroll/font residence and IRQ scheduling need scene review',
                         'Latin16 spacing not human approved; no natural credits/game clear or global corpus closure']}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
