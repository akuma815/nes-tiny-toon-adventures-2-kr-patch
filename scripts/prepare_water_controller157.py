from pathlib import Path
import hashlib,json,csv
from analyze_river120_v2 import machine
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def signed(x):return x if x<128 else x-256
def packed_y_add(word,off):
 z=(word+signed(off))&65535;hi,lo=z>>8,z&255
 if hi==word>>8:
  if lo>=240:hi=(hi+1)&255;lo=(lo+16)&255
 else:lo=(lo+(16 if off<128 else -16))&255
 return lo+hi*256
def box(ram,slot,shape):
 x=ram[0x4a0+slot]+256*ram[0x4b0+slot];y=ram[0x470+slot]+256*ram[0x480+slot]
 return [(x+signed(shape[0]))&65535,(x+signed(shape[1]))&65535,packed_y_add(y,shape[2]),packed_y_add(y,shape[3])]
def main():
 report=R/'qa/reports/water157_bbox_model.json';lua=R/'scripts/trace_water_controller157.lua';plan=R/'work/water157/run_plan.json';assert not any(p.exists()for p in [report,lua,plan])
 src=(R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes').read_bytes();rom=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 assert src[0x1e753:0x1e8ec]==rom[0x3e753:0x3e8ec]
 m,c=machine(src)
 player=[]
 for i in range(12):
  p=m[0xe743+i*2]+256*m[0xe744+i*2];player.append([m[p+j]for j in range(4)])
 actor=[[m[0xe8dc+i*4+j]for j in range(4)]for i in range(64)]
 q=R/'qa/dialogue/water154_damage049';events=list(csv.DictReader((q/'damage_events.csv').open()))
 tests=[]
 for event in events:
  if event['address']!='0430':continue
  r=(q/f"damage_{int(event['event']):04d}_before_ram.bin").read_bytes();slot=int(event['x']);shape=actor[r[0x530+slot]%64]
  for ylow in [0,16,104,239,240,255]:
   for offslot,offsets in [(0,player[0]),(slot,shape)]:
    pair=[];b=bytearray(r);b[0x470+offslot]=ylow
    for data in [src,rom]:
     mm,cc=machine(data);mm.ram[:2048]=b;mm.ram[0x10:0x14]=bytes(offsets);mm.ram[0x1fe:0x200]=bytes.fromhex('ff5f');cc.pc=0xe833;cc.x=offslot;cc.sp=0xfd;cc.p=0x30;steps=0
     while cc.pc!=0x6000:cc.step();steps+=1;assert steps<200
     actual=[mm.ram[j]+256*mm.ram[j+1]for j in [0,2,4,6]];assert actual==box(b,offslot,offsets);pair.append((cc.a,cc.x,cc.y,cc.p,cc.sp,cc.processorCycles,bytes(mm.ram)))
    assert pair[0]==pair[1];tests.append({'event':int(event['event']),'slot':offslot,'Ylow':ylow,'bounds':box(b,offslot,offsets)})
 report.write_text(json.dumps({'work':157,'status':'PASS_BOUNDED_NATIVE_COLLISION_BOX_COMPILER','ROM_sha256':hashlib.sha256(rom).hexdigest(),'CPU_case_pairs':tests,'player_profiles':player,'actor_shapes':actor,'geometry':'Native E833 signed offsets, modulo16 X and packed240-row Y carry adjustment; E74312 player profiles/E8DC64 shape entries. Future constant-velocity prediction is a new controller hypothesis, not CPU proof.','human_approved':False,'limits':['36 named source/current CPU pairs cover actual actor fixtures and Y boundary values; not whole geometry domain','Adaptive controls change controller only; no native coordinate/state writes']},ensure_ascii=False,indent=2)+'\n','utf-8')
 base=(R/'scripts/trace_water_damage154.lua').read_text('utf-8')
 tables='local profiles='+json.dumps(player,separators=(',',':')).replace('[','{').replace(']','}')+'\nlocal shapes='+json.dumps(actor,separators=(',',':')).replace('[','{').replace(']','}')+'\n'
 addition=r'''
-- Controller-only geometry prediction. All input polls recorded; no RAM writes.
local padlog=assert(io.open(out..'/adaptive_inputs.csv','wb'))
padlog:write('poll,frame,a,b,left,right,up,down,start,select,reason,target,player_x,boat_x,jump,life\n')
local decisions=assert(io.open(out..'/jump_decisions.csv','wb'))
decisions:write('frame,actor,predicted_horizon,actor_state,player_x,actor_x,player_y,actor_y,boat_x,life\n')
local polls=0;local untilA=-1;local lastjump=-100;local reason='fixed';local target=-1
local function r(a)return emu.read(a,emu.memType.nesDebug)end
local function w(lo,hi)return r(lo)+256*r(hi)end
local function sg(v)return v<128 and v or v-256 end
local function bit_or(a,b)local z=0;local p=1;for i=1,8 do if a%2==1 or b%2==1 then z=z+p end;a=math.floor(a/2);b=math.floor(b/2);p=p*2 end;return z end
local function yadd(y,o)
 local z=(y+sg(o))%65536;local hi=math.floor(z/256);local lo=z%256
 if hi==math.floor(y/256)then if lo>=240 then hi=(hi+1)%256;lo=(lo+16)%256 end
 else lo=(lo+(o<128 and 16 or -16))%256 end
 return lo+256*hi
end
local function bbox(i,s)
 local x=w(0x4a0+i,0x4b0+i);local y=w(0x470+i,0x480+i)
 return {(x+sg(s[1]))%65536,(x+sg(s[2]))%65536,yadd(y,s[3]),yadd(y,s[4])}
end
local function yp(y)return math.floor(y/256)*240+y%256 end
local function player_shape()
 if r(0x721)~=0 then return nil end
 local index=bit_or(r(0xa2),r(0x722))*2+(r(0xa8)~=0 and 1 or 0)+1
 return profiles[index]
end
local function predict()
 local ps=player_shape();if not ps then return nil end
 local pb=bbox(0,ps);local bvx=(w(0x4e1,0x4f1));if bvx>=32768 then bvx=bvx-65536 end;bvx=bvx/256
 local bvy=w(0x4c1,0x4d1);if bvy>=32768 then bvy=bvy-65536 end;bvy=bvy/256
 for i=2,15 do
  if r(0x420+i)==0x44 then
   local ab=bbox(i,shapes[r(0x530+i)%64+1])
   local avx=w(0x4e0+i,0x4f0+i);if avx>=32768 then avx=avx-65536 end;avx=avx/256
   local avy=w(0x4c0+i,0x4d0+i);if avy>=32768 then avy=avy-65536 end;avy=avy/256
   for n=8,20 do
    local ax0,ax1=ab[1]+avx*n,ab[2]+avx*n;local px0,px1=pb[1]+bvx*n,pb[2]+bvx*n
    local ay0,ay1=yp(ab[3])+avy*n,yp(ab[4])+avy*n;local py0,py1=yp(pb[3])+bvy*n,yp(pb[4])+bvy*n
    if ax1>=px0 and px1>=ax0 and ay1>=py0 and py1>=ay0 then return i,n end
   end
  end
 end
 return nil
end
emu.addEventCallback(function()
 local input={start=false,select=false,a=false,b=false,up=false,down=false,left=false,right=false}
 for _,e in ipairs(sequence)do if frame>=e.frame and frame<e.frame+e.duration then input[e.button]=true end end
 reason='fixed';target=-1
 if frame>=3300 and r(0x18)==4 and r(0x54)==5 and r(0x25)==3 then
  if r(0x99)==0 and r(0xc1)~=0 and r(0x430)>=2 and r(0x430)<=3 and frame-lastjump>=40 then
   local i,n=predict()
   if i then
    untilA=frame+8;lastjump=frame;target=i;reason='predicted_actor'
    decisions:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,i,n,r(0x430+i),w(0x4a0,0x4b0),w(0x4a0+i,0x4b0+i),w(0x470,0x480),w(0x470+i,0x480+i),w(0x4a1,0x4b1),r(0x7c0)))
   end
  end
  if frame<untilA then input.a=true end
  if input.a or r(0x99)~=0 and r(0xc1)==0 then
   local dx=w(0x4a0,0x4b0)-w(0x4a1,0x4b1)
   input.right=dx<=0;input.left=dx>0
   if reason=='fixed'then reason='air_follow_boat'end
  end
 end
 emu.setInput(input,0);polls=polls+1
 local b=function(v)return v and 1 or 0 end
 padlog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d,%d,%d\n',polls,frame,b(input.a),b(input.b),b(input.left),b(input.right),b(input.up),b(input.down),b(input.start),b(input.select),reason,target,w(0x4a0,0x4b0),w(0x4a1,0x4b1),r(0x99),r(0x7c0)))
end,emu.eventType.inputPolled)
emu.addEventCallback(function()if frame==limit then padlog:close();decisions:close()end end,emu.eventType.endFrame)
'''
 # Raw template contains intentional literal backslash-n, suitable for Lua.
 addition=addition.replace('\\n','\n')
 s=base+'\n'+tables+addition
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
 plan.write_text(json.dumps({'work':157,'observer_sha256':sha(lua),'geometry_report_sha256':sha(report),'fixed_prefix_input':'config/water_first_hazard_steer156.json','adaptive_start_frame':3300,'frames':9000,'scope':'Read-only native geometry plus actual logged controller predictions; not a preverified winning route','command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water157_controller049 --frames 9000 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_controller157.lua','input_evidence':'adaptive_inputs.csv records every final input poll; environment.input is fixed prefix only. Adaptive Lua callback overrides inherited fixed callback after3300.'},indent=2)+'\n','utf-8');print('PASS157 bbox36source/current CPU pairs; prepared controller hypothesis')
if __name__=='__main__':main()
