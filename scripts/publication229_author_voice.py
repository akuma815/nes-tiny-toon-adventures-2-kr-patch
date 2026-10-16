"""Apply the author's supplied Cafe voice to the worklog; no game changes."""
import base64, html, json, re, shutil
from seal_nonplay171 import R, sha
from publication221 import canvas, f, INK, BLUE

NAME='TinyToon2_KR_Worklog_AuthorVoice_20261009'
OUT=R/'workspace/publication'/NAME
OLD=R/'workspace/publication/TinyToon2_KR_Worklog_Reader_20261009'
TITLE='타이니툰 어드벤처 2 한국어화 작업기'
INTRO=[
 '안녕하세요. 1편에 이어 2편도 한국어화 작업을 마쳐 공개합니다.',
 '1편과 달리 2편은 놀이공원 미니게임 모음입니다. 짧은 플레이타임을 보완하려는 건지 개별 미니게임의 난이도가 꽤 높은 편이네요. 당시에는 티켓을 모아야 한다는 개념을 몰라서, 아무 의미 없이 계속 미니게임만 하다가 질려서 그만뒀던 기억이 있습니다. ㅠㅠ',
 '이번에는 한국어화하면서 드디어 엔딩까지 보게 됐습니다. 작업 덕분에 어릴 때 끝내지 못했던 게임을 마무리하게 된 감사한 케이스라고 할 수 있겠네요. ㅎㅎ',
 '1편에서 해봤던 방법을 이어가면 되겠다고 생각했는데, 막상 시작하니 2편에서도 새로 확인할 게 많았습니다. 타이틀부터 대사, 글꼴 확대까지 어떤 과정을 거쳤는지 남겨보려고 합니다. 나중에 다른 게임을 한국어화하실 분들께도 조금이나마 도움이 됐으면 좋겠습니다.']

