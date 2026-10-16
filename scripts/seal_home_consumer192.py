"""Separate actual text-consumer bank from EndFrame and record requested layout6."""
from pathlib import Path
import csv,json
import seal_nonplay171 as records
from seal_nonplay171 import R,sha

def main():
    records.DATE='2026-10-09'
    log=R/'qa/dialogue/train142_native_049/prg_text_reads.csv';rows=[x for x in csv.DictReader(log.open()) if x['pointer']=='9731'];assert rows and all(int(x['PRG_relative_offset'],16)//8192==18 for x in rows)
    a=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes();b=(R/'build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes').read_bytes();ranges=[[0x253ed,0x2541e],[0x25c91,0x25c97],[0x25741,0x2574d]]
    assert all(a[lo:hi]==b[lo:hi] for lo,hi in ranges)
    report=R/'qa/reports/home11_192_consumer_and_layout_choice.json';assert not report.exists()
    report.write_text(json.dumps({'work':192,'status':'HOME_CANONICAL18_DATA_CONSUMPTION_SUPPORTED_END_FRAME_NOT_EXEC_BANK','prior049_reader_24_events':rows,'prior049_to053_relevant_reader_call_body_ranges_equal':ranges,'EndFrame053_lowPRG22_is_not_dialogue_bank_inference':True,'home054':'CPU-only candidate, runtime pending; not rejected merely from endFrame mapping; no font/layout adoption','user_choice':{'current053_as_global_font_layout_baseline':'Adjustment requested','specific_request':'Page6: move 깜짝 놀랄 onto same following line with 거다; 의문의 대부호로부터 right aligned','implemented_now':False},'new_runtime':False},ensure_ascii=False,indent=2)+'\n','utf-8')
    body='''홈054의새실행없이기존실행근거를추가확인했다. [24개actual읽기/범위동등성](../qa/reports/home11_192_consumer_and_layout_choice.json). 과거049의pointer9731 읽기는physicalPRG18에서CPU9395로소비됐고관련reader/9C81호출/9731본문은현재053과같다. 053의EndFrame22/23매핑을실행중대사뱅크로간주할수없다. [기존홈수명문서](POC_DIALOGUE_HOME.md)도프레임끝6/7과실제2/3의차이를명시했다. 현재확대ROM의logicalbank32/33은physical18/19이며원래logical2는별도폰트helper다. 그래서‘054가홈호출에연결되지않았다’는중간설명은정정한다. 054는CPU후보이며실제054소비성공은여전히미검증이다.

사용자가053의폰트·줄바꿈을그대로전체기준에쓰는선택을거부하고구체적으로‘문단6 깜짝놀랄부분을거다와합쳐서아래줄, 의문의대부호로부터오른쪽정렬’을요청했다. 다음작업은이구체레이아웃이다. 현재갈무리11폰트파일을유지하면서1행‘친구들도데려와!’,2행‘깜짝놀랄거다!’,3행빈줄,4행서명한줄오른쪽으로구성한다. 이는원래문구를변경하는일괄변환이아니라사용자지정문단의배치다. 전체폰트/다른문단의사람최종승인으로확대하지않는다.

원본/051/053/054/CSV/사용자Mesen·세이브보존. 새ROM/에뮬레이터/자동플레이/054채택·패키지없음. [192매니페스트](../manifests/nonplay192_assets.json)에파일해시를기록했다. 이작업은기존로그와바이트동등성의정적감사이며새실행결과가아니다. 카페완성작업기/외부게시없음.'''
    records.seal(192,'HOME11_CONSUMER_AND_PAGE6_LAYOUT_CHOICE_192.md','홈실행뱅크 판정정정·오프닝6문단 조정요청',body,'기존049읽기와053동등범위로physical18홈소비연결.054실제미검증유지.사용자문단6줄바꿈/서명오른쪽정렬을다음작업으로전환.', '053기반으로문단6만사용자지정줄바꿈·서명오른쪽정렬한새오프닝PoC를만든다.',[Path(__file__),report,log,R/'docs/POC_DIALOGUE_HOME.md',R/'qa/reports/text11_190_audit.json',R/'qa/reports/home11_191_audit.json'])
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';s=p.read_text('utf-8').replace('현재 개발049 / 작업192','기준051 / 오프닝053 / 홈054미실행 / 문단6수정요청192',1);p.write_text(s,'utf-8')

if __name__=='__main__':main()
