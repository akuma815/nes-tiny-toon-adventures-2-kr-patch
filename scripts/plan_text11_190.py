"""Consumer-separated11px capacity plan; no ROM edits or emulator execution."""
from pathlib import Path
import csv,json,collections,html,re
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from extract_title_png import encode,decode
from compile_ui_card_group import variable_codes
from verify_dialogue_home import MPU
import seal_nonplay171 as records
from seal_nonplay171 import R,sha

def family(slot):
    if slot<=9:return 'opening_verified053'
    if slot<=0x15:return 'home_booth_lower'
    if slot<=0x1c:return 'castle_lower'
    if slot==0x1d:return 'ride_lower_price_FA'
    if slot<=0x22:return 'ride_upper_rule'
    if slot<=0x28:return 'ride_upper_title'
    if slot<=0x2b:return 'ride_lower_shortage_start_F8'
    return 'credits_scroll'

def wrap(s):
    lines=[]
    for raw in s.split('\n'):
        while len(raw)>16:
            cut=raw.rfind(' ',0,17);cut=cut if cut>0 else 16
            lines.append(raw[:cut]);raw=raw[cut:].lstrip(' ')
        lines.append(raw)
    assert ' '.join(s.split())==' '.join(' '.join(lines).split())
    return lines

def draw(lines,face):
    im=Image.new('L',(192,len(lines)*16));d=ImageDraw.Draw(im)
    for y,line in enumerate(lines):
        left=(192-len(line)*12)//2
        for x,c in enumerate(line):d.text((left+12*x,y*16-1),c,font=face,fill=2)
    assert set(im.get_flattened_data())<={0,2}
    tiles={bytes(64)}
    for y in range(0,im.height,8):
        for x in range(0,192,8):
            bits=bytes(im.crop((x,y,x+8,y+8)).get_flattened_data());assert decode(encode(bits))==bits;tiles.add(bits)
    return im,tiles

