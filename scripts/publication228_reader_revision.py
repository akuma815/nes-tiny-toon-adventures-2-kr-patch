"""Rewrite public articles by subject; preserve private build identities and raw evidence."""
from pathlib import Path
import base64, html, json, re, shutil
from PIL import Image
from seal_nonplay171 import R, sha
from publication221 import canvas, pair, paste, f, INK, BLUE
import build_technical_guide228 as guide

NAME='TinyToon2_KR_Worklog_Reader_20261009'
OUT=R/'workspace/publication'/NAME
GUIDE=R/'workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009'
PATCH='TinyToonAdventures2_KR_v1.0_Release_20261009.zip'
TITLE='타이니툰 어드벤처 2 한글화 작업기 — 그림과 대사가 화면에 닿기까지'
LEAD='타이틀을 한글로 바꾸는 작은 실험에서 시작해, 대사 출력과 글꼴 확대, 티켓 교환 오류 수정까지 이어진 작업을 정리했습니다. 다른 NES 게임의 한글화를 시작하는 분에게도 도움이 되도록, 결과와 함께 시행착오의 원인을 설명합니다.'

SECTIONS=[
('1. 타이틀 한 장에서 시작했습니다',[
 '1편에서 사용한 PNG 추출 → 생성형 이미지 → 게임 타일 재삽입 흐름을 2편에서도 이어갔습니다. 로고에는 ‘타이니 툰 어드벤처’와 ‘몬타나랜드에 어서 오세요’를 넣고, 숫자 2와 PUSH START, 저작권 문구는 유지했습니다.',
 '처음에는 화면에서 보이는 타일을 찾으면 될 것 같았지만, 2편은 화면을 그리는 도중 글자 그림과 배치를 바꿨습니다. 프레임 끝의 메모리만 보면 실제 로고에 쓰인 데이터를 놓칠 수 있었습니다. ROM에서 찾은 후보가 언제, 어디에 표시되는지 실행 경로까지 연결해야 했습니다.'],[1]),
('2. 생성형 이미지를 NES 그림으로 바꾸기',[
 '생성형 이미지는 한글 로고의 모양을 잡는 데 사용했습니다. 게임에 넣는 단계에서는 원래 로고 공간과 4색 팔레트에 맞춰 픽셀을 정리하고, 8×8 타일로 나눈 뒤 중복 타일을 묶었습니다. 화면 배치 데이터도 다시 만들고 압축 공간에 맞춰 넣었습니다.',
 '그림이 보기 좋다고 삽입까지 끝난 것은 아니었습니다. 축소하면서 작은 글자의 획이 사라졌고, 리본 문구는 정적 합성과 실제 화면의 위치가 달랐습니다. 리본과 보조 글자를 따로 교정하면서 생성 결과를 게임이 표시할 수 있는 형태로 다듬었습니다. 재현할 때는 새 이미지를 다시 생성하는 대신, 채택한 PNG를 고정 입력으로 사용합니다.'],[2]),
('3. 글자를 찾는 것에서 출력기를 이해하는 것으로',[
 '대사는 일본어 문장을 한글로 치환하는 것만으로 해결되지 않았습니다. 문자 코드와 폰트 타일, 포인터와 제어코드, 화면에 한 글자씩 보내는 출력기가 서로 연결돼 있었습니다. 문단에 필요한 한글 글꼴을 공급하면서도 원래의 대기·지우기·분기 동작을 유지해야 했습니다.',
 '오프닝, 홈과 놀이기구 선택, 매표소, 놀이기구 안내, 성 입구와 크레딧을 작업했습니다. 지도·간판·결과 화면·HUD·정지 표지판처럼 그림으로 들어 있는 글자는 별도로 처리했습니다. 등록 대상은 오프닝 9문단, 일반 대사 33문단, 크레딧 3문단입니다. 이 수량은 숨은 문자열까지 모두 발견했다는 뜻은 아닙니다.',
 '사용 경로가 확정되지 않은 HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT는 사용자 결정에 따라 원문을 유지했습니다. 확인한 표시 경로와 이번 번역 범위를 기록해 두는 일도 한글화의 일부였습니다.'],[]),
('4. 티켓 교환 뒤 대사가 깨진 이유',[
 '교환 전에는 읽히던 대사가 티켓을 바꾼 뒤 깨졌습니다. 문장 데이터가 잘못된 것이 아니라, 숫자를 갱신하는 경로가 하단 대사에 필요한 글꼴을 다른 글꼴로 바꾸는 충돌이었습니다. 같은 화면에서 숫자와 대사가 각자 다른 출력 경로를 사용하고 있었던 것입니다.',
 '숫자를 갱신해도 하단 대사의 글꼴을 유지하도록 수정했습니다. 초기 재화를 설정해 같은 교환 경로를 재현하고, 수정 전·후 화면과 CPU 상태를 비교했습니다. 이 경험은 새 문단을 출력하는 순간뿐 아니라, 숫자가 바뀌거나 다음 대사를 기다리는 동안에도 글꼴이 유지되는지 확인해야 한다는 지침이 됐습니다.'],[3]),
('5. HUD 여백과 움직이는 정지 표지판',[
 '상태창의 왼쪽과 아래가 비어 보인다는 제보는 원본과 같은 입력으로 비교했습니다. 왼쪽 8픽셀의 배경색 띠와 아래 검은 여백은 일본판에도 있었습니다. 한글 HUD 내용이 2픽셀 아래로 이동한 변경은 따로 구분했습니다. 화면이 어색해 보인다는 이유만으로 모두 패치 오류라고 판단할 수는 없었습니다.',
 '고정 정지 표지판을 번역한 뒤에도 위아래로 움직이는 표지판에는 STOP이 남아 있었습니다. 모양은 비슷해도 사용하는 스프라이트 타일이 달랐습니다. 움직이는 표지판의 실제 타일을 찾아 글자만 ‘정지’로 바꾸고, 테두리와 기둥은 보존했습니다. 같은 단어가 한 번 번역됐다고 모든 표시 경로가 처리된 것은 아니었습니다.'],[4,5]),
('6. 일반 대사를 11px로 키우기',[
 'HUD와 정지 표지판은 원래 그림의 공간이 좁아 기존 크기를 유지했습니다. 그 외 등록 문단은 Galmuri11로 확대했습니다. 최대 한글 획높이 11px를 폭 12px·높이 16px 셀에 넣고, 두 타일 행으로 출력했습니다. 숫자는 기존 8px 타일 간격을 사용하므로 모든 문자가 같은 획높이를 갖는 것은 아닙니다.',
 '오프닝부터 시험하면서 줄바꿈을 조정했습니다. 여섯 번째 문단의 ‘깜짝 놀랄 거다!’는 아래 한 줄로 묶고, ‘의문의 대부호로부터’는 오른쪽에 맞췄습니다. 글꼴 크기를 바꾸면 문장이 차지하는 폭과 빈줄, 화자 표시도 함께 조정해야 했습니다.',
 '일반 대사와 크레딧으로 확장할 때는 한 화면에 동시에 필요한 글꼴과 저장 용량도 확인했습니다. 놀이기구 이름과 설명은 공유 글꼴로 배치했고, 크레딧의 이름·KONAMI·권리 문자열은 유지하면서 글자 그림을 확대했습니다. 영문 이름은 16px 간격을 사용합니다.',
 '아래 오프닝은 글꼴 확대 시험 당시의 실제 캡처로, 각 문단이 완성된 시점은 서로 다릅니다. 크레딧 그림은 배포 데이터의 정적 복원입니다. 작업 과정의 실제 캡처와 정적 복원을 구분해 실었습니다.'],[6,7]),
('7. 완성 화면과 배포 파일을 각각 확인했습니다',[
 '깨끗한 원본에서 다시 빌드하고, 계획한 쓰기 범위를 재적용해 최종 ROM 전체와 비교했습니다. 차분 패치를 적용한 결과도 같은 바이트인지 확인했습니다. 바뀐 부분의 목록만 보는 것보다, 최종 결과 전체가 재현되는지 확인하는 것이 중요했습니다.',
 '배포 적용 도구는 실제 Windows에서 정상 입력과 오류 입력을 포함한 8개 사례를 확인했습니다. 최종 ZIP을 다시 풀어 한글·공백 경로에서 apply.cmd를 실행했고, 생성된 ROM이 배포 결과와 완전히 같았습니다.',
 '텍스트 출력·변수·건너뛰기·은행 복귀와 인터럽트는 한정된 CPU 모델 조건에서 검사했습니다. 옛 출력 경로를 직접 호출해 잘못 판단했던 측정은 철회하고 실제 진입점에서 다시 확인했습니다. 이 검사는 모델에서 조사한 조건의 근거이며, 모든 하드웨어 환경의 동작을 보증하는 결과로 확대하지 않습니다.',
 '2026년 10월 9일, 사용자가 실제 화면과 완주의 1차 검수를 완료했다고 보고했습니다. 배포 이후에는 추가 제보와 검증을 이어갈 예정입니다. 이 글의 비교 이미지는 각 수정 과정을 남긴 자료이며, 완주 전체를 촬영한 기록은 아닙니다.'],[8]),
('8. 배포와 다음 한글화에 남기는 기록',[
 f'배포 파일은 {PATCH}입니다. 게임 ROM은 포함하지 않았습니다. 일본판 Tiny Toon Adventures 2 - Montana Land e Youkoso의 깨끗한 원본 .nes 파일을 준비하고, ZIP을 모두 푼 뒤 원본을 apply.cmd에 끌어 놓으면 원본이름_KR.nes가 생성됩니다. 원본과 기존 출력 파일은 덮어쓰지 않습니다.',
 '원본은 262,160바이트, 결과는 524,304바이트입니다. 적용 도구가 크기와 SHA-256을 검사하므로 이전 한글판에 덧씌우지 않고 일본판 원본에서 시작합니다. 원본 SHA-256은 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d, 결과는 7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce입니다.',
 '이전 세이브스테이트의 호환은 확인되지 않았습니다. 수정 확인은 새 ROM을 열고 초기화한 뒤 진행합니다. 오류 제보에는 사용 ROM 해시, 에뮬레이터 버전, 직전 행동과 장면 이미지를 함께 남기면 재현 경로를 좁히는 데 도움이 됩니다.',
 '이번 작업에는 Galmuri7/Galmuri11과 xdelta3를 사용했고, 출처와 라이선스는 배포 ZIP에 넣었습니다. 원작과 캐릭터의 권리는 각 권리자에게 있습니다.',
 '후속 한글화에 가장 남기고 싶은 것은 화면과 데이터를 연결한 기록입니다. 채택한 그림과 번역 원천, 재현 명령, 검증한 조건과 아직 확인하지 못한 조건을 함께 남겨야 다음 사람이 같은 시행착오를 줄일 수 있습니다.'],[])]