SECTIONS=[
('1. 이번에도 타이틀부터 시작했습니다',[
 '1편처럼 타이틀을 PNG로 추출하고, 생성형 이미지로 한글 로고를 만든 뒤 게임에 다시 넣는 방식으로 시작했습니다. 게임명은 ‘타이니 툰 어드벤처’, 부제는 ‘몬타나랜드에 어서 오세요’로 바꿨습니다. 숫자 2와 PUSH START, 저작권 문구는 그대로 뒀고요.',
 '처음엔 화면에 보이는 타일만 찾으면 될 줄 알았습니다. 그런데 2편은 화면을 그리는 중간에 글자 그림과 배치를 바꾸더라고요. 프레임 끝의 메모리만 보면 실제 로고에 쓰인 데이터를 놓칠 수 있어서, ROM에서 찾은 그림이 어느 순간에 화면으로 나오는지까지 따라가야 했습니다.'],[1]),
('2. AI로 만든 그림도 손볼 곳이 많았습니다',[
 '생성형 이미지는 한글 로고의 모양을 잡는 데 도움이 됐습니다. 다만 만들어진 그림을 그대로 게임에 넣을 수는 없었습니다. 원래 로고 공간과 4색 팔레트에 맞춰 픽셀을 정리하고, 8×8 타일로 나눈 뒤 같은 타일을 묶었습니다. 화면 배치도 다시 만들고 압축 공간에 맞춰 넣어야 했고요.',
 '큰 그림에서는 괜찮아 보이던 글자도 줄이면 획이 없어지는 경우가 있었습니다. 리본 문구는 정적으로 합쳐 본 위치와 실제 게임에서 나오는 위치가 달랐고요. 그래서 리본과 작은 보조 글자는 따로 교정했습니다. 이미지 한 장 만들면 끝날 줄 알았는데, 게임 안에서 읽히게 만드는 작업이 또 남아 있었네요. ㅎㅎ',
 '다시 만들 때는 이미지를 새로 생성하지 않고, 최종적으로 채택한 PNG를 같은 입력으로 사용하도록 했습니다. 생성 결과가 매번 같지는 않으니 이 부분은 고정해 두는 게 좋겠더라고요.'],[2]),
('3. 대사는 번역문만 바꾸면 되는 게 아니었습니다',[
 '대사는 일본어 문장을 한글로 바꾸는 것 외에도 손볼 게 많았습니다. 문자 코드, 글자 그림, 포인터와 제어코드, 화면에 한 글자씩 보내는 출력기가 서로 연결돼 있었습니다. 문단마다 필요한 한글 글꼴을 준비하면서, 원래 게임의 대기·지우기·분기 동작도 같이 유지해야 했습니다.',
 '오프닝, 홈과 놀이기구 선택, 매표소, 놀이기구 안내, 성 입구와 크레딧을 작업했습니다. 지도와 간판, 결과 화면, HUD, 정지 표지판처럼 그림으로 들어 있는 글자는 따로 바꿨습니다. 등록해서 작업한 대상은 오프닝 9문단, 일반 대사 33문단, 크레딧 3문단입니다. 숨은 문자열까지 전부 찾았다는 뜻은 아니고, 확인해서 작업한 범위라고 봐주시면 됩니다.',
 'HOWTO·PAUSE·POW와 서명 모양, 사용 경로가 확정되지 않은 배경 데이터, 진단용 STAGE SELECT는 이번에는 원문을 유지하기로 했습니다. 어디에서 쓰이는지 확실하지 않은 그림까지 바꾸기보다는, 확인한 표시 경로와 남겨 둔 범위를 기록해 뒀습니다.'],[]),
('4. 티켓을 바꾸고 나니 대사가 깨졌습니다',[
 '플레이하면서 보니 티켓을 교환하기 전에는 멀쩡하던 대사가, 교환 후에 깨지는 문제가 있었습니다. 처음엔 문장 데이터 쪽 문제인가 싶었는데, 원인은 글꼴이었습니다. 숫자를 갱신하는 과정에서 하단 대사에 필요한 글꼴을 다른 글꼴로 바꾸고 있더라고요.',
 '숫자가 바뀌어도 대사의 글꼴은 유지하도록 수정했습니다. 초기 재화를 설정해 같은 교환 경로를 재현하고, 수정 전·후 화면과 CPU 상태를 비교했습니다. 글자가 처음 잘 나오는지만 볼 게 아니라, 숫자가 바뀌거나 다음 대사를 기다리는 동안에도 유지되는지 확인해야 한다는 걸 다시 배웠네요.'],[3]),
('5. HUD 여백과 움직이는 STOP도 확인했습니다',[
 '놀이기구를 타다 보니 상태창 왼쪽과 아래가 비어 보여서, 이것도 패치하면서 생긴 문제인지 확인했습니다. 원본과 같은 입력으로 비교해 보니 왼쪽 8픽셀의 배경색 띠와 아래 검은 여백은 일본판에도 있었습니다. 한글 HUD 내용이 2픽셀 아래로 이동한 변경은 따로 구분했고요. 원래 이런 화면이었구나 싶었습니다.',
 '정지 표지판은 고정된 것부터 바꿨는데, 몇 개 지나고 나오는 위아래 움직이는 표지판에는 STOP이 남아 있었습니다. 비슷하게 생겼어도 다른 스프라이트 타일을 쓰고 있더라고요. 움직이는 표지판의 실제 타일을 찾아 글자만 ‘정지’로 바꾸고 테두리와 기둥은 그대로 뒀습니다.',
 '같은 글자가 한 곳에서 번역됐다고 다른 곳도 다 끝난 건 아니었습니다. 그림 글자는 이렇게 같은 모양의 다른 표시 경로가 있는지까지 확인해야 하네요.'],[4,5]),
('6. 작은 대사 글꼴도 조금 키워봤습니다',[
 '작업하다 보니 대사 글자가 작아서, 좀 더 크게 읽을 수 있으면 좋겠다는 생각이 들었습니다. HUD와 정지 표지판은 원래 그림의 공간이 좁아 기존 크기를 유지하고, 그 외 등록 문단은 Galmuri11로 확대했습니다.',
 '한글은 최대 획높이 11px를 폭 12px·높이 16px 셀에 넣고, 두 타일 행으로 출력했습니다. 숫자는 기존 8px 간격을 사용해서 모든 문자가 똑같은 높이로 커지는 방식은 아닙니다. 글꼴 파일만 바꾸면 되는 일이 아니라, 글자를 배치하고 화면에 보내는 방식도 같이 손봐야 했습니다.',
 '오프닝부터 시험하면서 줄바꿈을 맞췄습니다. 여섯 번째 문단의 ‘깜짝 놀랄 거다!’는 아래 한 줄로 묶고, ‘의문의 대부호로부터’는 오른쪽에 맞췄습니다. 글자가 커지니 문장이 차지하는 폭도 달라져서, 빈줄과 문장 배치를 같이 조정하게 되더라고요.',
 '일반 대사와 크레딧으로 넓혀 갈 때는 한 화면에 필요한 글꼴이 다 들어가는지도 확인했습니다. 놀이기구 이름과 설명은 글꼴을 공유하도록 배치했습니다. 크레딧의 이름·KONAMI·권리 문자열은 유지하면서 글자 그림을 확대했고, 영문 이름은 16px 간격으로 넣었습니다.',
 '아래 오프닝 비교는 글꼴 확대를 시험할 때 찍은 실제 화면입니다. 각 문단이 완성된 시점은 서로 다릅니다. 크레딧 그림은 배포 데이터에서 정적으로 복원한 자료라서, 실제 실행 캡처와는 구분해서 봐주시면 됩니다.'],[6,7]),
('7. 플레이 확인과 패치 적용도 마무리했습니다',[
 '작업 파일이 잘 만들어지는 것과 배포한 패치가 잘 적용되는 것은 따로 확인했습니다. 깨끗한 원본에서 다시 빌드하고, 계획한 쓰기 범위를 재적용해 최종 ROM 전체와 비교했습니다. 차분 패치로 만든 결과도 같은 바이트인지 확인했고요.',
 '적용 도구는 Windows에서 정상 입력과 오류 입력을 포함한 8개 사례를 확인했습니다. 마지막에는 배포 ZIP을 다시 풀어 한글·공백이 들어간 경로에서 apply.cmd를 실행했습니다. 여기서 만들어진 ROM도 배포 결과와 같았습니다.',
 '텍스트 출력과 변수, 건너뛰기, 은행 복귀와 인터럽트는 한정된 CPU 모델 조건에서 검사했습니다. 조사 중에는 옛 출력 경로를 직접 호출해서 잘못 판단했던 측정도 있었습니다. 그 결과는 철회하고 실제 진입점에서 다시 확인했습니다. 모델 검사에서 확인한 조건과 실제 플레이로 확인한 부분은 구분해 뒀습니다.',
 '실제 화면을 보면서 플레이했고, 완주까지 포함한 1차 검수는 마쳤습니다. 덕분에 이번에는 엔딩도 보게 됐네요. ㅎㅎ 배포 이후에도 제보를 받아 추가로 확인할 예정입니다. 아래 비교 이미지들은 각 수정 과정을 남긴 자료이고, 완주 전체를 촬영한 기록은 아닙니다.'],[8]),
('8. 적용 방법과 작업을 마치며',[
 '배포 파일은 TinyToonAdventures2_KR_v1.0_Release_20261009.zip입니다. 게임 ROM은 들어 있지 않습니다. 일본판 Tiny Toon Adventures 2 - Montana Land e Youkoso의 깨끗한 원본 .nes 파일을 준비해 주세요. ZIP을 모두 푼 뒤 원본을 apply.cmd에 끌어 놓으면 원본이름_KR.nes가 만들어집니다. 원본과 기존 출력 파일은 덮어쓰지 않도록 했습니다.',
 '원본은 262,160바이트, 결과는 524,304바이트입니다. 적용 도구가 크기와 SHA-256을 검사하니 이전 한글판에 덧씌우지 말고 일본판 원본에서 시작해 주세요. 원본과 결과의 전체 해시는 배포 파일의 안내에 함께 넣었습니다.',
 '이전 세이브스테이트의 호환은 확인하지 못했습니다. 수정된 ROM을 확인하실 때는 새로 열고 초기화한 뒤 진행해 주세요. 이상한 장면을 발견하시면 사용 ROM 해시, 에뮬레이터 버전, 직전에 한 행동과 화면 이미지를 같이 남겨주시면 확인하는 데 도움이 됩니다.',
 '이번 작업에는 Galmuri7/Galmuri11과 xdelta3를 사용했고, 출처와 라이선스는 배포 ZIP에 넣었습니다. 원작과 캐릭터의 권리는 각 권리자에게 있습니다.',
 '1편에서 해봤으니 2편은 좀 더 수월하지 않을까 했는데, 이번에도 게임 안에서 그림과 글자가 실제로 어떻게 나오는지 확인하는 일이 많이 남아 있었습니다. 그래도 예전에 중간에 그만뒀던 게임을 한국어로 읽고 엔딩까지 볼 수 있게 돼서 개인적으로는 의미 있는 작업이었네요.',
 '나중에 다른 게임을 한국어화하실 분들께는 번역문뿐 아니라, 어떤 그림을 썼는지와 어떻게 다시 만들 수 있는지, 어디까지 확인했는지도 같이 남겨두시라고 말씀드리고 싶습니다. 이번 기록이 작은 참고가 됐으면 좋겠습니다. 재미있게 즐겨주세요. :)'],[])]

