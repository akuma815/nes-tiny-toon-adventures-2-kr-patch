"""Close reported HUD margins as original layout with measured2px localization shift."""
from pathlib import Path
import json,csv,base64
from PIL import Image,ImageChops
from seal_nonplay171 import R,sha,seal

def j(p):return json.loads(p.read_text('utf-8'))
def main():
    report=R/'qa/reports/hud180_geometry.json';assert not report.exists()
    old=R/'qa/dialogue/hud180_coaster_source';new=R/'qa/dialogue/hud180_coaster_050'
    oe,ne=[j(d/'environment.json') for d in [old,new]]
    assert oe['exit_code']==ne['exit_code']==0
    for k in ['exe_sha256','lua_sha256','config_sha256','frames','input','intervention']:assert oe[k]==ne[k],k
    for d,e in [(old,oe),(new,ne)]:
        for f,h in e['files'].items():assert sha(d/f)==h,(d.name,f)
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rom=R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes'
    s=source.read_bytes();r=rom.read_bytes();assert sha(source)==oe['rom_sha256'] and sha(rom)==ne['rom_sha256']
    assert s[0xd182:0xd282]==r[0xd182:0xd282]
    assert s[0x1fce5]==0x2f and r[0x3fce5]==0x0f and s[0x1fcf9]==124 and r[0x3fcf9]==206
    writes=[list(csv.DictReader((d/'hud_register_writes.csv').open(encoding='utf-8'))) for d in [old,new]]
    assert writes[0]==writes[1] and len(writes[0])==1896
    samples=[]
    for f in sorted(old.glob('*_ram.bin')):
        a=f.read_bytes();b=(new/f.name).read_bytes();tag=f.name[:-8]
        if a[0x18]!=4 or b[0x18]!=4:continue
        im=[Image.open(d/(tag+'.png')).convert('RGB') for d in [old,new]]
        if len(set(im[0].crop((8,190,256,215)).get_flattened_data()))==1:continue
        assert a[0x25]==b[0x25]==0
        assert (old/(tag+'_ppu.bin')).read_bytes()[0x2000:]==(new/(tag+'_ppu.bin')).read_bytes()[0x2000:]
        assert ImageChops.difference(im[0].crop((0,0,256,190)),im[1].crop((0,0,256,190))).getbbox() is None
        assert im[0].crop((0,190,8,240)).tobytes()==im[1].crop((0,190,8,240)).tobytes()
        assert all(im[0].getpixel((x,y))==(0,0,0) for x in range(8,256) for y in range(215,235))
        assert all(im[1].getpixel((x,y))==(0,0,0) for x in range(8,256) for y in range(217,237))
        assert im[0].crop((8,215,256,238)).tobytes()==im[1].crop((8,217,256,240)).tobytes()
        samples.append(int(tag[6:]))
    assert len(samples)==7
    # Use one observed frame for exact strip heights; these colors are scene-specific.
    ims=[Image.open(d/'frame_03000.png').convert('RGB') for d in [old,new]]
    assert all(ims[0].getpixel((x,y))==(192,223,255) for x in range(8,256) for y in range(235,240))
    assert all(ims[1].getpixel((x,y))==(192,223,255) for x in range(8,256) for y in range(237,240))
    states=[dict(x.split('=',1) for x in (d/'frame_03000_state.txt').read_text('utf-8').splitlines()) for d in [old,new]]
    for st in states:
        assert st['ppu.mask.backgroundEnabled']=='true' and st['ppu.mask.backgroundMask']=='false' and st['ppu.mask.spriteMask']=='false'
    html=R/'workspace/review/hud180/compare.html';assert not html.exists();html.parent.mkdir(parents=True)
    blocks=''.join(f'<figure><figcaption>{label}</figcaption><img width="768" height="720" alt="{label} 실제 실행 화면" src="data:image/png;base64,{base64.b64encode((d/"frame_03000.png").read_bytes()).decode()}"></figure>' for label,d in [('일본판 원본',old),('한글 개발050',new)])
    html.write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HUD 원본과050 비교180</title><style>body{font-family:sans-serif;background:#eee;margin:24px}main{display:flex;flex-wrap:wrap;gap:20px}figure{margin:0;max-width:100%}img{max-width:100%;height:auto;image-rendering:pixelated}figcaption{font-weight:bold;margin:10px 0}</style><h1>상태창 왼쪽·아래 여백 비교</h1><p>동일 host·설정·입력의 실제3000프레임 캡처. 원본에도 왼쪽8픽셀 배경색과 창 아래 검은20픽셀 여백이 있다. 050는 한글높이 확보를 위해 HUD 내용을2픽셀 내린 기존변경으로 검은여백/맨아래띠도2픽셀 이동한다.</p><main>'+blocks+'</main><p>사진에 화소 수정/생성형 보정 없음. 256×240 원본PNG를CSS로확대했다. 사용자가보낸후반갈색지형의동일프레임을복원한것은아니며 같은롤러코스터HUD의원본/050 비교다. 브라우저시각검증/전게임검증 주장없음.</p></html>','utf-8')
    d={'work':180,'status':'PASS_ORIGINAL_HUD_LEFT_AND_BOTTOM_LAYOUT_WITH_KNOWN_2PX_KOREAN_SHIFT','source_sha256':sha(source),'ROM050_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_and050_controller_only_runs':3600,'same_host_settings_input':True,'visible_HUD_paired_frames':samples,'native_PPUMASK_write_rows_exact':1896,'native_HUD_template_equal':True,'HUD_NT_attribute_palette_equal':True,'outside_HUD_gameplay_RGB_equal':True,'left8_HUD_RGB_equal':True,'black_bottom_margin_height_pixels':20,'frame3000_source_black_margin_y':[215,235],'frame3000_050_black_margin_y':[217,237],'frame3000_source_bottom_backdrop_height':5,'frame3000_050_bottom_backdrop_height':3,'localization_change':'Previously adopted work44 fineY2->0 shifts HUD body+2pixels, preserving7 visible Korean header rows. Not a new050 change.','left_clip_cause':'Measured PPUMASK18: background/sprite left8 disabled in source and050. Backdrop hue varies with scene.','comparison_HTML':html.relative_to(R).as_posix(),'fullplay':False,'ROM_CSV_package_changed':False,'limits':['Same rollercoaster HUD and matching cold input scene, not exact late brown-terrain user frame/state','Only seven rendered HUD snapshots, not all rides/scroll/reset/emulator configurations','First cart observer pair incomplete exitFFFFFFFF; not gameplay-defect evidence. Narrow PPUMASK observer v2 passed.']}
    report.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자가 실행화면 상태창 왼쪽과 아래가채워지지않는다고원본/패치여부확인을요청했다. 기술결론: 왼쪽8픽셀배경색띠/창아래검은여백은원본에존재한다.050새결함이아니다. 한글HUD를처음삽입한44에서fineY2→0으로내용을2픽셀아래로옮긴차이는별도로남아있다. 그래서아래끝배경색띠높이는이관측시점원본5픽셀/0503픽셀이며이전의큰여백을새로만든것은아니다. 글자높이7행확보용기존변경을누락이나완전동일로표현하지않는다.

[정적/실행 보고](../qa/reports/hud180_geometry.json), [실제 원본/050 확대 비교](../workspace/review/hud180/compare.html), [원본3000PNG](../qa/dialogue/hud180_coaster_source/frame_03000.png), [0503000PNG](../qa/dialogue/hud180_coaster_050/frame_03000.png). 같은격리MesenCE2.2.1·설정·controller로각3600프레임coldboot, seed/강제PC/세이브로드/RAM·ROM쓰기없음. 첨부이미지의후반갈색지형정확시점을복원한것은아니며같은롤러코스터HUD경로의서로동일한장면을대조했다.2880..3600간실제HUD7시점의왼쪽8픽셀RGB동일,全NT/attribute/palette동일,HUD위게임화면全RGB동일. 원본의검은여백20픽셀(y215..234)이050에서같은20픽셀(y217..236)이고bottomRGB가2픽셀shift로exact. 실제PPUMASK쓰기1896행의프레임/PC/값/scanline/dot도모두동일. source/current PPUMASK18·leftbg/spr disabled를확인했다. [NESdev PPU programmer reference](https://www.nesdev.org/wiki/PPU_programmer_reference#PPUMASK)는왼쪽8픽셀을숨길때배경색을표시함을설명한다. 해당지형이갈색이면띠도갈색으로보이는것은같은mask조건의palette에대한해석이며첨부프레임RAM은읽지않았다.

정적source HUD template D182..D281은050와동일. 원본fixed-bank fineY operand1FCE5=2F/current3FCE5=0F, fonte1FCF9=124/current3FCF9=206; 이는기존 [HUD44 검증](../qa/reports/game040_validation.json)의7행/2픽셀설계다. 현재ROM SHA `{sha(rom)}`, CSV SHA `{d['CSV_sha256']}` 불변. [050적용ZIP178](../dist/TinyToonAdventures2_KR_Review_050_BoothFix_20261008.zip)도변경없음. 조사/보고/HTML만생성하며이요청으로원본디자인변경이나추가패치를하지않았다.

관측기록: 첫menu_cart경로와넓은2000..2006 observer는두실행모두exitFFFFFFFF/완료기록없음으로보존했다.원인확정이나게임결함으로닫지않는다. 첨부화면의롤러코스터경로로대상을명확히하고2001만관측하는v2에서두실행exit0/3600완료확인. 구사본을수정하지않고 [v2 runner](../scripts/run_hud180_v2.py)와 [v2 observer](../scripts/trace_hud180_v2.lua)를신규생성했다. 재현: `python scripts/run_hud180_v2.py --rom "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --output qa/dialogue/NEW_HUD_SOURCE --frames 3600 --inputs config/menu_coaster_001.json --script scripts/trace_hud180_v2.lua`;050는rom인자를현재050로바꾼다.기존출력보호. 시작source검증은ExecutionPolicy거절후별도 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1`로PASS했다. 정책영구변경없음.

변경:4runner/observer·verifyseal·네실행QA·HTML/JSON·dated/journal/SURVEY/PLAN/README/canonical/manifest. 정적/두v2에뮬레이터/직접실제PNG비교PASS. 새빌드/적용/청음/전게임완주/실제사용자live조회/최종사람검수/HTML브라우저시각검증 없음. 원본·1편·기존QA/현재Mesen·세이브는수정하지않았다.44의오래된증거는현050실행과구분했다. 카페완성글/게시없음.'''
    files=[Path(__file__),R/'scripts/run_hud180.py',R/'scripts/trace_hud180.lua',R/'scripts/run_hud180_v2.py',R/'scripts/trace_hud180_v2.lua',R/'config/menu_cart_001.json',R/'config/menu_coaster_001.json',report,html,source,rom,R/'workspace/translation/text_ja.csv',R/'qa/reports/game040_validation.json']
    for name in ['hud180_cart_source','hud180_cart_050','hud180_coaster_source','hud180_coaster_050']:files.extend(p for p in (R/'qa/dialogue'/name).iterdir() if p.is_file())
    seal(180,'HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md','상태창 왼쪽·아래 원본비교 조사',body,'원본에도왼쪽8픽셀배경색띠/창아래검은20픽셀여백존재. 실제source/0507HUD시점·PPUMASK1896행동일.44의한글높이용2픽셀shift는구분;ROM/패키지변경없음.','사용자 실제 플레이 검수를 이어가며 새로 발견한 표시 문제를 해당 장면과 함께 기록한다.',files)
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';text=p.read_text('utf-8').replace('현재 개발049 / 작업180','현재 개발050 / 작업180',1);p.write_text(text,'utf-8')
    p=R/'docs/HANDOFF.md';text=p.read_text('utf-8');i=text.index('[작업107 실제');text=text[:i]+'최신상태창조사 [180](HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md): 왼쪽띠/아래여백은원본구성,7개현재source/050 HUD시점으로확인했다.44의2픽셀한글HUD이동은별도다.현재050 ROM/CSV/적용ZIP178 유지.\n\n'+text[i:];p.write_text(text,'utf-8')
    print(json.dumps({'status':d['status'],'HUD_samples':len(samples),'left_pixels':8,'black_margin_pixels':20,'source_bottom_backdrop':5,'050_bottom_backdrop':3,'ROM_changed':False},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
