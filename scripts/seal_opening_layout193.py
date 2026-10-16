"""Seal user-directed page6 layout build; runtime remains a separate194 record."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R,sha

def main():
    records.DATE='2026-10-09';p=R/'build/opening11_poc_055';q=R/'build/opening11_193_rebuild055';v=json.loads((p/'build_report.json').read_text('utf-8'))
    for n in ('TinyToon2_Opening11_PoC055.nes','TinyToon2_Opening11_PoC055.ips'):assert (p/n).read_bytes()==(q/n).read_bytes()
    body=f'''사용자문단6배치수정요청을053기반의새 **오프닝PoC055**로반영했다. [레이아웃입력](../workspace/translation/opening_layout_override193.json), [055ROM](../build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes) SHA `{v['output_sha256']}`, [IPS](../build/opening11_poc_055/TinyToon2_Opening11_PoC055.ips) SHA `{v['IPS_sha256']}`. 054홈후보는포함하지않았다.

6문단1행‘친구들도데려와!’,2행‘깜짝놀랄거다!’,3행빈줄,4행‘의문의대부호로부터’를한줄오른쪽정렬했다. CSV의띄어쓰기/어휘를정규화해모든단어동일검사 PASS. 갈무리11은동일하며폰트파일SHA `{v['font_sha256']}`. 서명셀끝은192px우측경계,시작72px; 앞두줄42px센터다. 빈줄은서명분리용이다. 마지막실획은셀오른쪽보다1px안쪽일수있으므로셀정렬과잉크끝을혼동하지않는다.

정적/빌드: immutable원본ExpectedWrite기대값·중첩·전체모델/허용최종diff/실제IPS적용/독립ROM·IPS재빌드 exact PASS. 053대비508바이트로6문단private본문타일코드196바이트와font140/141의2KiB범위안에서만변경. 본문길이196/FEFF위치/출력100단위/8×8상하페어·행간/원래대기제어유지,코드/fixedIRQ/다른8문단폰트/stream은동일하다. [055배치](../build/opening11_poc_055/opening11_plan.json), [9문단최종CPU](../qa/reports/opening_layout193_cpu.json). CPU상하NT/복귀/스택/terminator PASS이며NMI/IRQ실소비증거는아니다.

실제Mesen/직접시각은194로분리한다. build_report의runtime=PENDING은작성시점기록이며새결과는원보고를덮어쓰지않는다. 기준051/053패키지/054후보/원본/1편/CSV/사용자Mesen·세이브보존. CSV SHA `{v['CSV_sha256']}`,원본SHA `{v['source_sha256']}`. 글로벌폰트/다른문단최종승인으로확대하지않는다. 원문유지6건및타이틀/간판그림변경없음. 전체11px·전체플레이·최종미감·하드웨어/오디오/세이브호환미완료. 카페완성작업기/외부게시없음.

변경파일전체해시는 [193매니페스트](../manifests/nonplay193_assets.json). 재현: `python scripts/build_opening_layout193.py --output build/<new-directory>`. 기존출력은거부한다. 원문문장을변경한일괄치환이아니라사용자지정1문단배치입력만소비한다.'''
    records.seal(193,'OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md','오프닝6문단 줄바꿈·서명우측정렬 PoC055',body,'사용자지정문단6배치반영055.053대비508바이트/코드·제어위치·다른8문단불변.원본/IPS/독립ROM·최종CPU PASS;실제194분리.', '055오프닝9문단반복/6문단RGB와서명우측정렬·소거를실제Mesen자료로검증한다.',[Path(__file__),R/'scripts/build_opening_layout193.py',R/'workspace/translation/opening_layout_override193.json',R/'qa/reports/opening_layout193_cpu.json',*[x for d in (p,q) for x in d.iterdir() if x.is_file()]])
    f=R/'docs/LOCALIZATION_WORK_PLAN.md';s=f.read_text('utf-8').replace('현재 개발049 / 작업193','기준051 / 053검증본 / 055문단6배치후보 / 작업193',1);f.write_text(s,'utf-8')

if __name__=='__main__':main()