CAPTIONS=[
 '원본과 한글화 타이틀의 실제 캡처입니다. 게임명과 부제를 바꾸고 숫자 2·시작 안내·저작권은 그대로 뒀습니다.',
 '원본 PNG, AI로 만든 원천 이미지, NES 변환 결과입니다. 리본 문구와 작은 글자는 따로 교정했습니다.',
 '같은 티켓 교환 경로의 수정 전·후 실제 캡처입니다. 숫자 갱신 때문에 대사 글꼴이 바뀌던 문제를 수정했습니다.',
 '같은 입력으로 비교한 일본판과 한글판의 실제 화면입니다. 큰 여백은 원본에도 있고, 한글 HUD의 2픽셀 아래 이동은 별도 변경입니다.',
 '움직이는 표지판의 수정 전·후 실제 캡처입니다. 글자만 바꾸고 테두리와 기둥은 그대로 뒀습니다.',
 '오프닝 여섯 번째 문단의 글꼴 확대 전·후 실제 캡처입니다. 같은 프레임을 비교한 것은 아닙니다.',
 '크레딧 세 문단을 정적으로 복원한 자료입니다. 이름과 권리 문자열을 유지하면서 글자 그림을 확대했습니다.',
 '재빌드·Windows 적용과 한정 CPU 검사는 통과했습니다. 실제 화면·완주 1차 검수를 마쳤고, 배포 이후에도 추가로 확인할 예정입니다.']

