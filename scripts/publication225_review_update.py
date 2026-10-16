"""Update the public article with the user's first playthrough report."""
from pathlib import Path
import json,shutil,base64,re
from seal_nonplay171 import R,sha
from publication221 import canvas,f,INK,BLUE
NAME='TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009'
OUT=R/'workspace/publication'/NAME
OLD=R/'workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009_003'
PATCH='TinyToonAdventures2_KR_v1.0_Release_20261009.zip'

def main():
    assert not OUT.exists();shutil.copytree(OLD,OUT)
    old_caption='빌드·Windows적용은 통과했습니다. CPU/NMI/IRQ는 명명한 모델 조건에 한정하고062 실제 화면·완주 결과는 미기록으로 남겼습니다.'
    caption='빌드·Windows 적용은 통과했습니다. CPU/NMI/IRQ는 명명한 모델 조건에 한정합니다. 사용자가 062 실제 화면·완주 1차 검수를 완료했으며, 배포 이후 추가 검증을 이어갈 예정입니다.'
    replacements={
      'TinyToonAdventures2_KR_v1.0_20261009.zip':PATCH,
      'TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009.zip':NAME+'.zip',
      '실제062 화면·완주 검수 결과는 아직 기록되지 않았습니다.':'062의 실제 화면·완주 1차 검수를 마쳤습니다. 배포 이후 추가 검증을 이어갈 예정입니다.',
      '062 실제 화면·전체 플레이 검수 결과는 현재 작업 기록에 없습니다. 그 검수는 사용자가 담당합니다. 가독성, 소거와 화면 전환, 실제 글꼴 매핑과 크레딧 스크롤은 직접 확인할 항목으로 남겼습니다. 이전003/050/051 캡처를 이번 v1.0의 완주 증거로 취급하지 않았습니다.':
      '2026년 10월 9일, 062의 실제 화면·완주 1차 검수를 마쳤습니다. 배포 이후에도 제보와 추가 검증을 이어갈 예정입니다. 이번 글에 들어간 이전 003/050/051 캡처는 각 수정 과정을 설명하는 자료이며, 062의 완주 캡처로 바꾸어 표기하지 않았습니다.',
      '본문의 실제062 화면·플레이 검수 미기록 안내와 원문 유지 범위를 함께 게시합니다.':
      '본문의 062 실제 화면·완주 1차 검수 완료 및 배포 이후 추가 검증 예정 안내와 원문 유지 범위를 함께 게시합니다.',
      old_caption:caption,
      '7. 검증을 통과한 항목과 남겨 둔 항목':'7. 1차 검수 완료와 배포 이후 검증',
    }
    for p in OUT.iterdir():
        if p.suffix not in ('.txt','.md','.html'):continue
        txt=p.read_text('utf-8-sig')
        for a,b in replacements.items():txt=txt.replace(a,b)
        # Typography only; keep hashes, filenames and technical labels intact.
        for a,b in {'흐름을2편':'흐름을 2편','방식입니다. 숫자':'방식입니다. 숫자',
         '숫자2,':'숫자 2,','여기서45는':'여기서 45는','문단 수(오프닝9·일반33·크레딧3)':'문단 수(오프닝 9·일반 33·크레딧 3)',
         '이나100%':'이나 100%','원래 로고 공간과4색':'원래 로고 공간과 4색','같은8×8':'같은 8×8',
         '글꼴을11px':'글꼴을 11px','최대 한글 획높이11px를12px 폭·16px 높이':'최대 한글 획높이 11px를 12px 폭·16px 높이',
         '기존8px':'기존 8px','영문은16px':'영문은 16px','총212,764회':'총 212,764회',
         '일본판 Tiny Toon Adventures2':'일본판 Tiny Toon Adventures 2','원본은262,160':'원본은 262,160',
         '결과는524,304':'결과는 524,304','결과는7e32':'결과는 7e32','v1.0은062':'v1.0은 062',
         '기록입니다. v1.0':'기록입니다. v1.0'}.items():txt=txt.replace(a,b)
        p.write_text(txt,'utf-8-sig' if p.suffix=='.txt' else 'utf-8')
    im,d=canvas('08  1차 검수 완료와 배포 이후 검증','v1.0 데이터는 062와 동일 · 자동 검사와 사용자 검수를 구분합니다',700)
    data=[('독립 재빌드·전체 결과','원본 ExpectedWrites / ROM·IPS 동일','통과'),
      ('Windows 패치 적용','8개 사례 + 최종 ZIP 추출본 실제 적용','통과'),
      ('텍스트·인터럽트 CPU','등록 문단 검사 / 한정 IRQ 212,764회','한정 범위 통과'),
      ('062 실제 화면·완주','사용자 1차 검수 완료 / 배포 이후 추가 검증 예정','1차 완료')]
    for i,(title,sub,status) in enumerate(data):
        y=165+i*120;d.rounded_rectangle((50,y,1350,y+102),radius=14,fill='#ffffff',outline='#c6d0dc',width=2)
        d.text((76,y+13),title,font=f(28),fill=INK);d.text((76,y+56),sub,font=f(24),fill='#536071')
        d.text((1010,y+32),status,font=f(27),fill=BLUE)
    im.save(OUT/'images/08.png')
    p=OUT/'작업기.html';txt=p.read_text('utf-8')
    encoded=base64.b64encode((OUT/'images/08.png').read_bytes()).decode()
    matches=list(re.finditer(r'(<img src="data:image/png;base64,)([^" ]+)',txt));assert len(matches)==8
    m=matches[7];txt=txt[:m.start(2)]+encoded+txt[m.end(2):];p.write_text(txt,'utf-8')
    q=json.loads((R/'qa/reports/publication221_sources.json').read_text('utf-8'))
    q.update(work=225,article=OUT.relative_to(R).as_posix(),user_first_QA='COMPLETED_USER_REPORTED',post_release_QA='PLANNED')
    item=q['figures'][7];item.update(caption=caption,image_sha256=sha(OUT/'images/08.png'))
    refs=[R/'qa/reports/release224_verified.json',R/'qa/reports/user_review224.json',
      R/'qa/reports/irq217_injection.json',R/'qa/reports/irq218_opening_credits.json']
    item['sources']=[{'path':p.relative_to(R).as_posix(),'sha256':sha(p)} for p in refs]
    (R/'qa/reports/publication225_sources.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf-8')
    (OUT/'이미지_출처_구분.json').write_text(json.dumps([{k:v for k,v in item.items() if k!='sources'} for item in q['figures']],ensure_ascii=False,indent=2)+'\n','utf-8')
    plain=(OUT/'카페_복사용_본문.txt').read_text('utf-8-sig')
    assert '미기록' not in plain and '아직 기록되지' not in plain and PATCH in plain
    assert '1차 검수를 마쳤습니다' in plain and '배포 이후 추가 검증' in plain
    print(json.dumps({'status':'UPDATED_PENDING_RENDER','folder':OUT.relative_to(R).as_posix()},ensure_ascii=False))

if __name__=='__main__':main()
