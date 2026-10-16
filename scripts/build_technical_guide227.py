"""Create a ROM-free posting kit and offline reader from reviewed guide text."""
from pathlib import Path
import re,html,json
from PIL import Image,ImageDraw,ImageFont
from seal_nonplay171 import R,sha
OUT=R/'workspace/publication/TinyToon12_TechnicalGuide_20261009'
TITLE='타이니툰 어드벤처 1편과 2편으로 배우는 NES 한글화 기술 지침'

def diagram(name,title,sub,items):
    im=Image.new('RGB',(1400,950),'#f3f6fa');d=ImageDraw.Draw(im)
    def font(size):return ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',size)
    d.rectangle((0,0,1400,10),fill='#245d91')
    d.text((55,35),title,font=font(40),fill='#163449')
    d.text((55,105),sub,font=font(24),fill='#536478')
    for i,(label,detail) in enumerate(items):
        y=167+i*145
        d.rounded_rectangle((130,y,1270,y+108),radius=18,fill='white',outline='#b7cadc',width=2)
        d.text((163,y+20),f'{i+1:02}',font=font(35),fill='#245d91')
        d.text((255,y+13),label,font=font(31),fill='#163449')
        d.text((255,y+61),detail,font=font(24),fill='#536478')
        if i<4:
            d.line((700,y+115,700,y+135),fill='#245d91',width=4)
            d.polygon([(689,y+128),(711,y+128),(700,y+141)],fill='#245d91')
    im.save(OUT/'images'/name)

def inline(s):
    s=html.escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2" rel="noreferrer">\1</a>',s)

