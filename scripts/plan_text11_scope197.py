"""User scope: enlarge script text, preserve compact bitmap/HUD/sign consumers."""
from pathlib import Path
import csv
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    p = R / 'qa/reports/text11_197_scope.json'
    assert not p.exists()
    plan = json.loads((R / 'qa/reports/text11_190_plan.json').read_text('utf-8'))
    rows = list(csv.DictReader((R / 'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')))
    targets = []
    for z in plan['pages']:
        group = z['family']
        targets.append({'entry_id': z['entry_id'], 'native_ids': z['aliases'], 'family': group,
                        'status': ('OPENING055_VERIFIED' if group == 'opening_verified053' else
                                   'SCROLL_REDESIGN_REQUIRED' if group == 'credits_scroll' else
                                   'DIALOGUE_RENDERER_EXTENSION_REQUIRED'),
                        'font_tile_capacity190': z.get('all_variable_values_font_union_tiles')})
    d = {'work': 197, 'status': 'USER_SCOPE_SCRIPT_TEXT11_EXCLUDING_COMPACT_GRAPHICS',
         'request': 'HUD나 정지 같은 스프라이트 이미지는 제외하고 그 외 텍스트 확대 가능성 확인 후 진행',
         'baseline': 'opening11_poc_055', 'baseline_sha256': sha(R / 'build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes'),
         'CSV_sha256': sha(R / 'workspace/translation/text_ja.csv'), 'registered_main_drafts': 45,
         'targets': targets, 'opening_verified': 9, 'ordinary_remaining': 33, 'credits_remaining': 3,
         'excluded_compact_graphics': ['HUD labels/numerals', 'fixed and moving STOP sign', 'sprite notices',
                                       'baked title/map/booth-board/results/gameover/sign art'],
         'excluded_original_retention': ['HOWTO', 'PAUSE', 'POW', 'RYO51', 'NT1C', 'DIAGNOSTIC_STAGE_SELECT'],
         'next_group': 'home_booth_lower: twelve entries, 168px wide, at most two16px lines',
         'critical_conditions': ['Skip-button instantaneous925E and progressive93E1 must both understand paired rows',
                                 'Keep booth possession refresh from changing the live lower font (050 fix)',
                                 'Shared card font193 exceeds128; use per-consumer font residency',
                                 'F8 digit combination union175 needs isolated numeral slots',
                                 'CreditsFC scroll and staff/legal rows need separate renderer/lifetime proof'],
         'new_ROM_or_runtime': False, 'global_inventory_complete': False,
         'automatic_play': 'No new controller or full-play experiment; user owns gameplay review'}
    assert len(rows) == 54 and len(targets) == 45
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = '''사용자는 HUD·정지 표지판 같은 작은 그림 글자는 유지하고, 그 외 텍스트를 확대할 수 있는지 확인한 뒤 진행하도록 요청했다. [대상·제약 원장](../qa/reports/text11_197_scope.json)을 만들었다. 기존 번역 CSV의45개 초안은 오프닝9개(055 실제 검증), 일반 대사·홈 선택명·놀이기구 안내33개, 크레딧3개로 나뉜다. 이 수량은 등록된 원천의 범위이며 전게임 인벤토리 완결 주장은 아니다.

이번 확대 대상은 문자열 출력기로 표시하는 대사·선택명·놀이기구 안내·크레딧이다. HUD/정지/공지 스프라이트 및 기존 타이틀·지도·매표소 상태판·결과·게임오버·간판 그림은 현재 크기를 유지한다. 원문 유지6건도 그대로다. 그림 안의 메뉴 글자까지 이번 문자열 전환에 포함했다고 주장하지 않는다.

오프닝055의11px 방식은 일반 대사로 확장 가능하다. 홈·매표소는168px/최대2줄에 맞추고, 점진 출력과 버튼 건너뛰기의 즉시 출력925E를 함께 구현해야 한다. 기존050의 매표소 숫자 갱신 시 하단 글꼴 보존도 유지한다. 상단 안내 공유 글꼴193은267타일로128슬롯을 초과하므로 문단별 전환이 필요하다. 보유 티켓 F8의175타일 조합 수요는 숫자 전용 슬롯으로 분리할 수 있는지 검증한다. 크레딧은 스크롤과 제작진/법적 문구 보존을 별도 검증해야 한다.

변경은 스크립트·정적 범위 원장·문서뿐이다. ROM/CSV/원본/1편/사용자Mesen·세이브는 보존했다. 신규 빌드·패치 적용·에뮬레이터·직접 장면 검증은 이 작업에서 수행하지 않았다. 사용자 담당 실제 플레이를 자동 실험으로 대체하지 않는다. 재현 스크립트는 이미 고정된 출력 경로를 덮어쓰지 않는다. 변경 파일/해시는 [197매니페스트](../manifests/nonplay197_assets.json)에 기록한다.'''
    records.seal(197, 'TEXT11_SCRIPT_SCOPE_AND_FEASIBILITY_197.md', '그림 글자 제외·문자열11px 확대 범위와 제약', body,
                 '사용자 범위를 문자열 출력기로 고정. 오프닝9/일반33/크레딧3 구분. HUD·정지 등 그림 유지, 다음 홈·매표소12개.',
                 '055를 기준으로 홈·매표소12개에11px 점진/즉시 출력을 적용하고 최종6502와 독립 재빌드를 검증한다.',
                 [Path(__file__), p, R / 'qa/reports/text11_190_plan.json'])
    f = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    s = f.read_text('utf-8').replace('현재 개발049 / 작업197', '기준051 / 오프닝055 / 문자열11px 확장 / 작업197', 1)
    f.write_text(s, 'utf-8')
    print(json.dumps({'status': d['status'], 'ordinary_remaining': 33, 'credits_remaining': 3}, indent=2))


if __name__ == '__main__':
    main()
