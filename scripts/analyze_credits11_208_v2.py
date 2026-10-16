"""Measure actual native geometry and sparse packet demand before choosing an engine."""
from pathlib import Path
import json
from asm6502 import Disassembler, MPU
from verify_ui_native_latch_hooks import Memory
from seal_nonplay171 import R, sha

rom = (R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes').read_bytes()
m = Memory(rom)
m.banks[:2] = [18, 19]
dis = Disassembler(MPU(memory=m))
for lo, hi in ((0x8023, 0x8070), (0xfd19, 0xfd60), (0xcc20, 0xcc50)):
    pc = lo
    while pc < hi:
        n, text = dis.instruction_at(pc)
        print(f'{pc:04X} {text}')
        assert n > 0
        pc += n
d = json.loads((R / 'qa/reports/credits11_202_capacity.json').read_text('utf-8'))['cases'][1]
pages = []
for p in d['pages']:
    packets = []
    origin = 0x2005 if p['entry_id'] == 'MAIN_05999' else 0x2805
    for y, row in enumerate(p['NT_rows']):
        ix = [x for x, code in enumerate(row) if code]
        assert all(x < 27 for x in ix), 'Glyph reaches beyond visible native NT row'
        spans = []
        if ix:
            start = end = ix[0]
            for x in ix[1:]:
                if x - end > 5:
                    spans.append((start, end + 1))
                    start = x
                end = x
            spans.append((start, end + 1))
        for start, end in spans:
            address = origin + y * 32 + start
            packets.append([1, address >> 8, address & 255, *row[start:end], 255])
    pages.append({'entry_id': p['entry_id'], 'native_origin': origin,
                  'paired_glyph_rows': len(p['NT_rows']), 'NT_row_stride': 32,
                  'logical_line_stride': 64, 'logical_lines': len(p['lines']),
                  'optimal_sparse_queue_bytes': sum(map(len, packets)),
                  'packets': packets})
print(json.dumps(pages, indent=2))
