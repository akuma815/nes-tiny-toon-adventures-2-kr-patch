"""Freeze user booth evidence and create a private copy of their existing MesenCE."""
from pathlib import Path
import hashlib,json,shutil,struct,subprocess
from seal_nonplay171 import R,sha

def main():
    out=R/'qa/issue176_user_booth';host=R/'tools/mesence_user176'
    assert not out.exists() and not host.exists()
    settings=json.loads(Path('H:/Mesen/settings.json').read_text('utf-8-sig'))
    path=Path(settings['RecentFiles']['Items'][0]['RomFile']['Path'])
    assert sha(path)==sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes')=='31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa'
    out.mkdir();host.mkdir()
    copies=[]
    for name in ['Mesen.exe','MesenCore.dll','libHarfBuzzSharp.dll','libSkiaSharp.dll','librashader.dll']:
        p=Path('H:/Mesen')/name;digest=sha(p);q=host/name;shutil.copy2(p,q);assert sha(q)==sha(p)==digest
        copies.append({'source':str(p),'copy':q.relative_to(R).as_posix(),'sha256':digest})
    (host/'settings.json').write_bytes((R/'config/mesen_survey.json').read_bytes())
    states=[]
    for slot in [1,11]:
        p=Path('H:/Mesen/SaveStates')/f'Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan)_KR_{slot}.mss'
        data=p.read_bytes();digest=hashlib.sha256(data).hexdigest();q=out/f'user_slot{slot}.mss';q.write_bytes(data);assert sha(p)==sha(q)==digest
        vals=struct.unpack_from('<8I',data,3);assert data[:3]==b'MSS' and vals[:3]==(0x20201,4,2)
        pos=35+vals[-1];length=struct.unpack_from('<I',data,pos)[0];name=data[pos+4:pos+4+length].decode('utf-8')
        assert name==path.name
        states.append({'source':str(p),'copy':q.relative_to(R).as_posix(),'sha256':digest,'saved_mtime_ns':p.stat().st_mtime_ns,
            'emu_version_hex':hex(vals[0]),'file_format':vals[1],'console_type':vals[2],'stored_ROM_name':name,
            'has_ROM_hash_in_header':False,'attribution_limit':'ROM049 tied to current recent path/hash and user report, not an embedded savestate ROM digest.'})
    result={'work':176,'status':'FROZEN_USER_HOST_AND_SAVED_BOOTH_STATES_RUNTIME_PENDING',
        'user_report':'Ticket exchange followed by garbled lower booth dialogue; attached user screenshot. Natural user observation, not assistant gameplay.',
        'observed_process_ID':22308,'user_host':'H:/Mesen/Mesen.exe','ROM_recent_path':str(path),'ROM_sha256':sha(path),
        'host_copies':copies,'states':states,'Computer_Use_unavailable':'Native pipe absent (os error2), repeated list_apps failed.',
        'emucap_attached':False,'current_live_screen_or_memory_read':False,
        'private_reproduction_policy':'Read frozen copied user state in identical2.2.1 host copy; no change to running user process/ROM/settings/state files. Focused issue QA only.'}
    (out/'provenance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
