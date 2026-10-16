"""Read-only first-line CPU diagnosis."""
import json
from verify_credits11_210 import initial, execute
from seal_nonplay171 import R
page = json.loads((R / 'build/text11_candidate_061/credits11_plan.json').read_text('utf-8'))['pages'][1]
a = initial((R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes').read_bytes(), page)
b = initial((R / 'build/text11_candidate_061/TinyToon2_Text11_Candidate061.nes').read_bytes(), page)
print([(x['native_event_count'], x['data_PC']) for x in page['descriptors']])
for index in range(15):
    details = []
    for m in (a, b):
        m.ram[0x1e] = 0
        c = execute(m, 0x93e1)
        details.append({'6C3': m.ram[0x6c3], '6C4': m.ram[0x6c4], 'delay': m.ram[0x58],
                        'carry': c.p & 1, 'queue': m.ram[0x1e], 'count03': m.ram[3], 'tag': m.ram[0x2b]})
    print(index + 1, details)