def F8_values(source):
    mem=bytearray(65536);mem[0x8000:0xc000]=source[0x4010:0x8010];mem[0x600:0x602]=bytes.fromhex('f8 ff')
    results=[]
    for n in range(1000):
        mem[0x7d0:0x7d3]=bytes((n%10,n//10%10,n//100));mem[0x6cd:0x6cf]=(0x600).to_bytes(2,'little');mem[0x6c3]=mem[0x6c4]=0
        cpu=MPU(memory=mem);codes=[]
        for call in range(4):
            cpu.pc=0x937c;cpu.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');steps=0
            while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<10000
            if cpu.a==255:break
            codes.append(cpu.a)
        assert len(codes)==3 and all(x==0 or 0x70<=x<=0x79 for x in codes),(n,codes)
        text=''.join(' ' if x==0 else str(x-0x70) for x in codes)
        assert int(text.strip() or '0')==n,(n,text)
        results.append(text)
    return results

def main():
    records.DATE='2026-10-09'
    out=R/'workspace/review/text11_plan190';out.mkdir(exist_ok=False)
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';baseline=R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes';font=R/'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf'
    assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(font)=='e24256f42e43713d2ea086a1e1669d78b968f5b3cc547e5c157f0606ffa5def1'
    rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')));texts=[r for r in rows if r['translation_ko'] and r['status']=='draft'];assert len(rows)==54 and len(texts)==45
    original=source.read_bytes();rom=baseline.read_bytes();face=ImageFont.truetype(str(font),12);cmap=TTFont(font).getBestCmap()
    prices=[]
    for ride in range(6):
        codes=variable_codes(original,ride);assert len(codes)==2
        assert all(x==0 or 0x70<=x<=0x79 for x in codes)
        prices.append({'ride':ride,'codes':codes,'text':''.join(' ' if x==0 else str(x-0x70) for x in codes)})
    tickets=F8_values(original);plans=[];shared=collections.defaultdict(set);cards=[]
    for r in texts:
        slot=int(r['reference_ids'].split(',')[0],16);group=family(slot);tokens=re.findall(r'\{variable_[A-F0-9]+\}',r['translation_ko']);assert all(t in ('{variable_FA}','{variable_F8}') for t in tokens)
        literal=re.sub(r'\{variable_[A-F0-9]+\}','',r['translation_ko'])
        for c in literal:
            if c.isspace():continue
            assert ord(c) in cmap,(r['entry_id'],c)
            glyph=Image.new('L',(20,20));ImageDraw.Draw(glyph).text((0,-1),c,font=face,fill=2);assert glyph.getbbox(),(r['entry_id'],c)
        aliases=[int(x,16) for x in r['reference_ids'].split(',')];banks=sorted({rom[0x5710+2*x] for x in aliases})
        if group=='credits_scroll':
            plans.append({'entry_id':r['entry_id'],'family':group,'original_text':r['translation_ko'],'aliases':aliases,'current_font_banks':banks,'status':'SEPARATE_SCROLL_PROOF_REQUIRED','source_line_count':len(r['translation_ko'].split('\n')),'why_not_dialogue4line_budget':'NativeFC/FE/FF scroll andFD32 spacing, name/legal rows and residence across three chunks; do not repaginate as ordinary dialogue.'});continue
        variants=[r['translation_ko']]
        if '{variable_FA}' in tokens:
            applicable=prices[5:] if slot==0x1a else prices
            variants=[r['translation_ko'].replace('{variable_FA}',x['text']) for x in applicable]
        elif '{variable_F8}' in tokens:variants=[r['translation_ko'].replace('{variable_F8}',x) for x in tickets]
        fonts=set();line_counts=set();stream_lengths=set();maxsingle=0;sample=None;samplelines=None
        for text in variants:
            lines=wrap(text);im,tiles=draw(lines,face);fonts|=tiles;line_counts.add(len(lines));stream_lengths.add(49*len(lines));maxsingle=max(maxsingle,len(tiles))
            if sample is None:sample=im;samplelines=lines
        for bank in banks:shared[bank]|=fonts
        status='STATIC_PAGE_FONT_FITS128' if len(fonts)<=128 and max(line_counts)<=4 else 'REQUIRES_CAPACITY_OR_LAYOUT_REDESIGN'
        info={'entry_id':r['entry_id'],'family':group,'aliases':aliases,'current_font_banks':banks,'original_text':r['translation_ko'],'sample_lines':samplelines,'variant_count':len(variants),'line_counts':sorted(line_counts),'blank_tail_line_retained':r['translation_ko'].endswith('\n'),'max_single_font_tiles':maxsingle,'all_variable_values_font_union_tiles':len(fonts),'fits_existing128_slot_pair':len(fonts)<=128,'paired_stream_bytes':sorted(stream_lengths),'over4_lines':max(line_counts)>4,'status':status,'actual_UI_clear_geometry_verified11px':group=='opening_verified053','sample_PNG':'page_'+r['entry_id']+'.png'}
        plans.append(info);rgb=Image.new('RGB',sample.size);rgb.putdata([(255,254,255) if x else (0,0,0) for x in sample.get_flattened_data()]);rgb.save(out/info['sample_PNG'])
        cards.append(f'<article><h2>{html.escape(r["entry_id"])} · {group}</h2><p>후보 {min(line_counts)}~{max(line_counts)}행 / 문단 전체 타일 {len(fonts)} / 값 {len(variants)}개. {status}</p><img src="{info["sample_PNG"]}"><pre>{html.escape(chr(10).join(samplelines))}</pre></article>')
    consumer_groups=collections.Counter(z['family'] for z in plans)
    unions=[{'bank':bank,'entries':[z['entry_id'] for z in plans if bank in z['current_font_banks']],'union_tiles':len(tiles),'fits128':len(tiles)<=128,'scope':'All individually centered192px wordwrapped pages union; static demand, not simultaneous lifetime proof'} for bank,tiles in sorted(shared.items())]
    (out/'review.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>전체11px 다음적용 정적계획190</title><style>body{font-family:sans-serif;margin:24px;background:#202027;color:white}article{padding:16px 0;border-top:1px solid #777}img{width:576px;max-width:100%;image-rendering:pixelated}pre{white-space:pre-wrap}</style><h1>11px 다음적용 정적계획190</h1><p>새로 그린 정적 문자 배치 후보이며 실제 게임 화면이 아닙니다. 오프닝053만 실제표시검증이 있습니다. 변수는 기존6502 reader의 값으로 치환해 글리프 수요를 계산했고, 동적 삽입 코드·문단 전환·UI 지우기 구현은 아직 없습니다. 크레딧은 별도 스크롤 설계입니다.</p>'+''.join(cards)+'</html>','utf-8')
    graphics=[]
    for name,need in [('booth_graphics_plan_001.json','Status board labels/digits separate NT command renderer'),('game_hud_plan_001.json','IRQ/fineY geometry, captions/digits andframe extent'),('results_graphics_plan_001.json','Compressed NT commands anddynamic bonus digits'),('gameover_graphics_plan_001.json','Selection states/cursor/redraw andpalette'),('notices_graphics_plan_001.json','Sprite notice dimensions/OAM layout'),('train_sign_graphics_plan_001.json','Baked sign fields/IRQ CHR layout')]:
        p=R/'workspace/translation'/name;d=json.loads(p.read_text('utf-8'));graphics.append({'source':p.relative_to(R).as_posix(),'sha256':sha(p),'label_records':len(d.get('labels',[])),'registered_texts':[z.get('translation_ko') or z.get('draft_ko') or z.get('ko_draft') for z in d.get('labels',[])],'need':need,'11px_implemented':False})
    result={'work':190,'status':'STATIC_11PX_NEXT_CONSUMER_AND_WORKINGSET_PLAN_ONLY','registered_CSV_rows':54,'draft_main_entries':45,'not_global_complete_population':True,'families':dict(consumer_groups),'font_sha256':sha(font),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'baseline051_sha256':sha(baseline),'opening053_sha256':sha(R/'build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes'),'ROM_CSV_unchanged':True,'native_FA_price_pairs':prices,'native_F8_legitimate_three_decimal_digits_CPU_cases':1000,'pages':plans,'shared_font_union':unions,'graphics_consumers':graphics,'next_representative':{'entry_id':'MAIN_05741','native_id':10,'family':'home_booth_lower','text':'자, 어디로 갈까?','reason':'Existing one-line home prompt before dynamic cost/dual card IRQ; paired11px needs native lower22A8 origin and5row clear proof; current bank130 lifetime must be protected','new_ROM_or_runtime_this_work':False},'limits':['42finite dialogue static masks do not prove their UI extents/clear/timing/CHR lifetime','Shared fonts193/196 need consumer-separated residency, not onefont overwrite per paragraph','Native FA6selectors andF8BCD0..999 are a conditional font-demand proof, not runtime11px numeral consumption','Credits3streams require separate scroll/name/legal spacing proof','Graphic catalog and globalpopulation incomplete; explicit six retentions andtitle unchanged','Human final font preference/review pending; currentcandidate used for static planning only']}
    report=R/'qa/reports/text11_190_plan.json';assert not report.exists();report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    overflow=[x for x in unions if not x['fits128']];body=f'''053패키지188·감사189를마친뒤전체텍스트11px의다음출력경로를정리했다. [문단/변수/공유폰트계획](../qa/reports/text11_190_plan.json), [정적배치검토HTML](../workspace/review/text11_plan190/review.html), [053실제비교](../workspace/review/opening11_187/review.html). 정적HTML의42PNG는폰트에서새로만든문자마스크이며실제게임캡처가아니다.

등록54CSV행중45draft본문을분리했다: {json.dumps(dict(consumer_groups),ensure_ascii=False)}. 오프닝9만실제053검증완료. 나머지일반문단은기존어휘와blank tail line을보존해12×16셀/192px/16문자폭으로줄바꿈·2bpp왕복했다. 3크레딧은FC/FE/FF스크롤·FD32빈간격·스태프/법적고지행이별도이므로일반4행모델에대입하지않았다. 글리프누락/빈글리프없음,문구/CSV/ROM수정없음.

원본6502의FA를6course에서실행해2자리요금출력을그대로사용했다. F8을합법적인3자리BCD0..999의1000경우에서실행해leading blank/숫자3칸을보존했다. 변수문자열을문자그대로세거나최대값하나만샘플링하지않고모든해당값의타일합집합을계산했다. 이는정적활성폰트수요검사이며11px실제숫자삽입성공은아니다.

기존동일폰트뱅크의여러문단을합치면128슬롯초과그룹{len(overflow)}건이다: {[(x['bank'],x['union_tiles']) for x in overflow]}. 그러므로상단공유카드193등을문단하나의폰트로교체하면다른문구를잃는다. 소비별전환/동시상단·하단글꼴·지우기수명증명을한뒤bank별재사용또는선택자를설계해야한다. 매표소상태판/HUD/결과/게임오버/공지스프라이트/기차간판은기존그림계획의별도consumer로연결했으며11px구현은미실시다. 등록개수는전체게임분모가아니다. 원문유지6건과타이틀그림은일괄변경하지않는다.

다음대표는홈 MAIN_05741/native0A ‘자, 어디로 갈까?’다. 현재font130,lower22A8와기존5행지우기를대상으로위아래동시출력/문단초기화/대기·지우기/다음선택지의폰트수명을연결한다. 단순문단부터검증한후12홈·매표소/동적요금·티켓/카드/기타출력기로확대한다. 현재후보갈무리11로설계를계속하지만사람의최종미감승인으로간주하지않는다.

정적/CPU계획만수행. 신규ROM/IPS/xdelta/실제Mesen/자동플레이/전체게임/HTML브라우저렌더검증없음. 원본SHA `{sha(source)}`,051SHA `{sha(baseline)}`,053SHA `{result['opening053_sha256']}`,CSV SHA `{result['CSV_sha256']}` 보존. 전체변경파일SHA는 [190매니페스트](../manifests/nonplay190_assets.json). 카페완성작업기/외부게시없음.

재현: `python scripts/plan_text11_190.py`는기존확정출력을덮어쓰지않는다. 새출력경로를설정한복제스크립트에서재현한다. 현재재실행으로기존190을초기화하지않는다.'''
    next_action='홈한줄MAIN_05741의lower22A8/5행지우기·font130 수명을확인하고11px 상하동시출력 대표UI 후보를 만든다.'
    files=[Path(__file__),report,R/'qa/reports/opening11_189_audit.json',R/'scripts/compile_ui_card_group.py',R/'scripts/compile_ui_possession.py',*[p for p in out.iterdir() if p.is_file()],*[R/x['source'] for x in graphics]]
    records.seal(190,'GLOBAL_TEXT11_NEXT_CONSUMER_PLAN_190.md','전체11px 다음출력기·변수·공유폰트 용량계획',body,'45draft를출력경로별로분리.42정적배치/FA6course/F8CPU1000숫자수요/공유font합집합 계산.다음홈한줄PoC;새ROM/실제실행없음.',next_action,files)
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업190','기준051 / 오프닝11px PoC053 / 작업190',1);p.write_text(s,'utf-8')
    p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');s=s.replace('053패키지188과무결성감사189를완료하고전체11px의다음UI를설계한다.','053패키지188·감사189·전체11px출력기계획190을완료했다. [다음UI계획190](GLOBAL_TEXT11_NEXT_CONSUMER_PLAN_190.md)의홈한줄MAIN_05741을다음대표로삼는다.',1);p.write_text(s,'utf-8')
    print(json.dumps({'status':result['status'],'families':result['families'],'shared_font_overflows':[(x['bank'],x['union_tiles']) for x in overflow],'F8_CPU_cases':1000,'next':result['next_representative']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
