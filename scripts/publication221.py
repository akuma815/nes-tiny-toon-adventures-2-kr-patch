"""Cafe article, eight evidence-labelled figures, embedded offline reader. No new game run."""
from pathlib import Path
import json,base64,html,re,shutil
from PIL import Image,ImageDraw,ImageFont
from seal_nonplay171 import R,sha

NAME='TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009'
OUT=R/'workspace/publication'/(NAME+'_003')
FONT='C:/Windows/Fonts/malgun.ttf'
BG='#f7f5ed';INK='#152c40';BLUE='#255fa5'
def f(n):return ImageFont.truetype(FONT,n)
def canvas(title,subtitle,height=700):
    im=Image.new('RGB',(1400,height),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1400,12),fill=BLUE)
    d.text((52,33),title,font=f(42),fill=INK)
    d.text((52,93),subtitle,font=f(24),fill='#526273')
    return im,d
def paste(im,source,x,y,box,nearest=True,max_scale=None):
    p=Image.open(source).convert('RGB');scale=min(box[0]/p.width,box[1]/p.height)
    if nearest and scale>=1:scale=max(1,int(scale))
    if max_scale is not None:scale=min(scale,max_scale)
    p=p.resize((int(p.width*scale),int(p.height*scale)),Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
    im.paste(p,(x+(box[0]-p.width)//2,y+(box[1]-p.height)//2))
def pair(title,subtitle,left,right,labels,height=700):
    im,d=canvas(title,subtitle,height)
    for x,p,label in [(60,left,labels[0]),(735,right,labels[1])]:
        d.text((x+25,150),label,font=f(28),fill=INK);paste(im,p,x,205,(605,480))
    return im

def main():
    assert not OUT.exists();(OUT/'images').mkdir(parents=True)
    provenance=[]
    def save(n,im,caption,kind,builds,sources):
        p=OUT/'images'/f'{n:02d}.png';im.save(p)
        provenance.append({'index':n,'image':f'images/{n:02d}.png','caption':caption,'kind':kind,'builds':builds,
            'image_sha256':sha(p),'sources':[{'path':s.relative_to(R).as_posix(),'sha256':sha(s)} for s in sources]})
    comparison=R/'qa/title/title_kr_ai_003_comparison.png'
    # Crop already composed historical screenshots; original pixels untouched.
    source=Image.open(comparison).convert('RGB')
    a=OUT/'original_title_crop.png';b=OUT/'korean_title_crop.png'
    source.crop((128,20,384,260)).save(a);source.crop((648,20,904,260)).save(b)
    save(1,pair('01  타이틀에서 시작한 한글화','실제 과거 캡처 · 원본과 title_kr_ai_003 · v1.0 실행 캡처가 아닙니다',a,b,['일본판 원본','타이틀 한글화 003']),
         '원본과 타이틀003의 실제 캡처 비교. 게임명·부제는 한글로 바꾸고 숫자2·시작 안내·저작권은 유지했습니다.','historical_actual_capture',['original','title_kr_ai_003'],[comparison])
    a.unlink();b.unlink()
    raw=R/'workspace/graphics/title/ai_main_001/main_ai_raw.png'
    original=R/'extracted/title/title_20261004_001/main_original.png'
    converted=R/'build/title_kr_ai_003/main_nes.png'
    im,d=canvas('02  PNG → 생성형 이미지 → NES 타일','제작 원천과 변환 결과 · 실제 게임 화면이 아닌 작업 설명 자료',620)
    for x,p,t in [(35,original,'원본 PNG 추출'),(485,raw,'AI 생성 원천'),(935,converted,'NES 4색·타일 변환')]:
        d.text((x+20,175),t,font=f(27),fill=INK);paste(im,p,x,230,(425,280),nearest=p!=raw)
    d.text((52,550),'생성 결과를 그대로 넣지 않고 픽셀·팔레트·타일·압축 공간에 맞춰 변환했습니다.',font=f(26),fill=INK)
    save(2,im,'원본 추출 PNG, 생성형 이미지 원천, NES 변환 이미지. 작은 글자와 리본은 별도로 교정했습니다.','production_sources',['title_kr_ai_003'],[original,raw,converted])
    left=R/'qa/dialogue/issue177_exchange_049/frame_01710.png';right=R/'qa/dialogue/issue177_exchange_050/frame_01710.png'
    save(3,pair('03  티켓 교환 뒤 대사 깨짐 수정','실제 과거 캡처 · 049 → 050 · 초기 재화 seed를 사용한 재현 검사',left,right,['교환 뒤 글꼴 충돌 049','하단 대사 글꼴 유지 050']),
         '같은 티켓교환 장면의049/050 실제 캡처. 숫자 갱신이 하단 대사의 글꼴을 바꾸는 충돌을 수정했습니다. 초기 재화 seed를 사용했습니다.','historical_actual_capture',['049','050'],[left,right])
    left=R/'qa/dialogue/hud180_coaster_source/frame_03000.png';right=R/'qa/dialogue/hud180_coaster_050/frame_03000.png'
    save(4,pair('04  HUD 빈 여백은 원본과 비교','실제 과거 캡처 · 왼쪽8픽셀 띠와 아래 검은 여백은 원본에도 존재',left,right,['일본판 원본','한글판 050']),
         '동일 입력의 원본/050 롤러코스터 캡처. 큰 여백은 원래 구성이고, 한글 HUD의 기존2픽셀 아래 이동은 별도 변경입니다.','historical_actual_capture',['original','050'],[left,right])
    left=R/'qa/dialogue/moving_stop181_050/frame_04200.png';right=R/'qa/dialogue/moving_stop182_051/frame_04200.png'
    save(5,pair('05  움직이는 STOP도 별도 수정','실제 과거 캡처 · 고정 표지판과 다른 스프라이트 타일을 사용한 경우',left,right,['움직이는 STOP 050','움직이는 정지 051']),
         '움직이는 표지판050/051의 실제 캡처. 고정 정지 표지판과 다른 타일을 찾아 글자 영역만 바꿨습니다.','historical_actual_capture',['050','051'],[left,right])
    old=R/'workspace/review/opening11_194/page06_8px.png';new=R/'workspace/review/opening11_194/page06_11px.png'
    im=pair('06  일반 텍스트를11px로 확대','과거 실제 오프닝 캡처 · 각 문단 완성 시점 비교 · 동일 프레임 비교는 아닙니다',old,new,['기존8px','오프닝055의11px'])
    save(6,im,'오프닝6문단의 기존8px/05511px 실제 캡처. 완성시점이 서로 다르며055 오프닝 성공을062 전체 실행검수로 간주하지 않습니다.','historical_actual_capture',['existing_8px','opening055'],[old,new])
    sources=[R/'workspace/review/text11_211'/f'{key}.png' for key in ('MAIN_05939','MAIN_05999','MAIN_059E7')]
    im,d=canvas('07  크레딧까지 이어지는 글꼴 확대','062의 세 크레딧 문단 정적 복원 · 이름·KONAMI·권리 문구는 유지',730)
    for x,p,t in zip((26,484,942),sources,('크레딧 1','크레딧 2','크레딧 3')):
        d.text((x+22,156),t,font=f(28),fill=INK);paste(im,p,x,210,(432,470))
    save(7,im,'062에서 디코딩한 크레딧3문단. 한글과 이름 그림을 확대했으며 실제 크레딧 실행 캡처는 아닙니다.','static_ROM_decode',['062_static'],sources)
    im,d=canvas('08  검증 결과는 범위를 나누어 기록','v1.0 데이터는062와 동일 · CPU 모델과 실제 플레이 검수는 별개',700)
    data=[('독립 재빌드·전체 결과','원본 ExpectedWrites / ROM·IPS 동일','통과'),
          ('Windows 패치 적용','8개 사례 + 최종 ZIP 추출본 실제 적용','통과'),
          ('텍스트·인터럽트 CPU','등록 문단 검사 / 한정 IRQ212,764회','한정 범위 통과'),
          ('062 실제 화면·완주','가독성·소거·화면전환·실제매핑 / 사용자 담당','결과 미기록')]
    for i,(t,sub,status) in enumerate(data):
        y=165+i*120;d.rounded_rectangle((50,y,1350,y+102),radius=14,fill='#ffffff',outline='#c6d0dc',width=2)
        d.text((76,y+13),t,font=f(28),fill=INK);d.text((76,y+56),sub,font=f(24),fill='#536071')
        d.text((1010,y+32),status,font=f(27),fill=BLUE if i<3 else '#a75d16')
    proof=R/'qa/reports/release220_verified.json'
    save(8,im,'빌드·Windows적용은 통과했습니다. CPU/NMI/IRQ는 명명한 모델 조건에 한정하고062 실제 화면·완주 결과는 미기록으로 남겼습니다.','explanatory_validation_summary',['v1.0_exact062'],[proof,R/'qa/reports/irq217_injection.json',R/'qa/reports/irq218_opening_credits.json'])
    sections=[
    ('1. 타이틀 한 장에서 출발했습니다',[
     '1편에서 사용했던 PNG 추출 → 생성형 이미지 → 게임 타일 재삽입 흐름을2편에서도 이어갔습니다. 타이틀에는 ‘타이니 툰 어드벤처’와 ‘몬타나랜드에 어서 오세요’를 넣었습니다. 숫자2, PUSH START, 저작권 문구와 리본 바깥 모양은 유지했습니다.',
     '2편은 화면 중간에 글자 그림과 화면 배치를 바꿉니다. 프레임 끝에서 보이는 타일만 확인하면 실제 로고를 놓칠 수 있었습니다. 그래서 데이터를 찾는 일과 화면에서 쓰이는 경로를 연결하는 일을 함께 진행했습니다.'],[1]),
    ('2. AI 그림을 NES에 맞게 다시 만들었습니다',[
     '생성형 이미지가 완성된 뒤에도 바로 ROM에 넣을 수는 없었습니다. 원래 로고 공간과4색 팔레트에 맞춰 줄이고, 같은8×8 타일을 묶고, 화면 배치 데이터를 다시 압축했습니다. 리본 문구와 작은 보조 글자는 별도로 손봤습니다.',
     '작은 글자를 여러 번 축소하면 획이 사라지는 문제가 있었고, 리본의 실제 화면 위치도 정적 합성과 차이가 있었습니다. 이 과정을 거쳐 타이틀003을 채택했습니다. 아래 비교는 당시 실제 실행 기록입니다.'],[2]),
    ('3. 대사와 화면 속 그림을 함께 한글화했습니다',[
     '타이틀 다음으로 오프닝, 홈과 놀이기구 선택, 매표소, 놀이기구 이름·설명·요금·티켓 안내, 성 입구, 크레딧을 작업했습니다. 지도와 매표소 간판, 결과 화면, HUD, 정지 표지판 같은 그림 글자도 따로 처리했습니다.',
     '여기서45는 등록된 문단 수(오프닝9·일반33·크레딧3)입니다. 전게임 텍스트의 발견률이나100% 완료율을 뜻하지 않습니다. HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT는 이번 범위에서 원문을 유지하기로 했습니다. 타이틀의 시작 안내와 저작권 등 보호 대상도 그대로입니다.'],[]),
    ('4. 티켓 교환 뒤 깨진 대사를 고쳤습니다',[
     '티켓 교환 전까지 읽히던 대사가 교환 뒤 깨지는 문제가 제보됐습니다. 문장 자체보다 글자 그림의 선택 상태가 원인이었습니다. 숫자를 갱신하는 경로가 하단 대사에 필요한 글꼴을 다른 글꼴로 바꾸고 있었습니다.',
     '매표소의 숫자 갱신에서도 하단 대사 글꼴을 유지하도록050에서 수정했습니다. 초기 재화를 넣어 같은 교환 경로를 재현한 실제 캡처와 CPU 상태를 비교했습니다. 이 수정은 이후051과062에도 이어집니다.'],[3]),
    ('5. HUD 여백과 움직이는 표지판을 다시 확인했습니다',[
     '상태창 왼쪽과 아래가 비어 보인다는 제보는 원본과 같은 입력으로 비교했습니다. 왼쪽8픽셀의 배경색 띠와 아래 검은 여백은 원본에도 있었습니다. 한글 HUD를 위해 내용이2픽셀 아래로 이동한 기존 변경은 별도로 기록했습니다. 원본과 완전히 같은 배치라고 설명하지 않았습니다.',
     '정지 표지판도 고정형만 바꾸면 끝나는 일이 아니었습니다. 몇 개를 지나고 나오는 위아래 움직이는 표지판이 다른 스프라이트 타일을 사용했습니다. 그 실제 타일을 찾아051에서 STOP을 ‘정지’로 바꾸고 테두리와 기둥은 보존했습니다.'],[4,5]),
    ('6. 대사 글꼴을11px로 키웠습니다',[
     '작은 HUD와 정지 표지판은 원래 공간이 좁아 기존 크기를 유지했습니다. 그 외 등록 문단은 Galmuri11을 사용해 확대했습니다. 최대 한글 획높이11px를12px 폭·16px 높이 셀에 넣고 두 타일 행으로 출력하는 방식입니다. 숫자는 기존8px 타일 간격이라 모든 문자 획이11px인 것은 아닙니다.',
     '오프닝을 먼저 시험한 뒤 줄바꿈을 조정했습니다. 6문단의 ‘깜짝 놀랄 거다!’는 아래 한 줄로 묶고 ‘의문의 대부호로부터’는 오른쪽에 맞췄습니다. 이후 일반 대사와 크레딧까지 확대했고, 이름과 설명이 동시에 나오는 놀이기구 창은 같은 글꼴을 공유하도록 배치했습니다.',
     '크레딧의 이름·KONAMI·권리 문자열은 유지했습니다. 다만 글자 그림은 확대했고 영문은16px 간격을 사용합니다. 아래 오프닝 비교는 기존8px/05511px의 과거 실제 캡처, 크레딧은062 ROM의 정적 복원입니다. 055의 오프닝 확인을062 전체 실행 성공으로 옮기지 않았습니다.'],[6,7]),
    ('7. 검증을 통과한 항목과 남겨 둔 항목',[
     'v1.0 배포 데이터는062와 같습니다. 새 출력 경로에서 다시 빌드하고, 원본에서 계획한 쓰기 범위를 재적용해 전체 ROM과 비교했습니다. 기존 파일을 덮어쓰는 대신 새 빌드와 보고서를 남겼습니다.',
     '패치 적용은 실제 Windows에서 정상 입력과 오류 입력8개 사례를 확인했습니다. 최종 ZIP을 다시 풀어 한글·공백 경로에서 apply.cmd를 실행했고, 결과 ROM이 배포 빌드와 완전히 같았습니다.',
     '한정 CPU 검사에서는 텍스트 출력·변수·건너뛰기와 큐·은행 복귀를 확인했습니다. NMI 전송 조사에서는 처음에 옛 fallback을 직접 불러 잘못 판단했던 결과를 철회하고 현재 진입점으로 다시 측정했습니다. 올바른 경로의 모델 검사에는 초과가 없었지만 명목상 여유가 작아 하드웨어 안전성을 확정하지 않았습니다. IRQ는 일반대사·오프닝·크레딧에 총212,764회 한정 주입했습니다.',
     '062 실제 화면·전체 플레이 검수 결과는 현재 작업 기록에 없습니다. 그 검수는 사용자가 담당합니다. 가독성, 소거와 화면 전환, 실제 글꼴 매핑과 크레딧 스크롤은 직접 확인할 항목으로 남겼습니다. 이전003/050/051 캡처를 이번 v1.0의 완주 증거로 취급하지 않았습니다.'],[8]),
    ('8. 배포 파일과 적용 방법',[
     '첨부 배포 파일은 TinyToonAdventures2_KR_v1.0_20261009.zip입니다. 게임 ROM은 포함하지 않았습니다. 일본판 Tiny Toon Adventures2 - Montana Land e Youkoso의 깨끗한 원본 .nes 파일을 준비하고, ZIP을 모두 푼 뒤 원본을 apply.cmd에 끌어 놓으면 원본이름_KR.nes가 생성됩니다. 원본이나 기존 출력은 덮어쓰지 않습니다.',
     '원본은262,160바이트, 결과는524,304바이트입니다. 원본 SHA-256은 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d, 결과는7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce입니다. 적용 도구가 크기와 해시를 검사하므로 이전 한글판에 덧씌우지 말고 일본판 원본에서 시작하세요.',
     '새 ROM을 열고 초기화해 검수해 주세요. 이전 버전 세이브스테이트 호환은 확인되지 않았습니다. 오류를 발견하면 사용 ROM 해시, 에뮬레이터 버전, 직전 행동과 장면 이미지를 함께 기록해 두면 같은 경로를 좁히는 데 도움이 됩니다.',
     '이번 글꼴은 Galmuri7/Galmuri11, 적용 도구는 xdelta3를 사용했습니다. 해당 출처·라이선스는 배포 ZIP에 함께 넣었습니다. 원작과 캐릭터의 권리는 각 권리자에게 있습니다.'],[])]
    title='타이니툰 어드벤처2 한글패치 v1.0 배포와 작업기'
    lead='타이틀 PNG 작업에서 티켓 교환 오류와 움직이는 표지판 수정,11px 대사 확대까지의 기록입니다. v1.0은062와 같은 데이터이며 빌드·적용 검증을 마쳤습니다. 실제062 화면·완주 검수 결과는 아직 기록되지 않았습니다.'
    byid={x['index']:x for x in provenance};plain=[title,'',lead,''];markdown=[f'# {title}','',lead,''];blocks=[]
    for title2,paragraphs,indices in sections:
        plain+=[title2,'',*sum(([p,''] for p in paragraphs),[])];markdown+=[f'## {title2}','',*sum(([p,''] for p in paragraphs),[])]
        block=f'<section><h2>{html.escape(title2)}</h2>'+''.join(f'<p>{html.escape(p)}</p>' for p in paragraphs)
        for i in indices:
            item=byid[i];plain+=[f'[이미지 {i:02d} 삽입: {item["caption"]}]',''];markdown+=[f'![{item["caption"]}]({item["image"]})','']
            encoded=base64.b64encode((OUT/item['image']).read_bytes()).decode()
            block+=f'<figure><button class="zoom" aria-label="이미지{i:02d} 확대"><img src="data:image/png;base64,{encoded}" alt="{html.escape(item["caption"],quote=True)}"></button><figcaption>{html.escape(item["caption"])}</figcaption></figure>'
        blocks.append(block+'</section>')
    (OUT/'카페_복사용_본문.txt').write_text('\n'.join(plain),'utf-8-sig')
    (OUT/'작업기.md').write_text('\n'.join(markdown),'utf-8')
    css='''*{box-sizing:border-box}body{margin:0;background:#eef1f4;color:#203448;font-family:"Malgun Gothic",sans-serif}header{background:#162f48;color:white;padding:48px 24px}header div,main{max-width:960px;margin:auto}h1{font-size:32px;line-height:1.4;margin:12px 0}header p{line-height:1.8;color:#dce5ed}main{padding:32px 24px 64px;background:white}h2{font-size:25px;margin-top:44px;border-left:5px solid #316da6;padding-left:14px;line-height:1.5}p{font-size:17px;line-height:1.9;overflow-wrap:anywhere}figure{margin:26px 0 38px}.zoom{background:transparent;border:0;padding:0;width:100%;cursor:zoom-in}figure img{width:100%;height:auto;display:block}figcaption{font-size:14px;color:#536478;line-height:1.7;margin-top:10px}dialog{width:96vw;max-width:1500px;padding:10px;border:0;border-radius:8px}dialog::backdrop{background:#000c}dialog img{width:100%;height:auto}dialog button{font:inherit;padding:8px 16px;margin-bottom:10px}.tag{letter-spacing:2px;font-size:13px}@media(max-width:600px){header{padding:30px 20px}h1{font-size:26px}main{padding:18px 18px 40px}h2{font-size:22px}p{font-size:17px}}'''
    js='''const dialog=document.querySelector('dialog');document.querySelectorAll('.zoom').forEach(b=>b.addEventListener('click',()=>{dialog.querySelector('img').src=b.querySelector('img').src;dialog.showModal()}));dialog.querySelector('button').onclick=()=>dialog.close();dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});'''
    page=f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{css}</style><header><div><span class="tag">TINY TOON ADVENTURES 2 · 2026.10.09</span><h1>{title}</h1><p>{lead}</p></div></header><main>'+''.join(blocks)+f'</main><dialog><button>닫기</button><img alt="확대 자료"></dialog><script>{js}</script></html>'
    (OUT/'작업기.html').write_text(page,'utf-8')
    (OUT/'업로드_안내.txt').write_text(f'''네이버 카페 업로드 안내

제목: {title}
1. 카페_복사용_본문.txt의 내용을 게시글 본문에 붙여 넣습니다.
2. 이미지01~08 삽입 표시 위치에 images/01.png~08.png를 순서대로 업로드합니다.
3. 삽입 표시 문구는 제거하고 각 이미지 설명은 캡션으로 남깁니다.
4. 배포 첨부: TinyToonAdventures2_KR_v1.0_20261009.zip
5. 작업기 보관 첨부가 필요하면 {NAME}.zip도 함께 올립니다.

작업기.html은 인터넷 연결 없이 로컬에서 읽고 이미지를 확대하는 검토용입니다.
HTML 코드를 카페 편집기에 그대로 붙여 넣는 방식은 사용하지 않습니다.
이미지01/03/04/05/06은 이전 빌드의 실제 캡처,02는 제작 원천,07은 정적 복원,08은 설명 표입니다.
이전 캡처를 이번 v1.0 실행 캡처나 완주 결과로 설명하지 않습니다.
본문의 실제062 화면·플레이 검수 미기록 안내와 원문 유지 범위를 함께 게시합니다.
이미지07은 크레딧 내용입니다. 엔딩 관련 공개 범위는 카페 관례에 맞춰 접거나 표시할 수 있습니다.
게임 ROM·세이브·비공개 QA 보관본은 업로드 대상이 아닙니다.
이 자료 제작 과정에서는 카페 계정 접속이나 게시를 수행하지 않았습니다.
''','utf-8-sig')
    public=[{k:v for k,v in z.items() if k!='sources'} for z in provenance]
    (OUT/'이미지_출처_구분.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n','utf-8')
    evidence=R/'qa/reports/publication221_sources.json'
    evidence.write_text(json.dumps({'work':221,'article':OUT.relative_to(R).as_posix(),'new_game_execution':False,'figures':provenance},ensure_ascii=False,indent=2)+'\n','utf-8')
    assert len(re.findall(r'\[이미지 \d{2} 삽입:',(OUT/'카페_복사용_본문.txt').read_text('utf-8-sig')))==8
    assert page.count('<figure>')==8 and '\ufffd' not in page
    print(json.dumps({'status':'CREATED_PENDING_RENDER','files':len(list(OUT.rglob('*'))),'figures':8,'folder':OUT.relative_to(R).as_posix()},ensure_ascii=False))

if __name__=='__main__':main()
