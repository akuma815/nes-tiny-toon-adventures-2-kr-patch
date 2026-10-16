from pathlib import Path
import json
from analyze_river120_v2 import machine
from seal_continuation159 import R,sha,seal
def main():
 out=R/'qa/reports/water164_rope_model.json';assert not out.exists()
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';src,rom=sp.read_bytes(),rp.read_bytes()
 assert src[0x13711:0x13857]==rom[0x33711:0x33857]
 fixture=R/'qa/dialogue/water163_held_jump049/frame_08430_ram.bin';base=fixture.read_bytes();env=json.loads((fixture.parent/'environment.json').read_text('utf-8'));assert sha(fixture)==env['files'][fixture.name]
 x=base[0x4a2]+256*base[0x4b2];y=base[0x472]+240*base[0x482];assert x==3344 and y==368 and base[0x422]==2
 cases=[]
 for dx in [-24,0,24]:
  for dy in [-40,-16,0,16]:
   for vy in [-1,0]:
    for jump in [0,1]:
     b=bytearray(base);b[0x4a0]=(x+dx)&255;b[0x4b0]=(x+dx)>>8;b[0x470]=(y+dy)%240;b[0x480]=(y+dy)//240;b[0x4c0]=vy&255;b[0x4d0]=(vy>>8)&255;b[0x99]=jump
     pair=[]
     for data in [src,rom]:
      m,c=machine(data);m.ram[:2048]=b;c.pc=0xb701;n=0
      while c.pc not in [0xb700,0xb750]:c.step();n+=1;assert n<500
      pair.append((c.a,c.x,c.y,c.p,c.sp,c.pc,c.processorCycles,bytes(m.ram)))
     assert pair[0]==pair[1];caught=pair[0][5]==0xb750;assert(pair[0][-1][0xc9]!=0)==caught
     if caught:assert vy>=0 and pair[0][-1][0x541]==1
     cases.append({'player_dx':dx,'player_dy_packed240':dy,'player_Vy_signed':vy,'jump_before':jump,'captured':caught,'stop_PC':f'{pair[0][5]:04X}','cycles':pair[0][-2]})
 assert any(x['captured']for x in cases)and any(not x['captured']for x in cases)
 result={'work':164,'status':'PASS_BOUNDED_ROPE_CAPTURE_CONSUMER','source_sha256':sha(sp),'ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'fixture_sha256':sha(fixture),'CPU_pairs':cases,'fixture_target':{'type':2,'x':x,'y_packed240':y,'art2':base[0x402]},'finding':'Actualtype2 is rope/handle, not raft. NativeB701 checks nonnegative playerVy and collision with target2 offsetsX F0..10/Y EE..F4; B749 incrementsC9 and B74D sets0541. B774 heldUP selectsnegative verticalmotion; defaultdown, horizontalC0/256. Natural grab not yet observed.','natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['48 source/current CPU cases use synthetic player coordinates offline only; no runtime coordinate/state/RAM changes','Native rope consumer cases and actual target fixture are bounded, not globalgraphics/POW/clear proof','163 whole-prefix PNG equality failure remains unresolved; no new visual/render closure']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[48CPU 검증](../qa/reports/water164_rope_model.json), [분석 재현](../scripts/analyze_seal_water164.py), [실제8430 RAM](../qa/dialogue/water163_held_jump049/frame_08430_ram.bin).

실제type2/ED 구조물은통나무가아니라로프/손잡이다. nativeB701은 playerVy비음수와target2의 X F0..10/Y EE..F4 충돌상자를검사한다. 성공은B749 INC C9와B74D STA0541=1이다.48원본/049 CPU쌍에서양성/음성을검증했다. 합성player좌표는CPU만사용했고실제QA RAM변경없다. 붙잡은뒤nativeB774는UP held에서상향,기본하향이며가로C0/256으로이동한다. 실제붙잡기/그후clear는미관측이다.163의type1-only 갈아타기조건은이손잡이를제외했다.

변경:164분석/보고/상세/인계/journal/canonical·manifest/audit.원본SHA `{sha(sp)}`,ROM SHA `{sha(rp)}`,CSV SHA `{result['CSV_sha256']}`불변.각산출물SHA는manifest. 정적/48CPU/실제fixtureSHA PASS.새runtime/직접PNG/build/apply/reset/state/청음/실기/사람최종없음.163 PNG비교실패/자연급류clear/全corpus/HOWTO/PAUSE/POW/정식배포미완료.재현은스크립트출력경로새이름으로복제.카페원고/게시없음.'''
 seal(164,'WATER_ROPE_CAPTURE_NATIVE_MODEL.md','자연 손잡이 소비 조건',body,'type2=로프/손잡이.48CPU쌍 nonnegativeVy·충돌→C9/0541을검증,실제붙잡기는다음.','실제type2 손잡이를 향한 A/우측 도약을 컨트롤러에 추가하고 C9/0541 native쓰기·입력전수·후반진행을 새049 실행에서 확인한다.',[out,Path(__file__),sp,rp,fixture,fixture.parent/'environment.json',R/'scripts/analyze_river120_v2.py',R/'scripts/verify_gate_font_tag_hooks.py',R/'workspace/translation/text_ja.csv']);print('PASS164 48 rope CPU pairs')
if __name__=='__main__':main()
