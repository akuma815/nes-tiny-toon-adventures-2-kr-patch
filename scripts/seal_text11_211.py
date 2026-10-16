"""45 registered strings decoded from final062; explicit static-only comparison."""
from pathlib import Path
import json
import html
import shutil
from PIL import Image
from extract_title_png import decode
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    build = R / 'build/text11_candidate_062'
    target = build / 'TinyToon2_Text11_Candidate062.nes'
    rom = target.read_bytes()
    ordinary = json.loads((R / 'qa/reports/text11_211_ordinary_CPU.json').read_text('utf-8'))
    credit = json.loads((R / 'qa/reports/credits11_211_CPU.json').read_text('utf-8'))
    assert ordinary['status'] == 'PASS_FINAL062_33_ORDINARY_AND_NINE_OPENING_CPU'
    assert credit['status'] == 'PASS_FINAL062_CREDITS3_NATIVE_CALLS_SCROLL_CPU'
    assert ordinary['ROM_sha256'] == credit['ROM_sha256'] == sha(target)
    review = R / 'workspace/review/text11_211'
    review.mkdir(exist_ok=False)
    cards = []
    decoded = []
    for group, file in [('오프닝9', 'opening11_plan.json'), ('일반 대사·안내33', 'ordinary11_plan.json'), ('크레딧3', 'credits11_plan.json')]:
        pages = json.loads((build / file).read_text('utf-8'))['pages']
        for z in pages:
            columns = len(z['NT_rows'][0])
            image = Image.new('L', (columns * 8, len(z['NT_rows']) * 8))
            base = z['font_file_offset']
            for y, row in enumerate(z['NT_rows']):
                for x, code in enumerate(row):
                    image.paste(Image.frombytes('L', (8, 8), decode(rom[base + code * 16:base + (code + 1) * 16])), (x * 8, y * 8))
            rgb = Image.new('RGB', image.size)
            rgb.putdata([(255, 254, 255) if b else (0, 0, 0) for b in image.get_flattened_data()])
            name = z['entry_id'] + '.png'
            rgb.save(review / name)
            cards.append(f'<article><h2>{group} · {z["entry_id"]}</h2><img src="{name}"><pre>{html.escape(z.get("original_text", z.get("text", "")))}</pre></article>')
            decoded.append({'entry_id': z['entry_id'], 'group': group, 'font_bank': z['font_bank'],
                            'image': name, 'image_sha256': sha(review / name), 'actual_game_capture': False})
    assert len(decoded) == 45 and len({z['entry_id'] for z in decoded}) == 45
    for ride in range(1, 6):
        source = R / f'workspace/review/ordinary11_204/model_ride{ride:02}.png'
        name = source.name
        shutil.copyfile(source, review / name)
        cards.append(f'<article><h2>놀이기구{ride} 상단창 기하 모형</h2><p>033 원래 창의 NT 기하와059 CPU 출력으로 만든 모형입니다.062에서 이름/설명 글꼴과 문구 및 출력 픽셀이 동일함을 새CPU 검사로 확인했습니다. 실제062 캡처가 아닙니다.</p><img src="{name}"></article>')
    (review / 'review.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>텍스트11px 후보062 정적 검토</title><style>body{font-family:sans-serif;background:#202027;color:#eee;margin:24px;max-width:1200px}article{border-top:1px solid #777;padding:16px 0}img{image-rendering:pixelated;min-width:384px;width:auto;max-width:100%}pre{white-space:pre-wrap;line-height:1.5}a{color:#aee}</style><h1>텍스트11px 개발 후보062</h1><p>HUD·정지 등 작은 그림은 기존 크기를 유지했습니다. 오프닝9+일반33+크레딧3, 등록45개를 확대했습니다. 아래45개 PNG는 최종ROM 글꼴과 출력 계획을 디코딩한 정적 자료이며 실제 게임 화면이 아닙니다. 숫자는 원래8px 타일 간격을 유지하며 글자 종류에 따라 실제 획 높이가 다릅니다. 실제062 실행·CHR256 매핑·NMI/IRQ·소거·읽기 편의·최종 글꼴 승인은 아직 검수하지 않았습니다.</p><p>오프닝6문단은 ‘친구들도 데려와!’ 다음에 ‘깜짝 놀랄 거다!’를 묶었고, 빈 줄 다음 ‘의문의 대부호로부터’를 오른쪽 정렬했습니다. 크레딧은 한글12px·공백8px·영문16px 간격의 개발안입니다. 이름/KONAMI/권리 문자열은 그대로이며 글자 그림을 확대했습니다. ROM 채택·전게임 완료·공개배포·전체플레이 성공을 뜻하지 않습니다.</p>''' + ''.join(cards) + '</html>', 'utf-8')
    proof = R / 'qa/reports/text11_211_static_review.json'
    assert not proof.exists()
    proof.write_text(json.dumps({'work': 211, 'status': 'PASS_FINAL062_45_STATIC_FONT_DECODE_AND_CPU_PROVENANCE',
        'ROM_sha256': sha(target), 'decoded': decoded, 'card_models': 5,
        'actual_game_capture': False, 'new_emulator_run': False,
        'ordinary_CPU_sha256': sha(R / 'qa/reports/text11_211_ordinary_CPU.json'),
        'credits_CPU_sha256': sha(R / 'qa/reports/credits11_211_CPU.json')}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = f'''[062 ROM](../build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes) SHA `{sha(target)}`·524304바이트에 등록45개(오프닝9+일반33+크레딧3)를11px로 삽입했다. [정적45문단·상단창5모형](../workspace/review/text11_211/review.html), [원장](../qa/reports/text11_211_static_review.json). HUD·정지 등 작은 그림, 번역CSV,원문유지6건은 기존대로다. 크레딧 이름·KONAMI·법적 문자열은 보존하고11px 획으로 확대했으므로 옛 글자 bitmap 보존이라고 주장하지 않는다. 영문16px 간격은 개발안이다.

정적·빌드: 원본ExpectedWrite 전체·허용 diff·IPS 적용·독립 ROM/IPS 재빌드 exact. 기존42개의 문자 스트림/글꼴 픽셀은059와 동일하다. 새크레딧 font201/202 106슬롯을 사용한다. [기존42 CPU](../qa/reports/text11_211_ordinary_CPU.json):33문단1042수치상태/1071건너뛰기/4320초기화/1556비대상/교환050 보존10/놀이기구5개 동시거주·이름 테두리·오프닝9 PASS.

[크레딧 CPU](../qa/reports/credits11_211_CPU.json): A448 직접첫756NT셀·NMI/렌더 중지중2006/2007쓰기·2000 복원, 진행2E169/2F158호출에서 원래 carry/58대기/종료·전NT픽셀 exact. 최대이벤트 큐20/62바이트, 관측stack최저248·충돌없음. 원래A492의4000frame 수동동기CPU스케줄(6DF/FC/FF/6CF/58)이059와일치한다. 프레임루프는 CPU 입력값을 제공한 검증이며 에뮬레이터를 실행하지 않았다.

원래FF17은2000만복원하고2001은출력을중지한상태로다음nativeNMI를기다린다. 초기전체A430 하드웨어·다음NMI·실제PPU aliasing/스크롤/전송예산/폰트수명·상단창소거·CHR256 실제매핑·최종가독성은미수행이다.062는실제검수전·미채택개발후보다. 이전055오프닝실제근거를062전체성공으로옮기지않는다.060/061 CPU거부본과이전051/055/057/059·원본/CSV/1편·사용자Mesen/세이브를보존했다. 카페완성작업기·외부게시없음. 변경·해시는 [211매니페스트](../manifests/nonplay211_assets.json).

재현: `python scripts/build_credits11_211.py --output build/text11_211_repro_next`. 검사기는고정보고를덮어쓰지않으므로 새보고/빌드경로를쓴복제에서수행한다. 패키지작업에서실Windows 적용을추가한다.'''
    files = [Path(__file__), proof, *[R / f'scripts/{n}' for n in ('prepare_credits211.py', 'build_credits11_211.py', 'verify_credits11_211.py', 'verify_text11_ordinary211.py')],
             R / 'qa/reports/credits11_211_CPU.json', R / 'qa/reports/text11_211_ordinary_CPU.json',
             *[p for folder in (build, R / 'build/text11_211_rebuild062') for p in folder.iterdir() if p.is_file()],
             *[p for p in review.iterdir() if p.is_file()]]
    records.seal(211, 'TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md', '062 등록45개11px 빌드·CPU·정적 복원', body,
        '오프닝9+일반33+크레딧3 전등록45개11px 후보062.독립빌드/기존42CPU/크레딧327호출·4000frame동기CPU PASS.작은그림보존,실제062 미수행·미채택.',
        '062 ROM없는 적용패키지를 만들고 Windows8사례·최종ZIP 적용을 검증한다.', files)
    print(json.dumps({'status': 'PASS', 'registered11px': 45, 'static_images': 50, 'ROM_sha256': sha(target)}, indent=2))


if __name__ == '__main__':
    main()
