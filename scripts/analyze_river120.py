"""Bind the third bank61 producer to river dispatch and stage-only sprite IDs."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw
from verify_dialogue_home import MPU
from verify_gate_font_tag_hooks import Memory
from analyze_pow_metasprites096 import run as assemble
from extract_title_png import decode

R = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def machine(data, bank=0x38):
    m = Memory(data)
    m.banks = [bank, bank+1, 0x3e, m.count-1]
    c = MPU(memory=m); m.cpu = c
    c.sp = 0xfd; c.p = 0x30
    m.ram[0x1fe:0x200] = bytes.fromhex('ff 5f')
    return m, c

def constructor(data, state, hi, lo):
    m, c = machine(data)
    m.ram[:0x800] = b'\x55' * 0x800
    m.ram[0x1fe:0x200] = bytes.fromhex('ff 5f')
    m.ram[0x422] = state; m.ram[0x69] = hi; m.ram[0x6d] = lo
    before = bytes(m.ram)
    c.pc = 0xa5c6; c.x = 0x73; c.y = 0x92
    steps = 0
    while c.pc not in (0x6000, 0xb6cc):
        c.step(); steps += 1; assert steps < 100
    trigger = state == 0 and hi == 11 and lo >= 240
    expected = bytearray(before)
    if trigger:
        values = {0x699:15, 0x69a:32, 0x69b:39, 0x618:1, 0x5c:1,
                  0x482:1, 0x483:1, 0x484:1, 0x38:61, 0x4b2:13,
                  0x4a2:16, 0x472:128, 0x473:24, 0x422:2, 0x423:2, 0x424:2,
                  0x4e2:0, 0x4f2:0, 0x4c2:0, 0x4d2:0, 0x502:0,
                  0x512:0, 0x522:0, 0x532:0, 0x542:0, 0x402:0xed}
        for a, v in values.items():
            expected[a] = v
    elif state == 2:
        expected[0x402] = 0xed
    assert bytes(m.ram) == bytes(expected)
    assert (c.pc == 0xb6cc) == (trigger or state == 2)
    return (c.a, c.x, c.y, c.p, c.sp, c.pc, c.processorCycles, bytes(m.ram)), trigger

def main():
    out = R / 'qa/reports/river120_bank61.json'
    png = R / 'work/river120/stage_ED_EE_EF_static.png'
    assert not out.exists() and not png.exists()
    source = R / 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    current = R / 'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
    src, rom = source.read_bytes(), current.read_bytes()
    assert sha(source) == 'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(current) == '82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
    spans = [(0x1ed0c, 0x1ed28), (0x125d6, 0x12655), (0x12655, 0x1267b),
             (0x136dc, 0x13710), (0xf8d8, 0xf958)]
    for a, b in spans:
        assert src[a:b] == rom[a+0x20000:b+0x20000]
    banks = list(src[0x1ed23:0x1ed28]); assert banks == [0x38,0x38,0x36,0x38,0x30]
    targets = [int.from_bytes(src[0x1ed19+2*i:0x1ed1b+2*i], 'little') for i in range(5)]
    assert targets == [0x8280,0x953a,0x8001,0xa645,0x8001]
    dispatch = []
    for course in range(5):
        pair = []
        for data in (src, rom):
            m,c = machine(data, 0x32); m.ram[0x25] = course; c.pc = 0xecfc
            steps = 0
            while c.pc != targets[course]:
                c.step(); steps += 1; assert steps < 200
            assert m.banks[:2] == [banks[course], banks[course]+1]
            pair.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram),m.banks[:2],m.writes))
        assert pair[0] == pair[1]
        dispatch.append({'course':course,'bank_hex':f'{banks[course]:02X}',
                         'target_CPU_hex':f'{targets[course]:04X}','cycles':pair[0][5]})
    counts = {'new_bank61_initializations':0, 'state2_reuses_existing_bank':0, 'returns':0}
    cases = 0
    for state in (0,1,2,3):
        for hi in range(256):
            for lo in (0,239,240,255):
                a, trigger = constructor(src,state,hi,lo)
                b, trigger2 = constructor(rom,state,hi,lo)
                assert a == b and trigger == trigger2
                counts['new_bank61_initializations' if trigger else
                       'state2_reuses_existing_bank' if state == 2 else 'returns'] += 1
                cases += 1
    # Stage3 has a separate B8C8 table; common frames18/19 are not the ED lookup.
    records = []
    sheet = Image.new('RGB',(576,336),(25,25,25)); draw = ImageDraw.Draw(sheet)
    palette = [(25,25,25),(255,254,255),(116,80,168),(248,216,32)]
    for col, art in enumerate((0xed,0xee,0xef)):
        m,c,oam,steps = assemble(src,art,3)
        m2,c2,oam2,steps2 = assemble(rom,art,3)
        assert oam == oam2 and bytes(m) == bytes(m2)
        assert (c.a,c.x,c.y,c.p,c.sp,c.processorCycles,steps) == (c2.a,c2.x,c2.y,c2.p,c2.sp,c2.processorCycles,steps2)
        table = 0xb8c8 + 2*(art-0xc0)
        ptr = int.from_bytes(m[table:table+2],'little')
        size = m[ptr]; assert size == len(oam) and size in (36,8,4)
        expected = []
        for i in range(size//4,0,-1):
            y,t,attr,x = m[ptr+4*i-3:ptr+4*i+1]
            signed = lambda v: v if v<128 else v-256
            expected.extend((128+signed(y),t,attr,128+signed(x)))
        assert bytes(expected) == oam
        pic = Image.new('RGB',(64,96),palette[0])
        for i in range(0,len(oam),4):
            y,t,attr,x = oam[i:i+4]; local = (t&0xfe)-0x80
            assert t&1 and 0<=local<64
            raw = src[0x2f410+local*16:0x2f410+(local+2)*16]
            tile = Image.new('RGB',(8,16)); tile.putdata([palette[v]for v in list(decode(raw[:16]))+list(decode(raw[16:]))])
            if attr&64: tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if attr&128: tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            pic.paste(tile,(x-128+24,y-128+80))
        draw.text((col*192+8,6),f'STATIC stage3 / {art:02X}',fill=(255,255,255))
        sheet.paste(pic.resize((192,288),Image.Resampling.NEAREST),(col*192,30))
        records.append({'art_hex':f'{art:02X}','stage_table_CPU_hex':f'{table:04X}',
                        'descriptor_CPU_hex':f'{ptr:04X}','OAM_hex':oam.hex(),'sprites':size//4,
                        'CPU_cycles':c.processorCycles,'assumed_CHR_bank':61})
    png.parent.mkdir(parents=True,exist_ok=True); sheet.save(png)
    result = {'work':120,'status':'PASS_BOUNDED_RIVER_BANK61_PRODUCER_AND_STAGE_SPRITES',
              'source_sha256':sha(source),'ROM047_sha256':sha(current),
              'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),
              'source_current_guarded_spans_hex':[[f'{a:X}',f'{b:X}']for a,b in spans],
              'dispatch_CPU_case_pairs':5,'dispatch':dispatch,
              'constructor_CPU_case_pairs':cases,'constructor_case_categories':counts,
              'binding':{'course':3,'course_name':'river','native_bank_hex':'38',
                         'entry_CPU_hex':'A645','constructor_call_CPU_hex':'A665',
                         'condition':'RAM0422==0 && RAM69==0B && RAM6D>=F0',
                         'CHR61_load_CPU_hex':'A5FD','source_file_offset_hex':'1260D',
                         'current_file_offset_hex':'3260D','actor2_art_hex':'ED',
                         'next_consumer_CPU_hex':'B6CC',
                         'state2':'Refresh ED and enterB6CC; does not set bank61 anew.'},
              'stage3_sprite_records':records,'static_preview':png.relative_to(R).as_posix(),
              'static_preview_sha256':sha(png),'direct_static_visual_review':False,
              'limits':['Named dispatch and constructor bounds only; no global caller reachability or real river late-game activation.',
                        'Constructor tests stop atB6CC, before downstream geometry; RAM69/6D meanings and natural progression not proven here.',
                        'Stage-only ED/EE/EF use course3 table; no inference that a common18/19 POW frame was displayed.',
                        'Preview assumes physical bank61 atPPU1800, arbitrary explanation palette and synthetic coordinates. Not an emulator screenshot.',
                        'No new emulator/build/apply/ROM/CSV edit, no human preserve/translate decision or natural fullplay.'],
              'release_eligible':False}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(result['status'],cases,'constructor pairs',counts)

if __name__ == '__main__':
    main()
