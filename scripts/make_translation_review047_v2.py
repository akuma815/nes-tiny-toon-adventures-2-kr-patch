"""Work92 current047 ROM-free review kit; update the one SSOT sentence explicitly."""
from pathlib import Path
import json,csv,html,base64,re,zipfile,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=R/'workspace/review/translation046_20261005';out=R/'workspace/review/translation047_20261005';assert not out.exists();x=json.loads((old/'review_records.json').read_text('utf-8'));assert(len(x['units']),len(x['graphics']),len(x['actual_images']))==(54,33,13)
 ssot=R/'workspace/translation/text_ja.csv';by={z['entry_id']:z for z in csv.DictReader(ssot.open(encoding='utf-8-sig'))};changed=[];source=(old/'review.html').read_text('utf-8')
 for z in x['units']:
  current=by[z['entry_id']];assert z['status']==current['status'] and z['source_tokens']==current['source_tokens']
  if z['translation_ko']!=current['translation_ko']:
   assert z['entry_id']=='MAIN_057C1';needle=html.escape(z['translation_ko'].replace('\\n','\n'));replacement=html.escape(current['translation_ko'].replace('\\n','\n'));assert source.count(needle)==1;source=source.replace(needle,replacement);changed.append(z['entry_id'])
   oldnote=html.escape(z['notes']);newnote=html.escape(current['notes']);match=re.search(r'<details class="unit" id="MAIN_057C1">.*?<details>',source,re.S);assert match and match.group(0).count(oldnote)==1;head=match.group(0).replace(oldnote,newnote);source=source[:match.start()]+head+source[match.end():];z['notes']=current['notes']
  z['translation_ko']=current['translation_ko'];z['notes_scope']='Frozen insertion notes; current047 adoption and runtime scope in work90/91'
 assert changed==['MAIN_057C1']
 x['ROM_build']='dialogue_kr_poc_047';x['ROM_sha256']=sha(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes');x['SSOT_sha256']=sha(ssot);x['human_review_complete']=False
 for z in x['graphics']:assert sha(R/z['plan'])==z['plan_sha256']
 for z in x['actual_images']:
  assert sha(R/z['path'])==z['sha256'];z['evidence_scope']='Historical actual '+z['ROM_build']+' PNG. Preserved source artwork outside057C1/private175176 is byte exact in047; this is not a newly executed047 scene.'
 p=R/'qa/dialogue/gate091_castle047/frame_01920.png';e=json.loads((p.parent/'environment.json').read_text('utf-8'));assert sha(p)==e['files'][p.name]and e['rom_sha256']==x['ROM_sha256']
 x['actual_images'].append({'label':'성 입구 조건 — 현재047 수정 문장','path':p.relative_to(R).as_posix(),'sha256':sha(p),'type':'Actual native emulator PNG','ROM_build':x['ROM_build'],'ROM_sha256':x['ROM_sha256'],'intervention':e['intervention'],'evidence_scope':'Current047 actual native zero-gold route, complete text. Work91 paired046/047 runtime and native RGB reconstruction passed; not a natural earned-gold4 route.'})
 x['limits']=['Final human wording/terminology/artwork review pending; no automatic approval','Registered54units and33graphics are a bounded inventory, not whole-game percentage/global corpus closure','Gallery explicitly labels historical043/045/046 and current047 images; old057C1 wording is replaced only in current unit','Natural cart first segment cleared but second final2F times out; wholeplay/allbranches/physicalconsole/PCM listening not complete','046 reset/savestate verification belongs to that build; no fresh047 state/reset claim','POW/HOWTOCONTROL/PAUSE source candidates were not globally proved unused or approved for preservation','No final release or Cafe article; review archive contains no ROM/font/emulator']
 x['technical_reports']['gate090_validation.json']=sha(R/'qa/reports/gate090_validation.json');x['technical_reports']['gate091_validation.json']=sha(R/'qa/reports/gate091_validation.json')
 source=source.replace('046 사람 검토자료','047 사람 검토자료').replace('검토자료046','검토자료047').replace('현재046에는','현재047에는')
 source=source.replace('아래043/045 화면은 해당 빌드의 과거 실제 증거이며046에서 재촬영했다고 주장하지 않습니다.','아래043/045/046 화면은 해당 빌드의 과거 실제 증거입니다. 마지막 성 입구 사진은047에서 새로 실행한 실제 화면입니다. 성 입구 한 문장을 원문 문맥에 맞게 다듬었으며 전체 게임의 완주나 최종 사람 승인을 의미하지 않습니다.')
 gallery='<div class="gallery">'
 for z in x['actual_images']:
  encoded=base64.b64encode((R/z['path']).read_bytes()).decode();gallery+=f'<figure><img alt="{html.escape(z["label"])}" src="data:image/png;base64,{encoded}"><figcaption>{html.escape(z["label"])} · 실제 {html.escape(z["ROM_build"])}<br>{html.escape(z["evidence_scope"])}<br>{html.escape(z["path"])}</figcaption></figure>'
 gallery+='</div>';source,n=re.subn(r'<div class="gallery">.*?</div>',lambda _:gallery,source,count=1,flags=re.S);assert n==1
 assert '골드 티켓 4장이 있으면\n입장할 수 있어요'in source and '입장 조건은 골드 티켓 4장'not in source
 out.mkdir();(out/'review.html').write_text(source,'utf-8');(out/'review_records.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')
 pending=(old/'DECISIONS_PENDING.md').read_text('utf-8').replace('현재046','현재047').replace('043·045과거화면과046현재표본','043·045·046과거화면과047현재성입구표본');pending+='\n성 입구 MAIN_057C1은 작업90의 한 문장 수정과91 실제 출력검증을 반영했다. 기존046 검토자료와 별개로 현재047 문구를 검토한다. 최종사람검토 상태는 여전히 미완료다.\n';(out/'DECISIONS_PENDING.md').write_text(pending,'utf-8')
 (out/'README.txt').write_text('타이니툰2 현재047 사람검토자료\nreview.html: 오프라인PNG14개/본문54단위/그림33문구. 실제043·045·046사진은 역사적자료,047성입구사진은 새실행자료. 한 문장 수정CSV와ROM해시는records에보존. ROM/패치/폰트/에뮬레이터 없는 검토ZIP. 최종승인·카페작업기 아님.\n','utf-8')
 manifest={'work':92,'ROM_build':x['ROM_build'],'ROM_sha256':x['ROM_sha256'],'SSOT_sha256':x['SSOT_sha256'],'ROM_free':True,'human_review_complete':False,'registered_units':54,'graphics':33,'actual_images':14,'changed_unit':['MAIN_057C1'],'files':{p.name:sha(p)for p in sorted(out.iterdir())if p.is_file()}};(out/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')
 archive=R/'workspace/review/TinyToon2_Translation_Review_047_20261005.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for p in sorted(out.iterdir()):z.write(p,(Path(out.name)/p.name).as_posix())
 with zipfile.ZipFile(archive)as z:
  assert z.testzip()is None and len(z.namelist())==5
  for p in out.iterdir():assert z.read((Path(out.name)/p.name).as_posix())==p.read_bytes()
 result={'work':92,'status':'PASS_RECORDS_INLINE_ROMFREE_ZIP','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'registered_units':54,'graphics':33,'actual_images':14,'ROM_free':True,'ROM_sha256':x['ROM_sha256'],'SSOT_sha256':x['SSOT_sha256'],'changed_units':changed,'all_source_records_and_images_hash_verified':True,'human_review_complete':False,'render':'pending separatebrowser check','scope':'Private review only; explicit scene-build provenance; no Cafe/posting/final-release claim'}
 p=R/'qa/reports/review047_records.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()