from pathlib import Path
import json
from seal_continuation159 import R,sha
def main():
 lua=R/'scripts/trace_water_transfer160.lua';plan=R/'work/water160/run_plan.json';assert not lua.exists()and not plan.exists()
 src=R/'scripts/trace_water_exit_input158.lua';s=src.read_text('utf-8')
 key="local polls=0;local untilA=-1;local lastjump=-100;local reason='fixed';local target=-1";assert s.count(key)==1
 s=s.replace(key,key+"\nlocal transferring=false;local transfer_stage=-1\nlocal transferlog=assert(io.open(out..'/raft_transfer.csv','wb'))\ntransferlog:write('frame,event,stage,player_x,boat1_x,boat2_x,boat1_vy,jump,support,life\\n')\n")
 key='if frame>=3300 and r(0x18)==4 and r(0x54)==5 and r(0x25)==3 then';assert s.count(key)==1
 addition=r'''
  if transferring and r(0x716)~=transfer_stage then
   transferlog:write(string.format('%d,native_raft_swap,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,r(0x716),w(0x4a0,0x4b0),w(0x4a1,0x4b1),w(0x4a2,0x4b2),w(0x4c1,0x4d1),r(0x99),r(0xc1),r(0x7c0)))
   transferring=false
  end
  local ahead=w(0x4a2,0x4b2)-w(0x4a0,0x4b0)
  local fall=w(0x4c1,0x4d1)
  if not transferring and r(0x99)==0 and r(0xc1)~=0 and r(0x422)==1 and ahead>32 and ahead<110 and fall>=256 and fall<32768 then
   transferring=true;transfer_stage=r(0x716);untilA=frame+8;lastjump=frame;reason='transfer_begin';target=2
   transferlog:write(string.format('%d,begin,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,transfer_stage,w(0x4a0,0x4b0),w(0x4a1,0x4b1),w(0x4a2,0x4b2),fall,r(0x99),r(0xc1),r(0x7c0)))
  end
'''
 s=s.replace(key,key+addition)
 key='if r(0x99)==0 and r(0xc1)~=0 and r(0x430)>=2';assert s.count(key)==1;s=s.replace(key,'if not transferring and r(0x99)==0 and r(0xc1)~=0 and r(0x430)>=2')
 key='local dx=w(0x4a0,0x4b0)-w(0x4a1,0x4b1)';assert s.count(key)==1
 s=s.replace(key,'local follow=transferring and 2 or 1\n   local dx=w(0x4a0,0x4b0)-w(0x4a0+follow,0x4b0+follow)')
 key="if reason=='fixed'then reason='air_follow_boat'end";assert s.count(key)==1;s=s.replace(key,"if reason=='fixed'then reason=transferring and 'air_follow_raft2' or 'air_follow_boat'end")
 key='padlog:close();decisions:close()';assert s.count(key)==1;s=s.replace(key,key+';transferlog:close()')
 for quote in ["'",'"']:
  opened=False;esc=False
  for ch in s:
   if opened:
    assert ch not in '\r\n'
    if esc:esc=False
    elif ch=='\\':esc=True
    elif ch==quote:opened=False
   elif ch==quote:opened=True
  assert not opened
 assert 'emu.write('not in s and 'loadSavestate'not in s
 lua.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':160,'base_sha256':sha(src),'observer_sha256':sha(lua),'frames':6500,'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water160_raft_transfer049 --frames 6500 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_transfer160.lua','scope':'Controller-only A jump toward actual raft2 when raft1 begins falling and target exists; read-only native stage0716 and full final input requests. No success assumed.'},indent=2)+'\n','utf-8');print('PASS160 preflight')
if __name__=='__main__':main()