def make_worklog():
    assert not OUT.exists();(OUT/'images').mkdir(parents=True)
    evidence=[]
    def save(n,im,caption,kind,sources):
        p=OUT/'images'/f'{n:02d}.png';im.save(p)
        evidence.append({'index':n,'image':f'images/{n:02d}.png','caption':caption,'kind':kind,
          'image_sha256':sha(p),'sources':[{'path':s.relative_to(R).as_posix(),'sha256':sha(s)} for s in sources]})
    comparison=R/'qa/title/title_kr_ai_003_comparison.png'
    source=Image.open(comparison).convert('RGB')
    a=OUT/'original_title_crop.png';b=OUT/'korean_title_crop.png'
    source.crop((128,20,384,260)).save(a);source.crop((648,20,904,260)).save(b)
    save(1,pair('01  타이틀에서 시작한 한글화','타이틀 작업 당시 실제 실행 캡처',a,b,['일본판 원본','한글화 타이틀']),
      '원본과 한글화 타이틀의 실제 캡처. 게임명과 부제를 번역하고 숫자 2·시작 안내·저작권은 유지했습니다.','historical_actual_capture',[comparison])
    a.unlink();b.unlink()
    original=R/'extracted/title/title_20261004_001/main_original.png'
    raw=R/'workspace/graphics/title/ai_main_001/main_ai_raw.png'
    converted=R/'build/title_kr_ai_003/main_nes.png'
    im,d=canvas('02  PNG → 생성형 이미지 → NES 타일','제작 원천과 변환 결과 · 실제 게임 캡처가 아닌 설명 자료',620)
    for x,p,t in [(35,original,'원본 PNG 추출'),(485,raw,'AI 생성 원천'),(935,converted,'NES 4색·타일 변환')]:
        d.text((x+20,175),t,font=f(27),fill=INK);paste(im,p,x,230,(425,280),nearest=p!=raw)
    d.text((52,550),'픽셀·팔레트·타일과 압축 공간에 맞춰 변환한 뒤 작은 글자를 교정했습니다.',font=f(26),fill=INK)
    save(2,im,'원본 PNG, 생성형 이미지 원천, NES 변환 결과. 리본 문구와 작은 글자는 별도로 교정했습니다.','production_sources',[original,raw,converted])
    pairs=[
      (3,'티켓 교환 뒤 대사 깨짐 수정','실제 재현 캡처 · 초기 재화를 설정해 같은 교환 경로 비교',
       'qa/dialogue/issue177_exchange_049/frame_01710.png','qa/dialogue/issue177_exchange_050/frame_01710.png',
       ['수정 전 · 대사 글꼴 충돌','수정 후 · 대사 글꼴 유지'],
       '같은 티켓 교환 경로의 수정 전·후 실제 캡처. 숫자 갱신과 하단 대사 글꼴의 충돌을 수정했습니다.'),
      (4,'HUD의 빈 여백은 원본과 비교','실제 실행 캡처 · 왼쪽 띠와 아래 검은 여백은 원본에도 존재',
       'qa/dialogue/hud180_coaster_source/frame_03000.png','qa/dialogue/hud180_coaster_050/frame_03000.png',
       ['일본판 원본','한글판'],
       '동일 입력의 원본·한글판 롤러코스터 캡처. 큰 여백은 원래 구성이고, 한글 HUD의 2픽셀 아래 이동은 별도 변경입니다.'),
      (5,'움직이는 STOP도 따로 수정','실제 실행 캡처 · 고정 표지판과 다른 스프라이트 타일 사용',
       'qa/dialogue/moving_stop181_050/frame_04200.png','qa/dialogue/moving_stop182_051/frame_04200.png',
       ['수정 전 · 움직이는 STOP','수정 후 · 움직이는 정지'],
       '움직이는 표지판의 수정 전·후 실제 캡처. 다른 타일 경로를 찾아 글자만 바꾸고 테두리와 기둥은 보존했습니다.'),
      (6,'일반 텍스트를 11px로 확대','오프닝 시험 당시 실제 캡처 · 문단 완성 시점은 서로 다름',
       'workspace/review/opening11_194/page06_8px.png','workspace/review/opening11_194/page06_11px.png',
       ['확대 전 · 8px','확대 후 · 11px'],
       '오프닝 여섯 번째 문단의 글꼴 확대 전·후 실제 캡처. 같은 프레임의 비교는 아닙니다.')]
    for n,t,sub,l,r,labels,caption in pairs:
        left=R/l;right=R/r
        save(n,pair(f'{n:02d}  {t}',sub,left,right,labels),caption,'historical_actual_capture',[left,right])
    sources=[R/'workspace/review/text11_211'/f'{key}.png' for key in ('MAIN_05939','MAIN_05999','MAIN_059E7')]
    im,d=canvas('07  크레딧까지 이어지는 글꼴 확대','배포 데이터의 정적 복원 · 실제 실행 캡처가 아닙니다',730)
    for x,p,t in zip((26,484,942),sources,('크레딧 1','크레딧 2','크레딧 3')):
        d.text((x+22,156),t,font=f(28),fill=INK);paste(im,p,x,210,(432,470))
    save(7,im,'크레딧 세 문단의 정적 복원. 이름·KONAMI·권리 문자열을 유지하면서 글자 그림을 확대했습니다.','static_ROM_decode',sources)
    im,d=canvas('08  1차 검수 완료와 배포 이후 검증','자동 검사와 사용자 플레이 검수를 구분한 설명 표',700)
    data=[('독립 재빌드·결과 비교','계획한 쓰기 범위 / ROM·패치 결과 동일','통과'),
      ('Windows 패치 적용','8개 사례 + 최종 ZIP 추출본 실제 적용','통과'),
      ('텍스트·인터럽트 CPU','명명한 모델 조건의 검사','한정 범위 통과'),
      ('실제 화면·완주','사용자 1차 검수 완료 / 배포 이후 추가 검증 예정','1차 완료')]
    for i,(t,sub,status) in enumerate(data):
        y=165+i*120;d.rounded_rectangle((50,y,1350,y+102),radius=14,fill='#ffffff',outline='#c6d0dc',width=2)
        d.text((76,y+13),t,font=f(28),fill=INK);d.text((76,y+56),sub,font=f(24),fill='#536071');d.text((1010,y+32),status,font=f(27),fill=BLUE)
    save(8,im,'재빌드·Windows 적용과 한정 CPU 검사는 통과했습니다. 실제 화면·완주 1차 완료는 사용자 보고이며, 배포 이후 추가 검증은 예정 상태입니다.',
      'explanatory_validation_summary',[R/'qa/reports/release224_verified.json',R/'qa/reports/user_review224.json',R/'qa/reports/irq217_injection.json',R/'qa/reports/irq218_opening_credits.json'])
    byid={x['index']:x for x in evidence};plain=[TITLE,'',LEAD,''];md=['# '+TITLE,'',LEAD,''];blocks=[]
    for title,paragraphs,indices in SECTIONS:
        plain.extend([title,'']);md.extend(['## '+title,'']);block='<section><h2>'+html.escape(title)+'</h2>'
        for p in paragraphs:
            plain.extend([p,'']);md.extend([p,'']);block+='<p>'+html.escape(p)+'</p>'
        for i in indices:
            item=byid[i];caption=item['caption'];plain.extend([f'[이미지 {i:02d} 삽입: {caption}]','']);md.extend([f'![{caption}]({item["image"]})',''])
            encoded=base64.b64encode((OUT/item['image']).read_bytes()).decode()
            block+=f'<figure><button class="zoom" aria-label="이미지 {i:02d} 확대"><img src="data:image/png;base64,{encoded}" alt="{html.escape(caption,quote=True)}"></button><figcaption>{html.escape(caption)}</figcaption></figure>'
        blocks.append(block+'</section>')
    old=(R/'workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009/작업기.html').read_text('utf-8')
    css=re.search(r'<style>(.*?)</style>',old,re.S)[1];js=re.search(r'<script>(.*?)</script>',old,re.S)[1]
    page=f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><style>{css}</style><header><div><span class="tag">TINY TOON ADVENTURES 2 · 한글화 작업기</span><h1>{TITLE}</h1><p>{LEAD}</p></div></header><main>'+''.join(blocks)+f'</main><dialog><button>닫기</button><img alt="확대 자료"></dialog><script>{js}</script></html>'
    (OUT/'카페_복사용_본문.txt').write_text('\n'.join(plain),'utf-8-sig')
    (OUT/'작업기.md').write_text('\n'.join(md),'utf-8');(OUT/'작업기.html').write_text(page,'utf-8')
    (OUT/'업로드_안내.txt').write_text(f'''네이버 카페 업로드 안내

제목: {TITLE}
1. 카페_복사용_본문.txt를 게시글 본문에 붙여 넣습니다.
2. 이미지 삽입 표시 위치에 images/01.png~08.png를 순서대로 올립니다.
3. 삽입 표시를 제거하고 이미지 설명을 캡션으로 남깁니다.
4. 게임 패치 첨부: {PATCH}
5. 작업기 보관용 첨부: {NAME}.zip

작업기.html은 오프라인 검토용이며 이미지 확대를 지원합니다.
이미지 01·03·04·05·06은 작업 과정의 실제 게임 캡처입니다.
02는 제작 원천, 07은 크레딧 정적 복원, 08은 검증 설명 표입니다.
1차 실제 화면·완주 완료는 사용자 보고입니다. 배포 이후 추가 검증은 예정 상태입니다.
크레딧 그림은 엔딩 내용을 포함하므로 카페 관례에 맞춰 표시합니다.
ROM·세이브·비공개 QA는 업로드 대상이 아닙니다. 실제 카페 게시는 수행하지 않았습니다.
''','utf-8-sig')
    (OUT/'이미지_출처_구분.json').write_text(json.dumps([{k:v for k,v in z.items() if k!='sources'} for z in evidence],ensure_ascii=False,indent=2)+'\n','utf-8')
    (R/'qa/reports/publication228_sources.json').write_text(json.dumps({'work':228,'article':OUT.relative_to(R).as_posix(),'new_game_execution':False,'source_pixels_unchanged':True,'figures':evidence},ensure_ascii=False,indent=2)+'\n','utf-8')

