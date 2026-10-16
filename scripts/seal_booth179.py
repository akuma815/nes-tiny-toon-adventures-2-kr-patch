"""Final current050 handoff reconciliation; no new game/build/apply run."""
from pathlib import Path
import json
from seal_nonplay171 import R,sha,seal

def main():
    reports=[R/f'qa/reports/issue{n}_session.json' for n in [177,178]]
    for p in reports:
        d=json.loads(p.read_text('utf-8'));assert d['status']=='PASS_PROJECT_ASSETS_SOURCE_AND_LOCAL_LINKS' and d['adopted_ROM_build']=='dialogue_kr_poc_050'
    package=R/'dist/TinyToonAdventures2_KR_Review_050_BoothFix_20261008.zip';proof=R/'qa/reports/issue178_package.json';d=json.loads(proof.read_text('utf-8'));assert sha(package)==d['archive_sha256']
    body=f'''사용자신고176→수정/집중실행177→패키지178의현재기준을050으로대조했다. [수정/회귀](BOOTH_EXCHANGE_FONT_FIX_050_177.md), [적용/인계](BOOTH_FIX050_APPLY_PACKAGE_178.md), [050 ZIP](../dist/{package.name}). ZIP SHA `{sha(package)}`, ROM SHA `{d['ROM_sha256']}`. [177 감사](../qa/reports/issue177_session.json)는13,514원천/빌드/실행파일해시를확인했고 [178 감사](../qa/reports/issue178_session.json)는35개패키지/적용자산을확인했다. 원본/1편참조와프로젝트로컬2375링크PASS. 외부과거plugin3.3캐시링크하나의만료는별도표시했고프로젝트자산/현재3.4와혼동하지않는다.

현재README/canonical/datedhand/journal/SURVEY/PLAN은수정본050과ROM없는패키지178을가리킨다. 번호별049자료는역사로보존하며173/175의검수이미지를050전장면검증으로표현하지않는다. 새사용자결정은추가하지않고원문유지6건을그대로적용했다. CSV와CHR불변이다.053,760 CPU사례/독립ROM·IPS재빌드/집중네분기paired1116시점/실Windows8+최종ZIP적용은각기존177/178보고이며이작업에서게임/빌드/적용을반복하지않았다. `untranslated:9` 빌드보고필드의역사명은9기술공유단위이며새미번역산문9개를뜻하지않는다.

사용자검수: 새050 ROM을열고초기화후매표소에재진입해티켓교환대사를확인한다. 이미깨진049강제저장상태의자동복구는보장하지않는다. 기존사용자Mesen에는입력/리셋/로드/교체/종료하지않았다.176에서computer pipe미연결로현재live화면/메모리는직접읽지못했고사용자스크린샷·같은host의복사상태로재현했다. 그뒤coldboot/native콜러의같은입력실행으로원인과수정을검증했다. 전체플레이/최종문구·명칭·그림승인/전역원천완결/원문유지6건소비확정은여전히미완료다. 카페완성작업기/외부게시없음.

변경파일: 새감사helper/이최종seal·179인계/manifest·current문서. 재현명령은177의runner/seed를따르고, 적용은ZIP README/apply.cmd를따른다. 감사: `python scripts/audit_project_links179.py --manifest manifests/nonplay179_assets.json --output qa/reports/issue179_session.json` (기존출력보호).'''.replace('053,760','53,760')
    seal(179,'BOOTH_FIX050_FINAL_RECONCILIATION_179.md','티켓교환 수정050 최종 인계·자산감사',body,'050수정/178ZIP/current인계 대조 완료.177의13,514자산·178의35자산/원본·1편/로컬링크PASS. 실제전체플레이/최종사람검수는사용자담당.','사용자가 새050 ROM을 열고 초기화/매표소 재진입 후 티켓 교환 대사를 검수한다.',[Path(__file__),R/'scripts/audit_project_links179.py',*reports,R/'manifests/nonplay177_assets.json',R/'manifests/nonplay178_assets.json',proof,package,R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv'])
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업179','현재 개발050 / 작업179',1);p.write_text(s,'utf-8')
    p=R/'README.md';s=p.read_text('utf-8').replace('작업178 완료 / 티켓교환','작업179 완료 / 티켓교환',1).replace('현재 개발본 — 작업178 / 050','현재 개발본 — 작업179 / 050',1);p.write_text(s,'utf-8')
    print('PASS final050 handoff179')
if __name__=='__main__':main()
