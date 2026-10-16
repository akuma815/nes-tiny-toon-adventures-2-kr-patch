from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/verify_intro144.py';assert not p.exists()
 s=(R/'scripts/verify_reader_pair142.py').read_text('utf-8')
 s=s.replace("ea['frames']==eb['frames']==4500","ea['frames']==eb['frames']==6000").replace("read_text()=='4500'","read_text()=='6000'").replace("b/'frame_04500_ram.bin'","b/'frame_06000_ram.bin'").replace("assert normal==final_normal and gameplay","assert normal==final_normal").replace("'frames_each':4500","'frames_each':6000")
 s=s.replace("assert 'seed'not in eb","assert 'seed'not in eb and eb['input']['sequence']==[]")
 s=s.replace("Controller-only bounded route; not complete ride or wholeplay","No-input intro two loops; not wholeplay or human final approval")
 s+='''\nif __name__=='__main__':
 rom=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 cat=json.loads((R/'extracted/text/table_20261004_001/text_tokens.json').read_text('utf-8'))
 slot_units={z['index']:z['unit_id']for z in cat['tables'][0]['slots']}
 targets={f'intro{s:02X}':{'slot':s,'NT':0x21e4,'font_RAM':0xc6,'font':rom[0x5710+2*s]}for s in range(1,10)}
 verify(144,'intro',[],targets,[slot_units[s]for s in range(1,10)]+['MACRO_061C3'],0,0)
'''
 p.write_text(s,'utf-8');print('prepared exact6000/no-input intro verifier')
if __name__=='__main__':main()
