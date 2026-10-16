from pathlib import Path
import json
from analyze_river120_v2 import machine
from seal_continuation159 import R,sha,seal
def run(data,ram,pc,stop):
 m,c=machine(data);m.ram[:2048]=ram;c.pc=pc;c.x=1;n=0
 while c.pc!=stop:c.step();n+=1;assert n<100
 return(c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram))
def main():
 out=R/'qa/reports/water159_raft_control_model.json';assert not out.exists()
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';src,rom=sp.read_bytes(),rp.read_bytes()
 fixture=R/'qa/dialogue/water158_exit_input049/frame_03990_ram.bin';base=fixture.read_bytes();env=json.loads((fixture.parent/'environment.json').read_text('utf-8'));assert sha(fixture)==env['files'][fixture.name]
 for a,b in [(0x12eee,0x12f55),(0x1317d,0x1324a),(0x12536,0x12546),(0x12594,0x125d6)]:assert src[a:b]==rom[a+0x20000:b+0x20000]
 tilt=[]
 for angle in range(-3,4):
  for pad in [0,1,2,64,65,66]:
   for tick in [0,3]:
    b=bytearray(base);b[0x511]=angle&255;b[0x531]=tick;b[0x52]=pad;b[0xc1]=1
    a=run(src,b,0xaede,0xaf45);z=run(rom,b,0xaede,0xaf45);assert a==z
    v=a[-1][0x511];v=v if v<128 else v-256;assert -3<=v<=3
    tilt.append({'angle_before':angle,'held':pad,'rotation_tick_before':tick,'angle_after':v,'tick_after':a[-1][0x531],'cycles':a[-2]})
 m,c=machine(src);speed=[];acceleration=[]
 for angle in range(-3,4):
  j=angle+3;maxv=m[0xb22a+2*j]*256+m[0xb22b+2*j];neg=m[0xb21c+2*j]*256+m[0xb21d+2*j];speed.append({'angle':angle,'positive_speed_target':maxv,'negative_speed_target_signed':neg-65536})
  for v in [96,255,416]:
   b=bytearray(base);b[0x511]=angle&255;b[0x4e1]=v&255;b[0x4f1]=v>>8
   a=run(src,b,0xb16d,0xb200);z=run(rom,b,0xb16d,0xb200);assert a==z
   actual=a[-1][0x4e1]+256*a[-1][0x4f1];assert actual==v+(5 if v<maxv else -5)
   acceleration.append({'angle':angle,'Vx_before':v,'Vx_after':actual,'target':maxv,'cycles':a[-2]})
 actors=[{'slot':i,'type':base[0x420+i],'art':base[0x400+i],'x':base[0x4a0+i]+256*base[0x4b0+i],'y_packed240':base[0x470+i]+240*base[0x480+i]}for i in [0,1,2]]
 assert actors[2]['type']==1 and actors[2]['x']==1224 and actors[1]['x']==1146
 result={'work':159,'status':'PASS_BOUNDED_RAFT_CONTROL_AND_ACTUAL_NEXT_RAFT_BINDING','source_sha256':sha(sp),'ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'fixture_sha256':sha(fixture),'tilt_CPU_pairs':tilt,'speed_target_data':speed,'acceleration_CPU_pairs':acceleration,'actual3990_actors':actors,'finding':'B+right rotates raft toward+3; positive target256 atangle0/416 at+3, step5 oscillates. Actual second raft exists78px ahead at3990. Previous air-follow always targeted raft1. Transfer jump must target existing raft2; runtime landing not yet proven.','correction158':'158 boundary loop has16 CPU pairs, not32 as frozen prose says; JSON case list authoritative.','natural_clear_observed':False,'human_approved':False,'release_eligible':False}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[검증 보고](../qa/reports/water159_raft_control_model.json), [분석 재현](../scripts/analyze_seal_water159.py), [실제3990 RAM](../qa/dialogue/water158_exit_input049/frame_03990_ram.bin).

원본/049 nativeAEDE..AF45를84쌍 CPU로 검증했다. B+우측이 기울기를+3 방향으로 바꾼다. B16D..B200 21쌍은 가로속도를5씩 target으로 이동시키며, angle0 target256/+3 target416이다. target 도달/유지는 실제 경로 검증이 아니다. 3990의 raft1 X1146/Y377, raft2 X1224/Y408(type1/artDF)은 기존 실제 관측이다. 다음 통나무가78px 앞에 존재한다. 이전 컨트롤러는 공중조작으로 raft1 중심을 계속 따라갔다. raft2 목표의 A/우측 갈아타기는 새 가설로 검증해야 한다.

작업158 prose/인계의32경계 CPU쌍은16쌍으로 정정한다. JSON16항목이 실제 결과다. 기존 동결 이력을 보존한다. 외부 설명서 PDF는 접근실패로 내용/조작 근거로 사용하지 않았다.

변경:159분석/공통인계스크립트·보고·상세/날짜별인계/journal/canonical·manifest/audit. 원본 SHA `{sha(sp)}`, ROM SHA `{sha(rp)}`, CSV SHA `{result['CSV_sha256']}` 불변. 각산출물SHA는manifest. 정적/105CPU쌍/fixtureSHA PASS. 새실행/직접PNG/build/apply/reset/state/청음/실기/사람최종없음. 자연갈아타기/전체게임/全corpus/HOWTO/PAUSE/POW/정식배포미완료. 재현은분석스크립트출력경로를 새이름으로복제. 카페원고/게시없음.'''
 seal(159,'WATER_RAFT_CONTROL_AND_TRANSFER_MODEL.md','통나무 B 조작과 다음 통나무 연결',body,'84기울기/21속도CPU쌍. 실제다음raft가78px 앞에 존재.158 경계 표기32→16 정정.','실제 raft2 존재와 낙차 조건에 따라 A+우측으로 착지 목표를 raft2로 바꾼 컨트롤러를 새049 실행으로 검증한다.',[out,Path(__file__),sp,rp,fixture,fixture.parent/'environment.json',R/'scripts/analyze_river120_v2.py',R/'scripts/verify_gate_font_tag_hooks.py',R/'qa/reports/water158_exit_input_validation.json',R/'workspace/translation/text_ja.csv']);print('PASS159 84tilt+21speed pairs')
if __name__=='__main__':main()