def main():
    assert not (OUT/'기술_지침.html').exists();(OUT/'images').mkdir()
    diagram('01.png','ROM에서 화면까지 연결하기','설명도 · 실제 게임 캡처가 아닙니다',[
      ('ROM 원본 바이트','원본 해시 · 파일 오프셋 · 보호 구간'),
      ('포인터와 파서','압축 해제 · 제어 토큰 · 호출과 복귀'),
      ('화면 배치','네임테이블 · 스프라이트 · 출력 큐'),
      ('그 시점의 글꼴과 색','실제 CHR 매핑 · 팔레트 · 스캔라인'),
      ('실제 게임 화면','출력 중 · 대기 · 지우기 · 다음 문단')])
    diagram('02.png','앞 문장이 사라질 때까지 글꼴 유지','설계 원칙 설명도 · 실제 전환 조건은 게임별로 확인합니다',[
      ('현재 문단 출력','현재 문자 코드에 맞는 글꼴 사용'),
      ('현재 문단 대기','다음 포인터가 바뀌어도 화면의 글꼴은 유지'),
      ('이전 글자 지우기','지우는 동안 남은 글자가 다른 모양이 되지 않게 확인'),
      ('다음 문단 준비','다음 글꼴과 배치 데이터를 준비'),
      ('다음 글꼴 적용과 새 출력','원래 엔진의 지우기 완료 · 첫 글자 소비 조건에 연결')])
    text=(OUT/'기술_지침.md').read_text('utf-8');lines=text.splitlines()
    assert lines[0]=='# '+TITLE and text.count('```mermaid')==2
    blocks=[];plain=[TITLE,''];toc=[];i=2;head=fig=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            lang=line[3:];i+=1;code=[]
            while i<len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]);i+=1
            assert i<len(lines),'Unclosed fence';i+=1
            if lang=='mermaid':
                fig+=1;caption='ROM에서 화면까지의 경로' if fig==1 else '현재 문단에서 다음 문단까지의 글꼴 수명'
                blocks.append(f'<figure><img src="images/{fig:02}.png" alt="{caption}"><figcaption>설명도 {fig:02} · {caption} · 실제 게임 캡처가 아닙니다.</figcaption></figure>')
                plain.extend([f'[설명도 {fig:02} 삽입: images/{fig:02}.png — {caption}]',''])
            else:
                blocks.append(f'<pre><code class="language-{html.escape(lang)}">{html.escape(chr(10).join(code))}</code></pre>')
                plain.extend(['[코드 예제'+(' — '+lang if lang else '')+']',*code,''])
            continue
        if line.startswith('|'):
            table=[]
            while i<len(lines) and lines[i].startswith('|'):
                table.append([x.strip() for x in lines[i].strip().strip('|').split('|')]);i+=1
            labels=table[0];rows=table[2:];assert len(table)>2 and all(len(r)==len(labels) for r in rows)
            rendered='<table><thead><tr>'+''.join('<th>'+inline(h)+'</th>' for h in labels)+'</tr></thead><tbody>'
            for row in rows:
                rendered+='<tr>'+''.join(f'<td data-label="{html.escape(label,quote=True)}">{inline(cell)}</td>' for label,cell in zip(labels,row))+'</tr>'
                plain.extend([row[0],*['  '+label+': '+cell for label,cell in zip(labels[1:],row[1:])],''])
            blocks.append(rendered+'</tbody></table>');continue
        match=re.match(r'^(#{2,3}) (.*)',line)
        if match:
            level=len(match[1]);label=match[2];head+=1;key=f'section{head}'
            blocks.append(f'<h{level} id="{key}">{inline(label)}</h{level}>')
            if level==2:toc.append(f'<li><a href="#{key}">{inline(label)}</a></li>')
            plain.extend([label,'']);i+=1;continue
        if re.match(r'^(- |\d+\. )',line):
            ordered=bool(re.match(r'^\d+\.',line));tag='ol' if ordered else 'ul';items=[]
            while i<len(lines) and re.match(r'^(- |\d+\. )',lines[i]):
                items.append(re.sub(r'^(- |\d+\. )','',lines[i]));i+=1
            blocks.append(f'<{tag}>'+''.join('<li>'+inline(item)+'</li>' for item in items)+f'</{tag}>')
            plain.extend([('- '+item) for item in items]+['']);continue
        para=[]
        while i<len(lines) and lines[i].strip():
            para.append(lines[i]);i+=1
        blocks.append('<p>'+inline(' '.join(para))+'</p>');plain.extend([' '.join(para),''])
    plain_text='\n'.join(plain)
    plain_text=re.sub(r'`([^`]+)`',r'\1',plain_text)
    plain_text=re.sub(r'\*\*([^*]+)\*\*',r'\1',plain_text)
    plain_text=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'\1 (\2)',plain_text)
    (OUT/'카페_복사용_본문.txt').write_text(plain_text,'utf-8-sig')
    css='''*{box-sizing:border-box}body{margin:0;background:#edf2f7;color:#21364a;font-family:"Malgun Gothic",sans-serif}header{padding:42px 24px;background:#163449;color:white}header div,main{max-width:1000px;margin:auto}h1{font-size:32px;line-height:1.55;word-break:keep-all;margin:10px 0}header p{color:#d4e3ef}main{background:white;padding:26px 32px 70px}h2{font-size:25px;line-height:1.5;margin:46px 0 20px;border-left:5px solid #306da6;padding-left:14px;word-break:keep-all}h3{font-size:21px;margin-top:32px}p,li{font-size:17px;line-height:1.95;overflow-wrap:anywhere}code{font-family:Consolas,monospace;font-size:.91em;overflow-wrap:anywhere}p code,td code{background:#edf2f7;border-radius:3px;padding:1px 3px}pre{padding:19px;background:#152d43;color:#edf5fd;overflow-x:auto;border-radius:6px;max-width:100%;line-height:1.6}pre code{font-size:14px;overflow-wrap:normal}table{width:100%;border-collapse:collapse;font-size:15px;margin:24px 0;table-layout:fixed}td,th{padding:12px;border:1px solid #cbd5df;vertical-align:top;line-height:1.8;overflow-wrap:anywhere}th{background:#edf2f7;text-align:left}figure{margin:30px 0}figure img{width:100%;height:auto;display:block}figcaption{font-size:14px;line-height:1.8;color:#5c6c7d;margin-top:8px}details{padding:14px 20px;background:#f0f5f9}summary{cursor:pointer;font-weight:bold}nav li{font-size:15px}a{color:#2466a1}header a{color:#d4e3ef}@media(max-width:600px){header{padding:28px 18px}h1{font-size:25px}main{padding:20px 18px 50px}h2{font-size:22px}thead{display:none}tbody tr{display:block;margin-bottom:18px;border:1px solid #cbd5df}td{display:block;border:0;border-bottom:1px solid #e5ebf1;padding:10px}td:before{content:attr(data-label);display:block;font-weight:bold;color:#4c6276}pre{padding:14px}}'''
    page=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><style>{css}</style></head><body><header><div><p>NES 한국어화 기술 사례 · 2026.10.09</p><h1>{TITLE}</h1><p>타이틀과 문자열 출력기의 구현부터 오류 재현과 배포까지</p></div></header><main><details><summary>목차 보기</summary><nav><ol>'+''.join(toc)+'</ol></nav></details>'+''.join(blocks)+'</main></body></html>'
    (OUT/'기술_지침.html').write_text(page,'utf-8')
    (OUT/'게시_안내.txt').write_text('''NES 한글화 기술 지침 게시 자료

기술_지침.html: 로컬에서 읽는 검토용. 목차를 펼쳐 원하는 항목으로 이동할 수 있습니다.
기술_지침.md: 표·코드·Mermaid 원천이 포함된 편집용 문서입니다.
카페_복사용_본문.txt: 글쓰기 본문에 복사할 텍스트. 표는 항목별 문장으로 풀었습니다.
images/01.png, 02.png: 본문의 설명도 삽입 표식에 순서대로 올리고 표식 문구는 제거합니다.
examples_nes.py: Python 표준 라이브러리만 쓰는 교육용 코드. ROM을 읽거나 수정하지 않습니다.

일반 본문과 명령 예제를 구분해 편집합니다. HTML 코드를 카페 편집기에 그대로 넣는 용도가 아닙니다.
두 설명도는 실제 게임 화면이 아닙니다. 본문에 없는 추가 게임 검증이나 배포 후 검증 완료를 기재하지 않습니다.
이 자료는 프로젝트 전체 소스 배포가 아니며, 프로젝트 파일 참조를 따라하려면 각 게임의 원본과 등록된 입력을 별도로 준비합니다.
게임 ROM, 폰트 원천, 세이브, 덤프, 비공개 QA 보관본은 이 ZIP에 없습니다.
카페 계정 접속이나 실제 게시를 수행하지 않았습니다.
''','utf-8-sig')
    assert page.count('<figure>')==2 and len(toc)==16 and fig==2
    assert all('\ufffd' not in s for s in (text,page,plain_text))
    (R/'qa/reports/technical227_generation.json').write_text(json.dumps({'work':227,'status':'CREATED_PENDING_RENDER',
      'article':OUT.relative_to(R).as_posix(),'headings':len(toc),'explanatory_figures':2,'game_capture_figures':0,
      'source_sha256':sha(OUT/'기술_지침.md'),'ROM_free':True},ensure_ascii=False,indent=2)+'\n','utf-8')
    print('Created guide HTML, Cafe text, 2 explanatory figures and posting instructions')

if __name__=='__main__':main()
