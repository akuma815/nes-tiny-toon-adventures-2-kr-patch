from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'scripts/seal_coaster147.py';assert not p.exists()
 s=(R/'scripts/seal_cart146.py').read_text('utf-8').replace('146','147').replace('cart','coaster').replace('CART','COASTER')
 s=s.replace("assert v['actual_PRG_data_reads_each']==142","assert v['actual_PRG_data_reads_each']==137")
 s=s.replace('쇼킹 카트','롤러코스터').replace('짧은카트경로','롤러코스터 reader').replace('첫카트구간','초기 롤러코스터 구간')
 s=s.replace('기본티켓10장에서요금1장차감으로9장','기본티켓10장에서요금4장차감으로6장').replace('root4/phase5/course1','root4/phase5/course0').replace('339 wholePNG','312 wholePNG').replace('2712CHR','2496CHR').replace('read142건','read137건').replace('100 cycle동일/27건+38','81 cycle동일/41건+38').replace('helper18','helper16')
 s=s.replace('main1F(MAIN05867)','main1E(MAIN05849)').replace('main25(MAIN058F6)','main24(MAIN058F2)').replace('macro85(MACRO061DE)카트명','macro84(MACRO061D3)롤러코스터명').replace('native0C선택→1F/25','native0B선택→1E/24').replace('설명/요금1','설명/요금4')
 s=s.replace('4500 still first segment gameplay/HUD','4500 early rollercoaster gameplay/HUD').replace('cart title/rules and completed fee1','rollercoaster title/rules and completed fee4').replace('initial coaster game/HUD normal009','initial coaster game/HUD normal006')
 s=s.replace('티켓10→9','티켓10→6').replace('PRG142건/1F·25·macro85','PRG137건/1E·24·macro84').replace('각4500·339wholePNG','각4500·312wholePNG').replace('요금1','요금4')
 old="nxt='현재049/새047에서RAM seed 없는기본10장 롤러코스터메뉴·요금·출발경로를실행해,MAIN05849(rule1E)/MAIN058F2(title24)의실제reader/전줄NT완성과초기게임폰트수명을연결한다.'"
 new="nxt='성의normal49 거절과gold4 입장을현재049/새047에서각동결입력·seed로실행하며실제reader를기록해,main0F/16..1C/22/28의원천전체byte·완성NT를연결한다.'"
 assert old in s;s=s.replace(old,new).replace("replace('작업145 이후','작업147 이후')","replace('작업146 이후','작업147 이후')")
 p.write_text(s,'utf-8');print('prepared coaster147 handoff with exact measured counts')
if __name__=='__main__':main()