def prose(value):
    escaped=html.escape(value)
    for expression in ('ㅠㅠ','ㅎㅎ',':)'):
        escaped=escaped.replace(expression,'<span class="emotion">'+expression+'</span>')
    return escaped

def main():
    if OUT.exists():assert not (OUT/'SHA256.txt').exists(),'Sealed article must not be rewritten'
    else:shutil.copytree(OLD,OUT,ignore=shutil.ignore_patterns('SHA256.txt'))
    provenance=json.loads((R/'qa/reports/publication228_sources.json').read_text('utf-8'))
    provenance.update(work=229,article=OUT.relative_to(R).as_posix(),voice_basis='User-supplied first-person Cafe introduction',first_playthrough_evidence='User report; no new playthrough by assistant')
    im,d=canvas('08  1차 검수 완료와 배포 이후 검증','자동 검사와 실제 플레이에서 확인한 부분을 나눠 정리했습니다',700)
    data=[('독립 재빌드·결과 비교','계획한 쓰기 범위 / ROM·패치 결과 동일','통과'),
      ('Windows 패치 적용','8개 사례 + 최종 ZIP 추출본 실제 적용','통과'),
      ('텍스트·인터럽트 CPU','명명한 모델 조건의 검사','한정 범위 통과'),
      ('실제 화면·완주','직접 1차 검수 완료 / 배포 이후 추가 검증 예정','1차 완료')]
    for i,(t,sub,status) in enumerate(data):
        y=165+i*120;d.rounded_rectangle((50,y,1350,y+102),radius=14,fill='#ffffff',outline='#c6d0dc',width=2)
        d.text((76,y+13),t,font=f(28),fill=INK);d.text((76,y+56),sub,font=f(24),fill='#536071');d.text((1010,y+32),status,font=f(27),fill=BLUE)
    im.save(OUT/'images/08.png')
    for item,caption in zip(provenance['figures'],CAPTIONS):
        item.update(caption=caption,image_sha256=sha(OUT/item['image']))
    plain=[TITLE,''];md=['# '+TITLE,''];blocks=[]
    for p in INTRO:plain.extend([p,'']);md.extend([p,''])
    for (title,paragraphs,indices) in SECTIONS:
        plain.extend([title,'']);md.extend(['## '+title,'']);block='<section><h2>'+html.escape(title)+'</h2>'
        for p in paragraphs:
            plain.extend([p,'']);md.extend([p,'']);block+='<p>'+prose(p)+'</p>'
        for i in indices:
            item=provenance['figures'][i-1];caption=item['caption'];plain.extend([f'[이미지 {i:02d} 삽입: {caption}]','']);md.extend([f'![{caption}]({item["image"]})',''])
            encoded=base64.b64encode((OUT/item['image']).read_bytes()).decode()
            block+=f'<figure><button class="zoom" aria-label="이미지 {i:02d} 확대"><img src="data:image/png;base64,{encoded}" alt="{html.escape(caption,quote=True)}"></button><figcaption>{html.escape(caption)}</figcaption></figure>'
        blocks.append(block+'</section>')
    old=(OLD/'작업기.html').read_text('utf-8');css=re.search(r'<style>(.*?)</style>',old,re.S)[1];js=re.search(r'<script>(.*?)</script>',old,re.S)[1]
    css+='h1,h2{word-break:keep-all}.emotion{white-space:nowrap}'
    page=f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><style>{css}</style><header><div><span class="tag">TINY TOON ADVENTURES 2</span><h1>{TITLE}</h1>'+''.join('<p>'+prose(p)+'</p>' for p in INTRO)+'</div></header><main>'+''.join(blocks)+f'</main><dialog><button>닫기</button><img alt="확대 자료"></dialog><script>{js}</script></html>'
    (OUT/'카페_복사용_본문.txt').write_text('\n'.join(plain),'utf-8-sig');(OUT/'작업기.md').write_text('\n'.join(md),'utf-8');(OUT/'작업기.html').write_text(page,'utf-8')
    (OUT/'업로드_안내.txt').write_text(f'''네이버 카페 업로드 안내

제목: {TITLE}
카페_복사용_본문.txt를 붙여 넣고, 이미지 삽입 표시에 맞춰 images/01.png~08.png를 순서대로 올려주세요.
삽입 표시는 지우고 이미지 설명은 캡션으로 남기면 됩니다.
게임 패치 첨부: TinyToonAdventures2_KR_v1.0_Release_20261009.zip
작업기 보관용 첨부: {NAME}.zip

작업기.html은 이미지 확대가 가능한 오프라인 검토용입니다.
이미지 01·03·04·05·06은 작업 과정의 실제 게임 캡처입니다.
02는 제작 원천, 07은 크레딧 정적 복원, 08은 검증 설명 표입니다.
실제 화면·완주 1차 검수는 작성자가 마쳤고, 배포 이후 추가 검증은 예정 상태입니다.
크레딧 이미지는 엔딩 내용을 포함하므로 카페 관례에 맞춰 표시해주세요.
ROM·세이브·비공개 QA는 업로드 대상이 아닙니다. 실제 카페 게시는 수행하지 않았습니다.
''','utf-8-sig')
    (OUT/'이미지_출처_구분.json').write_text(json.dumps([{k:v for k,v in item.items() if k!='sources'} for item in provenance['figures']],ensure_ascii=False,indent=2)+'\n','utf-8')
    (R/'qa/reports/publication229_sources.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n','utf-8')
    assert page.count('<figure>')==8 and len(SECTIONS)==8
    assert '사용자가' not in '\n'.join(plain) and '보고했습니다' not in '\n'.join(plain)
    print(json.dumps({'status':'VOICE_APPLIED_PENDING_RENDER','folder':OUT.relative_to(R).as_posix()},ensure_ascii=False))

if __name__=='__main__':main()
