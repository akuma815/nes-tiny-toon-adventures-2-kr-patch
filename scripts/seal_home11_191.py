"""Record home054 candidate and source/staticCPU proof; actual runtime is not claimed."""
from pathlib import Path
import json,re
import seal_nonplay171 as records
from seal_nonplay171 import R,sha

def main():
    records.DATE='2026-10-09'
    candidate=R/'build/home11_candidate_054';rebuild=R/'build/home11_191_rebuild054';report=json.loads((candidate/'build_report.json').read_text('utf-8'));cpu=R/'qa/reports/home11_cpu191.json';assert json.loads(cpu.read_text('utf-8'))['status']=='PASS_STATIC_CPU_HOME054_AND_OPENING9'
    for n in ('TinyToon2_Home11_Candidate054.nes','TinyToon2_Home11_Candidate054.ips'):assert (candidate/n).read_bytes()==(rebuild/n).read_bytes()
    proof=R/'qa/reports/home11_191_development.json';assert not proof.exists()
    proof.write_text(json.dumps({'work':191,'status':'PASS_SOURCE_COMPOSED_CPU_AND_INDEPENDENT_REBUILD_ONLY','ROM_sha256':report['output_sha256'],'IPS_sha256':report['IPS_sha256'],'independent_ROM_IPS_equal':True,'native_home_root':8,'native_clear_origin':0x22a7,'native_clear_width':22,'native_clear_rows':5,'native_text_origin':0x22a8,'safe_text_tile_columns_inside_clear':21,'safe_width_pixels':168,'prior_actual_home_RAM_PPU_mapping':'qa/dialogue/opening11_187_train053/frame_00930','border_tile_codes_all_outside_newfont128_slot_range':True,'attempts':[{'script':'build_home11_191.py','result':'Pre-output assertion failure: privatePRG8 CPU9C81 lies in openingstream data, not cloned native JSR93E1','resolution':'v2 changes canonical18 callsite only; bank8 only holds wrapper/printer/body. All nine opening streams stay exact. No ROM emitted by failed attempt.'}],'new_emulator_execution':False,'actual054_scene_clear_residency_NMI_IRQ':'NOT_RUN','candidate_not_adopted_or_packaged':True},indent=2)+'\n','utf-8')
    body=f'''전체11px계획190의다음대표로홈MAIN_05741/native0A ‘자, 어디로 갈까?’만추가한 **054개발후보**를만들었다. 기준051과검증·패키지완료053을대체하지않는다. [054ROM](../build/home11_candidate_054/TinyToon2_Home11_Candidate054.nes) SHA `{report['output_sha256']}`, [IPS](../build/home11_candidate_054/TinyToon2_Home11_Candidate054.ips) SHA `{report['IPS_sha256']}`, [배치/ASM](../build/home11_candidate_054/home11_plan.json), [최종CPU](../qa/reports/home11_cpu191.json), [시행착오/범위](../qa/reports/home11_191_development.json).

정적근거: 기존053의실제frame00930 RAM에서홈root8/font130/pointer9731을확인했다. 홈root1가정은사용하지않았다. 같은PPU/매핑에서창테두리는C7..EB코드로128슬롯새폰트밖에있고관련CHR는보존한다. source6502의920A는clear22A7·폭22타일·5행,9417mode1의text원점22A8이다. 오른쪽끝clear경계를넘지않는최대21타일=168px를선택했다. 190의192px는일반문단수요검사용이며홈창에그대로채택하지않았다.

구현: 홈root8/native0A/font130/pointer9731에만9630의전용조건래퍼를적용한다. 9C81부모호출은canonical18에만변경,bank8은래퍼/프린터/본문만소비한다. private8의9C81은이미오프닝stream으로사용중이어서v1의복제callsite가정이출력전에거부됐고v2로수정했다. 실패v1과원래053을보존했다. 9630은053에서대체된오프닝raw본문영역을재사용하므로이경로외전역도달성은여전히미확정이다. 일반다른root/ID/font/pointer는native93E1로fallback한다. 이래퍼추가시간은기존과동일하다고주장하지않는다.

빌드/적용: immutable일본판의기존ExpectedWrite를최종054바이트로재구성해중첩/기대원본/전체모델/diff범위/실제IPS적용 exact PASS. 독립ROM/IPS재빌드 exact PASS. 053대비1044바이트,기존9오프닝폰트/stream/호출부와헤더/fixedIRQ는그대로다. 이는실행시간불변이나runtime전이를보장하는근거가아니다. 원본SHA `{report['source_sha256']}`,CSV SHA `{report['CSV_sha256']}` 불변.

CPU: 실제최종6502래퍼의22호출·42상하타일NT좌표·PRG18/19복귀·tag32·스택/FEFF 제어 PASS. 기존5회지우기의110셀안에새글자42셀이전부포함된다. 오프닝9문단최종CPU출력도동일,비대상fallback의778조건에서레지스터/게임RAM/큐/뱅크동일 PASS. 부모는출력뒤carry로대기/다음단계를선택하며변경된타일코드는새본문의의도된값이다.

에뮬레이터/직접장면: **054새실행없음**. 현재053자료는root/geometry의근거이며054의11px표시성공으로승계하지않는다. 실제054전송의NMI/IRQ예산·창안배치·출력도중/대기/5행소거·선택지전환·폰트130수명·오프닝회귀는아직검증하지않았다. 사용자실제플레이담당지시에따라새자동플레이/컨트롤러실험을진행하지않았다. 054미채택/미패키지,전체11px/최종폰트/오디오·하드웨어·세이브호환/전역미사용미확정이다.

변경파일전체SHA는 [191매니페스트](../manifests/nonplay191_assets.json). 190정적42PNG/공유font193(267타일)·196(238타일)초과와숫자조건계획은그대로다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT와타이틀/간판그림변경없음. 카페완성작업기/게시없음.

재현: `python scripts/build_home11_191_v2.py --output build/<new-directory>`를새빈출력경로에서사용한다. CPU검사기는현재054를고정대상으로읽고기존보고덮어쓰기를거부한다. 폴더/결과경로를새로정한복제에서재현한다. 사용자검수는새054ROM을열어초기화하고게임시작직후홈의‘자, 어디로 갈까?’와선택지전환을확인하는방법이며이를실시했다고기록하지않는다.'''
    next_action='054홈한줄의실제표시·상하타일소비·대기/지우기·선택지전환과오프닝회귀근거를확보한후 홈·매표소12문단확대로진행한다.'
    files=[Path(__file__),R/'scripts/build_home11_191.py',R/'scripts/build_home11_191_v2.py',R/'scripts/verify_home11_cpu191.py',proof,cpu,R/'qa/dialogue/opening11_187_train053/frame_00930_ram.bin',R/'qa/dialogue/opening11_187_train053/frame_00930_ppu.bin',R/'qa/dialogue/opening11_187_train053/frame_00930_mapping.csv',R/'qa/dialogue/opening11_187_train053/frame_00930.png',*[p for d in (candidate,rebuild) for p in d.iterdir() if p.is_file()]]
    records.seal(191,'HOME11_SINGLE_LINE_CANDIDATE054_191.md','홈한줄11px 후보054·원본빌드·CPU 검증',body,'홈root8/168px/5행소거경계로054한줄후보제작.ROM/IPS독립동일·42상하/110소거·778fallbackCPU PASS.054실제실행미수행·미채택.',next_action,files)
    p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');s=s.replace('053패키지188·감사189·전체11px출력기계획190을완료했다. [다음UI계획190](GLOBAL_TEXT11_NEXT_CONSUMER_PLAN_190.md)의홈한줄MAIN_05741을다음대표로삼는다.','053패키지188·감사189·전체11px계획190과 [홈한줄054후보191](HOME11_SINGLE_LINE_CANDIDATE054_191.md)를완료했다. 054는정적/빌드/CPU만PASS이고실제실행미수행·미채택이다. 검수용확정패키지는오프닝053이다.',1);p.write_text(s,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업191','기준051 / 오프닝053패키지 / 홈054미실행후보 / 작업191',1);p.write_text(s,'utf-8')
    p=R/'README.md';s=p.read_text('utf-8');s=re.sub(r'^> \*\*.*?\*\*[^\n]*','> **2026-10-09 작업191 / 기준051 유지 / 오프닝11px PoC053 패키지완료 / 홈054는CPU검증후보·실행미수행** [최신 인계](docs/HANDOFF.md)',s,count=1,flags=re.M);p.write_text(s,'utf-8')

if __name__=='__main__':main()
