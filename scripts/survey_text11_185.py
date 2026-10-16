"""Global11px ink target: static font/packing prototype; not a game build."""
from pathlib import Path
import csv,json,math,textwrap
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from extract_title_png import encode,decode
from seal_nonplay171 import R,sha,seal

def main():
    out=R/'workspace/review/text11_185';out.mkdir(parents=True,exist_ok=False)
    fonts=R/'workspace/fonts/galmuri11_candidate185';oldfont=R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf';newfont=fonts/'Galmuri11.ttf'
    old=ImageFont.truetype(str(oldfont),8);new=ImageFont.truetype(str(newfont),12)
    rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')))
    texts=[r for r in rows if r['translation_ko'] and r['status']=='draft']
    chars=set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!?.,× 체력점수시간티켓금정지')
    for r in texts:chars.update(c for c in r['translation_ko'] if not c.isspace())
    cm=TTFont(newfont).getBestCmap();missing=sorted(c for c in chars if ord(c) not in cm);assert not missing,missing
    boxes=[]
    for c in sorted(chars):
        if c==' ':continue
        im=Image.new('L',(32,32));ImageDraw.Draw(im).text((0,-1),c,font=new,fill=1)
        box=im.getbbox();assert box,(c,'empty')
        if '\uac00'<=c<='\ud7a3':assert box[3]-box[1]<=11 and box[2]<=12 and box[3]<=11,(c,box)
        boxes.append({'char':c,'ink_bbox':box,'advance':new.getlength(c)})
    # Paragraph-based bitmap prototype:12px fixed cells,16px line step,192px width.
    layouts=[]
    for r in texts:
        lines=[]
        for line in r['translation_ko'].split('\n'):
            lines.extend([line[i:i+16] for i in range(0,len(line),16)] or [''])
        layouts.append({'entry_id':r['entry_id'],'old_line_count':len(r['translation_ko'].split('\n')),'candidate_lines':lines,'candidate_line_count':len(lines),'needs_more_than_4_lines_at_192px':len(lines)>4,'note':'Character slicing only for capacity audit; final Korean word wrapping/pagination not implemented.'})
    sample=next(r for r in texts if r['entry_id']=='MAIN_05625')
    samplelayout=next(x for x in layouts if x['entry_id']==sample['entry_id'])
    bitmap=Image.new('L',(192,64));d=ImageDraw.Draw(bitmap)
    for i,line in enumerate(samplelayout['candidate_lines'][:4]):
        for x,c in enumerate(line):d.text((12*x,16*i-1),c,font=new,fill=2)
    data=bytearray()
    for y in range(0,64,8):
        for x in range(0,192,8):
            pixels=bytes(bitmap.crop((x,y,x+8,y+8)).get_flattened_data());raw=encode(pixels);assert decode(raw)==pixels;data.extend(raw)
    assert len(data)==192*16
    (out/'paragraph_12x16_prototype.chr').write_bytes(data)
    # Independent tile decode into full layout, prove packing without a game claim.
    recovered=Image.new('L',bitmap.size);i=0
    for y in range(0,64,8):
        for x in range(0,192,8):recovered.paste(Image.frombytes('L',(8,8),decode(data[i:i+16])),(x,y));i+=16
    assert recovered.tobytes()==bitmap.tobytes()
    # Newly drawn diagram, no runtime screenshot or asset edits.
    canvas=Image.new('RGB',(256,236),(25,25,32));d=ImageDraw.Draw(canvas)
    d.text((8,5),'STATIC DESIGN / NOT GAME CAPTURE',font=old,fill='white')
    d.text((8,22),'CURRENT:8x8 CELL / 24 COLUMNS',font=old,fill=(255,170,255))
    d.rectangle((31,38,224,101),fill='black',outline=(255,170,255))
    for y,line in enumerate(sample['translation_ko'].split('\n')):d.text((32,40+16*y-1),line,font=old,fill='white')
    d.text((8,110),'TARGET:11px INK /12x16 CELL',font=old,fill=(255,170,255))
    d.text((8,123),'SAME192px WIDTH /16 COLUMNS',font=old,fill=(255,170,255))
    d.rectangle((31,139,224,204),fill='black',outline=(255,170,255))
    for y,line in enumerate(samplelayout['candidate_lines'][:4]):
        for x,c in enumerate(line):d.text((32+x*12,141+y*16-1),c,font=new,fill='white')
    d.text((8,216),'LAYOUT+PRINTER+HUD REWORK REQUIRED',font=old,fill='white')
    canvas.save(out/'comparison_native.png');canvas.resize((1024,944),Image.Resampling.NEAREST).save(out/'comparison_4x.png')
    source={'candidate_only':True,'font':'Galmuri11','version':'2.404 releasev2.40.4','upstream':'https://github.com/quiple/galmuri/releases/tag/v2.40.4','release_zip_sha256':sha(R/'tools/fonts/galmuri_v2_40_4_185/Galmuri-v2.40.4.zip'),'official_recommended_em_px':12,'target_actual_Hangul_ink_height_max':11,'cell':[12,16],'rasterization':'Pillow font12; x0,y-1; no resize, antialias threshold not used: native aligned pixel shapes','license':'SIL OFL1.1; LICENSE.txt from release','files':{p.name:sha(p) for p in fonts.iterdir() if p.is_file()},'human_visual_approved':False}
    (fonts/'font_source.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n','utf-8')
    report={'work':185,'status':'PASS_STATIC_GLOBAL11PX_FONT_AND_PACKING_FEASIBILITY_ONLY','request':'Whole game text11px; previous assumption of moving STOP only corrected.','adopted_build_unchanged':'dialogue_kr_poc_051','ROM_sha256':sha(R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'draft_entries':len(texts),'tested_characters':len(chars),'missing_glyphs':missing,'glyph_metrics':boxes,'layout_candidates':layouts,'over4_lines_at192px':sum(x['needs_more_than_4_lines_at_192px'] for x in layouts),'bitmap_tiling_roundtrip_exact':True,'paragraph_full4line_capacity':{'pixel_width':192,'line_count':4,'line_height':16,'CHR_tiles':192,'CHR_bytes':3072,'existing_dialogue_font_pair_tiles':128,'existing_dialogue_font_pair_bytes':2048,'conclusion':'Four-row packed pre-rendered candidate exceeds existing2KiB dialogue font pair; CHR mapping/residency must change. Alternative glyph reuse/VWF needs separate working-set proof.'},'paths_requiring_changes':['main dialogue printer,cursor,buffers,controls,clear,pagination','shared UI/ride guides,ticket/score/name macros,dynamic digits','HUD captions,digits,borders,IRQ geometry','results/gameover selectors,credits scroll','bitmap word signs:currentSTOP inner field6..7px wide cannotfit12px cells; needsassetlayout change if included'],'not_verified':['actualNES consumption','CPU/NMI/IRQ budget','working-set residency throughwait/clear/transition','full corpus including all graphics text','final Korean wordwrap/pagination','HUD layout','runtime/user gameplay','global11px adopted ROM'],'sample_note':'comparison PNG is newly drawn static layout diagram, not actual game evidence.'}
    p=R/'qa/reports/text11_185_feasibility.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자가“전체텍스트를11로”라고정정했다. 앞서움직이는표지판만으로이해한조사는폐기하고게임전체의일반한글·숫자·기호를확대하는요구로기록한다. **051은현재검증기준으로보존하며아직11px ROM을채택하지않았다.**

현재일반대사/안내/크레딧/결과는Galmuri7 8×8 한타일,한글획은보통6×7. 대사192px 폭에24칸,카드매크로·숫자및FE/FF/FD/FA·커서/버퍼/소거가원래칸수와결합돼있다. HUD는상단캡션7행조차fineY/IRQ를조정해확보했다. 따라서font size 숫자만8→11로바꾸면글자가잘리고기존reader가두번째타일행을출력하지않는다.11px는하드웨어상불가능이라고판정한것이아니라**출력기·버퍼·페이지/레이아웃·글꼴공급의개편이필요**하다.

후보:Galmuri11v2.40.4를공식고정릴리즈에서취득하고원본ZIP·TTF/BDF/OFL·SHA를별도보존. 공식EM크기는12px이며로컬측정에서한글획높이는최대11px다. ‘Galmuri11’ 이름/EM12/실제획11/12×16출력셀을구분한다. [후보출처](../workspace/fonts/galmuri11_candidate185/font_source.json), [공식설명](https://github.com/quiple/galmuri). 현재Galmuri7 입력은바꾸지않았다.

정적근거:45draft본문과숫자/영문/기호의후보cmap·빈글리프·한글획범위검사. [상세보고](../qa/reports/text11_185_feasibility.json)는본문수·문자수·각문장줄수·글리프측정치를포함한다.192px폭의12px셀은16칸으로감소.기존문구는그대로두고줄바꿈/페이지를늘려야한다.4줄192×64 bitmapprototype의NES2bpp왕복 exact(192타일/3072바이트);현재2KiB/128타일 대사font pair를초과하므로매퍼공급/동적glyph재사용을다시설계해야한다. 이한정정적PoC는실제PPU소비나전체작동증거가아니다.

[크기·배치비교PNG](../workspace/review/text11_185/comparison_4x.png)는설명용새도식이며실제게임캡처가아니다. 갈무리11 미감이나전체그림최종승인은아직없다.11px 전체확대에는대사/안내/선택지뿐아니라HUD/동적숫자/결과/스크롤크레딧을각경로검증해야한다.그림간판의STOP 내부폭6..7px는확대폰트를넣을수없어그림글자까지포함할경우표지판모양/크기조정이필요하다.원문유지6건결정과타이틀그림을일괄자동변경하는승인으로확대하지않는다.

미수행:ROM개조/실제NES실행/CPU·NMI·IRQ시간/글꼴생명주기/전체원천완결/최종한국어줄바꿈/새HUD배치/사용자플레이. 에뮬레이터와사용자세이브를조작하지않았다. 정적조사와원천후보/도식작성만수행. 원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`,051SHA `{report['ROM_sha256']}`,CSV SHA `{report['CSV_sha256']}` 불변.카페완성작업기/게시없음.

재현: `python scripts/survey_text11_185.py`는이미있는후보/도식/인계를보존하기위해덮어쓰기를거절한다. 변경파일/전체해시는manifests/nonplay185_assets.json. candidateは新入力で現在ビルド採用フォントではない。'''
    body=body.replace('candidateは新入力で現在ビルド採用フォントではない。','후보는새입력이며현재빌드채택폰트가아니다.')
    next_action='11px 일반대사의12×16 출력셀/줄바꿈·소거·CHR공급 경로를 설계하고 대표문단 삽입PoC를 만든다.'
    assets=[Path(__file__),p,*[x for folder in (out,fonts,R/'tools/fonts/galmuri_v2_40_4_185') for x in folder.rglob('*') if x.is_file()]]
    seal(185,'GLOBAL_TEXT11_FEASIBILITY_185.md','전체텍스트11px 정적가능성·배치후보',body,'요구를전체텍스트11px로정정.현재8×8 출력은그대로대체불가;12×16셀/192px16칸/4줄3KiB 정적후보와PNG 비교작성.실제ROM/CPU/PPU검증전이며051 보존.',next_action,assets)
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업185','현재 개발051 / 작업185',1);p.write_text(s,'utf-8')
    print(json.dumps({k:report[k] for k in ['status','draft_entries','tested_characters','missing_glyphs','over4_lines_at192px','ROM_sha256','CSV_sha256']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
