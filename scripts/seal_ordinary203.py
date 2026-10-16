"""Reject058 isolated passes as whole-card proof: shared title/rule and frame geometry."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    p = R / 'qa/reports/ordinary11_203_scope_rejection.json'
    assert not p.exists()
    d = {'work': 203, 'status': 'REJECTED058_CARD_SHARED_FONT_AND_TITLE_GEOMETRY',
         'isolated_CPU': 'qa/reports/ordinary11_203_CPU.json',
         'single_page_CPU_pass_not_card_coexistence': True,
         'native_evidence': 'qa/dialogue/cards033_coaster/frame_01680_ppu.bin',
         'native_actual_image': 'qa/dialogue/cards033_coaster/frame_01680.png',
         'title': {'origin': 0x20a6, 'first_column': 6, 'last_column': 25, 'width_pixels': 160,
                   'top_border_y': 38, 'bottom_border_y': 49, 'original_text_y': 40,
                   'new16pixel_cell_would_overlap_original_bottom': True},
         'rules': {'origin': 0x2125, 'first_column': 5, 'last_column': 27, 'width_pixels': 184},
         'shared_consumption': 'Title and rule NT remain live with sameRAM34 upper font; separate fonts corrupt each other',
         'resolution': 'Five per-ride font unions,160px title/184px rule. Extend title frame bottom toNTrow7; native sides fromrow5.',
         'verifier_v1_failure': 'Oracle mapped old196 to254 even in deliberate phase0 retention; v2 preserves active font per010 ASM',
         'runtime058': 'NOT_RUN', 'adopted': False, 'package': False}
    p.write_text(json.dumps(d, indent=2) + '\n', 'utf-8')
    body = '''058に全普通文を入れたが共存と幾何の問題で不採用にした。'''
    body = '''全33개 일반 문자열을055/057 방식으로 확대한058 후보와 독립 재빌드를 만들었다. 원본ExpectedWrite/IPS exact, 새CHR256KiB,42개(오프닝9+일반33) 후보다. [단일 문단 CPU](../qa/reports/ordinary11_203_CPU.json)는1000F8·FA6selector×2문단·일반33·1101건너뛰기 경계·4320초기화·1556비대상·오프닝9 PASS다. 처음 CPU 검사의 phase0 글꼴 기대값은 원래010의 ‘지우는 동안 active196 유지’를 놓쳤으므로 v2에서 정확한 조건으로 정정했다. 실제 ROM은 그 사이 바꾸지 않았다.

그러나 한 문단 CPU 성공은 상단 제목과 설명의 동시거주를 증명하지 않는다. 기존033 실제 화면/NT를 대조해 둘이같은RAM34를 공유함을 확인했다.058은 두 문단에 다른 글꼴을 배정했으므로 동시에 표시하면 서로 글자가 깨진다. 또한 실제 이름 칸은20열160px/윗테두리y38·아랫테두리y49이고 설명은23열184px이다.058의192px 일반 예산을 그대로 쓰면 오른쪽 테두리/목재까지 덮고,11px 이름은 기존 낮은 테두리에 닿는다. [거부·실제 기하 원장](../qa/reports/ordinary11_203_scope_rejection.json).

따라서058은 미채택·미패키지이며 CPU PASS를 전체창 성공으로 표현하지 않는다. 기존 실제 [033 원본 창](../qa/dialogue/cards033_coaster/frame_01680.png)을 직접 열어 이름·설명 동시표시를 확인했다. 이것은 이전033 실행의 근거이지058 새실행이 아니다. 다음059는 놀이기구별 제목+설명5개 합집합 글꼴을 만들고 제목160px/설명184px를 사용한다. 이름의 아래 테두리를NT row7로 옮기며 row6 좌우는 원래 row5 세로선 타일을 재사용한다. 카드의 다른 그림은 보존한다.

원본·1편·CSV·051/055/057/058·사용자Mesen·세이브 보존. 크레딧3/작은그림·원문유지6건은 그대로다.058 새에뮬레이터/자동컨트롤러/직접장면 없음. 새256KiB CHR·NMI/IRQ·폰트수명·전역도달성은 미검증이다. 변경·해시는 [203매니페스트](../manifests/nonplay203_assets.json). 카페완성 작업기/게시 없음. 재현 빌더는 새경로만 사용하며 검사기는 기존보고를 덮어쓰지 않는다.'''
    records.seal(203, 'ORDINARY11_058_ISOLATED_CPU_CARD_REJECTION_203.md', '일반33개 후보058 단독CPU 성공·공유창 결함 거부', body,
                 '단독33문단/F8/FA/skip/초기화CPU PASS이나 제목·규칙 동시거주와 실제160/184px 창기하 결함 발견.058 미채택·미패키지.',
                 '새059 후보에서 놀이기구별 이름+설명 글꼴 공유와160/184px 기하·이름칸 높이를 수정해 동시거주를 검사한다.',
                 [Path(__file__), p, R / 'scripts/build_ordinary11_203.py', R / 'scripts/verify_ordinary11_203.py',
                  R / 'scripts/verify_ordinary11_203_v2.py', R / 'qa/reports/ordinary11_203_CPU.json',
                  R / 'workspace/asm/dialogue_page_font_010.asm', R / 'qa/dialogue/cards033_coaster/frame_01680_ppu.bin',
                  R / 'qa/dialogue/cards033_coaster/frame_01680.png',
                  *[f for folder in (R / 'build/ordinary11_candidate_058', R / 'build/ordinary11_203_rebuild058') for f in folder.iterdir() if f.is_file()]])


if __name__ == '__main__':
    main()