def make_guide():
    old=R/'workspace/publication/TinyToon12_TechnicalGuide_20261009'
    assert not GUIDE.exists();GUIDE.mkdir(parents=True)
    text=(old/'기술_지침.md').read_text('utf-8')
    replacements=[
      ('2편 v1.0은 후보 062와 같은 데이터이고, 사용자가 실제 화면·완주 1차 검수를 마쳤습니다.','2편 v1.0은 사용자가 실제 화면·완주 1차 검수를 마쳤습니다.'),
      ('아래는 이 프로젝트의 빌더 인터페이스 예이며 일반 NES 게임용 명령은 아닙니다.','원본 검증 명령은 아래와 같습니다. 실제 재빌드 명령은 각 프로젝트의 최신 인계문서에서 확인합니다.'),
      ('```powershell\n# 1편 프로젝트 루트, 원본과 등록된 입력 파일이 준비된 상태\npowershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1\npython -B scripts/build_dialogue_footer_fix.py --active-font-nops 2 --output build/guide_repro_new\n\n# 2편 프로젝트 루트, 원본과 등록된 입력 파일이 준비된 상태\npowershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1\npython -B scripts/build_credits11_211.py --output build/guide_repro_new\n```',
       '```powershell\n# 각 프로젝트 루트에서 원본과 등록된 입력 파일을 준비한 뒤 실행\npowershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1\n```'),
      ('아래 파일명은 작업 원천이 제공된 환경에서의 참조 위치입니다. 본 게시 자료에 프로젝트 전체 소스와 원본 ROM이 포함되는 것은 아닙니다.',
       '프로젝트를 이어받으면 최신 인계문서인 `docs/HANDOFF.md`에서 다음 목적에 맞는 자료를 찾습니다. 본 게시 자료에 프로젝트 전체 소스와 원본 ROM이 포함되는 것은 아닙니다.'),
      ('| 목적 | 1편 프로젝트 상대 경로 | 2편 프로젝트 상대 경로 |\n|---|---|---|\n| 타이틀 경로와 압축 | `docs/POC_TITLE.md` | `docs/POC_TITLE.md` |\n| 대사 추출 | `scripts/extract_dialogue.py` | `scripts/extract_text.py` |\n| 초기 한 문단 PoC | `docs/POC_DIALOGUE.md` | `docs/POC_DIALOGUE.md` |\n| 전체 글꼴·후크 구조 | `docs/DIALOGUE_FULL.md` | `docs/TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md` |\n| 교환 오류 원인과 수정 | `docs/HAMTON_FONT_FIX_2026-10-04.md` | `docs/BOOTH_EXCHANGE_FONT_FIX_050_177.md` |\n| 11px와 용량 설계 | `docs/FONT_SIZE_SURVEY.md` | `docs/OPENING11_PAIRED_ROW_POC053_BUILD_186.md`, `docs/TEXT11_REMAINING_NUMERALS_CARDS_CREDITS_DESIGN_201.md` |\n| 크레딧 정렬 | 원래 등록 대사·영화 소비기 확인 | `docs/CREDITS11_SHARED_FONT106_SPACING_OPTION_202.md`와 최종 211 기록 |\n| 최종 배포와 현재 상태 | `docs/HANDOFF.md` | `docs/HANDOFF.md`, `docs/FINAL_DELIVERY_CLEANUP_226.md` |',
       '| 목적 | 1편에서 읽을 자료 | 2편에서 읽을 자료 |\n|---|---|---|\n| 타이틀 경로와 압축 | 타이틀 추출·압축 조사 | 타이틀 추출·실제 CHR 매핑 조사 |\n| 대사 추출 | 대사 추출기와 등록 목록 | 텍스트 추출기와 번역 CSV |\n| 초기 한 문단 실험 | 대사 출력 검증 기록 | 한 문단 한글 출력 실험 |\n| 전체 글꼴·후크 구조 | 전체 대사 글꼴 공급 구조 | 일반 대사·오프닝·크레딧의 큰 글자 출력 구조 |\n| 교환 오류 원인과 수정 | 당근 교환 후 대기 글꼴 수정 | 티켓 교환 후 숫자·대사 글꼴 충돌 수정 |\n| 11px와 용량 설계 | 글꼴 크기와 공간 조사 | 두 타일 행 출력·숫자·카드·크레딧 용량 설계 |\n| 크레딧 정렬 | 등록 대사와 영화 출력 경로 | 공유 글꼴·문자 간격·최종 출력 검증 |\n| 최종 배포와 현재 상태 | 최신 인계·릴리즈 보고 | 최신 인계·릴리즈 보고·사용자 검수 보고 |'),
      ('이후 최종 062에서는 그 용량 해법을 구현해 검증했습니다.','최종 배포본에서는 그 용량 해법을 구현해 검증했습니다.')]
    for a,b in replacements:
        assert text.count(a)==1,a;text=text.replace(a,b)
    (GUIDE/'기술_지침.md').write_text(text,'utf-8')
    shutil.copyfile(old/'examples_nes.py',GUIDE/'examples_nes.py')
    (R/'qa/reports/technical228_replacements.json').write_text(json.dumps([{'old':a,'new':b} for a,b in replacements],ensure_ascii=False,indent=2)+'\n','utf-8')
    guide.OUT=GUIDE;guide.main()

def main():
    make_worklog();make_guide()
    for folder in (OUT,GUIDE):
        for p in folder.rglob('*'):
            if p.suffix in ('.md','.txt','.json','.html'):
                value=p.read_text('utf-8-sig')
                if p.suffix=='.html':value=re.sub(r'data:image/png;base64,[^"\s]+','[embedded PNG]',value)
                value=re.sub(r'\b[0-9a-f]{64}\b','[SHA256]',value)
                assert not re.search(r'(?<!\d)(?:003|049|050|051|053|055|062)(?!\d)|_\d{3}\b|작업\s*\d{3}',value),(p,value)
    print(json.dumps({'status':'REWRITTEN_PENDING_RENDER','worklog':str(OUT),'guide':str(GUIDE)},ensure_ascii=False))

if __name__=='__main__':main()
